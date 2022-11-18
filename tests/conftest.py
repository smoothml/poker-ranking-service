from typing import Any, Callable, TypeVar

import pytest
from mypy_extensions import KwArg

from poker.constants import Suit, Value
from poker.models import Card

T = TypeVar("T")
Factory = Callable[[KwArg(Any)], T]


@pytest.fixture(scope="session")
def card_factory() -> Factory[Card]:
    """Get Card object factory."""
    default = {
        "suit": Suit.CLUBS,
        "value": Value.ACE,
    }

    def factory(**kwargs: Any) -> Card:
        return Card(**(default | kwargs))

    return factory
