"""AI boundary: explanations are generated from structured evidence only."""
from .evidence import DiagnosisEvidence
from .explainer import build_prompt

__all__ = ["DiagnosisEvidence", "build_prompt"]
