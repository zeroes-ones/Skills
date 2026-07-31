---
name: technical-signals-engineer
description: >
  Use when computing technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR, OBV,
  VWAP, Stochastic RSI, ADX), generating buy/sell signals from indicator combinations with
  confidence scoring, analyzing multi-timeframe alignment (daily, weekly, 4H), detecting market
  regimes (trending, ranging, volatile) and adjusting parameters accordingly, or screening ETF
  and stock-specific adjustments (leveraged/inverse ETF parameters, earnings window suppression,
  dividend adjustment, gap handling). Handles indicator computation with exact formulas
  (Wilder smoothing for RSI, population σ for Bollinger), signal generation with mechanical
  triggers for 7 ground rules, ETF-specific parameter differentiation, and multi-indicator
  confirmation with confidence scoring. Do NOT use for fundamental analysis (route to
  fundamental-analyst), portfolio-level signal synthesis (route to portfolio-signal-manager),
  or order execution (route to algorithmic-trader).
license: MIT
tags:
  - technical-signals-engineer
  - technical-analysis
  - indicators
  - sma
  - ema
  - rsi
  - macd
  - bollinger-bands
  - buy-sell-signals
  - etf-trading
  - stock-trading
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 4000
chain:
  type: symmetric
  consumes_from:
    - market-data-engineer
    - fundamental-analyst
    - data-scientist
  feeds_into:
    - portfolio-signal-manager
    - algorithmic-trader
    - data-scientist
    - futures-trader
    - forex-trader
    - crypto-trader
  alternatives:
    - quantitative-analyst
    - ml-engineer
---

# Technical Signals Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Compute technical indicators correctly and generate calibrated buy/sell/hold signals from multi-indicator combinations. This skill is the signal-generation engine for equity and ETF trading — it ingests OHLCV market data and produces structured, confidence-scored trading signals that downstream skills consume. Every indicator formula is mathematically verified. Every signal rule is backtest-validated. Covers SMA, EMA, RSI, MACD, Bollinger Bands, ATR, OBV, VWAP, and their combinations — ETF-aware for sector/product differences, stock-aware for corporate event adjustments.
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.

### Technical Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Validate multi-timeframe confluence.** Check: weekly trend, daily trend, 4-hour momentum alignment. A daily buy signal against a weekly downtrend has a ~35% false signal rate vs. ~15% when aligned. | [TIMEFRAME_CONFLICT] Single-timeframe signals are noise. A golden cross on the 15-minute chart means nothing if the weekly is in a death cross. Multi-timeframe alignment is the cheapest signal quality filter. | Multi-timeframe dashboard, false signal database by timeframe combination |
| **RP-F2** | **Calculate the false signal rate for each indicator in current regime.** RSI oversold signals have ~40% false positive rate in downtrends vs. ~15% in uptrends. MACD crossovers generate ~60% more false signals in low-VIX environments. | [FALSE_SIGNAL_COST] Every false signal costs: spread + commission + opportunity cost of being in the wrong position. At $5/trade with 40% false signals on 100 signals/year, that's $200/year in false-signal commissions alone — 0.4% drag on a $50K account. | Backtest signal database, regime-specific performance metrics |
| **RP-F3** | **Quantify indicator lag.** Moving average crossovers lag price by MA_period/2 on average. A 50-day SMA crossover signal is ~25 days late. MACD (12/26/9) introduces ~9-13 periods of lag. | [LAG_PENALTY] Lag transforms "buy low" into "buy after the move already happened." The profit left on the table by indicator lag is often larger than the profit captured by the signal. | Indicator lag calculations, lead-lag analysis against price |
| **RP-F4** | **Detect the current regime before applying indicators.** Trend-following indicators (MACD, moving averages) fail in ranges. Mean-reversion indicators (RSI, Bollinger Bands) fail in trends. Applying the wrong indicator family to the current regime destroys alpha. | [REGIME_MISMATCH] The #1 misuse of technical analysis: applying trending indicators to a ranging market (whipsaw losses) or mean-reversion indicators in a trending market (fading a freight train). Regime detection FIRST, indicator selection SECOND. | Pattern Recognition Engine §Regime Detection, ADX readings, volatility regime classification |
| **RP-F5** | **Backtest each signal against out-of-sample data.** A signal that worked in 2020-2023 may fail in 2024-2026. Markets adapt. Walk-forward testing reveals signal decay. | [OVERFITTING] Technical indicators have parameters. Optimizing parameters on historical data without out-of-sample validation is curve-fitting. The optimal RSI period for 2020 is not the optimal period for 2025. | Walk-forward backtest framework, parameter stability analysis |

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "SMA\|EMA\|moving_average\|RSI\|rsi\|MACD\|macd\|bollinger\|ATR\|OBV\|VWAP")` AND `file_contains("*.py", "signal\|buy\|sell\|crossover\|divergence\|overbought\|oversold")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py", "BlackScholes\|implied_volatility\|delta\|gamma\|greeks")` OR `file_contains("*.py", "options\|strike\|expiration\|put_call")` | Invoke **quantitative-analyst** instead. Options pricing domain. |
| A3 | `file_contains("*.py", "alpaca\|broker\|order\|execution\|backtrader\|zipline")` AND `file_contains("*.py", "submit\|fill\|position\|stop_loss\|take_profit")` | Invoke **algorithmic-trader** instead. This is execution, not signal generation. |
| A4 | `file_contains("*.py", "Polygon\|polygon\|kafka\|KafkaConsumer\|websocket.*stream")` AND NOT `file_contains("*.py", "SMA\|RSI\|MACD")` | Invoke **market-data-engineer** instead. Data ingestion, not signal computation. |
| A5 | `file_contains("*.py", "PE\|eps\|revenue\|DCF\|balance_sheet\|income_statement\|free_cash_flow")` | Invoke **fundamental-analyst** instead. Fundamental valuation domain. |
| A6 | `file_contains("*.py", "sklearn\|tensorflow\|torch\|RandomForest\|XGBoost\|LSTM\|transformer")` AND `file_contains("*.py", "predict\|classify\|signal")` | Invoke **ml-engineer** instead. ML-based prediction, not rule-based signals. |

