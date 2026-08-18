from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse
from app.services.diagnosis_service import DiagnosisService
from quant_engine.diagnosis import diagnose

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.post("/", response_model=DiagnosisResponse)
def create_diagnosis(payload: DiagnosisRequest) -> DiagnosisResponse:
    rows = [bar.model_dump() for bar in payload.bars]
    try:
        result = diagnose(rows)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return DiagnosisResponse(
        symbol=payload.symbol.upper(),
        exchange=payload.exchange,
        as_of=rows[-1]["date"] if rows else "",
        diagnosis=result,
    )


@router.get("/{symbol}")
def stored_diagnosis(symbol: str, exchange: str = Query("NSE", pattern="^(NSE|BSE)$"), limit: int = 1000):
    try:
        return DiagnosisService().run(symbol, exchange, limit)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
