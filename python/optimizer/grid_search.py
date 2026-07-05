from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from typing import Dict, Sequence
from python.backtesting.backtester import Backtester


@dataclass
class OptimizationResult:
    best_params: Dict[str, int]
    best_metric: float
    history: pd.DataFrame


class GridSearchOptimizer:
    def __init__(self, backtester: Backtester):
        self.backtester = backtester

    def search(self, df: pd.DataFrame, param_grid: Dict[str, Sequence[int]], backtest_fn):
        history = []
        best_metric = float("-inf")
        best_params = {}

        keys = list(param_grid.keys())
        values = list(param_grid.values())

        def recursive_search(index: int, current: Dict[str, int]):
            nonlocal best_metric, best_params
            if index == len(keys):
                metrics = backtest_fn(df, current)
                if metrics.total_return > best_metric:
                    best_metric = metrics.total_return
                    best_params = current.copy()
                history.append({**current, "total_return": metrics.total_return})
                return
            for v in values[index]:
                current[keys[index]] = v
                recursive_search(index + 1, current)

        recursive_search(0, {})
        return OptimizationResult(best_params=best_params, best_metric=best_metric, history=pd.DataFrame(history))
