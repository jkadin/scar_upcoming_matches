import pytest
from django.utils import timezone
from datetime import datetime


@pytest.mark.django_db
def test_participant(participant):
    assert participant.id == 1
    assert participant.participant_name == "Player 2"
    assert participant.tournament_id.tournament_name == "Tournament 1"
    assert participant.user.username == "testuser"
    assert participant.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert participant.time_remaining == "00:00"
    assert participant.upcoming_matches.count() == 0
