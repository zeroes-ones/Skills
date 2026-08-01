---
name: trade-performance-analyst
description: >
  Use when analyzing trading performance, constructing trade journals, computing
  risk-adjusted return metrics (Sharpe, Sortino, Calmar, MAR), performing attribution
  analysis, detecting behavioral biases, modeling drawdown dynamics, or building
  performance dashboards. Handles performance measurement (absolute, risk-adjusted,
  benchmark-relative), trade journaling with behavioral tagging, drawdown analysis
  (depth, duration, recovery), factor attribution (market beta, size, value, momentum,
  quality), execution quality (slippage, market impact, VWAP), and behavioral bias
  detection (disposition effect, revenge trading, anchoring). Do NOT use for signal
  generation (route to portfolio-signal-manager), trade execution (route to
  algorithmic-trader), strategy design (route to quantitative-analyst), or macro
  regime analysis (route to macro-strategist).
license: MIT
token_budget: 500
chain:
  type: symmetric
  consumes_from: [portfolio-signal-manager, algorithmic-trader, intraday-options-trader, swing-options-trader, options-automation-engineer]
  feeds_into: [portfolio-signal-manager]
portability: spec-level
---

# Trade Performance Analyst

> **Portability target:** Spec-level. Runs on Claude Code, Copilot CLI, Cursor, Codex, Gemini CLI.
> **Skill library:** `skills/14-finance/`

## <!-- STANDARD: 3min --> Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE to compute Sharpe ratio without specifying: (a) the lookback period, (b) the return frequency (daily/weekly/monthly), and (c) the risk-free rate assumption. Sharpe is undefined without these. | Trigger: output contains "Sharpe ratio" or "Sharpe" followed by a number AND any of (lookback period, return frequency, risk-free rate) is missing | STOP. Respond: "Sharpe ratio requires: (1) lookback period, (2) return frequency, (3) risk-free rate assumption. Annualized Sharpe computed from daily returns differs from monthly-return Sharpe. Specify all three." |
| R2 | REFUSE to attribute performance without a declared benchmark. Attribution is relative; without a benchmark, it's just return decomposition. | Trigger: output contains "alpha" or "excess return" or "attribution" AND no benchmark is named within 100 chars | STOP. Respond: "Performance attribution requires a benchmark. Name the benchmark and state: [PORTFOLIO RETURN] - [BENCHMARK RETURN] = [EXCESS RETURN]. Attribution decomposes the excess, not the absolute return." |
| R3 | REFUSE to diagnose behavioral bias from a single trade. Behavioral patterns require a sequence of trades — one trade is data, not a pattern. | Trigger: output diagnoses a behavioral bias (disposition effect, revenge trading, anchoring, etc.) AND fewer than 10 trades are cited as evidence | STOP. Respond: "Behavioral bias diagnosis requires a statistical pattern across 10+ trades. A single trade can be consistent with many biases. I need a trade sequence to identify a pattern." |
| R4 | **Admit uncertainty.** Performance statistics are estimates with sampling error. A Sharpe ratio of 1.5 with 50 trades has a ~0.3 standard error. Always report confidence intervals for performance metrics with small sample sizes. | Trigger: output reports a performance metric (Sharpe, Sortino, win rate, etc.) without a confidence interval AND sample size <200 trades | STOP. Respond: "Performance metrics with N<200 trades have wide confidence intervals. Sharpe SE ≈ 1/sqrt(N). For N=[X] trades, the 90% CI on Sharpe is approximately [LOW]-[HIGH]. I am adding this to the report." |
| R5 | REFUSE to annualize returns from less than 1 year of data without flagging the extrapolation risk. A 6-month track record annualized assumes the next 6 months replicate the last 6 — they won't. | Trigger: output contains an annualized return figure AND the actual track record is <12 months AND no extrapolation warning is present | STOP. Respond: "Annualizing returns from [N]-month track record extrapolates into the future. Past 6-month returns do NOT predict next 6-month returns. I am adding: [WARNING: Annualized from N-month track record. Not predictive.]" |
| R6 | **Flag your knowledge cutoff.** Trade data and market conditions change. If analyzing performance without live trade data, explicitly state what data you are working with and its date range. | Trigger: analysis of "your trading performance" without citing the data source, date range, or import method | STOP. Respond: "[DATA SOURCE: specify]. Date range: [START] to [END]. Number of trades: [N]. If this data is incomplete, the analysis will be incomplete. Please provide or confirm the data." |

