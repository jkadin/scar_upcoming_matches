import pytest
from unittest.mock import patch
from fights.management.commands.update_from_api import update_database
from fights.models import Tournament, Match, Bot


@pytest.fixture
def mock_challonge():
    with patch("fights.management.commands.update_from_api.challonge") as mock:
        yield mock


# # @pytest.fixture
# # def mock_os():
# #     with patch("fights.management.commands.update_from_api.os") as mock:
# #         yield mock


# # @pytest.fixture
# # def mock_load_dotenv():
# #     with patch("fights.management.commands.update_from_api.load_dotenv") as mock:
# #         yield mock


# # @pytest.fixture
# # def mock_url_objects():
# #     with patch("fights.management.commands.update_from_api.Url.objects") as mock:
# #         yield mock


# # @pytest.fixture
# # def mock_tournament_objects():
# #     with patch("fights.management.commands.update_from_api.Tournament.objects") as mock:
# #         yield mock


# # @pytest.fixture
# # def mock_match_objects():
# #     with patch("fights.management.commands.update_from_api.Match.objects") as mock:
# #         yield mock


# # @pytest.fixture
# # def mock_bot_objects():
# #     with patch("fights.management.commands.update_from_api.Bot.objects") as mock:
# #         yield mock


# @pytest.fixture
# @pytest.mark.django_db
# def mock_load_bots():
#     with patch("fights.management.commands.update_from_api.load_bots") as mock:
#         yield mock


# @pytest.fixture
# def mock_create_null_bot():
#     with patch("fights.management.commands.update_from_api.create_null_bot") as mock:
#         yield mock


@pytest.mark.django_db
def test_update_database(
    tournament,
    url,
):
    update_database()
    assert len(Tournament.objects.all()) == 3
    assert len(Match.objects.all()) == 24
    assert len(Bot.objects.all()) == 15
