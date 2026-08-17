from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

Exchange = Literal["NSE", "BSE"]
AssetType = Literal["equity", "index", "etf", "future", "option"]


@dataclass(frozen=True)
class EODRecord:
    symbol: str
    exchange: Exchange
    trading_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    asset_type: AssetType = "equity"
    source: str = "unknown"
    received_at: datetime | None = None


@dataclass(frozen=True)
class DataBatch:
    records: list[EODRecord]
    source: str
    trading_date: date
    checksum: str | None = None
    raw_object: str | None = None
