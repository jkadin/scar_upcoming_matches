# from django.test import TestCase
import pytest

# from fights.models import Match, Tournament, Url, Participant, Profile, User

# from fights.views import time_out


# Create your tests here.
@pytest.mark.django_db
def test_time_out(authenticated_user, client, profile):
    print(f"{authenticated_user=}, {profile.last_timeout=}")
    url = "/fights/time_out"
    response = client.get(url)
    print(response.content)
    print(f"{authenticated_user=}, {profile.last_timeout=}")
    assert 1 == 1
