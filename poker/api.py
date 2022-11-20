from fastapi import Body, FastAPI
from loguru import logger

from poker.constants import Suit, Value
from poker.models import Card, Hand
from poker.rank import rank_hand

app = FastAPI()

_CARD_PATTERN = r"\s".join(5 * ["(2|3|4|5|6|7|8|9|10|J|K|Q|A)[CDHS]"])
_SUIT_MAP = {
    "C": Suit.CLUBS,
    "D": Suit.DIAMONDS,
    "H": Suit.HEARTS,
    "S": Suit.SPADES,
}
_VALUE_MAP = {
    "2": Value.TWO,
    "3": Value.THREE,
    "4": Value.FOUR,
    "5": Value.FIVE,
    "6": Value.SIX,
    "7": Value.SEVEN,
    "8": Value.EIGHT,
    "9": Value.NINE,
    "10": Value.TEN,
    "J": Value.JACK,
    "Q": Value.QUEEN,
    "K": Value.KING,
    "A": Value.ACE,
}


@app.get("/")
async def health_check() -> str:
    """Health check endpoint."""
    return "OK"


@app.post("/rank")
def rank(body: str = Body(regex=_CARD_PATTERN, example="2H 3D 5S 10C KD")) -> str:
    """Rank hand.

    TODO: Improve error response.
    """
    logger.info(f"Input hand: {body}")
    cards = [
        Card(suit=_SUIT_MAP[card[-1]], value=_VALUE_MAP[card[:-1]])
        for card in body.split()
    ]

    ranked_hand = rank_hand(Hand(cards=cards))

    logger.info(f"Hand rank: {ranked_hand.rank}")

    return ranked_hand.description
