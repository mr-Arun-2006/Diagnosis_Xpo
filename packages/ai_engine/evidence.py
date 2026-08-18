from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiagnosisEvidence:
    symbol: str
    exchange: str
    close: float
    score: float
    regime: str
    confidence: float
    indicators: dict[str, float | None]
    key_levels: dict[str, float | None]
    evidence: list[str]
    data_timestamp: str | None = None
