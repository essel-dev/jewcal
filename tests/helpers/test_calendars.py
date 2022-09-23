"""Unittests for jewcal.helpers.dates."""

from unittest import TestCase

from src.jewcal.helpers.calendars import (CalendarGenerator, CalendarsCache,
                                          Event)
from src.jewcal.models.enums import Chag, Fast, Month, YomTov

# pylint: disable=pointless-statement
# self.assertRaises without context (`with`)


class EventCase(TestCase):
    """Unittests for `Event`."""

    def test__str__(self) -> None:
        """Test __str__."""
        event = Event(YomTov.PESACH, erev=True)
        self.assertEqual(str(event), 'Erev Pesach')

        event = Event(YomTov.PESACH)
        self.assertEqual(str(event), 'Pesach')

        event = Event(Chag.PESACH_CHOL_HAMOED, day=1)
        self.assertEqual(str(event), 'Pesach Chol HaMoed 1')

        event = Event(Chag.HOSHANA_RABA, erev=True)
        self.assertEqual(str(event), 'Hoshana Raba')

        event = Event(
            Chag.ROSH_CHODESH, description=f'{Chag.ROSH_CHODESH} {Month.ADAR}'
        )
        self.assertEqual(str(event), 'Rosh Chodesh Adar')


class CalendarsCacheCase(TestCase):
    """Unittests for `CalendarsCache`."""

    def test_singleton(self) -> None:
        """Test the singleton."""
        logger = 'src.jewcal.helpers.calendars'

        with self.assertLogs(logger, level='INFO') as context_m:
            CalendarsCache.clear()

            CalendarGenerator(True, 5783)
            CalendarGenerator(True, 5783)
            CalendarGenerator(True, 5785)
            CalendarGenerator(True, 5783)

            self.assertEqual(
                context_m.output,
                [
                    f'INFO:{logger}:Singleton instance reset',

                    f'INFO:{logger}:Returning new Singleton instance',
                    f"INFO:{logger}:Calendar for (5783, 'DIASPORA') requested"
                    ' from Singleton',
                    f"INFO:{logger}:Calendar for (5783, 'DIASPORA') added to"
                    ' Singleton',

                    f'INFO:{logger}:Returning existing Singleton instance',
                    f"INFO:{logger}:Calendar for (5783, 'DIASPORA') requested"
                    ' from Singleton',

                    f'INFO:{logger}:Returning existing Singleton instance',
                    f"INFO:{logger}:Calendar for (5785, 'DIASPORA') requested"
                    ' from Singleton',
                    f"INFO:{logger}:Calendar for (5785, 'DIASPORA') added to"
                    ' Singleton',

                    f'INFO:{logger}:Returning existing Singleton instance',
                    f"INFO:{logger}:Calendar for (5783, 'DIASPORA') requested"
                    ' from Singleton',
                ]
            )


