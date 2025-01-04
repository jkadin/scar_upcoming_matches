import pytest


@pytest.mark.django_db
def test_profile(profile):

    assert profile.user.username == "testuser"
    assert profile.time_out_available is True
