"""Constants."""

from enum import Enum, IntEnum, unique
from typing import NamedTuple, Optional


@unique
class Category(Enum):
    """Does the shabbos or yom tov start (candles) or end (havdalah)."""

    CANDLES = 'Candles'
    HAVDALAH = 'Havdalah'


@unique
class Months(IntEnum):
    """The Jewish months."""

    TISHREI = 7
    CHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR = 12
    ADAR_2 = 13
    NISAN = 1
    IYAR = 2
    SIVAN = 3
    TAMUZ = 4
    AV = 5
    ELUL = 6


class Event(NamedTuple):
    """Named tuple for shabbos and yom tov."""

    title: str
    category: Optional[str]


# YOMTOV[jewish_month][day]
YOMTOV: dict[int, dict[int, Event]] = {
    6: {
        29: Event('Erev Rosh Hashana', Category.CANDLES.value),
    },
    7: {
        1: Event('Rosh Hashana 1', Category.CANDLES.value),
        2: Event('Rosh Hashana 2', Category.HAVDALAH.value),

        9: Event('Erev Yom Kippur', Category.CANDLES.value),
        10: Event('Yom Kippur', Category.HAVDALAH.value),

        14: Event('Erev Sukkos', Category.CANDLES.value),
        15: Event('Sukkos 1', Category.CANDLES.value),
        16: Event('Sukkos 2', Category.HAVDALAH.value),
        17: Event('Chol HaMoed 1 (Sukkos 3)', None),
        18: Event('Chol HaMoed 2 (Sukkos 4)', None),
        19: Event('Chol HaMoed 3 (Sukkos 5)', None),
        20: Event('Chol HaMoed 4 (Sukkos 6)', None),
        21: Event('Hoshana Rabba (Sukkos 7)', Category.CANDLES.value),
        22: Event('Shmini Atzeres (Sukkos 8)', Category.CANDLES.value),
        23: Event('Simchas Tora', Category.HAVDALAH.value),
    },
    1: {
        14: Event('Erev Pesach', Category.CANDLES.value),
        15: Event('Pesach 1', Category.CANDLES.value),
        16: Event('Pesach 2', Category.HAVDALAH.value),
        17: Event('Chol HaMoed 1 (Pesach 3)', None),
        18: Event('Chol HaMoed 2 (Pesach 4)', None),
        19: Event('Chol HaMoed 3 (Pesach 5)', None),
        20: Event('Chol HaMoed 4 (Pesach 6)', Category.CANDLES.value),
        21: Event('Pesach 7', Category.CANDLES.value),
        22: Event('Pesach 8', Category.HAVDALAH.value),
    },
    3: {
        5: Event('Erev Shavuos', Category.CANDLES.value),
        6: Event('Shavuos 1', Category.CANDLES.value),
        7: Event('Shavuos 2', Category.HAVDALAH.value),
    },
}

# SHABBOS[weekday]
SHABBOS: dict[int, Event] = {
    5: Event('Erev Shabbos', Category.CANDLES.value),
    6: Event('Shabbos', Category.HAVDALAH.value),
}
