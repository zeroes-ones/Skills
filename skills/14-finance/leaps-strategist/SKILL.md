---
name: leaps-strategist
description: >
  Use when the user wants to replace stock holdings with LEAPS for capital efficiency,
  design Poor Man's Covered Call (PMCC) setups, hedge portfolios with long-dated puts,
  trade LEAPS diagonals or calendars, implement dividend-aware LEAPS strategies, or
  analyze rho sensitivity for long-dated options in changing rate environments. Use when
  the user asks "LEAPS vs stock," "PMCC optimization," "long-dated hedging," or "best
  LEAPS strike selection." Handles LEAPS stock replacement valuation, PMCC ratio and
  strike optimization, multi-cycle LEAPS management (rolling, scaling), long-dated
  hedging with dividend-aware adjustments, rho-dominant risk modeling, and tax-aware
  LEAPS lifecycle planning. Do NOT use for standard 30-60 DTE strategies (route to
  options-strategist), intraday LEAPS trading (route to intraday-options-trader),
  swing-term 2-30 day trades (route to swing-options-trader), or advanced multi-leg
  LEAPS structures (route to advanced-options-structures).
license: MIT
tags:
  - LEAPS
  - long-dated-options
  - PMCC
  - stock-replacement
  - rho-sensitivity
  - dividend-strategies
  - hedging
  - capital-efficiency
chain:
  consumes_from: [fundamental-analyst, quantitative-analyst, options-strategist, swing-options-trader, options-risk-engineer]
  feeds_into: [options-risk-engineer, portfolio-signal-manager, algorithmic-trader, swing-options-trader]
version: 1.0.0
status: active
author: Skills Library
created: "2026-07-16"
category: "14-finance"
token_budget: 4000
---

# LEAPS Strategist

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).
> No vendor-specific frontmatter fields.

<!-- STANDARD: 3min -->
## Route the Request

| User Intent | Route To | Decision Gate |
|-------------|----------|---------------|
| "Replace stock with LEAPS" / "LEAPS instead of shares" | → Stock Replacement Workflow (§3) | Stock must have LEAPS available (∼2,500 tickers) |
| "PMCC" / "Poor Man's Covered Call" / "covered call on LEAPS" | → PMCC Workflow (§4) | Short strike > LEAPS strike required |
| "Hedge portfolio with LEAPS" / "long-dated protection" | → Hedging Workflow (§5) | IV rank < 30% at entry |
| "LEAPS calendar" / "double LEAPS diagonal" | → Multi-Cycle Workflow (§6) | Liquidity check: OI > 100 on all legs |
| "Dividend strategy with LEAPS" / "LEAPS on dividend stocks" | → Dividend Workflow (§7) | Dividend yield gate (§7.1) |
| "Rho impact on LEAPS" / "rate sensitivity" | → Rho Analysis (§8) | Rate path assumption must be explicit |
| "Tax-loss harvest LEAPS" / "LEAPS tax treatment" | → Tax Considerations (§9) | Consult CPA — this skill provides framework only |
| "Trade LEAPS earnings" / "LEAPS through events" | → LEAPS Event Playbook (§10) | Earnings blackout gate: close short legs before earnings |
| "LEAPS roll strategy" / "when to roll LEAPS" | → LEAPS Rolling (§11) | DTE < 90: roll or close decision |
| "Which LEAPS to buy" / "LEAPS strike selection" | → Strike Selection (§3.1) | Always check extrinsic % and annualized cost |

