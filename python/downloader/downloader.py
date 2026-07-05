"""Simple downloader using yfinance to fetch historical OHLCV data."""
from __future__ import annotations
import os
from typing import Optional
import pandas as pd


class Downloader:
    def __init__(self, ticker: str, period: str = "1y", interval: str = "1d", out_dir: Optional[str] = None):
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.out_dir = out_dir or os.path.join(os.getcwd(), "data", "raw")
        os.makedirs(self.out_dir, exist_ok=True)

    def fetch(self) -> pd.DataFrame:
        """Fetch historical data and save as CSV to `data/raw/`.

        Returns:
            pd.DataFrame: OHLCV dataframe indexed by datetime.
        """
        try:
            import yfinance as yf
        except Exception as e:
            raise RuntimeError("yfinance is required. Install with `pip install yfinance`") from e

        df = yf.download(self.ticker, period=self.period, interval=self.interval, progress=False)
        if df is None or df.empty:
            raise RuntimeError(f"No data returned for {self.ticker}")

        out_path = os.path.join(self.out_dir, f"{self.ticker.replace(':','_')}_{self.interval}_{self.period}.csv")
        df.to_csv(out_path)
        return df
