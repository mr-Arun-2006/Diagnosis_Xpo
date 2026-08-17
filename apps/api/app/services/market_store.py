from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class StoredEOD:
    symbol: str
    exchange: str
    trading_date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class MarketStore:
    """Storage boundary for normalized market data.

    PostgreSQL/Parquet implementations can be plugged in without changing
    provider adapters or API contracts.
    """

    def save_eod(self, rows: list[StoredEOD]) -> int:
        # Persistence is intentionally isolated until migrations are added.
        return len(rows)
