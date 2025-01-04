import pytest


@pytest.mark.django_db
def test_participant(participant):
    assert participant.id == 1
    assert participant.participant_name == "Player 2"
    assert participant.tournament_id.tournament_name == "Tournament 1"
    assert participant.user.username == "testuser"