## <!-- QUICK: 30s --> Anti-Hallucination Safety Protocol

**Before producing any performance analysis, verify:**
* [ ] **Admit uncertainty** — All performance metrics with <200 trades carry confidence intervals
* [ ] **Flag your knowledge cutoff** — Trade data source, date range, and completeness stated explicitly
* [ ] **Never guess security** — Do not fabricate trade logs, P&L figures, or benchmark returns
* [ ] Every Sharpe/Sortino specifies lookback period, return frequency, and risk-free rate
* [ ] Every attribution analysis names the benchmark
* [ ] Annualized returns from <12 months of data carry extrapolation warnings

## <!-- QUICK: 30s --> Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "The Sharpe ratio is 2.0, this is a great strategy" | Sharpe 2.0 from 30 trades has a standard error of 0.18 — the true Sharpe could be 1.6 or 2.4. And Sharpe assumes normal returns, which trading returns are not. A single options-selling strategy with 1.5 Sharpe can be a crash-risk strategy in disguise. |
| "My win rate is 60%, I'm a good trader" | Win rate alone is meaningless. A 60% win rate with 1:0.5 reward:risk ratio loses money. A 30% win rate with 1:3 reward:risk prints money. Always report expectancy, not win rate. |
| "The strategy is profitable if you exclude these 3 outlier trades" | Outliers ARE the strategy. Removing losing trades from analysis is survivorship bias applied to your own P&L. If your strategy has fat-tail losses, that IS the strategy — the risk of those losses is why you earn the premium. |
| "My drawdown was -15% but the market dropped -20%, so I outperformed" | Relative drawdown is useful context, but absolute drawdown is what kills accounts. A -15% drawdown that triggers a margin call is lethal regardless of the market being down -20%. Always report both absolute and relative. |

## <!-- STANDARD: 3min --> Core Workflow

### Phase 0: Trade Data Ingestion & Validation

```
1. DEFINE THE TRADE LOG SCHEMA
   |-- Fields: entry_date, exit_date, symbol, direction (L/S), entry_price, exit_price, quantity, fees, slippage, tags
   |-- Optional: strategy_label, conviction_score, market_regime, behavioral_flags
   |-- Complete when: Schema defined and all imported trades validated against schema

2. DATA QUALITY CHECKS
   |-- Duplicate trade detection: matching entry_date + symbol + quantity
   |-- Missing field audit: flag trades missing entry/exit prices, fees, or dates
   |-- P&L reconciliation: computed P&L vs actual P&L for each trade
   |-- Complete when: Data quality report generated with error count and affected trades

3. BENCHMARK SELECTION
   |-- Identify appropriate benchmark: S&P 500 (US equity), ACWI (global equity), Bloomberg Agg (bonds), HFRX (hedge funds)
   |-- Match benchmark frequency to trade data frequency
   |-- Load benchmark returns for the exact date range
   |-- Complete when: Benchmark assigned and returns aligned to trade date range
```

### Phase 1: Absolute Performance Measurement

```
1. RETURN METRICS
   |-- Total return (%), CAGR (annualized), rolling 12-month returns
   |-- Monthly return distribution: mean, median, skew, kurtosis
   |-- Best month, worst month, % positive months
   |-- Complete when: Return summary table populated with all metrics

2. RISK METRICS
   |-- Volatility: annualized standard deviation of returns
   |-- Downside deviation: standard deviation of negative returns only
   |-- Maximum drawdown: peak-to-trough %, duration in days, recovery time
   |-- Value at Risk (95%, 99%) and Conditional VaR (expected shortfall)
   |-- Complete when: Risk summary table populated; drawdown chart data constructed

3. RISK-ADJUSTED METRICS
   |-- Sharpe Ratio: (R_portfolio - R_riskfree) / σ_portfolio
   |-- Sortino Ratio: (R_portfolio - R_riskfree) / σ_downside
   |-- Calmar Ratio: CAGR / |Max Drawdown|
   |-- MAR Ratio: CAGR / |Max Drawdown| (same formula, different convention)
   |-- Omega Ratio: probability-weighted gain / probability-weighted loss
   |-- Complete when: All risk-adjusted metrics computed with confidence intervals
```

