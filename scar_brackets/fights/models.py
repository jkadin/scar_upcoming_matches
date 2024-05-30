from django.db import models


class Url(models.Model):
    url = models.CharField(primary_key=True, max_length=100)

    def __str__(self) -> str:
        return self.url


class Tournament(models.Model):
    tournament_id = models.CharField(max_length=100, primary_key=True)
    tournament_name = models.CharField(max_length=100)
    tournament_state = models.CharField(max_length=100)
    tournament_url = models.ForeignKey(Url, on_delete=models.CASCADE)
    tournament_needs_interleave = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.tournament_name


class Participant(models.Model):
    participant_id = models.CharField(max_length=100, null=True, blank=True)
    participant_name = models.CharField(max_length=100, null=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tournament_id", "participant_id"], name="unique-in-field"
            )
        ]

    def __str__(self) -> str:
        return f"{self.participant_name}"


class Match(models.Model):
    match_id = models.CharField(max_length=100, primary_key=True)
    player1_id = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, related_name="player1_id", null=True
    )
    player2_id = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, related_name="player2_id", null=True
    )
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match_state = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(null=True)
    suggested_play_order = models.IntegerField()
    calculated_play_order = models.IntegerField(default=0)
    estimated_start_time = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    underway_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.match_id
