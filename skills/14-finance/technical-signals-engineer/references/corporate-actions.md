# Corporate Actions — Signal Suppression Rules

## Earnings Window

Suppress ALL signals for individual stocks during:
- [-2 trading days, +2 trading days] relative to earnings announcement
- After earnings: wait for 5 full sessions of post-earnings price discovery
- Exception: signals from the PRE-earnings trend that triggered BEFORE [-2] window remain valid

Rationale: Earnings gap moves of 5-15% violate the continuity assumption of all technical indicators. RSI, MACD, BB values are mechanically distorted by gap opens.

## Dividend Dates

| Date Type | Action |
|-----------|--------|
| Declaration Date | No action — informational only |
| Ex-Dividend Date | SUPPRESS signals — price drop is mechanical, NOT a sell signal |
| Record Date | No action |
| Payable Date | No action |

Ex-dividend price adjustment: stock drops by dividend amount at open. This mechanical drop looks like a bearish signal to all indicators. It is NOT.

## Stock Splits

- Forward split (2:1, 3:1, etc.): Recalculate ALL indicators from scratch using split-adjusted history
- Reverse split: Same — recalculate from scratch
- NEVER compute indicators across split boundary without adjustment
- Split ratio must be applied to ALL historical data before any indicator computation

## Mergers & Acquisitions

- Target company: SUPPRESS all signals — price converges to deal price, not technical patterns
- Acquirer: WATCH for gap-down if deal premium is high (>25%). Reduce confidence by 20.
- Post-merger: Require 20 sessions of combined-entity trading before resuming signals

## Low Float / Low Volume Stocks

| Metric | Threshold | Action |
|--------|-----------|--------|
| Avg Daily Volume | < $5M | Flag: BB unreliable, OBV meaningless |
| Float | < 20M shares | Flag: manipulation-prone, double divergence requirements |
| Bid-Ask Spread | > 0.5% | Flag: slippage eats signal edge, reduce confidence 25 |
