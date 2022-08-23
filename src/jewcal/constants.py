"""Constants."""

from enum import Enum, IntEnum, unique
from typing import NamedTuple


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
    category: Category


# YOMTOV[jewish_month][day]
YOMTOV: dict[int, dict[int, Event]] = {
    6: {
        29: Event('Erev Rosh Hashana', Category.CANDLES),
    },
    7: {
        1: Event('Rosh Hashana 1', Category.CANDLES),
        2: Event('Rosh Hashana 2', Category.HAVDALAH),
        9: Event('Erev Yom Kippur', Category.CANDLES),
        10: Event('Yom Kippur', Category.HAVDALAH),
        14: Event('Erev Sukkos', Category.CANDLES),
        15: Event('Sukkos 1', Category.CANDLES),
        16: Event('Sukkos 2', Category.HAVDALAH),
        21: Event('Hoshana Rabba', Category.CANDLES),
        22: Event('Shmini Atzeres', Category.CANDLES),
        23: Event('Simchas Tora', Category.HAVDALAH),
    },
    1: {
        14: Event('Erev Pesach', Category.CANDLES),
        15: Event('Pesach 1', Category.CANDLES),
        16: Event('Pesach 2', Category.HAVDALAH),
        20: Event('Chol HaMoed Pesach 6', Category.CANDLES),
        21: Event('Pesach 7', Category.CANDLES),
        22: Event('Pesach 8', Category.HAVDALAH),
    },
    3: {
        5: Event('Erev Shavuos', Category.CANDLES),
        6: Event('Shavuos 1', Category.CANDLES),
        7: Event('Shavuos 2', Category.HAVDALAH),
    },
}

# SHABBOS[weekday]
SHABBOS: dict[int, Event] = {
    5: Event('Erev Shabbos', Category.CANDLES),
    6: Event('Shabbos', Category.HAVDALAH),
}
