from enum import IntEnum, auto

from poker.utils.enum import AutoName


class Suit(AutoName):
    """Card suit enum."""

    CLUBS: auto()
    DIAMONDS: auto()
    HEARTS: auto()
    SPADES: auto()


class Value(IntEnum):
    """Card value enum."""

    ACE = 1
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



