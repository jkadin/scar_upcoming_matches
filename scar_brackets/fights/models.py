from django.db import models
from preferences.models import Preferences
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta


class MyPreferences(Preferences):
    interleave_method = models.CharField(
        max_length=100, default="Fixed", null=True, blank=True
    )


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

    @property
    def last_updated(self):
        # Get the most recent match where the participant is either player1 or player2
        recent_match = (
            Match.objects.filter(
                Q(player1_id=self) | Q(player2_id=self), match_state="complete"
            )
            .order_by("-updated_at")
            .first()
        )

        # Return the updated_at of the most recent match, or None if no matches found
        return (
            recent_match.updated_at
            if recent_match
            else timezone.make_aware(datetime.min, timezone.get_default_timezone())
        )

    @property
    def time_remaining(self):
        now = timezone.now()
        time_remaining = timedelta(minutes=20) - (now - self.last_updated)  # type: ignore
        if time_remaining < timedelta(minutes=0):
            time_remaining = "00:00"
        else:
            time_remaining = ":".join(str(time_remaining).split(".")[0].split(":")[1:])
        return time_remaining

    @property
    def still_in_tournament(self):
        in_tournament = False
        matches = Match.objects.filter(
            ~Q(player1_id=self) | Q(player2_id=self), match_state="complete"
        )
        if matches:
            return True

        return in_tournament


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
    player1_is_prereq_match_loser = models.BooleanField(default=False)
    player2_is_prereq_match_loser = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.match_id
