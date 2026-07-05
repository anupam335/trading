from __future__ import annotations
import pandas as pd
from python.backtesting.backtester import BacktestResult


def backtest_summary(result: BacktestResult) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "initial_capital": result.initial_capital,
            "ending_capital": result.ending_capital,
            "total_return": result.total_return,
            "net_profit": result.net_profit,
            "win_rate": result.win_rate,
            "max_drawdown": result.max_drawdown,
            "profit_factor": result.profit_factor,
            "num_trades": result.num_trades,
        }
    ])


def export_summary_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)


def export_equity_curve(result: BacktestResult, path: str) -> None:
    result.equity_curve.to_csv(path, header=["equity"] )
