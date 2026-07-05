"""Main entry point for Project VEDA: simple CLI and scheduler for downloader."""

from __future__ import annotations
import argparse
import logging
import time
from typing import Optional

from python.downloader.downloader import Downloader


def run_download(ticker: str, period: str, interval: str, out_dir: Optional[str] = None):
    d = Downloader(ticker=ticker, period=period, interval=interval, out_dir=out_dir)
    df = d.fetch()
    print(f"Fetched {len(df)} rows for {ticker}")


def schedule_download(ticker: str, period: str, interval: str, minutes: int, out_dir: Optional[str] = None):
    """Run downloader repeatedly every `minutes` minutes."""
    logging.info("Starting scheduler: ticker=%s every %s minutes", ticker, minutes)
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except Exception as e:
        raise RuntimeError("apscheduler is required. Install with `pip install apscheduler`") from e

    def job():
        try:
            run_download(ticker, period, interval, out_dir)
        except Exception as e:
            logging.exception("Download job failed: %s", e)

    sched = BackgroundScheduler()
    sched.add_job(job, "interval", minutes=minutes, next_run_time=None)
    sched.start()
    print(f"Scheduler started: downloading {ticker} every {minutes} minutes. Ctrl-C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        sched.shutdown()


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

    args = parser.parse_args()
    if args.version:
        print("AI-NIFTY-Predictor-Pro v0.1")
        return

    if args.cmd == "download":
        run_download(args.ticker, args.period, args.interval, args.out)
    elif args.cmd == "schedule":
        schedule_download(args.ticker, args.period, args.interval, args.minutes, args.out)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
