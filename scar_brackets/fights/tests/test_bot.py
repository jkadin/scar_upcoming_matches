import pytest
from django.utils import timezone
from datetime import datetime


@pytest.mark.django_db
def test_bot(bots, client):
    bot1 = bots[0]
    assert bot1.id == 1
    assert bot1.bot_name == "rnrdsyj"
    assert bot1.tournament_id.tournament_name == "Api Tournament 2"
    assert bot1.user is None
    assert bot1.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert bot1.time_remaining == "00:00"
    assert bot1.upcoming_matches.count() == 0

    bot2 = bots[1]
    assert bot2.id == 2
    assert bot2.bot_name == "srth5h3g"
    assert bot1.tournament_id.tournament_name == "Api Tournament 2"
    assert bot1.user is None
    assert bot1.last_updated == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
    assert bot1.time_remaining == "00:00"
    assert bot1.upcoming_matches.count() == 0
    assert str(bot1) == "rnrdsyj"
    assert bot1.still_in_tournament is False

    url = f"/fights/bot/{bot1.bot_id}/"
    response = client.get(url)
    assert response.status_code == 200

    bot_name = "invalid"
    url = f"/fights/bot/{bot_name}/"
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_unassigned_matches_returns_bot_objects_and_template_uses_names(bots, client):
    from fights.models import Match, Bot

    tournament = bots[0].tournament_id
    null_bot = Bot.objects.get(bot_id=None, tournament_id=tournament)

    # Create a prerequisite match with assigned bots
    prereq = Match.objects.create(
        match_id="m-prereq",
        player1_id=bots[0],
        player2_id=bots[1],
        tournament_id=tournament,
        match_state="open",
        updated_at=timezone.now(),
        suggested_play_order=1,
        calculated_play_order=1,
    )

    # Create a match that references the previous match as player1 prereq
    match = Match.objects.create(
        match_id="m-future",
        player1_id=null_bot,
        player2_id=bots[2],
        tournament_id=tournament,
        match_state="open",
        updated_at=timezone.now(),
        suggested_play_order=2,
        calculated_play_order=2,
        player1_prereq_match_id=prereq.match_id,
    )

    player1_unassigned, player2_unassigned = match.unassigned_matches
    assert player1_unassigned[0].bot_name == bots[0].bot_name
    assert player1_unassigned[1].bot_name == bots[1].bot_name
    assert player2_unassigned == []

    # Ensure template shows names instead of IDs for winner-of match links
    url = f"/fights/bot/{bots[2].bot_id}/"
    response = client.get(url)
    content = response.content.decode()
    assert f'>{bots[0].bot_name}</a>' in content
    assert f'>{bots[1].bot_name}</a>' in content
