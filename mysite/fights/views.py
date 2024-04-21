from django.shortcuts import render
from .upcoming_matches import get_tournaments, interleave_matches, output
from .models import Url


def index(request):
    t = Url.objects.all()
    if not t:
        return render(
            request,
            "fights/no_tournaments.html",
        )

    tournaments = get_tournaments(t)
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