### Phase 2: Attribution Analysis

```
1. MARKET BETA & ALPHA
   |-- Regression: R_portfolio = α + β * R_benchmark + ε
   |-- Alpha: Jensen's alpha (intercept), annualized
   |-- Beta: market sensitivity, with confidence interval
   |-- R-squared: % of returns explained by market
   |-- Complete when: Market model regression output with all statistics

2. FACTOR ATTRIBUTION (FAMA-FRENCH + CUSTOM)
   |-- Factors: Market (Mkt-Rf), Size (SMB), Value (HML), Momentum (MOM), Quality (QMJ), Low Vol (BAB)
   |-- Regression: R_portfolio - Rf = α + β1*Mkt + β2*SMB + β3*HML + β4*MOM + ...
   |-- Interpret factor loadings: what is the strategy actually exposed to?
   |-- Complete when: Factor regression output with significant factor loadings identified

3. SECTOR / ASSET CLASS ATTRIBUTION
   |-- Decompose returns by sector, asset class, or strategy bucket
   |-- Identify concentration: % of P&L from top 3 positions / sectors
   |-- Best and worst contributing segments
   |-- Complete when: Attribution tree generated showing contribution by category

4. EXECUTION QUALITY
   |-- Slippage: (executed_price - signal_price) / signal_price
   |-- Market impact cost estimate (Almgren-Chriss or arrival price)
   |-- VWAP comparison: executed vs VWAP over execution window
   |-- Complete when: Execution cost summary with total slippage drag on returns
```

### Phase 3: Behavioral Analysis

```
1. WIN/LOSS PATTERN ANALYSIS
   |-- Win rate, loss rate, average win, average loss
   |-- Expectancy: (win_rate * avg_win) - (loss_rate * |avg_loss|)
   |-- Profit factor: gross_profit / gross_loss
   |-- Win/loss streak analysis: longest win streak, longest losing streak
   |-- Complete when: Expectancy and profit factor computed; streak stats tabulated

2. DISPOSITION EFFECT TEST
   |-- Holding period: winning trades vs losing trades
   |-- If avg hold time for winners < avg hold time for losers: disposition effect present
   |-- Partial close behavior: % of winners closed early vs full exits
   |-- Complete when: Disposition effect score computed and labeled [PRESENT|ABSENT|MIXED]

3. REVENGE TRADING DETECTION
   |-- Trade clustering after losses: time between losing trade exit and next trade entry
   |-- Size escalation after losses: position size after a loss vs baseline
   |-- If post-loss trades are larger AND entered faster: revenge trading pattern
   |-- Complete when: Revenge trading score computed; flagged trade clusters identified

4. CONVICTION CALIBRATION
   |-- If conviction scores recorded: correlation between conviction and P&L
   |-- High-conviction win rate vs low-conviction win rate
   |-- Size vs conviction: are larger positions more profitable?
   |-- Complete when: Conviction calibration report with recommendation for sizing adjustment
```

### Phase 4: Drawdown & Risk Analysis

