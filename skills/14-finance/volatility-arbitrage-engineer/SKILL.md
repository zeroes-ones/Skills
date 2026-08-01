---
name: volatility-arbitrage-engineer
description: >
  Use when the user wants to exploit volatility surface pricing discrepancies:
  dispersion trading, variance risk premium harvesting, skew arbitrage, term structure
  arbitrage, VIX futures/options, or correlation trading. Use when the user asks
  "dispersion trading," "variance risk premium," "skew arbitrage," "VIX futures," "vol
  regime detection," or "implied correlation." Handles dispersion basket construction,
  VRP harvesting with regime-adaptive sizing, skew arbitrage via risk reversals, VIX
  futures roll-yield modeling, VIX options with VVIX-based premium gates, 3-regime
  volatility detection, and correlation-aware portfolio construction. Do NOT use for
  directional options trading (route to options-strategist), premium selling without
  hedging (route to options-strategist), standard vol analysis (route to
  quantitative-analyst), trade execution (route to algorithmic-trader), or advanced
  multi-leg vol structures (route to advanced-options-structures).
license: MIT
tags:
  - volatility-arbitrage
  - dispersion-trading
  - variance-risk-premium
  - skew-arbitrage
  - term-structure
  - VIX-products
  - correlation-trading
  - vol-regime-detection
chain:
  consumes_from: [quantitative-analyst, options-risk-engineer, macro-strategist, options-strategist]
  feeds_into: [algorithmic-trader, portfolio-signal-manager, advanced-options-structures]
version: 1.0.0
status: active
author: Skills Library
created: "2026-07-16"
category: "14-finance"
token_budget: 4000
---

# Volatility Arbitrage Engineer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).
> No vendor-specific frontmatter fields.

<!-- STANDARD: 3min -->
## Route the Request

| User Intent | Route To | Decision Gate |
|-------------|----------|---------------|
| "Dispersion trading" / "index vs single-stock vol" / "sell index buy constituents" | → Dispersion Trading (§3, ref: dispersion-trading-math.md) | Account > $250K. Else execution costs exceed edge |
| "Variance risk premium" / "systematic short vol" / "harvest vol premium" | → VRP Harvesting (§4, ref: variance-risk-premium.md) | VIX < 30. Else elevated crash risk |
| "Skew arbitrage" / "risk reversal" / "put skew too high" | → Skew Arbitrage (§5, ref: skew-and-term-structure-arbitrage.md) | Never net short puts when VIX > 25 |
| "VIX futures" / "VIX options" / "vol of vol" / "VVIX" | → VIX Products (§6, ref: vix-products-guide.md) | Never long > 3 days. Never short without kill switch |
| "Vol regime" / "when to sell vol" / "when to buy vol" | → Regime Detection (§7, ref: vol-regime-detection.md) | 3 regimes: Low/Normal/High. Strategy matrix |
| "Correlation trading" / "implied correlation" / "pair correlation" | → Correlation Trading (§8, ref: correlation-trading.md) | Correlation → 1.0 in crashes. That's when these trades blow up |

