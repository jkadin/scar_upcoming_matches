import pytest


@pytest.mark.django_db
def test_claim_multiple_bots_post(client, authenticated_user, bots):
    url = "/fights/claim_multiple_bots/"
    response = client.post(url, {"claim": True,"username":"testuser","bots":bots})
    assert response.status_code == 200
    assert "Moose and Squirrel" in str(response.content)

@pytest.mark.django_db
def test_claim_multiple_bots_get(client, authenticated_user, bots):
    url = "/fights/claim_multiple_bots/"
    response = client.get(url)
    assert response.status_code == 200
    assert "Select User" in str(response.content)

