# Product Flow

## User journey

```text
Landing
  ↓
Login/Register
  ↓
Select role + language
  ↓
Dashboard
  ├─ Market overview
  ├─ NIFTY / SENSEX / VIX
  ├─ Market score / regime
  └─ Sector strength

Dashboard → Diagnosis → Quant evidence → AI explanation
Dashboard → Screener → filters → ranked universe → Diagnosis
Dashboard → Compare → up to 10 symbols → normalized metrics
Dashboard → Sectors → sector heatmap → candle/detail view
Dashboard → NSE vs BSE → exchange-specific universe
Dashboard → F&O Chain → provider API → CE/PE chain
Dashboard → Games → learning engine → 100+ questions
Dashboard → Settings → language/theme/exchange/notifications
Dashboard → Admin → RBAC-protected user/system controls
```

## Route map

| Route | Backend dependency | Primary purpose |
|---|---|---|
| `/` | none + optional market snapshot | 3D landing, ticker, education |
| `/login` | `/auth/*` | authentication and preferences |
| `/dashboard` | `/dashboard/summary` | market overview |
| `/diagnosis` | `/diagnosis/{symbol}` + `/ai/explain` | full stock diagnosis |
| `/compare` | diagnosis/market APIs | side-by-side comparison |
| `/sectors` | market + diagnosis APIs | sector heatmap and analysis |
| `/nse-vs-bse` | instruments + market APIs | exchange comparison |
| `/screener` | `/screener/scan` | quantitative live/EOD screening |
| `/fo-chain` | configured F&O provider | option-chain visualization |
| `/games` | question-bank API | financial education |
| `/settings` | `/auth/me` + user settings | preferences |
| `/admin` | RBAC admin APIs | user/system management |

## Diagnosis flow

```text
Symbol + exchange
       ↓
Validated PostgreSQL EOD history
       ↓
Pandas analytical frame
       ↓
50+ indicators
       ↓
Trend / momentum / volatility / volume
       ↓
Regime + patterns + key levels
       ↓
Score + confidence + risk
       ↓
Evidence object
       ↓
AI explanation in selected language
```

## Screener flow

```text
Exchange / sector / score / RSI / volume / regime filters
                         ↓
              latest row per symbol
                         ↓
                 history retrieval
                         ↓
                quantitative diagnosis
                         ↓
                 filter + rank + limit
                         ↓
                    results table
```

## Sector flow

```text
12 NSE sector universe
       ↓
sector aggregate return / breadth / volume
       ↓
heatmap
       ↓ touch / click
sector detail
       ↓
representative candles + explanation + strongest/weakest stocks
```

## F&O flow

```text
Browser
  ↓ authenticated API
F&O provider adapter
  ↓
normalization
  ↓
CE/PE strikes + OI + volume + IV + Greeks when supplied
  ↓
chain visualization
```

Provider keys are environment-only. The browser never receives provider credentials.

## Games flow

1. Quiz — fundamentals and market concepts.
2. Pattern — identify price patterns.
3. Ticker — recognize symbols/exchange data.
4. Regime — classify bullish/bearish/sideways evidence.
5. Portfolio — allocation/risk-learning simulation.
6. Predict — scenario-based reasoning with no real-money execution.

Question bank target: **100+ reviewed questions**, each with answer, explanation, difficulty, topic and language variants.