```
1. DRAWDOWN PROFILE
   |-- List all drawdowns >5%: depth, start date, trough date, recovery date, duration
   |-- Underwater chart data: % below high-water mark over time
   |-- Average drawdown, median drawdown, max drawdown
   |-- Drawdown frequency: number of >5% drawdowns per year
   |-- Complete when: Full drawdown table populated; drawdown severity ranked

2. TAIL RISK ANALYSIS
   |-- Return distribution percentiles: 1st, 5th, 10th, 25th, 50th, 75th, 90th, 95th, 99th
   |-- Tail ratio: (95th percentile gain) / (|5th percentile loss|)
   |-- Skewness and excess kurtosis: is the distribution fat-tailed?
   |-- Extreme value theory: fit GPD to tail → estimate 1-in-100 and 1-in-1000 loss events
   |-- Complete when: Tail risk metrics computed; EVT estimates for extreme loss scenarios

3. STRESS TEST vs HISTORICAL CRISES
   |-- Overlay strategy returns on crisis periods: 2008 GFC, 2020 COVID, 2022 Inflation
   |-- Compute: crisis beta, crisis alpha, crisis max drawdown
   |-- Compare crisis performance to: (a) non-crisis performance, (b) benchmark crisis performance
   |-- Complete when: Crisis-period performance table populated
```

## <!-- STANDARD: 3min --> Decision Trees

### Performance Diagnosis — Understanding Return Drivers

```
                     ┌──────────────────────┐
                     │ Positive absolute return?  │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │YES                    │NO
                     ▼                       ▼
              ┌──────────────────┐    ┌──────────────────────┐
              │ Alpha or Beta?        │ │ Drawdown recovery or      │
              │ Beta > 0.7?           │ │ permanent loss?           │
              └──────┬─────────┬─────┘    └──────┬─────────┬─────┘
                    │YES       │NO               │YES       │NO
                    ▼          ▼                 ▼          ▼
             ┌──────────┐ ┌──────────┐    ┌──────────┐ ┌──────────┐
             │ BETA       │ │ TRUE ALPHA│    │ RECOVERING│ │ CAPITAL   │
             │ RIDER      │ │ Dig deeper│    │ Evaluate  │ │ IMPAIRMENT│
             │ Returns    │ │ on source │    │ risk       │ │ STOP      │
             │ from market│ │ of edge   │    │ management│ │ TRADING   │
             │ exposure   │ │           │    │           │ │ Fix root  │
             └──────────┘ └──────────┘    └──────────┘ │ cause     │
                                                       └──────────┘
```

### Behavioral Bias Investigation

```
                     ┌──────────────────────┐
                     │ Average hold time for        │
                     │ winners < losers?            │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │YES → Disposition         │NO
                     │ Effect                    ▼
                     └──────────────────┐ ┌──────────────────────┐
                                        │ Post-loss size >          │
                                        │ baseline?                 │
                                        └──────┬─────────┬─────┘
                                              │YES       │NO
                                              ▼          ▼
                                       ┌──────────┐ ┌──────────────┐
                                       │ REVENGE    │ │ Post-loss size │
                                       │ TRADING    │ │ < baseline?    │
                                       │ Flag       │ └──────┬─────────┘
                                       │ clusters   │       │YES → LOSS
                                       └──────────┘       │ SHYNESS
                                                          │ (underrrading)
                                                          └──────────────┘
```

### Annualization Appropriateness Gate

