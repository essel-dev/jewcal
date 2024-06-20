"""Unittests for jewcal.utils.datetime."""

from datetime import datetime, timezone
from unittest import TestCase

from src.jewcal.utils.datetime import date_today, datetime_now

SECONDS = 3


class DatetimeTestCase(TestCase):
    """Unittests for datetime."""

    def test_datetime_now(self) -> None:
        """Test current date and time."""
        self.assertTrue(
            (datetime_now() - datetime.now(tz=timezone.utc)).total_seconds() < SECONDS,
        )

    def test_date_today(self) -> None:
        """Test current date."""
        self.assertEqual(date_today(), datetime.now(tz=timezone.utc).date())
