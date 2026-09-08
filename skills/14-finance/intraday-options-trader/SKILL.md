---
type: finance
name: intraday-options-trader
description: >
  Use when the user wants to trade 0DTE options, gamma scalp intraday, execute
  Opening Range Breakout (ORB) strategies with options, trade momentum on intraday
  timeframes, or navigate options market microstructure (spreads, liquidity windows).
  Use when the user asks "0DTE strategy," "gamma scalp setup," "intraday options
  momentum," "ORB options," "same-day options trade," or "intraday circuit breaker
  design." Handles 0DTE butterfly-only entry rules, gamma scalping with GEX-based
  sizing, intraday microstructure-driven timing and venue selection, momentum/ORB
  confirmation sequences, and intraday-specific risk controls including daily loss
  limits, 2-consecutive-loss pause, and VIX spike circuit breakers. Do NOT use for
  multi-day swing trades (route to swing-options-trader), for standard 30-60 DTE
  strategies (route to options-strategist), for LEAPS or long-dated options (route
  to leaps-strategist), or for automated execution of intraday strategies (route
  to options-automation-engineer).
license: MIT
tags:
  - intraday-trading
  - 0DTE
  - gamma-scalping
  - day-trading
  - options
  - market-microstructure
  - momentum
  - ORB
chain:
  examples:
  - skills/14-finance/intraday-options-trader/examples/backtest
  consumes_from: [technical-signals-engineer, market-data-engineer, quantitative-analyst, options-strategist]
  feeds_into: [algorithmic-trader, trade-performance-analyst, options-automation-engineer, options-risk-engineer]
version: 1.0.0
status: active
author: Skills Library
created: "2026-07-16"
category: "14-finance"
token_budget: 4000

---
**(QUICK: 30s)** Route: run Core Workflow with standard checks.
**(QUICK: 5min)** Standard: full workflow including verification.
**(QUICK: 20min)** Deep: full workflow with cross-skill coordination and provenance.

**Quick route (QUICK):** run Route → Execute → Verify.

**Standard route (QUICK):** follow Core Workflow end to end with checks.

**Escalation route (QUICK):** escalate once with full context when blocked.

# Intraday Options Trader

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).
> No vendor-specific frontmatter fields.

<!-- STANDARD: 3min -->
## Route the Request

| User Intent | Route To | Decision Gate |
|-------------|----------|---------------|
| "Trade 0DTE" / "same-day expiration options" | → 0DTE Playbook (§3, ref: 0dte-playbook.md) | ONLY SPX or SPY. Never individual stocks. Cash-settled preferred |
| "Gamma scalp" / "delta-hedge intraday" / "scalp volatility" | → Gamma Scalping (§4, ref: gamma-scalping-mechanics.md) | IV < HV required. DTE ≤ 7. SPX/SPY/QQQ only |
| "ORB with options" / "opening range breakout options" | → ORB with Options (§5, ref: momentum-and-orb-with-options.md) | SPX/SPY only for options ORB. Confirm spread < 5% |
| "Momentum options" / "intraday trend options" / "tape reading options" | → Momentum Options (§5, ref: momentum-and-orb-with-options.md) | 3-confirmation required: volume, price, T&S |
| "Options spread too wide" / "when to trade intraday" / "liquidity windows" | → Microstructure (§6, ref: intraday-market-microstructure.md) | Trade only 9:35 AM-3:00 PM ET |
| "How to size intraday options" / "max daily loss options" / "circuit breaker" | → Risk Management (§7, ref: intraday-risk-management.md) | HARD: daily loss limit, 2-consecutive-loss pause, VIX spike halt |

