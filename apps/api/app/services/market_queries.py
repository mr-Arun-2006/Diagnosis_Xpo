from __future__ import annotations

import os

import psycopg


class MarketQueryService:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.getenv("DATABASE_URL", "")

    def _connect(self):
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        return psycopg.connect(self.database_url)

    def latest(self, exchange: str, limit: int = 50) -> list[dict]:
        safe_limit = min(max(limit, 1), 500)
        with self._connect() as conn:
            rows = conn.execute(
                """SELECT symbol, company_name, sector, trading_date, open, high, low, close, volume
                   FROM (
                     SELECT DISTINCT ON (i.symbol)
                            i.symbol, i.company_name, i.sector, e.trading_date,
                            e.open, e.high, e.low, e.close, e.volume
                     FROM eod_prices e
                     JOIN instruments i ON i.id = e.instrument_id
                     WHERE i.exchange = %s AND i.active = TRUE
                     ORDER BY i.symbol, e.trading_date DESC
                   ) latest_per_symbol
                   ORDER BY trading_date DESC, symbol
                   LIMIT %s""",
                (exchange.upper(), safe_limit),
            ).fetchall()
        keys = ("symbol", "company_name", "sector", "trading_date", "open", "high", "low", "close", "volume")
        return [dict(zip(keys, row)) for row in rows]

    def history(self, symbol: str, exchange: str, limit: int = 5000) -> list[dict]:
        safe_limit = min(max(limit, 1), 5000)
        with self._connect() as conn:
            rows = conn.execute(
                """SELECT trading_date, open, high, low, close, volume
                   FROM eod_prices e JOIN instruments i ON i.id = e.instrument_id
                   WHERE i.symbol = %s AND i.exchange = %s
                   ORDER BY trading_date DESC LIMIT %s""",
                (symbol.upper(), exchange.upper(), safe_limit),
            ).fetchall()
        keys = ("trading_date", "open", "high", "low", "close", "volume")
        return [dict(zip(keys, row)) for row in reversed(rows)]
