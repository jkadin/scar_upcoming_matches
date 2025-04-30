from django.shortcuts import render
from django.http import JsonResponse
from .models import Match, Tournament, Url, Bot, Profile
from django.views.decorators.csrf import csrf_exempt
from itertools import chain, zip_longest
from datetime import datetime, timedelta
from django.contrib.auth.models import User


# from django.db.models import Q

import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from preferences import preferences

NEXT_MATCH_START = timedelta(minutes=1)
MATCH_DELAY = timedelta(minutes=3)
DEFAULT_BACKGROUND_COLOR = "DC3545"


def output(tournaments=[]):
    match_start = datetime.now() + NEXT_MATCH_START
    INTERLEAVE_METHOD = preferences.MyPreferences.interleave_method  # type: ignore
    if INTERLEAVE_METHOD.lower() == "fixed":  # type: ignore
        match_list = Match.objects.filter(match_state="open")
        if tournaments:
            match_list = match_list.filter(tournament_id__tournament_url__in=tournaments)
        match_list = match_list.order_by("calculated_play_order")
    else:
        match_list = match_by_tournament(tournaments)
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
                "unassigned_matches":match.unassigned_matches
            }
        )
        match_start += MATCH_DELAY
    return output_match


def index(request):
    tournaments = request.GET.getlist("tournaments")
    output_matches = output(tournaments=tournaments)
    bgcolor = bg_color(request)
    return render(
        request,
        "fights/index.html",
        {
            "output_matches": output_matches,
            "bgcolor": bgcolor,
            "tournaments": tournaments,
        },
    )

def bg_color(request):
    bgcolor = request.GET.get("bgcolor", DEFAULT_BACKGROUND_COLOR)
    bgcolor="#" + bgcolor
    return bgcolor


def challonge_index(request):
    tournaments = request.GET.getlist("tournaments")
    output_matches = output(tournaments=tournaments)
    return render(
        request,
        "fights/challonge_index.html",
        {   "output_matches": output_matches,
            "urls": Url.objects.all(),
            "tournaments": tournaments,
        },
        
    )


def no_background_index(request):
    tournaments = request.GET.getlist("tournaments")
    output_matches = output(tournaments=tournaments)
    return render(
        request,
        "fights/no_background_index.html",
        {
            "output_matches": output_matches,
            "tournaments": tournaments,
        },
    )


@login_required
@csrf_exempt
def time_out(
    request, username=None, cancel=False
):  # Take a timeout if one is available
    username = request.POST.get("username")
    cancel = request.POST.get("cancel", "false").lower() == "true"  # Convert to boolean
    if not username:
        user = request.user
    else:
        user = User.objects.get(username=username)
    now = timezone.now()
    profile = Profile.objects.get(user=user)
    if cancel:
        last_timeout = timezone.make_aware(
            datetime.min, timezone.get_default_timezone()
        )
        profile.last_timeout = last_timeout
        profile.save()
    else:
        if now.date() != profile.last_timeout.date():
            profile.last_timeout = now
            profile.save()

    return render(
        request,
        "fights/timeout.html",
        {"profile": profile, "users_match": True},
    )


@csrf_exempt
def user(request, user_id):
    try:
        profile = Profile.objects.get(user=user_id)
    except Profile.DoesNotExist:
        return render(
            request,
            "fights/user.html",
        )
    bgcolor = bg_color(request)
    bots = Bot.objects.filter(user=profile.user)
    users_match = False
    if request.user == profile.user:
        users_match = True
    return render(
        request,
        "fights/user.html",
        {"profile": profile, "bots": bots, "users_match": users_match,"bgcolor":bgcolor},
    )


def time_remaining(request):
    tournament_filter = request.GET.getlist("tournaments")
    bgcolor = bg_color(request)
    tournaments = Tournament.objects.filter(tournament_state="underway")
    if tournament_filter:
        tournaments = tournaments.filter(tournament_url__in=tournament_filter)
    tournaments.order_by("tournament_name")

    return render(
        request,
        "fights/time_remaining.html",
        {"tournaments": tournaments, "bgcolor":bgcolor, "tournament_filter": tournament_filter},
    )


def time_remaining_inner(request):
    tournament_filter = request.GET.getlist("tournaments")
    tournaments = Tournament.objects.filter(tournament_state="underway")
    if tournament_filter:
        tournaments = tournaments.filter(tournament_url__in=tournament_filter)
    tournaments.order_by("tournament_name")

    return render(
        request,
        "fights/time_remaining_inner.html",
        {"tournaments": tournaments},
    )


