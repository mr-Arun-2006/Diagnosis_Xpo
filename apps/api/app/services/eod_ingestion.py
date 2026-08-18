from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.services.data_quality import validate_ohlcv
from app.services.market_repository import EODRow, MarketRepository


@dataclass(frozen=True)
class IngestionResult:
    accepted: int
    rejected: int
    issues: list[str]


def ingest_eod(rows: list[dict], repository: MarketRepository) -> IngestionResult:
    issues = validate_ohlcv(rows)
    bad_rows = {issue.row for issue in issues}
    accepted_rows: list[EODRow] = []

    for index, row in enumerate(rows, start=1):
        if index in bad_rows:
            continue
        accepted_rows.append(
            EODRow(
                symbol=str(row["symbol"]).strip().upper(),
                exchange=str(row["exchange"]).strip().upper(),
                company_name=str(row.get("company_name") or row["symbol"]).strip(),
                trading_date=date.fromisoformat(str(row["trading_date"])),
                open=Decimal(str(row["open"])),
                high=Decimal(str(row["high"])),
                low=Decimal(str(row["low"])),
                close=Decimal(str(row["close"])),
                volume=int(row.get("volume", 0)),
                source=str(row.get("source") or "unknown"),
                checksum=row.get("checksum"),
            )
        )

    repository.upsert_instruments(accepted_rows)
    repository.upsert_eod(accepted_rows)
    return IngestionResult(len(accepted_rows), len(bad_rows), [i.message for i in issues])
