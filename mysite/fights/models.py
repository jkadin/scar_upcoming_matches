from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.url


class Match(models.Model):
    player1_id = models.CharField(max_length=100)
    player2_id = models.CharField(max_length=100)
    tournament_name = models.CharField(max_length=100)
    match_id = models.CharField(
        max_length=100, primary_key=True, default="Not Assigned"
    )

    def __str__(self) -> str:
        return self.match_id


class Tournament(models.Model):
    tournament_id = models.CharField(max_length=100, primary_key=True)
    tournament_name = models.CharField(max_length=100)
    tournament_state = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.tournament_name


class Participant(models.Model):
    participant_id = models.CharField(max_length=100, primary_key=True)
    participant_name = models.CharField(max_length=100)
    tournament_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.participant_name
