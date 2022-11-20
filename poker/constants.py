from enum import IntEnum, auto

from poker.utils.enum import AutoName


class Rank(IntEnum):
    """Poker rank enum."""

    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    PAIR = 9
    HIGH_CARD = 10

    def __str__(self) -> str:
        """Return string representation."""
        out: str = self.name.lower().replace("_", " ").title()
        return out


class Suit(AutoName):
    """Card suit enum."""

    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()


class Value(IntEnum):
    """Card value enum."""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self) -> str:
        """Return string representation."""
        if self.value in [1, 11, 12, 13, 14]:
            out: str = self.name.lower()
        else:
            out = str(self.value)
        return out
