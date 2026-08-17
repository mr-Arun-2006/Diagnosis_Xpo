from __future__ import annotations

from fastapi import APIRouter

from app.schemas.screener import ScreenerRequest, ScreenerResponse

router = APIRouter(prefix="/screener", tags=["screener"])


@router.post("/scan", response_model=ScreenerResponse)
def scan(payload: ScreenerRequest) -> ScreenerResponse:
    # The data adapter will populate this endpoint once a live/EOD provider is configured.
    return ScreenerResponse(count=0, rows=[], data_status="not_configured")
