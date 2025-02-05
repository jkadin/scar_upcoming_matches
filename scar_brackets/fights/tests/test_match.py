import pytest

from fights.views import match_by_tournament


@pytest.mark.django_db
def test_match(match):

    assert match.player1_id.bot_name == "Player 1"
    assert match.player2_id.bot_name == "Player 2"
    assert match.tournament_id.tournament_name == "Tournament 1"
    assert match.match_state == "open"
    assert match.updated_at is None
    assert match.suggested_play_order == 1
    assert match.calculated_play_order == 1
    assert str(match) == "test match"


@pytest.mark.django_db
def test_match_by_tournament(tournament):
    assert match_by_tournament() is not None
