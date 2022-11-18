import pytest
from pydantic import ValidationError

from poker.constants import Value
from poker.models import Card, Hand
from tests.conftest import Factory


def test_hand_should_contain_unique_cards(card_factory: Factory[Card]) -> None:
    cards = [
        Value.ACE,
        Value.TWO,
        Value.THREE,
        Value.FOUR,
    ]
    with pytest.raises(ValidationError):
        _ = Hand(
            cards=tuple(card_factory(value=value) for value in cards + [Value.FOUR])
        )

    _ = Hand(cards=tuple(card_factory(value=value) for value in cards + [Value.FIVE]))