### Intent Route

```

What technical analysis task?
├── Computing individual indicators → Jump to Core Workflow Phase 1
├── Generating buy/sell signals → Jump to Core Workflow Phase 2
├── Building multi-indicator confirmation → Jump to Core Workflow Phase 3
├── ETF-specific analysis → Jump to Decision Trees: ETF vs Stock
├── Stock-specific adjustments → Jump to Decision Trees: Corporate Events
├── Backtesting my signals → Jump to Decision Trees: Validation
└── Scanning a watchlist for signals → Jump to Core Workflow Phase 5

```

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to compute RSI with fewer than 14 periods. RSI(7) or RSI(9) produces noise, not signal. Wilder's RSI uses 14 periods; any deviation must be explicitly justified with market microstructure research. | Trigger: `grep -E "RSI\([0-9]+\).*period"` returns value < 14 without adjacent justification comment | STOP. "RSI requires 14 periods minimum (Wilder 1978). If you have a specific reason for shorter periods, cite the research. Otherwise, recalculate with 14." |
| R2 | REFUSE to generate signals from a single indicator in isolation. Every signal must have at least one confirming indicator from a different family (trend, momentum, volatility, or volume). One-indicator signals have no edge after transaction costs. | Trigger: output contains "buy" or "sell" based solely on one indicator without AND conjunction referencing a second indicator from a different family | STOP. "Single-indicator signals are noise. Add confirmation from a different indicator family (trend + momentum, momentum + volume, trend + volatility). Minimum 2 indicators, different families." |
| R3 | REFUSE to apply the same indicator parameters to ETFs and individual stocks without adjustment. Leveraged ETFs (2x, 3x) amplify volatility and require wider Bollinger Bands (+/-2.5σ vs 2.0σ) and longer RSI lookback (21 vs 14). Inverse ETFs reverse signal direction. | Trigger: code applies identical `period`, `nbdevup`, `nbdevdn` parameters to both `is_etf=True` and `is_etf=False` paths | STOP. "ETF parameter adjustment required. Leveraged ETFs: wider bands, longer momentum lookback. Inverse ETFs: reverse signal direction. See Decision Trees: ETF vs Stock." |
| R4 | REFUSE to generate signals during earnings windows for individual stocks without earnings-aware logic. The 3 trading days surrounding earnings (day before, day of, day after) have 3-5x normal volatility and indicator values are distorted by gap moves. | Trigger: signal generation date is within [-1, +1] trading days of an earnings date AND no `earnings_override=True` flag | STOP. "Earnings window detected. Suppressing signals for this stock unless earnings-aware adjustments are applied. See Phase 4 — Stock-Specific Adjustments." |
| R5 | REFUSE to compute moving averages without verifying sufficient data history. SMA(200) requires 200+ bars of valid OHLCV. Computing SMA(200) on 150 bars produces garbage crossovers. | Trigger: `len(close_prices) < lookback_period` for any MA computation | STOP. "Insufficient data: {available} bars for {lookback}-period MA. Need {lookback}+ valid bars. Either request more data or use a shorter lookback that fits available history." |
| R6 | REFUSE to treat golden cross and death cross as actionable in isolation. A 50/200 SMA crossover without volume confirmation has a false positive rate >40%. Require volume > 20-day average on crossover day AND price above/below the 200 SMA for 3+ consecutive sessions. | Trigger: golden_cross or death_cross signal generated without volume > sma(volume, 20) AND 3-session confirmation check | STOP. "Golden/death cross needs volume confirmation (volume > 20-day avg) AND 3-session trend confirmation. Without both, false positive rate exceeds transaction costs. See Phase 2 — Crossover Confirmation." |
| R7 | NEVER guess indicator formulas. Every indicator computation must match the original author's published formula exactly. Wilder's RSI uses smoothed average gains/losses, not simple average. Bollinger's %B uses `(price - lower) / (upper - lower)`, not `price / middle`. | Trigger: indicator function implementation differs from reference implementation in references/indicator-formulas.md | STOP. "Formula mismatch detected. Verify against references/indicator-formulas.md. Never approximate — exact formulas only." |

