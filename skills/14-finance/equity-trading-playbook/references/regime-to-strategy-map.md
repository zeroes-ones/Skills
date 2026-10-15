# Regime to strategy map

Which payoff corner pays is a function of the regime, and the regime is not owned here. The
**definitions** belong to `technical-signals-engineer` (`references/regime-detection.md`,
`references/multi-timeframe.md`) and to `macro-strategist` (`references/macro-regime-classification.md`,
`references/risk-on-risk-off-framework.md`). This file only maps a regime *label* onto a payoff
corner, an entry logic that expresses it, an exit rule, a sizing consequence, and the neighbour skill
that supplies the read. It never defines an indicator, a lookback or a classification threshold.

## The map

| Regime | Which corner pays | Entry logic that expresses it | Exit rule | Sizing consequence | Regime read comes from |
|---|---|---|---|---|---|
| **Trending / uptrend (bull market)** | High `b`: trend continuation, breakout, pullback continuation. `b >= 2`, `p* <= 0.333333` | Enter in the direction of the established structure on a pullback or a breakout, never mid-range. Structure-based stop, structural or fixed-R target | Fixed `b` target or a structural target; a trailing exit only if the card declares it and the `p` cost is measured | `R_max` **smallest**, because a sub-50% `p` implies the longest losing streaks: 1.2336% at `p = 0.40`, `n = 250` | `technical-signals-engineer` (trend/range read), `macro-strategist` (bull regime) |
| **Range-bound** | Low `b`, high `p`: range fade, failed breakout. `b ~ 0.5-1.0`, `p* ~ 0.5-0.667` | Enter against a tested boundary on a rejection; enter mid-range never. Stop beyond the boundary | Target the mid or the far boundary. A target **smaller** than the stop is the honest shape | `R_max` **larger**, because a high `p` implies short streaks: 2.5351% at `p = 0.65` | `technical-signals-engineer` (ADX-low / range read) |
| **High volatility** | High `b` only, and only with an ATR-scaled stop; the low-`b` corners become cost-heavy | Same entries, wider stops in price terms. **Fewer trades**: the same dollar risk buys fewer shares | ATR-scaled target, not a fixed percent | `R_max` **falls** as volatility rises, and this is the direction of the effect: `sl_pct` grows, but so does gap risk, and `R_max` is a fraction of *equity* while the dollars-per-share risk grows | `technical-signals-engineer` (volatility read); gap exposure from `equity-risk-and-capital-engineer` (`references/gap-and-event-risk.md`) |
| **Low volatility** | Both, and this is the regime where a tight stop's cost drag bites hardest | Contraction then expansion; a base break in the direction of the higher-timeframe read | Fixed `b`; the stop distance in percent is small, so `c_R` is large — compute it | `R_max` is at its most comfortable, but `c_R` may consume a *larger share* of `E` than in any other regime | `technical-signals-engineer` (band-width / ATR contraction read) |
| **Event-driven** | High `b` on the post-event drift; **not** a corner at all through the event | Enter **after** the event, once the gap holds. Holding through the event is a different card and must be pre-registered as one | Stop beyond the gap edge, sized for gap risk; target at `2R` or the measured move | `R_max` must be reduced where the position can gap **through** the stop. A stop is a level, not a guarantee | `equity-risk-and-capital-engineer` (`references/gap-and-event-risk.md`, `references/index-and-event-calendar.md`); earnings-window suppression in `technical-signals-engineer` (`references/etf-classification.md`) |
| **Risk-off / correlation spike** | The trend corner, short-side, and only if the card defines the short side; otherwise **stand down** | Same structure logic on the downside. In a correlation spike, everything is one position, so the entry is really a portfolio decision | Unchanged exit arithmetic; the *position count* is the thing that must fall | `R_max` must be cut by the **effective** number of simultaneous positions, not the nominal count — the concentration assessment belongs to `equity-risk-and-capital-engineer` (`references/concentration-and-correlation-risk.md`) | `macro-strategist` (`references/risk-on-risk-off-framework.md`) |

## The four regimes G14 requires, and what changes on this skill's side

**Bull market / bull regime / uptrend.** Serial correlation is positive and pullbacks resolve in the
direction of the trend. This is the regime where the high-`b` corners pay and the low-`b` corners
underperform, because a range-fade entry keeps selling into a move that does not come back. The
danger here is over-confidence: a measured `p` on a trend card estimated *entirely* inside a bull
market is a measurement of the bull market as much as of the card. Say which regime the sample
covers.

**Correction / pullback.** The characteristic damage is a cluster of losses that a fixed-`b` card
absorbs and a discretionary card does not. `L` for `p = 0.40` at `n = 250` is 10.809 — that is the
*expected longest* streak, and a correction is where you meet it. The correction is also where the
regime filter earns its keep: a card without one is in a trend corner during a downtrend.

