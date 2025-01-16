import pytest


@pytest.mark.django_db
def test_time_remaining_inner(client, profile, my_preferences, tournament, bots):
    url = "/fights/time_remaining_inner"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