## 10 Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE 0DTE trades that aren't butterflies. Credit spreads, long premium, and iron condors all have negative EV on 0DTE — it's gambling, not trading | Trigger: `DTE = 0 AND structure ≠ "butterfly"` in trade plan | STOP. "0DTE non-butterfly trade rejected. Only butterfly structures are +EV on 0DTE. Everything else: negative expectancy after spreads. Route to 3.2 for butterfly-only 0DTE rules." |
| R2 | REFUSE new entries after 3:00 PM ET. Gamma explosion in the final hour makes ATM options unhedgeable and spreads untradeable | Trigger: `current_time_ET > "15:00" AND trade_direction ≠ "close_only"` | STOP. "After 3:00 PM ET: CLOSE-ONLY mode. No new entries. All positions must be closed by 3:15 PM. Gamma risk is exponential — exits become impossible at fair prices." |
| R3 | REFUSE to continue trading when daily P&L hits loss limit. This is a HARD circuit breaker — no "one more trade to make it back" | Trigger: `daily_P&L ≤ -(daily_risk_budget)` in P&L tracker | STOP. "Daily loss limit hit. Trading stops NOW. Capital preservation is non-negotiable. Return tomorrow. The market will still be there — your capital won't if you override this." |
| R4 | REFUSE to continue after 2 consecutive max-loss trades. Two max-loss trades is not random noise — it signals broken thesis or tilted psychology | Trigger: `consecutive_max_loss_count ≥ 2` in trade journal | STOP. "2 consecutive max-loss trades. 30-minute mandatory pause. Step away, review the tape, check if thesis still valid. Resume at 50% size after review completes." |
| R5 | REFUSE trades where spread > 5% of option price. Spread costs consume any edge on intraday timeframes where edges are already 3-8% | Trigger: `(ask - bid) / mid > 0.05` for target option | STOP. "Spread > 5% of option price. Spread cost exceeds expected edge on intraday timeframe. Skip this setup or trade the underlying shares directly." |
| R6 | REFUSE to hold positions through a VIX spike > 50% intraday. Extreme vol = extreme spreads = cannot exit at fair prices | Trigger: `VIX_change_1min > 50% AND open_positions > 0` | STOP. "VIX spike > 50% intraday. CLOSE ALL POSITIONS, GO FLAT. Capital preservation > missed opportunity. Spreads are 10-30% wide right now." |
| R7 | REFUSE to hold individual stock options overnight on intraday timeframe. Single-stock overnight gap risk is unhedged and can produce 15-40% losses | Trigger: `underlying_type = "single_stock" AND hold_period ≠ "same_day" AND strategy = "intraday"` | STOP. "Individual stock overnight hold on intraday strategy. Overnight gaps are 2-3× larger than intraday moves. Close before market close or switch to SPX/SPY underlying." |
| R8 | REFUSE gamma scalp when GEX < $100 per 1% move. Below $100 GEX, hedging transaction costs exceed potential scalp profit | Trigger: `gamma × S² × 0.01 < 100 AND strategy = "gamma_scalp"` | STOP. "Gamma exposure too low for profitable scalp: GEX < $100 per 1% move. Transaction costs from delta hedging exceed the scalp edge. Skip." |
| R9 | NEVER set stops without gamma-adjusted buffer for DTE ≤ 3. Gamma acceleration causes exaggerated noise moves that trigger standard stops prematurely | Trigger: `DTE ≤ 3 AND stop_buffer_pct < 10 AND strategy = "intraday"` | STOP. "Stop buffer too tight for DTE ≤ 3. Gamma acceleration produces 10-15% noise moves. Add 10% to stop buffer or risk premature exit on noise, not signal." |
| R10 | REFUSE options ORB when spread > 5%. ORB works best with 1-tick spreads — options spread costs make marginal ORB setups negative EV | Trigger: `strategy = "ORB" AND option_spread_pct > 5` | STOP. "ORB options spread exceeds 5%. ORB edge requires tight spreads. Use shares for this ORB setup or switch to SPX/SPY where options spreads are 1-3 ticks." |

## Decision Tree

```
Intraday options request received
│
├─ 0DTE trade?
│  ├─ Structure = Butterfly? → YES → Entry window: 9:35-10:00 AM. Close by 2:45 PM. (§3)
│  ├─ Underlying = SPX (cash-settled)? → YES → Section 1256 tax treatment. Better than SPY. (§3.5)
│  ├─ Underlying = individual stock? → NO. 0DTE on individual stocks is assignment roulette.
│  └─ Structure ≠ Butterfly → REJECT. Only butterfly is +EV on 0DTE. [VERIFIED] (§3.2)
│
├─ Gamma scalp?
│  ├─ IV percentile < 30%? → YES → Proceed with scalp setup. (§4.2)
│  ├─ GEX > $100 per 1% move? → YES → Acceptable gamma exposure. (§4.3)
│  ├─ Hedging instrument selected (/MES, /ES, SPY shares)? → YES → Proceed. (§4.5)
│  └─ Any condition fails → SKIP. No scalp edge. (§4.2)
│
├─ ORB / Momentum setup?
│  ├─ All 3 confirmations (volume, price, T&S)? → YES → Proceed. (§5.2)
│  ├─ Options spread < 5%? → If no → use shares instead.
│  ├─ DTE ≥ 7? → If no → gamma-adjusted sizing required. (§7.3)
│  └─ → SELECT structure: ATM debit spread (strong signal) or ATM single leg (moderate). (§5.1)
│
├─ Risk management check (MANDATORY before every trade):
│  ├─ Daily loss limit hit? → STOP. (§7.1)
│  ├─ 2 consecutive max-loss? → 30-MINUTE PAUSE. (§7.2)
│  ├─ VIX stable? → If spike >20%: halve. >50%: flat. (§7.4)
│  ├─ Within time window (9:35-3:00 PM)? → If no: reject new entries. (§7.6)
│  └─ Position size calculated? → Vol-adjusted + gamma-adjusted. (§7.2-7.3)
│
└─ → EXECUTE with limit orders. Monitor. Exit at target/stop/time-stop.

```

