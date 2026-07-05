import os
import pandas as pd
from pathlib import Path
from python.main import run_backtest, run_optimizer
from python.downloader.downloader import Downloader


def make_sample_data() -> pd.DataFrame:
    index = pd.date_range("2023-01-01", periods=6, freq="D")
    return pd.DataFrame(
        {
            "Open": [100, 101, 102, 103, 104, 105],
            "High": [101, 102, 103, 104, 105, 106],
            "Low": [99, 100, 101, 102, 103, 104],
            "Close": [100, 101, 102, 101, 103, 104],
            "Volume": [1000, 1100, 900, 1200, 1300, 1400],
        },
        index=index,
    )


class DummyDownloader(Downloader):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def fetch(self) -> pd.DataFrame:
        return self._data.copy()


def test_run_backtest_exports_reports(monkeypatch, tmp_path: Path):
    df = make_sample_data()
    monkeypatch.setattr("python.main.Downloader", lambda *args, **kwargs: DummyDownloader(df))

    report_dir = tmp_path / "reports"
    result = run_backtest("TEST", "1y", "1d", None, str(report_dir), 10000.0)

    assert result.ending_capital >= result.initial_capital
    assert (report_dir / "backtest_summary_TEST.csv").exists()
    assert (report_dir / "equity_curve_TEST.csv").exists()


def test_run_optimizer_exports_history(monkeypatch, tmp_path: Path):
    df = make_sample_data()
    monkeypatch.setattr("python.main.Downloader", lambda *args, **kwargs: DummyDownloader(df))

    report_dir = tmp_path / "reports"
    result = run_optimizer("TEST", "1y", "1d", None, str(report_dir), 10000.0)

    assert result.best_params
    assert (report_dir / "optimization_history_TEST.csv").exists()
    assert result.history.shape[0] > 0
