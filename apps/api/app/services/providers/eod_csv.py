from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True)
class EODProviderConfig:
    name: str
    url: str


def parse_eod_csv(payload: bytes, exchange: str, source: str) -> list[dict]:
    """Parse provider CSV data into the stable EOD ingestion contract."""
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

    def parse_date(raw: str) -> date:
        for fmt in ("%d-%b-%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(raw, fmt).date()
            except ValueError:
                pass
        raise ValueError(f"Unsupported trading date: {raw}")

    rows: list[dict] = []
    for row in reader:
        rows.append({
            "symbol": value(row, aliases["symbol"]).upper(),
            "exchange": exchange.upper(),
            "trading_date": parse_date(value(row, aliases["date"])).isoformat(),
            "open": Decimal(value(row, aliases["open"])),
            "high": Decimal(value(row, aliases["high"])),
            "low": Decimal(value(row, aliases["low"])),
            "close": Decimal(value(row, aliases["close"])),
            "volume": int(float(value(row, aliases["volume"]))),
            "source": source,
        })
    return rows
