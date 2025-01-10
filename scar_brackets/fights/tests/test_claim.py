import pytest


@pytest.mark.django_db
def test_claim_user(client, authenticated_user, participants):
    participant1 = participants[0]
    # Case 1: Valid claim with "true"
    url = "/fights/claim_bot/Player 1/"
    response = client.post(url, {"claim": "true"})
    assert response.status_code == 200
    assert participant1.user.username == "testuser"

    # Case 2: Valid claim with "false"
    response = client.post(url, {"claim": "false"})

    participant1.refresh_from_db()
    assert response.status_code == 200
    assert participant1.user is None
    assert "bot" in response.context
    # assert response.context["bot"] == participant1
    # assert participant1.user is None

    # # Case 3: Participant does not exist
    # url = reverse("claim_bot", kwargs={"participant_name": "Nonexistent Participant"})
    # response = client.post(url, {"claim": "true"})

    # assert response.status_code == 200
    # assert response.context["bot"] is None
