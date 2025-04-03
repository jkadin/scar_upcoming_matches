import pytest


@pytest.mark.django_db
def test_not_staff(client, my_preferences):
    response = client.get("/fights/create_user/")
    assert response.status_code == 302  # Redirected to login page


@pytest.mark.django_db
def test_staff(client, authenticated_user, my_preferences):
    response = client.get("/fights/create_user/")
    assert response.status_code == 200  # Access granted
    assert "Logout" in str(response.content)
