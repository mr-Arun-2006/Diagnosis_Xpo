from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum


class Exchange(StrEnum):
    NSE = "NSE"
    BSE = "BSE"


@dataclass(frozen=True, slots=True)
class Instrument:
    symbol: str
    exchange: Exchange
    name: str | None = None
    sector: str | None = None
    isin: str | None = None


@dataclass(frozen=True, slots=True)
class Bar:
    symbol: str
    exchange: Exchange
    trading_date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    delivery_volume: float | None = None


@dataclass(frozen=True, slots=True)
class Quote:
    symbol: str
    exchange: Exchange
    price: float
    timestamp: datetime
    volume: float | None = None
    source: str = "unknown"
