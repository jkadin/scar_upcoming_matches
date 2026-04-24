import pytest

@pytest.mark.django_db
def test_all_bots(client):
    url = "/fights/users"
    response = client.get(url)
    assert response.status_code == 200
    assert "All Users" in str(response.content)
