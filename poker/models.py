from pydantic import BaseModel, validator

from poker.constants import Suit, Value


class Card(BaseModel):
    """Card domain model class."""

    suit: Suit
    value: Value

    def __hash__(self) -> int:
        """Hash function."""
        return hash(f"{self.value} {self.suit}")


HandType = tuple[Card, Card, Card, Card, Card]


class Hand(BaseModel):
    """Hand domain model class."""

    cards: HandType

    @validator("cards")
    def validate_unique(cls, cards: HandType) -> HandType:
        """Validate hand comprises unique cards."""
        if len(cards) != len(set(cards)):
            raise ValueError("Hand contains duplicate cards.")
        return cards
