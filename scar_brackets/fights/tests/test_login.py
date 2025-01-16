import pytest


@pytest.mark.django_db
def test_view_requires_authentication(client, my_preferences):
    response = client.get("/fights/")
    assert response.status_code == 200  # Redirected to login page
    assert "Login" in str(response.content)


@pytest.mark.django_db
def test_view_with_authenticated_user(client, authenticated_user, my_preferences):
    response = client.get("/fights/")
    assert response.status_code == 200  # Access granted
    assert "Logout" in str(response.content)
