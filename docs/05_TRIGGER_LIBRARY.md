# 05_TRIGGER_LIBRARY.md

# AI NIFTY Predictor Pro - Trigger Library

**Version:** 0.1.0 **Status:** Draft

------------------------------------------------------------------------

# Purpose

A trigger is the final confirmation required before entering a trade.

A trigger is **never valid on its own**.

A valid trade always follows:

Setup → Trigger → Entry

------------------------------------------------------------------------

# Trigger Lifecycle

``` text
Setup Detected
      ↓
Trigger Waiting
      ↓
Trigger Confirmed
      ↓
Risk Validation
      ↓
Trade Entry
```

------------------------------------------------------------------------

# Trigger Categories

1.  Candle Pattern
2.  Momentum
3.  Breakout
4.  Market Structure
5.  Volume
6.  Multi-Timeframe Confirmation

------------------------------------------------------------------------

# TG001 - Bullish Engulfing

## Purpose

Confirms buyers have regained control after a pullback.

## Rules

-   Bullish candle completely engulfs previous bearish body
-   Close near candle high
-   Prefer above EMA20 or VWAP

Works Best With

-   Trend Pullback
-   VWAP Reclaim
-   BOS Retest

Quality

★★★★★

------------------------------------------------------------------------

# TG002 - Bearish Engulfing

Mirror image of TG001.

Used for short opportunities.

Quality

★★★★★

------------------------------------------------------------------------

# TG003 - Momentum Candle

Requirements

-   Candle body larger than recent average
-   Strong close near high (bullish) or low (bearish)
-   ATR expansion
-   Relative volume above average

Quality

★★★★☆

------------------------------------------------------------------------

# TG004 - Previous Candle Break

Bullish

-   Break previous candle high
-   Close above breakout level

Bearish

-   Break previous candle low
-   Close below breakout level

Quality

★★★★☆

------------------------------------------------------------------------

# TG005 - BOS Confirmation

Requirements

-   Break of Structure detected
-   Candle closes beyond structure
-   Retest optional (higher confidence)

Quality

★★★★★

------------------------------------------------------------------------

# TG006 - Volume Breakout

Requirements

-   Relative Volume \> threshold
-   Breakout candle closes strongly
-   No immediate rejection

Quality

★★★★☆

------------------------------------------------------------------------

# TG007 - VWAP Reclaim Confirmation

Requirements

-   Price reclaims VWAP
-   Close above VWAP
-   Positive momentum

Quality

★★★★☆

------------------------------------------------------------------------

# Trigger Validation Checklist

Before entry confirm:

-   Setup Ready
-   Trigger Confirmed
-   Market Regime Valid
-   Higher Timeframe Aligned
-   Risk/Reward Acceptable
-   No major filter violated

If any answer is NO:

NO TRADE

------------------------------------------------------------------------

# Trigger Priority

  ID      Trigger                 Priority
  ------- ----------------------- ----------
  TG001   Bullish Engulfing       ★★★★★
  TG002   Bearish Engulfing       ★★★★★
  TG005   BOS Confirmation        ★★★★★
  TG003   Momentum Candle         ★★★★☆
  TG004   Previous Candle Break   ★★★★☆
  TG006   Volume Breakout         ★★★★☆
  TG007   VWAP Reclaim            ★★★★☆

------------------------------------------------------------------------

# Future Triggers

-   Order Block Confirmation
-   Fair Value Gap Fill
-   Liquidity Sweep Reversal
-   Delta Volume Confirmation
-   Options Flow Confirmation
-   India VIX Confirmation

------------------------------------------------------------------------

# Development Notes

Each trigger will receive:

-   Pine Script implementation
-   Unit test scenarios
-   Strategy validation
-   Historical win rate
-   Typical holding time
-   Failure analysis

Only statistically valuable triggers will remain enabled by default.
