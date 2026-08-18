from __future__ import annotations

from app.services.market_queries import MarketQueryService
from packages.quant_engine.quant_engine import diagnose


class DashboardService:
    def __init__(self, market: MarketQueryService | None = None):
        self.market = market or MarketQueryService()

    def build(self, exchange: str = "NSE", limit: int = 50) -> dict:
        latest = self.market.latest(exchange, limit)
        scored: list[dict] = []
        for row in latest:
            history = self.market.history(row["symbol"], exchange, 120)
            if len(history) < 60:
                continue
            diagnosis = diagnose(history)
            scored.append({
                "symbol": row["symbol"],
                "sector": row.get("sector"),
                "price": float(row["close"]),
                "score": float(diagnosis.get("score", 0)),
                "regime": str(diagnosis.get("regime", "unknown")),
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return {
            "exchange": exchange,
            "data_status": "live_database" if scored else "no_validated_data",
            "universe_count": len(scored),
            "top_ranked": scored[:10],
        }
