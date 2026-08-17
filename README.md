# Diagnosis_Xpo

**Indian Market Intelligence, Quantitative Diagnosis & AI Explanation Platform**

Diagnosis_Xpo is a production-oriented foundation for NSE/BSE market intelligence. It is designed to explain what happened in the market, quantify the evidence, and present the result at beginner, trader, and research levels.

## Product

- Market dashboard: NIFTY, SENSEX, India VIX, breadth, sectors and market score
- Stock Diagnosis: 50+ technical/quantitative features, regime, patterns, key levels and AI explanation
- Comparison: up to 10 instruments with radar/bar analysis
- Sectors: 12-sector heatmap with sector diagnosis and interactive candle view
- NSE vs BSE: exchange-separated instrument view
- Live Screener: signal, sector, market-cap, RSI, score and exchange filters
- F&O Chain: configurable live option-chain provider
- Games: Quiz, Pattern, Ticker, Regime and Predict with 100+ questions planned
- Authentication, roles, preferences and persistent user data
- English, Tamil, Hindi and Gujarati

## Architecture

```text
Next.js / React / TypeScript
          |
       FastAPI
          |
  +-------+--------+----------------+
  |       |        |                |
Postgres Redis   Quant Engine    AI Engine
                  |
          Market Data Adapters
             /           \
        NSE/BSE        Live/F&O
        official       providers
             |
       Raw -> Validate -> Normalize
             |
       Parquet / DuckDB / Postgres
```

## Engineering principles

1. Official NSE/BSE data is preferred for EOD/reference datasets.
2. Live/F&O vendors are isolated behind provider adapters and configured with environment variables.
3. Raw market files are preserved before normalization and validation.
4. Quant calculations are deterministic and performed outside the LLM.
5. AI receives structured evidence and explains it; it does not invent missing market data.
6. PostgreSQL stores application/metadata data; Parquet/DuckDB handle larger analytical datasets; Redis handles cache/realtime workloads.
7. Authentication and authorization are enforced server-side.
8. Every pipeline should expose health, quality and audit information.

## Application routes

`/` · `/login` · `/dashboard` · `/diagnosis` · `/compare` · `/sectors` · `/nse-vs-bse` · `/screener` · `/fo-chain` · `/games` · `/settings` · `/admin`

## UI direction

Blue and white financial-terminal visual system, Space Grotesk typography, restrained motion, precision crosshair interactions on charts, and a richer cursor treatment only on the landing page.

## Status

Foundation initialized. Implementation will proceed incrementally: application shell → database/auth → market-data contracts → EOD pipeline → quant engine → dashboard/diagnosis/screener → live/F&O → AI → games → deployment/testing.
