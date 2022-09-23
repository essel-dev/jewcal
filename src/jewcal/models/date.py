"""Jewish date model."""

from dataclasses import dataclass, field
from datetime import date

from ..helpers.dates import DateConverter
from .enums import Month


@dataclass(slots=True)
class Date:
    """A Jewish date."""

    gregorian: date
    """The Gregorian date."""

    year: int
    """The Jewish year in the range of 1-6000."""

    month: int
    """The Jewish month in the range of 1-13."""

    day: int
    """The Jewish day in the range of 1-30."""

    weekday: int
    """The Jewish weekday in the range of 0-6, where 0 = Sunday."""

    _leap: bool = field(repr=False)
    """Is it a Jewish leap year."""

    def __init__(self, gregorian: date) -> None:
        """Initialize a Jewish date.

        Args:
            gregorian: The Gregorian date.
        """
        converter = DateConverter(gregorian)

        self.gregorian = converter.gregorian
        self.year, self.month, self.day = converter.jewish_date
        self.weekday = converter.jewish_weekday
        self._leap = converter.jewish_leap

    def __str__(self) -> str:
        """Get the Jewish date as a readable string.

        Returns:
            The Jewish date.
        """
        return (
            f'{self.day}'
            f' {Month.get(self.month, self._leap)}'  # Adar 1/2 in leap year
            f' {self.year}'
            f' ({self.gregorian})'
        )
