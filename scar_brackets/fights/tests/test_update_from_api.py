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

    match_list = Match.objects.filter(match_state="open").order_by(
        "suggested_play_order"
    )
    assert match_list[0].match_id == "387469583"
    assert match_list[0].suggested_play_order == 2
    assert match_list[0].calculated_play_order == 3
    assert match_list[1].match_id == "387469591"
    assert match_list[1].suggested_play_order == 2
    assert match_list[1].calculated_play_order == 4
    assert match_list[2].match_id == "387469582"
    assert match_list[2].suggested_play_order == 3
    assert match_list[2].calculated_play_order == 5
    assert match_list[3].match_id == "387469598"
    assert match_list[3].suggested_play_order == 6
    assert match_list[3].calculated_play_order == 12
    assert match_list[4].match_id == "387469595"
    assert match_list[4].suggested_play_order == 8
    assert match_list[3].calculated_play_order == 12
