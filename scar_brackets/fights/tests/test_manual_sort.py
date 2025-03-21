import pytest
import json
from fights.models import Match


@pytest.mark.django_db
def test_manual_order(client, authenticated_user, url, tournament, bots, matches):
    match_list = Match.objects.filter(match_state="open").order_by(
        "suggested_play_order"
    )
    for i, match in enumerate(match_list):
        match.calculated_play_order = i
        match.save()
    assert match_list[0].match_id == "387469583"
    assert match_list[0].suggested_play_order == 2
    assert match_list[0].calculated_play_order == 0
    assert match_list[1].match_id == "387469591"
    assert match_list[1].suggested_play_order == 2
    assert match_list[1].calculated_play_order == 1
    assert match_list[2].match_id == "387469582"
    assert match_list[2].suggested_play_order == 3
    assert match_list[2].calculated_play_order == 2
    assert match_list[3].match_id == "387469598"
    assert match_list[3].suggested_play_order == 6
    assert match_list[3].calculated_play_order == 3
    assert match_list[4].match_id == "387469595"
    assert match_list[4].suggested_play_order == 8
    assert match_list[4].calculated_play_order == 4
    orderedItems = [
        {"id": "387469583", "order": 0},
        {"id": "387469591", "order": 1},
        {"id": "387469582", "order": 2},
        {"id": "387469598", "order": 3},
        {"id": "387469595", "order": 4},
    ]
    movedItem = {"matchID": "387469591", "newIndex": 0, "oldIndex": 1}

    data = {"orderedItems": orderedItems, "movedItem": movedItem}

    url = "/fights/manual_sort"
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("matchID") == "387469591"
    assert response.json().get("oldIndex") == 1
    assert response.json().get("newIndex") == 0

    match_list = Match.objects.filter(match_state="open").order_by(
        "calculated_play_order"
    )
    assert match_list[0].match_id == "387469591"
    assert match_list[0].suggested_play_order == 2
    assert match_list[0].calculated_play_order == 0
    assert match_list[1].match_id == "387469583"
    assert match_list[1].suggested_play_order == 2
    assert match_list[1].calculated_play_order == 1
    assert match_list[2].match_id == "387469582"
    assert match_list[2].suggested_play_order == 3
    assert match_list[2].calculated_play_order == 2
    assert match_list[3].match_id == "387469598"
    assert match_list[3].suggested_play_order == 6
    assert match_list[3].calculated_play_order == 3
    assert match_list[4].match_id == "387469595"
    assert match_list[4].suggested_play_order == 8
    assert match_list[4].calculated_play_order == 4
