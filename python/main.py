"""Main entry point for Project VEDA"""

import argparse


def main():
    parser = argparse.ArgumentParser(prog="ai-nifty-predictor-pro")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()
    if args.version:
        print("AI-NIFTY-Predictor-Pro v0.1")
    else:
        print("Run subcommands: downloader, backtest, optimize — see docs.")


if __name__ == "__main__":
    main()
