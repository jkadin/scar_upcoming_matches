import pytest


@pytest.mark.django_db
def test_url(url):

    assert url[0].url == "r5vq4p1l"
    assert url[1].url == "4vljhp3k"