## 10 Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to hold short-vol positions when VIX term structure inverts (backwardation). Backwardation is the single most reliable predictor of near-term vol events — every major vol spike was preceded by term structure inversion | Trigger: `VIX_futures.front_month > VIX_futures.second_month` AND `short_vol_positions > 0` | STOP. "VIX backwardation detected. CLOSE ALL SHORT VOL within 24 hours. No exceptions. Every major vol event in modern history was preceded by or coincided with term structure inversion." |
| R2 | REFUSE to continue vol arb strategies when VIX > 30 for 3+ consecutive days. Sustained VIX > 30 means regime shift — correlation → 1.0, gaps are common | Trigger: `VIX > 30 for ≥ 3 consecutive_days` AND `vol_arb_positions > 0` | STOP. "VIX > 30 sustained for 3+ days. HALT all vol arb strategies. Close all short-vol positions. Regime has shifted: correlation → 1.0, vol arb assumptions break, gaps are common. Wait for normalization." |
| R3 | REFUSE to enter vol arb positions without computing vega AND dollar-gamma at inception. Vega-neutral does NOT mean risk-neutral — a dispersion trade can lose 10%+ in a day through correlation moves | Trigger: `new_vol_arb_position AND (vega NOT computed OR dollar_gamma NOT computed)` | STOP. "Missing risk computation: compute vega AND dollar-gamma at inception for every vol arb position. Vega-neutral dispersion can still lose 10%+ in a day. Know the full second-order risk profile." |
| R4 | REFUSE to hold dispersion trade when implied correlation > realized + 0.15. The edge is correlation mean-reversion — when correlation significantly exceeds historical norms, thesis is invalidated | Trigger: `implied_correlation - realized_correlation > 0.15 AND position = "long_dispersion"` | STOP. "Dispersion thesis invalidated: implied correlation exceeds realized by 0.15+. The edge (correlation mean-reversion) is gone. Close the dispersion trade — long dispersion = short correlation." |
| R5 | REFUSE to hold long VIX futures beyond 3 days. Contango roll decay is 5-10% per month — long VIX futures are a tactical hedge, not an investment | Trigger: `position_type = "long_vix_futures" AND holding_days > 3` | STOP. "Long VIX futures exceeded 3-day max hold. Contango roll decay costs 5-10%/month. Exit on the specified catalyst date — win or lose. VIX futures are strictly tactical, not investment." |
| R6 | REFUSE to short VIX futures without a hard VIX-level kill switch. Shorting VIX futures is picking up nickels in front of a steamroller — one vol spike costs more than years of roll yield | Trigger: `grep "short.*vix_futures" strategy_code` → no `VIX_kill_switch_level` defined | STOP. "Missing VIX kill switch on short VIX futures. Define: VIX > 28 → close 50%. VIX > 35 → close 100%. One unexited spike costs more than 3-5 years of roll yield." |
| R7 | REFUSE to allocate > 20% of account to short-vol strategies, and scale with VIX. Vol selling is procyclical — feels safest when most dangerous (low VIX precedes spikes) | Trigger: `short_vol_allocation > 0.20 × account_value OR (VIX > 25 AND short_vol_allocation > 0)` | STOP. "Short-vol allocation violated. Max 20% of account. Scale: full at VIX < 15, half at VIX 20-25, zero at VIX > 25. Vol selling is procyclical — low VIX precedes spikes." |
| R8 | REFUSE dispersion basket with < 20 single-stock names or any single name > 8% of total vega. Concentration risk in dispersion is lethal — one M&A or earnings catastrophe wipes the entire trade | Trigger: `dispersion_basket_count < 20 OR max_single_name_vega_pct > 0.08` | STOP. "Dispersion basket under-diversified: minimum 20 names required, max 8% vega per name. One M&A announcement or earnings catastrophe on a concentrated name = trade wipeout ($50K-$200K loss)." |
| R9 | REFUSE to sell VIX options premium when VVIX > 130. When vol of vol is extreme, shorting VIX options is shorting an already-panicked market — the edge is gone | Trigger: `VVIX > 130 AND strategy = "sell_vix_options_premium"` | STOP. "VVIX > 130: do NOT sell VIX options premium. The market is pricing extreme vol-of-vol. The edge is gone — wait for VVIX < 110. Shorting panicked vol is negative expected value." |
| R10 | REFUSE to skip daily correlation check on systematic vol arb book. Above 0.60 correlation, diversification stops working — all positions become one market-direction bet | Trigger: `vol_arb_positions > 0 AND last_correlation_check_age > 24h` | STOP. "Daily correlation check overdue. Run now. If average pairwise correlation > 0.60: PAUSE all new entries. Above 0.60, vol arb diversification fails — all positions are one big direction bet." |

## Decision Tree

