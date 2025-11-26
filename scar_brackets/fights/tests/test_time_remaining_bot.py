import pytest


@pytest.mark.django_db
def test_time_remaining_bot(
    client,
    bots
):

    bot1 = bots[0]
    url = f"/fights/time_remaining_bot/{bot1.bot_name}/"
    response = client.get(url)
    assert response.status_code == 200