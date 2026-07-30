# Commitment of Traders (COT) Analysis Framework

> COT interpretation: categories, positioning extremes, z-score computation, contrarian signal detection.

## What Is the COT Report?

The CFTC's Commitment of Traders report is released every **Friday at 3:30 PM ET**, reporting positions as of the **prior Tuesday's close**. It shows aggregate long and short positions for different trader categories across all US futures markets.

**Source:** cftc.gov/MarketReports/CommitmentsofTraders

## Trader Categories (Disaggregated Report)

| Category | Who They Are | Trading Style | Signal Value |
|----------|-------------|---------------|-------------|
| Producer/Merchant | Miners, farmers, oil companies | Hedging physical production | HIGH — they know supply |
| Swap Dealers | Banks hedging OTC swaps | Customer facilitation | MEDIUM — customer-driven |
| Managed Money | Hedge funds, CTAs | Trend-following, momentum | CONTRARIAN — herd at extremes |
| Other Reportables | Non-commercial large traders | Varied | LOW — mixed |
| Nonreportable | Small speculators (retail) | Emotional, trend-chasing | CONTRARIAN — wrong at turns |

## Computing Positioning Extremes

### Z-Score Method

```
z_score = (current_net_position - 3yr_mean) / 3yr_stddev

Where:
- current_net_position = long_contracts - short_contracts
- 3yr_mean = average net position over past 156 weeks
- 3yr_stddev = standard deviation over past 156 weeks
```

### Extreme Thresholds

| z_score | Interpretation | Action |
|---------|---------------|--------|
| > 2.0 | 2σ extreme — crowded position | Strong contrarian signal |
| 1.0 to 2.0 | Moderately extended | Weakening trend momentum |
| -1.0 to 1.0 | Normal range | Neutral signal |
| -2.0 to -1.0 | Moderately extended (opposite) | Weakening counter-trend |
| < -2.0 | 2σ extreme (opposite) | Strong contrarian signal (opposite direction) |

## Contrarian Signal Matrix

| Commercials (Producers) | Large Specs (Managed Money) | Signal | Rationale |
|------------------------|---------------------------|--------|-----------|
| NET LONG (extreme) | NET SHORT (extreme) | **BULLISH** | Producers buying (they know supply constraints), specs all short (no sellers left) |
| NET SHORT (extreme) | NET LONG (extreme) | **BEARISH** | Producers hedging aggressively (they see oversupply), specs all-in long (no buyers left) |
| NET LONG (extreme) | NET LONG (extreme) | CAUTION | Everyone bullish — who's left to buy? |
| NET SHORT (extreme) | NET SHORT (extreme) | CAUTION | Everyone bearish — who's left to sell? |

## COT Report Lag

The COT report is released Friday for positions as of Tuesday — a 3-day lag. In fast-moving markets, positioning may have changed significantly by the time you read the report. Use COT for:
- **Medium-term bias (weeks to months)** — positioning extremes take time to unwind
- **NOT for entry timing** — prices can extend further before the COT signal plays out

## COT + Technical Integration

```
COT Extreme + Technical Support/Resistance = Higher conviction contrarian trade
COT Extreme + Trend still intact = Wait for technical confirmation before fading the trend
COT Neutral + Strong Trend = Trend is the higher-probability trade
```

## Practical Examples

### Example 1: Corn (ZC) — Bullish COT Signal

```
Date: 2026-03-15
Commercials: Net long +350,000 (z-score: 2.8σ)
Large Specs: Net short -180,000 (z-score: 2.1σ)

Interpretation: Commercials are buying heavily — they expect higher grain prices.
Specs are heavily short — crowded position, squeeze fuel.
Signal: CONTRARIAN BULLISH. Look for technical confirmation to go long.
```

### Example 2: S&P 500 (ES) — Bearish COT Signal

```
Date: 2026-07-15
Commercials: Net short -120,000 (z-score: 1.8σ)
Large Specs: Net long +95,000 (z-score: 2.3σ)

Interpretation: Dealers hedging customer downside. Specs fully invested.
Signal: CONTRARIAN BEARISH (moderate). Large specs all-in long — buying exhaustion.
Action: Tighten stops on longs. Consider hedging with puts.
```

## Data Sources

- **CFTC Legacy Report:** cftc.gov/dea/futures/deacbtlf.txt — futures-only
- **CFTC Disaggregated Report:** cftc.gov/dea/futures/deacbtlf-disagg.txt — preferred for analysis
- **CFTC Supplemental Report:** cftc.gov/dea/futures/deacbtlf-supp.txt — index trader detail
- **Barchart COT:** barchart.com/futures/commitment-of-traders — visual + historical
- **Sentimentrader:** sentimentrader.com — COT indexes and extremes

