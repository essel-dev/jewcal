"""Unittests for jewcal.helpers.dates."""

from datetime import date
from unittest import TestCase

from src.jewcal.helpers.dates import DateConverter


class DateConverterTestCase(TestCase):
    """Unittests for `DateConverter`."""

    def test__init__(self) -> None:
        """Test __init__."""
        gregorian = date(2022, 8, 21)
        converter = DateConverter(gregorian)

        self.assertEqual(converter.gregorian, gregorian)
        self.assertEqual(converter.jewish_date, (5782, 5, 24))
        self.assertEqual(converter.jewish_weekday, 0)

        gregorian = date(2022, 9, 2)
        converter = DateConverter(gregorian)

        self.assertEqual(converter.gregorian, gregorian)
        self.assertEqual(converter.jewish_date, (5782, 6, 6))
        self.assertEqual(converter.jewish_weekday, 5)

    def test__init__fail(self) -> None:
        """Test __init__ should fail."""
        with self.assertRaises(TypeError) as context_manager:
            DateConverter(0)  # type: ignore[arg-type]
        self.assertEqual(
            'unsupported type int',
            str(context_manager.exception)
        )

        with self.assertRaises(TypeError) as context_manager:
            DateConverter('invalid')  # type: ignore[arg-type]
        self.assertEqual(
            'unsupported type str',
            str(context_manager.exception)
        )
