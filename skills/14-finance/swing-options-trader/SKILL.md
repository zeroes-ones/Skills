---
name: swing-options-trader
description: >
  Use when the user wants to swing trade options on 2-30 day holding periods, select
  optimal DTE for swing timeframes, trend-follow with options, enter pullback/reversal
  patterns, rotate sectors using options, or navigate earnings swings. Use when the
  user asks "swing trade options," "multi-day options strategy," "best DTE for 2-week
  trade," "trend following with puts/calls," "pullback entry options," or "sector
  rotation options allocation." Handles DTE selection with Greek evolution modeling,
  trend-following option structures, pullback/reversal entry, sector rotation through
  ETFs, earnings swing playbook, and swing risk management (Half-Kelly, weekend gap
  protection, drawdown circuit breakers). Do NOT use for same-day intraday (route to
  intraday-options-trader), multi-year LEAPS (route to leaps-strategist), standard
  30-60 DTE (route to options-strategist), or position-trade > 30 days (route to
  options-strategist).
license: MIT
tags:
  - swing-trading
  - options
  - multi-day
  - trend-following
  - pullback-patterns
  - sector-rotation
  - earnings-rules
  - risk-management
chain:
  consumes_from: [technical-signals-engineer, options-strategist, fundamental-analyst, quantitative-analyst, leaps-strategist]
  feeds_into: [portfolio-signal-manager, algorithmic-trader, trade-performance-analyst, leaps-strategist, options-automation-engineer]
version: 1.0.0
status: active
author: Skills Library
created: "2026-07-16"
category: "14-finance"
token_budget: 4000
---

# Swing Options Trader

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).
> No vendor-specific frontmatter fields.

<!-- STANDARD: 3min -->
## Route the Request

| User Intent | Route To | Decision Gate |
|-------------|----------|---------------|
| "Swing trade options" / "multi-day options strategy" / "2-week options" | → Timeframe Optimization (§3, ref: swing-timeframe-optimization.md) | Entry DTE ≥ 2× expected hold period |
| "Trend following with options" / "pullback entry options" | → Trend Following & Pullbacks (§4-5, refs: trend-following, pullback-and-reversal) | ADX 20-30 optimal. Higher scores ≠ better outcomes |
| "Sector rotation options" / "which sector options to trade" | → Sector Rotation (§6, ref: sector-rotation-options.md) | Only liquid sector ETFs. RS confirmation required |
| "Earnings options strategy" / "pre-earnings options" / "post-earnings drift" | → Earnings Playbook (§7, ref: earnings-swing-playbook.md) | NEVER hold full-size directional through earnings |
| "Swing position sizing" / "Kelly for options" / "swing risk management" | → Risk Management (§8, ref: swing-risk-management.md) | Half-Kelly with 5% max per trade |
| "Gap strategy options" / "weekend gap options" | → Gap Strategies (§5.3, ref: pullback-and-reversal-patterns.md) | Reduce size 25-50% before weekends |

