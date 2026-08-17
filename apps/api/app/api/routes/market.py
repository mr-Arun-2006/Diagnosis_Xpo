from fastapi import APIRouter
from app.schemas.market import MarketSnapshot

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/snapshot", response_model=MarketSnapshot)
def market_snapshot():
    # Provider adapters will replace these placeholders with validated data.
    return MarketSnapshot(
        nifty=0.0,
        sensex=0.0,
        india_vix=0.0,
        market_score=0,
        data_status="not_configured",
    )
