from __future__ import annotations

from app.services.market_queries import MarketQueryService
from packages.quant_engine.quant_engine import diagnose


class ScreenerService:
    def __init__(self, market: MarketQueryService | None = None):
        self.market = market or MarketQueryService()

    def scan(self, payload) -> list[dict]:
        rows = self.market.latest(payload.exchange, min(payload.limit * 4, 500))
        results: list[dict] = []
        for row in rows:
            history = self.market.history(row["symbol"], payload.exchange, 300)
            if len(history) < 60:
                continue
            result = diagnose(history)
            score = float(result.get("score", 0))
            regime = str(result.get("regime", "unknown"))
            indicators = result.get("indicators", {})
            rsi = indicators.get("rsi")
            relative_volume = indicators.get("relative_volume")
            if payload.sector and (row.get("sector") or "").lower() != payload.sector.lower():
                continue
            if payload.regime and regime.lower() != payload.regime.lower():
                continue
            if payload.min_score is not None and score < payload.min_score:
                continue
            if payload.min_rsi is not None and (rsi is None or rsi < payload.min_rsi):
                continue
            if payload.max_rsi is not None and (rsi is None or rsi > payload.max_rsi):
                continue
            if payload.min_relative_volume is not None and (relative_volume is None or relative_volume < payload.min_relative_volume):
                continue
            results.append({"symbol": row["symbol"], "exchange": payload.exchange, "sector": row.get("sector"), "price": float(row["close"]), "score": score, "regime": regime, "rsi": rsi, "relative_volume": relative_volume})
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:payload.limit]
