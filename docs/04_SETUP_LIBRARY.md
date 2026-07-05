# 04_SETUP_LIBRARY.md

# AI NIFTY Predictor Pro - Setup Library

**Version:** 0.1.0 **Status:** Draft

------------------------------------------------------------------------

# Purpose

This document defines every trading setup supported by the system.

A setup is **not** an entry signal.

A setup identifies a favorable market condition. An entry is taken only
after a valid trigger confirms the setup.

------------------------------------------------------------------------

# Setup Lifecycle

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

------------------------------------------------------------------------

# Setup Quality Rating

     Score  Grade  Action
  -------- ------- ------------
    90-100   A+    Excellent
     80-89    A    Strong
     70-79    B    Good
     60-69    C    Aggressive
      \<60    D    No Trade

------------------------------------------------------------------------

# SETUP 1 - Trend Pullback

## Objective

Join an existing trend after a healthy pullback.

## Best Market

-   Trending
-   ADX rising
-   Higher timeframe aligned

## Checklist

-   EMA20 \> EMA50 \> EMA200
-   Price above VWAP
-   ADX \> threshold
-   Pullback to EMA20 or VWAP
-   Volume contracts during pullback

## Trigger

-   Bullish engulfing
-   Break of previous candle high
-   Momentum candle

## Stop Loss

Below swing low or ATR × 1.5

## Targets

-   T1 = 1R
-   T2 = 2R
-   T3 = Trail

## Failure Conditions

-   Pullback breaks EMA50
-   Price loses VWAP
-   ADX weakens sharply

Priority: ★★★★★

------------------------------------------------------------------------

# SETUP 2 - Opening Range Breakout (ORB)

## Objective

Trade the breakout of the opening range.

## Opening Range

Default: First 15 minutes

## Checklist

-   Trend aligned
-   Relative Volume above average
-   Breakout after range formation

## Trigger

-   Close outside opening range
-   Volume expansion

## Failure Conditions

-   False breakout
-   Immediate reversal into range

Priority: ★★★★☆

------------------------------------------------------------------------

# SETUP 3 - VWAP Reclaim

## Objective

Trade when price reclaims VWAP in the direction of the higher timeframe.

## Checklist

-   Higher timeframe trend bullish
-   Price reclaims VWAP
-   Momentum improving

## Trigger

Bullish confirmation candle

Priority: ★★★★☆

------------------------------------------------------------------------

# SETUP 4 - Previous Day High Breakout

## Objective

Trade continuation after breaking PDH.

## Checklist

-   Consolidation below PDH
-   Volume builds
-   Trend supports breakout

## Trigger

Confirmed breakout candle

Priority: ★★★★☆

------------------------------------------------------------------------

# SETUP 5 - Previous Day Low Breakdown

Mirror image of PDH breakout for bearish conditions.

Priority: ★★★★☆

------------------------------------------------------------------------

# SETUP 6 - CPR Breakout

## Objective

Trade expansion after a narrow CPR.

## Checklist

-   Narrow CPR
-   Increasing ADX
-   Volume expansion

Priority: ★★★☆☆

------------------------------------------------------------------------

# SETUP 7 - BOS Retest

## Objective

Enter after a confirmed Break of Structure and successful retest.

## Checklist

-   BOS detected
-   Retest holds
-   Confirmation candle

Priority: ★★★★★

------------------------------------------------------------------------

# SETUP 8 - Liquidity Sweep Reversal

## Objective

Capture reversals after liquidity grabs.

## Checklist

-   Sweep of swing high/low
-   Rejection candle
-   Strong reversal volume

Priority: ★★★★☆

------------------------------------------------------------------------

# Common Filters

Every setup must pass:

-   Market regime filter
-   Trend filter
-   Higher timeframe filter
-   Volume filter
-   Risk filter

If any mandatory filter fails:

**NO TRADE**

------------------------------------------------------------------------

# Future Setups

-   Gap Fill
-   VWAP Fade
-   Trend Continuation Flag
-   Triangle Breakout
-   Compression Breakout
-   Expiry Day Momentum
-   News Recovery

------------------------------------------------------------------------

# Development Notes

Each setup will later receive:

-   Pine Script implementation
-   Strategy implementation
-   Historical statistics
-   Win rate
-   Profit factor
-   Typical holding time
-   Failure analysis

Only setups that improve overall system performance will remain in the
production indicator.
