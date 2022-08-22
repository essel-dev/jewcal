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
        jewcal = Jewcal(date(2022, 8, 14))
        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

    def test_create_jewish_date_yomtov_candles(self) -> None:
        """Create new date and it is a yom tov with candles as category."""
        jewcal = Jewcal(date(2022, 4, 16))
        self.assertEqual(jewcal.shabbos, 'Shabbos')
        self.assertEqual(jewcal.yomtov, 'Pesach 1')  # first day on Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES)

    def test_create_jewish_date_yomtov_havdalah(self) -> None:
        """Create new date and it is a yom tov with havdalah as category."""
        jewcal = Jewcal(date(2022, 4, 17))
        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, 'Pesach 2')
        self.assertEqual(jewcal.category, Category.HAVDALAH)

    def test_create_jewish_date_erev_shabbos(self) -> None:
        """Create new date and it is erev shabbos with candles as category."""
        jewcal = Jewcal(date(2022, 8, 19))
        self.assertEqual(jewcal.shabbos, 'Erev Shabbos')
        self.assertEqual(jewcal.category, Category.CANDLES)
        self.assertIsNone(jewcal.yomtov)

    def test_create_jewish_date_shabbos(self) -> None:
        """Create new date and it is shabbos with havdalah as category."""
        jewcal = Jewcal(date(2022, 8, 20))
        self.assertEqual(jewcal.shabbos, 'Shabbos')
        self.assertEqual(jewcal.category, Category.HAVDALAH)
        self.assertIsNone(jewcal.yomtov)

    def test_jewcal_to_string(self) -> None:
        """Test `Jewcal`-object to `str`."""
        jewcal = Jewcal(date(2022, 4, 16))
        self.assertEqual(str(jewcal), '15 Nisan 5782')

    def test_jewcal_to_repr(self) -> None:
        """Test `Jewcal`-object to `repr`."""
        jewcal = Jewcal(date(2022, 8, 18))
        self.assertEqual(
            repr(jewcal),
            'Jewcal(year=5782, month=5, day=21, shabbos=None,'
            ' yomtov=None, category=None)'
        )
