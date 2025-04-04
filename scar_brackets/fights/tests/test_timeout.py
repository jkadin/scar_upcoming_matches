import pytest
from django.utils import timezone
from datetime import datetime

now = timezone.now()


@pytest.mark.django_db
def test_time_out(authenticated_user, client, profile):
    print(f"{authenticated_user=}, {profile.last_timeout=}")
    url = "/fights/time_out"
    response = client.post(url)
    print(response.content)
    profile.refresh_from_db()
    print(f"{authenticated_user=}, {profile.last_timeout=}")
    assert profile.last_timeout.date() == now.date()
    # Test cancel timeout
    response = client.post(url, {"cancel": "true"})
    profile.refresh_from_db()
    assert profile.last_timeout == timezone.make_aware(
        datetime.min, timezone.get_default_timezone()
    )
