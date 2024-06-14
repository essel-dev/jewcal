"""Jewish calendar calculations in Python.

`Absolute date` means the number of days elapsed since the Gregorian date
Sunday, December 31, 1 BCE. (Since there was no year 0, the year following
1 BCE is 1 CE.) Thus the Gregorian date January 1, 1 CE is absolute date
number 1.

Source code Copyright © by Ulrich and David Greve (2005)
https://www.david-greve.de/luach-code/jewish-python.html
"""

from calendar import isleap, monthrange
from datetime import date

TISHREI = 7

# Calculated date of the world's creation, is equivalent to sunset on the Julian
# proleptic calendar date 6 October 3761 BCE
JEWISH_EPOCH = 1373429

# Moon's 19 year cycle where the Moon returns to the same place
METONIC_CYCLE = 19


def is_gregorian_leap(year: int) -> bool:
    """Is the Gregorian year a leap year.

    97 leap years occur every 400 years so that every year divisible by 4 is a
    leap year, except if it is divisible by 100 and not divisible by 400.

    Args:
        year: The Gregorian year.

    Returns:
        True for leap year, False otherwise.
    """
    return isleap(year)


def is_jewish_leap(year: int) -> bool:
    """Is the Jewish year a leap year.

    Jewish years have 12 months in a regular year and 13 in a leap year.
    Leap years occur on the 3rd, 6th, 8th, 11th, 14th, 17th, and 19th years of
    the Metonic cycle. This is the Moon's 19 year cycle where the Moon returns
    to exactly the same place (at the same longitude and against the same
    constellation) in the sky with the same phase.

    Args:
        year: The Jewish year.

    Returns:
        True for leap year, False otherwise.
    """
    return bool((((year * 7) + 1) % METONIC_CYCLE) < 7)  # noqa: PLR2004


def days_in_gregorian_month(month: int, year: int) -> int:
    """Get the number of days in a Gregorian month.

    Args:
        month: The Gregorian month.
        year: The Gregorian year.

    Returns:
         The number of days.
    """
    return monthrange(year, month)[1]


def days_in_jewish_year(year: int) -> int:
    """Get the number of days in a Jewish year.

    This is calculated as the difference between the elapsed days in
    successive years.

    Args:
        year: The Jewish year.

    Returns:
        The number of days.
    """
    return _first_day_of_jewish_year(year + 1) - _first_day_of_jewish_year(year)


def days_in_jewish_month(year: int, month: int) -> int:
    """Get the number of days in a Jewish month.

    Args:
        year: The Jewish year.
        month: The Jewish month.

    Returns:
        The number of days.
    """
    match month:
        case 2 | 4 | 6 | 10 | 13:
            return 29
        case 12:
            if not is_jewish_leap(year):
                return 29
        case 8:
            if not _is_long_cheshvan(year):
                return 29
        case 9:
            if _is_short_kislev(year):
                return 29

    return 30


def months_in_jewish_year(year: int) -> int:
    """Get the number of months in a Jewish year.

    Args:
        year: The Jewish year.

    Returns:
        The number of months.
    """
    if is_jewish_leap(year):
        return 13

    return 12


def gregorian_to_absdate(year: int, month: int, day: int) -> int:
    """Convert the Gregorian date to an absolute date number.

    Args:
        year: The Gregorian year.
        month: The Gregorian month.
        day: The Gregorian day.

    Returns:
        The absolute date number.
    """
    return date(year, month, day).toordinal()


def jewish_to_absdate(year: int, month: int, day: int) -> int:
    """Convert the Jewish date to an absolute date number.

    Args:
        year: The Jewish year.
        month: The Jewish month.
        day: The Jewish day.

    Returns:
        The absolute date number.
    """
    # Days so far this month.
    value = day
    return_value = value

    # If before Tishrei
    if month < TISHREI:
        # add days in prior months this year before and after Nisan.
        for i in range(TISHREI, months_in_jewish_year(year) + 1):
            value = days_in_jewish_month(year, i)
            return_value += value
        for i in range(1, month):
            value = days_in_jewish_month(year, i)
            return_value += value
    else:
        for i in range(TISHREI, month):
            value = days_in_jewish_month(year, i)
            return_value += value

    # Days in prior years.
    value = _first_day_of_jewish_year(year)
    return_value += value

    # Days elapsed before absolute date 1.
    value = JEWISH_EPOCH
    return_value -= value

    return return_value


