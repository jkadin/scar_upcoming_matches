from django.shortcuts import render
from .models import Tournament, Match
from dotenv import load_dotenv
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


def output(tournaments, ordered_matches):
    match_start = datetime.now() + NEXT_MATCH_START
    output_match = []
    for i, match in enumerate(ordered_matches[:5]):
        tournament_name = tournaments[match.get("tournament_id_id")]["tournament_name"]
        output_match.append(
            {
                "index": i + 1,
                "player1_name": match.get("player1_name"),
                "player2_name": match.get("player2_name"),
                "match_start": match_start.strftime("%I:%M %p"),
                "tournament_name": tournament_name,
            }
        )
        match_start += MATCH_DELAY
    return output_match


def get_tournaments():
    tournament_list = Tournament.objects.filter(tournament_state="underway").values()
    tournaments = {t.get("tournament_id"): t for t in tournament_list}
    for t in tournament_list:
        matches = Match.objects.filter(tournament_id=t.get("tournament_id")).values()
        match_list = Match.objects.filter(tournament_id=t.get("tournament_id"))
        for y, match in enumerate(matches):
            matches[y]["player1_name"] = match_list[y].player1_id.participant_name
            matches[y]["player2_name"] = match_list[y].player2_id.participant_name

        tournaments[t.get("tournament_id")]["matches"] = matches
    return tournaments


def index(request):
    tournaments = get_tournaments()
    ordered_matches = interleave_matches(tournaments)
    output_matches = output(tournaments, ordered_matches)

    return render(
        request,
        "fights/index.html",
        {
            "output_matches": output_matches,
        },
    )


def display_matches(request):
    tournaments = get_tournaments()
    ordered_matches = interleave_matches(tournaments)
    output_matches = output(tournaments, ordered_matches)

    return render(
        request,
        "fights/matches.html",
        {
            "output_matches": output_matches,
        },
    )
