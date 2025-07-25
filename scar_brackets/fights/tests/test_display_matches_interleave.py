import pytest


@pytest.mark.django_db
def test_display_matches(client, my_preferences_interleave,matches):
    url = "/fights/display_matches"
    response = client.get(url)
    assert response.status_code == 200
    assert "(Api Tournament 2)" in str(response.content)
    assert "(Api Testing Tournament)" in str(response.content)

##add tests for passing tournament url
@pytest.mark.django_db
def test_display_matches_with_one_tournament_filter(client, my_preferences_interleave,tournament_urls,tournaments,matches):
    url = f"/fights/display_matches?tournaments={tournament_urls[0]}"
    response = client.get(url)
    assert response.status_code == 200
    assert "hw46h4" in str(response.content)
    assert "(Api Tournament 2)" in str(response.content)
    assert "(Api Testing Tournament)" not in str(response.content)

@pytest.mark.django_db
def test_display_matches_with_two(client, my_preferences_interleave,tournament_urls,matches):
    url = f"/fights/display_matches?tournaments={tournament_urls[0]}&tournaments={tournament_urls[1]}"
    response = client.get(url)
    assert response.status_code == 200
    assert "(Api Tournament 2)" in str(response.content)
    assert "(Api Testing Tournament)" in str(response.content)
