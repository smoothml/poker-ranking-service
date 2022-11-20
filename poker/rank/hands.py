from typing import Optional, Union

from poker.constants import Rank, Value
from poker.models import Card, Hand, RankedHand
from poker.rank.descriptions import DESCRIPTIONS


def _is_flush(cards: list[Card]) -> bool:
    """Calculate whether hand is a flush."""
    return len(set(card.suit for card in cards)) == 1


def _is_straight(cards: list[Card]) -> Optional[Value]:
    """Calculate whether hand is a straight.

    Arguments:
        cards: List of cards in hand.

    Returns:
        High card if hand is a straight, None otherwise.
    """
    card_values = sorted([card.value for card in cards])

    # If card values are not unique it is not a straight
    if len(set(card_values)) != len(card_values):
        return None

    # Check for a ace low straight
    if card_values == [Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.ACE]:
        return Value.FIVE

    # If all card differences are 1 it is a straight
    diffs = [second - first for first, second in zip(card_values[:-1], card_values[1:])]
    if set(diffs) == {1}:
        return max(cards).value

    return None


def royal_flush(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand a royal flush."""
    if not _is_flush(hand.cards):
        return {}

    values = [card.value for card in hand.cards]
    _is = all(
        value in values
        for value in [Value.ACE, Value.KING, Value.QUEEN, Value.JACK, Value.TEN]
    )
    if _is:
        return {"suit": hand.cards[0].suit}

    return {}


def straight_flush(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand a straight flush."""
    high = _is_straight(hand.cards)
    if high is not None and _is_flush(hand.cards):
        return {
            "high": high,
            "suit": hand.cards[0].suit,
        }

    return {}


def four_of_a_kind(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand has four of a kind."""
    if hand.value_counts[0][1] == 4:
        return {"value": hand.value_counts[0][0]}

    return {}


def full_house(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand is a full house."""
    if hand.value_counts[0][1] == 3 and hand.value_counts[1][1] == 2:
        return {
            "trips": hand.value_counts[0][0],
            "pair": hand.value_counts[1][0],
        }

    return {}


def flush(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand is a flush."""
    high = _is_straight(hand.cards)
    if _is_flush(hand.cards) and high is None:
        return {"suit": hand.cards[0].suit}

    return {}


def straight(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand is a flush."""
    high = _is_straight(hand.cards)
    if high is not None and not _is_flush(hand.cards):
        return {"high": high}

    return {}


def three_of_a_kind(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand is a full house."""
    if (
        hand.value_counts[0][1] == 3
        and hand.value_counts[1][1] == 1
        and hand.value_counts[2][1] == 1
    ):
        return {"value": hand.value_counts[0][0]}

    return {}


def two_pair(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand is a two pair."""
    if hand.value_counts[0][1] == 2 and hand.value_counts[1][1] == 2:
        values = [hand.value_counts[0][0], hand.value_counts[1][0]]
        return {
            "high": max(values),
            "low": min(values),
        }

    return {}


def pair(hand: Hand) -> dict[str, Union[str, int]]:
    """Calculate whether hand is a pair."""
    if hand.value_counts[0][1] == 2 and hand.value_counts[1][1] == 1:
        return {"value": hand.value_counts[0][0]}

    return {}


def high_card(hand: Hand) -> dict[str, Union[str, int]]:
    """Get high card."""
    return {"value": max(hand.cards).value}


_FUNCTIONS = {
    Rank.ROYAL_FLUSH: royal_flush,
    Rank.STRAIGHT_FLUSH: straight_flush,
    Rank.FOUR_OF_A_KIND: four_of_a_kind,
    Rank.FULL_HOUSE: full_house,
    Rank.FLUSH: flush,
    Rank.STRAIGHT: straight,
    Rank.THREE_OF_A_KIND: three_of_a_kind,
    Rank.TWO_PAIR: two_pair,
    Rank.PAIR: pair,
    Rank.HIGH_CARD: high_card,
}


def rank_hand(hand: Hand) -> RankedHand:
    """Get hand rank.

    TODO: Use a factory pattern to avoid this huge flow control.
    """
    out = None
    for rank, func in _FUNCTIONS.items():
        result = func(hand)
        if result:
            out = RankedHand(
                cards=hand.cards,
                rank=rank,
                description=DESCRIPTIONS[rank].format(**result),
            )

    if out is None:
        raise ValueError("No rank found.")

    return out
