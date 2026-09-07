---
name: algorithmic-trader
description: >
  Use when developing algorithmic trading strategies, building backtesting engines, designing
  position sizing logic, or integrating with broker APIs. Handles entry/exit/trim strategy design,
  vectorized and event-driven backtesting, walk-forward optimization, position sizing (Kelly,
  risk-parity, fixed-fractional), risk management (VaR, CVaR, drawdown limits), broker API
  integration (Alpaca, Interactive Brokers), and order execution algorithms (TWAP, VWAP, iceberg).
  Do NOT use for quantitative research, market data pipeline engineering, or options pricing model
  development.
license: MIT
tags:
  - algorithmic-trader
  - trading-bot
  - backtesting
  - position-sizing
  - order-execution
  - options-trading
  - risk-management
  - broker-api
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  examples:
  - skills/14-finance/algorithmic-trader/examples/backtest
  consumes_from:
    - options-risk-engineer
    - fundamental-analyst
    - portfolio-signal-manager
    - technical-signals-engineer
    - commodities-analyst
    - crypto-trader
    - forex-trader
    - fixed-income-analyst
    - futures-trader
    - options-strategist
    - financial-security
    - quantitative-analyst
    - market-data-engineer
    - system-architect
    - backend-developer
    - observability-engineer
    - futures-trader
    - forex-trader
    - crypto-trader
    - macro-strategist
    - advanced-options-structures
    - leaps-strategist
    - intraday-options-trader
    - swing-options-trader
    - options-automation-engineer
    - volatility-arbitrage-engineer
  feeds_into:
    - backend-developer
    - frontend-developer
    - observability-engineer
    - trade-performance-analyst
    - options-automation-engineer
    - portfolio-signal-manager
    - options-quant-engineer
  alternatives:
    - ml-engineer
workflow:
  artifacts:
    inputs: [market-data, strategy-hypothesis]
    outputs: [strategy-spec]
  completion:
    criteria:
      - Strategy rules and risk limits specified precisely
      - Backtest and live assumptions separated and labeled
      - Failure modes and kill switches documented
    evidence: required
  escalate_to: [human-gate]

---
**(QUICK: 30s)** Route: run Core Workflow with standard checks.
**(QUICK: 5min)** Standard: full workflow including verification.
**(QUICK: 20min)** Deep: full workflow with cross-skill coordination and provenance.

**Quick route (QUICK):** run Route → Execute → Verify.

**Standard route (QUICK):** follow Core Workflow end to end with checks.

**Escalation route (QUICK):** escalate once with full context when blocked.

# Algorithmic Trader
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Algorithmic trading strategy development and execution — from signal consumption through position
management to post-trade analysis. This skill is the bridge between quantitative research output
and live market execution. Covers entry/exit/trim strategy design for unusual-options-activity
(UOA) signals, multi-engine backtesting, walk-forward optimization, position sizing across
regimes, broker API integration, order execution algorithms, and portfolio-level risk monitoring.
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

