# from django.test import TestCase
import pytest

# from fights.models import Match, Tournament, Url, Participant, Profile, User

# from fights.views import time_out


# Create your tests here.
@pytest.mark.django_db
def test_time_out(authenticated_user, client, profile):
    url = "/fights/time_out/Player/"
    response = client.get(url)
    print(response)
    print(authenticated_user, profile.last_timeout)
    assert 1 == 1
