"""Jewish day model."""

from dataclasses import dataclass
from datetime import date as datetime_date
from typing import Final

from ..helpers.calendars import CalendarGenerator, Category, Event
from .date import Date, Months

SHABBAT: Final[dict[int, Event]] = {
    5: Event('Erev Shabbat', [Category.EREV]),
    6: Event('Shabbat', [Category.SHABBAT]),
}


@dataclass
class Day:  # pylint: disable=too-many-instance-attributes
    """A day in the Jewish calendar."""

    __slots__ = [
        '__jewish_date',
        '__erev',
        '__shabbat',
        '__yom_tov',
        '__chol_hamoed',
        '__chag',
        '__rosh_chodesh',
        '__fast',
        '__names',
    ]

    date: Date
    erev: bool
    shabbat: bool
    yom_tov: bool
    chol_hamoed: bool
    chag: bool
    rosh_chodesh: bool
    fast: bool
    names: list[str]

    def __init__(self, gregorian: datetime_date, diaspora: bool) -> None:
        """Create a Jewish day.

        Args:
            gregorian: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self.__jewish_date: Date = Date(gregorian)

        self.__erev: bool = False
        self.__shabbat: bool = False
        self.__yom_tov: bool = False
        self.__chol_hamoed: bool = False
        self.__chag: bool = False
        self.__rosh_chodesh: bool = False
        self.__fast: bool = False

        self.__names: list[str] = []

        events: list[Event] = []
        weekday = self.__jewish_date.weekday

        # shabbat
        if weekday in (5, 6):
            events.append(SHABBAT[weekday])

        # special day
        year = self.__jewish_date.year
        month = Months(self.__jewish_date.month)
        day = self.__jewish_date.day
        calendar = CalendarGenerator(diaspora, year).calendar
        try:
            calendar[month][day]
        except KeyError:
            pass
        else:
            events.extend(calendar[month][day])

        # save in self
        for event in events:
            for category in event.categories:
                attr = f'_Day__{category.name.lower()}'
                if hasattr(self, attr):
                    setattr(self, attr, True)

            self.__names.append(event.name)

    @property  # type: ignore[no-redef]
    def date(self) -> Date:
        """Get the Jewish date.

        Returns:
            The Jewish date.
        """
        return self.__jewish_date

    @property  # type: ignore[no-redef]
    def erev(self) -> bool:
        """Is it the day before Shabbat or Yom Tov.

        Returns:
            True for Erev, False otherwise.
        """
        return self.__erev

    @property  # type: ignore[no-redef]
    def shabbat(self) -> bool:
        """Is it shabbat.

        Returns:
            True for Shabbat, False otherwise.
        """
        return self.__shabbat

    @property  # type: ignore[no-redef]
    def yom_tov(self) -> bool:
        """Is it Yom Tov.

        Returns:
            True for Yom Tov, False otherwise.
        """
        return self.__yom_tov

    @property  # type: ignore[no-redef]
    def chol_hamoed(self) -> bool:
        """Is it Chol HaMoed.

        Returns:
            True for Chol HaMoed, False otherwise.
        """
        return self.__chol_hamoed

    @property  # type: ignore[no-redef]
    def chag(self) -> bool:
        """Is it a Chag.

        Returns:
            True for Chag, False otherwise.
        """
        return self.__chag

    @property  # type: ignore[no-redef]
    def rosh_chodesh(self) -> bool:
        """Is it Rosh Chodesh.

        Returns:
            True for Rosh Chodesh, False otherwise.
        """
        return self.__rosh_chodesh

    @property  # type: ignore[no-redef]
    def fast(self) -> bool:
        """Is it a Fast day.

        Returns:
            True for Fast day, False otherwise.
        """
        return self.__fast

    @property  # type: ignore[no-redef]
    def names(self) -> list[str]:
        """Get the names of the holiday(s) / fast.

        Returns:
            The names.
        """
        return self.__names

    def __str__(self) -> str:
        """Get the day as a readable string.

        Returns:
            The day.
        """
        date: str = f'{str(self.__jewish_date)}'

        names: str = f' {", ".join(self.__names)}' if self.__names else ''

        return f'{date}{names}'
