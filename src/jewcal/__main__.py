"""JewCal quickstart.

This script can be invoked from the command line:
    `jewcal`
"""

from pprint import pprint

from jewcal import JewCal
from jewcal.models.zmanim import Location


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
    print(f'{today.is_issur_melacha()=}')
    print(f'\n{today!r}')

    print('\n\nZmanim for Jerushalayim:')
    location = Location(
        latitude=31.76904,
        longitude=35.21633,
        use_tzeis_hakochavim=True,
        hadlokas_haneiros_minutes=40,
        tzeis_minutes=72,
    )

    jewcal = JewCal(diaspora=False, location=location)
    if jewcal.zmanim:
        pprint(jewcal.zmanim.to_dict())

    print(f'\n{location}')


if __name__ == '__main__':  # pragma: no cover
    main()
