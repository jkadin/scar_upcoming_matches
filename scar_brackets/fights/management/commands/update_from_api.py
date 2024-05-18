from django.core.management.base import BaseCommand
from django.db import IntegrityError
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
    tournament_list = []
    for tournament_url in Url.objects.all():
        tournament_list.append(
            challonge.tournaments.show(tournament=f"/{tournament_url}")
        )
    # Load Tournament and Participants first
    for t in tournament_list:
        t1 = Tournament(t.get("id"), t.get("name"), t.get("state"), tournament_url)
        t1.save()
        print(f"Tournament_id= - {t1.tournament_id}")
        print("Loading participants")
        load_particpants(t1)
        create_null_particpant(t1)
        print("Participant loading complete")

    # load matches
    for t in tournament_list:
        t1 = Tournament(t.get("id"), t.get("name"), t.get("state"), tournament_url)
        for match in challonge.matches.index(t1.tournament_id, state="all"):
            p1 = match.get("player1_id")
            p2 = match.get("player2_id")
            print(p1, p2)
            player1_id = Participant.objects.get(
                participant_id=match.get("player1_id"), tournament_id=t1
            )
            player2_id = Participant.objects.get(
                participant_id=match.get("player2_id"), tournament_id=t1
            )
            m1 = Match(
                player1_id=player1_id,
                player2_id=player2_id,
                tournament_id=t1,
                match_id=match.get("id"),
                match_state=match.get("state"),
                updated_at=match.get("updated_at"),
                suggested_play_order=match.get("suggested_play_order"),
                calculated_play_order=0,
                estimated_start_time=None,
            )
            try:
                m1.save()
            except IntegrityError:
                print("Match already exists")


def load_particpants(t1):
    for participant in challonge.participants.index(t1.tournament_id):
        print(f'Participant_id= - {participant.get("id")}')
        p1 = Participant(
            participant_id=participant.get("id"),
            participant_name=participant.get("name"),
            tournament_id=t1,
        )
        try:
            p1.save()
        except IntegrityError:
            print("Participant already exists")


def create_null_particpant(t1):
    try:
        p1 = Participant.objects.get(participant_id=None, tournament_id=t1)
        print(p1)
    except:
        p1 = Participant(
            participant_id=None,
            participant_name="Not assigned",
            tournament_id=t1,
        )
        p1.save()
