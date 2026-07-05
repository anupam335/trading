"""Signal generation helpers for backtesting."""
from __future__ import annotations
import pandas as pd


def generate_signals(
    df: pd.DataFrame,
    fast_len: int = 14,
    slow_len: int = 50,
    rsi_len: int = 14,
    obv_ma_len: int = 20,
    setup_ema_len: int = 20,
    atr_len: int = 14,
    entry_threshold: int = 3,
    exit_threshold: int = 0,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    if "Close" not in df.columns or "High" not in df.columns or "Low" not in df.columns:
        raise ValueError("DataFrame must contain Close, High, and Low columns")

    ema_fast = pd.Series(df["Close"].ewm(span=fast_len, adjust=False).mean(), index=df.index)
    ema_slow = pd.Series(df["Close"].ewm(span=slow_len, adjust=False).mean(), index=df.index)
    trend = ema_fast.gt(ema_slow).astype(int).replace({0: -1})

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=rsi_len, min_periods=1).mean()
    avg_loss = loss.rolling(window=rsi_len, min_periods=1).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-9)
    rsi = 100 - (100 / (1 + rs))
    mom = rsi.gt(60).astype(int).replace({0: -1})
    mom = mom.where(rsi.lt(40), 1).fillna(-1)

    obv = (delta.gt(0).astype(int).replace({0: -1}) * df["Volume"]).cumsum()
    obv_ma = obv.rolling(window=obv_ma_len, min_periods=1).mean()
    vol = obv.gt(obv_ma).astype(int).replace({0: -1})

    setup_ema = pd.Series(df["Close"].ewm(span=setup_ema_len, adjust=False).mean(), index=df.index)
    setup = df["Close"].gt(setup_ema).astype(int).replace({0: -1})

    atr = pd.concat(
        [df["High"] - df["Low"], (df["High"] - df["Close"].shift(1)).abs(), (df["Low"] - df["Close"].shift(1)).abs()],
        axis=1,
    ).max(axis=1)
    atr_val = atr.rolling(window=atr_len, min_periods=1).mean()
    risk = atr_val.lt(atr_val.rolling(window=50, min_periods=1).mean()).astype(int).replace({0: -1})

    confidence = trend + mom + vol + setup + risk
    entry = confidence.ge(entry_threshold)
    exit = confidence.le(exit_threshold)

    return entry, exit, confidence