## 10 Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE LEAPS stock replacement when extrinsic > 4%. Extrinsic above 4% means the annualized "rent" on leverage exceeds margin rates | Trigger: `grep "extrinsic_pct" leaps_screener` → `extrinsic_pct > 4` AND `strategy = "stock_replacement"` | STOP. "Extrinsic > 4% on stock-replacement LEAPS. Annualized cost exceeds margin rate. Go deeper ITM (0.85+ delta) or find different ticker." |
| R2 | REFUSE PMCC when short strike < LEAPS strike. This creates guaranteed loss on assignment: (short_K − LEAPS_K) × 100 + lost time premium | Trigger: `PMCC_short_strike < PMCC_long_strike` in trade plan | STOP. "PMCC short strike below LEAPS strike. Guaranteed loss on assignment. Raise short strike above LEAPS strike or reject trade." |
| R3 | REFUSE to buy LEAPS puts for hedging when IV rank > 50%. Buying long-dated insurance at elevated vol locks in high premiums for years | Trigger: `grep "leaps_put.*hedge" trade_plan` → `IV_rank > 50` | STOP. "IV rank > 50% on hedging LEAPS put. Wait for IV rank < 30% or dollar-cost average over 3 entries. Your 2-year premium is 40-60% above fair value." |
| R4 | REFUSE LEAPS stock replacement on dividend yield > 4% without quantifying the gap. Over 2 years, 8%+ of notional lost to missed dividends | Trigger: `dividend_yield > 4 AND strategy = "leaps_stock_replacement"` AND no dividend-gap analysis | STOP. "Dividend yield > 4% on LEAPS stock replacement. Calculate 2-year dividend gap vs LEAPS savings. Usually -EV. Consider selling puts instead or pick lower-yield ticker." |
| R5 | REFUSE PMCC when LEAPS DTE < 180. Insufficient time to amortize LEAPS extrinsic through premium cycles | Trigger: `DTE < 180 AND strategy = "PMCC"` in trade plan | STOP. "LEAPS DTE < 180 for PMCC entry. Cannot amortize extrinsic in under 6 months. Minimum 365 DTE; 540+ DTE ideal for multi-cycle premium capture." |
| R6 | REFUSE to continue PMCC after 2+ cycles of debit rolls. Repeated debit rolling ("death by a thousand rolls") silently erodes 40%+ of initial capital | Trigger: `roll_count ≥ 2 AND roll_type = "debit" AND position_P&L < 0` | STOP. "PMCC has 2+ debit roll cycles. Death by a thousand rolls — positions rolled 3+ times underperform by -40% cumulative. Close position and re-evaluate thesis." |
| R7 | REFUSE rho exposure > 10% of max profit without hedging. For 18-month LEAPS, a 2% rate move swings P&L by ±$500+ on 10-contract positions | Trigger: `rho × expected_rate_change × position_size > 0.10 × max_profit` AND no rho_hedge | STOP. "Rho risk exceeds 10% of max profit unhedged. A 2% rate move costs ±$500 per 10 contracts. Add rate hedge or reduce size to bring rho within profit buffer." |
| R8 | REFUSE to hold PMCC short calls through ex-dividend when ITM/ATM. Rational call holders exercise ITM calls before ex-dividend — forced LEAPS exercise loses remaining time premium | Trigger: `short_call.ITM_or_ATM AND ex_div_date ≤ DTE AND strategy = "PMCC"` | STOP. "PMCC short call faces ex-dividend assignment. Cost: lost remaining LEAPS time premium ($300-$800 per contract). Close or roll short call before ex-div date." |
| R9 | REFUSE directional LEAPS trades with asymmetric exit ratio < 2:1. 1:1 RR at 50% WR = -5% expectancy after spreads | Trigger: `max_profit / max_loss < 2 AND strategy = "directional_leaps"` | STOP. "Exit ratio < 2:1. At 50% win rate with 1:1 RR, expectancy = -5% after spread costs. Define entry, profit target, stop loss, AND time stop that collectively achieve ≥ 2:1." |
| R10 | REFUSE LEAPS entry when trend_score < threshold AND HV percentile > 70. Low trend + high vol = poor LEAPS environment where time decay fights a losing directional battle | Trigger: `trend_score < 30 AND HV_percentile > 70 AND strategy = "LEAPS"` | STOP. "Unfavorable LEAPS environment: trend_score < 30 + HV > 70th percentile. Low conviction meets high noise. Wait for trend_score > 50 or HV < 50th percentile." |

## Decision Tree

