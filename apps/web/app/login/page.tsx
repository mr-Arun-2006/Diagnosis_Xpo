"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Mode = "login" | "register";

export default function Login() {
  const router = useRouter();
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [language, setLanguage] = useState("en");
  const [exchange, setExchange] = useState("NSE");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");

    try {
      const endpoint = mode === "login" ? "/api/v1/auth/login" : "/api/v1/auth/register";
      const body = mode === "login"
        ? { email, password }
        : { email, password, role, language, default_exchange: exchange };

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "Authentication failed");

      sessionStorage.setItem("diagnosis_access_token", data.access_token);
      sessionStorage.setItem("diagnosis_refresh_token", data.refresh_token);
      sessionStorage.setItem("diagnosis_user", JSON.stringify(data.user));
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <section className="section" style={{ maxWidth: 560, paddingTop: 80 }}>
        <div className="eyebrow">Secure access</div>
        <h1 style={{ fontSize: 48 }}>{mode === "login" ? "Welcome back." : "Create your account."}</h1>
        <form className="card" onSubmit={submit}>
          <label htmlFor="email">Email</label>
          <input id="email" required value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: "100%", padding: 13, margin: "8px 0 18px", border: "1px solid #dbe7f5", borderRadius: 10 }} type="email" placeholder="you@example.com" />

          <label htmlFor="password">Password</label>
          <input id="password" required minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: "100%", padding: 13, margin: "8px 0 18px", border: "1px solid #dbe7f5", borderRadius: 10 }} type="password" placeholder="At least 8 characters" />

          {mode === "register" && (
            <>
              <label htmlFor="role">Role</label>
              <select id="role" value={role} onChange={(e) => setRole(e.target.value)} style={{ width: "100%", padding: 13, margin: "8px 0 18px", border: "1px solid #dbe7f5", borderRadius: 10 }}>
                <option value="user">Beginner</option>
                <option value="trader">Trader</option>
                <option value="researcher">Researcher</option>
              </select>

              <label htmlFor="language">Language</label>
              <select id="language" value={language} onChange={(e) => setLanguage(e.target.value)} style={{ width: "100%", padding: 13, margin: "8px 0 18px", border: "1px solid #dbe7f5", borderRadius: 10 }}>
                <option value="en">English</option>
                <option value="ta">Tamil</option>
                <option value="hi">Hindi</option>
                <option value="gu">Gujarati</option>
              </select>

              <label htmlFor="exchange">Default exchange</label>
              <select id="exchange" value={exchange} onChange={(e) => setExchange(e.target.value)} style={{ width: "100%", padding: 13, margin: "8px 0 22px", border: "1px solid #dbe7f5", borderRadius: 10 }}>
                <option value="NSE">NSE</option>
                <option value="BSE">BSE</option>
              </select>
            </>
          )}

          {error && <p role="alert" style={{ color: "#b42318", marginBottom: 16 }}>{error}</p>}
          <button className="cta" style={{ width: "100%" }} disabled={busy} type="submit">
            {busy ? "Connecting…" : mode === "login" ? "Sign in" : "Register"}
          </button>
        </form>
        <button className="secondary" style={{ marginTop: 14 }} onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}>
          {mode === "login" ? "Need an account? Register" : "Already registered? Sign in"}
        </button>
      </section>
    </main>
  );
}
