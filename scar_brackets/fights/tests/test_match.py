import pytest
import datetime

from fights.views import match_by_tournament


@pytest.mark.django_db
def test_match(matches):

    match = matches[0]

    assert match.player1_id.bot_name == "Small Sharp Object"
    assert match.player2_id.bot_name == "Moose and Squirrel"
    assert match.tournament_id.tournament_name == "Api Testing Tournament"
    assert match.match_state == "complete"
    assert match.suggested_play_order == 1
    assert match.calculated_play_order == 0
    assert str(match) == "387469590"


@pytest.mark.django_db
def test_match_by_tournament(tournament):
    assert match_by_tournament() is not None
