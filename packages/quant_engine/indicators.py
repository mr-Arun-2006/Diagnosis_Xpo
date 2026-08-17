from __future__ import annotations

import numpy as np
import pandas as pd


def _sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()


def _ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def _wma(s: pd.Series, n: int) -> pd.Series:
    weights = np.arange(1, n + 1, dtype=float)
    return s.rolling(n, min_periods=n).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)


def _rsi(close: pd.Series, n: int = 14) -> pd.Series:
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    rs = up.ewm(alpha=1 / n, adjust=False, min_periods=n).mean() / down.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + rs)


def _true_range(df: pd.DataFrame) -> pd.Series:
    prev = df.close.shift(1)
    return pd.concat([(df.high - df.low), (df.high - prev).abs(), (df.low - prev).abs()], axis=1).max(axis=1)


def _atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    return _true_range(df).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def calculate_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate a broad, dependency-light technical feature set.

    Required columns: open, high, low, close, volume. The returned frame keeps
    the original columns and adds 60+ named features. Missing early windows
    remain NaN rather than being fabricated.
    """
    required = {"open", "high", "low", "close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing OHLCV columns: {sorted(missing)}")
    df = frame.copy().astype(float)
    c, h, l, v = df.close, df.high, df.low, df.volume

    for n in (5, 10, 20, 50, 100, 200):
        df[f"sma_{n}"] = _sma(c, n)
        df[f"ema_{n}"] = _ema(c, n)
    df["wma_20"] = _wma(c, 20)
    half = max(2, int(np.sqrt(20)))
    df["hma_20"] = 2 * _wma(c, 10) - _wma(c, 20)
    df["hma_20"] = _wma(df["hma_20"], half)

    df["rsi_14"] = _rsi(c, 14)
    low14, high14 = l.rolling(14).min(), h.rolling(14).max()
    stoch_k = 100 * (c - low14) / (high14 - low14).replace(0, np.nan)
    df["stoch_k"] = stoch_k
    df["stoch_d"] = stoch_k.rolling(3).mean()
    df["williams_r"] = -100 * (high14 - c) / (high14 - low14).replace(0, np.nan)
    df["roc_12"] = c.pct_change(12) * 100
    df["momentum_10"] = c.diff(10)
    tp = (h + l + c) / 3
    mean_tp = tp.rolling(20).mean()
    df["cci_20"] = (tp - mean_tp) / (0.015 * tp.rolling(20).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)).replace(0, np.nan)

    ema12, ema26 = _ema(c, 12), _ema(c, 26)
    df["macd"] = ema12 - ema26
    df["macd_signal"] = _ema(df["macd"], 9)
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    df["ppo"] = 100 * (ema12 - ema26) / ema26.replace(0, np.nan)
    df["ppo_signal"] = _ema(df["ppo"], 9)

    tr = _true_range(df)
    atr14 = _atr(df, 14)
    df["tr"] = tr
    df["atr_14"] = atr14
    df["natr_14"] = 100 * atr14 / c.replace(0, np.nan)
    up_move, down_move = h.diff(), -l.diff()
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)
    atr_safe = atr14.replace(0, np.nan)
    df["plus_di"] = 100 * plus_dm.ewm(alpha=1 / 14, adjust=False).mean() / atr_safe
    df["minus_di"] = 100 * minus_dm.ewm(alpha=1 / 14, adjust=False).mean() / atr_safe
    dx = 100 * (df["plus_di"] - df["minus_di"]).abs() / (df["plus_di"] + df["minus_di"]).replace(0, np.nan)
    df["adx_14"] = dx.ewm(alpha=1 / 14, adjust=False).mean()

    mid = _sma(c, 20)
    std = c.rolling(20).std()
    df["bb_mid"] = mid
    df["bb_upper"] = mid + 2 * std
    df["bb_lower"] = mid - 2 * std
    df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / mid.replace(0, np.nan)
    df["bb_pct_b"] = (c - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"]).replace(0, np.nan)
    df["keltner_mid"] = _ema(c, 20)
    df["keltner_upper"] = df["keltner_mid"] + 2 * atr14
    df["keltner_lower"] = df["keltner_mid"] - 2 * atr14
    df["donchian_high_20"] = h.rolling(20).max()
    df["donchian_low_20"] = l.rolling(20).min()
    df["donchian_mid_20"] = (df["donchian_high_20"] + df["donchian_low_20"]) / 2

    direction = np.sign(c.diff()).fillna(0)
    df["obv"] = (direction * v).cumsum()
    mf_multiplier = ((c - l) - (h - c)) / (h - l).replace(0, np.nan)
    df["adl"] = (mf_multiplier.fillna(0) * v).cumsum()
    df["mfi_14"] = 100 - 100 / (1 + ((tp * v).where(tp.diff() > 0, 0).rolling(14).sum() / (tp * v).where(tp.diff() < 0, 0).abs().rolling(14).sum()).replace(0, np.nan))
    df["cmf_20"] = (mf_multiplier.fillna(0) * v).rolling(20).sum() / v.rolling(20).sum().replace(0, np.nan)
    df["vwap"] = (tp * v).cumsum() / v.cumsum().replace(0, np.nan)
    df["relative_volume_20"] = v / v.rolling(20).mean().replace(0, np.nan)
    df["volume_zscore_20"] = (v - v.rolling(20).mean()) / v.rolling(20).std().replace(0, np.nan)

    ret = c.pct_change()
    df["volatility_20"] = ret.rolling(20).std() * np.sqrt(252)
    df["zscore_20"] = (c - mid) / std.replace(0, np.nan)
    df["trix_15"] = _ema(_ema(_ema(c, 15), 15), 15).pct_change() * 100
    df["dpo_20"] = c.shift(11) - _sma(c, 20)
    pc = c.diff()
    abs_pc = pc.abs()
    df["tsi"] = 100 * _ema(_ema(pc, 25), 13) / _ema(_ema(abs_pc, 25), 13).replace(0, np.nan)
    df["chande_momentum_14"] = 100 * pc.clip(lower=0).rolling(14).sum() / pc.abs().rolling(14).sum().replace(0, np.nan) - 50
    df["force_index_13"] = (c.diff() * v).ewm(span=13, adjust=False).mean()

    # Aroon
    def _aroon_up(x: np.ndarray) -> float:
        return 100 * (len(x) - 1 - int(np.argmax(x))) / (len(x) - 1)
    def _aroon_down(x: np.ndarray) -> float:
        return 100 * (len(x) - 1 - int(np.argmin(x))) / (len(x) - 1)
    df["aroon_up_25"] = h.rolling(25).apply(_aroon_up, raw=True)
    df["aroon_down_25"] = l.rolling(25).apply(_aroon_down, raw=True)

    # Vortex, Ultimate Oscillator, Ease of Movement, Mass Index and Elder Ray
    vm = (h - l.shift(1)).abs() - (l - h.shift(1)).abs()
    df["vortex_pos_14"] = (h - l.shift(1)).abs().rolling(14).sum() / tr.rolling(14).sum().replace(0, np.nan)
    df["vortex_neg_14"] = (l - h.shift(1)).abs().rolling(14).sum() / tr.rolling(14).sum().replace(0, np.nan)
    bp = c - pd.concat([c.shift(1), l], axis=1).min(axis=1)
    tr7 = pd.concat([h, c.shift(1)], axis=1).max(axis=1) - pd.concat([l, c.shift(1)], axis=1).min(axis=1)
    df["ultimate_oscillator"] = 100 * (4 * bp.rolling(7).sum() / tr7.rolling(7).sum() + 2 * bp.rolling(14).sum() / tr7.rolling(14).sum() + bp.rolling(28).sum() / tr7.rolling(28).sum()) / 7
    midpoint = (h + l) / 2
    df["ease_of_movement_14"] = ((h.diff() + l.diff()) / 2) / (v / (h - l).replace(0, np.nan))
    df["ease_of_movement_14"] = df["ease_of_movement_14"].rolling(14).mean()
    df["elder_bull_power"] = h - _ema(c, 13)
    df["elder_bear_power"] = l - _ema(c, 13)
    hl_range = h - l
    df["mass_index"] = hl_range.ewm(span=9, adjust=False).mean().div(hl_range.ewm(span=9, adjust=False).mean().ewm(span=9, adjust=False).mean()).rolling(25).sum()

    return df


INDICATOR_NAMES = [
    c for c in calculate_indicators(pd.DataFrame({"open":[1.0]*200,"high":[1.1]*200,"low":[0.9]*200,"close":[1.0]*200,"volume":[1000.0]*200})).columns
    if c not in {"open", "high", "low", "close", "volume"}
]