## 10 Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE swing entries when DTE < 2× expected hold period. Theta decay in the final 21 DTE is too aggressive for a swing timeframe | Trigger: `entry_DTE < 2 × expected_hold_days` in swing trade plan | STOP. "Entry DTE < 2× hold period: a 10-day swing needs ≥21 DTE. A 21-day swing needs ≥45 DTE. Theta acceleration in final 21 days will destroy swing edge." |
| R2 | REFUSE to hold credit spreads past 50% max profit. The remaining 50% takes >50% of time and carries increasing gamma risk | Trigger: `current_pnl ≥ 0.50 × max_profit AND position_type = "credit_spread"` | STOP. "Credit spread at 50% max profit. Close now. The remaining 50% takes >50% of time with increasing gamma risk. Take the win and redeploy capital." |
| R3 | REFUSE directional positions through earnings. Post-earnings gaps of 5-15% wipe months of swing profits in one event | Trigger: `earnings_date BETWEEN today AND expected_exit_date AND position_direction ≠ "neutral"` | STOP. "Earnings falls within holding period on directional position. Close before earnings or reduce to 25% max. Post-earnings gaps (5-15%) can wipe 2-3 months of swing P&L." |
| R4 | REFUSE to enter at full size when swing entry score > 85. High scores predict mean reversion on 9/11 test tickers — calibration is inverted | Trigger: `swing_entry_score > 85 AND position_size = “full”` in trade plan | STOP. "Swing entry score > 85 — calibration inverted. Reduce size by 25% and verify with trend duration. Use score for direction, trend duration for conviction." |
| R5 | REFUSE directional swing trades with asymmetric exit ratio < 2:1. 1:1 RR at 50% WR = -5% expectancy after spreads | Trigger: `max_profit / max_loss < 2 AND strategy = “directional_swing”` | STOP. "Exit ratio < 2:1. 1:1 RR at 50% WR = -5% expectancy after spread costs. Every trade plan must define profit target, stop loss, time stop, AND thesis invalidation exit." |
| R6 | REFUSE to add swing positions when portfolio correlation exceeds threshold. Diversification fails in crashes — assume crash correlation 0.7-0.9 | Trigger: `portfolio_correlation > 0.60 AND new_position_correlation > 0.50` | STOP. "New position would push portfolio correlation above threshold. Reduce combined position size by 25%. In a crash, all equity positions correlate at 0.7-0.9." |
| R7 | NEVER hold DTE ≤ 7 options over a weekend without 10% stop buffer. Weekend gaps are 2-3× overnight gaps; gamma tightening compounds the risk | Trigger: `DTE ≤ 7 AND holding_over_weekend AND stop_buffer_pct < 10` | STOP. "Weekend gap risk unaddressed for DTE ≤ 7. Add 10% to stop buffer. Weekend gaps are 2-3× larger than overnight gaps, and gamma acceleration magnifies every point move." |
| R8 | REFUSE long swing entries in bearish regime (SPY < 50SMA, RSI < 35). Long trades in bearish regimes underperform across all tickers | Trigger: `SPY < SPY_50SMA AND RSI_14 < 35 AND trade_direction = "long"` | STOP. "Bearish market regime: no long swing entries. SPY below 50SMA + RSI < 35. Long trades underperform universally. Wait for regime improvement or trade neutral/short structures." |
| R9 | REFUSE to continue full-size trading when drawdown exceeds -20% from portfolio high. Drawdowns compound — early intervention prevents -20% from becoming -57% | Trigger: `drawdown_from_high < -0.20` in portfolio tracker | STOP. "Drawdown exceeded -20% from portfolio high. Close 50% of positions. Pause new entries for 1 week. Cascade: -10% review, -20% reduce, -30% close all." |
| R10 | REFUSE to swing trade options on individual stocks with OI < 100 or spread > 5%. Illiquid options are untradeable on multi-day swings — spread costs compound | Trigger: `underlying = "single_stock" AND (OI < 100 OR spread_pct > 5)` in options scanner | STOP. "Option liquidity insufficient for swing: OI < 100 or spread > 5%. Illiquid options compound spread costs across 2-30 days. Only trade liquid options on swing timeframe." |

## Decision Tree

