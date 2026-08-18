# Diagnosis_Xpo Architecture

## 1. System boundary

```text
                         ┌──────────────────────────────┐
                         │          Web / Mobile        │
                         │ Next.js + blue/white design │
                         └──────────────┬───────────────┘
                                        │ HTTPS
                         ┌──────────────▼───────────────┐
                         │          FastAPI API         │
                         │ auth · market · analytics    │
                         └───────┬─────────┬─────────────┘
                                 │         │
                    ┌────────────▼───┐ ┌──▼────────────────┐
                    │ PostgreSQL     │ │ Redis              │
                    │ users + EOD    │ │ cache + jobs       │
                    └───────┬────────┘ └────────┬──────────┘
                            │                   │
                 ┌──────────▼──────────┐ ┌──────▼───────────┐
                 │ Quant Engine        │ │ AI Engine         │
                 │ deterministic       │ │ evidence-grounded │
                 └──────────▲──────────┘ └────────▲─────────┘
                            │                     │
                 ┌──────────┴─────────────────────┴──────┐
                 │              Data Plane                │
                 │ official NSE/BSE + provider fallback │
                 └───────────────────────────────────────┘
```

## 2. Repository structure

```text
Diagnosis_Xpo/
├── apps/
│   ├── api/                 # FastAPI application
│   └── web/                 # Next.js application
├── packages/
│   ├── contracts/           # canonical cross-layer data contracts
│   ├── market-data/         # provider adapters and validation
│   ├── data_pipeline/       # ingestion orchestration
│   ├── quant_engine/        # indicators, regime, score, diagnosis
│   └── ai_engine/           # evidence packaging and LLM boundary
├── docs/                    # build/run/product documentation
├── .github/workflows/       # CI
├── docker-compose.yml
└── .env.example
```

Python package directories use underscores. Provider-specific implementation must never leak into API or UI code.

## 3. EOD data flow

```text
Source selection
   ↓
Official NSE/BSE EOD source
   ↓ if unavailable/explicitly configured
Provider fallback
   ↓
Raw archive
   ↓
Parse
   ↓
Schema + trading-date + symbol + OHLCV validation
   ↓
Deduplicate / normalize
   ↓
PostgreSQL canonical store
   ↓
Parquet/DuckDB analytical representation
   ↓
Quant features
   ↓
API/cache
```

Official exchange data is preferred. Unofficial sources are adapters/fallbacks and are marked with provenance; they are never silently treated as official.

## 4. Quant flow

```text
OHLCV → trend → momentum → volatility → volume → structure
      → 50+ indicators → regime → patterns → key levels
      → deterministic score/confidence → diagnosis evidence
```

## 5. AI flow

```text
Quant evidence + sector/index/F&O context
                ↓
         typed evidence object
                ↓
       configured LLM provider
                ↓
 explanation + uncertainty + education
                ↓
       EN / TA / HI / GU
```

Numerical truth remains in the database/quant engine.

## 6. Product navigation

```text
Landing /
  ↓
Login / Register
  ↓
Dashboard
  ├── Diagnosis
  ├── Compare
  ├── Sectors
  ├── NSE vs BSE
  ├── Screener
  ├── F&O Chain
  ├── Games
  ├── Settings
  └── Admin (RBAC)
```

## 7. Reliability gates

A stage is complete only when:
- its data contract exists;
- loading, empty and error states exist;
- backend and frontend are connected;
- secrets are environment-only;
- automated tests pass;
- Docker startup is healthy;
- CI is green.
