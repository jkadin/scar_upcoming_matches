import pytest


@pytest.mark.django_db
def test_time_remaining_inner(client, profile, my_preferences, tournament, bots):
    url = "/fights/time_remaining_inner"
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_time_remaining_inner_one_tournament(client, profile, my_preferences, tournament, bots):
    url = "/fights/time_remaining_inner?tournaments=r5vq4p1l"
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_time_remaining_inner_two_tournaments(client, profile, my_preferences, tournament, bots):
    url = "/fights/time_remaining_inner?tournaments=r5vq4p1l&tournaments=4vljhp3k"
    response = client.get(url)
    assert response.status_code == 200
