import pytest


@pytest.mark.django_db
def test_user(
    authenticated_user,
    client,
):
    url = "/fights/user/1/"
    response = client.get(url, authenticated_user)
    print(response.content)
    assert response.status_code == 200
    assert 1 == 1
