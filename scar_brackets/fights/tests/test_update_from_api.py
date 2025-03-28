import pytest
from fights.management.commands.update_from_api import update_database
from fights.models import Tournament, Match, Bot


@pytest.mark.django_db
def test_update_database(
    url, mock_challonge_matches, mock_challonge_participants, mock_challonge_tournaments
):
    update_database()
    assert len(Tournament.objects.all()) == 2
    assert len(Match.objects.all()) == 24
    assert len(Bot.objects.all()) == 15
