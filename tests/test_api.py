import pytest
from fastapi.testclient import TestClient

from poker.api import app


@pytest.fixture(scope="function")
def client() -> TestClient:
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "OK"


@pytest.mark.parametrize(
    "body,expected",
    [
        ("AH KH QH JH 10H", "royal flush: hearts"),
        ("6H 7H 8H 9H 10H", "straight flush: 10-high hearts"),
        ("AH AC AD AS KH", "four of a kind: ace"),
        ("AH AC AD KS KH", "full house: ace over king"),
        ("KC 10C 8C 7C 5C", "flush: clubs"),
        ("10H 9C 8D 7S 6H", "straight: 10-high"),
        ("AH AC AD KS QH", "three of a kind: ace"),
        ("AH AC KD KS 7H", "two pair: ace and king"),
        ("AH AC KD JS 7H", "pair: ace"),
        ("AH KC QD 9S 7H", "high card: ace"),
    ],
    ids=[
        "royal-flush",
        "straight-flush",
        "four-of-a-kind",
        "full-house",
        "flush",
        "straight",
        "three-of-a-kind",
        "two-pair",
        "pair",
        "high-card",
    ],
)
def test_rank(client: TestClient, body: str, expected: str) -> None:
    response = client.post("/rank", json=body)

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize(
    "body",
    [
        "AH KH QH JH",
        "AH KH QH JH 99W",
    ],
    ids=[
        "too-few",
        "not-a-card",
    ],
)
def test_rank_bad_input(client: TestClient, body: str) -> None:
    response = client.post("/rank", json=body)

    assert response.status_code != 200
