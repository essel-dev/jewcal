"""Unittests for jewcal.core."""

from datetime import date
from unittest import TestCase

from src.jewcal.core import JewCal
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