```
Volatility arbitrage request
│
├─ Regime Assessment (ALWAYS FIRST) (§7)
│  ├─ Low Vol (VIX < 15, steep contango) → Full allocation. Harvest VRP. Sell premium.
│  ├─ Normal (VIX 15-22, mild contango) → Standard allocation. All strategies viable.
│  └─ High Vol (VIX > 25, backwardation) → Close short vol. Buy premium only. Small.
│
├─ Strategy Selection
│  ├─ VRP Harvesting (§4) → Short strangles, credit spreads. Pure premium capture.
│  │  └─ Gate: VIX < 25. Regime: Low or Normal. Sizing: 50-100% of vol allocation.
│  ├─ Dispersion Trading (§3) → Index vol vs. single-stock vol relative value.
│  │  └─ Gate: Account > $250K. 20+ names. > 2σ signal. Regime: Low or Normal.
│  ├─ Skew Arbitrage (§5) → Put skew vs call skew. Risk reversals.
│  │  └─ Gate: Skew z-score > 2.0. No short puts if VIX > 25.
│  ├─ Term Structure Arb (§5) → Calendar spreads. VIX futures curve.
│  │  └─ Gate: Term structure anomaly > 2σ. Contango for short, backwardation for long.
│  ├─ VIX Options/Futures (§6) → Vol of vol. Tactical only.
│  │  └─ Gate: VVIX signal. < 3 day hold for long futures. Kill switch for short.
│  └─ Correlation Trading (§8) → Pair correlation. Sector correlation. Dispersion.
│     └─ Gate: Realized correlation < 0.60. Exit if rising rapidly.
│
└─ Risk Management (MANDATORY)
   ├─ Vega neutrality daily? Rebalance if vega drifts > 10%.
   ├─ Correlation risk? Close if corr exceeds threshold.
   ├─ Gap risk? Earnings blackout active?
   ├─ Regime shift? Term structure inverted? VIX spike?
   └─ Drawdown? -10% reduce, -20% close vol arb book.
```

## Core Workflow

### Phase 1: Regime Assessment (Daily, Pre-Market)

1. Check VIX level + VIX percentile (1-year lookback)
2. Check VIX futures term structure (contango %)
3. Check VVIX (vol of vol)
4. Check SPX 20-day realized vol
5. Determine regime: Low / Normal / High
6. Set sizing multiplier: 1.0 / 0.8 / 0.4 (or 0)

### Phase 2: Signal Generation (Daily)

1. VRP signal: IV - RV spread across SPX + liquid ETFs
2. Dispersion signal: Implied correlation vs realized correlation for SPX constituents
3. Skew signal: 25-delta put IV vs 25-delta call IV for each underlying
4. Term structure signal: Calendar spread pricing anomalies
5. VIX signal: VVIX percentile, VIX futures curve shape
6. Pair correlation signal: IV spread divergence for correlated pairs

### Phase 3: Position Construction

1. Select strategy based on regime + strongest signal
2. Size according to regime multiplier + Kelly fraction
3. Construct to be vega-neutral (or intentional vega exposure with defined risk)
4. Verify gamma profile: negative gamma = risk. Positive gamma = cost.
5. Document every position: thesis, edge, risk, exit conditions

### Phase 4: Monitoring & Exit

1. Daily vega reconciliation — rebalance if drift > 10%
2. Daily correlation check — exit if exceeded threshold
3. Real-time regime monitoring — instant exit on regime shift
4. Profit targets: specific to each strategy type
5. Hard stops: specific to each strategy type

## Strategy Deep Dives

### 1. Dispersion Trading

> **Reference:** dispersion-trading-math.md

Index IV vs weighted constituent IV. Implied correlation vs realized. Trade construction: vega-neutral long/short dispersion. 20+ names minimum. $250K+ account minimum.

### 2. Variance Risk Premium Harvesting

> **Reference:** variance-risk-premium.md

VRP decomposition: IV² - RV². Historical: 3-5 vol point premium. Strategies: short strangles, ratio spreads, variance swaps (institutional). Calendar effects: pre-FOMC expansion, post-FOMC collapse. Tail risk: 2020-type events.

### 3. Skew & Term Structure Arbitrage

> **Reference:** skew-and-term-structure-arbitrage.md

Skew: put IV premium over call IV. Risk reversals. Skew ratio put/call spread credit. Term structure: calendar spreads on vol. VIX futures curve. Contango (80% of time) vs backwardation (20%).

### 4. VIX Products

> **Reference:** vix-products-guide.md

VIX spot (untradeable) vs VIX futures vs VIX options. VVIX (vol of vol, typically 80-110). VIX ETNs: VXX, UVXY, SVXY. Contango roll decay (5-10%/mo). Golden rule: never long > 3 days, never short without kill switch.

### 5. Volatility Regime Detection

> **Reference:** vol-regime-detection.md

