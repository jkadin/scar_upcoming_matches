from django.core.management.base import BaseCommand
import challonge
import os
from fights.models import Url, Tournament, Match, Bot
# from itertools import chain, zip_longest
from dotenv import load_dotenv
from preferences import preferences
# from math import gcd
# from functools import reduce

# Read interleave method lazily to avoid DB access at import time
load_dotenv()


class Command(BaseCommand):
    help = "Updates the data from the API"

    def handle(self, *args, **options):
        update_database()

        self.stdout.write(self.style.SUCCESS("Successfully updated data"))


def update_database():
    challonge.set_credentials(
        os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_API_KEY")
    )
    challonge_tournament_list = get_tournament_list_from_challonge()
    process_tournaments(challonge_tournament_list)
    load_all_bots()

    load_matches_from_challonge(challonge_tournament_list)

    # assign calculated_play_order
    needs_interleave = Tournament.objects.filter(tournament_needs_interleave=True)
    interleave_method = preferences.MyPreferences.interleave_method  # type: ignore
    if not needs_interleave and "Fixed" in interleave_method:
        return
    interleave()
    # interleaved = zip_longest(*interleaved_matches)
    # list_of_tuples = chain.from_iterable(interleaved)
    # remove_fill(interleaved_matches)


def interleave()->None:
    # Pop different amounts based on flag and calculations
    matches_list:list[list[Match]] = []
    for tournament in Tournament.objects.all():
        tournament.tournament_needs_interleave = False
        tournament.save()
        matches_list.append(
            list(
                Match.objects.filter(
                    tournament_id=tournament, 
                ).order_by("suggested_play_order")
            )
        )

    adjustments=even_distribution(matches_list)
    for i, m in enumerate(adjustments):
        m.calculated_play_order = i + 1
        m.save()
    # if INTERLEAVE_METHOD in ('Fixed_multiple','Interleave_multiple'):
    #     interleaved_matches:list[Match]=[] #new list to replace remove_fill
    #     while any(matches_list):
    #         for i,tournament in enumerate(matches_list):
    #             for _ in range(adjustments[i]):
    #                 try:
    #                     interleaved_matches.append(tournament.pop(0))
    #                 except IndexError:
    #                     continue


def even_distribution(groups:list[list[Match]]) ->list[Match]:
    remaining = [list(g) for g in groups]
    pattern = []

    # Sort group indices by length (ascending)
    sorted_indices = sorted(range(len(groups)), key=lambda i: len(groups[i]))

    while any(remaining):
        # Find the smallest remaining group
        min_group_idx = min(
            (i for i in range(len(remaining)) if remaining[i]),
            key=lambda i: len(remaining[i]),
        )
        # Always take 1 from the smallest group
        pattern.append(remaining[min_group_idx].pop(0))

        # Take proportional items from other groups
        for i in sorted_indices:
            if i == min_group_idx or not remaining[i]:
                continue
            # Determine proportion relative to the smallest group
            proportion = len(groups[i]) // max(len(groups[min_group_idx]), 1)
            take = min(proportion, len(remaining[i]))
            if preferences.MyPreferences.interleave_method in ("Fixed","Interleave"):
                take=1
            for _ in range(take):
                pattern.append(remaining[i].pop(0))

    return pattern


# def remove_fill(list_of_matches:list[Match])->None:
#     for i, m in enumerate(list_of_matches):
#         m.calculated_play_order = i + 1
#         m.save()


def load_matches_from_challonge(challonge_tournament_list):
    for t in challonge_tournament_list:
        t1 = Tournament(t.get("id"), t.get("name"), t.get("state"), t.get("url"))
        challonge_matches: list = challonge.matches.index(t1.tournament_id)  # type: ignore
        update_or_create_matches(t1, challonge_matches)


def process_tournaments(challonge_tournament_list:list):
    for t in challonge_tournament_list:
        t_state = t.get("state")
        url=Url.objects.get(url=t.get("url"))
        try:
            t_old_state = Tournament.objects.get(tournament_id=t.get('id')).tournament_state
        except Tournament.DoesNotExist:
            t_old_state = None
        t1,created=Tournament.objects.update_or_create(
            tournament_id=t.get('id'),
            defaults={"tournament_name": t.get("name"),
            "tournament_state": t_state,
            "tournament_url": url,
            },
        )
        if (t_state == 'underway' and (t_old_state != t_state)):
            t1.tournament_needs_interleave=True
            t1.save()
        if (t_state == 'pending' and (t_old_state != t_state)):
            t1.match_set.all().delete()


def load_all_bots():
    for t1 in Tournament.objects.all():
        load_bots_from_challonge(t1)
        create_null_bot(t1)


def update_or_create_matches(t1: Tournament, challonge_matches: list):
    for challonge_match in challonge_matches:
        bot_id = challonge_match.get("player1_id")
        player1_id = Bot.objects.get(bot_id=bot_id, tournament_id=t1)
        player2_id = Bot.objects.get(
            bot_id=challonge_match.get("player2_id"), tournament_id=t1
        )

        Match.objects.update_or_create(
            match_id=challonge_match.get("id"),
            defaults={
                "player1_id": player1_id,
                "player2_id": player2_id,
                "tournament_id": t1,
                "match_state": challonge_match.get("state"),
                "updated_at": challonge_match.get("updated_at"),
                "suggested_play_order": challonge_match.get("suggested_play_order"),
                "estimated_start_time": None,
                "started_at": challonge_match.get("started_at"),
                "underway_at": challonge_match.get("underway_at"),
                "player1_is_prereq_match_loser": challonge_match.get(
                    "player1_is_prereq_match_loser"
                ),
                "player2_is_prereq_match_loser": challonge_match.get(
                    "player2_is_prereq_match_loser"
                ),
                "player1_prereq_match_id": challonge_match.get(
                    "player1_prereq_match_id"
                ),
                "player2_prereq_match_id": challonge_match.get(
                    "player2_prereq_match_id"
                ),
            },
        )


def get_tournament_list_from_challonge()->list:
    tournament_list = []
    for tournament_url in Url.objects.all():
        challonge_tournament = challonge.tournaments.show(
            tournament=f"/{tournament_url.url}"
        )
        tournament_list.append(challonge_tournament)
    tournament_list = [t for t in tournament_list ]
    return tournament_list


def load_bots_from_challonge(t1):
    participants = challonge.participants.index(t1.tournament_id)
    for bot in participants:
        bot_name=bot["name"]
        Bot.objects.update_or_create(
            bot_id=bot["id"],  # type: ignore
            tournament_id=t1,
    defaults={'bot_name': bot_name}
        )


def create_null_bot(t1):
    try:
        p1 = Bot.objects.get(bot_id=None, tournament_id=t1)
    except Exception as E:
        p1 = Bot(
            bot_id=None,
            bot_name="Not assigned",
            tournament_id=t1,
        )
        p1.save()
