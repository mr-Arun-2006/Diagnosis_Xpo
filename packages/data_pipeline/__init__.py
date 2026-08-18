"""Deterministic ingestion orchestration boundary."""
from .pipeline import IngestionResult, run_pipeline

__all__ = ["IngestionResult", "run_pipeline"]