def absdate_to_gregorian(absdate: int) -> tuple[int, int, int]:
    """Convert the absolute date number to a Gregorian date.

    Args:
        absdate: The absolute date number.

    Returns:
        A tuple with the Gregorian year, month and day.
    """
    gregorian = date.fromordinal(absdate)

    return (gregorian.year, gregorian.month, gregorian.day)


def absdate_to_jewish(absdate: int) -> tuple[int, int, int]:
    """Convert the absolute date number to a Jewish date.

    Args:
        absdate: The absolute date number.

    Returns:
        A tuple with the Jewish year, month and day.
    """
    approx = (absdate + JEWISH_EPOCH) // 366

    year_temp = approx
    while 1:
        absdate_temp = jewish_to_absdate(year_temp + 1, 7, 1)
        if absdate < absdate_temp:
            break
        year_temp += 1
    year = year_temp

    absdate_temp = jewish_to_absdate(year, 1, 1)
    start = 7 if absdate < absdate_temp else 1

    month_temp = start
    while 1:
        absdate_temp = jewish_to_absdate(
            year,
            month_temp,
            days_in_jewish_month(year, month_temp),
        )
        if absdate <= absdate_temp:
            break
        month_temp += 1
    month = month_temp

    absdate_temp = jewish_to_absdate(year, month, 1)
    day = absdate - absdate_temp + 1

    return (year, month, day)


def weekday_from_absdate(absdate: int) -> int:
    """Get the weekday for the absolute date number.

    Args:
        absdate: The absolute date number.

    Returns:
        The weekday number in the range of 0-6, where 0=Sunday.
    """
    return absdate % 7


def _first_day_of_jewish_year(year: int) -> int:
    # pylint: disable-next=line-too-long
    """Get the first day of the Jewish year as an absolute date number.

    There are 4 possibilities when the Jewish year starts:
    https://en.wikibooks.org/wiki/Mathematics_of_the_Jewish_Calendar/The_four_postponements_of_the_New_Year

    Args:
        year: The Jewish year.

    Returns:
        The absolute date number.
    """
    # Months in complete cycles so far.
    value = 235 * ((year - 1) // METONIC_CYCLE)
    months_elapsed = value

    # Regular months in this cycle.
    value = 12 * ((year - 1) % METONIC_CYCLE)
    months_elapsed += value

    # Leap months this cycle.
    value = ((((year - 1) % METONIC_CYCLE) * 7) + 1) // METONIC_CYCLE

    months_elapsed += value

    parts_elapsed = ((months_elapsed % 1080) * 793) + 204

    hours_elapsed = (
        5
        + (months_elapsed * 12)
        + ((months_elapsed // 1080) * 793)
        + (parts_elapsed // 1080)
    )

    # Conjunction day.
    day = 1 + (29 * months_elapsed) + (hours_elapsed // 24)

    # Conjunction parts.
    parts = ((hours_elapsed % 24) * 1080) + (parts_elapsed % 1080)

    if any(
        [
            (parts >= 19440),  # new moon is at or after midday  # noqa: PLR2004
            all(
                [
                    ((day % 7) == 2),  # or is on a Tuesday  # noqa: PLR2004
                    (
                        parts >= 9924  # noqa: PLR2004
                    ),  # and at 9 hours, 204 parts or later
                    (not is_jewish_leap(year)),  # and of a common year
                ],
            ),
            all(
                [
                    ((day % 7) == 1),  # or is on a Monday
                    (
                        parts >= 16789  # noqa: PLR2004
                    ),  # and at 15 hours, 589 parts or later
                    (is_jewish_leap(year - 1)),  # and at the end of a leap year
                ],
            ),
        ],
    ):
        alternative_day = day + 1  # postpone Rosh Hashana one day
    else:
        alternative_day = day

    # if Rosh Hashana starts on Sunday, Wednesday or Friday
    if alternative_day % 7 in [0, 3, 5]:
        alternative_day += 1  # postpone it one (more) day

    return alternative_day


def _is_long_cheshvan(year: int) -> bool:
    """Is Cheshvan a long month.

    Cheshvan is the eighth month of the Jewish year and the number of days
    can vary.

    Args:
        year: The Jewish year.

    Returns:
         True for long, False otherwise.
    """
    return bool((days_in_jewish_year(year) % 10) == 5)  # noqa: PLR2004


def _is_short_kislev(year: int) -> bool:
    """Is Kislev a short month.

    Kislev is the ninth month of the Jewish year and the number of days can
    vary.

    Args:
        year: The Jewish year.

    Returns:
         True for short, False otherwise.
    """
    return bool((days_in_jewish_year(year) % 10) == 3)  # noqa: PLR2004
