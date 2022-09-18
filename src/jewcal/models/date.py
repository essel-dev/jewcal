"""Jewish date model."""

from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum

from ..helpers.dates import DateConverter


class Months(IntEnum):
    """The Jewish months."""

    NISAN = 1
    IYAR = 2
    SIVAN = 3
    TAMUZ = 4
    AV = 5
    ELUL = 6
    TISHREI = 7
    CHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR = 12
    ADAR_2 = 13

    def __str__(self) -> str:
        """Get the month as a readable string.

        Returns:
            The month.
        """
        return self.name.capitalize().replace('_', ' ')


@dataclass(slots=True)
class Date:
    """A date in the Jewish calendar."""

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
        """Create a Jewish date.

        Args:
            gregorian: The Gregorian date.
        """
        converter = DateConverter(gregorian)

        self.gregorian = converter.gregorian
        self.year, self.month, self.day = converter.jewish_date
        self.weekday = converter.jewish_weekday
        self._leap = converter.jewish_leap

    @property
    def month_name(self) -> str:
        """Get the Jewish month name.

        Returns:
            The Jewish month name.
        """
        month = str(Months(self.month))

        if self._leap and self.month == 12:
            month = 'Adar 1'

        return month

    def __str__(self) -> str:
        """Get the Jewish date as a readable string.

        Returns:
            The Jewish date.
        """
        return (
            f'{self.day}'
            f' {self.month_name}'
            f' {self.year}'
            f' ({self.gregorian})'
        )
