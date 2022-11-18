from pydantic import BaseModel, Field

from poker.constants import Suit, Value


class Card(BaseModel):
    """Card domain model class."""

    suit: Suit
    value: Value


class Hand(BaseModel):
    """Hand domain model class."""

    cards: list[Card] = Field(..., min_length=5, max_length=5)
