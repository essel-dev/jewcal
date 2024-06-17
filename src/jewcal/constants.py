"""Constants."""

from __future__ import annotations

from enum import Enum, unique
from typing import Final, NamedTuple


@unique
class Action(Enum):
    """Does the shabbos or yom tov start (candles) or end (havdalah)."""

    CANDLES = 'Candles'
    HAVDALAH = 'Havdalah'


class Event(NamedTuple):
    """Named tuple for shabbos and yom tov."""

    title: str
    action: str | None


YOMTOV: Final[dict[int, dict[int, Event]]] = {
    6: {
        29: Event('Erev Rosh Hashana', Action.CANDLES.value),
    },
    7: {
        1: Event('Rosh Hashana 1', Action.CANDLES.value),
        2: Event('Rosh Hashana 2', Action.HAVDALAH.value),
        9: Event('Erev Yom Kippur', Action.CANDLES.value),
        10: Event('Yom Kippur', Action.HAVDALAH.value),
        14: Event('Erev Sukkos', Action.CANDLES.value),
        15: Event('Sukkos 1', Action.CANDLES.value),
        16: Event('Sukkos 2', Action.HAVDALAH.value),
        17: Event('Chol HaMoed 1 (Sukkos 3)', None),
        18: Event('Chol HaMoed 2 (Sukkos 4)', None),
        19: Event('Chol HaMoed 3 (Sukkos 5)', None),
        20: Event('Chol HaMoed 4 (Sukkos 6)', None),
        21: Event('Hoshana Rabba (Sukkos 7)', Action.CANDLES.value),
        22: Event('Shmini Atzeres (Sukkos 8)', Action.CANDLES.value),
        23: Event('Simchas Tora', Action.HAVDALAH.value),
    },
    1: {
        14: Event('Erev Pesach', Action.CANDLES.value),
        15: Event('Pesach 1', Action.CANDLES.value),
        16: Event('Pesach 2', Action.HAVDALAH.value),
        17: Event('Chol HaMoed 1 (Pesach 3)', None),
        18: Event('Chol HaMoed 2 (Pesach 4)', None),
        19: Event('Chol HaMoed 3 (Pesach 5)', None),
        20: Event('Chol HaMoed 4 (Pesach 6)', Action.CANDLES.value),
        21: Event('Pesach 7', Action.CANDLES.value),
        22: Event('Pesach 8', Action.HAVDALAH.value),
    },
    3: {
        5: Event('Erev Shavuos', Action.CANDLES.value),
        6: Event('Shavuos 1', Action.CANDLES.value),
        7: Event('Shavuos 2', Action.HAVDALAH.value),
    },
}

YOMTOV_ISRAEL: Final[dict[int, dict[int, Event]]] = {
    6: {
        29: Event('Erev Rosh Hashana', Action.CANDLES.value),
    },
    7: {
        1: Event('Rosh Hashana 1', Action.CANDLES.value),
        2: Event('Rosh Hashana 2', Action.HAVDALAH.value),
        9: Event('Erev Yom Kippur', Action.CANDLES.value),
        10: Event('Yom Kippur', Action.HAVDALAH.value),
        14: Event('Erev Sukkot', Action.CANDLES.value),
        15: Event('Sukkot 1', Action.HAVDALAH.value),
        16: Event('Chol HaMoed 1 (Sukkot 2)', None),
        17: Event('Chol HaMoed 2 (Sukkot 3)', None),
        18: Event('Chol HaMoed 3 (Sukkot 4)', None),
        19: Event('Chol HaMoed 4 (Sukkot 5)', None),
        20: Event('Chol HaMoed 5 (Sukkot 6)', None),
        21: Event('Hoshana Rabba (Sukkot 7)', Action.CANDLES.value),
        22: Event('Shmini Atzeret / Simchat Tora', Action.HAVDALAH.value),
    },
    1: {
        14: Event('Erev Pesach', Action.CANDLES.value),
        15: Event('Pesach 1', Action.HAVDALAH.value),
        16: Event('Chol HaMoed 1 (Pesach 2)', None),
        17: Event('Chol HaMoed 2 (Pesach 3)', None),
        18: Event('Chol HaMoed 3 (Pesach 4)', None),
        19: Event('Chol HaMoed 4 (Pesach 5)', None),
        20: Event('Chol HaMoed 5 (Pesach 6)', Action.CANDLES.value),
        21: Event('Pesach 7', Action.HAVDALAH.value),
    },
    3: {
        5: Event('Erev Shavuot', Action.CANDLES.value),
        6: Event('Shavuot', Action.HAVDALAH.value),
    },
}

SHABBOS: Final[dict[int, Event]] = {
    5: Event('Erev Shabbos', Action.CANDLES.value),
    6: Event('Shabbos', Action.HAVDALAH.value),
}