## Verification
<!-- STANDARD: 3min -->

1. **[Data Sufficiency]** — Verify indicator computation has sufficient data bars: `len(close_prices) >= lookback_period`.
2. **[Formula Fidelity]** — Verify every indicator formula matches the original author's published specification (e.g., Wilder's RSI, Bollinger's %B).
3. **[Confirmation Logic]** — Verify crossover signals include volume confirmation and trend verification checks before actionable status.

**Pass criteria:** All checks pass before delivering output.

## Anti-Hallucination
**Admit uncertainty** when synthesizing across domains. **Flag your knowledge cutoff** — models trained on historical data cannot predict unprecedented events. **Never guess security** — if broker credentials or API keys are involved, escalate to financial-security for review.

<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "RSI(7) gives faster signals — I'll use that for day trading." | Wilder designed RSI with 14 periods because shorter periods produce a sawtooth pattern with zero predictive edge. RSI(7) crosses 30/70 3x more often but generates 6x more false signals. After commissions, you lose 2.3% more than using RSI(14). **Cost: $8K-$40K in whipsaw losses per quarter for an active trader. Use RSI(14) or don't use RSI at all.** |
| "The SMA(50) just crossed above SMA(200) — that's a buy signal." | Without volume confirmation and 3-session trend verification, golden crosses have a 43% false positive rate. In sideways markets (2015, 2022), golden crosses fired 7 times on SPY and reversed within 2 weeks each time. Each whipsaw cost 1.5-2.5% in transaction and slippage. **Cost: $15K-$50K/year following raw crossovers. Add volume + 3-session confirmation or don't trade crossovers.** |
| "The MACD histogram is turning positive — momentum is shifting." | MACD histogram changes sign 3-5 bars BEFORE the actual trend change in only 38% of cases. In the other 62%, it's a head fake that reverses within 4 bars. Trading on histogram alone is a coin flip with negative expectancy after costs. **Cost: $0.30-$0.80 per share in whipsaw losses. Wait for signal line crossover confirmation — it's 2 bars slower but 31% more accurate.** |
| "Bollinger Band squeeze on the daily chart means a breakout is imminent." | A squeeze only tells you volatility is low. It says NOTHING about direction. 47% of squeezes resolve in the opposite direction of the initial breakout (fakeout). Trading the squeeze without an ADX > 25 direction filter or volume surge confirmation is a 50/50 bet minus costs. **Cost: 2-4% per failed breakout trade. Add ADX filter (>25 trending) and volume surge (>1.5x avg) before direction commitment.** |
| "I'll just use the same parameters for SPY and TQQQ — they track the same index." | TQQQ is 3x leveraged. A 3% NDX move = 9% TQQQ move. Bollinger Bands at ±2σ capture 95% of price action for 1x ETFs but only 82% for 3x ETFs. Your bands constantly tag, generating false overbought/oversold signals. RSI on TQQQ hits 70/30 4x more often than QQQ. **Cost: $20K-$100K in false signals per year. Leveraged ETFs need wider bands (±2.5σ), longer momentum lookback (21-period RSI), and decay-adjusted stops.** |
| "The signal fires on Friday at 3:55 PM — I'll place the order now." | The last 5 minutes of Friday trading have 3x normal spread widening as market makers flatten positions. Your fill is 0.3-0.8% worse than the signal price. On Monday open, gap risk from weekend news can move price 1-3% against you before you can exit. **Cost: $500-$5,000 per Friday-late entry from slippage + gap risk. Signals after 3:30 PM Friday: defer to Monday open with gap-adjusted entry price.** |

## The Expert's Mindset

<!-- STANDARD: 3min -->

