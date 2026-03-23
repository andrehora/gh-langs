import pytest
from history_analysis import fetch_language_stats


@pytest.fixture(scope="module")
def data_100():
    return fetch_language_stats("1.0.0")


@pytest.fixture(scope="module")
def data_950():
    return fetch_language_stats("9.5.0")


@pytest.mark.parametrize("index,expected", [
    (0, 156),
    (1, 43),
    (2, 356),
    (3, 35),
])
def test_languages_100(index, expected, data_100):
    assert data_100[index] == expected


@pytest.mark.parametrize("index,expected", [
    (0, 804),
    (1, 413),
    (2, 1700),
    (3, 401),
])
def test_languages_950(index, expected, data_950):
    assert data_950[index] == expected