from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

@dataclass(frozen=True)
class Quote:
    symbol: str
    exchange: str
    price: float
    timestamp: datetime

class MarketDataProvider(Protocol):
    name: str
    def quote(self, symbol: str, exchange: str) -> Quote: ...

class EODProvider(Protocol):
    name: str
    def download(self, trading_date: str) -> bytes: ...