### Trading Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Validate backtest integrity.** Check for look-ahead bias, survivorship bias, overfitting (parameters > data points), and walk-forward vs. in-sample performance divergence. | [OVERFITTING_RISK] A backtest with 95% win rate on 7 parameters over 100 trades is curve-fit noise. Walk-forward validation that drops from 95% to 52% exposes the illusion. Every backtest must survive out-of-sample testing. | Backtest engine logs, parameter count vs. trade count ratio |
| **RP-F2** | **Benchmark execution assumptions.** Verify slippage estimates (default: 0.05% for liquid, 0.5% for illiquid), commission schedules, and fill probability against real broker data. | [EXECUTION_GAP] A strategy that returns +18% in simulation with zero slippage returns +9% in production with real fills. The execution gap is real and quantifiable — ignore it at your capital's peril. | Broker fill reports, bid-ask spread history, TCA (Transaction Cost Analysis) |
| **RP-F3** | **Check exchange rules and circuit breakers.** Verify that strategy parameters (DTE, strike width, position size) comply with exchange limits, margin requirements, and circuit breaker thresholds. | [EXCHANGE_REJECTION] Strategies that violate exchange rules fail silently in simulation and catastrophically in production. A position too large for the market maker to fill = partial fill at worst price. | Exchange rulebooks, broker API limits, Reg T/portfolio margin rules |
| **RP-F4** | **Stress-test against historical tail events.** Run the strategy against March 2020, October 1987, August 2015 flash crash, and 2008 financial crisis data. Document max drawdown in each. | [TAIL_BLINDNESS] A strategy that never saw a crash in backtest WILL face one in production. Historical tail events are the cheapest stress tests available — use them. | Historical market data, VIX spike periods, flash crash dates |
| **RP-F5** | **Verify strategy capacity.** Compute estimated market impact at current position size. If AUM/strategy capacity > 50%, returns will degrade from slippage alone. | [CAPACITY_CEILING] A market-neutral strategy that works at $500K may break at $50M. Market impact is nonlinear — doubling size more than doubles impact. | Average daily volume (ADV), bid-ask spread as % of price, depth of book |

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "The backtest shows Sharpe 4.2 and 93% win rate — this strategy is bulletproof." | You tuned 18 parameters on the full dataset with zero out-of-sample validation. Every parameter was curve-fit to noise. In live trading, true Sharpe is 0.3 and you lose 12% in the first quarter. **Cost: $50K-$500K in live losses before you accept reality. Split your data or your account gets split instead.** |
| "I'll add the stop-loss after this trade — the signal is too good to pass up." | The market doesn't care about your signal confidence. A single untrimmed loss on a momentum reversal can erase 40% of your account in hours. March 2020, August 2024 VIX spikes — positions without stops became account liquidations. **No stop = no strategy. You are gambling, and the casino is the market maker.** |
| "The signal is getting stronger as price drops — I should add to the position." | UOA signals have a shelf life measured in hours, not days. Smart money exited at the first adverse move. You're now buying what institutions are selling. Averaging down on a losing position is how a $5K loss becomes a $50K account blowup. **The market does not owe you a recovery. Cut it.** |
| "Mid-prices in backtesting are fine — the spread is only a few cents." | A 5-cent spread on a $50 stock is 0.1%. 500 trades/year compounds to a 40% drag on returns that your backtest never captured. Add slippage on market orders during volatility and you're leaking 3-5% annually into a hole your backtest doesn't even model. **You're not trading the mid-price. The market maker knows this. So should you.** |
| "I'll deploy now and add idempotency keys, correlation checks, and circuit breakers next sprint." | Your broker API retries a submission during a network hiccup and fills the order twice. Your bracket order gets rejected silently — the entry fills but the stop-loss never activates. You now hold an unprotected position you didn't know about until the margin call. **Production without idempotency is a liquidation event with a countdown you can't see.** |

