import pytest


@pytest.mark.django_db
def test_no_background_index(
    authenticated_user,
    client,
    profile,
    my_preferences,
):
    url = "/fights/stream"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
