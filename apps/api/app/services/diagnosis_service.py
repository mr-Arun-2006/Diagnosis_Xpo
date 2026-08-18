from __future__ import annotations

import pandas as pd

from app.services.market_queries import MarketQueryService
from packages.quant_engine import diagnose


class DiagnosisService:
    def __init__(self, market: MarketQueryService | None = None):
        self.market = market or MarketQueryService()

    def run(self, symbol: str, exchange: str, limit: int = 1000) -> dict:
        history = self.market.history(symbol, exchange, limit)
        if len(history) < 60:
            raise ValueError(f"At least 60 validated sessions are required; found {len(history)}")
        frame = pd.DataFrame(history)
        result = diagnose(frame)
        return {
            "symbol": symbol.upper(),
            "exchange": exchange.upper(),
            "sessions": len(history),
            **result,
        }
