from django.core.management.base import BaseCommand
from django.db import IntegrityError, DatabaseError
import challonge
import os
from fights.models import Url, Tournament, Match, Bot
from itertools import chain, zip_longest
from dotenv import load_dotenv

# import pprint

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
    tournament_list = []
    for tournament_url in Url.objects.all():
        tournament_list.append(
            challonge.tournaments.show(tournament=f"/{tournament_url}")
        )
    # Load Tournament and bots first
    for t in tournament_list:
        exists = Tournament.objects.filter(tournament_id=t.get("id"))
        print("state", t.get("state"))
        if t.get("state") != "underway":
            if exists:
                exists.delete()
            continue
        needs_interleave = True
        if exists:
            needs_interleave = False
        t1 = Tournament(
            t.get("id"),
            t.get("name"),
            t.get("state"),
            tournament_url,
            needs_interleave,
        )
        t1.save()
        print(f"{t1.tournament_needs_interleave=}")
        print(f"Tournament_id= - {t1.tournament_id}")
        print("Loading bots")
        load_particpants(t1)
        create_null_particpant(t1)
        print("bot loading complete")

    # remove non-underway tournaments
    tournament_list = [t for t in tournament_list if t.get("state") == "underway"]

    # load matches
    print("Loading Matches")
    for t in tournament_list:
        t1 = Tournament(t.get("id"), t.get("name"), t.get("state"), tournament_url)
        # print(f"{t1.tournament_id=}")
        # pprint.pp(challonge.matches.index(t1.tournament_id))
        for match in challonge.matches.index(t1.tournament_id, state="all"):
            player1_id = Bot.objects.get(
                bot_id=match.get("player1_id"), tournament_id=t1
            )
            player2_id = Bot.objects.get(
                bot_id=match.get("player2_id"), tournament_id=t1
            )
            m1 = Match(
                player1_id=player1_id,
                player2_id=player2_id,
                tournament_id=t1,
                match_id=match.get("id"),
                match_state=match.get("state"),
                updated_at=match.get("updated_at"),
                suggested_play_order=match.get("suggested_play_order"),
                estimated_start_time=None,
                started_at=match.get("started_at"),
                underway_at=match.get("underway_at"),
                player1_is_prereq_match_loser=match.get(
                    "player1_is_prereq_match_loser"
                ),
                player2_is_prereq_match_loser=match.get(
                    "player2_is_prereq_match_loser"
                ),
            )
            try:
                m1.save(
                    update_fields=[
                        "match_state",
                        "updated_at",
                        "started_at",
                        "underway_at",
                        "player1_id",
                        "player2_id",
                        "player1_is_prereq_match_loser",
                        "player2_is_prereq_match_loser",
                    ]
                )
            except DatabaseError:
                try:
                    m1.save()
                except IntegrityError:
                    print("Match already exists")
    # assign calculated_play_order
    print("Check interleave")
    matches_list = []
    needs_interleave = Tournament.objects.filter(tournament_needs_interleave=True)
    if not needs_interleave:
        print("No interleave needed")
        return
    print("Interleave needed")
    for t, tournament in enumerate(Tournament.objects.all()):
        print(tournament.tournament_name)
        tournament.tournament_needs_interleave = False
        tournament.save()
        matches_list.append(
            Match.objects.filter(tournament_id=tournament).order_by(
                "suggested_play_order"
            )
        )
    print(matches_list)
    interleaved = zip_longest(*matches_list)
    print(interleaved)
    list_of_tuples = chain.from_iterable(interleaved)
    print("list of tuples - ", list_of_tuples)
    remove_fill = [x for x in list_of_tuples if x is not None]
    print(remove_fill)
    for i, m in enumerate(remove_fill):
        print(m.tournament_id.tournament_name, m.suggested_play_order)
        m.calculated_play_order = i + 1
        print(m.calculated_play_order)
        m.save()


def load_particpants(t1):
    for bot in challonge.participants.index(t1.tournament_id):
        p1 = Bot(
            bot_id=bot.get("id"),
            bot_name=bot.get("name"),
            tournament_id=t1,
        )
        try:
            p1.save()
        except IntegrityError:
            # print(f"bot {p1} already exists")
            pass


def create_null_particpant(t1):
    try:
        p1 = Bot.objects.get(bot_id=None, tournament_id=t1)
        print(p1)
    except Exception as E:
        print("Exception", E)
        p1 = Bot(
            bot_id=None,
            bot_name="Not assigned",
            tournament_id=t1,
        )
        p1.save()
