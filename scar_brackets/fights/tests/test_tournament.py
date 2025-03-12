import pytest


@pytest.mark.django_db
def test_tournament(tournament):

    assert str(tournament[0]) == "Api Tournament 2"
    assert str(tournament[1]) == "Api Testing Tournament"
    assert tournament[0].tournament_id == "13875076"
    assert tournament[0].tournament_name == "Api Tournament 2"
    assert tournament[0].tournament_repair_time == 20
    assert tournament[1].tournament_id == "13874863"
    assert tournament[1].tournament_name == "Api Testing Tournament"
    assert tournament[1].tournament_repair_time == 20