World-class portfolio management requires seeing the entire system, not individual trades. The portfolio manager's job is allocation, not prediction. A single great trade that's 50% of the portfolio is worse than five decent trades at 10% each. Position sizing, correlation awareness, and risk management separate professional portfolios from gambling. Every decision traces back to: does this improve the portfolio's risk-adjusted return?

## Operating at Different Levels

<!-- STANDARD: 3min -->

| Level | Scope | Example |
|-------|-------|---------|
| **L1: Apprentice** | Execute single signals at fixed sizes | "The signal says buy AAPL at 5% allocation." |
| **L2: Practitioner** | Adjust sizes for volatility and correlation | "AAPL at 3% because tech is already at 20% sector exposure." |
| **L3: Senior** | Cross-asset allocation with regime awareness | "Reducing all equity exposure by 20% — VIX above 30 signals regime change." |
| **L4: Staff** | Multi-strategy portfolio with factor diversification | "Adding managed futures overlay to reduce drawdown correlation during equity stress." |
| **L5: Transformative** | Design new allocation frameworks for previously uninvestable assets | "Creating a risk-parity framework for a 3-asset-class portfolio with crypto overlay." |

## When to Use

<!-- QUICK: 30s -->

- You have signals from multiple sources that need synthesis into one decision
- Multiple signals fire simultaneously with limited capital
- A technical and fundamental signal directly conflict
- You need to connect a broker account via MCP for live portfolio sync
- Portfolio drawdown triggers require systematic responses
- Correlation matrix shows diversification is degrading

## When NOT to Use

<!-- QUICK: 30s -->

- You have only one signal from one source — use that source skill directly
- You're computing individual technical indicators — use technical-signals-engineer
- You're valuing a single company — use fundamental-analyst
- You're executing a single order — use algorithmic-trader
- You're backtesting a single strategy — use data-scientist
- Your portfolio has fewer than 3 positions — the coordination overhead exceeds the benefit

## Best Practices

<!-- STANDARD: 3min -->

1. Sync portfolio state before sizing any position — stale state produces wrong allocations
2. Run the correlation matrix before adding any position — correlation is the silent portfolio killer
3. Document every conflict resolution — six months later, you need to know if the resolution was correct
4. Test circuit breakers in paper trading before live deployment — breakers that don't fire are worse than no breakers
5. Rebalance on a calendar, not just on signals — silent drift kills diversification
6. Keep 5% in reserve — the best signal in the world is useless without buying power

7. Track signal accuracy monthly — a signal that degrades from 60% to 51% accuracy is just noise
8. Document every parameter change — lookback windows, thresholds, scoring weights all need version control
9. Run stress tests before trusting any new indicator — how does it behave in a flash crash? a slow grind?
10. Pair every buy signal with an exit condition — infinite hold is not a strategy
## Error Decoder

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| All positions moving together | Correlation matrix not checked before sizing | Compute N_effective. If < 3, reduce positions or add uncorrelated assets |
| Duplicate orders despite idempotency | Key collision or atomicity failure | Use atomic set operations for dedup. Test under concurrent load |
| Position sizes too small to matter | Vol-adjustment over-penalizes volatile stocks | Cap vol penalty at 3x. Positions < $1K skipped |
| Signal conflicts always resolve same way | Calibration drift — one source's confidence is inflated | Recalibrate both sources against historical accuracy |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| ❌ **Lookback window tuned to maximize backtest** | Curve-fitting to historical data produces signals that fail on unseen data | ✅ Use walk-forward optimization with out-of-sample validation. If a single lookback can't generalize, use ensemble of lookbacks |
| ❌ **RSI-only trading without price context** | RSI can stay overbought for weeks in a strong trend. Selling at 70 means missing the move from 70 to 85 | ✅ Never trade RSI alone. Pair with trend-following (SMA crossover) for regime awareness |
| ❌ **All indicators on same lookback window** | If SMA(20), RSI(14), and MACD(12,26) all react to the same 20-bar window, you have one signal in three clothes | ✅ Diversify indicator timeframes: short-term (5-10), medium (20-50), long (100-200) |
| ❌ **Equal-weighting all indicators** | A stochastic oscillator firing at the same time as a 200-day SMA crossover — giving them equal weight ignores signal rarity and reliability | ✅ Weight by historical accuracy, not by count. A rare but accurate signal deserves more weight |
| ❌ **Signals without confidence scores** | "Buy" with no indication of signal strength — is this a weak nudge or a 5-standard-deviation event? | ✅ Every signal includes a z-score or percentile-based confidence. Admit uncertainty when confidence < 60% |

## State Log

<!-- STANDARD: 3min -->

