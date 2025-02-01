import pytest


@pytest.mark.django_db
def test_url(url):

    assert url.url == "http://www.google.com"
    assert str(url) == "http://www.google.com"
