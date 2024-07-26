"""Unittests for jewcal.__main__."""

import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from src.jewcal.__main__ import main


class MainTestCase(TestCase):
    """Unittests for __main__."""

    def test_main(self) -> None:
        """Test main()."""
        with patch.object(sys, 'stdout', StringIO()) as output:
            main()  # Call function.

        self.assertIn('Today is', output.getvalue())
        self.assertIn('JewCal(jewish_date=JewishDate(year=', output.getvalue())

        self.assertIn('Zmanim for Jerushalayim:', output.getvalue())
        self.assertIn('sunrise', output.getvalue())
        self.assertIn('Location(latitude=31.76904', output.getvalue())
