from __future__ import annotations
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def atr(frame: pd.DataFrame, period: int = 14) -> pd.Series:
    prev_close = frame["close"].shift(1)
    tr = pd.concat([
        frame["high"] - frame["low"],
        (frame["high"] - prev_close).abs(),
        (frame["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def diagnosis(frame: pd.DataFrame) -> dict:
    if frame.empty:
        return {"regime": "unknown", "score": 0, "confidence": 0}
    close = frame["close"]
    last = close.iloc[-1]
    e20, e50 = ema(close, 20).iloc[-1], ema(close, 50).iloc[-1]
    r = rsi(close).iloc[-1]
    score = 50
    score += 15 if last > e20 else -15
    score += 15 if e20 > e50 else -15
    score += 10 if r >= 55 else (-10 if r <= 45 else 0)
    score = max(0, min(100, int(score)))
    regime = "bullish" if score >= 65 else "bearish" if score <= 35 else "sideways"
    confidence = round(abs(score - 50) / 50, 2)
    return {"regime": regime, "score": score, "confidence": confidence, "rsi": float(r) if pd.notna(r) else None}
