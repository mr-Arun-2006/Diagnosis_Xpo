"""Canonical market-data adapters and ingestion pipeline."""
from .csv_parser import parse_eod_csv
from .provider import EODProvider, ProviderRouter, UrlTemplateProvider
from .validation import QualityReport, validate_bars

__all__ = ["EODProvider", "ProviderRouter", "UrlTemplateProvider", "QualityReport", "parse_eod_csv", "validate_bars"]