## Route the Request
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "backtrader\|zipline\|vectorbt\|alpaca\|ib_insync")` OR `file_contains("*.py", "class.*Strategy\|def next(self)\|def __init__.*cerebro")` OR `file_exists("backtest.py\|live_trader.py\|execution_engine.py")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py\|*.sql", "SELECT.*FROM.*options_flow\|tick_data\|CREATE TABLE.*ticks")` OR `file_contains("docker-compose.yml", "kafka\|redpanda\|timescale")` | Invoke **market-data-engineer** instead. This is data pipeline and storage work. |
| A3 | `file_contains("*.py", "BlackScholes\|black_scholes\|bsm_price\|implied_volatility\|delta\|gamma\|theta")` OR `file_contains("*.py", "scipy.stats.norm\|monte_carlo\|heston")` | Invoke **quantitative-analyst** instead. This is pricing and Greeks analysis. |
| A4 | `file_contains("*.py\|*.sql", "CREATE TABLE.*backtest\|SELECT.*sharpe\|SELECT.*drawdown")` AND `file_contains("*.py", "pandas\|numpy\|sklearn\|statsmodels")` | Invoke **data-scientist** instead. This is statistical validation and backtesting. |
| A5 | `file_contains("*.py", "sklearn\|tensorflow\|torch\|xgboost\|lightgbm\|RandomForest")` OR `file_contains("requirements.txt", "scikit-learn\|tensorflow\|torch")` | Invoke **ml-engineer** instead. This is ML-based signal detection. |
| A6 | `file_contains("*.py\|*.yml", "FastAPI\|flask\|django\|@app\.(get\|post)")` AND `file_contains("*.py", "order\|trade\|fill\|execution")` | Jump to **Core Workflow** — Phase 3 (Broker API Integration). |
| A7 | `file_contains("*.py", "prometheus\|grafana\|alert\|metrics\|pagerduty")` OR `file_exists("prometheus.yml\|grafana/")` | Invoke **observability-engineer** instead. This is monitoring and dashboard work. |
| A8 | `file_contains("*.py", "kafka\|redis\|rabbitmq\|celery\|event.bus")` OR `file_contains("docker-compose.yml", "zookeeper\|kafka\|redis")` | Invoke **system-architect** instead. This is trading system architecture. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```

What are you trying to do?
├── Design a trading strategy (entry rules, exit/trim rules, position sizing) → Jump to "Decision Trees" — Entry Strategy Selection
├── Backtest a strategy (vectorized or event-driven, walk-forward validation) → Jump to "Core Workflow" — Phase 6 (Backtesting)
├── Integrate a broker API (Alpaca, IB, Schwab) or design order execution → Jump to "Core Workflow" — Phase 3 (Entry Execution)
├── Set up risk management (position sizing, correlation matrix, circuit breakers) → Jump to "Core Workflow" — Phase 5 (Risk Monitoring)
├── Debug a losing streak or drawdown → Jump to "Error Decoder"
├── Need quantitative signal generation or pricing models → Invoke quantitative-analyst skill instead
└── Not sure? → Describe the trade or problem in plain language and I'll route you

```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to generate a trade entry without a liquidity-grab-aware stop-loss.** Every position must have a predefined exit price before entry, placed through all 6 anti-grab layers (regime-adjusted multiplier, swing-low buffer, round-number avoidance, VWAP floor, safety check, audit trail). A naive `2x ATR` stop without these protections is gambling — market makers hunt exactly that level. | Trigger: generated code creates an order (`order = Order(` or `api.submit_order(` or `create_order(`) without a corresponding `stop_loss` or `stop_price` parameter within 10 lines, OR uses `stop_loss = entry - (2 * ATR)` without calling `compute_stop_loss()` | STOP. Insert: `initial_stop, stop_audit = compute_stop_loss(entry_price, atr, swing_low, round_step, vix, vwap_band_low, macro_stop_mult); bracket_order = api.submit_bracket(parent_order, stop_loss=initial_stop, take_profit=tier_1_target)` — must run through all 6 grab-protection layers. |
| **R2** | **REFUSE to present backtest results without a 30% haircut.** Survivorship bias, look-ahead bias, and in-sample overfitting inflate backtest returns. Always reduce Sharpe, win rate, and CAGR by 30% for realistic forward expectations. | Trigger: generated output reports "Sharpe ratio=X.X" or "CAGR=Y%" or "win rate=Z%" without immediately following text like "haircut" or "adjusted" or "forward estimate" | STOP. Append: "**⚠️ Forward Estimate (30% haircut):** Sharpe ~{X*0.7:.1f}, CAGR ~{Y*0.7:.1f}%, Win Rate ~{Z*0.7:.0f}%. If the strategy does not survive this haircut, it is not production-ready." |
| **R3** | **REFUSE to average down on a losing position UNLESS all 13 gated conditions pass.** The default stance is REFUSE — adding to a losing position is how accounts blow up. The narrow exception requires: original thesis intact (no fundamental deterioration), not a gap down, above 200-SMA, at major support, volume expanding (>1.5x avg), bullish divergence, macro-clear (>24h to event), max 1 add, add ≤ 50% of original, total risk ≤ 2% NAV, layered stop valid, backtested in current regime, win-rate confirmed in backtest. If ANY gate fails, the add is rejected. | Trigger: generated code adds to an existing losing position without running `evaluate_average_down()` first and checking `can_average_down` property | STOP. Insert gate check: `gate = evaluate_average_down(position, price, atr, prices, volumes, highs, lows, rsi, vix, nav); if not gate.can_average_down: logger.warning(f'Average-down gate REJECTED: {[f for f in dataclasses.fields(gate) if not getattr(gate, f)]}'); return SignalDecision.REJECT` — Default is REJECT. The 13-gate check is the narrow exception. |
| **R4** | **REFUSE to ignore position correlation in portfolio sizing.** Five UOA signals on five tickers in the same sector are one leveraged bet. Position-level risk limits are an illusion without daily correlation monitoring. | Trigger: generated portfolio code creates >3 positions without computing `returns.corr()` or `np.corrcoef()` and checking `max_corr > 0.7` | STOP. Insert: `corr_matrix = returns.corr(); high_corr_pairs = [(i,j) for i in corr_matrix.columns for j in corr_matrix.columns if i<j and corr_matrix.loc[i,j] > 0.7]; if high_corr_pairs: logger.warning(f'High correlation pairs: {high_corr_pairs}. Reduce exposure or drop newest positions.')` |
| **R5** | **STOP and ASK when execution context is missing.** Do not size or enter a position without knowing: option chain liquidity, borrow costs, real-time fill data availability, and whether the broker supports bracket orders. | Trigger: generating position sizing or entry code without explicit confirmation of ADV, borrow cost, bid-ask spread, and broker capabilities in the conversation | STOP. Ask: "What's the stock's ADV and option OI? What's the borrow cost for shorts? What's the current bid-ask spread? Does your broker support bracket orders (OCO) natively?" |
| **R6** | **DETECT and WARN about broker API calls without idempotency keys.** Retried orders can double-fill. A rejected bracket order means the stop-loss never activates. Every order submission MUST have idempotency protection. | Trigger: generated code calls `api.submit_order(` or `broker.place_order(` or `create_order(` without an `idempotency_key` or `client_order_id` parameter | WARN: Insert `client_order_id = f"{signal_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"`. Add comment: `# Idempotency key prevents double-submission on retry. Broker must reject duplicate client_order_id.` |
| **R7** | **DETECT and WARN about backtests that use closing mid-prices for fills.** Mid-prices assume infinite liquidity at zero spread — reality is crossing the spread on every trade. | Trigger: generated backtest code contains `df['close']` or `df['adj_close']` as the fill price without adding/subtracting half the spread: `fill_price = close - spread/2 if sell else close + spread/2` | WARN: Insert `spread = (df['ask'] - df['bid']).mean(); fill_price = df['close'] + np.sign(side) * spread/2`. Add comment: `# WARNING: Using mid-prices overestimates returns by transaction costs. Real fills cross the spread.` |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R10** | **REFUSE to execute a stop-loss exit without running the 5-layer liquidity grab detector first.** A stop trigger is not automatically an exit. Run `is_liquidity_grab()` with wick/body, close-below, volume, time-of-day, and multi-timeframe checks before deciding EXIT vs HOLD vs WIDEN_AND_HOLD. | Trigger: generated exit code calls `api.submit_order(side='sell'...)` or `close_position()` immediately after `if price <= stop_loss` or `if price <= trailing_stop` without calling `is_liquidity_grab()` first | STOP. Insert grab detector call: `is_grab, action, reason = is_liquidity_grab(trigger_price, stop_type, bars_1m, bars_5m, avg_vol_20d, premarket, postmarket, seconds_since_open); if action != 'EXIT': return None  # hold or widen, not a real breakdown`. |
| **R11** | **REFUSE to enter a trade within 2 hours of a red-flag macro event (FOMC, CPI, NFP). Within 24 hours, halve size and widen stops 1.5x.** Macro events cause 2-4x normal intraday volatility — any signal edge is noise against central bank or economic data releases. | Trigger: generated entry code calls `api.submit_order(` or `create_order(` without first checking `hours_to_next_macro_event() <= 2 and is_red_flag_event()` | STOP. Insert macro gate check: `hours = hours_to_next_macro_event(); if hours <= 2 and is_red_flag_event(): return SignalDecision.REJECT; elif hours <= 24 and is_high_impact_event(): signal['adjusted_size'] *= 0.5; signal['stop_multiplier'] = 1.5`. |
| **R12** | **REFUSE to let a runner become a loser.** Once T1 (+10%) is hit and 25% is trimmed, the stop MUST move to breakeven — no exceptions. After T2 (+20%) is hit, switch from fixed targets to progressive ATR-based trailing. The final runner (remaining 25% after T3) exits ONLY on SAR exhaustion, NEVER on a fixed price. A runner that reaches +100% should not be curtailed at an arbitrary +40% target. | Trigger: a position hits T1/T2/T3 targets but the stop remains below entry or the trail logic still uses fixed price targets | STOP. After T1: move stop to entry price. After T2: compute `trail_stop = max(highs[-10:]) - (1.5 * atr)`. After T3: run `sar_exhaustion_signal(highs, lows)` and exit only if `exhausted=True`. No fixed T3 exit — let the SAR flip decide. |
| **R13** | **REFUSE to pyramid into a position that is not already a confirmed winner.** Adding to a position (pyramid scaling) is only valid when: gain >5%, volume confirms the move, the add is on a pullback to support (not at highs), trend structure is intact, and the add is ≤ 50% of original size. Only one pyramid add per position. The blended stop after the add must be tighter than the original. | Trigger: generated code adds to an existing position but `position.unrealized_pnl` < 5% of entry, or volume on the add bar < 20-day avg, or the add happens >1 ATR above 10-EMA | STOP. Insert pyramid gate: `pyramid = evaluate_pyramid_add(position, price, atr, highs, lows, volumes, nav); if not pyramid.can_add: logger.warning(f'Pyramid gate REJECTED: gain={pyramid.gain_from_entry}%, vol_ok={pyramid.volume_confirmation}, pullback={pyramid.pullback_to_support}, trend={pyramid.trend_intact}'); return SignalDecision.HOLD` — Only add to winners on confirmation pullbacks. |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

