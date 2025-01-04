import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_claim_user(client, authenticated_user, participant):
    # Set up test data
    # user = User.objects.create_user(username="testuser", password="password")
    # Case 1: Valid claim with "true"
    url = "/fights/claim_user/Player 2/"
    response = client.post(url, {"claim": "true"})

    assert response.status_code == 200
    assert participant.user == authenticated_user
    assert "bot" in response.context
    assert response.context["bot"] == participant

    # Case 2: Valid claim with "false"
    response = client.post(url, {"claim": "false"})

    participant.refresh_from_db()
    assert response.status_code == 200
    assert participant.user is None
    assert "bot" in response.context
    assert response.context["bot"] == participant

    # Case 3: Participant does not exist
    url = reverse("claim_user", kwargs={"participant_name": "Nonexistent Participant"})
    response = client.post(url, {"claim": "true"})

    assert response.status_code == 200
    assert response.context["bot"] is None
