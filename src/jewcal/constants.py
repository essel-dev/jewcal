"""Constants."""

from enum import Enum, IntEnum, unique
from typing import List, Union


@unique
class Category(Enum):
    """Does the shabbos or yomtov start (candles) or end (havdalah)."""

    CANDLES = 'Candles'
    HAVDALAH = 'Havdalah'


@unique
class Months(IntEnum):
    """The jewish months."""

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


YOMTOV: dict[int, dict[int, List[Union[str, Category]]]] = {
    6: {
        29: ['Erev Rosh Hashana', Category.CANDLES],
    },
    7: {
        1: ['Rosh Hashana 1', Category.CANDLES],
        2: ['Rosh Hashana 2', Category.HAVDALAH],
        14: ['Erev Sukkos', Category.CANDLES],
        15: ['Sukkos 1', Category.CANDLES],
        16: ['Sukkos 2', Category.HAVDALAH],
        21: ['Hoshana Rabba', Category.CANDLES],
        22: ['Shmini Atzeres', Category.CANDLES],
        23: ['Simchas Tora', Category.HAVDALAH],
    },
    1: {
        14: ['Erev Pesach', Category.CANDLES],
        15: ['Pesach 1', Category.CANDLES],
        16: ['Pesach 2', Category.HAVDALAH],
        20: ['Chol HaMoed Pesach 6', Category.CANDLES],
        21: ['Pesach 7', Category.CANDLES],
        22: ['Pesach 8', Category.HAVDALAH],
    },
    3: {
        5: ['Erev Shavuos', Category.CANDLES],
        6: ['Shavuos 1', Category.CANDLES],
        7: ['Shavuos 2', Category.HAVDALAH],
    },
}

SHABBOS: dict[int, List[Union[str, Category]]] = {
    5: ['Erev Shabbos', Category.CANDLES],
    6: ['Shabbos', Category.HAVDALAH],
}
