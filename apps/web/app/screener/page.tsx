"use client";

import { FormEvent, useState } from "react";

type Row = { symbol: string; exchange: string; sector?: string; price: number; score: number; regime: string; rsi?: number; relative_volume?: number };

export default function ScreenerPage() {
  const [exchange, setExchange] = useState("NSE");
  const [minScore, setMinScore] = useState("60");
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function scan(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError("");
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const response = await fetch(`${base}/screener/scan`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ exchange, min_score: Number(minScore), limit: 50 }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || "Screener request failed");
      setRows(body.rows || []);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to run screener"); setRows([]); }
    finally { setLoading(false); }
  }

  return <main className="app-shell"><nav className="nav"><a className="logo" href="/">Diagnosis<span>_Xpo</span></a><div className="navlinks"><a href="/dashboard">Dashboard</a><a href="/diagnosis">Diagnosis</a><a href="/compare">Compare</a><a href="/sectors">Sectors</a></div></nav><section className="page-head"><div><div className="eyebrow">Quantitative stock scanner</div><h1>Find stocks by evidence.</h1><p className="lead">Results are ranked by the same deterministic diagnosis engine used by Stock Diagnosis.</p></div></section><section className="panel"><form className="compare-input" onSubmit={scan}><select value={exchange} onChange={e => setExchange(e.target.value)}><option>NSE</option><option>BSE</option></select><input type="number" min="0" max="100" value={minScore} onChange={e => setMinScore(e.target.value)} placeholder="Minimum score"/><button className="cta" disabled={loading}>{loading ? "Scanning…" : "Run screener"}</button></form>{error && <p className="error">{error}</p>}<div style={{overflowX:"auto",marginTop:18}}><table style={{width:"100%",borderCollapse:"collapse"}}><thead><tr>{["Symbol","Sector","Price","Score","Regime","RSI","Rel. Vol."].map(h => <th key={h} style={{textAlign:"left",padding:12}}>{h}</th>)}</tr></thead><tbody>{rows.map(row => <tr key={`${row.exchange}-${row.symbol}`}>{<><td style={{padding:12,fontWeight:700}}>{row.symbol}</td><td style={{padding:12}}>{row.sector || "—"}</td><td style={{padding:12}}>{row.price.toFixed(2)}</td><td style={{padding:12}}>{row.score.toFixed(1)}</td><td style={{padding:12}}>{row.regime}</td><td style={{padding:12}}>{row.rsi?.toFixed(1) ?? "—"}</td><td style={{padding:12}}>{row.relative_volume?.toFixed(2) ?? "—"}</td></>}</tr>)}{!rows.length && <tr><td colSpan={7} style={{padding:24,textAlign:"center"}}>Run the screener after validated EOD data is available.</td></tr>}</tbody></table></div></section></main>;
}
