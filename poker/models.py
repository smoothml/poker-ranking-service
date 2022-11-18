from __future__ import annotations

from pydantic import BaseModel, validator

from poker.constants import Rank, Suit, Value


class Card(BaseModel):
    """Card domain model class."""

    suit: Suit
    value: Value

    def __hash__(self) -> int:
        """Hash function."""
        return hash(f"{self.value} {self.suit}")

    def __le__(self, other: Card) -> bool:
        """Less than or equal to."""
        return self.value <= other.value

    def __lt__(self, other: Card) -> bool:
        """Strictly less than."""
        return self.value < other.value


class Hand(BaseModel):
    """Hand domain model class."""

    cards: list[Card]

    @validator("cards")
    def validate_unique(cls, cards: list[Card]) -> list[Card]:
        """Validate hand comprises unique cards."""
        if len(cards) != len(set(cards)):
            raise ValueError("Hand contains duplicate cards.")
        return cards

    @validator("cards")
    def validate_length(cls, cards: list[Card]) -> list[Card]:
        """Validate hand has five cards."""
        if len(cards) != 5:
            raise ValueError("Hand must have five cards.")
        return cards


class RankedHand(Hand):
    """Ranked hand  domain model class."""

    rank: Rank
    description: str
