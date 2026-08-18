from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Iterable

from packages.contracts import Bar, Exchange


@dataclass(frozen=True, slots=True)
class IngestionResult:
    exchange: Exchange
    trading_date: date
    rows_read: int
    rows_valid: int
    rows_rejected: int
    source: str


def run_pipeline(
    rows: Iterable[dict],
    *,
    exchange: Exchange,
    trading_date: date,
    source: str,
    persist: Callable[[list[Bar]], None],
) -> IngestionResult:
    """Normalize/validate rows, then persist only canonical bars.

    Provider adapters own parsing. This boundary owns the invariant that bad rows
    never reach the analytical store.
    """
    normalized: list[Bar] = []
    read = 0
    rejected = 0
    seen: set[tuple[str, date]] = set()
    for row in rows:
        read += 1
        try:
            symbol = str(row["symbol"]).strip().upper()
            key = (symbol, trading_date)
            if not symbol or key in seen:
                raise ValueError("empty or duplicate symbol")
            bar = Bar(
                symbol=symbol,
                exchange=exchange,
                trading_date=trading_date,
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row["volume"]),
                delivery_volume=(float(row["delivery_volume"]) if row.get("delivery_volume") not in (None, "") else None),
            )
            if not (bar.low <= bar.open <= bar.high and bar.low <= bar.close <= bar.high):
                raise ValueError("OHLC range invariant failed")
            if bar.volume < 0:
                raise ValueError("negative volume")
            seen.add(key)
            normalized.append(bar)
        except (KeyError, TypeError, ValueError):
            rejected += 1
    if normalized:
        persist(normalized)
    return IngestionResult(exchange, trading_date, read, len(normalized), rejected, source)
