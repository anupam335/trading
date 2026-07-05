"""Main entry point for Project VEDA: CLI, scheduler with logging and graceful shutdown."""

from __future__ import annotations
import argparse
import logging
import os
import signal
import threading
import time
from typing import Optional

import pandas as pd
from python.backtesting.backtester import Backtester
from python.backtesting.signals import generate_signals
from python.downloader.downloader import Downloader
from python.optimizer.grid_search import GridSearchOptimizer
from python.reports.reporting import backtest_summary, export_equity_curve, export_summary_csv


# Basic logging configuration
LOG_LEVEL = os.environ.get("VEDA_LOG_LEVEL", "INFO")
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("veda")


def run_download(ticker: str, period: str, interval: str, out_dir: Optional[str] = None):
    d = Downloader(ticker=ticker, period=period, interval=interval, out_dir=out_dir)
    df = d.fetch()
    logger.info("Fetched %s rows for %s", len(df), ticker)
    return df


def schedule_download(ticker: str, period: str, interval: str, minutes: int, out_dir: Optional[str] = None):
    """Run downloader repeatedly every `minutes` minutes with graceful shutdown."""
    logger.info("Starting scheduler: ticker=%s every %s minutes", ticker, minutes)
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except Exception as e:
        raise RuntimeError("apscheduler is required. Install with `pip install apscheduler`") from e

    stop_event = threading.Event()

    def job():
        try:
            run_download(ticker, period, interval, out_dir)
        except Exception:
            logger.exception("Download job failed")

    sched = BackgroundScheduler()
    # run immediately and then at fixed intervals
    sched.add_job(job, "interval", minutes=minutes, next_run_time=None)

    def _shutdown(signum=None, frame=None):
        logger.info("Shutdown signal received (%s). Shutting down scheduler...", signum)
        try:
            sched.shutdown(wait=True)
        except Exception:
            logger.exception("Error while shutting down scheduler")
        stop_event.set()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, _shutdown)
    try:
        signal.signal(signal.SIGTERM, _shutdown)
    except Exception:
        # SIGTERM may not be available on Windows
        logger.debug("SIGTERM not available on this platform")

    sched.start()
    logger.info("Scheduler started: downloading %s every %s minutes", ticker, minutes)

    try:
        # Wait until shutdown is requested
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        _shutdown(signal.SIGINT, None)


def run_backtest(
    ticker: str,
    period: str,
    interval: str,
    out_dir: Optional[str],
    report_dir: Optional[str],
    initial_capital: float,
):
    df = run_download(ticker, period, interval, out_dir)
    entry, exit, confidence = generate_signals(df)
    backtester = Backtester(initial_capital=initial_capital)
    result = backtester.run(df, entry, exit)

    summary_df = backtest_summary(result)
    report_dir = report_dir or os.path.join(os.getcwd(), "data", "reports")
    os.makedirs(report_dir, exist_ok=True)
    summary_path = os.path.join(report_dir, f"backtest_summary_{ticker.replace('^','')}.csv")
    equity_path = os.path.join(report_dir, f"equity_curve_{ticker.replace('^','')}.csv")
    export_summary_csv(summary_df, summary_path)
    export_equity_curve(result, equity_path)
    logger.info("Backtest complete: summary=%s equity=%s", summary_path, equity_path)
    return result


