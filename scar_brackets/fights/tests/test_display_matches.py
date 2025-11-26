import pytest


@pytest.mark.django_db
def test_display_matches(client, my_preferences):
    url = "/fights/display_matches"
    response = client.get(url)
    assert response.status_code == 200
    assert 'No active tournaments' in str(response.content)

##add tests for passing tournament url
@pytest.mark.django_db
def test_display_matches_with_one_tournament_filter(client, my_preferences):
    url = "/fights/display_matches?tournaments=xxx"
    response = client.get(url)
    assert response.status_code == 200
    assert 'No active tournaments' in str(response.content)

@pytest.mark.django_db
def test_display_matches_with_two(client, my_preferences):
    url = "/fights/display_matches?tournaments=xxx?tournaments=yyy"
    response = client.get(url)
    assert response.status_code == 200
    assert 'No active tournaments' in str(response.content)
