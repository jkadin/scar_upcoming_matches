import pytest
import json


@pytest.mark.django_db
def test_manual_order(client, authenticated_user, url, tournament, bots):
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
    assert response.status_code == 500