## Core Workflow

### Phase 1: Pre-Market Preparation (15 min before open)

1. **Market regime check:** SPY vs 50SMA, VIX level, overnight futures. Note direction and magnitude.
2. **Economic calendar:** Any data releases today? FOMC? CPI? NFP? If yes, adjust strategy.
3. **IV environment:** Compute IV rank for SPY/SPX. If IV rank > 50%, reduce position sizes.
4. **Watchlist:** Identify 2-3 tickers with options liquidity (OI > 100, spread < 5%) for potential setups.
5. **Set daily risk budget:** Compute daily P&L limit. Reset from previous session.

### Phase 2: Opening Window (9:30-10:00 AM)

1. **Wait 3-5 minutes** after open. Opening prints are chaotic.
2. **Observe OR levels:** 5-min ORB or 30-min ORB. Note direction and volume.
3. **0DTE butterfly assessment:** If conditions met (premium favorable, spread tight), enter at 9:35-10:00 AM.
4. **T&S scan:** Any large block prints? Aggressive buying/selling?

### Phase 3: Active Trading (10:00 AM-3:00 PM)

1. **Monitor open positions:** Delta drift, gamma acceleration, IV changes.
2. **New setups:** ORB continuation, momentum, post-news scalp (if news triggered).
3. **Apply time-of-day sizing:** Reduce 25% during 10:30-11:30, reduce 50% during 11:30-1:30 PM.
4. **Close 0DTE positions by 2:45 PM.**
5. **All other positions: close by 3:00 PM.**

### Phase 4: Post-Market Review (30 min after close)

1. **Journal all trades:** Entry/exit times, strategy, P&L, MAE, MFE.
2. **Attribute P&L:** Skill, luck, or noise?
3. **Bias check:** Disposition effect (held losers too long), revenge trading, overconfidence.
4. **Update daily P&L tracker.** If daily loss limit approached, reduce next day's risk budget.

## Strategy Deep Dives

### 1. 0DTE Trading

> **Reference:** 0dte-playbook.md

**The 0DTE iron law:** Butterfly is the ONLY +EV 0DTE structure. Credit spreads = -$10 EV. Long premium = -$375 EV. Iron condors = -$34.40 EV. [VERIFIED from published research]

Trade ONLY SPX (cash-settled, Section 1256). Enter 9:35-10:00 AM. Close by 2:45 PM. Never individual stocks. Never after 3:00 PM.

### 2. Gamma Scalping

> **Reference:** gamma-scalping-mechanics.md

Dynamically delta-hedge a long ATM option to capture realized vol > implied vol. Requires: IV < HV, hedge bands, tight spreads. P&L decomposition is critical — don't confuse directional luck with scalp skill.

### 3. ORB & Momentum with Options

> **Reference:** momentum-and-orb-with-options.md

ORB with SPX/SPY options only. Momentum requires 3 confirmations (volume, price, T&S). ATM debit spreads preferred over single legs for stronger signals. Apply FalseStopGuard before exiting on pullbacks.

### 4. Market Microstructure

> **Reference:** intraday-market-microstructure.md

Trade during liquidity windows (9:35-11:00 AM optimal). Avoid final hour. Use limit orders. Use native spread orders for multi-leg. Understand PFOF vs DMA routing. Read the tape for institutional flow.

### 5. Intraday Risk Management

> **Reference:** intraday-risk-management.md

HARD circuit breakers: daily loss limit, 2-consecutive-loss pause, VIX spike halt. Volatility-adjusted + gamma-adjusted sizing. FalseStopGuard prevents noise exits. Time-based position limits.

## Research Prerequisites

**RP1 (LIQUIDITY):** Check bid-ask spread % for target options. Must be < 5% at entry window. Check open interest.

**RP2 (VOL ENVIRONMENT):** Compute IV percentile for the underlying. Determine HV for gamma scalp edge assessment.

**RP3 (ECONOMIC CALENDAR):** Any data releases, FOMC, or earnings within the trading day? If yes, strategy must account for event risk.

**RP4 (GREEK PROFILE):** For any position: compute delta, gamma, theta at entry. Project gamma at 3:00 PM if holding near-dated options.

**RP5 (CORRELATION CHECK):** If trading individual stock options, is the trade thesis stock-specific or just riding SPY beta? If beta-driven, trade SPY options instead (better liquidity).

**RP6 (TICKER CALIBRATION):** [BACKTEST-EVIDENCE] Check trend_score and HV percentile. Not all tickers work for intraday options.

**RP7 (MICROSTRUCTURE CHECK):** What exchange is this option most active on? What's the typical spread at this time of day?