Masters of algorithmic trader don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 algorithmic trader, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing entry, exit, and trim strategies for unusual options activity (UOA) signals
- Building backtesting engines: vectorized (pandas/numpy) for speed or event-driven for realism
- Running walk-forward optimization to validate strategy robustness across market regimes
- Implementing position sizing: Kelly criterion, fixed-fractional, volatility-adjusted, risk-parity
- Integrating with broker APIs: Alpaca (equity/options), Interactive Brokers (TWS/Client Portal), Schwab (trader API)
- Executing orders with minimal market impact: TWAP, VWAP, iceberg, implementation shortfall algorithms
- Building real-time risk dashboards: VaR, CVaR, beta exposure, correlation matrix, max drawdown monitors
- Conducting post-trade analysis: P&L attribution, slippage audit, signal decay analysis, regime detection
- Hardening a strategy for production: circuit breakers, duplicate order prevention, broker reconnect logic

## Decision Trees

<!-- STANDARD: 3min -->
Full detail → references/algorithmic-trader-computations.md

### DT1: Execution Method → Full detail in references

```

Order size >10% ADV? → YES → TWAP/VWAP (minimize impact). Split across day.
  ↓ NO
Spread >0.5%? → YES → Limit order (patient). NO → Marketable limit (immediate).
  ↓
Urgency HIGH? → Smart router + marketable limit. Urgency LOW → Iceberg, hide size.

```