```
LEAPS request received
│
├─ Replace stock with LEAPS?
│  ├─ Dividend yield > 4%? → YES → Quantify gap. Usually -EV. Consider selling puts instead. (§3, §7)
│  ├─ Extrinsic < 4%? → YES → Calculate annualized cost. Proceed if < margin rate. (§3.2)
│  └─ Extrinsic ≥ 4%? → Go deeper ITM or wait for pullback. (§3.1)
│
├─ PMCC (Poor Man's Covered Call)?
│  ├─ LEAPS DTE ≥ 365? → NO → REJECT. Not enough cycles. (§4.1)
│  ├─ Short K > Long K? → NO → REJECT. Guaranteed loss on assignment. (§4.2)
│  ├─ Short Δ ≤ 0.30? → NO → Too aggressive. Assign risk too high. (§4.3)
│  ├─ Ex-div within short DTE and short ITM? → YES → Close short before ex-div. (§7.5)
│  └─ → EXECUTE PMCC. Monthly premium target: 1.0-1.5% of LEAPS cost. (§4)
│
├─ Hedge with LEAPS?
│  ├─ IV rank > 50%? → YES → DELAY. Expensive insurance. (§5.2)
│  ├─ Tail hedge (deep OTM)? → Allocate 2-5% of portfolio/year. (§5.4)
│  ├─ Full protection (ATM puts)? → Quantify cost vs. expected drawdown. (§5.3)
│  └─ → SELECT strikes and ladder if needed. (§5.5)
│
├─ Double LEAPS Calendar / Diagonal?
│  ├─ All legs OI > 100? → NO → REJECT. Illiquid LEAPS are untradable. (§6.1)
│  ├─ Delta-neutral? → Confirm net Δ ≈ 0. (§6.2)
│  └─ Vega-positive in low IV? → YES → Proceed. (§6.3)
│
├─ Rho analysis needed?
│  ├─ DTE > 180? → YES → Compute rho impact. (§8)
│  └─ → Factor rate path into strategy selection. (§8.3)
│
└─ Rolling / Exiting LEAPS?
   ├─ DTE < 90? → DECIDE: roll up/out or close. (§11)
   ├─ LEAPS at 0.95+ delta? → Take profits or roll up to reset delta. (§11.2)
   └─ Tax-loss harvest opportunity? → Consider: sell for loss, buy similar but not identical replacement. (§9)
```

## Core Workflow

### Phase 1: LEAPS Feasibility Assessment (15 min)

1. **Check LEAPS availability:** Not all stocks have LEAPS. Verify on your broker's option chain. [VERIFIED: ~2,500 stocks/ETFs have LEAPS]
2. **Liquidity check:** Open interest > 100 on target strike. Bid-ask spread < 5% of option price.
3. **Dividend assessment:** Compute yield. Apply GR4 if > 4%.
4. **Extrinsic analysis:** For stock replacement, compute extrinsic_pct and annualized cost (ref: stock-replacement-math.md).
5. **Rate environment:** Note current Fed funds rate, expected rate path over LEAPS life. Factor rho (ref: rho-and-rates-sensitivity.md).
6. **IV environment:** Check IV rank/percentile. Apply GR3 for puts, GR3 analog for calls.

### Phase 2: Strategy Construction (20 min)

1. **Select LEAPS structure** based on objective (stock replacement, income, hedging, etc.).
2. **Strike selection:** Use DITM for stock replacement (Δ ≥ 0.80). ATFM for PMCC long leg. OTM for hedges.
3. **DTE selection:** Minimum 365 for PMCC. 540+ preferred. For stock replacement, 365-730.
4. **Sizing:** Apply volatility-adjusted sizing: `size = 1.5 - (hv%/100) × 1.1` clipped [0.3, 1.5] [BACKTEST-EVIDENCE].
5. **Exit plan:** Define target (e.g., LEAPS at 0.95Δ → take profit). Define stop (e.g., LEAPS extrinsic exceeds 10% → close).

### Phase 3: Execution & Monitoring (10 min + ongoing)

1. **Enter with limit orders.** LEAPS spreads are wider than near-dated. Use mid ± 2%.
2. **Document entry:** Strike, DTE, delta, extrinsic %, planned exit, rho exposure.
3. **Monthly review:** Check LEAPS delta drift, rho impact, IV changes, dividend calendar.
4. **PMCC cycle management:** Review short call weekly. Roll at 50% profit or 7 DTE (whichever first).

### Phase 4: Exit & Post-Mortem (10 min)

1. **Exit triggers:** DTE < 90 (roll or close), Δ > 0.95 (profit target), extrinsic > acceptable threshold, thesis invalidated.
2. **Journal trade:** Entry thesis, actual outcome, rho contribution, dividend impact, lessons.
3. **Cross-reference:** Feed exit data to `trade-performance-analyst` for pattern detection.

## Strategy Deep Dives

### 1. LEAPS Stock Replacement

> **Reference:** stock-replacement-math.md

