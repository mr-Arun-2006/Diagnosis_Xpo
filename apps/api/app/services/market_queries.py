from __future__ import annotations

import os
from datetime import date

import psycopg


class MarketQueryService:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.getenv("DATABASE_URL", "")

    def _connect(self):
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        return psycopg.connect(self.database_url)

    def latest(self, exchange: str, limit: int = 50) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """SELECT i.symbol, i.company_name, i.sector, e.trading_date,
                          e.open, e.high, e.low, e.close, e.volume
                   FROM eod_prices e JOIN instruments i ON i.id=e.instrument_id
                   WHERE i.exchange=%s ORDER BY e.trading_date DESC, i.symbol LIMIT %s""",
                (exchange.upper(), min(max(limit, 1), 500)),
            ).fetchall()
        return [dict(zip(("symbol","company_name","sector","trading_date","open","high","low","close","volume"), r)) for r in rows]

    def history(self, symbol: str, exchange: str, limit: int = 5000) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """SELECT trading_date, open, high, low, close, volume
                   FROM eod_prices e JOIN instruments i ON i.id=e.instrument_id
                   WHERE i.symbol=%s AND i.exchange=%s
                   ORDER BY trading_date DESC LIMIT %s""",
                (symbol.upper(), exchange.upper(), min(max(limit, 1), 5000)),
            ).fetchall()
        keys = ("trading_date", "open", "high", "low", "close", "volume")
        return [dict(zip(keys, r)) for r in reversed(rows)]
