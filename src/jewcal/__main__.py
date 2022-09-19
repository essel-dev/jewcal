"""Simple JewCal example.

This script can be invoked from the command line:
    `jewcal`
"""

from . import JewCal


def main() -> None:
    """Run a simple example."""
    jewcal = JewCal()

    print(f'Today is {jewcal.day}')

    print(f'It is Erev Shabbat: {jewcal.day.is_erev_shabbat()}')
    print(f'It is Erev Yom Tov: {jewcal.day.is_erev_yom_tov()}')
    print(f'It is Shabbat: {jewcal.day.is_shabbat()}')
    print(f'It is Yom Tov: {jewcal.day.is_yom_tov()}')
    print(f'It is Issur Melacha: {jewcal.day.is_issur_melacha()}')

    print(f'\nYesterday was {jewcal.days(-1)[0]}')
    print(f'Tomorrow is {jewcal.days(1)[0]}')

    print('\nPast week:')
    for day in jewcal.weeks(-1):
        print(day)

    print('\nCurrent week:')
    for day in jewcal.current_week():
        print(day)

    print('\nNext 2 weeks:')
    for day in jewcal.weeks(2):
        print(day)


if __name__ == '__main__':
    main()
