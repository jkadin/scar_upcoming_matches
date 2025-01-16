import pytest


@pytest.mark.django_db
def test_my_preferences(client, my_preferences, match, tournament):
    assert my_preferences.interleave_method == "Fixed"
    my_preferences.interleave_method = "Interleave"
    my_preferences.save()
    my_preferences.refresh_from_db()
    assert my_preferences.interleave_method == "Interleave"

    response = client.get("/fights/")
    assert response.status_code == 200  # Access granted