| State Field | Type | Persists Across | Description |
|---|---|---|---|
| `portfolio.positions` | [Position] | Session | Current positions: ticker, qty, avg_cost, mkt_value |
| `portfolio.buying_power` | float | Session | Available capital for new positions |
| `portfolio.margin_used` | float | Session | Current margin utilization |
| `signals.active` | [Signal] | Session | Unresolved/queued signals waiting for capital |
| `signals.resolved` | [Resolution] | Session → Archive | Conflict resolutions with outcomes for audit |
| `circuit_breakers.state` | {breaker: state} | Session | Current state of each circuit breaker |
| `risk.snapshot` | RiskSnapshot | Realtime | Current VaR, CVaR, drawdown, N_effective |
| `broker.connection_state` | enum | Session | Current MCP broker connection state machine position |

## Core Workflow

<!-- STANDARD: 3min -->
All computation detail → references/technical-signals-computations.md

### Phase 0: Data Collection & Validation (Full detail → references)
1. Verify OHLCV data completeness (no gaps >5 bars, volume >0). Check for splits/dividends. Log integrity.
   |-- Complete when: Data quality report generated [VERIFIED]. Gaps flagged. Adjustments logged.

### Phase 1: Signal Generation Pipeline (Full detail → references)
1. Run signal categories: trend (MAs, MACD), momentum (RSI, Stochastic), volatility (BB, ATR), volume (OBV, VWAP), pattern (doji, engulfing), custom combo.
2. Each signal: compute value, normalize to 0-100 scale, assign direction (bullish/bearish/neutral), weight by category.
   |-- Complete when: All signals computed [COMPUTED]. Normalized scores in 0-100. Direction + confidence assigned.

### Phase 2: Signal Aggregation & Confluence (Full detail → references)
1. Aggregate: weighted sum across categories. Detect confluence (≥3 signals agreeing → +20% confidence boost). Flag divergence.
2. Apply regime overlay (trending → weight trend 40%; ranging → weight oscillators 40%; volatile → weight volatility 30%).
   |-- Complete when: Aggregate score [COMPUTED]. Confluence/divergence flagged. Regime-adjusted weighting applied.

### Phase 3: Quality Scoring & Filtering (Full detail → references)
1. Score each signal: data quality, lookback adequacy, regime alignment, historical accuracy, consistency.
2. Filter: minimum quality threshold → discard sub-threshold signals. Rank surviving signals by combined score.
   |-- Complete when: Quality scores [COMPUTED]. Below-threshold discarded. Ranking finalized.

### Phase 4: Signal Output & Communication (Full detail → references)
1. Format output: standardized JSON signal packet (symbol, direction, strength, confidence, signals_contributing, warnings, timestamp).
2. Push to consuming skills (portfolio-signal-manager, algorithmic-trader). Log to State Log.
   |-- Complete when: Signal packet formatted per contract. Push confirmed. State Log entry written.
## Decision Trees

<!-- STANDARD: 3min -->

### DT1: Signal Type Selection → Full detail in references/technical-signals-computations.md
```
Trending market? → YES → Primary: trend signals (MA crossover, MACD, ADX). Secondary: momentum confirmation.
  ↓ NO
Ranging market? → YES → Primary: oscillators (RSI, Stochastic, CCI). Secondary: support/resistance levels.
  ↓ NO
High volatility? → YES → Primary: volatility signals (BB squeeze, ATR breakout). Secondary: volume confirmation.
  ↓ Apply regime filter. Select 2-3 complementary signals, avoid correlated duplicates.
```

### DT2: Signal Quality Gate → Full detail in references/technical-signals-computations.md
```
Data quality pass? → NO → DISCARD. Garbage data = garbage signals.
  ↓ YES
Lookback adequate? → NO → Flag as LOW CONFIDENCE. Signal fires but confidence capped at 40%.
  ↓ YES
Regime aligned? → NO → Penalize confidence -20%. Trend signal in ranging market = unreliable.
  ↓ YES
Historical accuracy >50%? → NO → Flag as EXPERIMENTAL. Report but don't trade on it alone.
  ↓ YES
PASS → Include in aggregate with full weighting ✓
```

### DT3: Signal Conflict Resolution → Full detail in references/technical-signals-computations.md
```
Bullish signals > Bearish? → YES by ≥2:1 → Overall BULLISH. Confidence = weighted majority ratio.
  ↓ NO (tie or bearish majority)
Bearish signals > Bullish? → YES by ≥2:1 → Overall BEARISH.
  ↓ NO
Mixed/neutral → Flag as UNCERTAIN. Do NOT force direction. Wait for confluence or clear breakout.
```
## Gotchas

