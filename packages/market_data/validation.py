from __future__ import annotations

from dataclasses import dataclass
from packages.contracts import Bar


@dataclass(frozen=True, slots=True)
class QualityReport:
    total: int
    valid: int
    duplicate: int
    invalid_ohlc: int
    invalid_volume: int

    @property
    def passed(self) -> bool:
        return self.valid > 0 and self.duplicate == 0 and self.invalid_ohlc == 0 and self.invalid_volume == 0


def validate_bars(bars: list[Bar]) -> QualityReport:
    seen: set[tuple[str, str, object]] = set()
    duplicate = invalid_ohlc = invalid_volume = 0
    valid = 0
    for bar in bars:
        key = (bar.exchange.value, bar.symbol, bar.trading_date)
        if key in seen:
            duplicate += 1
            continue
        seen.add(key)
        if min(bar.open, bar.high, bar.low, bar.close) <= 0 or bar.high < max(bar.open, bar.close) or bar.low > min(bar.open, bar.close):
            invalid_ohlc += 1
            continue
        if bar.volume < 0:
            invalid_volume += 1
            continue
        valid += 1
    return QualityReport(len(bars), valid, duplicate, invalid_ohlc, invalid_volume)
