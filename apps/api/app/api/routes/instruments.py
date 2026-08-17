from fastapi import APIRouter
from app.schemas.instruments import Instrument

router = APIRouter(prefix="/instruments", tags=["instruments"])


@router.get("/search", response_model=list[Instrument])
def search_instruments(q: str, exchange: str | None = None):
    """Search contract. Real instrument-master storage plugs in here."""
    if not q.strip():
        return []
    return []
