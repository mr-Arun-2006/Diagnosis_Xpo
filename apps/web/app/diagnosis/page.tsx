"use client";

import type { FormEvent } from "react";
import { useState } from "react";

export default function DiagnosisPage() {
  const [symbol, setSymbol] = useState("RELIANCE");
  const [exchange, setExchange] = useState("NSE");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setData(null);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const response = await fetch(
        `${base}/diagnosis/${encodeURIComponent(symbol.trim().toUpperCase())}?exchange=${exchange}`,
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || "Diagnosis request failed");
      setData(body);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load diagnosis");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <nav className="nav">
        <a className="logo" href="/">Diagnosis<span>_Xpo</span></a>
        <div className="navlinks">
          <a href="/dashboard">Dashboard</a>
          <a href="/screener">Screener</a>
          <a href="/compare">Compare</a>
          <a href="/sectors">Sectors</a>
        </div>
      </nav>
      <section className="page-head">
        <div>
          <div className="eyebrow">Evidence-first quantitative diagnosis</div>
          <h1>Understand what is happening in a stock.</h1>
          <p className="lead">The engine uses stored EOD history and calculated indicators. AI explanations will consume this evidence rather than invent market numbers.</p>
        </div>
      </section>
      <section className="panel">
        <form className="compare-input" onSubmit={submit}>
          <input value={symbol} onChange={(e) => setSymbol(e.target.value)} placeholder="Symbol" />
          <select value={exchange} onChange={(e) => setExchange(e.target.value)}>
            <option>NSE</option>
            <option>BSE</option>
          </select>
          <button className="cta" disabled={loading}>{loading ? "Analysing…" : "Diagnose"}</button>
        </form>
        {error && <p className="error">{error}</p>}
        {data && (
          <div className="grid" style={{ padding: "18px 0 0" }}>
            <div className="card"><small>Regime</small><div className="score">{data.regime}</div></div>
            <div className="card"><small>Quant score</small><div className="score">{data.score}</div></div>
            <div className="card"><small>Confidence</small><div className="score">{Math.round((data.confidence || 0) * 100)}%</div></div>
            <div className="card"><small>Risk</small><div className="score">{data.risk}</div></div>
          </div>
        )}
        {data?.latest && (
          <div className="panel" style={{ marginTop: 18 }}>
            <h3>Latest evidence</h3>
            <p>Close: {data.latest.close ?? "—"} · RSI: {data.latest.rsi_14 ?? "—"} · ADX: {data.latest.adx_14 ?? "—"} · Relative volume: {data.latest.relative_volume_20 ?? "—"}</p>
          </div>
        )}
        {data?.evidence?.length > 0 && (
          <div className="panel" style={{ marginTop: 18 }}>
            <h3>Why the score moved</h3>
            <ul>{data.evidence.map((item: string) => <li key={item}>{item}</li>)}</ul>
          </div>
        )}
      </section>
    </main>
  );
}
