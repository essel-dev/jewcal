"""Events model."""

from dataclasses import InitVar, dataclass, field

from jewcal.constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Action


@dataclass
class Events:
    """The events with an action."""

    weekday: InitVar[int]
    """The weekday number in the range of 0-6, where 0=Sunday."""

    month: InitVar[int]
    """The month of the Jewish year."""

    day: InitVar[int]
    """The day in the Jewish month."""

    diaspora: InitVar[bool]
    """`True` if outside of Israel, `False` if in Israel."""

    shabbos: str | None = field(init=False, default=None)
    """(Erev) Shabbos definition."""

    yomtov: str | None = field(init=False, default=None)
    """(Erev) Yom Tov definition."""

    action: str | None = field(init=False, default=None)
    """The action (`Candles` or `Havdalah`).

    If Shabbos and Yom Tov has `Candles` and `Havdalah`, `Candles` has priority.
    """

    def __post_init__(self, weekday: int, month: int, day: int, diaspora: bool) -> None:
        """Post init.

        Args:
            weekday:  The weekday number in the range of 0-6, where 0=Sunday.
            month: The month of the Jewish year.
            day: The day in the Jewish month.
            diaspora: `True` if outside of Israel, `False` if in Israel.
        """
        self._set_shabbos(weekday)
        self._set_yomtov(month, day, diaspora=diaspora)

    def _set_shabbos(self, weekday: int) -> None:
        if weekday in SHABBOS:
            event = SHABBOS[weekday]
            self.shabbos = event.title
            self.action = event.action

    def _set_yomtov(self, month: int, day: int, *, diaspora: bool) -> None:
        holidays = YOMTOV if diaspora else YOMTOV_ISRAEL
        if month in holidays and day in holidays[month]:
            event = holidays[month][day]
            self.yomtov = event.title

            # don't overwrite action `None` if Chol HaMoed is on Shabbos
            if event.action:
                if not self.action:
                    self.action = event.action
                elif self.action != event.action:
                    # if Shabbos / Yom Tov has Candles / Havdalah, Candles has priority
                    self.action = Action.CANDLES.value

    def __str__(self) -> str:
        """Get all the events as a string.

        Returns:
            All the events as a string.
        """
        names = []
        if self.shabbos:
            names.append(self.shabbos)
        if self.yomtov:
            names.append(self.yomtov)

        return ', '.join(names) if names else ''

    def _has_events(self) -> bool:
        return self.shabbos is not None or self.yomtov is not None

    def _is_erev_shabbos(self) -> bool:
        return self.shabbos is not None and 'Erev' in self.shabbos

    def _is_shabbos(self) -> bool:
        return self.shabbos is not None and not self._is_erev_shabbos()

    def _is_erev_yomtov(self) -> bool:
        return all(
            [
                self.yomtov is not None,
                any(
                    [
                        self.yomtov and 'Erev' in self.yomtov,
                        self.yomtov and 'Hoshana Rabba' in self.yomtov,
                        self.yomtov and 'Pesach 6' in self.yomtov,
                    ],
                ),
                self.action == Action.CANDLES.value,
            ],
        )

    def _is_yomtov(self) -> bool:
        return all(
            [
                self.yomtov is not None,
                not self._is_erev_yomtov(),
                self.yomtov and 'Chol HaMoed' not in self.yomtov,
            ],
        )

    def _is_erev(self) -> bool:
        is_erev_shabbos = self._is_erev_shabbos()
        is_erev_yomtov = self._is_erev_yomtov()

        return self.action == Action.CANDLES.value and any(
            [
                is_erev_shabbos and self.yomtov is None,
                self.shabbos is None and is_erev_yomtov,
                is_erev_shabbos and is_erev_yomtov,
                is_erev_shabbos and self.yomtov and 'Chol HaMoed' in self.yomtov,
            ],
        )

    def _is_issur_melacha(self) -> bool:
        return self.action is not None and not self._is_erev()
