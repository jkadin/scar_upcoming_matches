import pytest
from preferences import preferences


@pytest.mark.django_db
def test_my_preferences(client):
    test_preferences = preferences.MyPreferences  # type: ignore
    assert test_preferences.interleave_method=='Fixed'
    test_preferences.interleave_method = "interleave" # type: ignore
    test_preferences.save()
    test_preferences.refresh_from_db()
    assert test_preferences.interleave_method == "interleave"

    response = client.get("/fights/")
    assert response.status_code == 200  # Access granted
