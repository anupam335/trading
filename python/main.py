"""Main entry point for Project VEDA: CLI, scheduler with logging and graceful shutdown."""

from __future__ import annotations
import argparse
import logging
import os
import signal
import threading
import time
from typing import Optional

from python.downloader.downloader import Downloader


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
