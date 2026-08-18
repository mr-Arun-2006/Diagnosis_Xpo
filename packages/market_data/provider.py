from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from urllib.request import Request, urlopen


class ProviderError(RuntimeError):
    pass


class EODProvider:
    name: str = "unknown"
    authority: str = "third-party"

    def fetch(self, trading_date: date, exchange: str) -> bytes:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class UrlTemplateProvider(EODProvider):
    """HTTP provider configured by environment; keeps provider URLs out of application logic."""

    name: str
    url_template: str
    authority: str = "third-party"
    timeout_seconds: int = 30
    user_agent: str = "Diagnosis_Xpo/1.0"

    def fetch(self, trading_date: date, exchange: str) -> bytes:
        url = self.url_template.format(
            date=trading_date.isoformat(),
            yyyymmdd=trading_date.strftime("%Y%m%d"),
            exchange=exchange,
        )
        request = Request(url, headers={"User-Agent": self.user_agent, "Accept": "text/csv,*/*"})
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = response.read()
        except Exception as exc:
            raise ProviderError(f"{self.name} failed for {exchange} {trading_date}: {exc}") from exc
        if not payload:
            raise ProviderError(f"{self.name} returned an empty payload")
        return payload


@dataclass(frozen=True, slots=True)
class ProviderRouter:
    primary: EODProvider
    fallback: EODProvider | None = None

    def fetch(self, trading_date: date, exchange: str) -> tuple[bytes, str, str]:
        try:
            return self.primary.fetch(trading_date, exchange), self.primary.name, self.primary.authority
        except ProviderError as primary_error:
            if self.fallback is None:
                raise
            try:
                return self.fallback.fetch(trading_date, exchange), self.fallback.name, self.fallback.authority
            except ProviderError as fallback_error:
                raise ProviderError(f"Primary and fallback providers failed: {primary_error}; {fallback_error}") from fallback_error
