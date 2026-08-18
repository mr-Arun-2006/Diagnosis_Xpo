from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class QualityIssue:
    row: int
    code: str
    message: str


def validate_ohlcv(rows: list[dict]) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    seen: set[tuple[str, str, str]] = set()
    for i, row in enumerate(rows, start=1):
        symbol = str(row.get("symbol", "")).strip().upper()
        exchange = str(row.get("exchange", "")).strip().upper()
        trading_date = str(row.get("trading_date", ""))
        key = (exchange, symbol, trading_date)
        if key in seen:
            issues.append(QualityIssue(i, "duplicate", f"Duplicate {key}"))
        seen.add(key)
        try:
            o, h, l, c = (Decimal(str(row[x])) for x in ("open", "high", "low", "close"))
            volume = int(row.get("volume", 0))
            if min(o, h, l, c) <= 0:
                raise ValueError("prices must be positive")
            if h < max(o, c) or l > min(o, c) or h < l or volume < 0:
                raise ValueError("invalid OHLCV relationships")
        except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
            issues.append(QualityIssue(i, "invalid_ohlcv", str(exc)))
    return issues
