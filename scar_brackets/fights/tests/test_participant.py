import pytest
from django.utils import timezone
from datetime import datetime


@pytest.mark.django_db
def test_participant(participants):
    participant1 = participants[0]
    assert participant1.id == 1
    assert participant1.participant_name == "Player 1"
    assert participant1.tournament_id.tournament_name == "Tournament 1"
    assert participant1.user.username == "testuser"
    assert participant1.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert participant1.time_remaining == "00:00"
    assert participant1.upcoming_matches.count() == 0

    participant2 = participants[1]
    assert participant2.id == 2
    assert participant2.participant_name == "Player 2"
    assert participant1.tournament_id.tournament_name == "Tournament 1"
    assert participant1.user.username == "testuser"
    assert participant1.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert participant1.time_remaining == "00:00"
    assert participant1.upcoming_matches.count() == 0
