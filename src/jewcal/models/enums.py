"""Constants as enums."""

from __future__ import annotations

from enum import Enum, IntEnum, unique


@unique
class Month(IntEnum):
    """The Jewish months."""

    NISAN = 1
    IYAR = 2
    SIVAN = 3
    TAMUZ = 4
    AV = 5
    ELUL = 6
    TISHREI = 7
    CHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR = 12
    ADAR_1 = 14
    ADAR_2 = 13

    def __str__(self) -> str:
        """Get the month as a readable string.

        Returns:
            The month.
        """
        return self.name.capitalize().replace('_', ' ')

    @classmethod
    def get(cls, number: int, leap: bool) -> Month:
        """Get the enum member.

        Regarding the months Adar, Adar 1 and 2:
        - If the Jewish year is non-leap, it returns Adar.
        - If the Jewish year is leap, it returns Adar 1 or Adar 2.

        Args:
            number: The month number.
            leap: Is the Jewish year a leap year.

        Returns:
            The enum member.
        """
        match number:
            case 12:
                return Month.ADAR_1 if leap else Month.ADAR
            case _:
                return Month(number)


@unique
class CalendarType(Enum):
    """The calendar types."""

    DIASPORA = 'Diaspora'
    ISRAEL = 'Israel'


@unique
class Shabbat(Enum):
    """Constants for Shabbat."""

    EREV = 'Erev Shabbat'
    SHABBAT = 'Shabbat'

    def __str__(self) -> str:
        """Get Shabbat as a readable string.

        Returns:
            The Shabbat.
        """
        return self.value


@unique
class YomTov(Enum):
    """Constants for the Yamim Tovim."""

    PESACH = 'Pesach'
    ROSH_HASHANA = 'Rosh Hashana'
    SHAVUOT = 'Shavuot'
    SHMINI_ATZERET = 'Shmini Atzeret'
    SIMCHAT_TORA = 'Simchat Tora'
    SUKKOT = 'Sukkot'
    YOM_KIPPUR = 'Yom Kippur'

    def __str__(self) -> str:
        """Get the Yom Tov as a readable string.

        Returns:
            The Yom Tov.
        """
        return self.value


@unique
class Chag(Enum):
    """Constants for the Chagim."""

    PESACH_CHOL_HAMOED = 'Pesach Chol HaMoed'
    SUKKOT_CHOL_HAMOED = 'Sukkot Chol HaMoed'
    CHANUKA = 'Chanuka'
    HOSHANA_RABA = 'Hoshana Raba'
    ISRU_CHAG = 'Isru Chag'
    LAG_BAOMER = 'Lag BaOmer'
    PURIM = 'Purim'
    ROSH_CHODESH = 'Rosh Chodesh'
    SHUSHAN_PURIM = 'Shushan Purim'
    TU_BISHVAT = 'Tu BiShvat'

    def __str__(self) -> str:
        """Get the Chag as a readable string.

        Returns:
            The Chag.
        """
        return self.value


@unique
class Fast(Enum):
    """Constants for the fasts."""

    AV_9 = 'Tisha BeAv'
    TAMUZ_17 = 'Shiva Asar BeTamuz'
    TANIT_ESTHER = 'TaAnit Esther'
    TEVET_10 = 'Asara BeTevet'
    TZOM_GEDALIA = 'Tzom Gedalia'
    YOM_KIPPUR = 'Yom Kippur'

    def __str__(self) -> str:
        """Get the fast as a readable string.

        Returns:
            The fast.
        """
        return self.value
