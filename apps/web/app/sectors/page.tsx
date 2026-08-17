"use client";

import Link from "next/link";

const sectors = ["Financial Services", "Information Technology", "Oil & Gas", "Automobile", "Pharmaceuticals", "Metals", "FMCG", "Telecom", "Consumer Durables", "Realty", "Power", "Healthcare"];

export default function Sectors() {
  return <main className="app-shell"><nav className="nav"><Link className="logo" href="/">Diagnosis<span>_Xpo</span></Link><div className="navlinks"><Link href="/dashboard">Dashboard</Link><Link href="/diagnosis">Diagnosis</Link><Link href="/compare">Compare</Link><Link href="/screener">Screener</Link></div></nav><section className="page-head"><div><div className="eyebrow">Sector intelligence</div><h1>Where is the market moving?</h1><p className="lead">The sector heatmap will combine breadth, relative strength, momentum and volatility. Touch a sector to reveal its candle visualization and explanation.</p></div></section><section className="sector-grid">{sectors.map((sector,i)=><article className="sector-card" key={sector}><div className="sector-top"><span>{sector}</span><span className="muted">12 sectors</span></div><div className="sector-candle"><span style={{height:`${35 + (i%5)*10}px`}}/><span style={{height:`${55 + (i%4)*12}px`}}/><span style={{height:`${28 + (i%6)*9}px`}}/><span style={{height:`${48 + (i%3)*14}px`}}/></div><div className="sector-foot">Awaiting validated data</div></article>)}</section></main>;
}
