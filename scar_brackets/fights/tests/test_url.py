import pytest


@pytest.mark.django_db
def test_url(url):

    assert url[0].url == "4vljhp3k"
    assert url[1].url == "r5vq4p1l"
