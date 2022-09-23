"""Simple JewCal example.

This script can be invoked from the command line:
    `jewcal`
"""

from . import JewCal


def main() -> None:
    """Run a simple example."""
    jewcal = JewCal()

    print(f'Today is {jewcal.day}')
    print(f'Is Erev Shabbat: {jewcal.day.is_erev_shabbat()}')
    print(f'Is Shabbat: {jewcal.day.is_shabbat()}')
    print(f'Is Erev Yom Tov: {jewcal.day.is_erev_yomtov()}')
    print(f'Is Yom Tov: {jewcal.day.is_yomtov()}')
    print(f'Is Issur Melacha: {jewcal.day.is_issur_melacha()}')


if __name__ == '__main__':
    main()
