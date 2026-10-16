import pytest
from fights.management.commands.update_from_api import (
    even_distribution,
    interleave_matches_in_db,
    update_database,
)
from fights.models import Tournament, Match, Bot


def test_interleave_uses_fixed_distribution():
    groups = [
        ["first-1", "first-2"],
        ["second-1", "second-2", "second-3", "second-4"],
    ]

    assert even_distribution(groups, "Interleave") == even_distribution(groups, "Fixed")
    assert even_distribution(groups, "Interleave") == [
        "first-1",
        "second-1",
        "first-2",
        "second-2",
        "second-3",
        "second-4",
    ]


def test_interleave_multiple_keeps_proportional_distribution():
    groups = [
        ["first-1", "first-2"],
        ["second-1", "second-2", "second-3", "second-4"],
    ]

    assert even_distribution(groups, "Interleave_multiple") == [
        "first-1",
        "second-1",
        "second-2",
        "first-2",
        "second-3",
        "second-4",
    ]


@pytest.mark.django_db
def test_update_database(
    url, mock_challonge_matches, mock_challonge_participants, mock_challonge_tournaments
):
    update_from_api.update_database()
    assert len(Tournament.objects.all()) == 2
    assert len(Match.objects.all()) == 24
    assert len(Bot.objects.all()) == 15

    match_list = Match.objects.filter(match_state="open").order_by(
        "suggested_play_order"
    )
    assert match_list[0].match_id == "387469583"
    assert match_list[0].suggested_play_order == 2
    assert match_list[0].calculated_play_order == 1
    assert match_list[1].match_id == "387469591"
    assert match_list[1].suggested_play_order == 2
    assert match_list[1].calculated_play_order == 2
    assert match_list[2].match_id == "387469582"
    assert match_list[2].suggested_play_order == 3
    assert match_list[2].calculated_play_order == 3
    assert match_list[3].match_id == "387469598"
    assert match_list[3].suggested_play_order == 6
    assert match_list[3].calculated_play_order == 4
    assert match_list[4].match_id == "387469595"
    assert match_list[4].suggested_play_order == 8
    assert match_list[4].calculated_play_order == 5


@pytest.mark.django_db
def test_interleave_does_not_let_completed_matches_take_a_turn(matches, tournament):
    Match.objects.all().delete()
    first_tournament, second_tournament = list(Tournament.objects.all())
    Match.objects.create(
        match_id="completed-first",
        tournament_id=first_tournament,
        match_state="complete",
        suggested_play_order=1,
    )
    first_next = Match.objects.create(
        match_id="first-next",
        tournament_id=first_tournament,
        match_state="open",
        suggested_play_order=2,
    )
    second_first = Match.objects.create(
        match_id="second-first",
        tournament_id=second_tournament,
        match_state="open",
        suggested_play_order=1,
    )

    interleave_matches_in_db("Interleave")

    open_matches = list(
        Match.objects.filter(match_state="open").order_by("calculated_play_order")
    )
    assert open_matches[:2] == [first_next, second_first]
