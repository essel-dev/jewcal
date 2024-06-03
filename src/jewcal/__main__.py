"""JewCal quickstart.

This script can be invoked from the command line:
    `jewcal`
"""

from datetime import date

from jewcal import JewCal


def main() -> None:
    """Run a simple example."""
    jewcal = JewCal(date.today())

    print(f'Today is {jewcal}', end='\n\n')

    print(repr(jewcal))


if __name__ == '__main__':  # pragma: no cover
    main()