```
Swing options request received
│
├─ Timeframe & Structure Selection
│  ├─ Hold 2-5 days → 21-30 DTE entry. Tight spreads. Weekly options OK. (§3.1)
│  ├─ Hold 5-10 days → 30-45 DTE entry. Theta sweet spot. (§3.1)
│  ├─ Hold 10-20 days → 45-60 DTE entry. More time for thesis. (§3.1)
│  └─ Hold 20-30 days → 60-90 DTE entry. Position trade territory. (§3.1)
│
├─ Strategy Selection by Market View
│  ├─ Bullish trend, pullback → Bull Put Spread at support (0.25-0.30Δ) (§4, §5)
│  ├─ Bearish trend, rally → Bear Call Spread at resistance (§4)
│  ├─ Strong momentum, early trend → ATM Debit Spread (§4.1)
│  ├─ Neutral, range-bound → Iron Condor (0.15-0.20Δ wings) (§4.1)
│  ├─ Sector rotation view → Sector pair: long strong, short weak (§6)
│  └─ Earnings drift → PEAD: Debit spread in surprise direction (§7.2)
│
├─ Risk Management Gate (MANDATORY)
│  ├─ Earnings within DTE? → Close before or reduce to 25%. (§7.5)
│  ├─ Weekend within DTE? → Reduce size 25-50%. (§8.6)
│  ├─ Broad market regime check → SPY vs 50SMA, VIX level. (§8.2)
│  ├─ Correlation check → New vs existing positions. (§8.7)
│  ├─ Drawdown check → -10%/-20%/-30% circuit breakers. (§8.8)
│  └─ Sizing: Half-Kelly × vol_multiplier × regime_multiplier. (§8.1-8.2)
│
└─ Exit Plan (ALL 4 defined)
   ├─ Profit target: Strategy-specific. (§8.4)
   ├─ Stop loss: Strategy-specific. (§8.5)
   ├─ Time stop: Exit at DTE threshold. (§8.6)
   └─ Thesis invalidation: What would prove the trade wrong? (§8.3)
```

## Core Workflow

### Phase 1: Weekend Prep (30-60 min, Sunday)

1. **Market regime assessment:** SPY vs 50SMA, VIX, sector RS rankings. Determine regime multiplier.
2. **Economic calendar:** Earnings, FOMC, data releases for the week. Map blackout windows.
3. **Watchlist screening:** Scan for pullbacks to MAs, sector RS shifts, earnings drift candidates.
4. **Existing position review:** Check DTE, delta drift, IV changes. Plan rolls/exits for the week.
5. **Set weekly risk budget:** Max loss for the week. Position sizing for new entries.

### Phase 2: Daily Routine (15-30 min)

1. **Market open assessment:** Overnight gaps, futures, VIX change.
2. **Monitor existing positions:** Any thesis invalidations? DTE approaching time stop?
3. **New setups:** Pullback completions, sector RS changes, earnings drift confirmations.
4. **Execute entries/exits** based on plan from Phase 1.

### Phase 3: Position Management (ongoing)

1. **Credit spreads:** Close at 50% profit. Roll at 21 DTE if still OTM.
2. **Debit spreads:** Trail profit target up as stock moves favorably. Cut at 50% loss.
3. **Iron condors:** Close at 25% of wing width profit. Adjust untested side if one side tested.
4. **Long calls/puts:** Manage aggressively — theta is enemy. Take profits at 100%+ or cut at 40% loss.

### Phase 4: Post-Trade Review (weekly)

1. **Journal all closed trades:** Entry/exit, P&L, MAE/MFE, attribution.
2. **Update win rate, avg_win, avg_loss** for Kelly sizing recalibration.
3. **Bias detection:** Disposition effect, overconfidence, revenge trading.
4. **Strategy drift check:** Are you following the plan or improvising?

## Strategy Deep Dives

### 1. Swing Timeframe Optimization

> **Reference:** swing-timeframe-optimization.md

Entry DTE must be ≥ 2× expected hold. Greek evolution across swing periods. Theta acceleration zone (DTE ≤ 21). Strike selection by conviction level.

### 2. Trend Following with Options

> **Reference:** trend-following-with-options.md

ADX-based trend phase identification. Pullback entries on MAs. Score calibration trap — high scores predict reversion. Options structures by trend phase: debit spreads for new trends, credit spreads for mature trends.

### 3. Pullback & Reversal Patterns

> **Reference:** pullback-and-reversal-patterns.md

Fibonacci-based entry zones. Support/resistance strike placement. Gap fade strategies (60-70% fill rate for common gaps). Pullback vs. reversal differentiation.

### 4. Sector Rotation

> **Reference:** sector-rotation-options.md

Economic cycle → sector → options. Relative strength analysis. Sector pair trades (market-neutral). Intermarket signals (DXY, bonds, VIX, crude). Seasonal patterns (September tightening).

### 5. Earnings Swing Playbook

> **Reference:** earnings-swing-playbook.md