Replace 100 shares with 1 DITM LEAPS call. Capital efficiency: 60-80% savings. Risk: defined at premium paid. Cost: extrinsic premium + missed dividends - interest on saved capital.

**When it wins:** Bullish multi-year view, limited capital, want leverage without margin calls, don't need dividends.
**When it loses:** Sideways market (extrinsic bleeds), high dividend stocks, falling rate environment (rho headwind).

### 2. PMCC (Poor Man's Covered Call)

> **Reference:** pmcc-optimization.md

LEAPS diagonal where the DITM LEAPS call backs near-dated short calls. Monthly premium offsets LEAPS extrinsic + dividend gap.

**Strike hierarchy:** SHORT > LONG. Always. Non-negotiable.
**DTE sweet spot:** 30-45 DTE for short calls. 365+ for LEAPS.
**Roll cadence:** At 50% profit OR 7 DTE. Never let ITM short call approach ex-div.

### 3. LEAPS Protective Puts & Hedging

> **Reference:** leaps-hedging-and-insurance.md

LEAPS puts for long-dated portfolio insurance. Cheaper on annualized basis than rolling monthly puts. Critical: buy when IV rank < 30%.

**Tail hedging:** 2-5% of portfolio/year in deep OTM LEAPS puts. They expire worthless 90%+ of time but pay 10-50x in crashes.
**Collars:** Sell LEAPS calls to finance LEAPS puts. Zero-cost or credit. Accept the upside cap.

### 4. LEAPS Diagonals & Double Calendars

> **Reference:** leaps-diagonals-and-calendars.md

Multi-cycle premium harvesting. One LEAPS call backs 8-24 cycles of near-dated shorts. Double calendars: delta-neutral, vega-positive premium harvesting.

### 5. Dividend-Aware LEAPS

> **Reference:** dividend-strategies-with-leaps.md

Quantify the dividend gap. For high-yield stocks: sell LEAPS puts instead of buying LEAPS calls. PMCC premium must exceed dividend gap. Close ITM short calls before ex-div.

### 6. Rho Management

> **Reference:** rho-and-rates-sensitivity.md

LEAPS rho is 3-5x short-dated options. For 18-month LEAPS, 1% rate change = ±$40-50/contract for DITM options. Factor the expected rate path into strategy selection.

## Research Prerequisites

**RP1 (QUANTITATIVE):** Compute extrinsic_pct and annualized extrinsic cost for the target LEAPS strike. Compare to the risk-free rate and margin rates.

**RP2 (MARKET CONTEXT):** Check IV rank/percentile for the underlying. Is this a favorable entry environment for the strategy type (buying vs. selling premium)?

**RP3 (DIVIDEND CALENDAR):** For any strategy involving short calls, check all ex-dividend dates within the short leg's DTE. Identify assignment risk windows.

**RP4 (RATE PATH):** What is the market-implied rate path over the LEAPS' life? Quantify rho impact under bull, base, and bear rate scenarios.

**RP5 (LIQUIDITY):** Verify open interest > 100 on the target LEAPS strike. Check bid-ask spread as % of option price. Reject if spread > 10%.

**RP6 (TICKER CALIBRATION):** For directional LEAPS, check trend_score, HV percentile, and LEAPS-specific performance data. [BACKTEST-EVIDENCE] Not all tickers work for LEAPS.

**RP7 (CORRELATION DECAY):** For LEAPS hedges on a basket, verify that index LEAPS actually correlate with your holdings. Single-stock LEAPS hedges don't protect against broad market crashes.

**RP8 (TAX ANALYSIS):** LEAPS held > 1 year qualify for LTCG. But LEAPS vs. stock tax treatment differs beyond just holding period. Consult a CPA.

## Error Decoder