3 regimes: Low (VIX < 15) / Normal (15-22) / High (> 25). Multi-factor scoring: VIX level, VIX percentile, term structure, realized vol, VVIX. Strategy matrix per regime. Transition detection.

### 6. Correlation Trading

> **Reference:** correlation-trading.md

Implied vs realized correlation. Pair correlation. Sector correlation norms. Correlation swap (institutional). The correlation → 1.0 problem in crashes. Sizing: 5% per trade, 15% total correlation book.

## Research Prerequisites

**RP1 (VOL REGIME):** VIX level, VIX percentile, term structure, SPX realized vol, VVIX. Updated daily.

**RP2 (VRP SIGNAL):** IV vs RV spread across target underlyings. Minimum 1-year history for statistical significance.

**RP3 (DISPERSION SIGNAL):** Implied correlation computed from SPX + top-50 constituent options. Compare to 2-year historical correlation.

**RP4 (SKEW SIGNAL):** 25-delta put IV / 25-delta call IV for each target. z-score vs 1-year history.

**RP5 (TERM STRUCTURE):** VIX futures curve. Calendar spread pricing on target underlyings.

**RP6 (VVIX):** VIX options IV. Percentile vs 1-year history. VIX futures term structure.

**RP7 (CORRELATION MATRIX):** Pairwise realized correlation for all position underlyings. Updated weekly.

**RP8 (EARNINGS CALENDAR):** Any single-stock earnings in the vol arb book within 2 weeks.

## Error Decoder

| # | Symptom | Root Cause | Exact Fix | Lesson |
|---|---------|-----------|-----------|--------|
| E1 | "Dispersion trade lost 15% in a week despite vega neutrality" | Correlation spike. Implied correlation → 1.0 during market stress. Short correlation position crushed | Close dispersion trade when realized correlation exceeds implied + 0.15. Correlation is the dominant risk, not vega | Vega neutrality gives false comfort. In vol arb, correlation is the silent killer |
| E2 | "Short VIX futures position lost 40% in 3 days. VIX went from 18 to 32" | No kill switch. VIX spike was preceded by 3 days of term structure flattening | Implement hard VIX-level exit: VIX > 25: close 50%; VIX > 30: close 100%. Term structure inversion = pre-close now | Shorting vol without a mechanical exit is gambling. The exit must fire before you can talk yourself out of it |
| E3 | "Short strangles profitable for 11 months, then lost 2 years of profits in March 2020" | Position sizing didn't scale down as VIX rose. Full size at VIX 22 is not the same as full size at VIX 14 | Scale position size inversely with VIX: full at VIX < 15, half at 20, zero > 25. This is the ONLY way to survive vol events | VRP strategies have positive expectancy long-term but negative skew. Sizing must account for the 100-year flood that happens every 5 years |
| E4 | "Bought VIX calls as a hedge — VIX went up but the calls barely moved" | VIX call IV (VVIX) was already elevated when bought. The vol spike was priced in | Check VVIX before buying VIX options. If VVIX > 120, the move you're hedging is already partially priced. Use VIX futures for clean delta exposure | Options on an already-expensive vol index have limited upside. You're paying vol-of-vol premium |
| E5 | "Dispersion basket: short 8 names. One had an M&A rumor — stock jumped 25%. Single-name loss > all other profits combined" | Single-name concentration. 12.5% vega in one name. No M&A screen | Maximum 8% vega per name. Screen for M&A targets, earnings, FDA decisions, regulatory events before basket construction | One idiosyncratic event on a concentrated short-vega position is a portfolio killer |
| E6 | "Skew arbitrage: sold expensive SPX puts because skew was 3σ above normal. Market dropped 8% in 2 days" | Skew was expensive for a reason. The market was pricing legitimate downside risk. Buying expensive insurance ≠ bad trade when the house burns down | Never be net short puts during: VIX > 25, market < 200SMA, Fed days, geopolitical events. Skew is the market's fear gauge — respect it | "Statistically cheap" and "should revert" are not the same thing. Skew can stay expensive until the event it's pricing occurs |
| E7 | "Vol arb book was 12 positions. All closed within 48 hours because one regime signal was missed" | Regime detection was manual. Trader was busy and didn't check VIX term structure for 3 days | Automate regime detection. Daily push notification: VIX, VIX percentile, term structure, VVIX. Regime shift = automated alert + pause on new entries | If regime detection isn't automated, it doesn't exist. The cost of automation is trivial vs the cost of missing a regime shift |

