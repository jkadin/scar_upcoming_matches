from django.shortcuts import render
from .models import Url, Tournament, Match, Participant
import challonge
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from operator import itemgetter
from itertools import chain, zip_longest

load_dotenv()
NEXT_MATCH_START = timedelta(minutes=1)
MATCH_DELAY = timedelta(minutes=3)


def most_recent_match_time(tournament):
    most_recent_match_time = datetime.min
    for m in tournament["matches"]:
        if m["match_state"] != "complete":
            continue
        match_time = m["updated_at"].replace(tzinfo=None)
        if match_time > most_recent_match_time:
            most_recent_match_time = match_time
    return most_recent_match_time


def interleave_matches(tournaments):
    matches_list = [
        t["matches"] for t in sorted(tournaments.values(), key=most_recent_match_time)
    ]
    for i, ml in enumerate(matches_list):
        matches_list[i] = sorted(
            [m for m in ml if m["match_state"] == "open"],
            key=itemgetter("suggested_play_order"),
        )
    interleaved_with_fill = zip_longest(*matches_list)
    list_of_tuples = chain.from_iterable(interleaved_with_fill)
    remove_fill = [x for x in list_of_tuples if x is not None]
    return remove_fill


def update_database():
    challonge.set_credentials(
        os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_API_KEY")
    )
    t = Url.objects.all()
    tournament_list = []
    for tournament_url in t:
        tournament_list.append(
            challonge.tournaments.show(tournament=f"/{tournament_url}")
        )
    for t in tournament_list:
        t1 = Tournament(t.get("id"), t.get("name"), t.get("state"))
        t1.save()
        for match in challonge.matches.index(t1.tournament_id, state="all"):
            m1 = Match(
                player1_id=match.get("player1_id"),
                player2_id=match.get("player2_id"),
                tournament_id=match.get("tournament_id"),
                match_id=match.get("id"),
                match_state=match.get("state"),
                updated_at=match.get("updated_at"),
                suggested_play_order=match.get("suggested_play_order"),
            )
            m1.save()

        for participant in challonge.participants.index(t1.tournament_id):
            p1 = Participant(
                participant.get("id"),
                participant.get("name"),
                participant.get("tournament_id"),
            )
            p1.save()


def output(tournaments, ordered_matches):
    match_start = datetime.now() + NEXT_MATCH_START
    output_match = []
    for i, match in enumerate(ordered_matches[:10]):
        output_match.append(
            {
                "index": i + 1,
                "player1_name": match["player1_name"],
                "player2_name": match["player2_name"],
                "match_start": match_start.strftime("%I:%M %p"),
                "tournament_name": match["tournament_name"],
            }
        )
        match_start += MATCH_DELAY
    return output_match


def get_tournaments():
    tournament_list = Tournament.objects.filter(tournament_state="underway").values()
    tournaments = {t.get("id"): t for t in tournament_list}
    for t in tournaments:
        # Populate matches
        matches = Match.objects.all().values()
        # Populate participants
        participants = Participant.objects.filter(tournament_id=t).values()
        participants = {p["id"]: p for p in participants}
        for y, match in enumerate(matches):
            tournament_name = Tournament.objects.get(
                tournament_id=match.get("tournament_id")
            )
            try:
                matches[y]["player1_name"] = Participant.objects.get(
                    participant_id=match.get("player1_id")
                )
            except:
                matches[y]["player1_name"] = "Unassigned"
            try:
                matches[y]["player2_name"] = Participant.objects.get(
                    participant_id=match.get("player2_id")
                )
            except:
                matches[y]["player2_name"] = "Unassigned"

            matches[y]["tournament_name"] = tournament_name
        tournaments[t]["matches"] = matches
    return tournaments


def index(request):
    t = Url.objects.all()
    if not t:
        return render(
            request,
            "fights/no_tournaments.html",
        )

    tournaments = get_tournaments()
    ordered_matches = interleave_matches(tournaments)
    output_matches = output(tournaments, ordered_matches)

    return render(
        request,
        "fights/index.html",
        {
            "matches": ordered_matches,
            "tournaments": tournaments,
            "output_matches": output_matches,
        },
    )
