"use client";

import Link from "next/link";

export default function Compare() {
  return <main className="app-shell"><nav className="nav"><Link className="logo" href="/">Diagnosis<span>_Xpo</span></Link><div className="navlinks"><Link href="/dashboard">Dashboard</Link><Link href="/diagnosis">Diagnosis</Link><Link href="/screener">Screener</Link><Link href="/sectors">Sectors</Link></div></nav><section className="page-head"><div><div className="eyebrow">Quant comparison</div><h1>Compare up to 10 stocks.</h1><p className="lead">Side-by-side evidence for trend, momentum, volatility, volume and score. Select stocks after the instrument database is populated.</p></div></section><section className="panel compare-panel"><div className="compare-input"><input placeholder="Add NSE/BSE symbols e.g. RELIANCE, TCS, INFY"/><button className="cta">Add</button></div><div className="empty-state"><strong>No instruments selected</strong><p>The comparison engine is ready for real normalized market data.</p></div></section></main>;
}