**RP8 (SIZING CHECK):** Run vol-adjusted + gamma-adjusted sizing. Confirm position fits within daily risk budget per-trade allocation.

## Error Decoder

| # | Symptom | Root Cause | Fix | Lesson |
|---|---------|-----------|-----------|--------|
| E1 | "0DTE credit spread lost $450 on a 5-wide spread" | Gamma explosion at 3:30 PM. Underlying breached short strike in final minutes | Never hold 0DTE positions past 3:00 PM. Close by 2:45 PM to have buffer. Butterfly only for 0DTE | 0DTE short premium is negative EV. The occasional losses are larger than the frequent small wins |
| E2 | "Gamma scalp lost money even though stock was volatile" | Realized vol < implied vol. Theta decay exceeded scalp profits | Before entry: confirm IV percentile < 30% and current HV > IV. If not, scalp will lose | Gamma scalping only works when realized vol exceeds implied. Buying expensive vol for scalping guarantees losses |
| E3 | "Stopped out of momentum trade, then it reversed and ran to target" | Premature exit on noise. FalseStopGuard not applied | Add FalseStopGuard: confirm reversal with volume + wick + thin-window analysis before exiting | Noise is the #1 cause of intraday losses. Not every pullback is a reversal |
| E4 | "Blew through daily loss limit chasing a 'sure thing' recovery trade" | Revenge trading after a loss. Disposition effect: "I'll make it back" | HARD circuit breaker: daily loss limit = STOP FOR THE DAY. No exceptions. No "one more trade" | The market doesn't know or care about your P&L. Daily loss limits protect capital for tomorrow |
| E5 | "Opening range breakout option entry slipped 8% from intended price" | Entered during first 2 minutes after open. Spreads were 15% wide | Always wait until 9:35 AM minimum before entering. Verify spread has tightened to < 5% | The opening 2 minutes is market maker price discovery, not a tradeable market for retail |
| E6 | "Assigned on SPY calls held overnight — bought 200 shares at $50,000" | Individual stock/ETF options have physical delivery. Held an ITM call through expiration | For intraday: close ALL positions before close. For SPY specifically: never hold ITM short-dated calls through expiration unless you want the shares | Equity/ETF options settle to shares. SPX (cash-settled) eliminates this risk for 0DTE |
| E7 | "Two losses, paused 30 minutes, came back, lost again, quit for the day" | Pause worked. The day was a losing day. Accepting this prevented a $5,000 loss from becoming a $15,000 loss | **This is correct behavior.** Two-losses-then-pause then third loss → STOP FOR THE DAY. This IS the system working | Some days you lose. The system limits the damage. Tomorrow is a new day with fresh setups |

## Anti-Hallucination

**[VERIFIED]** — Confirmed via CBOE specifications, academic research (Brogaard et al., 2024), SEC 0DTE report, or exchange documentation.
**[COMPUTED]** — Calculated using standard options models (Black-Scholes) with stated assumptions.
**[ESTIMATED]** — Ranges based on practitioner experience with explanation of uncertainty.
**[COMMON-PRACTICE]** — Widely used by professional day traders but not codified in exchange rules or academic literature.
**[BACKTEST-EVIDENCE]** — Inferred from the companion Trading project's 1,068-trade backtest across 11 tickers.

**Gamma acceleration near expiration is model-dependent.** Different models give different gamma values in the final hours. Gamma scalping P&L is path-dependent and the standard P&L approximation formula is just that — an approximation.

- **Admit uncertainty**: if a claim cannot be verified, say so and open the question rather than asserting.
- **Flag your knowledge cutoff**: "My training data ends in [date] — verify current market/spec data before treating it as fact."
- **Never guess security**: if a config or exposure question touches security, refuse to guess and point to official guidance.
- **[VERIFIED]**: mark definitive claims [VERIFIED] only when confirmed against a source; otherwise mark [BEST-KNOWN].

## Cross-Skill Coordination

### Upstream

| Skill | What to Request | Decision Gate |
|-------|----------------|---------------|
| `technical-signals-engineer` | ORB levels, momentum signals, volume profile, intraday support/resistance | Is the technical setup valid for options entry, or is the spread too wide? |
| `market-data-engineer` | NBBO data, time & sales, volume profile, exchange routing data | Is liquidity sufficient for the intended strategy? |
| `quantitative-analyst` | IV rank, IV-HV spread, gamma exposure, expected move | Is the vol environment favorable for the strategy type? |
| `options-strategist` | Strategy construction fundamentals, standard Greeks | Confirm the selected options structure is valid |

### Downstream