Pre-earnings IV run-up (calendars, long vega). Post-earnings drift — PEAD (debit spreads). Post-earnings IV crush capture (iron condors). Earnings blackout gate.

### 6. Swing Risk Management

> **Reference:** swing-risk-management.md

Half-Kelly sizing with volatility + regime adjustments. 4-exit system. Weekend gap risk. Correlation decay. Drawdown circuit breakers.

## Research Prerequisites

**RP1 (REGIME):** SPY vs 50SMA, VIX level, sector RS rankings. Determines long/short bias and position sizing.

**RP2 (TREND ASSESSMENT):** ADX, moving averages, trend duration for each target ticker. Determines strategy type.

**RP3 (EARNINGS CALENDAR):** Any earnings within holding period for all target tickers. Triggers GR3.

**RP4 (OPTIONS LIQUIDITY):** OI > 100, spread < 5% on target strikes. Non-negotiable.

**RP5 (IV ENVIRONMENT):** IV rank/percentile. Determines debit vs credit strategy preference.

**RP6 (CORRELATION CHECK):** New position correlation with existing positions and broad portfolio.

**RP7 (SCORE CALIBRATION):** [BACKTEST-EVIDENCE] Is the ticker one where scores are inverted? Check historical score-to-outcome relationship.

**RP8 (WEEKEND GAP ASSESSMENT):** Any events over the weekend? Adjust Friday sizes accordingly.

## Error Decoder

| # | Symptom | Root Cause | Exact Fix | Lesson |
|---|---------|-----------|-----------|--------|
| E1 | "Credit spread won't hit 50% profit after 25 days" | Strike too far OTM (delta too low). Premium too small relative to time needed | Next trade: target 0.25-0.30Δ for credit spreads. 50% profit should hit within 40-50% of DTE | If the credit spread is too conservative, the premium doesn't justify the capital |
| E2 | "Stopped out of pullback entry, then it reversed and rallied to target" | Entered at first sign of pullback before support confirmed. FalseStopGuard not applied | Wait for support test AND bounce confirmation. Enter on the green candle after support holds, not during the drop | Patience on entry is as important as the entry itself. The pullback needs to prove support held |
| E3 | "Held a bull put spread through earnings — stock beat but dropped 12% on guidance" | Earnings event held at full size. Blackout gate violated | Always check earnings calendar before entry. Close directional positions before earnings or reduce to 25% | Guidance matters more than the earnings beat/miss. Binary event risk is not manageable through position sizing alone |
| E4 | "Kelly said 12% allocation — now I'm down 15% on the position and it's my entire monthly P&L" | Full Kelly sizing without half-Kelly adjustment or 5% cap | Max 5% per trade regardless of what Kelly says. Apply half-Kelly as standard. Quarter-Kelly for <$25K accounts | Kelly maximizes growth rate but produces extreme drawdowns. Constraints are survival mechanisms |
| E5 | "Sector rotation trade: long XLK call spread, short XLF call spread. XLK dropped, XLF rallied. Double loss" | Both legs were directional, not truly market-neutral. Net delta was positive | Sector pair trade: use credit spreads on both sides (bull put on strong, bear call on weak) for market-neutral delta | "Long strong, short weak" sounds market-neutral but if both are call-based, net delta can still be significant |
| E6 | "Portfolio down 35% — I kept adding because the setups were 'high probability'" | Drawdown circuit breakers not enforced. Greed/overconfidence bias | Enforce: -10% review, -20% close 50%, -30% close all, -40% full stop. These are HARD circuit breakers | Drawdowns compound faster than they recover. A 35% drawdown requires a 54% gain to break even |
| E7 | "Earnings drift trade: bought call spread on a 15% beat. Stock drifted down for 2 weeks. Lost 100%" | PEAD requires post-earnings price confirmation. Bought before confirming drift direction | Enter PEAD 1-3 days AFTER earnings. Stock must continue in surprise direction. Gap must not fade within 3 days | The earnings surprise direction is NOT the drift direction. The market's post-earnings reaction defines the drift |

## Anti-Hallucination

