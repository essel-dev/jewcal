"""Unittests for jewcal.core."""

from datetime import date, timedelta
from unittest import TestCase

from src.jewcal.core import JewCal
from src.jewcal.models.date import Date
from src.jewcal.models.day import Day


class JewCalTestCase(TestCase):
    """Unittests for `JewCal`."""

    def test__init__(self) -> None:
        """Test __init__."""
        gregorian = date(2022, 9, 1)
        jewcal = JewCal(gregorian)

        jewish_day = Day(gregorian, True)

        self.assertEqual(jewcal.day, jewish_day)

    def test__str__(self) -> None:
        """Test __str__."""
        gregorian = date(2022, 4, 16)
        jewcal = JewCal(gregorian)

        jewish_day = Day(gregorian, True)

        self.assertEqual(str(jewcal), str(jewish_day))

    def test_day(self) -> None:
        """Test get the current day."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        self.assertEqual(jewcal.day, Day(gregorian, True))

    def test_set_day(self) -> None:
        """Test set the current day."""
        jewcal = JewCal(date(2022, 9, 5))

        gregorian = date(2022, 9, 7)
        jewcal.date(gregorian)

        self.assertEqual(jewcal.day, Day(gregorian, True))

    def test_next_day(self) -> None:
        """Test get the next day."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        self.assertEqual(
            jewcal.days(1), [Day(gregorian + timedelta(days=1), True)]
        )

    def test_next_days(self) -> None:
        """Test get the next several days."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        self.assertEqual(
            jewcal.days(5),
            [
                Day(gregorian + timedelta(days=1), True),
                Day(gregorian + timedelta(days=2), True),
                Day(gregorian + timedelta(days=3), True),
                Day(gregorian + timedelta(days=4), True),
                Day(gregorian + timedelta(days=5), True),
            ],
        )

    def test_past_day(self) -> None:
        """Test get the past day."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        self.assertEqual(
            jewcal.days(-1), [
                Day(gregorian - timedelta(days=1), True)]
        )

    def test_past_days(self) -> None:
        """Test get several past days."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        self.assertEqual(
            jewcal.days(-5),
            [
                Day(gregorian - timedelta(days=5), True),
                Day(gregorian - timedelta(days=4), True),
                Day(gregorian - timedelta(days=3), True),
                Day(gregorian - timedelta(days=2), True),
                Day(gregorian - timedelta(days=1), True),
            ],
        )

    def test_days_fail(self) -> None:
        """Test get days should fail."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        with self.assertRaises(TypeError) as c_m:
            jewcal.days(0.1)  # type: ignore[arg-type]

        self.assertEqual(
            'unsupported type float', str(c_m.exception)
        )

        with self.assertRaises(ValueError) as c_m:  # type: ignore[assignment]
            jewcal.days(0)
        self.assertEqual(
            'days must be positive or negative',
            str(c_m.exception)
        )

    def test_current_week(self) -> None:
        """Test get the current week."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        self.assertEqual(
            jewcal.current_week(),
            [
                Day(gregorian - timedelta(days=1), True),
                Day(gregorian, True),
                Day(gregorian + timedelta(days=1), True),
                Day(gregorian + timedelta(days=2), True),
                Day(gregorian + timedelta(days=3), True),
                Day(gregorian + timedelta(days=4), True),
                Day(gregorian + timedelta(days=5), True),
            ],
        )

    def test_next_week(self) -> None:
        """Test get the next week."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        next_sunday = 7 - Date(gregorian).weekday

        self.assertEqual(
            jewcal.weeks(1),
            [
                Day(gregorian + timedelta(days=next_sunday), True),
                Day(gregorian + timedelta(days=next_sunday + 1), True),
                Day(gregorian + timedelta(days=next_sunday + 2), True),
                Day(gregorian + timedelta(days=next_sunday + 3), True),
                Day(gregorian + timedelta(days=next_sunday + 4), True),
                Day(gregorian + timedelta(days=next_sunday + 5), True),
                Day(gregorian + timedelta(days=next_sunday + 6), True),
            ]
        )

    def test_next_weeks(self) -> None:
        """Test get the next several weeks."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        next_sunday = (
            gregorian
            - timedelta(days=Date(gregorian).weekday)
            + timedelta(weeks=1)
        )

        days = jewcal.weeks(2)

        self.assertEqual(
            days[0],
            Day(next_sunday, True),
        )

        self.assertEqual(
            days[13], Day(next_sunday + timedelta(days=13), True)
        )

    def test_past_week(self) -> None:
        """Test get the past week."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        this_sunday = gregorian - timedelta(days=Date(gregorian).weekday)

        self.assertEqual(
            jewcal.weeks(-1),
            [
                Day(this_sunday - timedelta(days=7), True),
                Day(this_sunday - timedelta(days=6), True),
                Day(this_sunday - timedelta(days=5), True),
                Day(this_sunday - timedelta(days=4), True),
                Day(this_sunday - timedelta(days=3), True),
                Day(this_sunday - timedelta(days=2), True),
                Day(this_sunday - timedelta(days=1), True),
            ],
        )

    def test_past_weeks(self) -> None:
        """Test get several past weeks."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        this_sunday = gregorian - timedelta(days=Date(gregorian).weekday)

        days = jewcal.weeks(-3)

        self.assertEqual(
            days[0], Day(this_sunday - timedelta(days=21), True)
        )

        self.assertEqual(
            days[20], Day(this_sunday - timedelta(days=1), True)
        )

    def test_weeks_fail(self) -> None:
        """Test get weeks should fail."""
        gregorian = date(2022, 9, 5)
        jewcal = JewCal(gregorian)

        with self.assertRaises(TypeError) as c_m:
            jewcal.weeks(0.1)  # type: ignore[arg-type]
        self.assertEqual(
            'unsupported type float',
            str(c_m.exception)
        )

        with self.assertRaises(ValueError) as c_m:  # type: ignore[assignment]
            jewcal.weeks(0)
        self.assertEqual(
            'weeks must be positive or negative',
            str(c_m.exception)
        )
