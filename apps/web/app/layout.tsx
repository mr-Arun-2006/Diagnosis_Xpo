import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Diagnosis Xpo | Indian Market Intelligence",
  description: "EOD, live market intelligence, quantitative diagnosis and AI explanations for NSE and BSE."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
