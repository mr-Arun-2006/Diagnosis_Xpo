from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field


class OHLCVBar(BaseModel):
    date: date
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)


class DiagnosisRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=40)
    exchange: str = Field(default="NSE", pattern="^(NSE|BSE)$")
    bars: list[OHLCVBar] = Field(min_length=60, max_length=5000)


class DiagnosisResponse(BaseModel):
    symbol: str
    exchange: str
    as_of: date
    diagnosis: dict