### DT2: Slippage Response → Full detail in references

```

Slippage >2x expected? → YES → PAUSE. Review: market moving? Wide spread? Routing issue?
  ↓ NO                                                ↓
Continue ✓                                     Adjust: switch venue, change limit price, or abort.

```

### Decision Tree 1: In-scope or out?
- In-scope: follow Core Workflow and verify.
- Out-of-scope: route to the owning skill and stop.

## Gotchas
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Algorithm executes with stale market data producing incorrect signals | $10K-$1M in trading losses per incident | Implement data freshness heartbeat checks; halt trading on stale data; use redundant data feeds with failover under 100ms |
| Backtest overfits to historical data — 'looks great in backtest, fails in production' | $50K-$500K in strategy deployment losses | Use walk-forward validation; out-of-sample test on unseen periods; incorporate transaction costs and slippage in backtest; paper trade for 30+ days before live |
| Position sizing error due to unhandled edge case (corporate action, split, dividend) | $5K-$100K in unintended exposure | Automate corporate action handling; add position size sanity limits as circuit breakers; reconcile positions against prime broker daily |
| Personal finance plan excludes emergency fund leading to forced asset liquidation | $5K-$50K in opportunity cost and tax penalties | Build 3-6 month emergency fund before investing; keep in high-yield savings; treat as non-negotiable first step in any financial plan |
| Home purchase decision based on pre-approval max without accounting for hidden costs | $20K-$100K in financial strain over first year | Model total cost of ownership including taxes, insurance, maintenance (1-2% of home value/year), HOA, and utilities; stay under 28% DTI for housing |

