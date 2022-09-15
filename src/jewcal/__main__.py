"""Simple JewCal example.

This script can be invoked from the command line:
    `python -m jewcal`
"""

from .core import JewCal


def main() -> None:
    """Run a simple example."""
    jewcal = JewCal()

    print(f'Today is {jewcal.day}\n')

    print(repr(jewcal.day))


if __name__ == '__main__':
    main()
