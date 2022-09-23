"""Unittests for jewcal.models.enums."""

from unittest import TestCase

from src.jewcal.models.enums import Month


class MonthEnumTestCase(TestCase):
    """Unittests for `Month`."""

    def test__str__(self) -> None:
        """Test __str__."""
        self.assertEqual(str(Month.NISAN), 'Nisan')
        self.assertEqual(str(Month.ADAR), 'Adar')
        self.assertEqual(str(Month.ADAR_1), 'Adar 1')
        self.assertEqual(str(Month.ADAR_2), 'Adar 2')

    def test__get(self) -> None:
        """Test get Month."""
        # non-leap
        self.assertEqual(Month.get(1, False), Month.NISAN)
        self.assertEqual(Month.get(12, False), Month.ADAR)

        # leap
        self.assertEqual(Month.get(12, True), Month.ADAR_1)
        self.assertEqual(Month.get(13, True), Month.ADAR_2)
