"""Unittests for jewcal.helpers.dates."""

from unittest import TestCase

from src.jewcal.helpers.calendars import CalendarGenerator, CalendarsCache
from src.jewcal.models.date import Months

# pylint: disable=pointless-statement
# self.assertRaises without context (`with`)


class CalendarGeneratorCase(TestCase):
    """Unittests for `Calendargenerator`."""

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

    def test_diaspora(self) -> None:
        """Test diaspora."""
        generator = CalendarGenerator(True, 5782)  # 2022

        self.assertEqual(
            generator.calendar[Months.NISAN][16][0].name,
            'Pesach 2'
        )

    def test_israel(self) -> None:
        """Test Israel."""
        generator = CalendarGenerator(False, 5782)  # 2022

        self.assertEqual(
            generator.calendar[Months.NISAN][16][0].name,
            'Chol HaMoed 1 (Pesach 2)'
        )

    def test_chanuka(self) -> None:
        """Test Chanuka."""
        # long kislev
        generator = CalendarGenerator(False, 5782)  # 2022

        self.assertEqual(
            generator.calendar[Months.KISLEV][29][0].name,
            'Chanuka 5'
        )
        self.assertEqual(
            generator.calendar[Months.KISLEV][30][0].name,
            'Chanuka 6'
        )
        self.assertEqual(
            generator.calendar[Months.TEVET][2][0].name,
            'Chanuka 8'
        )
        self.assertEqual(
            generator.calendar[Months.TEVET][10][0].name,
            'Asara BeTevet'
        )

        # short kislev
        generator = CalendarGenerator(False, 5784)  # 2023
        self.assertEqual(
            generator.calendar[Months.TEVET][3][0].name,
            'Chanuka 8'
        )
        self.assertEqual(
            generator.calendar[Months.TEVET][10][0].name,
            'Asara BeTevet'
        )

    def test_purim(self) -> None:
        """Test Purim."""
        # Adar
        generator = CalendarGenerator(False, 5783)  # 2023
        self.assertEqual(
            generator.calendar[Months.ADAR][14][0].name,
            'Purim'
        )

        # Adar 2
        generator = CalendarGenerator(False, 5782)  # 2022
        with self.assertRaises(KeyError):
            generator.calendar[Months.ADAR][14]
        self.assertEqual(
            generator.calendar[Months.ADAR_2][14][0].name,
            'Purim'
        )

    def test_fasts_tamuz(self) -> None:
        """Test Shiva Asar BeTamuz."""
        # not on shabbat
        generator = CalendarGenerator(False, 5784)  # 2023
        self.assertEqual(
            generator.calendar[Months.TAMUZ][17][0].name,
            'Shiva Asar BeTamuz'
        )
        with self.assertRaises(KeyError):
            generator.calendar[Months.TAMUZ][18]

        # postponed
        generator = CalendarGenerator(False, 5782)  # 2022
        with self.assertRaises(KeyError):
            generator.calendar[Months.TAMUZ][17]
        self.assertEqual(
            generator.calendar[Months.TAMUZ][18][0].name,
            'Shiva Asar BeTamuz'
        )

    def test_fasts_av(self) -> None:
        """Test Tisha BeAv."""
        # not on shabbat
        generator = CalendarGenerator(False, 5784)  # 2023
        self.assertEqual(
            generator.calendar[Months.AV][9][0].name,
            'Tisha BeAv'
        )
        with self.assertRaises(KeyError):
            generator.calendar[Months.AV][10]

        # postponed
        generator = CalendarGenerator(False, 5782)  # 2022
        with self.assertRaises(KeyError):
            generator.calendar[Months.AV][9]
        self.assertEqual(
            generator.calendar[Months.AV][10][0].name,
            'Tisha BeAv'
        )

    def test_fasts_tishrei(self) -> None:
        """Test Tzom Gedalia."""
        # not on shabbat
        generator = CalendarGenerator(False, 5783)  # 2022
        self.assertEqual(
            generator.calendar[Months.TISHREI][3][0].name,
            'Tzom Gedalia'
        )
        with self.assertRaises(KeyError):
            generator.calendar[Months.TISHREI][4]

        # postponed
        generator = CalendarGenerator(False, 5785)  # 2024
        with self.assertRaises(KeyError):
            generator.calendar[Months.TISHREI][3]
        self.assertEqual(
            generator.calendar[Months.TISHREI][4][0].name,
            'Tzom Gedalia'
        )

    def test_fasts_adar(self) -> None:
        """Test TaAnit Esther."""
        # not on shabbat
        generator = CalendarGenerator(False, 5783)  # 2023
        self.assertEqual(
            generator.calendar[Months.ADAR][13][0].name,
            'TaAnit Esther'
        )
        with self.assertRaises(KeyError):
            generator.calendar[Months.ADAR][11]

        # moved to thursday before shabbat
        generator = CalendarGenerator(False, 5784)  # 2024 - adar 2
        with self.assertRaises(KeyError):
            generator.calendar[Months.ADAR_2][13]
        self.assertEqual(
            generator.calendar[Months.ADAR_2][11][0].name,
            'TaAnit Esther'
        )

        # moved to thursday before shabbat
        generator = CalendarGenerator(False, 5788)  # 2028
        with self.assertRaises(KeyError):
            generator.calendar[Months.ADAR][13]
        self.assertEqual(
            generator.calendar[Months.ADAR][11][0].name,
            'TaAnit Esther'
        )

    def test_rosh_chodesh(self) -> None:
        """Test Rosh Chodesh."""
        generator = CalendarGenerator(False, 5782)  # 2022

        self.assertEqual(
            generator.calendar[Months.NISAN][1][0].name,
            'Rosh Chodesh Nisan'
        )
        self.assertEqual(len(generator.calendar[Months.NISAN][1]), 1)

        self.assertEqual(
            generator.calendar[Months.NISAN][30][0].name,
            'Rosh Chodesh Iyar'
        )
        self.assertEqual(len(generator.calendar[Months.NISAN][30]), 1)
        self.assertEqual(
            generator.calendar[Months.IYAR][1][0].name,
            'Rosh Chodesh Iyar'
        )
        self.assertEqual(len(generator.calendar[Months.IYAR][1]), 1)

        with self.assertRaises(KeyError):
            generator.calendar[Months.IYAR][30]
        self.assertEqual(
            generator.calendar[Months.SIVAN][1][0].name,
            'Rosh Chodesh Sivan'
        )
        self.assertEqual(len(generator.calendar[Months.SIVAN][1]), 1)

        self.assertEqual(
            generator.calendar[Months.SIVAN][30][0].name,
            'Rosh Chodesh Tamuz'
        )
        self.assertEqual(len(generator.calendar[Months.SIVAN][30]), 1)
        self.assertEqual(
            generator.calendar[Months.TAMUZ][1][0].name,
            'Rosh Chodesh Tamuz'
        )
        self.assertEqual(len(generator.calendar[Months.TAMUZ][1]), 1)

        with self.assertRaises(KeyError):
            generator.calendar[Months.TAMUZ][30]
        self.assertEqual(
            generator.calendar[Months.AV][1][0].name,
            'Rosh Chodesh Av'
        )
        self.assertEqual(len(generator.calendar[Months.AV][1]), 1)

        self.assertEqual(
            generator.calendar[Months.AV][30][0].name,
            'Rosh Chodesh Elul'
        )
        self.assertEqual(len(generator.calendar[Months.AV][30]), 1)
        self.assertEqual(
            generator.calendar[Months.ELUL][1][0].name,
            'Rosh Chodesh Elul'
        )
        self.assertEqual(len(generator.calendar[Months.ELUL][1]), 1)

        self.assertEqual(len(generator.calendar[Months.ELUL][29]), 1)
        self.assertEqual(
            generator.calendar[Months.ELUL][29][0].name,
            'Erev Rosh Hashana'
        )
        self.assertEqual(len(generator.calendar[Months.TISHREI][1]), 1)
        self.assertEqual(
            generator.calendar[Months.TISHREI][1][0].name,
            'Rosh Hashana 1'
        )

        self.assertEqual(
            generator.calendar[Months.TISHREI][30][0].name,
            'Rosh Chodesh Cheshvan'
        )
        self.assertEqual(len(generator.calendar[Months.TISHREI][30]), 1)
        self.assertEqual(
            generator.calendar[Months.CHESHVAN][1][0].name,
            'Rosh Chodesh Cheshvan'
        )
        self.assertEqual(len(generator.calendar[Months.CHESHVAN][1]), 1)

        self.assertEqual(
            generator.calendar[Months.KISLEV][1][0].name,
            'Rosh Chodesh Kislev'
        )
        self.assertEqual(len(generator.calendar[Months.KISLEV][1]), 1)

        self.assertEqual(
            generator.calendar[Months.KISLEV][30][1].name,
            'Rosh Chodesh Tevet'
        )
        self.assertEqual(len(generator.calendar[Months.KISLEV][30]), 2)
        self.assertEqual(
            generator.calendar[Months.TEVET][1][1].name,
            'Rosh Chodesh Tevet'
        )
        self.assertEqual(len(generator.calendar[Months.TEVET][1]), 2)

        self.assertEqual(
            generator.calendar[Months.SHEVAT][1][0].name,
            'Rosh Chodesh Shevat'
        )
        self.assertEqual(len(generator.calendar[Months.SHEVAT][1]), 1)

        self.assertEqual(
            generator.calendar[Months.SHEVAT][30][0].name,
            'Rosh Chodesh Adar 1'
        )
        self.assertEqual(len(generator.calendar[Months.SHEVAT][30]), 1)
        self.assertEqual(
            generator.calendar[Months.ADAR][1][0].name,
            'Rosh Chodesh Adar 1'
        )
        self.assertEqual(len(generator.calendar[Months.ADAR][1]), 1)

        self.assertEqual(
            generator.calendar[Months.ADAR][30][0].name,
            'Rosh Chodesh Adar 2'
        )
        self.assertEqual(len(generator.calendar[Months.ADAR][30]), 1)
        self.assertEqual(
            generator.calendar[Months.ADAR_2][1][0].name,
            'Rosh Chodesh Adar 2'
        )
        self.assertEqual(len(generator.calendar[Months.ADAR_2][1]), 1)

    def test_isru_chag(self) -> None:
        """Test Isru Chag."""
        # diaspora
        generator = CalendarGenerator(True, 5783)  # 2022
        self.assertEqual(
            generator.calendar[Months.TISHREI][24][0].name,
            'Isru Chag'
        )

        # Israel
        generator = CalendarGenerator(False, 5783)
        self.assertEqual(
            generator.calendar[Months.TISHREI][23][0].name,
            'Isru Chag'
        )

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