| Gotcha | Cost | Fix |
|--------|------|-----|
| Algorithm executes with stale market data producing incorrect signals | $10K-$1M in trading losses per incident | Implement data freshness heartbeat checks; halt trading on stale data; use redundant data feeds with failover under 100ms |
| Backtest overfits to historical data — 'looks great in backtest, fails in production' | $50K-$500K in strategy deployment losses | Use walk-forward validation; out-of-sample test on unseen periods; incorporate transaction costs and slippage in backtest; paper trade for 30+ days before live |
| Position sizing error due to unhandled edge case (corporate action, split, dividend) | $5K-$100K in unintended exposure | Automate corporate action handling; add position size sanity limits as circuit breakers; reconcile positions against prime broker daily |
| Personal finance plan excludes emergency fund leading to forced asset liquidation | $5K-$50K in opportunity cost and tax penalties | Build 3-6 month emergency fund before investing; keep in high-yield savings; treat as non-negotiable first step in any financial plan |
| Home purchase decision based on pre-approval max without accounting for hidden costs | $20K-$100K in financial strain over first year | Model total cost of ownership including taxes, insurance, maintenance (1-2% of home value/year), HOA, and utilities; stay under 28% DTI for housing |

## Verification
<!-- STANDARD: 3min -->

- [ ] Backtest: no look-ahead bias — all signals use data that was available at the time of the trade
- [ ] Survivorship-free universe: backtest universe includes delisted and acquired securities
- [ ] Transaction costs: model accounts for commission, bid-ask spread, and market impact at trade size
- [ ] Out-of-sample test: strategy performs on unseen data (different time period) within acceptable degradation
- [ ] Walk-forward: strategy parameters re-optimized on rolling windows — performance stable across periods

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## Best Practices

1. **Paper trade for 30 days minimum before live capital.** The gap between backtest and reality is always larger than you think. Paper trade with realistic fills (not mid-price) and actual slippage assumptions. If you cann
2. **Half-Kelly is full Kelly in practice.** Full Kelly assumes you know your edge exactly — you do not. Half-Kelly preserves 75% of the growth rate with 50% of the drawdown risk. When in doubt, quarter-Kelly.
3. **Size positions by risk, not conviction.** "High conviction" signals do not deserve larger positions. They deserve the same 1-2% risk per trade. Conviction is an emotion; position sizing is math. Let the math win.
4. **Walk-forward validation is the only backtest that matters.** A single in-sample backtest with optimized parameters is curve-fitting, not strategy development. Minimum five walk-forward windows with stable parameters ac
5. **Monitor signal decay in real time.** UOA signals have a half-life measured in hours to days. If your signal-to-execution pipeline takes more than 5 minutes, you are trading stale information. Benchmark: time from signa
6. **Treat commissions as a strategy input, not an afterthought.** On a $3,000 options position with $65 round-trip commissions, you need +2.2% just to break even. Factor commissions into position sizing — $2,000 minimum tr
7. **Log everything — every fill, every rejection, every reconnect.** Trading bugs are discovered in logs, not in P&L. Structured JSON logs with correlation IDs from signal → validation → order → fill → position update → ex
8. **Run a "paper clone" of live strategies.** Mirror your live strategy in a paper account with the same signals, same sizing, same timing. Divergence between paper and live P&L reveals execution problems — slippage you di

