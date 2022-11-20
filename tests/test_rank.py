from itertools import cycle
from typing import Optional, Union

import pytest

from poker.constants import Suit, Value
from poker.models import Card, Hand
from poker.rank.hands import (
    _is_flush,
    _is_straight,
    flush,
    four_of_a_kind,
    full_house,
    high_card,
    pair,
    royal_flush,
    straight,
    straight_flush,
    three_of_a_kind,
    two_pair,
)
from tests.conftest import Factory


@pytest.mark.parametrize(
    "suits,expected",
    [
        ([Suit.CLUBS, Suit.DIAMONDS, Suit.SPADES, Suit.HEARTS, Suit.CLUBS], False),
        ([Suit.CLUBS, Suit.CLUBS, Suit.CLUBS, Suit.CLUBS, Suit.CLUBS], True),
    ],
    ids=[
        "non-unique",
        "unique",
    ],
)
def test__is_flush(
    card_factory: Factory[Card], suits: list[Suit], expected: dict[str, Union[str, int]]
) -> None:
    result = _is_flush([card_factory(suit=suit) for suit in suits])

    if expected:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "values,expected",
    [
        ([Value.TWO, Value.TWO, Value.THREE, Value.FOUR, Value.FIVE], None),
        ([Value.THREE, Value.TWO, Value.ACE, Value.TEN, Value.KING], None),
        ([Value.ACE, Value.TWO, Value.THREE, Value.FOUR, Value.FIVE], Value.FIVE),
        ([Value.ACE, Value.KING, Value.TEN, Value.JACK, Value.QUEEN], Value.ACE),
        ([Value.THREE, Value.FIVE, Value.TWO, Value.FOUR, Value.SIX], Value.SIX),
    ],
    ids=[
        "non-unique",
        "not-flush",
        "low-ace",
        "high-ace",
        "middle-flush",
    ],
)
def test__is_straight(
    card_factory: Factory[Card], values: list[Value], expected: Optional[Value]
) -> None:
    suits = cycle(Suit)
    result = _is_straight(
        [card_factory(suit=suit, value=value) for suit, value in zip(suits, values)]
    )

    assert result == expected


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.TEN, Value.THREE, Value.FOUR, Value.FIVE], False, {}),
        (
            [Value.ACE, Value.KING, Value.TEN, Value.JACK, Value.QUEEN],
            False,
            {"suit": Suit.CLUBS},
        ),
        ([Value.ACE, Value.KING, Value.TEN, Value.JACK, Value.QUEEN], True, {}),
    ],
    ids=[
        "not-flush",
        "royal-flush",
        "flush-not-royal",
    ],
)
def test_is_royal_flush(
    card_factory: Factory[Card],
    values: list[Value],
    different_suits: bool,
    expected: dict[str, Union[str, int]],
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = royal_flush(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = royal_flush(
            Hand(cards=[card_factory(value=value) for value in values])
        )

    assert result == expected


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], True, {}),
        ([Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN], False, {}),
        (
            [Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX],
            False,
            {"high": Value.SIX, "suit": Suit.CLUBS},
        ),
    ],
    ids=[
        "straight-only",
        "flush-only",
        "straight-flush",
    ],
)
def test_is_straight_flush(
    card_factory: Factory[Card],
    values: list[Value],
    different_suits: bool,
    expected: dict[str, Union[str, int]],
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = straight_flush(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = straight_flush(
            Hand(cards=[card_factory(value=value) for value in values])
        )

    assert result == expected


@pytest.mark.parametrize(
    "cards,expected",
    [
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {"value": Value.TWO},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TEN),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {},
        ),
    ],
    ids=[
        "four-of-a-kind",
        "not-four-of-a-kind",
    ],
)
def test_is_four_of_a_kind(
    cards: list[Card], expected: dict[str, Union[str, int]]
) -> None:
    result = four_of_a_kind(Hand(cards=cards))

    assert result == expected


@pytest.mark.parametrize(
    "cards,expected",
    [
        (
            [
                Card(suit=Suit.CLUBS, value=Value.THREE),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.THREE),
            ],
            {"trips": Value.TWO, "pair": Value.THREE},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {},
        ),
    ],
    ids=[
        "full-house",
        "not-full-house",
    ],
)
def test_is_full_house(cards: list[Card], expected: dict[str, Union[str, int]]) -> None:
    result = full_house(Hand(cards=cards))

    assert result == expected


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], True, {}),
        (
            [Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN],
            False,
            {"suit": Suit.CLUBS},
        ),
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], False, {}),
    ],
    ids=[
        "straight-only",
        "flush-only",
        "straight-flush",
    ],
)
def test_is_flush(
    card_factory: Factory[Card],
    values: list[Value],
    different_suits: bool,
    expected: dict[str, Union[str, int]],
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = flush(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = flush(Hand(cards=[card_factory(value=value) for value in values]))

    assert result == expected


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        (
            [Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX],
            True,
            {"high": Value.SIX},
        ),
        ([Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN], False, {}),
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], False, {}),
    ],
    ids=[
        "straight-only",
        "flush-only",
        "straight-flush",
    ],
)
def test_is_straight(
    card_factory: Factory[Card],
    values: list[Value],
    different_suits: bool,
    expected: dict[str, Union[str, int]],
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = straight(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = straight(Hand(cards=[card_factory(value=value) for value in values]))

    assert result == expected


@pytest.mark.parametrize(
    "cards,expected",
    [
        (
            [
                Card(suit=Suit.CLUBS, value=Value.THREE),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.THREE),
            ],
            {},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {"value": Value.TWO},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TEN),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {},
        ),
    ],
    ids=["full-house", "three-of-a-kind", "not-three-of-a-kind"],
)
def test_is_three_of_a_kind(
    cards: list[Card], expected: dict[str, Union[str, int]]
) -> None:
    result = three_of_a_kind(Hand(cards=cards))

    assert result == expected


@pytest.mark.parametrize(
    "cards,expected",
    [
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.THREE),
                Card(suit=Suit.DIAMONDS, value=Value.THREE),
            ],
            {},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.ACE),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {"high": Value.ACE, "low": Value.TWO},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {},
        ),
    ],
    ids=["full-house", "two-pair", "three-of-a-kind"],
)
def test_is_two_pair(cards: list[Card], expected: dict[str, Union[str, int]]) -> None:
    result = two_pair(Hand(cards=cards))

    assert result == expected


@pytest.mark.parametrize(
    "cards,expected",
    [
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.THREE),
                Card(suit=Suit.DIAMONDS, value=Value.THREE),
            ],
            {},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.ACE),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {},
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.KING),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            {"value": Value.TWO},
        ),
    ],
    ids=["full-house", "two-pair", "pair"],
)
def test_is_pair(cards: list[Card], expected: dict[str, Union[str, int]]) -> None:
    result = pair(Hand(cards=cards))

    assert result == expected


def test_high_card(card_factory: Factory[Card]) -> None:
    values = [Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN]
    result = high_card(Hand(cards=[card_factory(value=value) for value in values]))
    assert result == {"value": Value.TEN}
