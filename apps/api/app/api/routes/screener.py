from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.screener import ScreenerRequest, ScreenerResponse
from app.services.screener_service import ScreenerService

router = APIRouter(prefix="/screener", tags=["screener"])


@router.post("/scan", response_model=ScreenerResponse)
def scan(payload: ScreenerRequest) -> ScreenerResponse:
    try:
        rows = ScreenerService().scan(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ScreenerResponse(count=len(rows), rows=rows, data_status="live_database")
