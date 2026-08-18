# Diagnosis_Xpo — Rebuild Plan

This repository is rebuilt in dependency order. Each stage must be structurally correct and CI-green before the next stage is started.

## Stage 0 — Foundation
- Monorepo boundaries
- Python package naming conventions
- Canonical market-data contracts
- Environment/secrets policy
- CI baseline

## Stage 1 — Data plane
```text
NSE/BSE official EOD CSV/API
        +
Configured unofficial/provider fallback
        ↓
Provider adapter
        ↓
Raw payload archive
        ↓
Parser + validation + deduplication
        ↓
Canonical OHLCV
        ↓
PostgreSQL metadata + EOD store
        ↓
Parquet/DuckDB analytical cache
```

## Stage 2 — Quantitative engine
```text
Canonical OHLCV
      ↓
50+ technical/statistical features
      ↓
Trend / momentum / volatility / volume
      ↓
Regime + pattern + key levels
      ↓
Deterministic score + confidence
```

## Stage 3 — API
FastAPI exposes stable contracts for auth, dashboard, diagnosis, compare, sectors, screener, EOD, instruments and F&O. Provider credentials never reach the browser.

## Stage 4 — AI intelligence
```text
Quant evidence + market context
        ↓
Typed evidence package
        ↓
Configured LLM provider
        ↓
Human-readable explanation
        ↓
English / Tamil / Hindi / Gujarati
```
The LLM explains evidence; it does not calculate or fabricate market data.

## Stage 5 — Web application
```text
Landing → Login → Dashboard
             ↓
Diagnosis / Compare / Sectors / NSE-BSE / Screener / F&O / Games / Settings / Admin
```
Blue + white visual system, distinctive typography, responsive mobile-first layout. Landing gets expressive motion; application pages use a precise fast cursor/crosshair rather than a slow cursor.

## Stage 6 — Reliability
- Unit tests
- API contract tests
- Quant regression tests
- Data-quality tests
- Docker health checks
- CI build
- Deployment smoke tests

## Stage 7 — Product completion
1. Dashboard
2. Diagnosis
3. Screener
4. Compare
5. Sectors
6. NSE vs BSE
7. F&O
8. Authentication/RBAC
9. Games with 100+ question bank
10. AI explanations and four languages
11. Notifications/settings/admin

### Non-negotiable rule
No feature is considered complete until its data source, backend contract, frontend state, error state, loading state, test and deployment path are connected.
