"""JewCal quickstart.

This script can be invoked from the command line:
    `jewcal`
"""

from jewcal import JewCal


def main() -> None:
    """Run a simple example."""
    today = JewCal()

    print(f'Today is {today.jewish_date!s}', end='\n\n')

    print(f'{today.has_events()=}')
    print(f'{today.is_erev()=}')
    print(f'{today.is_erev_shabbos()=}')
    print(f'{today.is_shabbos()=}')
    print(f'{today.is_erev_yomtov()=}')
    print(f'{today.is_yomtov()=}')
    print(f'{today.is_issur_melacha()=}', end='\n\n')

    print(repr(today))


if __name__ == '__main__':  # pragma: no cover
    main()
