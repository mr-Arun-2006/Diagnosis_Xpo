from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import os

from app.services.eod import EODBatch, EODProvider, parse_csv


@dataclass
class ProviderConfig:
    primary: str = os.getenv("EOD_PRIMARY_PROVIDER", "nse")
    secondary: str = os.getenv("EOD_SECONDARY_PROVIDER", "bse")


class ConfiguredProvider:
    """HTTP provider adapter boundary; concrete NSE/BSE clients plug in here."""

    def __init__(self, name: str, url_env: str):
        self.name = name
        self.url = os.getenv(url_env, "").strip()

    def fetch(self, trading_date: date) -> bytes:
        raise RuntimeError(
            f"{self.name} provider is not configured. Set the provider URL/API integration for {trading_date}."
        )


class ProviderChain:
    def __init__(self, providers: list[EODProvider]):
        self.providers = providers

    def ingest(self, trading_date: date) -> EODBatch:
        errors: list[str] = []
        for provider in self.providers:
            try:
                payload = provider.fetch(trading_date)
                return parse_csv(payload, provider.name, trading_date)
            except Exception as exc:
                errors.append(f"{provider.name}: {exc}")
        raise RuntimeError("All EOD providers failed: " + " | ".join(errors))


def default_provider_chain() -> ProviderChain:
    return ProviderChain(
        [
            ConfiguredProvider("nse", "NSE_EOD_URL"),
            ConfiguredProvider("bse", "BSE_EOD_URL"),
        ]
    )
