from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(exchange: str = Query("NSE", pattern="^(NSE|BSE)$"), limit: int = 50):
    try:
        return DashboardService().build(exchange, limit)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
