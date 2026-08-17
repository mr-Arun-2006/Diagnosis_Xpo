from __future__ import annotations

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse
from quant_engine.diagnosis import diagnose

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.post("/", response_model=DiagnosisResponse)
def create_diagnosis(payload: DiagnosisRequest) -> DiagnosisResponse:
    rows = [bar.model_dump() for bar in payload.bars]
    frame = pd.DataFrame(rows).sort_values("date").drop_duplicates("date", keep="last")
    if len(frame) < 60:
        raise HTTPException(status_code=422, detail="At least 60 unique trading sessions are required")
    try:
        result = diagnose(frame[["open", "high", "low", "close", "volume"]].reset_index(drop=True))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return DiagnosisResponse(
        symbol=payload.symbol.upper(),
        exchange=payload.exchange,
        as_of=frame["date"].iloc[-1],
        diagnosis=result,
    )
