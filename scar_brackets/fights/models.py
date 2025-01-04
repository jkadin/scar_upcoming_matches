from django.db import models
from preferences.models import Preferences
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

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
    def time_out(self):
        try:
            time_out = Profile.objects.get(user=self.user).last_timeout
        except Profile.DoesNotExist:
            time_out = timezone.make_aware(
                datetime.min, timezone.get_default_timezone()
            )
        return time_out

    @property
    def time_remaining(self):
        now = timezone.now()
        time_out_remaining = timedelta(minutes=20) - (now - self.time_out)  # type: ignore
        time_remaining = timedelta(minutes=20) - (now - self.last_updated)  # type: ignore
        if time_out_remaining > time_remaining:
            time_remaining = time_out_remaining
        if time_remaining < timedelta(minutes=0):
            time_remaining = "00:00"
        else:
            time_remaining = ":".join(str(time_remaining).split(".")[0].split(":")[1:])

        return time_remaining

    @property
    def still_in_tournament(self):
        return self.upcoming_matches

    @property
    def upcoming_matches(self):
        matches = Match.objects.filter(
            Q(player1_id=self) | Q(player2_id=self), ~Q(match_state="Complete")
        )
        return matches

    @property
    def time_out_available(self):
        now = timezone.now()
        if self.time_out.date() == now.date():
            return False
        if (now - self.time_out).total_seconds() >= 0:
            return True


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_timeout = models.DateTimeField(null=True, blank=True)

    @property
    def display_name(self):
        try:
            display_name = self.user.socialaccount_set.filter(provider="discord")[0].extra_data["global_name"]
        except Exception as e:
            raise e
            display_name = self.user.name
        return display_name