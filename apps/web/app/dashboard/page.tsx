import Link from "next/link";

const cards = [
  ["NIFTY 50", "—", "Awaiting live/EOD provider"],
  ["SENSEX", "—", "Awaiting live/EOD provider"],
  ["INDIA VIX", "—", "Awaiting live/EOD provider"],
  ["MARKET SCORE", "—", "Calculated after validated data"]
];

export default function Dashboard() {
  return <main className="shell"><nav className="nav"><div className="logo">Diagnosis<span>_Xpo</span></div><div className="navlinks"><Link href="/">Home</Link><Link href="/diagnosis">Diagnosis</Link><Link href="/screener">Screener</Link><Link href="/sectors">Sectors</Link></div></nav><section className="section" style={{paddingTop:50}}><div className="eyebrow">Market Dashboard</div><h1 style={{fontSize:52}}>Today in the market.</h1><p className="lead">The dashboard will combine validated NSE/BSE EOD data with configurable live feeds. No provider is hard-coded into the UI.</p><div className="grid" style={{padding:"20px 0"}}>{cards.map(([a,b,c])=><div className="card" key={a}><small>{a}</small><div className="score">{b}</div><small>{c}</small></div>)}</div><div className="card"><h2>Market narrative</h2><p className="lead">Data ingestion is not configured yet. Once a provider is added to the environment, the pipeline will validate the source, calculate market breadth/regime metrics and publish the evidence here.</p></div></section></main>;
}
