"use client";

import Link from "next/link";

export default function FOChain() {
  return <main className="app-shell"><nav className="nav"><Link className="logo" href="/">Diagnosis<span>_Xpo</span></Link><div className="navlinks"><Link href="/dashboard">Dashboard</Link><Link href="/diagnosis">Diagnosis</Link><Link href="/screener">Screener</Link><Link href="/sectors">Sectors</Link></div></nav><section className="page-head"><div><div className="eyebrow">F&O Intelligence</div><h1>Option chain.</h1><p className="lead">CE and PE strikes, OI, change in OI, volume, IV and analytics will be streamed from the configured F&O provider.</p></div><div className="status-pill"><span className="status-dot"/> Provider not configured</div></section><section className="panel"><div className="panel-head"><h2>Option chain</h2><span>ATM centered</span></div><div className="chain-head"><span>CALLS</span><span>STRIKE</span><span>PUTS</span></div><div className="empty-state"><strong>Waiting for F&O provider</strong><p>Configure FO_PROVIDER and FO_API_KEY in the environment. The UI will not display fabricated option-chain values.</p></div></section></main>;
}
