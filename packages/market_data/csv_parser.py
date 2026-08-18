from __future__ import annotations

import csv
import io
from datetime import date

from packages.contracts import Bar, Exchange


ALIASES = {
    "symbol": {"symbol", "ticker", "security", "securitysymbol", "sc_code"},
    "open": {"open", "openprice"},
    "high": {"high", "highprice"},
    "low": {"low", "lowprice"},
    "close": {"close", "closeprice", "last", "lastprice"},
    "volume": {"volume", "tottrdqty", "totaltradedquantity", "qty"},
}


def _key(value: str) -> str:
    return "".join(ch for ch in value.strip().lower() if ch.isalnum() or ch == "_")


def _columns(fieldnames: list[str]) -> dict[str, str]:
    normalized = {_key(name): name for name in fieldnames}
    found: dict[str, str] = {}
    for target, aliases in ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                found[target] = normalized[alias]
                break
    missing = {"symbol", "open", "high", "low", "close", "volume"} - found.keys()
    if missing:
        raise ValueError(f"EOD CSV missing required columns: {sorted(missing)}")
    return found


def parse_eod_csv(payload: bytes, *, exchange: Exchange, trading_date: date) -> list[Bar]:
    text = payload.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("EOD CSV has no header")
    columns = _columns(reader.fieldnames)
    rows: list[Bar] = []
    for row in reader:
        symbol = str(row[columns["symbol"]]).strip().upper()
        if not symbol:
            continue
        rows.append(Bar(
            symbol=symbol,
            exchange=exchange,
            trading_date=trading_date,
            open=float(row[columns["open"]]),
            high=float(row[columns["high"]]),
            low=float(row[columns["low"]]),
            close=float(row[columns["close"]]),
            volume=float(row[columns["volume"]]),
        ))
    return rows
