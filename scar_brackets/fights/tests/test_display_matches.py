import pytest


@pytest.mark.django_db
def test_time_remaining_inner(client, profile, my_preferences, tournament, bots, match):
    url = "/fights/display_matches"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
