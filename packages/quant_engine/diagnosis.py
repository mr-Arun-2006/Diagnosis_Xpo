from __future__ import annotations

import pandas as pd

from .indicators import calculate_indicators


def _last(frame: pd.DataFrame, column: str) -> float | None:
    value = frame[column].iloc[-1]
    return None if pd.isna(value) else float(value)


def _levels(x: pd.DataFrame) -> dict[str, float | None]:
    close = _last(x, "close")
    if close is None:
        return {"support": None, "resistance": None, "pivot": None}
    high20 = _last(x, "donchian_high_20")
    low20 = _last(x, "donchian_low_20")
    return {
        "support": low20,
        "resistance": high20,
        "pivot": round((high20 + low20 + close) / 3, 4) if high20 is not None and low20 is not None else None,
    }


def _patterns(x: pd.DataFrame) -> list[str]:
    if len(x) < 2:
        return []
    a, b = x.iloc[-2], x.iloc[-1]
    patterns: list[str] = []
    body = abs(b.close - b.open)
    candle_range = max(b.high - b.low, 1e-12)
    if body / candle_range < 0.15:
        patterns.append("indecision_candle")
    if b.close > b.open and a.close < a.open and b.close >= a.open and b.open <= a.close:
        patterns.append("bullish_engulfing")
    if b.close < b.open and a.close > a.open and b.open >= a.close and b.close <= a.open:
        patterns.append("bearish_engulfing")
    if b.high >= x["donchian_high_20"].iloc[-2]:
        patterns.append("20_period_high_test")
    if b.low <= x["donchian_low_20"].iloc[-2]:
        patterns.append("20_period_low_test")
    return patterns


def diagnose(frame: pd.DataFrame) -> dict:
    """Create deterministic evidence from OHLCV; AI consumes this result only."""
    if len(frame) < 60:
        raise ValueError("At least 60 OHLCV rows are required for diagnosis")
    x = calculate_indicators(frame)
    last = x.iloc[-1]
    score = 50.0
    evidence: list[str] = []

    checks = [
        (last.close > last.ema_20, 8, "Price is above EMA20"),
        (last.ema_20 > last.ema_50, 8, "EMA20 is above EMA50"),
        (last.rsi_14 >= 55, 6, "RSI momentum is positive"),
        (last.rsi_14 <= 45, -6, "RSI momentum is weak"),
        (last.macd_hist > 0, 7, "MACD histogram is positive"),
        (last.adx_14 >= 20, 5, "ADX indicates a meaningful trend"),
        (last.plus_di > last.minus_di, 5, "Directional movement favors buyers"),
        (last.close > last.vwap, 4, "Price is above VWAP proxy"),
        (last.relative_volume_20 >= 1.25, 4, "Volume is above its 20-period average"),
        (last.close > last.bb_mid, 3, "Price is above the Bollinger midpoint"),
        (last.aroon_up_25 > last.aroon_down_25, 3, "Aroon structure favors an uptrend"),
    ]
    for condition, weight, text in checks:
        if bool(condition):
            score += weight
            if weight > 0:
                evidence.append(text)
        elif weight > 0:
            score -= weight

    score = max(0.0, min(100.0, score))
    regime = "bullish" if score >= 68 else "bearish" if score <= 32 else "sideways"
    atr_pct = _last(x, "natr_14")
    risk = "high" if atr_pct is not None and atr_pct >= 4 else "moderate" if atr_pct is not None and atr_pct >= 2 else "low"
    confidence = round(min(0.99, 0.50 + abs(score - 50) / 100), 2)
    patterns = _patterns(x)
    levels = _levels(x)
    evidence.extend(f"Pattern detected: {pattern}" for pattern in patterns)

    return {
        "regime": regime,
        "score": round(score, 1),
        "confidence": confidence,
        "risk": risk,
        "latest": {
            "close": _last(x, "close"),
            "rsi_14": _last(x, "rsi_14"),
            "atr_14": _last(x, "atr_14"),
            "natr_14": atr_pct,
            "adx_14": _last(x, "adx_14"),
            "macd_hist": _last(x, "macd_hist"),
            "relative_volume_20": _last(x, "relative_volume_20"),
            "bb_pct_b": _last(x, "bb_pct_b"),
        },
        "key_levels": levels,
        "patterns": patterns,
        "evidence": evidence,
        "indicator_count": len([c for c in x.columns if c not in frame.columns]),
    }
