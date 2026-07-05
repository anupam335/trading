"""Simple indicator implementations (SMA, ATR)."""
from __future__ import annotations
import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple moving average."""
    return series.rolling(window=window, min_periods=1).mean()


def atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """Average True Range (ATR).

    Expects dataframe with `High`, `Low`, `Close` columns.
    """
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift(1)).abs()
    low_close = (df["Low"] - df["Close"].shift(1)).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=window, min_periods=1).mean()
