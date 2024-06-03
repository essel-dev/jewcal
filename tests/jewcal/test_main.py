"""Unittests for jewcal.__main__."""

import sys
from io import StringIO
from unittest import TestCase

from src.jewcal.__main__ import main


class MainTestCase(TestCase):
    """Unittests for __main__."""

    def test_main(self) -> None:
        """Test main()."""
        # capture standard output by temporarily redirecting sys.stdout to a StringIO
        # https://stackoverflow.com/a/34738440
        capturedOutput = StringIO()  # Create StringIO.
        sys.stdout = capturedOutput  # Redirect stdout.
        main()  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertIn('Today is', capturedOutput.getvalue())
        self.assertIn('JewCal(year=', capturedOutput.getvalue())
