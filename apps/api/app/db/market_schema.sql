CREATE TABLE IF NOT EXISTS instruments (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(64) NOT NULL,
    exchange VARCHAR(8) NOT NULL CHECK (exchange IN ('NSE','BSE')),
    company_name TEXT NOT NULL,
    sector TEXT,
    industry TEXT,
    isin VARCHAR(32),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (exchange, symbol)
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
    source VARCHAR(64) NOT NULL,
    checksum VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (instrument_id, trading_date),
    CHECK (open > 0 AND high > 0 AND low > 0 AND close > 0),
    CHECK (high >= low AND high >= open AND high >= close AND low <= open AND low <= close),
    CHECK (volume >= 0)
);

CREATE INDEX IF NOT EXISTS idx_eod_prices_date ON eod_prices(trading_date);
CREATE INDEX IF NOT EXISTS idx_instruments_sector ON instruments(sector);
