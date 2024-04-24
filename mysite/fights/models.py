from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.url


class Match(models.Model):
    player1_id = models.CharField(max_length=100, null=True)
    player2_id = models.CharField(max_length=100, null=True)
    tournament_id = models.CharField(max_length=100)
    match_id = models.CharField(max_length=100, primary_key=True)
    match_state = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(null=True)
    suggested_play_order = models.CharField(max_length=100, null=True)

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