def run_optimizer(
    ticker: str,
    period: str,
    interval: str,
    out_dir: Optional[str],
    report_dir: Optional[str],
    initial_capital: float,
):
    df = run_download(ticker, period, interval, out_dir)

    def backtest_fn(data: pd.DataFrame, params: dict):
        entry, exit, _ = generate_signals(
            data,
            fast_len=params["fast_len"],
            slow_len=params["slow_len"],
            rsi_len=params["rsi_len"],
            obv_ma_len=params["obv_ma_len"],
            setup_ema_len=params["setup_ema_len"],
            atr_len=params["atr_len"],
            entry_threshold=params["entry_threshold"],
            exit_threshold=params["exit_threshold"],
        )
        bt = Backtester(initial_capital=initial_capital)
        return bt.run(data, entry, exit)

    optimizer = GridSearchOptimizer(Backtester(initial_capital=initial_capital))
    param_grid = {
        "fast_len": [10, 14],
        "slow_len": [30, 50],
        "rsi_len": [12, 14],
        "obv_ma_len": [20],
        "setup_ema_len": [20],
        "atr_len": [14],
        "entry_threshold": [3, 4],
        "exit_threshold": [0, 1],
    }
    result = optimizer.search(df, param_grid, backtest_fn)
    report_dir = report_dir or os.path.join(os.getcwd(), "data", "reports")
    os.makedirs(report_dir, exist_ok=True)
    history_path = os.path.join(report_dir, f"optimization_history_{ticker.replace('^','')}.csv")
    result.history.to_csv(history_path, index=False)
    logger.info("Optimization complete: best_params=%s history=%s", result.best_params, history_path)
    return result


def main():
    parser = argparse.ArgumentParser(prog="ai-nifty-predictor-pro")
    parser.add_argument("--version", action="store_true", help="Show version")
    sub = parser.add_subparsers(dest="cmd", required=False)

    p_dl = sub.add_parser("download", help="Fetch historical data once")
    p_dl.add_argument("ticker", help="Ticker symbol (e.g. ^NSEI or NIFTY) or full symbol")
    p_dl.add_argument("--period", default="1y")
    p_dl.add_argument("--interval", default="1d")
    p_dl.add_argument("--out", default=None, help="Output directory for raw data")

    p_sched = sub.add_parser("schedule", help="Schedule repeated downloads")
    p_sched.add_argument("ticker", help="Ticker symbol to download")
    p_sched.add_argument("--period", default="1y")
    p_sched.add_argument("--interval", default="1d")
    p_sched.add_argument("--minutes", type=int, default=60, help="Interval in minutes between runs")
    p_sched.add_argument("--out", default=None, help="Output directory for raw data")

    p_bt = sub.add_parser("backtest", help="Run a backtest and export reports")
    p_bt.add_argument("ticker", help="Ticker symbol to backtest")
    p_bt.add_argument("--period", default="1y")
    p_bt.add_argument("--interval", default="1d")
    p_bt.add_argument("--out", default=None, help="Output directory for raw data")
    p_bt.add_argument("--report-dir", default=None, help="Directory to save backtest reports")
    p_bt.add_argument("--initial-capital", type=float, default=100000.0, help="Initial capital for backtest")

    p_opt = sub.add_parser("optimize", help="Run a grid search optimizer and export results")
    p_opt.add_argument("ticker", help="Ticker symbol to optimize")
    p_opt.add_argument("--period", default="1y")
    p_opt.add_argument("--interval", default="1d")
    p_opt.add_argument("--out", default=None, help="Output directory for raw data")
    p_opt.add_argument("--report-dir", default=None, help="Directory to save optimization history")
    p_opt.add_argument("--initial-capital", type=float, default=100000.0, help="Initial capital for optimization backtests")

    args = parser.parse_args()
    if args.version:
        print("AI-NIFTY-Predictor-Pro v0.1")
        return

    if args.cmd == "download":
        run_download(args.ticker, args.period, args.interval, args.out)
    elif args.cmd == "schedule":
        schedule_download(args.ticker, args.period, args.interval, args.minutes, args.out)
    elif args.cmd == "backtest":
        run_backtest(
            args.ticker,
            args.period,
            args.interval,
            args.out,
            args.report_dir,
            args.initial_capital,
        )
    elif args.cmd == "optimize":
        run_optimizer(
            args.ticker,
            args.period,
            args.interval,
            args.out,
            args.report_dir,
            args.initial_capital,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
