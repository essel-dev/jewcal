"""Simple JewCal example.

This script can be invoked from the command line:
    `jewcal`
"""

from datetime import date

from . import JewCal


def main() -> None:
    """Run a simple example."""
    jewcal = JewCal()
    print(f'Today is {jewcal.day}.\n')

    jewcal = JewCal(date(2022, 4, 16))
    print(jewcal.day, '\n')
    print(repr(jewcal.day))


if __name__ == '__main__':
    main()
