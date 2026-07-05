"""Feature engineering utilities."""
from __future__ import annotations
import pandas as pd
from python.indicators.simple import sma, atr


def create_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create a baseline set of features for modeling.

    Adds: `sma_5`, `sma_20`, `atr_14`, `ret`, `vol_10`.

    Expects DataFrame with `Close`, `High`, `Low` columns.
    """
    out = df.copy()
    out["sma_5"] = sma(out["Close"], 5)
    out["sma_20"] = sma(out["Close"], 20)
    out["atr_14"] = atr(out[["High", "Low", "Close"]], window=14)
    out["ret"] = out["Close"].pct_change().fillna(0)
    out["vol_10"] = out["ret"].rolling(window=10, min_periods=1).std()
    return out
