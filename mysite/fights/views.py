from django.shortcuts import render
from django.db import IntegrityError
from .upcoming_matches import get_tournaments, interleave_matches, output
from .models import Url, Tournament, Match, Participant
import challonge
from dotenv import load_dotenv
import os

load_dotenv()


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
            )
            print(match.get("id"), match.get("identifier"))
            try:
                m1.save()
            except IntegrityError:
                print("id", match.get("identifier"))

        for participant in challonge.participants.index(t1.tournament_id):
            p1 = Participant(
                participant.get("id"),
                participant.get("name"),
                participant.get("tournament_id"),
            )
            p1.save()


def index(request):
    update_database()
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
