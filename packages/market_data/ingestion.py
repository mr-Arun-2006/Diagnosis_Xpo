from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from typing import Callable

from packages.contracts import Bar, Exchange
from .csv_parser import parse_eod_csv
from .provider import ProviderRouter
from .validation import QualityReport, validate_bars


@dataclass(frozen=True, slots=True)
class IngestionResult:
    exchange: Exchange
    trading_date: date
    provider: str
    authority: str
    checksum: str
    report: QualityReport


def ingest_eod(
    router: ProviderRouter,
    *,
    exchange: Exchange,
    trading_date: date,
    persist_raw: Callable[[bytes, str, date, str], None],
    persist_bars: Callable[[list[Bar]], None],
) -> IngestionResult:
    payload, provider, authority = router.fetch(trading_date, exchange.value)
    checksum = hashlib.sha256(payload).hexdigest()
    persist_raw(payload, provider, trading_date, checksum)
    bars = parse_eod_csv(payload, exchange=exchange, trading_date=trading_date)
    report = validate_bars(bars)
    if not report.passed:
        raise ValueError(f"EOD quality gate failed: {report}")
    persist_bars(bars)
    return IngestionResult(exchange, trading_date, provider, authority, checksum, report)
