import pytest


@pytest.mark.django_db
def test_select_multiole_bots(client, authenticated_user ):
    ###Need to test and handle duplicate bots
    bots=["Player 1"]
    url = "/fights/select_multiple_bots/"
    response = client.post(url, {"claim": True,"username":"testuser","bots":bots})
    assert response.status_code == 200

@pytest.mark.django_db
def test_select_multiole_bots_get(client, authenticated_user ):
    url = "/fights/select_multiple_bots/"
    response = client.get(url )
    assert response.status_code == 200
