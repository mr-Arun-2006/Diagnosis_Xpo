"use client";

import { motion } from "framer-motion";
import Link from "next/link";

const quotes = [
  ["NIFTY 50", "—", "Awaiting feed"],
  ["SENSEX", "—", "Awaiting feed"],
  ["INDIA VIX", "—", "Awaiting feed"],
  ["MARKET SCORE", "—", "EOD pipeline pending"],
];

export default function Home() {
  return (
    <main className="shell">
      <nav className="nav">
        <div className="logo">Diagnosis<span>_Xpo</span></div>
        <div className="navlinks">
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/diagnosis">Diagnosis</Link>
          <Link href="/screener">Screener</Link>
          <Link href="/sectors">Sectors</Link>
        </div>
        <Link className="cta" href="/login">Sign in</Link>
      </nav>

      <section className="hero">
        <div>
          <motion.div className="eyebrow" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>Indian Market Intelligence</motion.div>
          <motion.h1 initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .08 }}>Understand the market.<br /><span style={{color:"#155eef"}}>Not just the price.</span></motion.h1>
          <motion.p className="lead" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .16 }}>A quantitative diagnosis platform for NSE and BSE that turns EOD and live market evidence into clear explanations for beginners, traders and researchers.</motion.p>
          <div className="actions"><Link className="cta" href="/dashboard">Explore dashboard</Link><Link className="secondary" href="/diagnosis">Try diagnosis</Link></div>
        </div>
        <motion.div className="ticker" initial={{ opacity: 0, rotateY: -14, x: 30 }} animate={{ opacity: 1, rotateY: -5, x: 0 }} transition={{ duration: .7 }}>
          <div className="tickerHead"><span>MARKET PULSE</span><span>DATA STATUS</span></div>
          {quotes.map(([name, value, status]) => <div className="quote" key={name}><div><strong>{name}</strong><div><small>{status}</small></div></div><div className="value">{value}</div></div>)}
        </motion.div>
      </section>

      <section className="grid">
        {[["50+", "Quant indicators"],["4", "Languages"],["12", "NSE sectors"],["100+", "Game questions"]].map(([v,l]) => <div className="card" key={l}><small>{l}</small><div className="score">{v}</div></div>)}
      </section>

      <section className="section"><h2>One evidence engine. Three ways to understand it.</h2><div className="grid" style={{padding:"10px 0 0"}}><div className="card"><h3>Beginner</h3><p className="lead">Plain-language market explanations without requiring finance expertise.</p></div><div className="card"><h3>Trader</h3><p className="lead">Signals, momentum, regime, support, resistance and risk context.</p></div><div className="card"><h3>Researcher</h3><p className="lead">Features, relative strength, statistical context and reproducible evidence.</p></div></div></section>
      <footer className="footer">Diagnosis_Xpo · Evidence-first market intelligence · Data providers configured through environment variables.</footer>
    </main>
  );
}
