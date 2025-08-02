import pytest
from django.contrib.auth.models import User
from django.test import Client
from fights.models import Match, Tournament, Url, Bot, Profile
from preferences import preferences
from django.utils import timezone
import pytest_mock
import pickle
from pathlib import Path
from fights.management.commands.update_from_api import (
    get_tournament_list_from_challonge,
    process_tournaments,
    create_null_bot,
)

now = timezone.now()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(
        username="testuser", email="email.gmail.com", password="password"
    )
    user.is_staff = True
    user.save()
    client.force_login(user)
    return user


@pytest.fixture
def tournaments(url, mock_challonge_tournaments):
    challonge_tournament_list = get_tournament_list_from_challonge()
    process_tournaments(challonge_tournament_list)
    return Tournament.objects.all()


@pytest.fixture
def url():
    return [
        Url.objects.create(url="4vljhp3k"),
        Url.objects.create(url="r5vq4p1l"),
    ]


@pytest.fixture
def bots(tournaments, authenticated_user, tournament_urls):
    participants = []
    for tournament_url in tournament_urls:
        tournament_id = Tournament.objects.get(tournament_url=tournament_url)
        pickle_file_path = (
            Path(__file__).parent.parent / f"participants{tournament_url}.pkl"
        )
        with open(pickle_file_path, "rb") as f:
            participants = pickle.load(f)
        for bot in participants:
            Bot.objects.update_or_create(
                bot_id=bot["id"],  # type: ignore
                bot_name=bot["name"],  # type: ignore
                tournament_id=tournament_id,
                user=authenticated_user
            )
        create_null_bot(tournament_id)

    return Bot.objects.all()


@pytest.fixture
def profile(authenticated_user):
    return Profile.objects.get(user=authenticated_user)


@pytest.fixture
def matches(bots, tournaments):
    for tournament_ in tournaments:
        tournament_url = tournament_.tournament_url
        tournament_id = tournament_.tournament_id
        pickle_file_path = Path(__file__).parent.parent / f"matches{tournament_url}.pkl"
        with open(pickle_file_path, "rb") as f:
            matches = pickle.load(f)

        for match in matches:
            bot_id = match.get("player1_id")
            player1_id = Bot.objects.get(
                bot_id=bot_id, tournament_id=tournament_.tournament_id
            )
            player2_id = Bot.objects.get(
                bot_id=match.get("player2_id"), tournament_id=tournament_id
            )
            Match.objects.update_or_create(
                match_id=match.get("id"),
                defaults={
                    "player1_id": player1_id,
                    "player2_id": player2_id,
                    "tournament_id": tournament_,
                    "match_state": match.get("state"),
                    "updated_at": match.get("updated_at"),
                    "suggested_play_order": match.get("suggested_play_order"),
                    "started_at": match.get("started_at"),
                    "underway_at": match.get("underway_at"),
                    "player1_is_prereq_match_loser": match.get(
                        "player1_is_prereq_match_loser"
                    ),
                    "player2_is_prereq_match_loser": match.get(
                        "player2_is_prereq_match_loser"
                    ),
                },
            )
    return Match.objects.all()


@pytest.fixture
def my_preferences():
    prefs = preferences.MyPreferences # type: ignore
    prefs.interleave_method = "fixed"
    prefs.save()
    return prefs

@pytest.fixture
def my_preferences_interleave():
    prefs = preferences.MyPreferences # type: ignore
    prefs.interleave_method = "interleave"
    prefs.save()
    return prefs


@pytest.fixture
def tournament_urls():
    return ["4vljhp3k", "r5vq4p1l"]


def load_matches_from_pickle(tournament_urls):
    matches = []
    for tournament_url in tournament_urls:
        pickle_file_path = Path(__file__).parent.parent / f"matches{tournament_url}.pkl"
        with open(pickle_file_path, "rb") as f:
            matches.append(pickle.load(f))
    return matches


@pytest.fixture
def mock_challonge_matches(mocker: pytest_mock.MockerFixture, tournament_urls):
    matches = load_matches_from_pickle(tournament_urls)
    return mocker.patch("challonge.matches.index", side_effect=matches)


def load_participants_from_pickle(tournament_urls):
    participants = []
    for tournament_url in tournament_urls:
        pickle_file_path = (
            Path(__file__).parent.parent / f"participants{tournament_url}.pkl"
        )
        with open(pickle_file_path, "rb") as f:
            participants.append(pickle.load(f))
    return participants


@pytest.fixture
def mock_challonge_participants(mocker: pytest_mock.MockerFixture, tournament_urls):
    participants = load_participants_from_pickle(tournament_urls)
    return mocker.patch("challonge.participants.index", side_effect=participants)


def load_tournaments_from_pickle(tournament_urls):
    tournaments = []
    for tournament_url in tournament_urls:
        pickle_file_path = (
            Path(__file__).parent.parent / f"tournaments{tournament_url}.pkl"
        )
        with open(pickle_file_path, "rb") as f:
            tournaments.append(pickle.load(f))
    return tournaments


@pytest.fixture
def mock_challonge_tournaments(mocker: pytest_mock.MockerFixture, tournament_urls):
    tournaments = load_tournaments_from_pickle(tournament_urls)
    return mocker.patch("challonge.tournaments.show", side_effect=tournaments)
