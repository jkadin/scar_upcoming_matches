from django.shortcuts import render
from django.http import JsonResponse
from .models import Match, Tournament, Url, Participant
from django.views.decorators.csrf import csrf_exempt
from itertools import chain, zip_longest
from datetime import datetime, timedelta
from preferences import preferences
import json
from django.utils import timezone

NEXT_MATCH_START = timedelta(minutes=1)
MATCH_DELAY = timedelta(minutes=3)


def output():
    match_start = datetime.now() + NEXT_MATCH_START
    INTERLEAVE_METHOD = preferences.MyPreferences.interleave_method  # type: ignore
    print(f"{INTERLEAVE_METHOD=}")
    if INTERLEAVE_METHOD.lower() == "fixed":
        match_list = Match.objects.filter(match_state="open").order_by(
            "calculated_play_order"
        )
    else:
        match_list = match_by_tournament()
    output_match = []
    for i, match in enumerate(match_list[:15]):
        output_match.append(
            {
                "index": i + 1,
                "player1_name": match.player1_id,
                "player2_name": match.player2_id,
                "match_start": match_start.strftime("%I:%M %p"),
                "tournament_name": match.tournament_id.tournament_name,
                "suggested_play_order": match.suggested_play_order,
                "losers_bracket": match.player1_is_prereq_match_loser
                or match.player2_is_prereq_match_loser,
                "match_id": match.match_id,
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


def challonge_index(request):
    output_matches = output()
    return render(
        request,
        "fights/challonge_index.html",
        {"output_matches": output_matches, "urls": Url.objects.all()},
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


def last_complete_list():
    participants = Participant.objects.all()
    print()
    return participants


def time_remaining(request):

    now = timezone.now()
    participants = {}
    for p in Participant.objects.exclude(participant_id=None):
        time_remaining = timedelta(minutes=20) - (now - p.last_updated)  # type: ignore
        if time_remaining < timedelta(minutes=0):
            time_remaining = "00:00"
        else:
            time_remaining = str(time_remaining).split(".")[0]
        participants[p.participant_name] = time_remaining

    return render(
        request,
        "fights/time_remaining.html",
        {
            "participants": sorted(participants.items(), key=lambda x: x[0]),
        },
    )


def end_match(ordered_matches, new_index):
    return ordered_matches[new_index].get("id")


def match_indexes(start_match_id, end_match_id, match_list):
    for index, match in enumerate(match_list):
        if start_match_id == match.match_id:
            match_start_index = index
        if end_match_id == match.match_id:
            match_end_index = index
    return match_start_index, match_end_index


def update_manaual_play_order(start_match_id, old_index, new_index, ordered_items):
    if old_index == new_index:
        return
    screen_distance = new_index - old_index
    direction = int(screen_distance / abs(screen_distance))
    end_match_id = end_match(ordered_items, new_index)
    match_list = Match.objects.order_by("calculated_play_order")
    match_start_index, match_end_index = match_indexes(
        start_match_id, end_match_id, match_list
    )
    distance = match_end_index - match_start_index
    print(f"{match_start_index=},{match_end_index=},{distance=}")

    for index, match in enumerate(match_list):
        if match.match_id == start_match_id:
            match.calculated_play_order += distance
            print(f"Updated Match - {match.match_id} to  {match.calculated_play_order}")
            match.save()
            break

    ##move the rest
    direction = int(distance / abs(distance))
    for i in range(index + direction, index + distance + direction, direction):
        match = match_list[i]
        # print(
        #     i,
        #     match,
        #     match.calculated_play_order,
        #     match.calculated_play_order + direction,
        # )
        match.calculated_play_order -= direction
        match.save()


@csrf_exempt
def manual_sort(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ordered_items = data.get("orderedItems")
            match_id = data.get("movedItem").get("matchID")
            old_index = data.get("movedItem").get("oldIndex")
            new_index = data.get("movedItem").get("newIndex")
            update_manaual_play_order(match_id, old_index, new_index, ordered_items)
            return JsonResponse(
                {
                    "status": "success",
                    "matchID": match_id,
                    "oldIndex": old_index,
                    "newIndex": new_index,
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=405
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
                "calculated_play_order"
            )
        )
    interleaved = zip_longest(*matches_list)
    list_of_tuples = chain.from_iterable(interleaved)
    remove_fill = [x for x in list_of_tuples if x is not None]
    return remove_fill
