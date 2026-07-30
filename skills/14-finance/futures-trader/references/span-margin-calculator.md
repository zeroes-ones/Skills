# SPAN Margin Calculator

> SPAN (Standard Portfolio Analysis of Risk) margin computation: risk arrays, scan range, cross-margining rules, exchange minimums.

## SPAN Overview

SPAN is CME's proprietary margin system used by all major futures exchanges. Unlike Reg T (equities), SPAN uses scenario-based risk analysis across 16 standardized scenarios per product.

## SPAN Risk Array (16 Scenarios)

Each futures contract has a risk array of 16 scenarios:

| # | Category | Price Change | Vol Change | Coverage |
|---|----------|-------------|------------|----------|
| 1 | Price Scan | -ScanRange × 1/3 | 0 | 33% move |
| 2 | Price Scan | -ScanRange × 2/3 | 0 | 67% move |
| 3 | Price Scan | -ScanRange × 3/3 | 0 | Full move |
| 4 | Price Scan | +ScanRange × 1/3 | 0 | 33% move |
| 5 | Price Scan | +ScanRange × 2/3 | 0 | 67% move |
| 6 | Price Scan | +ScanRange × 3/3 | 0 | Full move |
| 7 | Volatility | -ScanRange × 1/3 | +VolShift | Price down + vol up |
| 8 | Volatility | -ScanRange × 2/3 | +VolShift | Price down + vol up |
| 9 | Volatility | -ScanRange × 3/3 | +VolShift | Price down + vol up |
| 10 | Volatility | +ScanRange × 1/3 | -VolShift | Price up + vol down |
| 11 | Volatility | +ScanRange × 2/3 | -VolShift | Price up + vol down |
| 12 | Volatility | +ScanRange × 3/3 | -VolShift | Price up + vol down |
| 13 | Extreme | -ExtremeMove | 0 | Extreme price down |
| 14 | Extreme | +ExtremeMove | 0 | Extreme price up |
| 15 | Extreme | -ExtremeMove × 0.35 | 0 | 35% extreme down |
| 16 | Extreme | +ExtremeMove × 0.35 | 0 | 35% extreme up |

## SPAN Margin for Outright Futures

```
SPAN Margin = ScanRisk × ContractMultiplier × Contracts

Example: ES scan range = 240 points
1 ES contract: 240 × $50 = $12,000
```

## Scan Range Determination

The scan range is set by the exchange weekly based on recent volatility:
- Typical ES scan range: 200-280 points (as of mid-2026)
- Typical CL scan range: $6-10 per barrel
- Typical GC scan range: $80-120 per ounce
- Scan ranges INCREASE near expiration and during high-vol periods

**Always pull current scan range from exchange or broker API.** CME publishes updated ranges weekly on Fridays.

## Cross-Margining

When a portfolio contains offsetting positions:
- Long futures + Short calls on same underlying → reduced combined margin
- The SPAN system computes all 16 scenarios for the combined portfolio
- Offsetting positions reduce the worst-case loss across scenarios
- Typical reduction: 20-60% vs computing each position independently

## Cross-Margining Between Products

SPAN also recognizes inter-commodity spreads:
- Corn vs Wheat: correlated grains → reduced margin
- Crude vs Heating Oil: crack spread → reduced margin
- 2Y Note vs 10Y Note: yield curve → reduced margin
- ES vs NQ: equity index correlation → reduced margin

Inter-commodity spread credits are defined in the SPAN parameter file.

## Margin Call Mechanics

1. **Initial Margin:** Required to open a position
2. **Maintenance Margin:** Minimum equity to maintain position (~75-80% of initial)
3. **Margin Call:** Issued when equity falls below maintenance. Must be met intraday.
4. **Liquidation:** If margin call not met, broker liquidates positions without notice.

## Broker-Specific SPAN Access

- **IBKR:** SPAN margin available via TWS API. Use `reqMktData` with generic tick type 238 (SPAN margin).
- **Schwab (thinkorswim):** SPAN displayed in Analyze tab. API access via Schwab Developer Portal.
- **Alpaca:** Futures not yet supported as of 2026-07.
- **CME FTP:** ftp.cmegroup.com/pub/span — raw SPAN parameter files (advanced).

## SPAN vs Reg T vs Portfolio Margin

| Regime | Applies To | Methodology | Typical Margin |
|--------|-----------|-------------|---------------|
| Reg T | Equities | Fixed 50% initial | 50% of position value |
| Portfolio Margin | Equity options | Scenario-based | 15-25% of position value |
| SPAN | Futures & futures options | 16-scenario risk array | 3-8% of notional value |

**Key insight:** SPAN is generally the most capital-efficient because futures are inherently leveraged instruments and SPAN reflects actual portfolio risk, not a fixed percentage.

