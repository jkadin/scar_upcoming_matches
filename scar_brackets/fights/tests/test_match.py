import pytest
import datetime

from fights.views import match_by_tournament


@pytest.mark.django_db
def test_match(matches):

    match = matches[0]

    assert match.player1_id.bot_name == "hw45jdtum"
    assert match.player2_id.bot_name == "hw46h4"
    assert match.tournament_id.tournament_name == "Api Tournament 2"
    assert match.match_state == "complete"
    assert match.updated_at == datetime.datetime(
        2024, 10, 20, 23, 41, 5, 634000, tzinfo=datetime.timezone.utc
    )
    assert match.suggested_play_order == 1
    assert match.calculated_play_order == 0
    assert str(match) == "387469581"


@pytest.mark.django_db
def test_match_by_tournament():
    assert match_by_tournament() is not None
