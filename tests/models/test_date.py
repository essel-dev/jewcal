"""Unittests for jewcal.models.date."""

from datetime import date
from unittest import TestCase

from src.jewcal.models.date import Date


class DateTestCase(TestCase):
    """Unittests for `Date`."""

    def test__slots__fail(self) -> None:
        """Test __slots__ should fail."""
        jewish_date = Date(date(2022, 9, 1))

        with self.assertRaises(AttributeError):
            # pylint: disable-next=protected-access, unused-private-member
            jewish_date.__day = 'x'  # type: ignore[assignment]

        with self.assertRaises(AttributeError):
            # pylint: disable-next=assigning-non-slot
            jewish_date.x = 'x'  # type: ignore[attr-defined]

    def test__init__(self) -> None:
        """Test __init__."""
        gregorian = date(2022, 9, 2)
        jewish_date = Date(gregorian)

        self.assertEqual(jewish_date.gregorian, gregorian)
        self.assertEqual(jewish_date.year, 5782)
        self.assertEqual(jewish_date.month, 6)
        self.assertEqual(jewish_date.day, 6)
        self.assertEqual(jewish_date.weekday, 5)

    def test__init__fail(self) -> None:
        """Test __init__ should fail."""
        with self.assertRaises(TypeError):
            Date('date(2022, 9, 5)')  # type: ignore[arg-type]

    def test__str__(self) -> None:
        """Test __str__."""
        gregorian = date(2022, 4, 16)
        jewish_date = Date(gregorian)

        self.assertEqual(str(jewish_date), '15 Nisan 5782 (2022-04-16)')

        # non-leap
        gregorian = date(2023, 3, 15)
        jewish_date = Date(gregorian)

        self.assertEqual(str(jewish_date), '22 Adar 5783 (2023-03-15)')

        # leap
        jewish_date = Date(date(2022, 2, 27))
        self.assertEqual(str(jewish_date), '26 Adar 1 5782 (2022-02-27)')

        jewish_date = Date(date(2022, 3, 16))
        self.assertEqual(str(jewish_date), '13 Adar 2 5782 (2022-03-16)')
