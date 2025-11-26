import pytest

@pytest.mark.django_db
def test_all_bots(client):
    url = "/fights/bots"
    response = client.get(url)
    assert response.status_code == 200
    assert "All Bots" in str(response.content)
