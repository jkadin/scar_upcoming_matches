import pytest
import json
from fights.models import Match


@pytest.mark.django_db
def test_manual_order(client, authenticated_user, url, tournament, bots, matches):
    match_list = Match.objects.filter(match_state="open").order_by(
        "calculated_play_order"
    )
    for match in match_list:
        print(match, match.calculated_play_order)
    orderedItems = [
        {"id": "387469591", "order": 0},
        {"id": "387469583", "order": 1},
        {"id": "387469598", "order": 2},
        {"id": "387469582", "order": 3},
        {"id": "387469595", "order": 4},
    ]
    movedItem = {"matchID": "387469591", "newIndex": 1, "oldIndex": 0}

    data = {"orderedItems": orderedItems, "movedItem": movedItem}

    url = "/fights/manual_sort"
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200

    match_list = Match.objects.filter(match_state="open").order_by(
        "calculated_play_order"
    )
    for match in match_list:
        print(match, match.calculated_play_order)
