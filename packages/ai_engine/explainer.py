from __future__ import annotations

from .evidence import DiagnosisEvidence


def build_prompt(evidence: DiagnosisEvidence, language: str = "en") -> str:
    """Build an evidence-grounded prompt; model/provider invocation stays outside this package."""
    return (
        "You are a market-education analyst. Explain only the supplied evidence; "
        "do not invent prices, indicators, events or certainty. Distinguish facts "
        "from interpretation and state when data is missing. Language: " + language + "\n\n"
        f"Symbol: {evidence.symbol}\nExchange: {evidence.exchange}\n"
        f"Close: {evidence.close}\nScore: {evidence.score:.2f}\n"
        f"Regime: {evidence.regime}\nConfidence: {evidence.confidence:.2f}\n"
        f"Indicators: {evidence.indicators}\nKey levels: {evidence.key_levels}\n"
        f"Evidence: {evidence.evidence}\nTimestamp: {evidence.data_timestamp}\n"
    )