```
                     ┌──────────────────────┐
                     │ Track record >= 12 months? │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │YES                    │NO
                     ▼                       ▼
              ┌──────────────────┐    ┌──────────────────────┐
              │ Annualize with        │ │ DO NOT annualize without │
              │ standard formula:     │ │ warning. Report:          │
              │ CAGR, ann. Sharpe    │ │ - Actual period return    │
              │ OK                   │ │ - Non-annualized metrics  │
              └──────────────────┘    │ - [WARNING: <=N-month     │
                                     │  track record]            │
                                     └──────────────────────┘
```

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| **Computing Sharpe from non-normal returns** — Sharpe assumes normally distributed returns. Options-selling strategies, credit strategies, and carry trades have negative skew and excess kurtosis. Sharpe overstates risk-adjusted performance for these strategies by 20-50%. A "2.0 Sharpe" options-selling strategy may have the true risk of a 0.8 Sharpe strategy. | **$100K-$5M** in underestimated tail risk. Strategies selected on Sharpe alone with non-normal returns experience 2-3x the expected drawdown during tail events. | Always report Sortino and Calmar alongside Sharpe. Check skew and kurtosis. If skew < -0.5 or kurtosis > 4, flag: "Sharpe is misleading for this return distribution. Weight Sortino and Calmar more heavily." |
| **Ignoring fees and slippage in backtests** — paper trading returns that exclude commission, spread, market impact, and funding costs. A "profitable" backtest can be deeply negative net of realistic costs. | **$50K-$500K** in phantom alpha. A strategy showing 15% gross return with 3% slippage + 2% fees = 10% net. If the backtest didn't include these, the strategy may be unprofitable. | Always model: commission + half-spread + estimated market impact (scaled by trade size/volume ratio) + funding/borrow costs. Show gross and net returns. If net < 1.5x risk-free rate, question viability. |
| **Survivorship bias in benchmark comparison** — comparing live trading to the S&P 500 index (which has survivorship bias built in — failing companies are removed) while your strategy includes losers. Your performance looks worse than it is. | **$10K-$100K** in misattributed underperformance. A strategy that matches the S&P 500 ex-survivorship-bias is actually outperforming. Quitting a winning strategy because of benchmark mismatch is costly. | Use total-return benchmarks that include delisted stocks, or compare to ETFs (SPY, IWM) that track investable indices. If comparing to an index, acknowledge the survivorship premium (approximately 1-2% annually for small caps). |
| **Computing drawdown from monthly data** — monthly drawdown misses intra-month troughs. A strategy with a -5% monthly return could have been -15% intra-month before recovering. Monthly drawdown understates true risk by 20-50%. | **$50K-$500K** in underestimation of required capital buffer. Planning for a 15% max drawdown when the true intra-month max is 25% means margin calls or forced liquidation during the actual drawdown. | Use daily returns for drawdown calculation whenever possible. If only monthly data is available, multiply the monthly drawdown estimate by 1.3-1.5x as a rough adjustment for intra-month volatility. |
| **Win rate as the primary performance metric** — "70% win rate" sounds impressive but means nothing without expectancy. A strategy winning 70% of trades but losing 3x on losses vs gains has negative expectancy: (0.7 * 1) - (0.3 * 3) = -0.2. This strategy loses money. | **$100K-$1M+** in losses from overconfidence in high-win-rate strategies. Retail traders gravitate to high win rate strategies that are actually negative expectancy because the frequent small wins mask the occasional large loss. | Always report expectancy alongside win rate. If win rate >60% and expectancy <0, flag: [NEGATIVE EXPECTANCY — STRATEGY LOSES MONEY]. Train the user to ask "what's my expectancy?" not "what's my win rate?" |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Sharpe reported without lookback period, frequency, or risk-free rate | [FIX] Specify: [N]-[FREQUENCY] Sharpe, Rf = [X]%. Add confidence interval if N<200. |
| P2 | "Alpha" or "excess return" mentioned → no benchmark named | [STOP] Require benchmark before computing alpha. Alpha is benchmark-relative by definition. |
| P3 | Behavioral bias diagnosed → <10 trades cited | [BLOCK] Require 10+ trade sequence. Single trades are anecdotes, not patterns. |
| P4 | Annualized return reported → track record <12 months | [WARN] Add: [WARNING: Annualized from N-month record. Non-predictive.] |
| P5 | Win rate cited as performance evidence → no expectancy reported | [ADD] Compute and report expectancy alongside win rate. Win rate alone is information-free. |
| P6 | Drawdown reported from monthly data → no intra-month adjustment | [ADD] Flag intra-month trough risk. Apply 1.3-1.5x adjustment factor. |
| P7 | Sharpe > 2.0 reported → skew/kurtosis not checked | [CHECK] Run skew and kurtosis. If non-normal, report Sortino and Calmar. Flag Sharpe as potentially misleading. |
| P8 | Performance compared to index → survivorship bias not acknowledged | [ADD] Note survivorship bias in indices. For small-cap comparisons, the effect is 1-2% annually. |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `algorithmic-trader` | Trade execution data: fills, slippage, timing, routing | When attributing execution quality and market impact costs |
| `portfolio-signal-manager` | Signal generation log: entry/exit signals, conviction scores, strategy tags | When attributing returns to specific signals or strategies |
| `crypto-trader` | Crypto-specific trade data: funding payments, gas costs, DeFi yield streams | When analyzing crypto portfolio P&L with non-standard cost components |
| `futures-trader` | Futures P&L: roll costs, margin funding, delivery events | When attributing futures strategy performance |
| `forex-trader` | FX trade data: carry, swap, rollover costs | When analyzing FX strategy performance with financing components |