## Anti-Hallucination

**[VERIFIED]** — CBOE VIX methodology, VIX futures/options specifications, exchange rules, academic research on VRP (Bollerslev, Todorov, et al.).
**[COMPUTED]** — Implied correlation, VRP decomposition, vega calculations with stated model assumptions.
**[ESTIMATED]** — Contango roll costs (vary with curve shape), dispersion execution costs (vary with name count).
**[COMMON-PRACTICE]** — Institutional vol arb desk practices. Not codified in any single source.
**[BACKTEST-EVIDENCE]** — Where available. Vol arb backtests are challenging due to options data costs and survivorship bias.

**Vol arb backtests are noisy.** The sample size of major vol events (VIX > 40) is small (~10-15 events in modern history). Statistical confidence in tail risk estimates is low by definition. This is why regime-based risk management (knee-jerk exit on regime shift) is more reliable than model-based risk management (VaR, expected shortfall).

## Cross-Skill Coordination

### Upstream

| Skill | What to Request | Decision Gate |
|-------|----------------|---------------|
| `quantitative-analyst` | IV/RV analytics, correlation matrices, VRP decomposition, skew metrics | Is the statistical edge significant? |
| `options-risk-engineer` | Vega/gamma/charm/vanna profiles, stress scenarios, correlation risk | Does the risk framework handle vol arb's unique risks? |
| `macro-strategist` | Rate expectations, economic cycle, VIX regime outlook | Is the macro environment supportive of vol arb? |
| `options-strategist` | Strategy structure validation, Greek verification, execution feasibility | Can the strategy be constructed with available instruments? |

### Downstream

| Skill | When to Hand Off | Handoff Format |
|-------|-----------------|----------------|
| `algorithmic-trader` | Vol arb strategy ready for systematic execution | "Vol arb strategy: [type], [signal], [instruments], [sizing_rules], [exit_rules]" |
| `portfolio-signal-manager` | Vol arb positions needed in portfolio context | "Vol position: [notional], [vega], [gamma], [correlation_to_portfolio], [regime_dependence]" |
| `advanced-options-structures` | Vol arb requires advanced structures (box spreads, synthetics, ratio diagonals) | "Structure requirement: [purpose], [vol_profile], [capital_constraint]" |

## What Good Looks Like

