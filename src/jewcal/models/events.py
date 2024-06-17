"""Events model."""

from dataclasses import dataclass, field

from jewcal.constants import Action


@dataclass
class Events:
    """The events with an action."""

    shabbos: str | None = field(init=False, default=None)
    """(Erev) Shabbos definition."""

    yomtov: str | None = field(init=False, default=None)
    """(Erev) Yom Tov definition."""

    action: str | None = field(init=False, default=None)
    """The action (`Candles` or `Havdalah`).

    If Shabbos and Yom Tov has `Candles` and `Havdalah`, `Candles` has priority.
    """

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