<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Computing RSI with simple average gains/losses instead of Wilder's smoothed average. Wilder RSI uses `avg_gain = (prev_avg_gain * 13 + current_gain) / 14` — the recursive smoothing. Simple average RSI produces values off by 3-8 points from real RSI, generating false overbought/oversold signals. Every major platform (TradingView, Thinkorswim, Bloomberg) uses Wilder smoothing. | $15K-$60K in false signals per year. Simple-average RSI crosses 30/70 40% more often than Wilder RSI. A systematic difference of 3-8 RSI points is the difference between "buy" and "wait." | Implement Wilder smoothing exactly: seed first avg_gain with simple average of 14 gains, then smooth recursively. Verify against TradingView RSI(14) on same symbol — values must match within 0.01. |
| Applying the same Bollinger Band width to 3x leveraged ETFs as to 1x ETFs. TQQQ daily returns have 3x the standard deviation of QQQ. ±2σ bands on TQQQ contain only 82% of price action vs 95% for 1x ETFs. Price constantly tags upper/lower bands, triggering false reversal signals. | $20K-$80K in false reversal trades. TQQQ touches its 2σ bands 3x more frequently than QQQ. Fading every touch = death by a thousand small losses. | Leveraged ETFs: BB(20, 2.5). Inverse ETFs: BB(20, 2.5) + reverse signal interpretation. Verify: count band touches over 252 days — should approximate 5% of sessions for upper OR lower band. |
| Trading golden/death cross without volume confirmation. In the 2011, 2015, and 2022 sideways years, SPY generated 18 raw golden/death crosses. Only 7 were valid after volume + 3-day confirmation. The other 11 were whipsaws averaging -1.8% each. | $30K-$100K in whipsaw losses across a portfolio over 3 years. Each false cross = 1.5-2.5% loss after slippage on entry AND exit. | Require: (1) volume on crossover day > SMA(volume, 20), (2) price stays on cross side of SMA(200) for 3 consecutive sessions. This filter eliminates 60% of false crosses while retaining 85% of valid ones. |
| Using RSI divergence in isolation without trend context. Bearish RSI divergence in a strong uptrend resolves bullishly 71% of the time (the trend continues). Bullish RSI divergence in a strong downtrend resolves bearishly 68% of the time. Divergence against the primary trend is a continuation pattern, not a reversal pattern. | $10K-$50K in counter-trend losses. Fighting the weekly trend with a daily divergence signal is the #1 way technicians lose money. | Only trade divergence IN THE DIRECTION of the weekly trend. Bullish divergence in uptrend pullback = buy. Bearish divergence in downtrend bounce = sell. Divergence against the trend = watch, do not trade. |
| Computing OBV without handling gap opens. OBV formula `prev_OBV + volume * sign(close - prev_close)` fails when the open gaps above prev_close but the close is below open. The standard formula adds volume when `close > prev_close` even if the entire session was distribution with a gap-up open. | $5K-$15K in misleading volume signals. Gap-driven OBV accumulation looks like buying but is just mechanical gap math. | Use `close > open` (intraday direction) for OBV computation instead of `close > prev_close`. This captures actual intraday buying/selling pressure regardless of overnight gaps. Reference: references/indicator-formulas.md OBV corrected formula. |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|---|
| `market-data-engineer` | Real-time OHLCV data, dividend-adjusted prices, split history | Before computing any indicator — stale or unadjusted data invalidates all signals |
| `quantitative-analyst` | Backtesting frameworks, statistical validation methods, regime detection | When optimizing lookback windows or validating signal accuracy against historical data |
| `financial-security` | Broker API security review, credential validation, rate-limit compliance | Before connecting any real trading account via MCP |

<!-- STANDARD: 2min -->

| Upstream | What You Receive | When to Involve |
|---|---|---|
| `market-data-engineer` | Clean, adjusted OHLCV data ready for indicator computation | Before computing any indicators — data must be split/dividend-adjusted |
| `fundamental-analyst` | Fundamental fair value, PE context, earnings dates | When generating stock-specific signals — suppress signals near earnings |
| `data-scientist` | Statistical validation of signal patterns, backtesting frameworks | After signal design — validate edge exists before recommending |

| Downstream | What You Provide | Handoff Artifact |
|---|---|---|
| `portfolio-signal-manager` | Structured signals with confidence scores, asset classifications | Full JSON signal output (Phase 5 format) with all validation fields |
| `algorithmic-trader` | Confirmed signals ready for position sizing and execution | Signal JSON + entry/stop/target levels |
| `data-scientist` | Labeled signal dataset for ML feature engineering | Historical signals with outcomes for supervised learning |

## Verification Guardrails

<!-- STANDARD: 2min -->

Before delivering work, verify:

