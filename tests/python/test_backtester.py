import pandas as pd
from python.backtesting.backtester import Backtester


def test_backtester_basic():
    df = pd.DataFrame({
        "Close": [100, 101, 102, 101, 103, 104, 105, 106],
    })
    entries = pd.Series([True, False, False, False, False, False, False, False], index=df.index)
    exits = pd.Series([False, False, False, True, False, False, False, False], index=df.index)

    result = Backtester(initial_capital=1000).run(df, entries, exits)
    assert result.num_trades == 1
    assert result.ending_capital != result.initial_capital
    assert result.equity_curve.iloc[-1] == result.ending_capital
