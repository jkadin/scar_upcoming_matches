import pytest


@pytest.mark.django_db
def test_tournament(tournament):

    assert str(tournament) == "Tournament 1"
