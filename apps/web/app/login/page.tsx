"use client";

import { useState } from "react";

export default function Login() {
  const [mode, setMode] = useState<"login" | "register">("login");
  return <main className="shell"><section className="section" style={{maxWidth:560,paddingTop:80}}><div className="eyebrow">Secure access</div><h1 style={{fontSize:48}}>{mode === "login" ? "Welcome back." : "Create your account."}</h1><div className="card"><label>Email</label><input style={{width:"100%",padding:13,margin:"8px 0 18px",border:"1px solid #dbe7f5",borderRadius:10}} type="email" placeholder="you@example.com"/><label>Password</label><input style={{width:"100%",padding:13,margin:"8px 0 18px",border:"1px solid #dbe7f5",borderRadius:10}} type="password" placeholder="••••••••"/><label>Role</label><select style={{width:"100%",padding:13,margin:"8px 0 18px",border:"1px solid #dbe7f5",borderRadius:10}}><option>Trader</option><option>Researcher</option><option>Beginner</option></select><label>Language</label><select style={{width:"100%",padding:13,margin:"8px 0 22px",border:"1px solid #dbe7f5",borderRadius:10}}><option>English</option><option>Tamil</option><option>Hindi</option><option>Gujarati</option></select><button className="cta" style={{width:"100%"}}>{mode === "login" ? "Sign in" : "Register"}</button></div><button className="secondary" style={{marginTop:14}} onClick={()=>setMode(mode === "login" ? "register" : "login")}>{mode === "login" ? "Need an account? Register" : "Already registered? Sign in"}</button></section></main>;
}
