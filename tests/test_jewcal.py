"""Unittests for jewcal."""

from datetime import date
from unittest import TestCase

from src.jewcal import Jewcal
from src.jewcal.constants import SHABBOS, YOMTOV, Category


class JewcalTestCase(TestCase):
    """Unittests for jewcal."""

    def setUp(self) -> None:
        """Initialize."""

    def tearDown(self) -> None:
        """Clean up after tests."""

    def test_no_shabbos_and_yom_tov(self) -> None:
        """Create a new date."""
        gregorian_date = date(2022, 8, 14)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

    def test_yomtov_candles(self) -> None:
        """It is a Yom Tov with candles as category."""
        gregorian_date = date(2022, 4, 16)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.yomtov, YOMTOV[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.category, Category.CANDLES.value)

    def test_yomtov_havdalah(self) -> None:
        """It is a Yom Tov with havdalah as category."""
        gregorian_date = date(2022, 4, 17)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, YOMTOV[1][16].title)  # Pesach 2
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)

    def test_erev_shabbos(self) -> None:
        """It is Erev Shabbos with candles as category."""
        gregorian_date = date(2022, 8, 19)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES.value)
        self.assertIsNone(jewcal.yomtov)

    def test_shabbos(self) -> None:
        """It is Shabbos with havdalah as category."""
        gregorian_date = date(2022, 8, 20)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertIsNone(jewcal.yomtov)

    def test_shabbos_chol_hamoed_sukkos(self) -> None:
        """It is Shabbos Chol Hamoed Sukkos with havdalah as category."""
        gregorian_date = date(2021, 9, 25)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV[7][19].title)  # Ch'H Sukkos 5

    def test_shabbos_chol_hamoed_pesach(self) -> None:
        """It is Shabbos Chol Hamoed Pesach with havdalah as category."""
        gregorian_date = date(2020, 4, 11)
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV[1][17].title)  # Ch'H Pesach 3

    def test_jewcal_to_string(self) -> None:
        """Test `Jewcal`-object to `str`."""
        jewcal = Jewcal(date(2022, 4, 16))
        self.assertEqual(str(jewcal), '15 Nisan 5782')
