# 03_TRADING_SYSTEM_SPEC.md

# AI NIFTY Predictor Pro - Trading System Specification

**Version:** 0.1.0\
**Status:** Draft

------------------------------------------------------------------------

# Purpose

This document defines the business rules for the trading system.

Every trading signal, setup, filter, entry, exit and risk management
rule must follow this specification.

------------------------------------------------------------------------

# Primary Market

-   NIFTY 50

Future Markets

-   BANKNIFTY
-   FINNIFTY
-   MIDCPNIFTY

------------------------------------------------------------------------

# Trading Timeframes

  Purpose        Timeframe
  -------------- ------------
  Execution      5 Minutes
  Confirmation   15 Minutes
  Trend Bias     30 Minutes

------------------------------------------------------------------------

# Trading Session

  Session        Action
  -------------- -------------------
  09:15--09:20   Observe Only
  09:20--11:30   Preferred
  11:30--13:00   Trade Selectively
  13:00--15:15   Normal Trading
  After 15:15    No New Trades

------------------------------------------------------------------------

# Trading Lifecycle

``` mermaid
flowchart LR
A[Scan]
-->B[Market Regime]
-->C[Setup]
-->D[Trigger]
-->E[Entry]
-->F[Manage]
-->G[Exit]
-->H[Review]
```

------------------------------------------------------------------------

# Market Regimes

The system classifies the market before looking for trades.

## Trending

Characteristics

-   EMA alignment
-   ADX \> threshold
-   Price respects VWAP

Preferred Setups

-   Trend Pullback
-   VWAP Reclaim

------------------------------------------------------------------------

## Ranging

Characteristics

-   Low ADX
-   Flat EMAs

Preferred Action

No trend-following trades.

------------------------------------------------------------------------

## High Volatility

Characteristics

-   ATR expansion
-   Large candles

Preferred Action

Reduce position size or wait for confirmation.

------------------------------------------------------------------------

# Setup Lifecycle

``` text
Scanning
↓
Setup Forming
↓
Setup Ready
↓
Trigger Waiting
↓
Trigger Confirmed
↓
Trade Active
↓
Trade Closed
```

------------------------------------------------------------------------

# Initial Setup Library

## Setup 1 - Trend Pullback

Requirements

-   EMA20 \> EMA50 \> EMA200
-   Price above VWAP
-   ADX confirms trend
-   Pullback toward EMA20 or VWAP
-   Lower volume during pullback

Trigger

-   Bullish engulfing
-   Strong bullish candle
-   Break of previous candle high

Priority

★★★★★

------------------------------------------------------------------------

## Setup 2 - Opening Range Breakout

Requirements

-   Define first 15-minute range
-   Trend aligned
-   Relative volume above normal

Trigger

Breakout with momentum.

------------------------------------------------------------------------

## Setup 3 - VWAP Reclaim

Requirements

-   Price regains VWAP
-   Higher timeframe trend agrees

Trigger

Bullish confirmation candle.

------------------------------------------------------------------------

## Setup 4 - Previous Day High Breakout

Requirements

-   Consolidation below PDH
-   Increasing volume

Trigger

Confirmed breakout.

------------------------------------------------------------------------

# Trigger Rules

A trigger is valid only when an approved setup exists.

Supported triggers

-   Bullish Engulfing
-   Bearish Engulfing
-   Momentum Candle
-   Break Previous High
-   Break Previous Low

------------------------------------------------------------------------

# Entry Rules

A trade is allowed only when:

-   Market regime is valid.
-   Setup quality meets threshold.
-   Trigger is confirmed.
-   Risk/Reward is acceptable.

Otherwise:

NO TRADE.

------------------------------------------------------------------------

# Exit Rules

Exit conditions

-   Stop loss
-   Target reached
-   Trailing stop
-   Structure failure
-   End-of-session exit (configurable)

------------------------------------------------------------------------

# Risk Management

Default Stop Loss

ATR × 1.5

Targets

-   Target 1 = 1R
-   Target 2 = 2R
-   Target 3 = Trail

Maximum trades/day

Configurable (default 3)

------------------------------------------------------------------------

# Confidence Score

  Component            Weight
  ------------------ --------
  Trend                    20
  Momentum                 15
  Volume                   10
  Structure                20
  Setup Quality            20
  Risk                     10
  Higher Timeframe          5

Interpretation

-   90--100 : Excellent
-   80--89 : Strong
-   70--79 : Good
-   60--69 : Average
-   Below 60 : No Trade

------------------------------------------------------------------------

# Dashboard Requirements

Display

-   Market Regime
-   Trend
-   Active Setup
-   Trigger Status
-   Confidence
-   Entry
-   Stop Loss
-   Targets
-   Risk:Reward

------------------------------------------------------------------------

# Alert Requirements

Alerts for

-   Setup Ready
-   Trigger Confirmed
-   Buy
-   Sell
-   Stop Loss
-   Target 1
-   Target 2
-   Target 3
-   Trend Change

------------------------------------------------------------------------

# Acceptance Criteria

A feature is accepted only if:

-   Documented
-   Implemented
-   Backtested
-   Non-repainting
-   Improves or maintains overall performance

------------------------------------------------------------------------

# Open Questions

These will be validated through research and backtesting.

-   Best ADX threshold?
-   Best ATR multiplier?
-   Best ORB duration?
-   Best pullback depth?
-   Expiry-day behavior?
-   Lunch session filter effectiveness?
-   Impact of India VIX?
-   Value of options-chain data?
