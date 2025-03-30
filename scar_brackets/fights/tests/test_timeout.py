import pytest
from django.utils import timezone

now = timezone.now()


@pytest.mark.django_db
def test_time_out(authenticated_user, client, profile):
    print(f"{authenticated_user=}, {profile.last_timeout=}")
    url = "/fights/time_out"
    response = client.get(url)
    print(response.content)
    profile.refresh_from_db()
    print(f"{authenticated_user=}, {profile.last_timeout=}")
    assert profile.last_timeout.date() == now.date()