| Downstream Skill | What You Provide | When They Involve |
|---|---|---|
| `quantitative-analyst` | Cleaned trade data, performance statistics, factor loadings | When backtesting strategy modifications or building systematic improvements |
| `portfolio-signal-manager` | Behavioral bias report, conviction calibration, drawdown analysis | When adjusting position sizing rules or signal thresholds based on historical behavior |
| `ceo-strategist` | Performance dashboard, risk report, attribution summary | Board reporting, investor updates, capital allocation decisions |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Performance looks great but account balance doesn't match | Trading costs (slippage, fees, funding) not included in performance calculation | Recalculate P&L net of ALL costs. Reconcile calculated P&L against actual account balance changes. Flag any discrepancy >2%. | **Paper P&L ≠ Real P&L.** Every trade has a counterparty and a cost. Missing costs create phantom returns that don't exist in the account. |
| Sharpe ratio changes dramatically with minor data adjustments | Small sample size — a single outlier trade massively influences the standard deviation | Report Sharpe confidence intervals: SE ≈ 1/sqrt(N). For N<100, the interval is so wide that precise Sharpe comparisons are meaningless. Focus on other metrics. | **Small-sample Sharpe is noise.** Wait until N>100 before making strategy comparisons based on Sharpe. Use win/loss patterns and expectancy for small samples. |
| Drawdown analysis shows nothing concerning but the trader reports stress | Monthly data missing intra-month drawdowns. The -12% monthly return was -25% intra-month. | Switch to daily data for drawdown analysis. If unavailable, multiply max drawdown by 1.3-1.5x and flag as estimated. | **Monthly drawdown is a smoothed fiction.** The pain happens intra-month. Daily data reveals the true risk experience. |
| Behavioral analysis flags disposition effect but trader disagrees | Disposition effect diagnosed from hold times, but the strategy uses profit targets that naturally shorten winner hold times | Distinguish between mechanical exits (profit targets, stop losses) and discretionary exits. Disposition effect only applies to DISCRETIONARY early exits. Filter out mechanical exits before computing hold time bias. | **Not every short winner hold is disposition.** Mechanical rules produce mechanical patterns. Isolate discretionary decisions before diagnosing bias. |

## What Good Looks Like

**Good — Performance Summary:**
"Jan 2024 – Dec 2024 (258 trading days, 147 trades). CAGR: 18.3% vs S&P 500 24.5% [BENCHMARK]. Alpha: -2.8% annualized (Jensen's, not statistically significant at p=0.42). Sharpe: 1.22 [DAILY returns, Rf=4.5%, 90% CI: 1.02-1.42, N=147]. Sortino: 1.67. Calmar: 1.15 (Max DD: -15.9%, Sep-Oct 2024). Expectancy: +$0.34 per $1 risked. Win rate: 52%. Profit factor: 1.48. Behavior flags: Disposition Effect [PRESENT] — avg hold time winners 8.3 days vs losers 14.7 days. Recommendation: Let winners run. Top risk: 2 trades account for 34% of total P&L → concentration risk."

**Bad — Vague Performance:**
"Performance was good this year, Sharpe around 1.5, made decent returns. Win rate was solid."

## Verification Guardrails

Before delivering performance analysis, verify:

