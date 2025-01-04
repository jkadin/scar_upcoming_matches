import pytest


@pytest.mark.django_db
def test_view_requires_authentication(client):
    response = client.get("/fights/claim_user/Player 2/")
    assert response.status_code == 302  # Redirected to login page


@pytest.mark.django_db
def test_view_with_authenticated_user(client, authenticated_user, participant):
    response = client.get("/fights/claim_user/Player 2/")
    assert response.status_code == 200  # Access granted
