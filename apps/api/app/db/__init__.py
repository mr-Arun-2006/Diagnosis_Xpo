from __future__ import annotations

import os
from pathlib import Path


def initialize_database() -> None:
    """Initialize local PostgreSQL schema when DATABASE_URL is configured.

    This lightweight bootstrap is intentionally idempotent. Production
    deployments should run versioned migrations before starting workers.
    """
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        return

    try:
        import psycopg
    except ImportError:
        return

    schema_path = Path(__file__).resolve().parent / "market_schema.sql"
    with psycopg.connect(database_url) as conn:
        conn.execute(schema_path.read_text(encoding="utf-8"))
        conn.commit()
