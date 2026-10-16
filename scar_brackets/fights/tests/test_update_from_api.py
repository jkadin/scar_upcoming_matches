import pytest
from fights.management.commands import update_from_api
from fights.models import Tournament, Match, Bot, Url


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


@pytest.mark.django_db
def test_fixed_multiple_recalculates_when_no_tournament_needs_interleave(
    monkeypatch, my_preferences
):
    Url.objects.create(url="tournament")
    Tournament.objects.create(
        tournament_id="tournament",
        tournament_name="Tournament",
        tournament_state="underway",
        tournament_url_id="tournament",
    )
    preferences = update_from_api.preferences.MyPreferences  # type: ignore[attr-defined]
    preferences.interleave_method = "Fixed_multiple"
    preferences.save()

    monkeypatch.setattr(update_from_api, "get_tournament_list_from_challonge", lambda: [])
    monkeypatch.setattr(update_from_api, "process_tournaments", lambda _: None)
    monkeypatch.setattr(update_from_api, "load_all_bots", lambda: None)
    monkeypatch.setattr(update_from_api, "load_matches_from_challonge", lambda _: None)
    recalculated_methods = []
    monkeypatch.setattr(
        update_from_api,
        "interleave_matches_in_db",
        lambda method: recalculated_methods.append(method),
    )

    update_from_api.update_database()

    assert recalculated_methods == ["Fixed_multiple"]


@pytest.mark.parametrize("method", ["Interleave", "Interleave_multiple"])
def test_interleave_methods_use_spread_without_grouping_matches(method):
    groups = [
        [Match(match_id=f"t1-{index}") for index in range(10)],
        [Match(match_id=f"t2-{index}") for index in range(20)],
        [Match(match_id=f"t3-{index}") for index in range(20)],
    ]

    ordered = update_from_api.even_distribution(groups, method)

    assert [match.match_id.split("-")[0] for match in ordered] == [
        "t1", "t2", "t3", "t2", "t3",
    ] * 10


@pytest.mark.parametrize("method", ["Interleave", "Interleave_multiple"])
def test_interleave_methods_handle_non_divisible_match_counts(method):
    groups = [
        [Match(match_id=f"t1-{index}") for index in range(39)],
        [Match(match_id=f"t2-{index}") for index in range(79)],
        [Match(match_id=f"t3-{index}") for index in range(79)],
    ]

    ordered = update_from_api.even_distribution(groups, method)

    tournament_sequence = [match.match_id.split("-")[0] for match in ordered]
    assert tournament_sequence[:5] == ["t1", "t2", "t3", "t2", "t3"]
    assert len(ordered) == 197
    assert {tournament: tournament_sequence.count(tournament) for tournament in ("t1", "t2", "t3")} == {
        "t1": 39,
        "t2": 79,
        "t3": 79,
    }
