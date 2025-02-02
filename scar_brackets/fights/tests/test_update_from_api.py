import pytest
from unittest.mock import patch
from fights.management.commands.update_from_api import update_database
from fights.models import Tournament, Match, Bot


@pytest.fixture
def mock_challonge():
    with patch("fights.management.commands.update_from_api.challonge") as mock:
        yield mock


@pytest.mark.django_db
def test_update_database(
    tournament,
    url,
):
    update_database()
    assert len(Tournament.objects.all()) == 3
    assert len(Match.objects.all()) == 24
    assert len(Bot.objects.all()) == 15