**[VERIFIED]** — CBOE/OCC specifications, SEC filings, peer-reviewed research.
**[COMPUTED]** — Black-Scholes/model-derived with stated assumptions.
**[ESTIMATED]** — Practitioner ranges with uncertainty acknowledged.
**[COMMON-PRACTICE]** — Professional swing trading methodology, not codified in exchange rules.
**[BACKTEST-EVIDENCE]** — Trading project 1,068-trade backtest across 11 tickers.

**Kelly sizing depends on accurate inputs.** Win rate and win/loss ratio estimates from small samples (< 50 trades) are unreliable. Use conservative defaults when historical data is sparse.

## Cross-Skill Coordination

### Upstream

| Skill | What to Request | Decision Gate |
|-------|----------------|---------------|
| `technical-signals-engineer` | ADX, RSI, moving averages, support/resistance, volume profile | Is there a valid technical setup for swing entry? |
| `options-strategist` | Standard strategy construction, Greeks analysis | Does the selected structure fit the thesis? |
| `fundamental-analyst` | Earnings dates, sector cycle assessment, company outlook | Is the fundamental backdrop supportive of the trade direction? |
| `quantitative-analyst` | IV rank, HV percentile, correlation matrix, Kelly inputs | Is the vol environment favorable? |

### Downstream

| Skill | When to Hand Off | Handoff Format |
|-------|-----------------|----------------|
| `portfolio-signal-manager` | Swing position ready for portfolio integration | "Swing position: [ticker], [structure], [size], [delta], [correlation_to_portfolio], [risk_amount], [holding_period]" |
| `algorithmic-trader` | Swing strategy ready for automation | "Swing automation: [setup conditions], [entry rules], [exit rules], [risk parameters]" |
| `trade-performance-analyst` | Swing trades completed — journal | "Swing closed: [strategy], [entry/exit], [P&L], [MAE/MFE], [bias flags], [attribution]" |
| `leaps-strategist` | Swing timeframe extending → consider LEAPS as core position | "LEAPS evaluation: [ticker], [long-term view], [capital available], [swing history]" |

## What Good Looks Like

**Bull Put Spread Pullback (GOOD):** SPY uptrend confirmed (weekly: price > 20SMA, 20SMA > 50SMA). Daily: price pulled back to 20SMA. RSI = 45 (reset). Volume < average on pullback. Entry: Sell $495/$490 bull put spread, 35 DTE, $1.20 credit. Target: close at $0.60 (50% profit). Stop: $2.40 (2× credit). Time stop: 14 DTE. Result: Target hit in 12 days. P&L: +$120/contract.

**Earnings PEAD (GOOD):** Stock beat EPS by 8%, gapped up 4%, held gap for 3 days, above-average volume. Entry: Buy ATM $105/$110 call spread, 40 DTE, $2.50 debit. Target: $5.00 (100%). Stop: $1.25 (50% loss). Time stop: 14 DTE. Result: Target hit in 15 days as drift continued. P&L: +$250/contract.

**Sector Pair Trade (GOOD):** XLK RS rising 6 weeks. XLE RS falling 6 weeks. Entry: Sell XLK $210/$205 bull put + sell XLE $95/$100 bear call. Net credit: $1.80. Combined delta: ~0.02 (market-neutral). Target: 50% ($0.90). Stop: 2× credit ($3.60). Result: Both expired OTM. Full credit collected. P&L: +$180/contract pair.

## Operating at Different Levels

| Level | Scope | Key Capability |
|-------|-------|----------------|
| **L1: Apprentice** | Execute bull put/bear call spreads on SPY pullbacks following the multi-timeframe confirmation. Use pre-calculated sizing | Knows: DTE selection, 4-exit system, earnings blackout. Doesn't know: sector rotation, PEAD, Kelly sizing |
| **L2: Practitioner** | Independently trade trend-following pullbacks, sector rotations, and earnings drift. Apply Kelly sizing and regime adjustments | Adds: sector analysis, PEAD, half-Kelly sizing, broad market regime gate |
| **L3: Specialist** | Build multi-strategy swing portfolio with correlation-aware sizing. Navigate earnings seasons with pre/post strategies. Sector pair trades | Adds: portfolio correlation management, earnings season playbook, intermarket analysis |
| **L4: Architect** | Design systematic swing options programs. Walk-forward optimization of entry/exit parameters. Multi-underlying portfolio with dynamic sizing | Adds: systematic strategy design, walk-forward testing, dynamic portfolio sizing |
| **L5: Transformative** | Publish swing options research. Define industry best practices. Create new swing strategy frameworks | Adds: research leadership, strategy innovation, industry influence |

