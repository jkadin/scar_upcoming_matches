import pytest


@pytest.mark.django_db
def test_authenticated_user(
    authenticated_user,
    client,
    profile,
):
    url = "/fights/user/1/"

    response = client.get(url)
    # print(response.context)
    assert response.status_code == 200

    assert "Logout" in str(response.content)


@pytest.mark.django_db
def test_un_authenticated_user(
    client,
):
    url = "/fights/user/1/"
    response = client.get(url)
    assert response.status_code == 200
    assert "Logout" not in str(response.content)
