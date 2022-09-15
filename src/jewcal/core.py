"""Jewish Calendar."""

# https://stackoverflow.com/a/67483317
# Show return type in Sphinx without its full path
from __future__ import annotations

from datetime import date
from typing import Optional, cast

from .models.day import Day


class JewCal:
    """The Jewish Calendar."""

    __slots__ = [
        '__day',
        '__diaspora',
    ]

    def __init__(
        self,
        gregorian: Optional[date] = None,
        diaspora: bool = True
    ) -> None:
        """Create a Jewish calendar with a starting date as the current day.

        Args:
            gregorian: The Gregorian date. Defaults to today.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self.__diaspora = diaspora
        self.day = cast(Day, gregorian if gregorian else date.today())

    def __str__(self) -> str:
        """Get the day as a readable string.

        Returns:
            The day.
        """
        return str(self.__day)

    def __repr__(self) -> str:
        """Get the day as a formal string.

        Returns:
            The day.
        """
        return repr(self.__day)

    @property
    def day(self) -> Day:
        """Get the current day.

        Returns:
            The day.
        ----
        .. # noqa: DAR102 gregorian
        .. # noqa: DAR201 return
        Set the current day.

        Args:
            gregorian: The Gregorian date.
        """
        return self.__day

    @day.setter
    def day(self, gregorian: date) -> None:
        self.__day = Day(gregorian, self.__diaspora)