> Full depth: `references/best-practices.md`

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Live trading executed on stale data from the previous close — system traded on 4-hour-old quotes | Market-data feed lost connection; signal validation used last cached prices without a freshness check; no timestamp validation before order submission | Reject any signal where `(now - data.timestamp).seconds > 60` during market hours; add feed heartbeat monitoring that halts trading if the feed drops >120s | Stale data is worse than no data — a freshness gate and feed heartbeat are mandatory before any order is generated |
| Broker API retry caused a double-fill — 2,000 shares bought instead of 1,000, doubling position and risk | Network timeout on order submission; code retried without an idempotency key; broker processed both as independent orders; the stop only covered the first fill | Add `client_order_id` to every order; check order status before retrying; never resubmit a timed-out order without confirming it did not fill | Timeouts are not rejections — idempotency keys and status checks are what prevent double execution |
| Circuit breaker fired at -20% drawdown but liquidation crashed mid-loop, leaving positions open | Liquidation iterated `portfolio.positions` and one position had already been closed by a stop-loss; the IndexError aborted liquidation of the rest | Wrap each position iteration in try/except; skip missing positions; liquidate independently so one failure cannot block the others | A breaker that cannot liquidate is decoration — liquidation must be resilient per-position |
| Backtest reported Sharpe 2.5; live Sharpe was -0.3 | Walk-forward validation used only 1-2 out-of-sample windows of ~6 months each — too little data to distinguish skill from luck | Require ≥252 trading days per out-of-sample window and ≥5 walk-forward windows; reject if out-of-sample Sharpe varies >50% across windows | Short backtests inflate ratios — statistical significance requires enough out-of-sample data |
| Position ran unprotected for hours after an order-submission timeout | Broker call timed out at market open; no retry with backoff and no order-status verification; the order had actually filled but the client never learned | Exponential backoff (1s→16s, max 5); after timeout query order status before retrying; alert after 5 retries | A lost confirmation is not a lost order — verify status, then decide whether to retry |

> Full decoder with auto-recovery loops: `references/error-decoder.md`
## Production Checklist

Before delivering, verify:

- [ ] **ID:** Checklist Item

> Full checklist with validation commands: `references/checklist.md`

## State Log
All material decisions, regime/calibration changes, and escalations are appended to the decision ledger ({at, what, by}); version bumps are recorded in the repository changelog so context is recoverable without replaying prior sessions.

## Error Recovery
| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Model/backtest disagrees with live market | Re-validate inputs and data source; reproduce the signal | Cross-check against a second data vendor and regime filter | Escalate with both datasets attached; do not trade on the disagreement |
| Strategy underperforms its backtest | Check regime drift, slippage, and position sizing assumptions | Recalibrate parameters against the current regime | Mark the strategy suspended until recalibration is verified |
| Data feed gap or stale quote | Confirm feed status and timestamp freshness | Fail over to the secondary feed; widen execution guards | Halt automated flow; escalate with the incident record |
| Unexpected risk/limit breach | Freeze position growth; recompute exposure | Reduce size to within limits | Escalate with full P&L and exposure evidence |

## Cross-Skill Coordination
| Upstream Skill | What You Receive | When to Involve |
|----------------|------------------|-----------------|
| `data-engineer` / market-data sources | Clean price/volume and fundamentals | Before any model or strategy work |
| `quantitative-analyst` or analytics | Model outputs and statistical baselines | When validating signals or calibrating |
| `risk-engineer` / risk tooling | Limits and exposure context | When sizing positions or setting guards |

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
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)

## Core Workflow

1. Intake: read the task and confirm scope.
2. Execute: perform the domain work per this skill's guidance.
3. Verify: check the output against the request with concrete evidence before delivering.

## Proactive Triggers

- New task arrives that matches the description: invoke this skill's workflow.
- Existing output needs re-verification: re-run the verify step rather than assuming.
- A claim lacks a source: flag it instead of passing it forward.

## What Good Looks Like

Output is scoped to the request, grounded in evidence, states its assumptions and limitations, and is ready for downstream consumption without re-derivation.
| ☐ | Complete when output is scoped to the request and grounded in evidence 1 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 2 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 3 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 4 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 5 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 6 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 7 | the check in the criterion passes and is recorded |
| ☐ | Complete when output is scoped to the request and grounded in evidence 8 | the check in the criterion passes and is recorded |
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

## Anti-Patterns

- ❌ Adding unverified claims to look complete | ✅ Marking unknowns as unknown
- ❌ Copying the structure without the evidence | ✅ Filling every section from the actual task
- ❌ Looping on the same failed approach | ✅ Changing one lever per retry
- ❌ Hiding a limitation until review | ✅ Naming limitations up front
- ❌ Optimizing for length | ✅ Optimizing for verifiable correctness
- In-scope: proceed through Core Workflow.
- Out-of-scope: route to the owning skill and stop.

### Decision Tree 2: Verify or escalate?
- Verifiable locally: run the check and record the result.
- Blocked externally: escalate once with full context.

### Decision Tree 3: Ship or revise?
- Meets What Good Looks Like: deliver with evidence.
- Gaps found: revise before delivering.
