from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Match, Tournament, Option

from itertools import chain, zip_longest
from datetime import datetime, timedelta


NEXT_MATCH_START = timedelta(minutes=1)
MATCH_DELAY = timedelta(minutes=3)


def output():
    match_start = datetime.now() + NEXT_MATCH_START
    try:
        interleave_type = Option.objects.get(option_name="Interleave type").option_value
    except ObjectDoesNotExist:
        interleave_type = "Fixed"
    if interleave_type == "Fixed":
        match_list = Match.objects.filter(match_state="open").order_by(
            "calculated_play_order"
        )
    else:
        match_list = match_by_tournament()
    output_match = []
    for i, match in enumerate(match_list[:6]):
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


def no_background_index(request):
    output_matches = output()
    return render(
        request,
        "fights/no_background_index.html",
        {
            "output_matches": output_matches,
        },
    )


def display_matches(request):
    output_matches = output()
    return render(
        request,
        "fights/matches.html",
        {
            "output_matches": output_matches,
        },
    )


def least_recent_match():
    ordered_output = []
    tournament_list = {}
    for tournament in Tournament.objects.all():
        tournament_matches = Match.objects.filter(
            tournament_id=tournament, match_state="open"
        )
        sorted_list = sorted(tournament_list, key=lambda x: x.started_at)
        tournament_list[tournament] = tournament_matches.order_by("started_at").last()
    for t1 in sorted_list:
        ordered_output.append(
            tournament_matches.order_by("calculated_play_order").first()
        )

    return ordered_output


def match_by_tournament():
    matches_list = []
    for tournament in Tournament.objects.all():
        matches_list.append(
            Match.objects.filter(tournament_id=tournament, match_state="open").order_by(
                "suggested_play_order"
            )
        )
    interleaved = zip_longest(*matches_list)
    list_of_tuples = chain.from_iterable(interleaved)
    remove_fill = [x for x in list_of_tuples if x is not None]
    return remove_fill
