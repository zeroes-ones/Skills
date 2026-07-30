# Tax Treatment — Section 1256

> Section 1256 60/40 treatment, mark-to-market rules, wash sale inapplicability, Form 6781 filing requirements.

## Section 1256 Overview

Futures contracts (both cash-settled and physical-delivery) are classified as **Section 1256 contracts** under the Internal Revenue Code. This provides significant tax advantages over equity trading.

## 60/40 Rule

All futures gains and losses are taxed:

- **60%** at the **long-term capital gains rate** (max 20% federal)
- **40%** at the **short-term capital gains rate** (ordinary income rate, max 37%)

Regardless of how long you held the position. Even a 5-minute day trade gets the 60/40 split.

### Effective Tax Rate Comparison

| Holding Period | Stocks (LTCG only if >1yr) | Futures (always 60/40) | Advantage |
|---------------|---------------------------|----------------------|-----------|
| Day trade | 37% (all short-term) | 26.8% (blended) | Futures: +10.2% after-tax |
| 6 months | 37% (all short-term) | 26.8% (blended) | Futures: +10.2% after-tax |
| 13 months | 20% (all long-term) | 26.8% (blended) | Stocks: +6.8% after-tax |

**Key insight:** For active traders holding positions less than 1 year, futures offer a ~10% after-tax advantage. For buy-and-hold (>1 year), stocks are ~7% better after tax.

## Blended Tax Rate Computation

```
blended_rate = (0.60 × LTCG_rate) + (0.40 × ordinary_rate)

Example (top bracket: 37% ordinary, 20% LTCG):
blended_rate = (0.60 × 0.20) + (0.40 × 0.37) = 0.12 + 0.148 = 0.268 = 26.8%
```

## Mark-to-Market Rule

At year-end (December 31), all open Section 1256 positions are **marked to market**:
- Unrealized gains are treated as realized gains
- Unrealized losses are treated as realized losses
- You pay tax on paper profits. You harvest paper losses.
- This happens AUTOMATICALLY — you don't choose

### Mark-to-Market Example

```
Dec 30: Bought 1 ES at 5500.00
Dec 31: ES closes at 5525.50. Unrealized gain: 25.50 pts × $50 = $1,275
Tax treatment: $1,275 is treated as realized on Dec 31, taxed at 26.8% (blended).
Jan 2: ES is sold at 5550.00. Realized gain for new tax year: 24.50 pts × $50 = $1,225
```

The Dec 31 mark-to-market creates a "tax lot reset" — your cost basis becomes the year-end price.

## Wash Sale Exemption

**Wash sale rules DO NOT apply to Section 1256 contracts.** This is a major advantage.

| Scenario | Stocks | Futures |
|----------|--------|---------|
| Sell ES at loss on Dec 29, buy back Dec 31 | Wash sale — loss deferred | Loss fully deductible this year |
| Sell AAPL at loss on Dec 29, buy back Dec 31 | Wash sale — loss deferred, added to cost basis | N/A (stocks are not 1256) |

This means you can harvest futures losses at year-end and re-enter positions immediately without triggering wash sale rules.

## Form 6781

Futures gains and losses are reported on **Form 6781: Gains and Losses from Section 1256 Contracts and Straddles**.

```
Form 6781 Part I: Section 1256 Contracts Marked to Market
├── Line 1: Total gains/losses from Section 1256 contracts
├── Line 8: Mark-to-market adjustment (year-end unrealized)
└── Line 9/10: 60% LTCG + 40% STCG flow to Schedule D
```

## Broker Reporting

Brokers issue **Form 1099-B** for futures:
- Futures transactions are reported separately from equities
- The 1099-B should show aggregate profit/loss for the year
- Many brokers provide a realized gain/loss summary with 60/40 split
- **Always verify broker calculations** — errors in 1256 reporting are common

## Tax Planning Strategies

### Strategy 1: Year-End Loss Harvesting
```
Sell losing futures positions before Dec 31 → deduct losses this year
Immediately re-enter positions on Jan 2 → same economic exposure, harvested loss
No wash sale rule to prevent this
```

### Strategy 2: Defer Gains via Spreads
```
Enter a calendar spread that locks in gains for this year
The spread straddles year-end — mark-to-market applies
Consult a tax professional for straddle rules (different from wash sale)
```

### Strategy 3: Asset Location
```
Trade futures in taxable accounts (60/40 advantage)
Trade equities in tax-advantaged accounts (avoid short-term rates)
The tax alpha from 60/40 treatment compounds significantly over time
```

## Important Exceptions

- **FX futures (6E, 6J, 6B):** Section 1256 unless trader elects Section 988 (ordinary gain/loss treatment). Default: 1256. Election: 988.
- **Broad-based index options (SPX, NDX):** Also Section 1256 (cash-settled index options)
- **Single-stock futures:** Section 1256 (but very limited liquidity)
- **Futures options:** Section 1256 (options on Section 1256 contracts inherit the treatment)

## Disclaimer

This reference is for educational purposes. Tax laws change. Consult a qualified tax professional before implementing futures tax strategies. Section 1256 does NOT apply to securities (stocks), ETF options, or cryptocurrency futures on non-CFTC-regulated exchanges.

