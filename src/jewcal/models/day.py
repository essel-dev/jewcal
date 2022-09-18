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


@dataclass(slots=True)
class DayCategories:
    """The different categories of holidays / fast."""

    erev: bool = False
    """Is it the day before Shabbat or Yom Tov."""

    shabbat: bool = False
    """Is it Shabbat."""

    yom_tov: bool = False
    """Is it Yom Tov."""

    chol_hamoed: bool = False
    """Is it Chol HaMoed."""

    chag: bool = False
    """Is it a Chag."""

    rosh_chodesh: bool = False
    """Is it Rosh Chodesh."""

    fast: bool = False
    """Is it a Fast day."""


@dataclass(slots=True)
class Day:
    """A day in the Jewish calendar.

    A day has categories and names for holidays and fasts.
    """

    date: Date
    """The Jewish date."""

    categories: DayCategories
    """The categories."""

    names: list[str]
    """The holiday names."""

    def __init__(self, gregorian: datetime_date, diaspora: bool) -> None:
        """Create a Jewish day.

        Args:
            gregorian: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self.date = Date(gregorian)
        self.categories = DayCategories()
        self.names = []

        events: list[Event] = []
        weekday = self.date.weekday

        # shabbat
        if weekday in (5, 6):
            events.append(SHABBAT[weekday])

        # special day
        year = self.date.year
        month = Months(self.date.month)
        day = self.date.day
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
                attr = f'{category.name.lower()}'
                setattr(self.categories, attr, True)

            self.names.append(event.name)

    def __str__(self) -> str:
        """Get the day as a readable string.

        Returns:
            The day.
        """
        date: str = f'{str(self.date)}'

        names: str = f' {", ".join(self.names)}' if self.names else ''

        return f'{date}{names}'
