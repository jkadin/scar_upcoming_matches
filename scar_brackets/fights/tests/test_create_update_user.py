import pytest

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_not_staff(client, my_preferences):
    response = client.get("/fights/create_user/")
    assert response.status_code == 302  # Redirected to login page


@pytest.mark.django_db
def test_staff(client, authenticated_user, my_preferences, bots):
    response = client.get("/fights/create_user/")
    assert response.status_code == 200  # Access granted
    assert "Update" in str(response.content)
    url = "/fights/create_user/"
    response = client.post(url, {"username": "Testuser"})
    assert response.status_code == 200
    assert "hw45yhw" in str(response.content)
    assert "hw46h4" in str(response.content)
    assert "rnrdsyj" in str(response.content)
    assert "Small Sharp Object" in str(response.content)
    assert "Thagclonizer" in str(response.content)
    assert "Lonx" in str(response.content)
    assert "Elephants Gerald" in str(response.content)
    assert "Moose and Squirrel" in str(response.content)

    # test create_user
    create_user = "Newuser"
    response = client.post(url, {"username": create_user})
    assert response.status_code == 200
    new_user = User.objects.get(username=create_user)
    assert new_user.username == create_user
    assert "hw45yhw" in str(response.content)
    assert "hw46h4" in str(response.content)
    assert "rnrdsyj" in str(response.content)
    assert "Small Sharp Object" in str(response.content)
    assert "Thagclonizer" in str(response.content)
    assert "Lonx" in str(response.content)
    assert "Elephants Gerald" in str(response.content)
    assert "Moose and Squirrel" in str(response.content)


@pytest.mark.django_db
def test_staff_exists(client, authenticated_user, my_preferences, bots):
    url = "/fights/create_user/"
    response = client.post(url, {"username": "Testuser"})
    assert response.status_code == 200
    assert "hw45yhw" in str(response.content)
    assert "hw46h4" in str(response.content)
    assert "rnrdsyj" in str(response.content)
    assert "Small Sharp Object" in str(response.content)
    assert "Thagclonizer" in str(response.content)
    assert "Lonx" in str(response.content)
    assert "Elephants Gerald" in str(response.content)
    assert "Moose and Squirrel" in str(response.content)
