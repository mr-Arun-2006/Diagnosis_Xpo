from fastapi import APIRouter, HTTPException, Query

from app.schemas.market import MarketSnapshot
from app.services.market_queries import MarketQueryService

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/snapshot", response_model=MarketSnapshot)
def market_snapshot():
    # Index-level providers are wired separately; never fabricate values.
    return MarketSnapshot(
        nifty=0.0,
        sensex=0.0,
        india_vix=0.0,
        market_score=0,
        data_status="provider_not_configured",
    )


@router.get("/eod")
def latest_eod(exchange: str = Query("NSE", pattern="^(NSE|BSE)$"), limit: int = 50):
    try:
        return {"exchange": exchange, "data": MarketQueryService().latest(exchange, limit)}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/history/{symbol}")
def symbol_history(symbol: str, exchange: str = Query("NSE", pattern="^(NSE|BSE)$"), limit: int = 5000):
    try:
        data = MarketQueryService().history(symbol, exchange, limit)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if not data:
        raise HTTPException(status_code=404, detail="No validated EOD history found")
    return {"symbol": symbol.upper(), "exchange": exchange, "data": data}
