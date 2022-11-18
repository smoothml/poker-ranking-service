from itertools import cycle

import pytest

from poker.constants import Suit, Value
from poker.models import Card, Hand
from poker.rank.hands import (
    _is_flush,
    _is_straight,
    is_flush,
    is_four_of_a_kind,
    is_full_house,
    is_pair,
    is_royal_flush,
    is_straight,
    is_straight_flush,
    is_three_of_a_kind,
    is_two_pair,
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
    card_factory: Factory[Card], suits: list[Suit], expected: bool
) -> None:
    result = _is_flush([card_factory(suit=suit) for suit in suits])

    if expected:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "values,expected",
    [
        ([Value.TWO, Value.TWO, Value.THREE, Value.FOUR, Value.FIVE], False),
        ([Value.THREE, Value.TWO, Value.ACE, Value.TEN, Value.KING], False),
        ([Value.ACE, Value.TWO, Value.THREE, Value.FOUR, Value.FIVE], True),
        ([Value.ACE, Value.KING, Value.TEN, Value.JACK, Value.QUEEN], True),
        ([Value.THREE, Value.FIVE, Value.TWO, Value.FOUR, Value.SIX], True),
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
    card_factory: Factory[Card], values: list[Value], expected: bool
) -> None:
    suits = cycle(Suit)
    result = _is_straight(
        [card_factory(suit=suit, value=value) for suit, value in zip(suits, values)]
    )

    if expected:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.TEN, Value.THREE, Value.FOUR, Value.FIVE], False, False),
        ([Value.ACE, Value.KING, Value.TEN, Value.JACK, Value.QUEEN], False, True),
        ([Value.ACE, Value.KING, Value.TEN, Value.JACK, Value.QUEEN], True, False),
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
    expected: bool,
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = is_royal_flush(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = is_royal_flush(
            Hand(cards=[card_factory(value=value) for value in values])
        )

    if expected:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], True, False),
        ([Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN], False, False),
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], False, True),
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
    expected: bool,
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = is_straight_flush(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = is_straight_flush(
            Hand(cards=[card_factory(value=value) for value in values])
        )

    if expected:
        assert result
    else:
        assert not result


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
            True,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TEN),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            False,
        ),
    ],
    ids=[
        "four-of-a-kind",
        "not-four-of-a-kind",
    ],
)
def test_is_four_of_a_kind(cards: list[Card], expected: bool) -> None:
    result = is_four_of_a_kind(Hand(cards=cards))

    if expected:
        assert result
    else:
        assert not result


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
            True,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.TWO),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            False,
        ),
    ],
    ids=[
        "full-house",
        "not-full-house",
    ],
)
def test_is_full_house(cards: list[Card], expected: bool) -> None:
    result = is_full_house(Hand(cards=cards))

    if expected:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], True, False),
        ([Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN], False, True),
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], False, False),
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
    expected: bool,
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = is_flush(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = is_flush(Hand(cards=[card_factory(value=value) for value in values]))

    if expected:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "values,different_suits,expected",
    [
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], True, True),
        ([Value.TWO, Value.THREE, Value.FIVE, Value.SIX, Value.TEN], False, False),
        ([Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX], False, False),
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
    expected: bool,
) -> None:
    suits = cycle(Suit)

    if different_suits:
        result = is_straight(
            Hand(
                cards=[
                    card_factory(suit=suit, value=value)
                    for suit, value in zip(suits, values)
                ]
            )
        )
    else:
        result = is_straight(
            Hand(cards=[card_factory(value=value) for value in values])
        )

    if expected:
        assert result
    else:
        assert not result


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
            False,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            True,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TEN),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            False,
        ),
    ],
    ids=["full-house", "three-of-a-kind", "not-three-of-a-kind"],
)
def test_is_three_of_a_kind(cards: list[Card], expected: bool) -> None:
    result = is_three_of_a_kind(Hand(cards=cards))

    if expected:
        assert result
    else:
        assert not result


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
            False,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.ACE),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            True,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.TWO),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            False,
        ),
    ],
    ids=["full-house", "two-pair", "three-of-a-kind"],
)
def test_is_two_pair(cards: list[Card], expected: bool) -> None:
    result = is_two_pair(Hand(cards=cards))

    if expected:
        assert result
    else:
        assert not result


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
            False,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.ACE),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            False,
        ),
        (
            [
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.DIAMONDS, value=Value.TWO),
                Card(suit=Suit.HEARTS, value=Value.KING),
                Card(suit=Suit.SPADES, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.THREE),
            ],
            True,
        ),
    ],
    ids=["full-house", "two-pair", "pair"],
)
def test_is_pair(cards: list[Card], expected: bool) -> None:
    result = is_pair(Hand(cards=cards))

    if expected:
        assert result
    else:
        assert not result
