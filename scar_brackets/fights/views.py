from django.shortcuts import render
from .models import Match

from datetime import datetime, timedelta


NEXT_MATCH_START = timedelta(minutes=1)
MATCH_DELAY = timedelta(minutes=3)


def most_recent_match_time(tournament):
    most_recent_match_time = datetime.min
    for m in tournament["matches"]:
        if m.match_state != "complete":
            continue
        match_time = m.updated_at.replace(tzinfo=None)
        if match_time > most_recent_match_time:
            most_recent_match_time = match_time
    return most_recent_match_time


def output():
    match_start = datetime.now() + NEXT_MATCH_START
    match_list = Match.objects.filter(match_state="open").order_by(
        "calculated_play_order"
    )
    print(match_list)
    output_match = []
    for i, match in enumerate(match_list[:5]):
        output_match.append(
            {
                "index": i + 1,
                "player1_name": match.player1_id,
                "player2_name": match.player2_id,
                "match_start": match_start.strftime("%I:%M %p"),
                "tournament_name": match.tournament_id.tournament_name,
            }
        )
        match_start += MATCH_DELAY
    return output_match


def index(request):
    output_matches = output()
    return render(
        request,
        "fights/index.html",
        {
            "output_matches": output_matches,
        },
    )


def display_matches(request):
    # tournaments = get_tournaments()
    # ordered_matches = interleave_matches(tournaments)
    output_matches = output()

    return render(
        request,
        "fights/matches.html",
        {
            "output_matches": output_matches,
        },
    )
