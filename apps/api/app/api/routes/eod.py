from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.services.providers.http_eod import HTTPProviderManager

router = APIRouter(prefix="/eod", tags=["eod"])


@router.post("/ingest")
def run_eod(exchange: str = Query("NSE", pattern="^(NSE|BSE)$"), trading_date: date | None = None):
    target = trading_date or date.today()
    attempts, accepted = HTTPProviderManager().ingest(exchange, target)
    if not attempts:
        raise HTTPException(status_code=503, detail="No EOD provider URL configured")
    return {
        "exchange": exchange,
        "trading_date": target,
        "accepted": accepted,
        "attempts": [a.__dict__ for a in attempts],
    }
