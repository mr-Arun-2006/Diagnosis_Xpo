from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from io import StringIO
from typing import Protocol

import pandas as pd

REQUIRED_COLUMNS = ("symbol", "date", "open", "high", "low", "close", "volume")


@dataclass(frozen=True)
class EODBatch:
    source: str
    trading_date: date
    checksum: str
    rows: int
    records: list[dict]


class EODProvider(Protocol):
    name: str

    def fetch(self, trading_date: date) -> bytes: ...


def validate_eod_frame(frame: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing EOD columns: {', '.join(missing)}")

    result = frame[list(REQUIRED_COLUMNS)].copy()
    result["symbol"] = result["symbol"].astype(str).str.strip().str.upper()
    result["date"] = pd.to_datetime(result["date"], errors="coerce").dt.date
    for column in ("open", "high", "low", "close", "volume"):
        result[column] = pd.to_numeric(result[column], errors="coerce")

    result = result.dropna(subset=list(REQUIRED_COLUMNS))
    result = result.drop_duplicates(subset=["symbol", "date"], keep="last")
    valid_ohlc = (
        (result["open"] > 0)
        & (result["high"] >= result[["open", "close"]].max(axis=1))
        & (result["low"] <= result[["open", "close"]].min(axis=1))
        & (result["low"] > 0)
        & (result["volume"] >= 0)
    )
    result = result.loc[valid_ohlc].sort_values(["symbol", "date"])
    if result.empty:
        raise ValueError("EOD validation produced zero valid records")
    return result.reset_index(drop=True)


def parse_csv(payload: bytes, source: str, trading_date: date) -> EODBatch:
    checksum = sha256(payload).hexdigest()
    frame = validate_eod_frame(pd.read_csv(StringIO(payload.decode("utf-8-sig"))))
    return EODBatch(
        source=source,
        trading_date=trading_date,
        checksum=checksum,
        rows=len(frame),
        records=frame.to_dict(orient="records"),
    )
