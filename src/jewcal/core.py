"""Jewish Calendar."""

# https://stackoverflow.com/a/67483317
# Show return type in Sphinx without its full path
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from .models.day import Day


@dataclass(slots=True)
class JewCal:
    """The Jewish Calendar."""

    day: Day
    """The current day in the Jewish calendar."""

    _diaspora: bool = field(repr=False)
    """Is the calendar for Diaspora."""

    def __init__(
        self,
        gregorian: Optional[date] = None,
        diaspora: bool = True
    ) -> None:
        """Create a Jewish calendar with a starting Gregorian date.

        Args:
            gregorian: The Gregorian date. Default is today.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self._diaspora = diaspora
        self.date(gregorian if gregorian is not None else date.today())

    def __str__(self) -> str:
        """Get the current calendar day as a readable string.

        Returns:
            The calendar day.
        """
        return str(self.day)

    def date(self, gregorian: date) -> None:
        """Set the current date.

        Args:
            gregorian: The Gregorian date.
        """
        self.day = Day(gregorian, self._diaspora)