class CalendarGeneratorCase(TestCase):
    """Unittests for `CalendarGenerator`."""

    def test__init__fail(self) -> None:
        """Test __init__ should fail."""
        with self.assertRaises(TypeError) as context_manager:
            CalendarGenerator(0, 5782)  # type: ignore[arg-type, arg-type]
        self.assertEqual(
            'unsupported type int',
            str(context_manager.exception)
        )

        with self.assertRaises(TypeError) as context_manager:
            CalendarGenerator(True, '5782')  # type: ignore[arg-type]
        self.assertEqual(
            'unsupported type str',
            str(context_manager.exception)
        )

    def test_israel_diaspora_and_leap(self) -> None:
        """Test Israel and Diaspora and the number of month for (non-)leap."""
        # Israel and leap
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.NISAN][16],
            [Event(Chag.PESACH_CHOL_HAMOED, day=1)]
        )
        self.assertEqual(len(generator.calendar), 13)

        # Diaspora and non-leap
        generator = CalendarGenerator(True, 5783)

        self.assertEqual(
            generator.calendar[Month.NISAN][16], [Event(YomTov.PESACH, day=2)]
        )
        self.assertEqual(len(generator.calendar), 12)

    def test_pesach_israel(self) -> None:
        """Test Pesach Israel."""
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.NISAN][14],
            [Event(YomTov.PESACH, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][15], [Event(YomTov.PESACH)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][16],
            [Event(Chag.PESACH_CHOL_HAMOED, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][20],
            [Event(Chag.PESACH_CHOL_HAMOED, erev=True, day=5)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][21], [Event(YomTov.PESACH, day=7)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][22], [Event(Chag.ISRU_CHAG)]
        )

    def test_pesach_diaspora(self) -> None:
        """Test Pesach Diaspora."""
        generator = CalendarGenerator(True, 5782)

        self.assertEqual(
            generator.calendar[Month.NISAN][14],
            [Event(YomTov.PESACH, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][15], [Event(YomTov.PESACH, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][16], [Event(YomTov.PESACH, day=2)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][17],
            [Event(Chag.PESACH_CHOL_HAMOED, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][20],
            [Event(Chag.PESACH_CHOL_HAMOED, erev=True, day=4)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][21], [Event(YomTov.PESACH, day=7)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][22], [Event(YomTov.PESACH, day=8)]
        )

        self.assertEqual(
            generator.calendar[Month.NISAN][23], [Event(Chag.ISRU_CHAG)]
        )

    def test_lag_baomer(self) -> None:
        """Test Lag BaOmer."""
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.IYAR][18], [Event(Chag.LAG_BAOMER)]
        )

    def test_shavuot_israel(self) -> None:
        """Test Shavuot Israel."""
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.SIVAN][5],
            [Event(YomTov.SHAVUOT, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.SIVAN][6], [Event(YomTov.SHAVUOT)]
        )

        self.assertEqual(
            generator.calendar[Month.SIVAN][7], [Event(Chag.ISRU_CHAG)]
        )

    def test_shavuot_diaspora(self) -> None:
        """Test Shavuot Diaspora."""
        generator = CalendarGenerator(True, 5782)

        self.assertEqual(
            generator.calendar[Month.SIVAN][5],
            [Event(YomTov.SHAVUOT, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.SIVAN][6], [Event(YomTov.SHAVUOT, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.SIVAN][7], [Event(YomTov.SHAVUOT, day=2)]
        )

        self.assertEqual(
            generator.calendar[Month.SIVAN][8], [Event(Chag.ISRU_CHAG)]
        )

    def test_rosh_hashana_yom_kippur(self) -> None:
        """Test Rosh Hashana and Yom Kippur."""
        generator = CalendarGenerator(False, 5783)

        self.assertEqual(
            generator.calendar[Month.ELUL][29],
            [Event(YomTov.ROSH_HASHANA, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][1],
            [Event(YomTov.ROSH_HASHANA, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][2],
            [Event(YomTov.ROSH_HASHANA, day=2)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][9],
            [Event(YomTov.YOM_KIPPUR, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][10],
            [Event(YomTov.YOM_KIPPUR), Event(Fast.YOM_KIPPUR)]
        )

    def test_sukkot_israel(self) -> None:
        """Test Sukkot Israel."""
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.TISHREI][14],
            [Event(YomTov.SUKKOT, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][15], [Event(YomTov.SUKKOT)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][16],
            [Event(Chag.SUKKOT_CHOL_HAMOED, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][20],
            [Event(Chag.SUKKOT_CHOL_HAMOED, day=5)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][21],
            [Event(Chag.HOSHANA_RABA, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][22],
            [Event(YomTov.SHMINI_ATZERET), Event(YomTov.SIMCHAT_TORA)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][23], [Event(Chag.ISRU_CHAG)]
        )

    def test_sukkot_diaspora(self) -> None:
        """Test Sukkot Diaspora."""
        generator = CalendarGenerator(True, 5782)

        self.assertEqual(
            generator.calendar[Month.TISHREI][14],
            [Event(YomTov.SUKKOT, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][15],
            [Event(YomTov.SUKKOT, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][16],
            [Event(YomTov.SUKKOT, day=2)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][17],
            [Event(Chag.SUKKOT_CHOL_HAMOED, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][20],
            [Event(Chag.SUKKOT_CHOL_HAMOED, day=4)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][21],
            [Event(Chag.HOSHANA_RABA, erev=True)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][22],
            [Event(YomTov.SHMINI_ATZERET)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][23], [Event(YomTov.SIMCHAT_TORA)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][24], [Event(Chag.ISRU_CHAG)]
        )

    def test_chanuka(self) -> None:
        """Test Chanuka."""
        # long kislev
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.KISLEV][29], [Event(Chag.CHANUKA, day=5)]
        )

        self.assertIn(
            Event(Chag.CHANUKA, day=6), generator.calendar[Month.KISLEV][30]
        )
        self.assertEqual(
            generator.calendar[Month.TEVET][2], [Event(Chag.CHANUKA, day=8)]
        )

        # short kislev
        generator = CalendarGenerator(False, 5784)

        self.assertEqual(
            generator.calendar[Month.TEVET][3], [Event(Chag.CHANUKA, day=8)]
        )

    def test_tu_bishvat(self) -> None:
        """Test Tu BiShvat."""
        generator = CalendarGenerator(True, 5783)

        self.assertEqual(
            generator.calendar[Month.SHEVAT][15], [Event(Chag.TU_BISHVAT)]
        )

    def test_purim_and_shushan(self) -> None:
        """Test Purim and Shushan Purim."""
        # Adar
        generator = CalendarGenerator(False, 5783)

        self.assertEqual(
            generator.calendar[Month.ADAR][14], [Event(Chag.PURIM)]
        )

        self.assertEqual(
            generator.calendar[Month.ADAR][15], [Event(Chag.SHUSHAN_PURIM)]
        )

        # Adar 2
        generator = CalendarGenerator(False, 5782)

        with self.assertRaises(KeyError):
            generator.calendar[Month.ADAR_1][14]
            generator.calendar[Month.ADAR_1][15]

        self.assertEqual(
            generator.calendar[Month.ADAR_2][14], [Event(Chag.PURIM)]
        )

        self.assertEqual(
            generator.calendar[Month.ADAR_2][15], [Event(Chag.SHUSHAN_PURIM)]
        )

    def test_rosh_chodesh_non_leap(self) -> None:
        """Test Rosh Chodesh in a non leap year."""
        generator = CalendarGenerator(False, 5783)

        self.assertEqual(
            generator.calendar[Month.SHEVAT][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ADAR)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.SHEVAT][30]), 1)
        self.assertEqual(
            generator.calendar[Month.ADAR][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ADAR)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.ADAR][1]), 1)

        with self.assertRaises(KeyError):
            generator.calendar[Month.ADAR][30],

        self.assertEqual(
            generator.calendar[Month.NISAN][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.NISAN)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.NISAN][1]), 1)

    def test_rosh_chodesh_leap(self) -> None:
        """Test Rosh Chodesh in leap year."""
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.NISAN][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.NISAN)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.NISAN][1]), 1)

        self.assertEqual(
            generator.calendar[Month.NISAN][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.IYAR)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.NISAN][30]), 1)
        self.assertEqual(
            generator.calendar[Month.IYAR][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.IYAR)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.IYAR][1]), 1)

        with self.assertRaises(KeyError):
            generator.calendar[Month.IYAR][30]
        self.assertEqual(
            generator.calendar[Month.SIVAN][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.SIVAN)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.SIVAN][1]), 1)

        self.assertEqual(
            generator.calendar[Month.SIVAN][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.TAMUZ)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.SIVAN][30]), 1)
        self.assertEqual(
            generator.calendar[Month.TAMUZ][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.TAMUZ)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.TAMUZ][1]), 1)

        with self.assertRaises(KeyError):
            generator.calendar[Month.TAMUZ][30]
        self.assertEqual(
            generator.calendar[Month.AV][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.AV)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.AV][1]), 1)

        self.assertEqual(
            generator.calendar[Month.AV][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ELUL)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.AV][30]), 1)
        self.assertEqual(
            generator.calendar[Month.ELUL][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ELUL)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.ELUL][1]), 1)

        self.assertEqual(len(generator.calendar[Month.ELUL][29]), 1)
        self.assertEqual(
            generator.calendar[Month.ELUL][29],
            [Event(YomTov.ROSH_HASHANA, erev=True)]
        )
        self.assertEqual(len(generator.calendar[Month.TISHREI][1]), 1)
        self.assertEqual(
            generator.calendar[Month.TISHREI][1],
            [Event(YomTov.ROSH_HASHANA, day=1)]
        )

        self.assertEqual(
            generator.calendar[Month.TISHREI][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.CHESHVAN)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.TISHREI][30]), 1)
        self.assertEqual(
            generator.calendar[Month.CHESHVAN][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.CHESHVAN)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.CHESHVAN][1]), 1)

        self.assertEqual(
            generator.calendar[Month.KISLEV][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.KISLEV)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.KISLEV][1]), 1)

        self.assertIn(
            Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.TEVET)}'
            ),
            generator.calendar[Month.KISLEV][30],
        )
        self.assertEqual(len(generator.calendar[Month.KISLEV][30]), 2)
        self.assertIn(
            Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.TEVET)}'
            ),
            generator.calendar[Month.TEVET][1],
        )
        self.assertEqual(len(generator.calendar[Month.TEVET][1]), 2)

        self.assertEqual(
            generator.calendar[Month.SHEVAT][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.SHEVAT)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.SHEVAT][1]), 1)

        self.assertEqual(
            generator.calendar[Month.SHEVAT][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ADAR_1)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.SHEVAT][30]), 1)
        self.assertEqual(
            generator.calendar[Month.ADAR_1][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ADAR_1)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.ADAR_1][1]), 1)

        self.assertEqual(
            generator.calendar[Month.ADAR_1][30],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ADAR_2)}'
            )]
        )

        self.assertEqual(len(generator.calendar[Month.ADAR_1][30]), 1)
        self.assertEqual(
            generator.calendar[Month.ADAR_2][1],
            [Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {str(Month.ADAR_2)}'
            )]
        )
        self.assertEqual(len(generator.calendar[Month.ADAR_2][1]), 1)

    def test_fasts_17_tamuz(self) -> None:
        """Test Shiva Asar BeTamuz."""
        # not on shabbat
        generator = CalendarGenerator(False, 5784)

        self.assertEqual(
            generator.calendar[Month.TAMUZ][17], [Event(Fast.TAMUZ_17)]
        )
        with self.assertRaises(KeyError):
            generator.calendar[Month.TAMUZ][18]

        # postponed
        generator = CalendarGenerator(False, 5782)

        with self.assertRaises(KeyError):
            generator.calendar[Month.TAMUZ][17]
        self.assertEqual(
            generator.calendar[Month.TAMUZ][18], [Event(Fast.TAMUZ_17)]
        )

    def test_fasts_9_av(self) -> None:
        """Test Tisha BeAv."""
        # not on shabbat
        generator = CalendarGenerator(False, 5784)

        self.assertEqual(
            generator.calendar[Month.AV][9], [Event(Fast.AV_9)]
        )
        with self.assertRaises(KeyError):
            generator.calendar[Month.AV][10]

        # postponed
        generator = CalendarGenerator(False, 5782)

        with self.assertRaises(KeyError):
            generator.calendar[Month.AV][9]
        self.assertEqual(
            generator.calendar[Month.AV][10], [Event(Fast.AV_9)]
        )

    def test_fasts_tzom_gedalia(self) -> None:
        """Test Tzom Gedalia."""
        # not on shabbat
        generator = CalendarGenerator(False, 5783)

        self.assertEqual(
            generator.calendar[Month.TISHREI][3], [Event(Fast.TZOM_GEDALIA)]
        )
        with self.assertRaises(KeyError):
            generator.calendar[Month.TISHREI][4]

        # postponed
        generator = CalendarGenerator(False, 5785)  # 2024
        with self.assertRaises(KeyError):
            generator.calendar[Month.TISHREI][3]
        self.assertEqual(
            generator.calendar[Month.TISHREI][4], [Event(Fast.TZOM_GEDALIA)]
        )

    def test_fasts_10_tevet(self) -> None:
        """Test Asara BeTevet."""
        generator = CalendarGenerator(False, 5782)

        self.assertEqual(
            generator.calendar[Month.TEVET][10], [Event(Fast.TEVET_10)]
        )

    def test_fasts_tanit_esther(self) -> None:
        """Test TaAnit Esther."""
        # not on shabbat
        generator = CalendarGenerator(False, 5783)  # 2023 - Adar

        self.assertEqual(
            generator.calendar[Month.ADAR][13], [Event(Fast.TANIT_ESTHER)]
        )
        with self.assertRaises(KeyError):
            generator.calendar[Month.ADAR][11]

        # moved up to thursday before shabbat
        generator = CalendarGenerator(False, 5784)  # 2024 - Adar 2

        with self.assertRaises(KeyError):
            generator.calendar[Month.ADAR_2][13]
        self.assertEqual(
            generator.calendar[Month.ADAR_2][11], [Event(Fast.TANIT_ESTHER)]
        )

        # moved to thursday before shabbat
        generator = CalendarGenerator(False, 5788)  # 2028 - Adar

        with self.assertRaises(KeyError):
            generator.calendar[Month.ADAR][13]
        self.assertEqual(
            generator.calendar[Month.ADAR][11], [Event(Fast.TANIT_ESTHER)]
        )
