"""Unittests for jewcal.models.jewish_date."""

from datetime import date
from unittest import TestCase

from src.jewcal.models.jewish_date import JewishDate, Month


class MonthTestCase(TestCase):
    """Unittests for Month."""

    def test_month_to_string(self) -> None:
        """Test `Month`-object to `str`."""
        self.assertEqual(str(Month.TISHREI), 'Tishrei')

    def test_month_number_to_enum_member(self) -> None:
        """Test month number to enum member."""
        # non-leap year
        self.assertEqual(Month.get(1, leap=False), Month.NISAN)
        self.assertEqual(Month.get(12, leap=False), Month.ADAR)

        # leap year
        self.assertEqual(Month.get(1, leap=True), Month.NISAN)
        self.assertEqual(Month.get(12, leap=True), Month.ADAR_1)
        self.assertEqual(Month.get(13, leap=True), Month.ADAR_2)


class JewishDateTestCase(TestCase):
    """Unittests for JewishDate."""

    def test_jewcal_to_string(self) -> None:
        """Test `JewCal`-object to `str`."""
        # non-leap year
        date_ = JewishDate(5783, 12, 22, date(2023, 3, 15), _is_leap_year=False)
        self.assertEqual(str(date_), '22 Adar 5783')

        # leap year
        date_ = JewishDate(5782, 1, 15, date(2022, 4, 16), _is_leap_year=True)
        self.assertEqual(str(date_), '15 Nisan 5782')

        date_ = JewishDate(5782, 12, 26, date(2022, 2, 27), _is_leap_year=True)
        self.assertEqual(str(date_), '26 Adar 1 5782')

        date_ = JewishDate(5782, 13, 13, date(2022, 3, 16), _is_leap_year=True)
        self.assertEqual(str(date_), '13 Adar 2 5782')

        date_ = JewishDate(5784, 12, 1, date(2024, 2, 10), _is_leap_year=True)
        self.assertEqual(str(date_), '1 Adar 1 5784')

        date_ = JewishDate(5784, 13, 1, date(2024, 3, 11), _is_leap_year=True)
        self.assertEqual(str(date_), '1 Adar 2 5784')