**Systematic VRP Harvesting (GOOD):** Short 0.15-delta SPX strangles, 30 DTE, managed at 50% profit. Regime detection automated. Size: 100% at VIX < 15, 50% at VIX 15-20, 25% at VIX 20-25, 0% at VIX > 25. Term structure inversion = instant close. Result: 12-month Sharpe 1.3, max drawdown -12%, fully closed before March 2020 (-50% for those who didn't), fully closed before Aug 2024 vol event.

**Dispersion Trade (GOOD):** SPX IV = 19%, weighted top-20 IV = 16.5%. Implied correlation = 0.55 vs realized = 0.35. Signal: z-score > 2.0. Short SPX straddle, long 20 single-stock straddles, vega-neutral. Sizing: 5% of account. Correlation stop at 0.50 realized. Result: Held 3 weeks. Correlation mean-reverted. +3.2% on capital. Annualized: similar trades produce +8-12% gross.

**Regime Shift Avoided (GOOD):** VIX term structure flattened then inverted over 3 days. VIX rose 18 → 23 → 28. Automated regime detection flagged. All short-vol positions closed within 2 hours of backwardation signal. Result: Sat in cash for 8 days while VIX spiked to 35, then normalized. Re-entered at VIX 20 with term structure in contango. Avoided -22% drawdown that competitors experienced.

## Operating at Different Levels

| Level | Scope | Key Capability |
|-------|-------|----------------|
| **L1: Apprentice** | Understand VRP concept. Execute defined-risk credit spreads with vol-awareness | Knows: VIX, contango/backwardation, IV vs RV. Doesn't run vol arb independently |
| **L2: Practitioner** | Run simple VRP strategies (short strangles with regime rules). Execute dispersion on SPX only | Adds: Systematic VRP with regime sizing, basic dispersion, VIX product mechanics |
| **L3: Specialist** | Multi-strategy vol arb book: VRP + skew + term structure + basic dispersion. Automated regime detection | Adds: Skew arb, term structure arb, multi-name dispersion, automated risk |
| **L4: Architect** | Institutional vol arb operation. Correlation trading, variance swaps, cross-asset vol arb, options market-making patterns | Adds: Correlation trading, OTC products, cross-asset, market microstructure |
| **L5: Transformative** | Publish vol arb research. Design vol indices. Create vol arb frameworks used by the industry | Adds: Research, index design, framework creation |

## Anti-Patterns

| ❌ Common Mistake | ✅ Correct Approach |
|-------------------|-------------------|
| "The vol surface model says these options are 2σ mispriced — it's a sure thing" | Models are wrong during stress. Always check: is the "mispricing" actually the market correctly pricing a risk the model doesn't capture? |
| "VIX is at 12 — I'll put on maximum short-vol size because vol can't go lower" | Lowest VIX precedes highest vol spikes. 2017 VIX averaged 11 → Feb 2018 VIX spiked to 50. Maximum allocation at minimum VIX is how vol funds blow up |
| "I'll just sell the front-month strangle and roll it forever — it's free money" | Every vol seller who thought this way has either blown up or will. The premium exists BECAUSE selling vol occasionally causes catastrophic losses |
| "The dispersion signal is 2.5σ — I'll size this bigger than usual" | Extreme signals often precede regime shifts. When the signal is strongest, the risk of structural break is highest. Size DOWN on extreme signals |
| "I'll hedge the vol arb book with SPY puts" | SPY puts hedge delta, not vol-of-vol or correlation. The hedge you need is VIX calls or VIX futures — direct vol instruments. Equity hedges fail when vol arb fails |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Vol arb book has 12 positions diversified across strategies — but one missed regime shift (VIX term structure inversion → VIX spikes to 35) makes all positions correlated at 0.85+ simultaneously | $50K-$200K in a single vol event — dispersion, VRP, and skew trades all blow up together because correlation → 1.0 in stress | Automate regime detection with daily push notifications. Term structure inversion = close all short vol within 24 hours. No exceptions. The cost of automation ($0) is trivial vs the cost of missing a regime shift |
| "VIX at 12 — vol can't go lower, I'll max out short-vol allocation." Then Feb 2018: VIX goes from 11 to 50, short vol funds down 90%+ in a week | $100K-$1M+ for institutional vol sellers — maximum allocation at minimum VIX is the #1 cause of vol fund blow-ups | Scale allocation inversely with VIX: full at VIX < 15, half at VIX 20-25, zero at VIX > 25. Low VIX doesn't mean safe — it means the compression before the spike |
| VIX call bought as vol spike hedge, but VVIX was 135 at purchase — the vol spike was already priced into the option premium. VIX rises 10 points, call barely moves | $5K-$15K in wasted hedge cost — the hedge that was supposed to protect the portfolio does nothing when it's needed | Check VVIX before buying VIX options. If VVIX > 120, the move is partially priced in. Use VIX futures for clean delta exposure instead |
| Dispersion basket: 12 names, but one name at 15% of total vega. An M&A rumor sends the stock +25%. Single-name loss exceeds profits from all 11 other names combined | $30K-$100K in single-name blow-up — concentration risk is lethal when you're short single-stock vol | Maximum 8% vega per name. Minimum 20 stocks in basket. Screen for M&A targets, earnings, FDA decisions, regulatory events before basket construction |
| Skew arbitrage: "SPX puts are 3σ expensive vs historical skew — sell them." The market was pricing a legitimate event; skew stayed expensive for 2 more weeks, then the event materialized. Loss: -40% | $20K-$80K — "statistically cheap" and "should revert" are different things. Skew doesn't revert on your schedule | Never be net short puts during VIX > 25, market < 200SMA, FOMC days, or geopolitical events. Skew is the market's fear gauge — respect it. "Expensive" skew usually has a reason |
| VRP harvesting: short strangles profitable for 14 months straight. Sizing gets bigger because "the strategy works." Then a vol event wipes 2+ years of profits in 3 weeks | $100K-$500K at institutional scale — procyclical sizing (increasing when winning) is the silent portfolio killer for vol sellers | Fixed sizing regardless of streak length. Sizing should DECREASE when volatility is low (because the next spike is closer), never increase due to recent profitability. Half-Kelly as ceiling |
| VIX futures short position has a mental stop ("I'll exit if VIX goes above 30") but no mechanical kill switch in the system. VIX hits 35 overnight. Mental stop becomes rationalization to hold | $10K-$50K per incident — mechanical exit must fire BEFORE you can talk yourself out of it | Hard-code kill switch: VIX > 28 → close 50%. VIX > 35 → close 100%. This is code, not a note in a trading journal. The one vol spike you don't exit costs more than years of roll yield |

## Production Checklist

Before ANY vol arb position:

- [ ] 1. **Regime determined:** Low / Normal / High. Sizing multiplier applied.
- [ ] 2. **VIX term structure checked:** Contango or backwardation? Any short-vol positions if backwardated?
- [ ] 3. **Signal z-score calculated:** Minimum 2.0σ for dispersion/skew/term structure trades.
- [ ] 4. **Vega computed at inception:** Total position vega. Intentional exposure or vega-neutral?
- [ ] 5. **Gamma profile understood:** Negative gamma = acceleration on adverse moves. Positive gamma = cost.
- [ ] 6. **Correlation risk assessed:** For dispersion/correlation trades. Stop levels set.
- [ ] 7. **Single-name concentration checked:** No name > 8% of total vega. No earnings within 2 weeks.
- [ ] 8. **VIX exit levels set:** Short vol: VIX > 25 → reduce, VIX > 30 → close all. VIX futures short: hard kill switch.
- [ ] 9. **Drawdown circuit breakers set:** -10% book drawdown → review. -20% → close vol arb book.
- [ ] 10. **Term structure inversion protocol:** Automated alert + 24-hour close deadline on all short vol.
- [ ] 11. **Daily monitoring plan:** Regime check daily. Correlation check daily. Vega reconciliation daily.
- [ ] 12. **Tail hedge in place:** For VRP strategies: 1-2% of book value in OTM VIX calls or SPX puts.
- [ ] 13. **Liquidity verified:** All instruments tradeable. Exit possible even during vol events.
- [ ] 14. **Counterparty risk assessed:** For OTC products: ISDA, CSA, collateral terms.
- [ ] 15. **Journal entry:** Trade thesis, edge quantification, risk limits, exit conditions documented.

## References

| Reference | Covers | When to Read |
|-----------|--------|-------------|
| `dispersion-trading-math.md` | Index vs constituent vol, implied correlation, trade construction, risk management | Before any dispersion trade |
| `variance-risk-premium.md` | VRP decomposition, short strangle/strategy design, calendar effects, tail risk | Before systematic premium selling |
| `skew-and-term-structure-arbitrage.md` | Risk reversals, skew ratios, calendar spreads, VIX futures curve | For relative value vol trades |
| `vix-products-guide.md` | VIX futures, VIX options, VVIX, ETNs, contango decay, strategy matrix | Before trading any VIX product |
| `vol-regime-detection.md` | 3-regime classification, multi-factor scoring, transition detection, strategy matrix | DAILY — before any vol trading |
| `correlation-trading.md` | Implied vs realized correlation, pair/sector/dispersion correlation, crash dynamics | For correlation-based strategies |
| `black-swan-protection-for-vol-arb.md` | Tail hedging, convexity protection, circuit breakers for vol events, correlation collapse math | MUST READ — vol arb without tail protection is not arbitrage |
| `vol-arb-backtesting-methodology.md` | Path-by-path distribution, intraday sampling, regime-segmented testing, walk-forward validation | Before deploying ANY vol arb strategy to production |

**Cross-reference skills:** `quantitative-analyst` (math/models), `options-risk-engineer` (risk frameworks), `macro-strategist` (regime context), `algorithmic-trader` (systematic execution).

---

*Skill complete. Vol arb is the highest-risk/highest-sophistication domain in options. The edge is real but small. The risk is real and large. Regime detection, position sizing, and discipline are everything.*
