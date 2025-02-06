import pytest


@pytest.mark.django_db
def test_tournament(tournament):

    assert str(tournament[0]) == "Tournament 1"
    assert str(tournament[1]) == "Tournament 2"
    assert tournament[0].tournament_id == "1"
    assert tournament[0].tournament_name == "Tournament 1"
    assert tournament[0].tournament_repair_time == 30
    assert tournament[1].tournament_id == "2"
    assert tournament[1].tournament_name == "Tournament 2"
    assert tournament[1].tournament_repair_time == 20