| Skill | When to Hand Off | Handoff Format |
|-------|-----------------|----------------|
| `algorithmic-trader` | Intraday strategy needs automation (auto-execution, conditional orders) | "Intraday automation: [strategy], [entry conditions], [exit rules], [circuit breakers]" |
| `trade-performance-analyst` | Day's trades completed — journal for pattern analysis | "Intraday session: [date], [trades], [P&L], [bias flags], [lessons]" |
| `options-automation-engineer` | Strategy ready for scanner-to-execution pipeline | "Intraday pipeline: [scan parameters], [filter chain], [execution rules], [safety rails]" |
| `options-risk-engineer` | Intraday risk framework needs review for drawdowns or new strategies | "Intraday risk review: [max daily loss], [consecutive loss pattern], [VIX spike response], [drawdown analysis]" |

| Upstream Skill | What You Receive | When to Involve |
|----------------|------------------|-----------------|
| `data-engineer` / market-data sources | Clean price/volume and fundamentals | Before any model or strategy work |
| `quantitative-analyst` or analytics | Model outputs and statistical baselines | When validating signals or calibrating |
| `risk-engineer` / risk tooling | Limits and exposure context | When sizing positions or setting guards |

## What Good Looks Like

**0DTE Butterfly (GOOD):** SPX @ 5200 at 9:40 AM. IV rank: 25%. Enter 5200/5220/5240 call butterfly for $4.50 debit ($450/contract). Spread: 3% of option price. Close at 2:30 PM with SPX at 5218 for $8.00 credit. Profit: $350 (78% ROI). All within risk limits. [COMPUTED: Example only]

**Gamma Scalp (GOOD):** SPX ATM straddle, IV=14%, HV=18%. Entry at 9:45 AM. Hedge band = GEX × 0.50. 8 hedges during the day at ±$250 per hedge. Total scalp P&L: +$1,600. Theta cost: -$800. Net: +$800 after costs. [COMPUTED: Requires realized > implied]

**Momentum Options (GOOD):** SPY momentum signal confirmed (volume, price, T&S). Enter ATM $520 call, 10 DTE, $3.00 ($300/contract). Target: 50% (+$150). Stop: 30% (-$90). Time stop: 60 min. Hit target in 45 min. P&L: +$150. FalseStopGuard held through two minor pullbacks that were noise (low volume, <3 bars).
| ☐ | Complete when output is scoped to the request and grounded in evidence 1 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 2 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 3 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 4 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 5 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 6 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 7 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 8 | the check in the criterion passes and is recorded |
## Operating at Different Levels

| Level | Scope | Key Capability |
|-------|-------|----------------|
| **L1: Apprentice** | Execute 0DTE butterflies on SPX following the entry/exit timing rules. Use pre-calculated sizing | Knows: SPX butterfly construction, time-of-day rules, daily loss limit. Doesn't know: gamma scalping, microstructure, T&S reading |
| **L2: Practitioner** | Independently trade 0DTE butterflies, momentum options, ORB with options. Apply FalseStopGuard | Adds: T&S reading, momentum confirmation, gamma-adjusted sizing, post-trade attribution |
| **L3: Specialist** | Gamma scalp profitably. Navigate complex microstructure. Trade through news events with proper adjustments | Adds: gamma scalping mechanics, hedge band optimization, event-based trading, PFOF vs DMA routing |
| **L4: Architect** | Build intraday options trading systems. Design automated execution pipelines. Optimize across microstructure regimes | Adds: execution algorithm design, microstructure arbitrage, cross-exchange routing, market impact modeling |
| **L5: Transformative** | Operate at market-maker level sophistication. Publish intraday options research. Define industry best practices | Adds: HFT-grade execution, market making, order flow toxicity modeling |

## Anti-Patterns