| # | Symptom | Root Cause | Exact Fix | Lesson |
|---|---------|-----------|-----------|--------|
| E1 | "PMCC showing guaranteed loss on assignment calculation" | Short call strike < LEAPS strike | Roll short call UP to K > LEAPS_K. Never enter PMCC with short_K ≤ long_K | The strike hierarchy is the PMCC prime directive — check before EVERY short call sale |
| E2 | "LEAPS lost 30% but stock only dropped 15%" | DITM LEAPS delta < 0.85 at entry; extrinsic inflated the premium above intrinsic | Check delta at entry. ≥0.80 minimum. Extrinsic < 4%. The LEAPS should track stock within 10-15% | "Cheap" LEAPS (higher strike) have more extrinsic → worse stock tracking. Pay up for the DITM strike |
| E3 | "Assigned on short call, broker exercised LEAPS, lost $3,000 in time premium" | Short call ITM at expiration OR before ex-dividend. No roll before deadline | Roll at 7 DTE minimum if short call is ATM or ITM. If ex-div within DTE and call is ITM → close immediately | Time premium loss on forced LEAPS exercise is the silent PMCC killer. Always monitor DTE and ex-div |
| E4 | "LEAPS put hedge cost more than the drawdown it protected against" | Bought LEAPS puts when IV rank > 50%. Overpaid for insurance by 30-50% | Never buy LEAPS puts when IV rank > 30%. Wait for vol compression or ladder in during low-vol regimes | Long-dated insurance is only valuable if bought cheap. Overpaying for years of protection defeats the purpose |
| E5 | "PMCC premium collected: 0.4%/month → 4.8%/year → barely above risk-free rate after dividend gap" | Short call delta too conservative (0.10). Premium too low to offset extrinsic + dividend gap | Target 0.20-0.30 delta for short calls. If premium < 0.8%/month of LEAPS cost → the PMCC is -EV after extrinsic + dividends | PMCC needs to earn its keep. 1.0-1.5% monthly ROC is the target. Below 0.8% → use a different structure |
| E6 | "LEAPS DTE at 120, but I need 12 more months of premium → forced to roll LEAPS at a bad time" | Entered PMCC with LEAPS DTE < 365. Not enough cycles to amortize extrinsic | Minimum 365 DTE at PMCC entry. Plan for the remaining LEAPS life at each short call expiration | PMCC is a marathon, not a sprint. The LEAPS needs runway |
| E7 | "Interest rate cut caused LEAPS call to lose 5% despite stock being flat" | Ignored rho impact. 2% rate cut on 18-month 0.85Δ LEAPS = ~-$80-100/contract from rho alone | Compute rho exposure at entry. In a cutting cycle, favor LEAPS puts or neutral structures. Size for the rate scenario | Rho is a first-order Greek for LEAPS. Don't ignore it |

## Anti-Hallucination

Every claim in this skill must be tagged from one of five confidence levels:

**[VERIFIED]** — Confirmed via CBOE/OCC specifications, published academic research, or broker documentation.
**[COMPUTED]** — Calculated using Black-Scholes or other standard models with stated assumptions.
**[ESTIMATED]** — Ranges based on practitioner experience with explanation of uncertainty.
**[COMMON-PRACTICE]** — Widely used by professional options traders but not codified in exchange rules or academic literature.
**[BACKTEST-EVIDENCE]** — Inferred from the companion Trading project's 1,068-trade backtest across 11 tickers.

**When modeling LEAPS:** Always state your assumptions (IV, r, div yield, DTE). LEAPS Greeks are computed, not observed — they're model-dependent. Different models (Black-Scholes, binomial, stochastic vol) give different Greeks for long-dated options.

**When quoting rho:** Rho in Black-Scholes assumes parallel shifts in the yield curve. Real-world rate changes are non-parallel. Rho is directional, not precise.

## Cross-Skill Coordination

### Upstream (Consumes From)

| Skill | What to Request | Decision Gate |
|-------|----------------|---------------|
| `fundamental-analyst` | Multi-year business outlook, competitive moat, revenue growth trajectory | Is this company still investable in 2-3 years? If no → don't LEAPS |
| `quantitative-analyst` | IV rank/percentile, historical vol surface, rate path modeling | Is IV conducive to the strategy type (buying vs. selling premium)? |
| `options-strategist` | Standard strategy selection for comparison ("should this just be a 45-DTE vertical instead?") | Does this need 365+ DTE, or would a standard structure work just as well? |

### Downstream (Feeds Into)