## Anti-Patterns

| ❌ Common Mistake | ✅ Correct Approach |
|-------------------|-------------------|
| "The trend is strong (score 92) — I'll size up on this pullback entry" | [BACKTEST-EVIDENCE] High scores predict mean reversion. Size based on trend duration and pullback depth, not score |
| "I'll let this credit spread expire — it's so far OTM" | Close at 50% of credit. Expiration risk (pin, gamma, assignment) is not worth the last few dollars |
| "The bull put spread has been winning 8 out of 10 times — I'll increase allocation" | Win streaks are followed by loss clusters. Keep sizing consistent. Overconfidence after streaks is the top predictor of blow-ups |
| "Sector rotation is working — I'll add 3 more sector pairs" | Correlation between sector pairs increases with position count. Each additional pair has diminishing diversification benefit |
| "The stock beat earnings by 20% — I'll buy calls at the open" | PEAD requires waiting for post-earnings price confirmation. Immediate entry on the gap is gambling on momentum continuation, not drift |
| "Half-Kelly is too conservative — I have a 60% win rate" | Half-Kelly is not about win rate. It's about surviving the loss clusters that full Kelly can't. A 60% WR strategy still has 10%+ chance of 5+ consecutive losses |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Bull put spread held through earnings because "the company always beats." Stock beats on EPS, drops 12% on guidance. Full 2-month swing profit wiped in one overnight gap | $2K-$8K per position — a single earnings gap costs 6-12 winning trades at typical swing profit targets | Always check earnings calendar before entry. Close directional positions before earnings or reduce to 25%. No exceptions — binary events are unmanageable by position sizing |
| Credit spread allowed to expire because "it's so far OTM" — stock pins the short strike in the final 30 minutes, gamma explosion makes the position unhedgeable, assigned on 1,000 shares | $3K-$15K per incident — pin risk plus weekend gap on assigned shares creates unbounded loss from a "defined" risk trade | Close at 50% of max profit. The last few dollars are not worth gamma/pin/assignment risk. Credit spread winners should be harvested early, not held to expiration |
| Swing entry score = 92, sizing doubled because "high conviction." Score calibration is inverted — high scores predict mean reversion, not continuation. Stock reverses, -25% on oversized position | $3K-$10K per trade — conviction-based sizing amplifies losses on trades that were always likely to fail | [BACKTEST-EVIDENCE] Size based on trend duration and pullback depth, NOT entry score. High scores (>85) → REDUCE size by 25%. Score predicts direction; trend duration determines conviction |
| 6 consecutive wins, then sizing increased because "the system works." 3 consecutive losses at 2× size wipe the 6 wins plus additional capital | $5K-$20K in account drawdown — overconfidence after streaks is the #1 predictor of blown swing accounts | Fixed sizing regardless of streak length. After 3 consecutive wins, actually REDUCE size by 25%. Win streaks revert to mean — the probability of the next trade being a winner doesn't increase because the last 6 were |
| Portfolio: 5 swing positions across 5 sectors for "diversification." A broad market sell-off makes all 5 positions lose simultaneously because crash correlation = 0.7-0.9 | $5K-$25K in portfolio drawdown — sector diversification provides zero protection during broad sell-offs | Enforce portfolio correlation limit: no more than 60% of swing capital in correlated positions. Assume crash correlation of 0.7-0.9 for all equity positions. Diversification fails in crashes |
| Holding a DTE 5 option over the weekend. Monday gap was 2.5× normal overnight gap. Gamma acceleration made the option move 3× the underlying move | $1K-$3K per incident — weekend gap + gamma acceleration = compound risk that standard stops can't handle | If DTE ≤ 7 and holding over weekend: reduce size 25-50%, add 10% to stop buffer. Weekend gaps are 2-3× larger than weekday overnight gaps |
| Half-Kelly says 12% allocation. Applied without the 5% cap. Position loses 15% — now down 1.8% of portfolio from one trade, and it's the first of a 5-loss cluster | $3K-$10K per drawdown cycle — full Kelly maximizes growth rate but produces extreme drawdowns that most traders can't stomach | Max 5% per trade regardless of Kelly output. Apply half-Kelly as standard. Quarter-Kelly for accounts < $25K. Kelly constraints are survival mechanisms |

