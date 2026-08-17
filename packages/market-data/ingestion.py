import hashlib
from datetime import date

from .models import DataBatch
from .provider import MarketDataProvider, ProviderRouter
from .validation import QualityReport, require_valid_batch


class EODIngestionService:
    """Fetch -> quality gate -> publish boundary. Raw persistence is intentionally provider-specific."""

    def __init__(self, provider: MarketDataProvider, fallback: MarketDataProvider | None = None):
        self.router = ProviderRouter(provider, fallback)

    def run(self, trading_date: date) -> tuple[DataBatch, QualityReport]:
        batch = self.router.fetch_eod(trading_date)
        report = require_valid_batch(batch)
        return batch, report


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()
