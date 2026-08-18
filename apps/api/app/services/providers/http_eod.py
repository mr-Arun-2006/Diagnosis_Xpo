from __future__ import annotations

import hashlib
import os
import urllib.request
from dataclasses import dataclass
from datetime import date

from app.services.eod_ingestion import ingest_eod
from app.services.market_repository import MarketRepository
from app.services.providers.eod_csv import parse_eod_csv


@dataclass(frozen=True)
class ProviderAttempt:
    provider: str
    exchange: str
    status: str
    rows: int = 0
    error: str | None = None


class HTTPProviderManager:
    """Primary/secondary EOD provider chain.

    URLs are supplied by environment variables. Credentials never belong in
    source code and are expected to be embedded/configured by the provider
    endpoint or a future authenticated adapter.
    """

    def __init__(self, repository: MarketRepository | None = None):
        self.repository = repository or MarketRepository()

    def _download(self, url: str) -> bytes:
        request = urllib.request.Request(url, headers={"User-Agent": "Diagnosis_Xpo/0.1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()

    def ingest(self, exchange: str, trading_date: date) -> tuple[list[ProviderAttempt], int]:
        exchange = exchange.upper()
        names = [
            os.getenv(f"{exchange}_EOD_PRIMARY_URL", "").strip(),
            os.getenv(f"{exchange}_EOD_SECONDARY_URL", "").strip(),
        ]
        attempts: list[ProviderAttempt] = []
        for index, url in enumerate(names, start=1):
            if not url:
                continue
            provider = f"{exchange.lower()}-{index}"
            try:
                payload = self._download(url)
                checksum = hashlib.sha256(payload).hexdigest()
                rows = parse_eod_csv(payload, exchange, provider)
                rows = [r for r in rows if r["trading_date"] == trading_date.isoformat()]
                for row in rows:
                    row["checksum"] = checksum
                result = ingest_eod(rows, self.repository)
                attempts.append(ProviderAttempt(provider, exchange, "accepted", result.accepted, "; ".join(result.issues) or None))
                if result.accepted:
                    return attempts, result.accepted
            except Exception as exc:
                attempts.append(ProviderAttempt(provider, exchange, "failed", error=str(exc)))
        return attempts, 0
