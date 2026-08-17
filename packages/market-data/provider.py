from abc import ABC, abstractmethod
from datetime import date

from .models import DataBatch


class MarketDataProvider(ABC):
    """Provider boundary: official, licensed, broker or fallback sources implement this contract."""

    name: str
    authority: str = "third-party"

    @abstractmethod
    def fetch_eod(self, trading_date: date) -> DataBatch:
        raise NotImplementedError


class OfficialProviderUnavailable(RuntimeError):
    pass


class ProviderRouter:
    def __init__(self, primary: MarketDataProvider, secondary: MarketDataProvider | None = None):
        self.primary = primary
        self.secondary = secondary

    def fetch_eod(self, trading_date: date) -> DataBatch:
        try:
            return self.primary.fetch_eod(trading_date)
        except Exception as primary_error:
            if self.secondary is None:
                raise OfficialProviderUnavailable(
                    f"Primary provider {self.primary.name} failed and no fallback is configured"
                ) from primary_error
            return self.secondary.fetch_eod(trading_date)
