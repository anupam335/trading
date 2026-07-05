from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass
class BacktestResult:
    initial_capital: float
    ending_capital: float
    total_return: float
    net_profit: float
    win_rate: float
    max_drawdown: float
    profit_factor: float
    num_trades: int
    equity_curve: pd.Series


class Backtester:
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = float(initial_capital)

    def run(self, df: pd.DataFrame, entry_signals: pd.Series, exit_signals: pd.Series) -> BacktestResult:
        df = df.copy()
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain Close prices")

        entry_signals = entry_signals.fillna(False).astype(bool)
        exit_signals = exit_signals.fillna(False).astype(bool)

        cash = self.initial_capital
        position = 0.0
        entry_price = 0.0
        trades = []
        equity = []

        for i, price in enumerate(df["Close"]):
            if position == 0.0 and entry_signals.iloc[i]:
                position = cash / price
                entry_price = price
            elif position > 0.0 and exit_signals.iloc[i]:
                pnl = (price - entry_price) * position
                cash += pnl
                trades.append(pnl)
                position = 0.0
                entry_price = 0.0

            equity.append(cash + position * price)

        # Liquidate last open position if needed
        if position > 0.0:
            price = df["Close"].iloc[-1]
            pnl = (price - entry_price) * position
            cash += pnl
            trades.append(pnl)
            equity[-1] = cash

        equity_curve = pd.Series(equity, index=df.index)
        total_return = equity_curve.iloc[-1] / self.initial_capital - 1.0
        net_profit = equity_curve.iloc[-1] - self.initial_capital

        wins = [p for p in trades if p > 0]
        losses = [p for p in trades if p < 0]
        win_rate = len(wins) / len(trades) if trades else 0.0
        profit_factor = sum(wins) / abs(sum(losses)) if losses else float("inf") if wins else 0.0

        peak = equity_curve.cummax()
        drawdown = (peak - equity_curve) / peak
        max_drawdown = float(drawdown.max()) if not drawdown.empty else 0.0

        return BacktestResult(
            initial_capital=self.initial_capital,
            ending_capital=float(equity_curve.iloc[-1]),
            total_return=float(total_return),
            net_profit=float(net_profit),
            win_rate=float(win_rate),
            max_drawdown=max_drawdown,
            profit_factor=float(profit_factor),
            num_trades=len(trades),
            equity_curve=equity_curve,
        )
