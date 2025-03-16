import pytest


@pytest.mark.django_db
def test_claim_user(client, authenticated_user, bots):
    bot1 = bots[0]
    # Case 1: Valid claim with "true"
    url = f"/fights/claim_bot/{bot1}/"
    response = client.post(url, {"claim": "true"})
    assert response.status_code == 200
    bot1.refresh_from_db()
    assert bot1.user.username == "testuser"

    # Case 2: Valid claim with "false"
    response = client.post(url, {"claim": "false"})

    bot1.refresh_from_db()
    assert response.status_code == 200
    assert bot1.user is None
    assert "bot" in response.context
    assert response.context["bot"] == bot1
    assert bot1.user is None

    # Case 3: bot does not exist
    url = "/fights/claim_bot/invalid/"
    response = client.post(url, {"claim": "true"})

    assert response.status_code == 200
    assert response.context["bot"] is None
