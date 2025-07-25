import pytest


@pytest.mark.django_db
def test_tournament(tournaments):

    assert str(tournaments[0]) == "Api Tournament 2"
    assert str(tournaments[1]) == "Api Testing Tournament"
    assert tournaments[0].tournament_id == "13875076"
    assert tournaments[0].tournament_name == "Api Tournament 2"
    assert tournaments[0].tournament_repair_time == 20
    assert tournaments[1].tournament_id == "13874863"
    assert tournaments[1].tournament_name == "Api Testing Tournament"
    assert tournaments[1].tournament_repair_time == 20
