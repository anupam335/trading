# trading

## Setup

Install dependencies in your Python environment:

```bash
pip install -r requirements.txt
```

If you are using the Conda environment in this repository, activate it first.

## CLI Usage

This project includes a command-line interface for data download, scheduling, backtesting, and optimization.

### Run a historical download

```bash
python -m python.main download NIFTY --period 1y --interval 1d --out data/raw
```

### Schedule repeated downloads

```bash
python -m python.main schedule NIFTY --period 1y --interval 1d --minutes 60 --out data/raw
```

### Run a backtest and export reports

```bash
python -m python.main backtest NIFTY --period 1y --interval 1d --report-dir data/reports --initial-capital 100000
```

### Run an optimization search and export history

```bash
python -m python.main optimize NIFTY --period 1y --interval 1d --report-dir data/reports --initial-capital 100000
```

Reports are saved under `data/reports` by default if `--report-dir` is omitted.

## Tests

Run the test suite with:

```bash
python -m pytest -q
```

For a focused Phase 4 validation, run:

```bash
python -m pytest -q tests/python/test_main.py
```