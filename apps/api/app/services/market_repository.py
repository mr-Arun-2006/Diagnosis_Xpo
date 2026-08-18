from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True)
class EODRow:
    symbol: str
    exchange: str
    company_name: str
    trading_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    source: str
    checksum: str | None = None


class MarketRepository:
    """Persistence interface for normalized market data.

    The SQL schema is the source of truth. A concrete connection-backed
    implementation can be introduced without changing provider adapters.
    """

    def upsert_instruments(self, rows: Iterable[EODRow]) -> int:
        return len({(r.exchange, r.symbol) for r in rows})

    def upsert_eod(self, rows: Iterable[EODRow]) -> int:
        return sum(1 for _ in rows)
