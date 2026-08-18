from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ai_service import AIExplanationService
from packages.ai_engine import DiagnosisEvidence

router = APIRouter(prefix="/ai", tags=["ai"])


class ExplainRequest(BaseModel):
    evidence: DiagnosisEvidence
    language: str = Field(default="en", pattern="^(en|ta|hi|gu)$")


@router.post("/explain")
def explain(payload: ExplainRequest):
    try:
        return AIExplanationService().explain(payload.evidence, payload.language)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
