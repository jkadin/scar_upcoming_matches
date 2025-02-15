import pytest
from django.contrib.auth.models import User
from django.test import Client
from fights.models import Match, Tournament, Url, Bot, Profile, MyPreferences
from django.utils import timezone
import pytest_mock
import pickle
from pathlib import Path

now = timezone.now()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(
        username="testuser", email="email.gmail.com", password="password"
    )
    client.force_login(user)
    return user


@pytest.fixture
def tournament(url):
    return [
        Tournament.objects.create(
            tournament_name="Tournament 1",
            tournament_id="1",
            tournament_state="underway",
            tournament_url=url[0],
            tournament_needs_interleave=True,
            tournament_repair_time=30,
        ),
        Tournament.objects.create(
            tournament_name="Tournament 2",
            tournament_id="2",
            tournament_state="underway",
            tournament_url=url[1],
            tournament_needs_interleave=True,
            tournament_repair_time=20,
        ),
    ]


@pytest.fixture
def url():
    return [
        Url.objects.create(url="r5vq4p1l"),
        Url.objects.create(url="4vljhp3k"),
    ]


@pytest.fixture
def bots(tournament, authenticated_user):
    bot1 = (
        Bot.objects.create(
            bot_id=1,
            bot_name="Player 1",
            tournament_id=tournament[0],
            user=authenticated_user,
        ),
    )
    bot2 = (
        Bot.objects.create(
            bot_id=2,
            bot_name="Player 2",
            tournament_id=tournament[1],
            user=authenticated_user,
        ),
    )
    return [bot1, bot2]


@pytest.fixture
def profile(authenticated_user):
    return Profile.objects.create(user=authenticated_user)


@pytest.fixture
def match(bots, tournament):
    bot1 = bots[0][0]
    bot2 = bots[1][0]
    return Match.objects.create(
        match_id="test match",
        tournament_id=tournament[0],
        player1_id=bot1,
        player2_id=bot2,
        suggested_play_order=1,
        calculated_play_order=1,
        match_state="open",
        started_at=now,
    )


@pytest.fixture
def my_preferences():
    return MyPreferences.objects.create()


@pytest.fixture
def mock_challonge_matches(mocker: pytest_mock.MockerFixture):
    pickle_file_path = Path(__file__).parent.parent / "matches_data13874863.pkl"
    with open(pickle_file_path, "rb") as f:
        matches_data = pickle.load(f)
    return mocker.patch("challonge.matches.index", return_value=matches_data)


@pytest.fixture
def mock_challonge_participants(mocker: pytest_mock.MockerFixture):
    pickle_file_path = Path(__file__).parent.parent / "participants13874863.pkl"
    with open(pickle_file_path, "rb") as f:
        matches_data = pickle.load(f)
    return mocker.patch("challonge.participants.index", return_value=matches_data)


@pytest.fixture
def mock_challonge_tournaments(mocker: pytest_mock.MockerFixture):
    # tournaments = []
    pickle_file_path = Path(__file__).parent.parent / "tournament_list4vljhp3k.pkl"
    with open(pickle_file_path, "rb") as f:
        x = pickle.load(f)
    # with open(pickle_file_path, "rb") as f:
    #     pickle_file_path = Path(__file__).parent.parent / "tournament_listr5vq4p1l.pkl"
    #     tournaments.append(pickle.load(f))
    return mocker.patch("challonge.tournaments.show", return_value=x)
    return mocker.patch('challonge.tournaments.show( tournament=f"/{tournament_url}" ')
