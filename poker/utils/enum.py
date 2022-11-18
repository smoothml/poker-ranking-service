from enum import StrEnum
from typing import Any


class AutoName(StrEnum):
    """Use the lower case name as the value for Python Enum (default would be integers).

    Inherits from str to ensure all types are string and as a bonus it becomes JSON
    serializable.

    See here for more information:
    https://docs.python.org/3/library/enum.html#using-automatic-values
    """

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.value)

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> str:
        """Enum standard structure - the next value.

        See this on @staticmethod: https://github.com/python/mypy/issues/7591
        """
        return name.lower()
