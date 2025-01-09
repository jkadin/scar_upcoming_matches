import pytest
from django.contrib.auth.models import User
from django.test import Client
from fights.models import Match, Tournament, Url, Participant, Profile


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
    return Tournament.objects.create(
        tournament_name="Tournament 1",
        tournament_id=1,
        tournament_state="open",
        tournament_url=url,
        tournament_needs_interleave=True,
    )


@pytest.fixture
def url():
    return Url.objects.create(url="http://www.google.com")


@pytest.fixture
def participants(tournament, authenticated_user):
    return [
        Participant.objects.create(
            participant_id=1,
            participant_name="Player 1",
            tournament_id=tournament,
            user=authenticated_user,
        ),
        Participant.objects.create(
            participant_id=2,
            participant_name="Player 2",
            tournament_id=tournament,
            user=authenticated_user,
        ),
    ]


@pytest.fixture
def profile(authenticated_user):
    return Profile.objects.create(user=authenticated_user)


@pytest.fixture
def match(participants, tournament):
    participant1 = participants[0]
    participant2 = participants[1]
    return Match.objects.create(
        match_id="test match",
        tournament_id=tournament,
        player1_id=participant1,
        player2_id=participant2,
        suggested_play_order=1,
        calculated_play_order=1,
        match_state="open",
    )
