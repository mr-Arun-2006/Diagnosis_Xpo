from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class EODProviderConfig:
    name: str
    url: str


def parse_eod_csv(payload: bytes, exchange: str, source: str) -> list[dict]:
    """Parse a provider CSV into the normalized ingestion contract.

    Provider-specific column aliases are intentionally handled here so the
    rest of the pipeline receives one stable schema.
    """
    text = payload.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    aliases = {
        "symbol": ("SYMBOL", "Symbol", "symbol", "TckrSymb"),
        "date": ("TIMESTAMP", "Date", "DATE", "TradDt"),
        "open": ("OPEN", "Open", "open", "OpnPric"),
        "high": ("HIGH", "High", "high", "HghPric"),
        "low": ("LOW", "Low", "low", "LwPric"),
        "close": ("CLOSE", "Close", "close", "ClsPric"),
        "volume": ("TOTTRDQTY", "Volume", "VOLUME", "volume", "TtlTradgVol"),
    }

    def value(row: dict, names: tuple[str, ...]) -> str:
        for name in names:
            if name in row and row[name] not in (None, ""):
                return str(row[name]).strip()
        raise ValueError(f"Missing provider field; expected one of {names}")

    rows: list[dict] = []
    for row in reader:
        raw_date = value(row, aliases["date"])
        for fmt in ("%d-%b-%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                trading_date = date.fromisoformat(date.strptime(raw_date, fmt).isoformat())
                break
            except ValueError:
                trading_date = None
        if trading_date is None:
            raise ValueError(f"Unsupported trading date: {raw_date}")
        rows.append({
            "symbol": value(row, aliases["symbol"]).upper(),
            "exchange": exchange.upper(),
            "trading_date": trading_date.isoformat(),
            "open": Decimal(value(row, aliases["open"])),
            "high": Decimal(value(row, aliases["high"])),
            "low": Decimal(value(row, aliases["low"])),
            "close": Decimal(value(row, aliases["close"])),
            "volume": int(float(value(row, aliases["volume"]))),
            "source": source,
        })
    return rows