## Production Checklist

Before ANY swing options trade:

- [ ] 1. **Entry DTE ≥ 2× hold period:** 10-day swing = 21+ DTE entry. 21-day swing = 45+ DTE.
- [ ] 2. **Earnings calendar checked:** No earnings within holding period OR position reduced to 25%.
- [ ] 3. **Broad market regime assessed:** SPY vs 50SMA, VIX, regime multiplier applied.
- [ ] 4. **Multi-timeframe confirmed:** Weekly bias + daily setup + 4H entry timing aligned.
- [ ] 5. **Options liquidity verified:** OI > 100, spread < 5%. Native spread orders only.
- [ ] 6. **4-exit plan documented:** Profit target, stop loss, time stop, thesis invalidation.
- [ ] 7. **Asymmetric exit ratio verified:** ≥ 2:1 reward-to-risk on directional trades.
- [ ] 8. **Half-Kelly sizing calculated:** With vol_multiplier and regime_multiplier. ≤ 5% max per trade.
- [ ] 9. **Correlation check passed:** New position doesn't over-concentrate portfolio.
- [ ] 10. **Drawdown circuit breakers set:** -10% review, -20% reduce, -30% close all.
- [ ] 11. **Weekend gap plan:** If holding through weekend, size reduced and stop adjusted.
- [ ] 12. **Score used directionally, not for conviction:** Score determines direction. Trend duration determines size.
- [ ] 13. **IV environment favorable:** Credit spreads when IV > HV. Debit spreads when IV < HV.
- [ ] 14. **September/October sizing:** If these months, reduce all sizes by 50%.
- [ ] 15. **Journal template ready:** Entry thesis, expected vs. actual, bias check, lessons.

## References

| Reference | Covers | When to Read |
|-----------|--------|-------------|
| `swing-timeframe-optimization.md` | DTE selection, Greek evolution, strike selection, multi-timeframe | Before any swing trade entry |
| `trend-following-with-options.md` | ADX phases, pullback entries, score calibration, earnings blackout | For trend-following setups |
| `pullback-and-reversal-patterns.md` | Fibonacci zones, support/resistance, gap strategies, reversal confirmation | For counter-trend entries |
| `sector-rotation-options.md` | Economic cycle map, RS analysis, sector pairs, intermarket, seasonals | For sector-based swing trades |
| `earnings-swing-playbook.md` | Pre-earnings IV, PEAD, IV crush capture, blackout gate | During earnings season |
| `swing-risk-management.md` | Kelly sizing, 4-exit system, weekend gaps, correlation, drawdown management | Portfolio-level risk management |
| `regime-adaptation-for-swing.md` | Regime classifier, September/October adjustments, VIX-based sizing, broad market gate | At session start — 30-second regime check before any trade |
| `behavioral-bias-in-swing-trading.md` | Disposition effect, revenge trading, anchoring, overconfidence, loss aversion detection rules | Weekly review — bias detection from trade journal |

**Cross-reference skills:** `options-strategist` (standard structures), `intraday-options-trader` (same-day), `leaps-strategist` (multi-year), `technical-signals-engineer` (indicators), `options-risk-engineer` (portfolio risk).

---

*Skill complete. Route same-day trading to `intraday-options-trader`. Route multi-year to `leaps-strategist`. Route complex multi-leg to `advanced-options-structures`.*
