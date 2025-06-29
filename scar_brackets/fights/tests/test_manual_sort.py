import pytest
import json
from fights.models import Match


@pytest.mark.django_db
def test_manual_order(client, authenticated_user, url, tournament, bots, matches):
    match_list = Match.objects.filter().order_by(
        "calculated_play_order", "suggested_play_order"
    )
    assert match_list[0].match_id == "387469590"
    assert match_list[0].suggested_play_order == 1
    assert match_list[0].calculated_play_order == 0
    assert match_list[1].match_id == "387469591"
    assert match_list[1].suggested_play_order == 2
    assert match_list[1].calculated_play_order == 1
    assert match_list[2].match_id == "387469592"
    assert match_list[2].suggested_play_order == 3
    assert match_list[2].calculated_play_order == 2
    assert match_list[3].match_id == "387469593"
    assert match_list[3].suggested_play_order == 4
    assert match_list[3].calculated_play_order == 3
    assert match_list[4].match_id == "387469597"
    assert match_list[4].suggested_play_order == 5
    assert match_list[4].calculated_play_order == 4
    orderedItems = [
        {"id": "387469591", "order": 0},
        {"id": "387469595", "order": 1},
        {"id": "387469598", "order": 2},
        {"id": "387469582", "order": 3},
        {"id": "387469583", "order": 4},
    ]
    movedItem = {"matchID": "387469595", "newIndex": 0, "oldIndex": 1}

    data = {"orderedItems": orderedItems, "movedItem": movedItem}

    url = "/fights/manual_sort"
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert response.json().get("matchID") == "387469595"
    assert response.json().get("oldIndex") == 1
    assert response.json().get("newIndex") == 0

    match_list = Match.objects.all().order_by(
        "calculated_play_order", "suggested_play_order"
    )
    assert match_list[0].match_id == "387469590"
    assert match_list[0].suggested_play_order == 1
    assert match_list[0].calculated_play_order == 0
    assert match_list[1].match_id == "387469595"
    assert match_list[1].suggested_play_order == 8
    assert match_list[1].calculated_play_order == 1
    assert match_list[2].match_id == "387469591"
    assert match_list[2].suggested_play_order == 2
    assert match_list[2].calculated_play_order == 2
    assert match_list[3].match_id == "387469592"
    assert match_list[3].suggested_play_order == 3
    assert match_list[3].calculated_play_order == 3
    assert match_list[4].match_id == "387469593"
    assert match_list[4].suggested_play_order == 4
    assert match_list[4].calculated_play_order == 4

    # test with bad data for dail
    movedItem = {"matchID": "387469501", "newIndex": 1, "oldIndex": 0}
    data = {"orderedItems": orderedItems, "movedItem": movedItem}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 500
    # test old index = new_index
    movedItem = {"matchID": "387469591", "newIndex": 1, "oldIndex": 1}
    data = {"orderedItems": orderedItems, "movedItem": movedItem}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