| Skill | When to Hand Off | Handoff Format |
|-------|-----------------|----------------|
| `options-risk-engineer` | LEAPS position needs risk decomposition (delta/vega/rho contribution, tail risk, correlation break) | "LEAPS risk review: [ticker], [structure], [DTE], [notional], [net greeks], [key risks: rho, dividend, liquidity]" |
| `portfolio-signal-manager` | LEAPS position needs integration into broader portfolio (core-satellite, hedging overlay) | "LEAPS integration: [position], [portfolio_role], [% of NAV], [correlation to holdings], [rebalance cadence]" |
| `algorithmic-trader` | PMCC or diagonal needs automation (auto-roll, conditional orders, scanner) | "LEAPS automation: [structure], [entry rules], [roll triggers], [exit conditions], [safety rails]" |
| `swing-options-trader` | LEAPS is the long-dated "core" position; near-dated "swing" overlays needed | "Core LEAPS: [ticker], [strike], [DTE], [delta]. Swing overlay: [direction], [timeframe], [structure]" |
| `trade-performance-analyst` | LEAPS trade completed — journal for pattern analysis | "LEAPS closed: [entry/exit data], [rho contribution], [dividend impact], [actual vs. expected extrinsic decay]" |

## What Good Looks Like

**LEAPS Stock Replacement (GOOD):** SPY @ $500. Bought Jan 2027 350 Call (Δ=0.95+) for $161. Extrinsic: $11 (6.8%). Annualized extrinsic: 4.5%. Capital saved: $33,900. Interest earned on saved capital at 5%: $1,695/year. Net cost: ~$700/year for 4.3x leverage with defined risk. Exit trigger: DTE < 90 or Δ > 0.98.

**PMCC (GOOD):** SPY @ $500. Bought Jan 2027 400 Call (Δ=0.88, 540 DTE) for $115. Sold Feb 2026 520 Call (Δ=0.22, 30 DTE) for $2.20. Monthly ROC: 1.9%. Over 18 cycles: targeting 25-35% cumulative premium. Short_K ($520) > Long_K ($400) ✓. Ex-div check: SPY ex-div on [date] — short call expires before ex-div ✓. Exit: accumulated premium > LEAPS extrinsic cost + dividend gap. Net profit: remaining LEAPS value + total premium.

**LEAPS Portfolio Hedge (GOOD):** Portfolio $500,000. IV rank: 22% (favorable). Bought 2 SPY Jan 2027 430 Puts (14% OTM, Δ=-0.22) for $1,500 each. Annual cost: $2,000 (0.4% of portfolio). Protection kicks in at SPY < $430 (-14%). During COVID-style 35% crash: puts worth ~$25,000 each → partial portfolio offset.

## Operating at Different Levels

| Level | Scope | Key Capability |
|-------|-------|----------------|
| **L1: Apprentice** | Execute a single LEAPS stock replacement or PMCC on SPY/QQQ. Follow the strike hierarchy rule. Check extrinsic before entry | Knows: DITM selection, PMCC mechanics, dividend calendar. Doesn't know: rho, multi-leg LEAPS, portfolio integration |
| **L2: Practitioner** | Independently construct PMCCs and LEAPS hedges on any LEAPS-eligible ticker. Manage multi-cycle premium harvesting. Factor rho and dividends into strategy selection | Adds: rho analysis, dividend optimization, roll strategy, IV timing for LEAPS entry |
| **L3: Specialist** | Design LEAPS-based portfolio overlays (core-satellite with LEAPS core, LEAPS collar programs, tail hedging programs). Cross-skill coordination with risk engineer and portfolio manager | Adds: portfolio-level LEAPS deployment, correlation-aware hedging, tax-aware LEAPS management |
| **L4: Architect** | Build LEAPS-structured products for institutional deployment. LEAPS-based portable alpha. Custom LEAPS strategy composition combining multiple LEAPS structures | Adds: institutional LEAPS deployment, strategy composition, custom hedging algorithms |
| **L5: Transformative** | Create new LEAPS-based financial products. Publish LEAPS strategy research. Define industry standards for LEAPS-based portfolio construction | Adds: product innovation, research leadership, market structure influence |

## Anti-Patterns

