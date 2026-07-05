# 06_RISK_ENGINE.md

# AI NIFTY Predictor Pro - Risk Engine Specification

**Version:** 0.1.0\
**Status:** Draft

------------------------------------------------------------------------

# Purpose

The Risk Engine protects trading capital and standardizes trade
management.

A trade is valid only when both:

-   Setup quality is acceptable
-   Risk is acceptable

The Risk Engine has authority to reject any trade regardless of signal
quality.

------------------------------------------------------------------------

# Objectives

-   Preserve capital
-   Limit drawdown
-   Standardize exits
-   Improve consistency
-   Eliminate emotional decision making

------------------------------------------------------------------------

# Risk Philosophy

> Good trades are created by good risk management, not only good
> entries.

------------------------------------------------------------------------

# Trade Lifecycle

``` text
Setup
  ↓
Trigger
  ↓
Risk Validation
  ↓
Position Size
  ↓
Entry
  ↓
Manage Trade
  ↓
Exit
```

------------------------------------------------------------------------

# Position Risk

Default configuration:

  Parameter          Default
  ------------------ --------------
  Risk per Trade     1%
  Max Open Trades    1
  Max Trades / Day   3
  Max Daily Loss     3R
  Max Weekly Loss    Configurable

------------------------------------------------------------------------

# Stop Loss

Primary Method

ATR Based

Default Formula

Stop Loss = ATR × 1.5

Alternative Methods

-   Swing High / Low
-   VWAP
-   Structure Break
-   Fixed Points (optional)

------------------------------------------------------------------------

# Profit Targets

  Target   Rule
  -------- ---------------
  T1       1R
  T2       2R
  T3       Trailing Exit

------------------------------------------------------------------------

# Break-even Rules

Move Stop Loss to Entry when:

-   Target 1 achieved
-   User configurable

------------------------------------------------------------------------

# Trailing Stop

Supported Methods

-   ATR Trail
-   EMA20 Trail
-   Swing Trail
-   Structure Trail

Default

ATR Trail

------------------------------------------------------------------------

# Trade Invalidation

Cancel pending trade if:

-   Setup disappears
-   Trigger expires
-   Market regime changes
-   Risk:Reward below threshold
-   Session ends

------------------------------------------------------------------------

# Position Sizing

Future Version

Position Size = Account Risk / Stop Loss Distance

Current Pine Version

Display recommended position size (manual execution).

------------------------------------------------------------------------

# Daily Protection Rules

Stop trading for the day after:

-   Maximum daily loss reached
-   Maximum trades reached

Optional

Pause after consecutive losses.

------------------------------------------------------------------------

# Risk Reward Filter

Minimum acceptable:

1 : 2

Configurable by user.

Reject trades below minimum threshold.

------------------------------------------------------------------------

# Session Rules

Preferred

09:20 - 11:30

Selective

11:30 - 13:00

Normal

13:00 - 15:15

Avoid

After 15:15

------------------------------------------------------------------------

# Dashboard Requirements

Display

-   Entry
-   Stop Loss
-   Target 1
-   Target 2
-   Target 3
-   Risk:Reward
-   Trade Status

------------------------------------------------------------------------

# Alerts

Generate alerts for

-   Stop moved to Break-even
-   Target 1 Hit
-   Target 2 Hit
-   Trailing Stop Activated
-   Stop Loss Hit
-   Trade Closed

------------------------------------------------------------------------

# Acceptance Criteria

The Risk Engine must:

-   Never repaint
-   Produce deterministic calculations
-   Support strategy backtesting
-   Reject poor risk trades
-   Be fully configurable

------------------------------------------------------------------------

# Future Enhancements

-   Volatility-adjusted position sizing
-   Kelly Criterion (research only)
-   Portfolio exposure limits
-   Correlation-aware risk
-   AI-assisted stop optimization
-   Walk-forward optimized ATR multipliers
