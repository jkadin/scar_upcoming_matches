from django.core.management.base import BaseCommand
import challonge
import os
from fights.models import Url, Tournament, Match, Participant


class Command(BaseCommand):
    help = "Updates the data from the API"

    def handle(self, *args, **options):
        update_database()

        self.stdout.write(self.style.SUCCESS("Successfully updated data"))


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
        t1 = Tournament(t.get("id"), t.get("name"), t.get("state"), tournament_url)
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
