import pytest


@pytest.mark.django_db
def test_challonge_index(
    authenticated_user,
    client,
    profile,
    my_preferences,
):
    url = "/fights/challonge"
    response = client.get(url)
    assert response.status_code == 200