**Bear market / downturn / drawdown / recession.** The high-`b` trend corner works here **only if
the card defines the short side**. A long-only book on a trend corner in a bear market has a corner
whose `p` was measured in a bull market: the `b` is unchanged and the `p` is not. Re-measure, do not
re-derive.

**Crash / tail event / black swan (for example March 2020).** This is the regime where a fixed-`b`
card's `sd` assumption fails outright. A gap through the stop turns a `−1R` loss into a
`−2R` or `−3R` loss, which means the two-point distribution that underpins `sd`, `n_req` and `R_max`
is not the distribution being sampled. **A sample containing one crash and no second one cannot
estimate crash risk.** Treat the crash as a named observation and reduce size on gap risk grounds,
not on the arithmetic grounds this skill provides.

## The two directional claims, derived

### Claim 1 — a trend corner pays when serial correlation is positive, and is whipsawed in a range

Consider the entry "buy a pullback to support, stop below it, target 3R". Inside a trend, the
conditional probability that the next move resumes upward is elevated, so the realised `p` on the
card is above its unconditional value. Inside a range, the same "support" is the middle of nothing:
price crosses it in both directions, the stop is hit before the target on a larger fraction of
trades, and `p` falls. With `b = 3` fixed, `p* = 0.25` is unchanged — but a realised `p` of 0.22 in
the range gives `E = 0.22*3 − 0.78 = −0.12R`, while `p = 0.40` in the trend gives `+0.60R`.

**Same card, same `b`, sign flip on `p` alone.** The regime filter is not decoration; it is the
variable that decides which of those two numbers you get.

### Claim 2 — a mean-reversion corner pays in a range and is destroyed by a trend

Consider "sell the upper boundary, stop above it, target the mid", `b = 0.75`, `p* = 0.571429`. In a
range, price reverts and `p` is high. When a trend begins, two things happen at once and both are
arithmetic:

1. the boundary breaks instead of holding, so the stop fires more often — `p` falls;
2. the trades that do win win the same 0.75R, because the target is unchanged.

With `p` falling from 0.65 to 0.50 at `b = 0.75`:
`E = 0.50*0.75 − 0.50 = −0.125000R`. The corner is negative, and **no size change helps**. This is
the single most common shape of "my mean-reversion system worked for a year and then stopped": the
regime changed, the card did not, and the card was never `p*`-aware.

## Higher volatility widens the stop, which lowers `R_max`, which lowers size

This is a derived chain, not a preference. Take a card whose stop is a fixed ATR multiple.

```
sl_pct          = 100 * k * ATR / price           -- rises when ATR rises
R_dollars/shr   = k * ATR                         -- rises when ATR rises
shares for R    = risk_dollars / (k * ATR)        -- FALLS when ATR rises
c_R             = bps / (100 * sl_pct)            -- FALLS when ATR rises (wider stop, lower drag)
```

So: **volatility and position size move in opposite directions.** For a fixed dollar risk per trade,
a doubling of ATR halves the share count. And `R_max`, expressed as a percentage of equity, is the
ceiling on *dollars* at risk, so the combination is:

```
risk_dollars = equity * R_max_pct / 100
shares       = floor( risk_dollars / (k * ATR) )
```

Worked, at `k = 2.0`:

| ATR | price | `sl_pct` | shares at `R_max = 1.2336%`, equity `$100,000` | notional | `c_R` at 5 bps |
|---|---|---|---|---|---|
| `$5.00` | `$50.00` | 20.0% | `floor(1233.55/10.00) = 123` | `$6,150` | 0.002500R |
| `$2.50` | `$50.00` | 10.0% | `floor(1233.55/5.00) = 246` | `$12,300` | 0.005000R |
| `$1.25` | `$50.00` | 5.0% | `floor(1233.55/2.50) = 493` | `$24,650` | 0.010000R |

The dollar risk is identical in all three rows. The share count doubles as volatility halves, and the
cost drag in R doubles with it — **because a tighter stop spends a larger fraction of the position's
price on the round trip.** That is the whole reason a low-volatility regime is where `c_R` becomes
the binding term.

## What this file does not do

It does not define a trend, a range, a volatility level, or a regime boundary. If a card needs a
regime read, it gets it from `technical-signals-engineer` or `macro-strategist` and cites it. A
strategy whose regime filter uses an undefined "looks like a trend" is not a card; it is SC-0 in
`strategy-cards.md`.

## Cross-references

- The corners themselves: `payoff-corners-for-equities.md`
- Cost drag by stop distance: `cost-drag-and-stop-distance.md`
- Cards, one per regime: `strategy-cards.md`
- Which indicator defines which read: `technical-signals-engineer` →
  `references/regime-detection.md`, `references/indicator-formulas.md`, `references/multi-timeframe.md`
- Which macro regime is in force: `macro-strategist` → `references/macro-regime-classification.md`,
  `references/risk-on-risk-off-framework.md`
