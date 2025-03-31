import pytest


@pytest.mark.django_db
def test_my_preferences(client, my_preferences_interleave):
    # assert my_preferences_interleave.interleave_method == "Fixed"
    # my_preferences_interleave.interleave_method = "Interleave"
    # my_preferences_interleave.save()
    # my_preferences_interleave.refresh_from_db()
    assert my_preferences_interleave.interleave_method == "Interleave"

    response = client.get("/fights/")
    assert response.status_code == 200  # Access granted
