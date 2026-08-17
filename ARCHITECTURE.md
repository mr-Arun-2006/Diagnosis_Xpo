# Diagnosis_Xpo Architecture

## Runtime

```text
Browser
  -> Next.js web
  -> FastAPI API
       -> PostgreSQL (users, instruments, metadata, diagnoses)
       -> Redis (cache, realtime, task queue)
       -> Quant Engine (deterministic calculations)
       -> AI Engine (evidence-grounded explanation)
       -> Market Data Adapters (NSE/BSE EOD, configurable live/F&O)

Historical analytics:
raw files -> validation -> normalization -> Parquet -> DuckDB/Quant Engine
```

## Data contracts

All providers must map into a common instrument/quote/OHLCV contract. Provider-specific fields remain inside adapters. The frontend never calls a market provider directly.

## Pipeline stages

1. Acquire raw source.
2. Persist raw payload/file.
3. Validate schema, trading date, symbols, duplicates and numeric ranges.
4. Normalize exchange/provider fields.
5. Store canonical data.
6. Compute features and regimes.
7. Publish validated results to APIs/cache.
8. Generate AI explanation from structured evidence.

## AI boundary

The quantitative engine owns calculations. The AI engine receives a typed evidence package containing price, indicators, regime, sector/index context, key levels and confidence. The AI cannot be the source of truth for numerical market values.

## Security

Passwords are hashed; secrets remain in environment configuration; RBAC is enforced in FastAPI; admin routes are protected server-side; market-provider keys are never exposed to the browser.

## UI

Blue/white terminal-inspired design, Space Grotesk, restrained animation, accessible contrast, responsive layouts. Landing page may use an expressive cursor; application pages use precise pointer/crosshair interactions to avoid distraction.
