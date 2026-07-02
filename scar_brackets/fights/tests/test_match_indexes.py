import pytest

from fights.views import match_indexes


class Dummy:
    def __init__(self, match_id):
        self.match_id = match_id


def test_match_indexes_returns_indices():
    matches = [Dummy('a'), Dummy('b'), Dummy('c')]
    assert match_indexes('a', 'c', matches) == (0, 2)


def test_match_indexes_missing_raises():
    matches = [Dummy('a'), Dummy('b')]
    with pytest.raises(ValueError):
        match_indexes('a', 'z', matches)