| ❌ Common Mistake | ✅ Correct Approach |
|-------------------|-------------------|
| "0DTE iron condors are safe — high probability of profit" | Iron condors on 0DTE have -$34.40 EV. One loss wipes out 10+ wins. Only butterfly is +EV |
| "I can leg into the spread manually to get better prices" | Use native spread orders. Legging risk is real — one leg fills, the other doesn't, now you have a naked position in a fast market |
| "The stock is down 2%, option is down 40% — it'll bounce, I'll hold" | Intraday: gamma means small moves compound. "Wait for a bounce" is a multi-day concept. Intraday, cut losers at stop |
| "I'll use Robinhood for gamma scalping — commission-free!" | PFOF routing adds latency. DMA brokers (IBKR Pro) are required for rapid re-hedging. Free commissions = you're the product |
| "VIX spiked to 35 — great vol for my long straddle" | VIX spike = spreads widen = can't exit at fair price. The vol might be right but the execution is wrong |
| "I made 3 winning trades in a row — I'm on fire, let me size up" | Overconfidence bias. After 3 wins, reduce size by 25%. Win streaks revert to mean. Sizing up after wins is the top predictor of blown accounts |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| 0DTE iron condor: "it's high probability — 85% chance of profit." One loss at $450 wipes 10+ wins at $40 each = negative expected value | $2K-$5K/month in consistent 0DTE premium selling losses — the math is negative EV by $34.40/trade | Only butterfly is +EV on 0DTE. Credit spreads, iron condors, long premium all have negative EV. If you must trade 0DTE non-butterfly, you're gambling, not trading |
| Momentum trade entered 30 seconds after market open. Spread is 15% wide. Fill is 8% worse than intended. Edge is 5% — already underwater before the trade starts | $500-$2K/day in slippage on marginal setups — the spread is eating your edge before the trade has a chance | Wait until 9:35 AM minimum before entering. Verify spread < 5% of option price. The opening 2 minutes are market-maker price discovery, not a tradeable market for retail |
| "VIX spiked to 35 — great vol for my long straddle." Enter the trade. Spreads are 20-30% wide. Can't exit at fair price when vol mean-reverts. Lose on both entry and exit | $1K-$3K per trade — the vol environment might be right but the execution environment is wrong. Can't profit from vol if you can't trade it efficiently | VIX spike > 50% intraday = close everything, go flat. VIX > 25 = halve sizes, widen stops. VIX spike conditions = avoid new premium-buying entries because spreads are punitive |
| Not using FalseStopGuard — stopped out of momentum trade on noise, then it reversed and ran to target. 3 of these per week = -$900/month from premature exits | $500-$1,500/month in unnecessary stop-outs — the #1 cause of intraday losses is noise, not failed thesis | Apply FalseStopGuard: confirm reversal with volume + wick + thin-window analysis before exiting. Not every pullback is a reversal. Wait for confirmation before triggering a stop |
| 2 consecutive max-loss trades. "I'll make it back — this next setup is a sure thing." Third trade is also a max loss. Daily loss budget: -$800. Actual: -$2,400 | $1,500-$3,000 per blown daily limit — the "sure thing" recovery trade is the most expensive trade in intraday options | HARD daily loss limit = STOP FOR THE DAY. 2 consecutive max-loss trades = 30-minute mandatory pause. Resume at 50% size. Third loss = day over. No exceptions — the market is still there tomorrow |
| Gamma scalp on individual stock — need to delta-hedge rapidly. Using Robinhood (PFOF routing) with 200ms+ latency. Hedges are always late, scalp loses money consistently | $1K-$3K/week in latency costs — PFOF routing adds 100-300ms of execution delay that kills gamma scalp profitability | DMA broker only for gamma scalping (IBKR Pro, not Lite). Sub-50ms execution required for profitable hedging. Free commissions = you're the product — the latency cost far exceeds any commission savings |
| ORB breakout on SPY using options. Premium paid $1.50 with 10% spread. ORB needs a 5-point SPY move to break even. Move happens but profit is $0.20 after spread. Risk was $1.30 | $300-$1,000 per trade — option spread costs make marginal ORB setups net negative EV | ORB trades with options spread > 5% should use shares instead. ORB works best on instruments with 1-tick spreads. Options are a secondary vehicle for ORB — use SPY shares for the primary ORB setup |

## Production Checklist

Before ANY intraday options session:

- [ ] 1. **Economic calendar checked:** No major data releases during trading window. If FOMC: no intraday options holdings through 2:00 PM.
- [ ] 2. **VIX environment assessed:** VIX stable. If VIX > 25, halve all position sizes.
- [ ] 3. **IV rank computed:** For buying premium strategies: IV rank < 30%. For selling: IV rank > 50%.
- [ ] 4. **Daily risk budget set:** 1-2% of account max daily loss. Reset from previous session.
- [ ] 5. **Watchlist defined:** 2-3 tickers with options liquidity (OI > 100, spread < 5%).
- [ ] 6. **Time management:** First entries after 9:35 AM. All positions closed by 3:00 PM (0DTE by 2:45 PM).
- [ ] 7. **Position sizing pre-calculated:** Vol-adjusted formula applied. Gamma-adjusted for DTE ≤ 7.
- [ ] 8. **Circuit breakers programmed:** Daily loss limit, 2-consecutive-loss pause, VIX spike halt.
- [ ] 9. **Exit plans written for all positions:** Target, stop (gamma-adjusted), time stop.
- [ ] 10. **FalseStopGuard parameters set:** Volume threshold, wick threshold, thin-window bar count.
- [ ] 11. **Broker routing confirmed:** DMA for gamma scalping. PFOF OK for butterflies/slower strategies.
- [ ] 12. **Only native spread orders for multi-leg:** Never leg in manually.
- [ ] 13. **SPX for 0DTE:** Cash-settled. Individual stock 0DTE = assignment roulette. Only SPX.
- [ ] 14. **Post-session journal template ready:** Entry/exit, strategy, P&L, MAE/MFE, bias flag, attribution.
- [ ] 15. **Mental state check:** If tired, stressed, or emotional → reduce size by 50% or skip the session.

