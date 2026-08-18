import type { Metadata } from "next";
import "./globals.css";
import { MarketCursor } from "./components/market-cursor";

export const metadata: Metadata = {
  title: "Diagnosis Xpo | Indian Market Intelligence",
  description: "Evidence-first EOD, live market intelligence, quantitative diagnosis and AI explanations for NSE and BSE."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><MarketCursor />{children}</body></html>;
}
