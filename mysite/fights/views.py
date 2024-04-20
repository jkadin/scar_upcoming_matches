from django.shortcuts import render
from .upcoming_matches import get_tournaments, interleave_matches
from .models import Urls

from datetime import datetime, timedelta


def index(request):
    NEXT_MATCH_START = timedelta(minutes=1)
    match_start = (datetime.now() + NEXT_MATCH_START).strftime("%I:%M %p")
    t=Urls.objects.all()
    tournaments = get_tournaments(t)
    ordered_matches = interleave_matches(tournaments)

    return render(
        request,
        "fights/index.html",
        {
            "matches": ordered_matches,
            "tournaments": tournaments,
            "match_start": match_start,
        },
    )
