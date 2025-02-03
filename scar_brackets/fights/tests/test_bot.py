import pytest
from django.utils import timezone
from datetime import datetime


@pytest.mark.django_db
def test_bot(bots, client):
    bot1 = bots[0]
    assert bot1.id == 1
    assert bot1.bot_name == "Player 1"
    assert bot1.tournament_id.tournament_name == "Tournament 1"
    assert bot1.user.username == "testuser"
    assert bot1.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert bot1.time_remaining == "00:00"
    assert bot1.upcoming_matches.count() == 0

    bot2 = bots[1]
    assert bot2.id == 2
    assert bot2.bot_name == "Player 2"
    assert bot1.tournament_id.tournament_name == "Tournament 1"
    assert bot1.user.username == "testuser"
    assert bot1.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert bot1.time_remaining == "00:00"
    assert bot1.upcoming_matches.count() == 0
    assert str(bot1) == "Player 1"
    assert len(bot1.still_in_tournament) == 0

    url = f"/fights/bot/{bot1.bot_name}/"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200

    bot_name = "invalid"
    url = f"/fights/bot/{bot_name}/"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
