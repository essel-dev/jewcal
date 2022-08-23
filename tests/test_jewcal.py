"""Unittests for jewcal."""

from datetime import date
from unittest import TestCase

from src.jewcal import Jewcal
from src.jewcal.constants import Category


class JewcalTestCase(TestCase):
    """Unittests for jewcal."""

    def setUp(self) -> None:
        """Initialize."""

    def tearDown(self) -> None:
        """Clean up after tests."""

    def test_create_jewish_date(self) -> None:
        """Create new date."""
        gregorian_date = date(2022, 8, 14)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

    def test_create_jewish_date_yomtov_candles(self) -> None:
        """Create new date and it is a yom tov with candles as category."""
        gregorian_date = date(2022, 4, 16)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, 'Shabbos')
        self.assertEqual(jewcal.yomtov, 'Pesach 1')  # first day on Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES.value)

    def test_create_jewish_date_yomtov_havdalah(self) -> None:
        """Create new date and it is a yom tov with havdalah as category."""
        gregorian_date = date(2022, 4, 17)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, 'Pesach 2')
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)

    def test_create_jewish_date_erev_shabbos(self) -> None:
        """Create new date and it is erev shabbos with candles as category."""
        gregorian_date = date(2022, 8, 19)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, 'Erev Shabbos')
        self.assertEqual(jewcal.category, Category.CANDLES.value)
        self.assertIsNone(jewcal.yomtov)

    def test_create_jewish_date_shabbos(self) -> None:
        """Create new date and it is shabbos with havdalah as category."""
        gregorian_date = date(2022, 8, 20)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, 'Shabbos')
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertIsNone(jewcal.yomtov)

    def test_jewcal_to_string(self) -> None:
        """Test `Jewcal`-object to `str`."""
        jewcal = Jewcal(date(2022, 4, 16))
        self.assertEqual(str(jewcal), '15 Nisan 5782')
