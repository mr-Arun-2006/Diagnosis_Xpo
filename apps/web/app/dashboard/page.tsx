"use client";

import { motion } from "framer-motion";
import Link from "next/link";

const cards = [["NIFTY 50", "Awaiting EOD feed", "—"], ["SENSEX", "Awaiting EOD feed", "—"], ["INDIA VIX", "Awaiting EOD feed", "—"], ["MARKET SCORE", "Evidence engine", "—"]];

export default function Dashboard() {
  return <main className="app-shell">
    <nav className="nav"><Link className="logo" href="/">Diagnosis<span>_Xpo</span></Link><div className="navlinks"><Link href="/dashboard">Dashboard</Link><Link href="/diagnosis">Diagnosis</Link><Link href="/compare">Compare</Link><Link href="/sectors">Sectors</Link><Link href="/screener">Screener</Link><Link href="/fo-chain">F&O</Link></div><Link className="cta" href="/login">Account</Link></nav>
    <section className="page-head"><div><div className="eyebrow">Market Intelligence</div><h1>Today's market cockpit.</h1><p className="lead">A single evidence layer for indices, breadth, sectors, risk and quantitative signals. Live values appear when a provider is configured.</p></div><div className="status-pill"><span className="status-dot"/> Data pipeline: not configured</div></section>
    <section className="metric-grid">{cards.map(([name,status,value],i)=><motion.div key={name} className="metric-card" initial={{opacity:0,y:12}} animate={{opacity:1,y:0}} transition={{delay:i*.06}}><div className="metric-top"><span>{name}</span><span className="muted">NSE</span></div><div className="metric-value">{value}</div><small>{status}</small></motion.div>)}</section>
    <section className="dashboard-grid"><div className="panel"><div className="panel-head"><h2>Market narrative</h2><span>Evidence-first</span></div><div className="empty-state"><strong>Waiting for validated market data</strong><p>Once NSE/BSE EOD or a live provider is configured, this panel will summarize breadth, momentum, volatility and sector leadership without inventing values.</p></div></div><div className="panel"><div className="panel-head"><h2>Quick actions</h2></div><div className="quick-grid"><Link href="/diagnosis">Diagnose a stock</Link><Link href="/screener">Run screener</Link><Link href="/sectors">Explore sectors</Link><Link href="/compare">Compare stocks</Link><Link href="/fo-chain">Open F&O chain</Link><Link href="/games">Learn with games</Link></div></div></section>
  </main>;
}
