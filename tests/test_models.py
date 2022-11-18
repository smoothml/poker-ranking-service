import pytest
from pydantic import ValidationError

from poker.constants import Suit, Value
from poker.models import Card, Hand


def test_hand_should_contain_unique_cards() -> None:
    with pytest.raises(ValidationError):
        _ = Hand(
            cards=(
                Card(suit=Suit.CLUBS, value=Value.ACE),
                Card(suit=Suit.CLUBS, value=Value.TWO),
                Card(suit=Suit.CLUBS, value=Value.THREE),
                Card(suit=Suit.CLUBS, value=Value.FOUR),
                Card(suit=Suit.CLUBS, value=Value.FOUR),
            )
        )

    _ = Hand(
        cards=(
            Card(suit=Suit.CLUBS, value=Value.ACE),
            Card(suit=Suit.CLUBS, value=Value.TWO),
            Card(suit=Suit.CLUBS, value=Value.THREE),
            Card(suit=Suit.CLUBS, value=Value.FOUR),
            Card(suit=Suit.CLUBS, value=Value.FIVE),
        )
    )
