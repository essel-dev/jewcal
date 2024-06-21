"""Jewish date model."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, unique
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date  # pragma: no cover


@unique
class Month(IntEnum):
    """The Jewish months."""

    TISHREI = 7
    CHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR = 12
    ADAR_1 = 14
    ADAR_2 = 13
    NISAN = 1
    IYAR = 2
    SIVAN = 3
    TAMUZ = 4
    AV = 5
    ELUL = 6

    def __str__(self) -> str:
        """Get the month as a readable string.

        Returns:
            The month.
        """
        return self.name.capitalize().replace('_', ' ')

    @classmethod
    def get(cls: type[Month], number: int, *, is_leap: bool) -> Month:
        """Get the enum member.

        Regarding the months Adar, Adar 1 and 2:

        - If the Jewish year is non-leap, it returns Adar.
        - If the Jewish year is leap, it returns Adar 1 or Adar 2.

        Args:
            number: The month number.
            is_leap: Is the Jewish year a leap year.

        Returns:
            The enum member.
        """
        match number:
            case 12:
                return Month.ADAR_1 if is_leap else Month.ADAR
            case _:
                return Month(number)


@dataclass
class JewishDate:
    """The Jewish date."""

    year: int
    """The year in the Jewish calendar."""

    month: int
    """The month in the Jewish year."""

    day: int
    """The day in the Jewish month."""

    gregorian_date: date
    """The date in the Gregorian calendar."""

    _is_leap_year: bool = field(repr=False)
    """Is it a Jewish leap year."""

    def __str__(self) -> str:
        """The Jewish date as a string.

        Returns:
            The Jewish date.
        """
        return (
            f'{self.day}'
            f' {Month.get(self.month, is_leap=self._is_leap_year)}'
            f' {self.year}'
        )
