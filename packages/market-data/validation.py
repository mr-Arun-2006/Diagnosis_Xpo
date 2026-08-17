from dataclasses import dataclass
from decimal import Decimal

from .models import DataBatch


@dataclass(frozen=True)
class QualityReport:
    row_count: int
    duplicate_count: int
    invalid_ohlc_count: int
    invalid_volume_count: int

    @property
    def passed(self) -> bool:
        return self.duplicate_count == 0 and self.invalid_ohlc_count == 0 and self.invalid_volume_count == 0


def validate_batch(batch: DataBatch) -> QualityReport:
    seen: set[tuple[str, str, object]] = set()
    duplicates = 0
    invalid_ohlc = 0
    invalid_volume = 0

    for record in batch.records:
        key = (record.exchange, record.symbol, record.trading_date)
        if key in seen:
            duplicates += 1
        seen.add(key)

        values = [record.open, record.high, record.low, record.close]
        if any(value <= Decimal("0") for value in values):
            invalid_ohlc += 1
        if record.high < max(record.open, record.close) or record.low > min(record.open, record.close):
            invalid_ohlc += 1
        if record.volume < 0:
            invalid_volume += 1

    return QualityReport(
        row_count=len(batch.records),
        duplicate_count=duplicates,
        invalid_ohlc_count=invalid_ohlc,
        invalid_volume_count=invalid_volume,
    )


def require_valid_batch(batch: DataBatch) -> QualityReport:
    report = validate_batch(batch)
    if not report.passed:
        raise ValueError(f"Market-data quality gate failed: {report}")
    return report
