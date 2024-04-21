from django.shortcuts import render
from .upcoming_matches import get_tournaments, interleave_matches, output
from .models import Urls


def index(request):
    t = Urls.objects.all()
    tournaments = get_tournaments(t)
    ordered_matches = interleave_matches(tournaments)
    output_matches = output(tournaments, ordered_matches)
    print(output_matches)

    return render(
        request,
        "fights/index.html",
        {
            "matches": ordered_matches,
            "tournaments": tournaments,
            "output_matches": output_matches,
        },
    )