| ❌ Common Mistake | ✅ Correct Approach |
|-------------------|-------------------|
| "LEAPS are just long-dated options — same rules apply" | LEAPS have fundamentally different Greek behavior (rho 3-5x, vega 2-3x, theta different curve). Use LEAPS-specific analysis, not short-dated rules |
| "I'll buy a 0.60-delta LEAPS — it's cheaper and still directional" | 0.60Δ LEAPS has 35-40% extrinsic. Stock must rise 8-12% just to break even from extrinsic decay. Buy 0.80+Δ for stock replacement |
| "PMCC short strike can be anything — it's just premium collection" | Short strike MUST be above LEAPS strike. This is the #1 PMCC error. Check before every sale |
| "IV doesn't matter for LEAPS — I'm holding for years" | IV at entry is locked in for the entire holding period. Buying LEAPS in high IV can mean 30-50% overpayment that takes years to recover |
| "Dividends are small compared to LEAPS leverage" | Over 2 years, 4%+ yield = 8%+ of notional. This dwarfs the LEAPS extrinsic. Quantify before entry |
| "I'll figure out the exit later" | LEAPS exit strategy must be defined at entry. DTE < 90, Δ > 0.95, thesis invalidated — each triggers a different exit behavior |
| "Higher trend_score always means better LEAPS outcome" | [BACKTEST-EVIDENCE] Score calibration is often inverted. Higher scores correlated with mean reversion, not continuation, on 9/11 test tickers. Calibrate per ticker |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Bought 0.60Δ LEAPS because "it's cheaper" — $30/contract vs $161 for 0.95Δ. Stock rises 8% but LEAPS only gains 12% because extrinsic decay ate 35% of the premium value. Deep ITM LEAPS would have gained 22% | $1K-$3K per contract in opportunity cost — "cheap" LEAPS are more expensive in practice because extrinsic-to-intrinsic ratio is the real cost | Buy 0.80+ delta for stock replacement. 0.60Δ LEAPS has 35-40% extrinsic — the stock must rise 8-12% just to break even from extrinsic decay alone |
| PMCC entered with LEAPS DTE = 240. After 6 short call cycles, LEAPS DTE = 60 and only 25% of extrinsic amortized. Forced to either roll LEAPS at unfavorable terms or close with unamortized extrinsic loss | $1.5K-$3K in stranded extrinsic + roll costs — insufficient runway is the #1 PMCC destroyer | Minimum 365 DTE at PMCC entry. 540+ DTE ideal. Each short call cycle (30-45 DTE) amortizes ~20-25% of LEAPS extrinsic. Need 4+ cycles minimum to amortize and profit |
| LEAPS put hedge bought when IV rank = 55% because "the market looks shaky." Paid $3,500 for 2-year protection that would cost $2,200 at IV rank 25%. Overpaid by 60% for insurance that spent most of its life as a drag | $800-$1,500/year in excess hedge cost per contract — buying insurance when it's expensive defeats the purpose | Never buy LEAPS puts at IV rank > 30%. Wait for vol compression or dollar-cost average over 3 entries during low-vol windows. The insurance is only valuable if bought cheap |
| 2% Fed rate cut on an 18-month portfolio of LEAPS calls. Rho impact = -$800 per 10 contracts from rate change alone, despite stocks being flat-to-up. Trader: "I don't understand why my LEAPS are losing money" | $500-$2K per LEAPS position in unexpected rho losses — rho is a first-order Greek on long-dated options | Compute rho exposure at entry: rho × expected rate change × position size. In a rate-cutting cycle, favor LEAPS puts or add a rate hedge. Size for the rate scenario, not just the equity scenario |
| Dividend yield 4.5% stock replaced with LEAPS. Over 2 years, missed 9% of notional in dividends. The LEAPS leverage was 4:1 but the dividend gap consumed 40% of the capital efficiency benefit | $2K-$5K in hidden costs over the holding period — missed dividends quietly erode the LEAPS advantage | Quantify dividend gap before entry: yield × years × notional. If dividend yield > 4%, LEAPS stock replacement is rarely +EV. Consider selling puts instead or pick a lower-yield ticker |
| PMCC: short call ITM at 7 DTE. Thought "I'll let it expire and get assigned — I can sell the LEAPS to cover." Pre-ex-div assignment: forced LEAPS exercise loses $3,000 in remaining time premium | $2K-$4K per incident — the time premium on a 9+ month LEAPS that gets forcibly exercised can be 15-30% of premium | Roll at 7 DTE minimum if short call is ATM or ITM. If ex-div within DTE and call is ITM → close immediately. Time premium loss on forced LEAPS exercise is the silent PMCC killer |
| LEAPS rolling decision made purely on DTE ("DTE < 90 so I must roll") while ignoring IV rank. Rolling a LEAPS in high IV (IV rank > 60%) locks in expensive new premium for another 18+ months | $1K-$3K in unnecessary premium cost — rolling at high IV means overpaying for the replacement LEAPS | Roll decision criteria: DTE < 90 AND IV rank < 40% AND trend_score > 40. If IV rank is high, delay roll or switch to a different strike. The combination of DTE + vol + trend determines optimal roll timing |

