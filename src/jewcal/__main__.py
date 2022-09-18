"""Simple JewCal example.

This script can be invoked from the command line:
    `jewcal`
"""

from . import JewCal


def main() -> None:
    """Run a simple example."""
    jewcal = JewCal()

    print(f'Today is {jewcal.day}.')

    print(f'It is Erev Shabbat: {jewcal.day.is_erev_shabbat()}')
    print(f'It is Erev Yom Tov: {jewcal.day.is_erev_yom_tov()}')

    print(f'It is Shabbat: {jewcal.day.is_shabbat()}')
    print(f'It is Yom Tov: {jewcal.day.is_yom_tov()}')

    print(f'It is Issur Melacha: {jewcal.day.is_issur_melacha()}')


if __name__ == '__main__':
    main()