## Best Practices

1. Only butterfly is +EV on 0DTE. Credit spreads, iron condors, long premium all have negative EV. If you must trade 0DTE non-butterfly, you're gambling, not trading
2. Wait until 9:35 AM minimum before entering. Verify spread < 5% of option price. The opening 2 minutes are market-maker price discovery, not a tradeable market for retail
3. VIX spike > 50% intraday = close everything, go flat. VIX > 25 = halve sizes, widen stops. VIX spike conditions = avoid new premium-buying entries because spreads are punitive
4. Apply FalseStopGuard: confirm reversal with volume + wick + thin-window analysis before exiting. Not every pullback is a reversal. Wait for confirmation before triggering a stop
5. HARD daily loss limit = STOP FOR THE DAY. 2 consecutive max-loss trades = 30-minute mandatory pause. Resume at 50% size. Third loss = day over. No exceptions — the market is still there tomorrow
6. DMA broker only for gamma scalping (IBKR Pro, not Lite). Sub-50ms execution required for profitable hedging. Free commissions = you're the product — the latency cost far exceeds any commission savings
7. ORB trades with options spread > 5% should use shares instead. ORB works best on instruments with 1-tick spreads. Options are a secondary vehicle for ORB — use SPY shares for the primary ORB setup
<!-- DEEP: 10+min — extended deep-dive patterns and automation details live in this skill's references/ -->

## State Log
All material decisions, regime/calibration changes, and escalations are appended to the decision ledger ({at, what, by}); version bumps are recorded in the repository changelog so context is recoverable without replaying prior sessions.

## Error Recovery
| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Model/backtest disagrees with live market | Re-validate inputs and data source; reproduce the signal | Cross-check against a second data vendor and regime filter | Escalate with both datasets attached; do not trade on the disagreement |
| Strategy underperforms its backtest | Check regime drift, slippage, and position sizing assumptions | Recalibrate parameters against the current regime | Mark the strategy suspended until recalibration is verified |
| Data feed gap or stale quote | Confirm feed status and timestamp freshness | Fail over to the secondary feed; widen execution guards | Halt automated flow; escalate with the incident record |
| Unexpected risk/limit breach | Freeze position growth; recompute exposure | Reduce size to within limits | Escalate with full P&L and exposure evidence |

## Verification Guardrails
- Verify output against the strategy specification and current market data before acting.
- Confirm risk limits, position sizing, and kill-switch states are within bounds.
- Flag knowledge cutoff: re-verify model parameters and market structure against live sources.

## Failure Modes & Exit Rules

**Failure modes and known limitations** (what can go wrong, when it breaks):
- Failure mode: stale or mis-sourced input data produces a confident but wrong read. Mitigate by pinning the data revision and re-verifying before acting.
- Failure mode: the regime changes after calibration (bull -> correction -> bear -> crash). Mitigate by treating regime as a state to re-check, not a constant.
- Failure mode: liquidity thins exactly when the position needs to exit. Worst case: the intended stop-loss cannot fill at the planned level.
- Failure mode: leverage amplifies a small adverse move into a large loss. Edge case: margin call cascades before any exit rule can act.
- Failure mode: crowding - the same signal is held by many participants and unwinds at once. Known limitation: correlation rises in stress.
- Failure mode: model overfit - the backtest captures noise. Mitigate by holding out data and demanding the pattern repeats out-of-sample.
- Failure mode: execution slippage and spread widen in fast markets. What goes wrong: realized fill is worse than the modeled fill.
- Failure mode: counterparty or venue risk materializes (halt, rejection, failed settlement). Mitigate with venue fallbacks and pre-trade checks.
- Failure mode: a black-swan event outside the modeled distribution. What breaks: every correlated hedge at once. Mitigate by sizing for it anyway.

**Exit conditions / stop-loss rules:**
- Stop-loss: exit the position when the loss reaches the pre-defined level for this strategy; the level is set at entry and not widened intraday.
- Exit condition: close the position when the original thesis is invalidated (signal gone, data revised, regime flipped).
- Exit condition: time stop - if the expected catalyst has not appeared by the plan horizon, exit and re-evaluate.
- Exit plan: scale out into strength and never add to a losing position beyond plan.

**Regime notes (bull / correction / bear / crash):**
- Bull market: trends and momentum strategies tend to work; fade-strategy drawdowns are shallow; chase risk is the main failure mode.
- Correction (bull market pullback): mean-reversion can work; trend entries need patience; avoid adding risk at the first green candle.
- Bear market: short-duration and defensive positioning matter; long-biased strategies must respect the lower regime; rallies are exit opportunities.
- Crash regime: correlation goes to one, liquidity evaporates, and stop-losses gap. Position sizing is the only reliable defense; assume the crash can always come.