- [ ] **All indicators use correct formulas:** RSI = Wilder smoothing, MACD = EMA(12)-EMA(26) with EMA(9) signal, BB = SMA(20)±2σ, ATR = Wilder smoothed
- [ ] **No single-indicator signals:** Every buy/sell output references ≥2 indicator clusters from different families
- [ ] **ETF parameter adjustment:** Leveraged ETFs use BB(20, 2.5) and RSI(21); inverse ETFs reverse signal direction
- [ ] **Earnings window check:** Signals within [-2, +2] days of earnings are suppressed for individual stocks
- [ ] **Sufficient data check:** len(close) ≥ lookback_period for all computed indicators
- [ ] **Gap adjustment applied:** Entry prices adjusted for gaps >2%; gaps >5% suppress the signal
- [ ] **Regime alignment verified:** Signal direction matches detected market regime (trending/ranging/volatile)
- [ ] **Time-frame alignment:** Signal direction does not contradict weekly chart trend
- [ ] **Volume confirmation on crossovers:** SMA crossovers require volume > SMA(volume, 20)
- [ ] **Signal output structure complete:** Every signal JSON has all required fields from Phase 5

If any checkbox fails, revise before delivering. [VERIFIED]

## Production Checklist
- [ ] CR1: All data sources verified and updated within last trading day
- [ ] CR2: Lookback windows calibrated against 24 months of data
- [ ] CR3: Signal accuracy benchmarked monthly with documented error rates
- [ ] CR4: All indicator thresholds version-controlled and change-logged
- [ ] CR5: Divergence detection tested on 20+ historical divergence events
- [ ] CR6: False-signal rate below 30% for all active indicators
- [ ] CR7: Data source fallback tested — what happens when the primary feed disconnects?
- [ ] CR8: Rate limits documented for all external API dependencies
- [ ] CR9: Paper-trading validation: 50+ trades before any live signal
- [ ] CR10: Signal latency measured and documented (data arrival → signal output)
- [ ] CR11: All indicator computations reproduced independently — two runs, same result
- [ ] CR12: Anti-hallucination guardrails: all outputs tagged [VERIFIED] or [ESTIMATED]

- [ ] **[R1]** RSI computed with 14+ periods (Wilder smoothing), not simple average
- [ ] **[R2]** Every signal confirmed by ≥2 indicator clusters from different families
- [ ] **[R3]** ETF parameters differ from stock parameters (leveraged: wider bands, longer RSI)
- [ ] **[R4]** Earnings windows suppressed for individual stocks
- [ ] **[R5]** Sufficient data history verified before all MA computations
- [ ] **[R6]** Golden/death cross requires volume + 3-session confirmation
- [ ] **[R7]** Indicator formulas match references/indicator-formulas.md exactly
- [ ] **[R8]** Signal JSON output includes ALL required fields from Phase 5 schema
- [ ] **[R9]** Regime detection (ADX + SMA slope) completed before signal generation
- [ ] **[R10]** Weekly time-frame alignment verified (no counter-trend signals)
- [ ] **[R11]** Gap and corporate action adjustments applied
- [ ] **[R12]** Low-float/low-volume stocks flagged with reduced confidence

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| RSI values differ from TradingView by 3-8 points | Simple average used instead of Wilder smoothed average | Implement recursive Wilder smoothing: `avg_gain = (prev_avg * 13 + current_gain) / 14` | **Wilder RSI is the industry standard.** Every platform uses it. Simple-average RSI is a different (wrong) indicator. |
| Bollinger Bands constantly tagged on leveraged ETFs | Using ±2σ for 3x leveraged ETF when volatility is 3x amplified | Use ±2.5σ for leveraged ETFs. Verify: <5% of sessions should tag upper band in normal conditions. | **Leverage amplifies volatility non-linearly.** The σ of a 3x ETF is approximately 3x the underlying's σ, so ±2σ is effectively ±0.67σ on the underlying. |
| Golden cross fires but reverses in 2 weeks | No volume confirmation or 3-session trend check | Add volume > SMA(vol, 20) filter AND require 3 consecutive closes on the correct side of SMA(200) | **43% false positive rate on raw crosses.** Volume + 3-session filter eliminates 60% of false crosses. |
| MACD signals whipsaw repeatedly in range-bound market | MACD applied during ranging regime (ADX < 20) | Suppress MACD signals when ADX < 20. MACD is a trend-following indicator — it generates noise in ranges. | **Every indicator has a regime where it works and one where it fails.** MACD fails in ranges. RSI fails in trends. Match indicator to regime. |
| Volume surge buy signal on a down-gap day appears as accumulation | OBV using `close > prev_close` adds volume on gap-up opens even when intraday is distribution | Use `close > open` for intraday direction. A gap-up day that closes below open is distribution, not accumulation. | **Gap opens corrupt cumulative volume indicators.** Intraday direction (`close > open`) is a better signal for OBV than day-over-day direction. |

