# Black Swan Protection for Volatility Arbitrage

> **Portability target:** Spec-level. Tail risk concepts are universal — implement with any risk system.

## The Central Problem

Volatility arbitrage strategies have positive expected value with negative skew: you make $1,000/month for 11 months, then lose $50,000 in month 12. The cumulative P&L is negative despite 91.7% winning months. **Vol arb without tail protection is not arbitrage — it's picking up pennies in front of a steamroller.**

## The Four Tail Events

| Event | Historical Example | VIX Peak | Vol Arb Loss | Frequency |
|-------|-------------------|----------|-------------|-----------|
| Crash | Feb 2018 (Volmageddon) | 50.30 | Short vol funds: -90%+ | Every 2-4 years |
| Correction | Oct 2023 | 23.08 | Short vol: -15% to -30% | Every 1-2 years |
| Flash Crash | Aug 2015 (China deval) | 53.29 (intraday) | -20% to -40% | Every 3-5 years |
| Pandemic | Mar 2020 (COVID) | 82.69 | -30% to -60%+ | Every 10-20 years |

## Protection Framework

### Layer 1: Sizing (Pre-Trade)

The cheapest protection is correct sizing BEFORE the tail event.

```
Position Size = Base Size × Regime Multiplier × VIX Multiplier

Where:
  Base Size = Kelly-optimal allocation for the strategy (typically 2-5% of portfolio)
  Regime Multiplier:
    1.0 = Normal regime (VIX 15-20, contango)
    0.5 = Warning regime (VIX 20-25, term structure flattening)
    0.25 = Danger regime (VIX 25-30, term structure inverted)
    0.0 = Crisis regime (VIX > 30)
  VIX Multiplier = 15 / current VIX (capped at 1.0)
```

### Layer 2: Convexity Hedging (Active)

Short vol positions are short convexity. Tail hedges add positive convexity:

| Hedge | Cost | Protection | Best For |
|-------|------|-----------|----------|
| OTM SPX puts (5% OTM, 30 DTE) | 0.3-0.5%/month of notional | VIX > 30: 10-20× payoff | Daily/weekly roll, always on |
| VIX calls (30% OTM) | 0.2-0.4%/month | VIX > 30: 5-15× payoff | Structural hedge, monthly roll |
| VIX futures long | Carry cost in contango (-2% to -5%/month) | Direct VIX exposure | Only during term structure inversion |
| Tail risk fund allocation | 1-2% management fee + 10-20% performance | Professional tail hedging | 2-5% of portfolio, always on |

### Layer 3: Circuit Breakers (Automated)

| Trigger | Action | Restore Condition |
|---------|--------|------------------|
| VIX > 28 intraday | Close 50% of short vol positions | VIX < 22 for 3 consecutive days |
| VIX > 35 intraday | Close 100% of short vol positions | VIX < 25 + term structure in contango for 5 days |
| Single-day portfolio loss > 5% | Halve all vol arb positions | 3 consecutive days without a breach |
| Week-over-week loss > 10% | Close all vol arb, review strategy | Manual review + 1 week observation |
| Month-over-month loss > 15% | Close all, review whether vol arb is appropriate for this account | Full strategy review |

### Layer 4: Correlation Collapse Protection

The biggest tail risk is not the vol spike itself — it's that ALL strategies correlate.

| Scenario | Correlation During Crisis | Impact |
|----------|--------------------------|--------|
| Normal market | 0.2-0.4 across vol arb strategies | Diversification works |
| VIX > 25 | 0.5-0.7 | Diversification fading |
| VIX > 35 | 0.7-0.9 | Diversification gone — all positions lose together |
| Crash (VIX > 45) | 0.9-1.0 | Full correlation — everything is one trade |

**Rule:** Size each strategy assuming 0.8 correlation with every other strategy during stress. If individual strategy max allocation is 5% at 0 correlation, it's 2% at 0.8 correlation.

## The Math: Why 11 Months of Profits Don't Matter

```
Monthly expected profit: +$2,000 (0.92 probability)
Monthly tail loss: -$40,000 (0.08 probability)

Expected monthly P&L = 0.92 × $2,000 + 0.08 × (-$40,000)
                      = $1,840 - $3,200
                      = -$1,360 per month

The strategy loses money despite winning 11 of 12 months.

WITH tail hedge (cost: $400/month):
Expected monthly P&L = $1,840 - $3,200 - $400 + (0.08 × $25,000 hedge payoff)
                      = $1,840 - $3,200 - $400 + $2,000
                      = +$240 per month

The hedge cost is the price of positive expectancy.
```

## Non-Negotiable

1. **No vol arb strategy runs without a circuit breaker.** Hard stops, not mental stops. Code, not journal entries.
2. **Sizing must INVERSE VIX.** When VIX is low, the next spike is closer. Reduce size, not increase.
3. **Correlation assumptions fail in crisis.** Size for 0.8+ correlation, not 0.2.
4. **Tail hedging has negative carry.** Accept it. The $400/month bleed is cheaper than the $40,000 drawdown.
