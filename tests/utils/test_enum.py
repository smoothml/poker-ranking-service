from enum import auto

from poker.utils.enum import AutoName


def test_auto_name() -> None:
    class Example(AutoName):
        """Example Enum."""

        foo = auto()
        BAR = auto()
        WeIrD = auto()

    assert Example.foo.value == "foo"
    assert Example.BAR.value == "bar"
    assert Example.WeIrD.value == "weird"