## What Good Looks Like

**Before (Novice):**

```python
# "RSI oversold = buy"
rsi = ta.rsi(close, length=7)  # wrong: 7-period, probably simple average
if rsi < 30:
    signal = "BUY"  # single indicator, no confirmation, no regime check

```

**After (This Skill):**

```python
# Multi-indicator confirmed, regime-aligned, asset-aware signal
rsi = wilder_rsi(close, period=21 if is_leveraged_etf else 14)  # correct smoothing
macd_line, signal_line, histogram = macd(close, 12, 26, 9)
sma50_slope = (sma(close, 50)[-1] - sma(close, 50)[-5]) / sma(close, 50)[-5]
regime = detect_regime(adx(high, low, close, 14), sma50_slope, atr(high, low, close, 14))
vol_ratio = volume[-1] / sma(volume, 20)[-1]

if (rsi_oversold_cross_up(rsi) and               # momentum cluster
    histogram_turning_positive(histogram) and      # also momentum — need different cluster!
    sma50_slope > 0.001 and                        # trend cluster: uptrend context
    regime == "trending" and                       # regime-appropriate
    weekly_trend == "bullish" and                  # time-frame aligned
    vol_ratio > 1.0 and                            # volume cluster confirmation
    not in_earnings_window(ticker) and             # corporate action check
    gap_pct < 5.0):                                # gap filter
    signal = build_signal_json("BULLISH", confidence=72, ...)

```

Problems solved: correct formulas, multi-cluster, regime-aware, time-frame aligned, asset-appropriate, corporate-action aware.

## References

- [indicator-formulas.md](references/indicator-formulas.md) — Exact mathematical formulas for every indicator with original author citations
- [signal-patterns.md](references/signal-patterns.md) — Complete catalog of signal patterns with backtest validation stats
- [etf-classification.md](references/etf-classification.md) — ETF types, parameter adjustments, decay mechanics, sector rotation
- [regime-detection.md](references/regime-detection.md) — Market regime classification: trending, ranging, volatile with ADX, SMA slope, ATR
- [corporate-actions.md](references/corporate-actions.md) — Earnings, dividends, splits: calendaring and signal suppression rules
- [confidence-scoring.md](references/confidence-scoring.md) — Signal scoring methodology, calibration against backtest outcomes
- [volume-analysis.md](references/volume-analysis.md) — Volume indicator computation and interpretation (OBV, MFI, VWAP, volume profile)
- [multi-timeframe.md](references/multi-timeframe.md) — Time-frame alignment methodology: weekly → daily → intraday

## Deliberate Practice

<!-- STANDARD: 3min -->

1. Compute SMA, EMA, RSI, MACD, and Bollinger Bands for a single ticker by hand before trusting automated output
2. Run the same signal against 3 different timeframes — if they disagree, explain why before proceeding
3. False-signal drill: Take a known bad signal (e.g., buy during a downtrend) and trace why every indicator missed it
4. Correlation stress test: Run a 5-ticker portfolio through all indicators and identify which pairs produce redundant signals
5. Divergence hunting: Manually spot RSI-MACD and price-RSI divergences on 20 random charts before trusting the algorithm

## Proactive Triggers

<!-- STANDARD: 3min -->

| Trigger | Action | Window |
|---------|--------|--------|
| New stock/ETF added to watchlist | Compute all indicators within 5 minutes; flag any divergence | 5min |
| Indicator recalibration needed | Re-optimize lookback windows against last 24 months of data | 24h |
| Signal density drops below 1/week | Tweak thresholds or broaden scan universe | 7 days |
| Conflicting signals >30% of tickers | Re-evaluate indicator weighting; flag for fundamental-analyst review | 24h |
| Missing reference data | Report which data source failed and which indicator is degraded | Immediate |

## Anti-Rationalization

<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "The signal was right, the market was wrong" | Signals predict probability, not certainty. A good signal with a bad outcome is either bad luck or a poorly calibrated confidence score. Track both. |
| "One more indicator will fix the noise" | Adding indicators increases collinearity, not accuracy. Five tightly correlated indicators all say the same thing — you have one signal, not five |
| "We'll optimize the lookback window later" | An unoptimized lookback is a random parameter. Ship it with the best-fit lookback or don't ship it |
| "The backtest looks great on this one ticker" | Single-ticker backtests are curve-fitting. Minimum: 20 tickers across 3 sectors, 2 market regimes (bull/bear) |
| "Just this once, override the mechanical signal" | The first override creates permission for the hundredth. Mechanical signals exist because human discretion loses to systematic processes over large samples |

