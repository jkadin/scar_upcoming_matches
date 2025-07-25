import pytest


@pytest.mark.django_db
def test_my_preferences(client,my_preferences):
    test_preferences = my_preferences  # type: ignore
    assert test_preferences.interleave_method=='fixed'
    response = client.get("/fights/")
    assert response.status_code == 200  # Access granted

@pytest.mark.django_db
def test_my_preferences_interleave(client,my_preferences_interleave):
    test_preferences = my_preferences_interleave
    assert test_preferences.interleave_method == "interleave"
    response = client.get("/fights/")
    assert response.status_code == 200  # Access granted