def time_remaining_bot(request, bot_name):
    bot = Bot.objects.get(bot_name=bot_name)
    return render(
        request,
        "fights/time_remaining_bot.html",
        {"bot": bot},
    )


def bot(request, bot_name):
    bgcolor = bg_color(request)
    users_match = False
    try:
        bot = Bot.objects.get(bot_name__iexact=bot_name)
        try:
            if request.user == bot.user:
                users_match = True
        except AttributeError:
            pass
    except Bot.DoesNotExist:
        bot = None
    return render(
        request,
        "fights/bot.html",
        {"bot": bot, "users_match": users_match, "staff": request.user.is_staff,"bgcolor":bgcolor},
    )


@login_required
@csrf_exempt
def claim_multiple_bots(request):
    bot_names = request.POST.getlist("bots")
    username = request.POST.get("username")
    claim = True
    for bot_name in bot_names:
        claim_one_bot(username, bot_name, claim)
    return JsonResponse({"status": "success"})


@login_required
@csrf_exempt
def claim_bot(request, bot_name):
    users_match = False
    claim = request.POST.get("claim", "false").lower() == "true"  # Convert to boolean
    username = request.user
    users_match, bot = claim_one_bot(username, bot_name, claim)
    return render(
        request,
        "fights/claim_bot.html",
        {"bot": bot, "users_match": users_match, "staff": request.user.is_staff},
    )


def claim_one_bot(username, bot_name, claim):
    users_match = False
    user = User.objects.get(username=username)
    try:
        bot = Bot.objects.get(bot_name__iexact=bot_name)
        if not claim:
            bot.user = None
            users_match = False
        else:
            bot.user = user
            users_match = True
        bot.save()
    except Bot.DoesNotExist:
        bot = None
    return users_match, bot


@login_required  # type: ignore
@csrf_exempt
def create_user(request):
    if not request.user.is_staff:
        return render(request, "fights/index.html")
    if request.method == "GET":
        return render(request, "fights/create_user.html")

    if request.method == "POST":
        username = request.POST.get("username")

        user,created=User.objects.get_or_create(username=username)


        assigned_bots = Bot.objects.filter(user=user)
        unassigned_bots = Bot.objects.filter(user=None)
        profile = Profile.objects.get(user=user)
        users_match = False
        if user == profile.user:
            users_match = True
        return render(
            request,
            "fights/bot_claim_list.html",
            {
                "assigned_bots": assigned_bots,
                "unassigned_bots": unassigned_bots,
                "users_match": users_match,
                "username": username,
                "profile": profile,
            },
        )


@csrf_exempt
def end_match(ordered_matches, new_index):
    return ordered_matches[new_index].get("id")


def match_indexes(start_match_id, end_match_id, match_list):
    for index, match in enumerate(match_list):
        if start_match_id == match.match_id:
            match_start_index = index
        if end_match_id == match.match_id:
            match_end_index = index
    return match_start_index, match_end_index


def update_manual_play_order(start_match_id, old_index, new_index, ordered_items):
    if old_index == new_index:
        return
    screen_distance = new_index - old_index
    direction = int(screen_distance / abs(screen_distance))
    end_match_id = end_match(ordered_items, new_index)
    match_list = Match.objects.filter(match_state="open").order_by(
        "calculated_play_order"
    )
    match_start_index, match_end_index = match_indexes(
        start_match_id, end_match_id, match_list
    )
    distance = match_end_index - match_start_index

    for index, match in enumerate(match_list):
        if match.match_id == start_match_id:
            match.calculated_play_order += distance
            match.save()
            break

    ##move the rest
    direction = int(distance / abs(distance))
    for i in range(index + direction, index + distance + direction, direction):
        match = match_list[i]
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
            update_manual_play_order(match_id, old_index, new_index, ordered_items)
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
    tournaments = request.GET.getlist("tournaments")
    output_matches = output(tournaments=tournaments)
    return render(
        request,
        "fights/matches.html",
        {
            "output_matches": output_matches,
        },
    )


def match_by_tournament(tournament_urls=[]):
    matches_list = []
    tournaments = Tournament.objects.all()
    if tournament_urls:
        tournaments = tournaments.objects.filter(tournament_url__in=tournament_urls) # type: ignore
    for tournament in tournaments:
        matches_list.append(
            Match.objects.filter(tournament_id=tournament, match_state="open").order_by(
                "calculated_play_order"
            )
        )
    interleaved = zip_longest(*matches_list)
    list_of_tuples = chain.from_iterable(interleaved)
    remove_fill = [x for x in list_of_tuples if x is not None]
    return remove_fill
