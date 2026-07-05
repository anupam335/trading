"""Top-level package for Project VEDA Python modules.

This file makes the `python` directory a regular Python package so tests
and CI can import modules as `python.<submodule>`.
"""

__all__ = [
    "backtesting",
    "downloader",
    "indicators",
    "features",
    "setups",
    "triggers",
    "probability",
    "risk",
    "strategy",
    "optimizer",
    "reports",
]
