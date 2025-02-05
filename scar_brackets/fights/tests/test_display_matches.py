import pytest


@pytest.mark.django_db
def test_display_matches(client, my_preferences):
    url = "/fights/display_matches"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