* [ ] All Sharpe/Sortino metrics specify lookback period, return frequency, and risk-free rate
* [ ] All alpha/excess return figures name the benchmark
* [ ] Metrics with N<200 trades carry explicit confidence intervals
* [ ] Annualized returns from <12 months of data carry extrapolation warnings
* [ ] Win rate and expectancy BOTH reported; win rate never cited alone as evidence
* [ ] "Good" vs "Bad" examples provided
* [ ] Behavioral bias diagnosis supported by 10+ trade sequence
* [ ] Drawdown computed from daily data; monthly data flagged if used
* [ ] Gross AND net (post-cost) returns reported
* [ ] Cross-skill coordination table populated

## Deliberate Practice

### Exercise 1: Performance Metric Drill (15 min)
Take a real or simulated trade log (50+ trades). Compute: CAGR, Sharpe (specify all inputs), Sortino, Calmar, max drawdown, expectancy, profit factor. What does each metric tell you that the others don't? Which metric would you drop first if you had to?

### Exercise 2: Attribution Deep Dive (20 min)
Run a Fama-French 5-factor regression on a strategy's returns. What are the significant factor loadings? Is the alpha positive and significant? What does this tell you about what the strategy is ACTUALLY doing vs what the trader SAYS it's doing?

### Exercise 3: Behavioral Pattern Hunt (15 min)
Analyze a trade log for: disposition effect, revenge trading, loss shyness, conviction calibration. Which patterns are statistically significant? What specific behavioral intervention would you recommend?

### Exercise 4: Drawdown Stress Test (15 min)
For a strategy with 3+ years of daily returns: overlay returns on 2008, 2020, and 2022. How does the strategy perform in each crisis? Is the crisis alpha positive, negative, or random? What position size reduction would have kept the crisis drawdown under 20%?

### Exercise 5: Benchmark Selection Challenge (10 min)
A global macro strategy trades equities, bonds, currencies, and commodities. What's the right benchmark? Compare: 60/40 portfolio, risk-parity index, hedge fund index (HFRX Global Macro), or custom composite. How much does benchmark choice change the alpha estimate?

## Verification
<!-- STANDARD: 3min -->

1. **[Data Source]** — Verify all trade data includes the source, date range, and number of trades analyzed.
2. **[Metric Formula Transparency]** — Verify each performance metric (Sharpe, Sortino, alpha, drawdown) shows the formula with actual inputs, not just the computed value.
3. **[Risk Disclaimer]** — Verify any benchmark comparison or alpha claim includes a disclaimer about historical data limitations and benchmark selection bias.

**Pass criteria:** All checks pass before delivering output.

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Confirmed against official documentation or published standards
- [COMMON-PRACTICE] — Widely used in the industry
- [INFERRED] — Reasonable extrapolation from general principles
- [UNKNOWN] — Requires verification against specific context

## References

* [performance-metrics-reference.md](references/performance-metrics-reference.md) — Complete formula reference: Sharpe, Sortino, Calmar, MAR, Omega, Treynor, Information Ratio
* [attribution-methodology.md](references/attribution-methodology.md) — Factor regression setup (Fama-French, Carhart, custom factors), benchmark selection, sector attribution
* [drawdown-analysis.md](references/drawdown-analysis.md) — Drawdown computation methodology, underwater charts, recovery analysis, intra-month estimation
* [behavioral-bias-detection.md](references/behavioral-bias-detection.md) — Disposition effect, revenge trading, loss aversion, anchoring, overconfidence — detection algorithms
* [execution-quality.md](references/execution-quality.md) — Slippage, VWAP comparison, arrival price, market impact models, TCA framework
* [trade-journal-schema.md](references/trade-journal-schema.md) — Standardized trade log format, required fields, behavioral tagging taxonomy
* [risk-metrics-guide.md](references/risk-metrics-guide.md) — VaR, CVaR, tail risk, EVT for extreme losses, stress testing methodology
* [small-sample-statistics.md](references/small-sample-statistics.md) — Confidence intervals for performance metrics, minimum sample sizes, statistical power
* [error-recovery.md](references/error-recovery.md) — Additional patterns: look-ahead bias, data snooping, selection bias, benchmark mismatch
