from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.eod_ingestion import ingest_eod
from app.services.market_repository import MarketRepository

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


class EODInput(BaseModel):
    symbol: str
    exchange: str = Field(pattern="^(NSE|BSE)$")
    trading_date: str
    open: float
    high: float
    low: float
    close: float
    volume: int = 0
    company_name: str | None = None
    source: str = "api"
    checksum: str | None = None


@router.post("/eod")
def ingest(payload: list[EODInput]):
    result = ingest_eod([item.model_dump() for item in payload], MarketRepository())
    return {
        "accepted": result.accepted,
        "rejected": result.rejected,
        "issues": result.issues,
    }
