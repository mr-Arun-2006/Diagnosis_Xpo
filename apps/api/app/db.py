from collections.abc import Generator

import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user','trader','researcher','admin')),
    language TEXT NOT NULL DEFAULT 'en' CHECK (language IN ('en','ta','hi','gu')),
    default_exchange TEXT NOT NULL DEFAULT 'NSE' CHECK (default_exchange IN ('NSE','BSE')),
    notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS refresh_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS instruments (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(64) NOT NULL,
    exchange VARCHAR(8) NOT NULL CHECK (exchange IN ('NSE','BSE')),
    company_name TEXT NOT NULL DEFAULT '',
    sector TEXT,
    industry TEXT,
    isin VARCHAR(32),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (exchange, symbol)
);

CREATE TABLE IF NOT EXISTS raw_eod_payloads (
    id BIGSERIAL PRIMARY KEY,
    exchange VARCHAR(8) NOT NULL CHECK (exchange IN ('NSE','BSE')),
    trading_date DATE NOT NULL,
    provider VARCHAR(128) NOT NULL,
    authority VARCHAR(64) NOT NULL DEFAULT 'third-party',
    checksum VARCHAR(128) NOT NULL,
    payload BYTEA NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (exchange, trading_date, checksum)
);

CREATE TABLE IF NOT EXISTS eod_prices (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    trading_date DATE NOT NULL,
    open NUMERIC(20,6) NOT NULL,
    high NUMERIC(20,6) NOT NULL,
    low NUMERIC(20,6) NOT NULL,
    close NUMERIC(20,6) NOT NULL,
    volume BIGINT NOT NULL DEFAULT 0,
    source VARCHAR(128) NOT NULL,
    checksum VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (instrument_id, trading_date),
    CHECK (open > 0 AND high > 0 AND low > 0 AND close > 0),
    CHECK (high >= low AND high >= open AND high >= close AND low <= open AND low <= close),
    CHECK (volume >= 0)
);

CREATE INDEX IF NOT EXISTS idx_eod_prices_date ON eod_prices(trading_date);
CREATE INDEX IF NOT EXISTS idx_eod_prices_instrument_date ON eod_prices(instrument_id, trading_date DESC);
CREATE INDEX IF NOT EXISTS idx_instruments_sector ON instruments(sector);
CREATE INDEX IF NOT EXISTS idx_refresh_sessions_user_id ON refresh_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_sessions_expires_at ON refresh_sessions(expires_at);
"""


def get_connection() -> psycopg.Connection:
    return psycopg.connect(settings.database_url, row_factory=dict_row)


def connection() -> Generator[psycopg.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def initialize_database() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA)
        conn.commit()
