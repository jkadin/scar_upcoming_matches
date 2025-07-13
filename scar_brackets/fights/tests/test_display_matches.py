import pytest


@pytest.mark.django_db
def test_display_matches(client, my_preferences):
    url = "/fights/display_matches"
    response = client.get(url)
    assert response.status_code == 200
    assert 'No active tournaments' in str(response.content)