**Provenance of this guidance:**
- [COMMON-PRACTICE] Stop-loss placement, exit rules, and regime states are standard risk-management practice in trading literature.
- [ESTIMATED] Threshold levels quoted in this SKILL are illustrative calibrations, not broker-verified figures.
- [COMPUTED] Scenario arithmetic in the backtest example is deterministic and reproducible from its stated assumptions.
- [VERIFIED] The skill's structural invariants (sections, chain, references) are verified by the repository gates.
- [COMMON-PRACTICE] Regime definitions follow standard market-cycle nomenclature (bull/correction/bear/crash).
- [ESTIMATED] The failure-mode likelihood ordering is qualitative judgment, not a measured statistic.

## References

| Reference | Covers | When to Read |
|-----------|--------|-------------|
| `0dte-playbook.md` | 0DTE strategy EV, butterfly construction, gamma curve, entry/exit timing | Before any 0DTE trade |
| `gamma-scalping-mechanics.md` | Hedge bands, GEX calculation, breakeven math, post-event scalping | Before any gamma scalp |
| `intraday-market-microstructure.md` | NBBO, PFOF, liquidity windows, time & sales, order types | Before session prep |
| `momentum-and-orb-with-options.md` | ORB setup, momentum confirmation, FalseStopGuard, news trading | For ORB/momentum setups |
| `intraday-risk-management.md` | Circuit breakers, vol-adjusted sizing, gamma-adjusted sizing, time-based risk | Before entering any position |
| `order-flow-and-tape-reading.md` | Time & sales, institutional flow detection, FalseStopGuard exit confirmation, tape patterns | When entering momentum/ORB trades — confirms move is real, not noise |
| `options-execution-quality-metrics.md` | Fill-to-mid spread, slippage, time-to-fill, broker routing comparison, daily review checklist | Before any intraday session — execution IS the edge |
| `broker-comparison-for-intraday.md` | DMA vs smart routing vs PFOF, commission math, latency profiles, broker recommendations by style | Before selecting a broker for intraday options |

**Cross-reference skills:** `options-strategist` (standard strategy construction), `swing-options-trader` (multi-day options), `algorithmic-trader` (automation), `options-automation-engineer` (execution pipeline).

---

*Skill complete. Route standard multi-day options to `swing-options-trader`. Route standard 30-60 DTE strategies to `options-strategist`. Route automation requests to `options-automation-engineer`.*

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Do not assert unverified claims | You are about to state a number or fact without a source | Verify or mark [BEST-KNOWN] and say so |
| G2 | Do not act without confirming the task intent | Task scope is ambiguous | Restate the task and confirm before producing output |

## The Expert's Mindset

Treat every claim as needing evidence, every recommendation as carrying declared assumptions, and every limitation as something to name rather than hide.

## When to Use

Use this skill when the task matches the description's trigger conditions. When it does not, route to the owning skill instead.

## Decision Trees

1. Is the task in this skill's scope? If no, route to the owning skill.
2. Is the required input available and verifiable? If no, request or escalate.
3. Is the output verifiable against the request? If no, revise with evidence.
### Decision Tree 1: In-scope or out?
- In-scope: follow Core Workflow and verify.
- Out-of-scope: route to the owning skill and stop.

### Decision Tree 2: Verify locally or escalate?
- Locally verifiable: run the check and record the result.
- Blocked externally: escalate once with full context.

### Decision Tree 3: Ship or revise?
- Meets What Good Looks Like: deliver with evidence.
- Gaps found: revise before delivering.

## Proactive Triggers

- New task arrives that matches the description: invoke this skill's workflow.
- Existing output needs re-verification: re-run the verify step rather than assuming.
- A claim lacks a source: flag it instead of passing it forward.

## Deliberate Practice

- Run the workflow on a real task and compare output against the request.
- Review where verification caught an error and encode that check into the routine.
- Calibrate: adjust approach based on what the last N outputs revealed.

## Anti-Rationalization

- ❌ "This edge case won't happen" — every claimed edge case gets a concrete check.
- ❌ "It works because it must" — assert only what you can demonstrate.
- ❌ "Everyone does it this way" — precedent is not evidence for correctness here.
- ❌ "The output looks plausible" — plausible is not verified; run the check.
- ✅ State the risk of being wrong and what would change your mind.

## When NOT to Use

- The task needs judgment or authority this skill does not own.
- The request is a one-off convenience that bypasses the verified workflow.
- A specialized peer skill owns the exact scenario — route there instead.
- There is no way to verify the output against a source of truth.
- In-scope: proceed through Core Workflow.
- Out-of-scope: route to the owning skill and stop.

### Decision Tree 2: Verify or escalate?
- Verifiable locally: run the check and record the result.
- Blocked externally: escalate once with full context.

- Meets What Good Looks Like: deliver with evidence.
- Gaps found: revise before delivering.
