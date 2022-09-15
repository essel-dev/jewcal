"""Jewish date model."""

from dataclasses import dataclass
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


@dataclass
class Date:  # pylint: disable=too-many-instance-attributes
    """A date in the Jewish calendar."""

    __slots__ = [
        '__gregorian',
        '__year',
        '__month',
        '__day',
        '__weekday',
        '__leap',
    ]

    gregorian: date
    year: int
    month: int
    day: int
    weekday: int

    def __init__(self, gregorian: date) -> None:
        """Create a Jewish date.

        Args:
            gregorian: The Gregorian date.
        """
        converter = DateConverter(gregorian)

        self.__gregorian: date = converter.gregorian

        year, month, day = converter.jewish_date
        self.__year: int = year
        self.__month: int = month
        self.__day: int = day

        self.__weekday: int = converter.jewish_weekday

        self.__leap: bool = converter.jewish_leap

    @property  # type: ignore[no-redef]
    def gregorian(self) -> date:
        """Get the Gregorian date.

        Returns:
            The Gregorian date.
        """
        return self.__gregorian

    @property  # type: ignore[no-redef]
    def year(self) -> int:
        """Get the Jewish year.

        Returns:
            The Jewish year in the range of 1-6000.
        """
        return self.__year

    @property  # type: ignore[no-redef]
    def month(self) -> int:
        """Get the Jewish month number.

        Returns:
            The Jewish month in the range of 1-13.
        """
        return self.__month

    @property
    def month_name(self) -> str:
        """Get the Jewish month name.

        Returns:
            The Jewish month name.
        """
        month = str(Months(self.__month))

        if self.__leap and self.__month == 12:
            month = 'Adar 1'

        return month

    @property  # type: ignore[no-redef]
    def day(self) -> int:
        """Get the Jewish day number.

        Returns:
            The Jewish day in the range of 1-30.
        """
        return self.__day

    @property  # type: ignore[no-redef]
    def weekday(self) -> int:
        """Get the Jewish weekday number.

        Returns:
            The Jewish weekday in the range of 0-6, where 0 = Sunday.
        """
        return self.__weekday

    def __str__(self) -> str:
        """Get the Jewish date as a readable string.

        Returns:
            The Jewish date.
        """
        return (
            f'{self.__day}'
            f' {self.month_name}'
            f' {self.__year}'
            f' ({self.__gregorian})'
        )
