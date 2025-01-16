import pytest


@pytest.mark.django_db
def test_time_remaining(
    client,
    profile,
    my_preferences,
):
    url = "/fights/time_remaining"
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
