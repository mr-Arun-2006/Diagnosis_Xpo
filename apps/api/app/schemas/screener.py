from __future__ import annotations

from pydantic import BaseModel, Field


class ScreenerRequest(BaseModel):
    exchange: str = "NSE"
    sector: str | None = None
    regime: str | None = None
    min_score: float | None = Field(default=None, ge=0, le=100)
    max_rsi: float | None = Field(default=None, ge=0, le=100)
    min_rsi: float | None = Field(default=None, ge=0, le=100)
    min_relative_volume: float | None = Field(default=None, ge=0)
    limit: int = Field(default=50, ge=1, le=200)


class ScreenerRow(BaseModel):
    symbol: str
    exchange: str
    sector: str | None = None
    price: float
    score: float
    regime: str
    rsi: float | None = None
    relative_volume: float | None = None


class ScreenerResponse(BaseModel):
    count: int
    rows: list[ScreenerRow]
    data_status: str