## Production Checklist

Before deploying ANY LEAPS strategy to live trading:

- [ ] 1. **Extrinsic verified:** Stock replacement LEAPS extrinsic < 4%. Annualized cost computed and below risk-free + margin rate spread.
- [ ] 2. **Strike hierarchy checked:** If PMCC or diagonal, short K > long K confirmed.
- [ ] 3. **IV environment favorable:** IV rank < 30% for buying LEAPS (calls or puts). IV rank > 50% for selling LEAPS premium.
- [ ] 4. **Liquidity confirmed:** OI > 100 on all legs. Bid-ask spread < 5% for long legs, < 10% for short legs.
- [ ] 5. **Dividend calendar reviewed:** All ex-div dates within LEAPS life noted. Short call ex-div risk windows mapped.
- [ ] 6. **Rho impact computed:** Rho × expected rate change × position size calculated. Three scenarios (bull/base/bear rates).
- [ ] 7. **Exit plan documented:** At least 3 exit triggers defined (DTE threshold, delta threshold, thesis invalidation, profit target, max loss).
- [ ] 8. **Asymmetric exit ratio:** Minimum 2:1 reward-to-risk on directional LEAPS trades. [BACKTEST-EVIDENCE]
- [ ] 9. **Volatility-adjusted sizing:** `size = 1.5 - (hv%/100) × 1.1` clipped [0.3, 1.5]. [BACKTEST-EVIDENCE]
- [ ] 10. **Ticker calibration:** Trend_score checked. HV percentile checked. LEAPS-specific performance history reviewed.
- [ ] 11. **Broad market regime:** SPY vs 50SMA, VIX level, Fed funds rate and expected path documented.
- [ ] 12. **PMCC cycle plan:** Target monthly ROC computed. Number of cycles to amortize extrinsic calculated.
- [ ] 13. **Tax implications:** LTCG eligibility timeline noted. Tax-loss harvesting opportunities identified.
- [ ] 14. **Correlation check:** For LEAPS hedges, underlying correlation to portfolio holdings verified.
- [ ] 15. **Post-mortem template prepared:** Entry thesis, expected Greeks evolution, actual vs. expected P&L tracking sheet ready.

## References

| Reference | Covers | When to Read |
|-----------|--------|-------------|
| `stock-replacement-math.md` | DITM selection, extrinsic analysis, LEAPS vs. shares comparison, capital efficiency | When evaluating any LEAPS stock replacement |
| `pmcc-optimization.md` | PMCC construction, strike hierarchy, roll cadence, assignment management | Before entering or managing any PMCC |
| `leaps-diagonals-and-calendars.md` | Multi-cycle premium harvesting, double LEAPS calendars, ratio calendars | When designing multi-cycle LEAPS strategies |
| `leaps-hedging-and-insurance.md` | Protective puts, collars, tail hedging, Dragon Portfolio approach | When using LEAPS for portfolio protection |
| `rho-and-rates-sensitivity.md` | Rho scaling by DTE, rate path scenarios, rho hedging, rho cheat sheet | Before any LEAPS trade with DTE > 180 |
| `dividend-strategies-with-leaps.md` | Dividend gap quantification, PMCC dividend offset, high-yield strategies | When underlying pays > 1% dividend yield |
| `leaps-behavioral-pitfalls.md` | Leverage overconfidence, DTE complacency, extrinsic denial, roll-or-die, detection rules | Weekly portfolio review — behavioral drift detection |
| `leaps-tax-and-estate.md` | LTCG vs STCG, Section 1256 advantage, wash sale traps, PMCC tax drag, stepped-up basis | Before year-end or any LEAPS sale decision |

**Cross-reference skills:** `options-strategist` (standard strategies), `advanced-options-structures` (complex multi-leg LEAPS), `options-risk-engineer` (risk decomposition), `quantitative-analyst` (vol surface, rate modeling), `swing-options-trader` (near-dated overlays on LEAPS core).

---

*Skill complete. Route questions about standard short-dated options to `options-strategist`. Route questions about complex multi-leg LEAPS structures (zebra LEAPS, LEAPS ratio diagonals) to `advanced-options-structures`.*
