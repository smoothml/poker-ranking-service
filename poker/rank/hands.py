from poker.constants import Rank, Value
from poker.models import Card, Hand


def _is_flush(cards: list[Card]) -> bool:
    """Calculate whether hand is a flush."""
    return len(set(card.suit for card in cards)) == 1


def _is_straight(cards: list[Card]) -> bool:
    """Calculate whether hand is a straight."""
    card_values = sorted([card.value for card in cards])

    # If card values are not unique it is not a straight
    if len(set(card_values)) != len(card_values):
        return False

    # Check for a ace low straight
    if card_values == [Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.ACE]:
        return True

    # If all card differences are 1 it is a straight
    diffs = [second - first for first, second in zip(card_values[:-1], card_values[1:])]
    if set(diffs) == {1}:
        return True

    return False


def is_royal_flush(hand: Hand) -> bool:
    """Calculate whether hand a royal flush."""
    if not _is_flush(hand.cards):
        return False

    values = [card.value for card in hand.cards]
    return all(
        value in values
        for value in [Value.ACE, Value.KING, Value.QUEEN, Value.JACK, Value.TEN]
    )


def is_straight_flush(hand: Hand) -> bool:
    """Calculate whether hand a straight flush."""
    return _is_straight(hand.cards) and _is_flush(hand.cards)


def is_four_of_a_kind(hand: Hand) -> bool:
    """Calculate whether hand has four of a kind."""
    return hand.value_counts[0][1] == 4


def is_full_house(hand: Hand) -> bool:
    """Calculate whether hand is a full house."""
    return hand.value_counts[0][1] == 3 and hand.value_counts[1][1] == 2


def is_flush(hand: Hand) -> bool:
    """Calculate whether hand is a flush."""
    return _is_flush(hand.cards) and not _is_straight(hand.cards)


def is_straight(hand: Hand) -> bool:
    """Calculate whether hand is a flush."""
    return _is_straight(hand.cards) and not _is_flush(hand.cards)


def is_three_of_a_kind(hand: Hand) -> bool:
    """Calculate whether hand is a full house."""
    return (
        hand.value_counts[0][1] == 3
        and hand.value_counts[1][1] == 1
        and hand.value_counts[2][1] == 1
    )


def is_two_pair(hand: Hand) -> bool:
    """Calculate whether hand is a two pair."""
    return hand.value_counts[0][1] == 2 and hand.value_counts[1][1] == 2


def is_pair(hand: Hand) -> bool:
    """Calculate whether hand is a pair."""
    return hand.value_counts[0][1] == 2 and hand.value_counts[1][1] == 1


def get_rank(hand: Hand) -> Rank:
    """Get hand rank.

    TODO: Use a factory pattern to avoid this huge flow control.
    """
    if is_royal_flush(hand):
        return Rank.ROYAL_FLUSH
    elif is_straight_flush(hand):
        return Rank.STRAIGHT_FLUSH
    elif is_four_of_a_kind(hand):
        return Rank.FOUR_OF_A_KIND
    elif is_full_house(hand):
        return Rank.FULL_HOUSE
    elif is_flush(hand):
        return Rank.FLUSH
    elif is_straight(hand):
        return Rank.STRAIGHT
    elif is_three_of_a_kind(hand):
        return Rank.THREE_OF_A_KIND
    elif is_two_pair(hand):
        return Rank.TWO_PAIR
    elif is_pair(hand):
        return Rank.PAIR
    else:
        return Rank.HIGH_CARD
