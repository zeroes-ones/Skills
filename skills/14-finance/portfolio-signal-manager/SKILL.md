---
name: portfolio-signal-manager
description: >
  Use when synthesizing multiple trading signals (technical + fundamental) into unified
  portfolio decisions, resolving conflicts between contradictory signals via weighted
  decision matrix, managing position sizing (Kelly, risk-parity, volatility-adjusted 1/N),
  connecting broker accounts via MCP for portfolio synchronization, triaging signals when
  multiple fire simultaneously with limited capital, rebalancing with correlation-aware
  allocation (max 25% per sector, max 10% per position), or monitoring portfolio risk (VaR,
  CVaR, beta exposure, drawdown). Handles signal conflict resolution with calibrated source
  weights, MCP broker connectivity with full state machine, correlation-aware diversification
  using economic driver taxonomy, and circuit breakers for cascading failure protection.
  Do NOT use for generating technical signals (route to technical-signals-engineer), computing
  valuations (route to fundamental-analyst), or executing orders (route to algorithmic-trader).
license: MIT
tags:
  - portfolio-signal-manager
  - signal-synthesis
  - position-sizing
  - mcp-broker
  - risk-management
  - portfolio-optimization
  - conflict-resolution
  - multi-asset
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 4500
chain:
  consumes_from:
    - technical-signals-engineer
    - fundamental-analyst
    - algorithmic-trader
    - market-data-engineer
  feeds_into:
    - algorithmic-trader
    - data-scientist
    - observability-engineer
  alternatives:
    - data-scientist
---

# Portfolio Signal Manager
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Synthesize trading signals from multiple sources into unified, sized, risk-managed portfolio decisions. This skill is the central orchestrator of the trading ecosystem — it ingests technical signals from technical-signals-engineer and fundamental signals from fundamental-analyst, resolves conflicts through a weighted decision matrix, applies position sizing via Kelly and risk-parity, connects to broker accounts through MCP for portfolio synchronization, and outputs execution-ready trade instructions to algorithmic-trader. Built to handle the real problem: what do you do when the technicals say buy, the fundamentals say sell, and 5 other stocks are also firing signals with only 40% of capital remaining?
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


### Portfolio Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Resolve all active signal conflicts.** For every pair of conflicting signals (e.g., technical says BUY, macro says SELL), document the resolution logic. Signal conflicts that go unresolved produce contradictory position changes. | [SIGNAL_CONFLICT] A portfolio with 3 bullish signals and 2 bearish signals on the same asset has a net signal of zero — not bullish. Unresolved conflicts cause whipsaw: buy on one signal, sell on the next, accumulate transaction costs. | Signal dashboard, conflict resolution matrix, priority hierarchy |
| **RP-F2** | **Check circuit breaker thresholds.** Verify: drawdown limit (default: 15% from peak), single-position loss limit (default: 5%), correlation-based concentration limit (default: 30% in any sector), and daily loss limit (default: 3%). | [DRAWDOWN_SPIRAL] Without hard circuit breakers, a 10% drawdown becomes 20% becomes 40%. Each recovery requires progressively larger gains: -10% needs +11%, -20% needs +25%, -40% needs +67%. | Circuit breaker configuration, account drawdown history, daily P&L reports |
| **RP-F3** | **Rebalance check: are current allocations within tolerance bands?** Compare target weights vs. actual weights. Positions that have drifted >20% from target need rebalancing evaluation (cost vs. drift risk). | [DRIFT_RISK] A 5% tactical allocation that grows to 15% through outperformance has become a 15% strategic bet without a decision. Rebalancing isn't about locking in profits — it's about maintaining intended risk exposure. | Position sizing sheet, allocation targets, tax-impact analysis |
| **RP-F4** | **Assess liquidity of all holdings.** For each position: what % of ADV does the position represent? If any position > 5% of ADV, exiting will move the market against you. | [LIQUIDITY_TRAP] A profitable position you can't exit without crashing the price is not a position — it's a hostage situation. Liquidity risk is the most underestimated portfolio risk. | ADV data, bid-ask spread history, depth of market |
| **RP-F5** | **Stress-test the portfolio against the last 3 regime shifts.** Apply the portfolio composition to: (a) the most recent correction (-10%), (b) the most recent bear market (-20%), (c) the most recent crash (-30%+). Document max portfolio drawdown in each. | [REGIME_FRAGILITY] A portfolio optimized for the current regime is fragile by definition. Regime-agnostic portfolios survive; regime-optimized portfolios get destroyed when the regime changes — which it always does. | Historical regime dates, strategy backtest data, composite portfolio P&L simulation |



## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "portfolio\|allocation\|position_sizing\|signal.*conflict\|rebalance")` AND `file_contains("*.py", "kelly\|risk_parity\|VaR\|drawdown\|correlation")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py", "SMA\|EMA\|RSI\|MACD\|crossover")` AND NOT `file_contains("*.py", "portfolio\|allocation\|position_size")` | Invoke **technical-signals-engineer** instead. Single-signal generation. |
| A3 | `file_contains("*.py", "PE\|DCF\|discounted_cash\|piotroski\|altman")` AND NOT `file_contains("*.py", "portfolio\|conflict")` | Invoke **fundamental-analyst** instead. Single-stock valuation. |
| A4 | `file_contains("*.py", "alpaca\|broker.*order\|TWAP\|VWAP.*execution\|stop_loss")` AND NOT `file_contains("*.py", "portfolio.*signal\|signal.*synthes")` | Invoke **algorithmic-trader** instead. Order execution domain. |
| A5 | `file_exists("mcp_config.json\|broker_mcp.py")` AND `file_contains("*.py", "account\|positions\|buying_power")` | Jump to **Core Workflow** — Phase 0 (MCP Connection). |

### Intent Route

```

What portfolio management task?
├── Connecting broker account via MCP → Phase 0
├── Resolving conflicting signals (tech buy + fund sell) → Phase 1
├── Sizing positions across multiple signals → Phase 2
├── Risk monitoring and stop management → Phase 3
├── Correlation-aware portfolio construction → Phase 4
└── Full signal-to-execution pipeline → Phase 5

```

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to synthesize signals without receiving structured output from both signal sources. Portfolio decisions based on "I think the technicals look good" without actual signal JSON from technical-signals-engineer are guesses, not synthesis. | Trigger: portfolio decision references "technical analysis" or "fundamentals" without a signal_id or structured JSON from the source skill | STOP. "Synthesis requires structured input. Request signal JSON from technical-signals-engineer and/or fundamental-analyst before making portfolio decisions. Raw commentary is not signal data." |
| R2 | REFUSE to size a position without knowing current portfolio state. Position sizing without knowing existing positions, buying power, and correlation exposure is dangerous — it can lead to over-concentration, margin calls, or correlation cascades. | Trigger: position_size calculated without referencing current_portfolio.positions or buying_power | STOP. "Position sizing requires portfolio context. Sync portfolio state via MCP broker connection or manual input before sizing. Include: current positions, buying power, margin used, sector exposures." |
| R3 | REFUSE to execute when technical and fundamental signals directly conflict without explicit conflict resolution. A technical BUY + fundamental SELL must go through the weighted decision matrix (Phase 1). Never default to one source — neither technicals nor fundamentals are always right. | Trigger: conflicting signals detected (tech_signal != fund_signal) but no conflict_resolution block in output | STOP. "Signal conflict detected: technical={direction}, fundamental={direction}. Run weighted decision matrix (Phase 1) before proceeding. Document which source prevails and why." |
| R4 | REFUSE to allocate >25% of portfolio to any single sector without explicit user override. Sector concentration killed more portfolios than bad stock picking. In 2000 (tech), 2008 (financials), 2020 (energy), sector bets that looked smart became portfolio disasters. | Trigger: sector_exposure > 0.25 of portfolio_value AND sector_override != True | STOP. "Sector concentration {sector} at {pct}% exceeds 25% limit. Either reduce position sizes in this sector or explicitly override with documented rationale and stop-loss plan." |
| R5 | REFUSE to connect to broker API without verifying idempotency protections. MCP broker connections without idempotency keys risk duplicate orders during network retries — a $5K trade becomes $50K if submitted 10 times. | Trigger: broker connection established but idempotency_key not configured in order submission path | STOP. "Broker connection missing idempotency protection. Configure idempotency keys (UUID per order) before enabling live trading. Test with a $1 paper trade first." |
| R6 | REFUSE to rebalance within 30 minutes of market close. Last-30-minute spreads widen 3-5x, market-on-close orders have unpredictable fills, and weekend gap risk compounds any execution error. | Trigger: current_time within 30 minutes of market close (15:30-16:00 ET) AND rebalance_action contains market orders | STOP. "Within 30 minutes of close — wide spreads and MOC uncertainty. Defer rebalancing to next session open or use limit orders only with 3x normal patience." |
| R7 | NEVER treat past correlation as future correlation. The correlation matrix from the last 60 days will be wrong during the next regime change. In March 2020, all correlations went to 1.0 in 3 days. Diversification that relies on stable correlations is not diversification. | Trigger: portfolio optimization uses correlation_matrix without stress_test correlation → 1.0 scenario | STOP. "Correlation-based optimization without stress testing. Run portfolio through correlation→1.0 shock scenario. If drawdown > 30% in that scenario, reduce leverage or add uncorrelated assets." |

## Anti-Hallucination
**Admit uncertainty** when synthesizing across domains. **Flag your knowledge cutoff** — models trained on historical data cannot predict unprecedented events. **Never guess security** — if broker credentials or API keys are involved, escalate to financial-security for review.


<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "I have 5 BUY signals with 70+ confidence — I'll take all of them at full size." | Five 70-confidence signals with 0.7 correlation to SPY means you have essentially one big SPY bet with 5x the transaction costs. True signal independence is rare. In a 10% market correction, all 5 positions drop 8-12% simultaneously because they share a common factor (beta). Your "diversified" portfolio has an effective N of ~1.3, not 5. **Cost: $50K-$200K in correlated drawdowns that "shouldn't have happened" based on naive diversification assumptions.** |
| "The technical signal says BUY with 85 confidence and the fundamental signal says SELL with 55 confidence — technicals win." | Confidence scores from different systems are not comparable without calibration. Technical confidence measures pattern purity; fundamental confidence measures valuation margin. An 85 technical confidence on a 3-indicator alignment is not "more right" than a 55 fundamental confidence based on DCF range. They measure different things. **Cost: $30K-$150K in "high confidence" trades that fundamental analysis would have prevented. Calibrate each source independently before comparing scores.** |
| "I'll connect to the broker, sync the portfolio, and start trading — the MCP setup is straightforward." | Broker MCP connections have 12+ failure modes: auth token expiry mid-session, rate-limit backoffs that silently drop orders, WebSocket disconnects during high volatility, position sync lag after partial fills, and dividend adjustments that change cost basis overnight. Production broker connectivity is a state machine with 8 states, not a simple REST call. **Cost: $5K-$500K in execution errors from "straightforward" broker connections. Every failure mode needs a handler. See Phase 0 — MCP Connection State Machine.** |
| "Equal weight position sizing is good enough for a 10-stock portfolio." | Equal weight ignores volatility. A $10K position in a stock with 15% daily vol (e.g., TSLA) has 3x the risk contribution of a $10K position in a stock with 5% daily vol (e.g., JNJ). Your "equal weight" portfolio is actually 75% concentrated in the top 3 most volatile names by risk contribution. **Cost: $15K-$60K in unexpected volatility-driven drawdowns. Use volatility-adjusted position sizing: position = capital / (N × relative_volatility).** |
| "These two ETFs both say BUY — SPY and VOO are different products from different issuers." | SPY and VOO both track the S&P 500. Holding both is holding the same thing twice with different expense ratios. ETF overlap >90% by holdings weight = same position. You're paying two expense ratios for one exposure. **Cost: $100-$500/year in duplicate fees. Always check holdings overlap before adding a new ETF to an existing position.** |
| "The portfolio is diversified — 20 stocks across 8 sectors." | If 12 of those 20 stocks have beta >1.3 to SPY, and 8 of 20 are tech or tech-adjacent (Amazon is "consumer discretionary," Google is "communication services," but both move with tech), your 8-sector diversification is actually 3 real sectors with high beta. **Cost: $100K-$500K in "diversified" portfolios that crash together. Diversify by factor exposure, not GICS sector labels.** |


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
| ❌ **Equal-weight without vol adjustment** | A $10K position in a 3% vol stock has 9x the risk contribution of a 1% vol stock | ✅ Always vol-adjust positions. Risk-parity is the minimum; Kelly-optimal is the goal |
| ❌ **Skipping conflict resolution** | "The signals mostly agree" — undetected conflicts accumulate silently until a 20% drawdown forces attention | ✅ Run the weighted decision matrix for every ticker with multiple signals. Admit uncertainty when confidence gap is <10% |
| ❌ **GICS-based diversification** | Amazon (Consumer Disc) gets half profit from AWS (Tech). Sector labels lie about economic drivers | ✅ Diversify by economic driver and return correlation, not by GICS sector. Compute N_effective monthly |
| ❌ **Manual conviction sizing** | "I really like this one" doubles the position. Emotional sizing destroys mechanical risk budgets | ✅ Mechanical sizing only. No human override on position size. Flag any override for audit |
| ❌ **Broker connection tested once** | Tokens expire, rate limits change, APIs deprecate. One successful test is a snapshot, not a guarantee | ✅ Daily connection health check with paper-trade validation. Never guess security — test credentials on sandbox first |

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

### Phase 0: MCP Broker Connection (State Machine)

```

1. CONNECTION STATE MACHINE (8 states, all must be handled)
   DISCONNECTED → AUTHENTICATING → CONNECTED → SYNCING → READY → EXECUTING → RECONCILING → DISCONNECTED

   AUTHENTICATING:
   ├── OAuth token exchange or API key validation
   ├── Token expiry tracking: refresh 5 min before expiry
   └── Failure: retry 3x with exponential backoff (1s, 5s, 25s), then alert

   CONNECTED:
   ├── WebSocket for real-time order/position updates
   ├── Heartbeat: ping every 30s, reconnect if no pong in 60s
   └── Rate limit tracking: remaining requests per minute

   SYNCING:
   ├── Download positions: ticker, quantity, avg_cost, market_value, unrealized_pnl
   ├── Download orders: pending, filled (today), rejected
   ├── Download account: buying_power, margin_used, margin_limit, portfolio_value
   └── Reconcile: compare broker positions vs local state, flag discrepancies >$100

   READY:
   ├── Portfolio state current (sync < 60s old)
   ├── Buying power known
   ├── Idempotency key generator active
   └── Circuit breaker configured (max 5 rejected orders in 60s → halt)

   EXECUTING:
   ├── Submit order with idempotency key
   ├── Await fill confirmation (timeout 30s for market, 300s for limit)
   ├── On fill: update local position immediately
   ├── On reject: log reason, do NOT retry without investigation
   └── On timeout: query order status, do NOT resubmit (idempotency protects)

   RECONCILING:
   ├── Post-execution: compare expected vs actual fill price (slippage check)
   ├── Post-settlement: verify T+2 settlement completed
   └── Daily: full position reconciliation broker vs local

2. MCP INTERFACE CONTRACT (what the broker MCP server must expose)
   Tools:
   ├── get_account() → Account(buying_power, margin, portfolio_value, day_trades_left)
   ├── get_positions() → [Position(ticker, qty, avg_cost, mkt_value, unrealized_pnl)]
   ├── get_orders(status="open|filled|rejected") → [Order(id, ticker, side, qty, filled_qty, status)]
   ├── place_order(ticker, side, qty, type, limit_price, idempotency_key) → Order
   ├── cancel_order(order_id) → bool
   └── get_order_status(order_id) → Order

   Resources (optional but recommended):
   ├── broker://{broker_id}/account — live account snapshot
   ├── broker://{broker_id}/positions — live positions snapshot
   └── broker://{broker_id}/orders — live orders snapshot

   Complete when: MCP connection in READY state. Portfolio synced. Idempotency keys configured.

```

### Phase 1: Signal Ingestion & Conflict Resolution

```

1. SIGNAL INGESTION CONTRACT (standardized input from source skills)

   Input from technical-signals-engineer:
   {
     "source": "technical-signals-engineer",
     "signal_id": "tech-20260730-0421",
     "ticker": "AAPL",
     "timestamp": "2026-07-30T14:21:00Z",
     "direction": "BUY",
     "confidence": 78,
     "confidence_breakdown": {
       "indicator_alignment": 85,    # % of indicators agreeing
       "volume_confirmation": 72,    # volume supports the move
       "regime_support": 65,         # current regime favors this
       "timeframe_alignment": 80     # multi-timeframe agreement
     },
     "indicators": {
       "primary": ["SMA_50_200_cross", "RSI_oversold_reversal"],
       "confirming": ["MACD_bullish_cross", "OBV_rising"],
       "cautioning": ["BB_squeeze_breakout_unconfirmed"]
     },
     "regime": "trending",
     "parameters_used": {"rsi_period": 14, "bb_std": 2.0, "macd_fast": 12, "macd_slow": 26},
     "caveats": ["Near earnings (+5 trading days)", "Gap up 2 days ago"],
     "raw_confidence_after_caveats": 78
   }

   Input from fundamental-analyst:
   {
     "source": "fundamental-analyst",
     "signal_id": "fund-20260730-1135",
     "ticker": "AAPL",
     "timestamp": "2026-07-30T11:35:00Z",
     "direction": "HOLD",
     "confidence": 62,
     "confidence_breakdown": {
       "valuation_margin": 45,       # DCF vs market price spread
       "quality_triangulation": 78,  # F-Score + Z-Score + M-Score avg
       "earnings_quality": 70,       # FCF/NI ratio, accruals
       "comparable_alignment": 55    # vs industry median
     },
     "valuation": {
       "dcf_range": {"bear": 165, "base": 195, "bull": 230},
       "current_price": 198,
       "margin_of_safety": -0.015,   # negative = above base case
       "comparables_median_pe": 31.5,
       "company_pe": 34.2
     },
     "quality_scores": {
       "piotroski_f_score": 7,
       "altman_z_score": 6.8,
       "beneish_m_score": -2.4
     },
     "red_flags": [],
     "caveats": ["Premium to comparables", "Near top of DCF range"]
   }

2. CONFLICT DETECTION
   For each ticker with signals from both sources:
   ├── Both AGREE (both BUY, both SELL, both HOLD) → skip conflict resolution, proceed to sizing
   ├── One HOLD, other ACTION (BUY/SELL) → treat HOLD as "don't add" not "oppose"
   └── DIRECT CONFLICT (one BUY, other SELL) → enter WEIGHTED DECISION MATRIX

3. WEIGHTED DECISION MATRIX (for direct conflicts)

   Step 1: Calibrate confidence scores (different systems, different scales)
   ├── Technical confidence calibration factor: 0.85 (tends to overstate by ~15% in backtests)
   ├── Fundamental confidence calibration factor: 0.90 (tends to overstate by ~10%)
   └── Calibrated_tech = raw_tech_confidence × 0.85
       Calibrated_fund = raw_fund_confidence × 0.90

   Step 2: Apply regime-dependent source weighting
   ├── Trending regime (ADX > 25):    Technicals weight = 0.65, Fundamentals weight = 0.35
   ├── Ranging regime (ADX < 20):     Technicals weight = 0.35, Fundamentals weight = 0.65
   ├── Volatile regime (VIX > 30):    Technicals weight = 0.50, Fundamentals weight = 0.50
   └── Earnings week (+/- 5 days):    Technicals weight = 0.25, Fundamentals weight = 0.75

   Step 3: Compute weighted decision score
   Decision_Score = (Calibrated_tech × Tech_Weight × Tech_Direction) +
                    (Calibrated_fund × Fund_Weight × Fund_Direction)
   Where Direction: BUY=+1, HOLD=0, SELL=-1

   Step 4: Decision thresholds
   ├── Decision_Score > +15 → BUY  (strongly favors buy)
   ├── Decision_Score +5 to +15  → BUY_WITH_CAUTION (lean buy but flag risk)
   ├── Decision_Score -5 to +5   → HOLD (conflict unresolved, do nothing)
   ├── Decision_Score -5 to -15  → SELL_WITH_CAUTION (lean sell)
   └── Decision_Score < -15 → SELL (strongly favors sell)

   Step 5: For BUY_WITH_CAUTION or SELL_WITH_CAUTION — apply additional gates
   ├── Position size capped at 50% of normal allocation
   ├── Must set tighter stop-loss (1.5× ATR vs normal 2× ATR)
   └── Flag for review after 5 trading days

4. CONFLICT RESOLUTION DOCUMENTATION (every resolution is audit-trailed)
   {
     "ticker": "AAPL",
     "conflict": "BUY vs HOLD",
     "decision": "BUY_WITH_CAUTION",
     "decision_score": 11.2,
     "breakdown": {
       "tech_calibrated": 66.3,
       "fund_calibrated": 55.8,
       "regime": "trending",
       "tech_weight_applied": 0.65,
       "fund_weight_applied": 0.35
     },
     "rationale": "Technicals dominate in trending regime. Fundamentals don't say SELL — they say 'not cheap.' Trending regime supports following technicals with reduced size.",
     "risk_constraints": {
       "max_position_pct": 0.05,    # 50% of normal 10%
       "stop_loss_atr_multiple": 1.5,
       "review_date": "2026-08-06"
     }
   }

   Complete when: All incoming signals have a resolution (AGREE/CONFLICT_RESOLVED).
   Every conflict has a Decision_Score and documented rationale.

```

### Phase 2: Position Sizing

```

1. CAPITAL POOL CALCULATION
   Buying_Power = min(Account.cash * 2, Account.margin_limit)  # Reg T margin
   Reserved_Capital = max(Portfolio_Value * 0.05, $5,000)  # 5% always in reserve
   Available_Capital = Buying_Power - Current_Exposure - Reserved_Capital

   If Available_Capital <= 0: queue signals, trigger capital alert, STOP.

2. SIGNAL TRIAGE (when more signals than capital)
   Rank all resolved signals by:

   Signal_Priority_Score = (Calibrated_Confidence * 0.5) +        # how sure
                           (Quality_Triangulation_Score/100 * 0.3) + # how solid the company
                           (Regime_Compatibility * 0.2)            # how well it fits current market

   Sort descending. Allocate capital top-down until Available_Capital exhausted.

   Tiebreaker: prefer ETFs over individual stocks (diversification), prefer
               lower sector concentration (already-weighted sectors get deprioritized).

3. POSITION SIZING METHOD (per selected signal)

   Base_Position = Available_Capital × (1 / N_Selected_Signals)  # 1/N baseline

   Size Method A — Volatility-Adjusted 1/N (default, use when no Kelly):
   ├── Vol_Weight = 1 / (Asset_30d_Volatility / Median_Volatility_Across_All_Selected)
   ├── Adjusted_Position = Base_Position × Vol_Weight
   ├── Cap: Adjusted_Position ≤ min(Portfolio_Value × 0.10, $25,000) per position
   └── Cap: Leveraged ETF position ≤ Portfolio_Value × 0.05

   Size Method B — Kelly Criterion (use when: >50 trades history, win_rate known):
   ├── f* = (bp - q) / b  where b = avg_win/avg_loss, p = win_rate, q = 1-p
   ├── Half-Kelly: f = f* / 2  (standard practice — full Kelly is too aggressive)
   ├── Adjusted_Position = Portfolio_Value × f
   ├── REQUIREMENT: >50 historical trades for this ticker+strategy AND p > 0.45
   └── If requirements not met: FALL BACK to Method A with WARNING

   Size Method C — Risk-Parity (use when: portfolio-level rebalancing):
   ├── Risk_Budget = Available_Capital × (1 / N_Selected)
   ├── Position = Risk_Budget / Asset_30d_Volatility
   └── Rebalance: if drift > 20% from target weight, trigger rebalance

4. POSITION SIZING OVERRIDES AND EMERGENCY DOWNSIZES

   | Condition | Action |
   |-----------|--------|
   | ETF holdings overlap > 90% with existing position | Size = 0, raise "Duplicate Exposure" flag |
   | Stock is within +/- 5 days of earnings | Reduce size by 50% |
   | Signal is BUY_WITH_CAUTION or SELL_WITH_CAUTION | Reduce size by 50% |
   | Sector exposure would exceed 25% with this position | Reduce to keep sector ≤ 25% or skip |
   | Position would be < $1,000 after sizing | Skip (too small to be worth commissions/slippage) |
   | VIX > 35 (extreme fear) | Reduce ALL new positions by 40% |
   | Portfolio drawdown > 15% from peak | HALT all new positions. Only allow defensive exits. |

5. OUTPUT: SIZED SIGNAL QUEUE
   [
     {"rank": 1, "ticker": "AAPL", "direction": "BUY", "decision": "AGREE",
      "position_size": "$8,200", "pct_portfolio": 0.82, "method": "vol-adjusted-1/N",
      "stop_loss": "$185.40", "take_profit": "$215.00", "limit_price": "$198.50"},
     {"rank": 2, "ticker": "MSFT", "direction": "BUY", "decision": "BUY_WITH_CAUTION",
      "position_size": "$4,100", "pct_portfolio": 0.41, "method": "vol-adjusted-1/N (50% caution haircut)",
      "stop_loss": "$430.00", "take_profit": "$475.00", "limit_price": "$448.00"},
     ...
   ]

   Complete when: Every selected signal has a sized position within capital constraints.
   No position exceeds 10% portfolio cap. Sector concentrations checked.

```

### Phase 3: Portfolio Risk Monitoring

```

1. REAL-TIME RISK DASHBOARD (recompute every 60 seconds or on new fill)

   Portfolio-Level:
   ├── Total Value: $∑(position.mkt_value)
   ├── Beta-Weighted Exposure: $∑(position.mkt_value × position.beta)
   │   └── If Beta_Exposure > Portfolio_Value × 1.5: "Over-exposed to market risk"
   ├── VaR(95%, 1-day): $Value_At_Risk computed via historical simulation (252-day window)
   │   └── If VaR > Portfolio_Value × 0.03: "VaR Alert — 3% daily risk threshold breached"
   ├── CVaR(95%): $Expected shortfall beyond VaR (always > VaR, often 1.3-1.5x)
   ├── Max Drawdown from Peak: −XX.X%
   │   ├── Drawdown 5-10%: Yellow alert (consider reducing position sizes)
   │   ├── Drawdown 10-15%: Orange alert (halt new buys, tighten stops)
   │   ├── Drawdown 15-20%: Red alert (exit signal for weakest 50% of positions)
   │   └── Drawdown >20%: EMERGENCY (liquidate all, investigate root cause)
   ├── Sharpe Ratio (trailing 90-day): Risk-free = 3-month T-bill
   │   └── Sharpe < 0: "Negative risk-adjusted returns — strategy underperforms cash"
   └── Correlation Matrix (trailing 60-day, rolling):
       ├── If any pair correlation > 0.80: "High correlation pair: {A}, {B}"
       ├── Recompute effective N: N_effective = (sum of eigenvalues)² / sum(eigenvalues²)
       └── If N_effective < 3 for portfolio of 10+ stocks: "Diversification failure"

   Sector-Level:
   ├── Sector_Exposure[sector] = $∑(position.mkt_value) / Portfolio_Value per sector
   ├── If Sector_Exposure > 0.25: "SECTOR LIMIT BREACHED: {sector} at {pct}%"
   └── Factor exposure heatmap: Beta, Size, Value, Momentum, Quality, Low Vol

   Position-Level:
   ├── Each position: current P&L, P&L%, days held, signal age (stale if >20 trading days)
   ├── Stale signal (age > 20 days): request signal refresh from source skill
   ├── Stop-loss proximity: if price within 1.5× ATR of stop, flag "Stop-Loss Imminent"
   └── Gap risk: if position has earnings in next 10 days, flag "Earnings Gap Risk"

2. AUTOMATED RISK RESPONSES (configurable thresholds)

   | Trigger | Response |
   |---------|----------|
   | VaR(95%) > 4% of portfolio | Email/SMS alert. Reduce all position sizes by 25%. |
   | Two consecutive days with -2% loss | Halt new positions. Review all open signals. |
   | Correlation matrix N_effective drops below 3 | Reduce leverage by 50%. Sell highest-correlated pair. |
   | Any single position P&L > -15% | Auto-close position. Post-mortem required before re-entry. |
   | Margin used > 80% of margin limit | Reduce margin exposure to <60%. Sell weakest positions. |
   | Broker API disconnection > 2 minutes | Cancel all open orders. Do not submit new orders. |

3. STRESS TESTING (weekly, or on request)

   Run portfolio through these scenarios:
   ├── 2008-style: SPY -38%, Correlation → 1.0, VIX → 80
   ├── 2020-COVID: SPY -34% in 23 days, VIX → 82, bonds +5%
   ├── 2022-rate-hike: SPY -19%, Growth -30%, Value -7%
   ├── Tech-crash: QQQ -33%, correlation within tech → 1.0
   ├── Liquidity-crisis: Spreads 5x, no fills on limit orders > ATR
   └── Flash-crash: SPY -9% in 30 minutes, circuit-breakers triggered

   For each scenario: report estimated drawdown, max margin call, days to recovery.
   If any scenario produces drawdown > 40%: REDUCE LEVERAGE IMMEDIATELY.

   Complete when: Risk dashboard populated. All thresholds configured.
   Stress tests run and worst-case drawdown known.

```

### Phase 4: Correlation-Aware Portfolio Construction

```

1. PRE-ALLOCATION CORRELATION CHECK
   Before finalizing any position, compute pairwise correlations of the candidate
   with every existing position (trailing 60 days, daily returns):

   For each candidate ticker:
   ├── Compute correlation with each existing position
   ├── If any correlation > 0.80: flag "High correlation: {candidate} with {existing} (r={x.xx})"
   │   └── If candidate and existing track the same index/ETF with r > 0.95: REJECT (duplicate)
   ├── Compute sector after adding candidate
   └── If sector > 25%: either reduce other sector positions or reject candidate

2. EFFECTIVE DIVERSIFICATION CALCULATION
   Current N_effective = how many "independent bets" you're really making

   Method: Principal Component Analysis on returns covariance matrix
   N_effective = (Σ λᵢ)² / (Σ λᵢ²)  where λᵢ are eigenvalues

   If N_effective < 5 with 10+ positions: "Portfolio is undiversified.
   Adding more correlated positions increases costs without reducing risk."

3. ETF vs STOCK MIX OPTIMIZATION
   ├── Minimum 20% in broad-market ETFs (SPY, VTI, BND) for core ballast
   ├── Maximum 40% in single-stock positions (non-ETF)
   ├── Maximum 10% in leveraged/inverse ETFs total
   └── Maximum 5% in any single leveraged ETF

4. REBALANCE TRIGGERS
   ├── Calendar: quarterly rebalance (Jan, Apr, Jul, Oct 1st trading day)
   ├── Drift: any position > 20% from target weight → rebalance
   ├── Signal: new high-confidence signal conflicts with existing position → review
   └── Regime: VIX moves from <20 to >30 (calm → turbulent) → defensive rebalance

   Rebalance execution:
   ├── Calculate target weights from latest signals + sizing
   ├── Determine sells first (to free capital), then buys
   ├── Execute sells before buys (never assume sell will fill at expected price)
   └── Use limit orders at mid-price for rebalancing (not market orders)

5. TAX-AWARE REBALANCING (for taxable accounts)
   ├── Prefer selling lots with losses (tax-loss harvesting)
   ├── Prefer selling lots held >1 year (long-term cap gains)
   ├── Defer rebalancing if >80% of needed sells are short-term gains (wait for long-term)
   └── Flag: "Tax-aware: rebalancing deferred. Next review: {date}"

   Complete when: Correlation matrix checked for all candidates.
   N_effective computed. Sector limits enforced. Rebalance triggers configured.

```

### Phase 5: Full Signal-to-Execution Pipeline

```

1. END-TO-END FLOW (all phases integrated)

   External Skills                    Portfolio Signal Manager              External Skills
   ┌──────────────┐                   ┌─────────────────────┐              ┌──────────────────┐
   │tech-signals  │───signal JSON────→│                     │              │                  │
   │engineer      │                   │  PHASE 0: MCP Sync  │              │  Broker MCP      │
   └──────────────┘                   │  PHASE 1: Resolve   │────orders──→│  Server          │
                                      │  PHASE 2: Size      │              │                  │
   ┌──────────────┐                   │  PHASE 3: Monitor   │              └──────────────────┘
   │fundamental   │───signal JSON────→│  PHASE 4: Construct │              ┌──────────────────┐
   │analyst       │                   │                     │              │  algorithmic-    │
   └──────────────┘                   │  OUTPUT: Sized,     │──executed──→│  trader           │
                                      │  correlated, risk-  │              │  (execution)     │
   ┌──────────────┐                   │  managed orders     │              └──────────────────┘
   │market-data   │───corp actions───→│                     │
   │engineer      │                   └─────────────────────┘
   └──────────────┘

2. BIDIRECTIONAL COMMUNICATION PROTOCOL (this is what makes it an orchestrator)

   PUSH NOTIFICATIONS RECEIVED (from upstream skills):
   ├── technical-signals-engineer → "regimeChanged": trading → ranging → volatile
   │   Action: recalculate all position weightings, adjust stop-loss ATR multiples
   ├── fundamental-analyst → "redFlagDetected": M-Score > -1.78, earnings fraud suspected
   │   Action: IMMEDIATE close of position (skip queue). Suppress all new signals for this ticker.
   ├── market-data-engineer → "corporateAction": dividend, split, merger, spinoff
   │   Action: adjust position sizing (splits), flag tax implications (dividends),
   │           freeze trading during merger arb periods
   ├── market-data-engineer → "dataQualityDegraded": price feed stale > 5 minutes
   │   Action: HALT all new orders. Mark all signals > 5 min old as stale.
   └── algorithmic-trader → "executionAlert": fill significantly different from expected
       Action: adjust future position sizing assumptions. Flag slippage model update.

   PULL REQUESTS SENT (to upstream skills):
   ├── → technical-signals-engineer: "reScoreRequest"
   │   When: regime changed since signal generated; signal age > 20 days;
   │         portfolio manager wants signal with different parameters
   │   Payload: ticker, original_signal_id, new_parameters (optional)
   │   Expected response: updated signal JSON with current confidence
   ├── → fundamental-analyst: "valuationUpdateRequest"
   │   When: stock has moved >10% since valuation; earnings released since analysis;
   │         red flag surfaced in cross-check
   │   Payload: ticker, original_signal_id, event_triggering_update
   │   Expected response: updated valuation range + quality scores
   └── → market-data-engineer: "dataRefreshRequest"
       When: signals reference stale prices (>60 seconds old)
       Payload: tickers[], data_fields[]
       Expected response: fresh OHLCV data

   FEEDBACK LOOPS (bidirectional):
   ├── PM → FA: "Your DCF range for AAPL was $165-$230. Stock is now at $240.
   │             Re-evaluate with current data. Was the range wrong or did thesis change?"
   │   FA → PM: Updated valuation or thesis-confirmation with justification.
   │
   ├── PM → TSE: "Your SMA crossover signal fired but volume was 40% below average.
   │             Re-score with volume penalty applied."
   │   TSE → PM: Re-scored signal with volume-adjusted confidence.
   │
   └── AT → PM: "Order #1234 filled at $198.75 vs expected $198.50. Slippage: 0.13%.
   │            Recurring pattern on NASDAQ stocks in first 30 minutes."
       PM → sizing model: Update slippage assumption for NASDAQ from 0.05% to 0.15%.

3. CIRCUIT BREAKERS (last line of defense)

   │ Failure | Threshold | Action |
   │---------|-----------|--------|
   │ Rejected orders in 60 seconds | >5 | HALT. Investigate. Do not resubmit. |
   │ Consecutive stop-loss triggers | >3 in same session | HALT. Market regime check. |
   │ P&L swing (unrealized) | >$5,000 in <5 minutes | PAUSE new orders. Check news. |
   │ Broker margin call | Any | IMMEDIATE position reduction. Sell weakest 50%. |
   │ API error rate | >10% of requests | HALT. Connection integrity check. |
   │ Price gap (>3 ATR) on open position | Any | Close position at market. Gap is news-driven, not strategy-driven. |

4. COMPLETION CHECKLIST
   [VERIFIED] MCP broker connection in READY state
   [VERIFIED] All incoming signals have conflict resolution (AGREE or RESOLVED)
   [VERIFIED] No position >10% of portfolio (or 5% for leveraged ETFs)
   [VERIFIED] No sector >25% of portfolio
   [VERIFIED] N_effective computed and >3
   [VERIFIED] Stop-losses set for all positions (1.5-2× ATR from entry)
   [VERIFIED] Idempotency keys generated for all new orders
   [VERIFIED] Circuit breakers armed
   [VERIFIED] Stress tests run (6 scenarios), worst-case drawdown known

```


   Complete when: [VERIFIED] All positions sized within capital constraints.
   Complete when: [VERIFIED] Correlation matrix checked and N_effective > 3.
   Complete when: [VERIFIED] Circuit breakers armed and tested.
   Complete when: [VERIFIED] Broker connection in READY state.
   Complete when: [VERIFIED] No sector exceeds 25% exposure.
   Complete when: [VERIFIED] Stop-losses set for all open positions.
## Decision Trees

<!-- STANDARD: 3min -->

### DT1: Signal Source Credibility

```

Which signal source do I trust more for this decision?
├── Signal sources AGREE → Trust both. Full confidence. Proceed to sizing.
├── Signal sources CONFLICT (buy vs sell) → Weighted Decision Matrix (Phase 1, Step 2-4)
│   ├── Trending regime → Technicals weighted 65%
│   ├── Ranging regime → Fundamentals weighted 65%
│   ├── Earnings week → Fundamentals weighted 75% (technicals unreliable near earnings)
│   └── VIX > 30 → Equal weighting (both unreliable in chaos)
├── Only one source has signal → Use that source but:
│   ├── Cap confidence at 60% (single-source signals are weaker)
│   ├── Require minimum 55% confidence to act
│   └── Position size capped at 50% of normal
└── Neither source has signal → No action. Wait for signal.

   Always ask: "Is one source's confidence calibrated differently?"
   Technical signals average 10-15% higher raw confidence than fundamentals
   in backtests — this is a measurement artifact, not higher accuracy.

```

### DT2: Position Size Decision

```

How much capital for this signal?
├── Available capital > $1,000 → proceed to sizing method selection
│   ├── Have >50 historical trades for this ticker+strategy? → Kelly (half)
│   │   └── Win rate > 0.45? → Kelly
│   │       └── Win rate ≤ 0.45 → Volatility-adjusted 1/N (Kelly invalid with p≤0.45)
│   └── Don't have trade history → Volatility-adjusted 1/N (default)
├── Signal confidence < 55% → Skip (below action threshold)
├── Signal is BUY_WITH_CAUTION or SELL_WITH_CAUTION → 50% haircut on position size
├── Earnings within ±5 days → 50% haircut on position size
├── Sector concentration would exceed 25% → Reduce to fit or skip
├── Position would be < $1,000 → Skip (commissions/slippage erase edge)
└── Available capital exhausted → Queue signal for next available capital round

```

### DT3: When to Override a Signal

```

Should I override the automated decision?
├── External event (unscheduled news, analyst downgrade, FDA decision) → OVERRIDE
│   └── Model doesn't know about events it wasn't trained on. Human override required.
├── Liquidity crisis (bid-ask spread >5× normal, no volume on Level 2) → OVERRIDE
│   └── Sizing models assume normal liquidity. Abnormal liquidity = skip all orders.
├── Personal conviction ("I just feel this is wrong") → REJECT OVERRIDE
│   └── If you have a specific reason, add it to the model. "Feeling" is not a reason.
├── Model says BUY at 85 confidence but you remember a similar setup that failed → INVESTIGATE
│   └── Find that trade in history. Check if conditions match. If yes, add as caution flag.
└── News headline contradicts signal but you can't verify source → HOLD, VERIFY, THEN DECIDE
    └── Never override on unverified information. False news moves markets for minutes.

```

### DT4: Portfolio in Distress

```

Portfolio drawdown is at -12%. What now?
├── Drawdown < 10% → Normal. Monitor. No action needed.
├── Drawdown 10-15% → ORANGE ALERT
│   ├── Halt ALL new buy orders
│   ├── Tighten stops on all positions (reduce from 2× ATR to 1.5× ATR)
│   ├── Check: is this sector-specific or market-wide?
│   │   ├── Sector-specific → Exit weakest 50% of positions in that sector
│   │   └── Market-wide → Reduce all positions by 25%. Raise cash to 25%+ of portfolio.
│   └── Review correlation matrix: has everything gone to 1.0?
├── Drawdown 15-20% → RED ALERT
│   ├── Liquidate all positions opened in last 5 trading days (newest first)
│   ├── Reduce remaining positions by 50%
│   ├── Cancel all open orders
│   └── Mandatory 48-hour cooling-off period (no new orders)
└── Drawdown >20% → EMERGENCY
    ├── LIQUIDATE EVERYTHING. Market orders acceptable.
    ├── Post-mortem required: what broke? Model, execution, or market?
    ├── Do not resume trading until root cause identified AND fixed
    └── Minimum 5-trading-day lockout after root cause fix

```

## Cross-Skill Coordination

<!-- STANDARD: 5min — BIDIRECTIONAL: this skill is the orchestrator -->

### Upstream (Data & Signals Flow In)

| Upstream Skill | What You Receive | Communication Trigger | Your Response |
|---|---|---|---|
| `technical-signals-engineer` | Structured signal JSON: ticker, direction, confidence, confidence_breakdown, indicators, regime, parameters_used, caveats | **PUSH:** Signal generated. **PUSH:** Regime changed (trending→ranging→volatile). **PULL:** reScoreRequest sent by you when signal stale or parameter change needed | Regime change → recalculate all position weights. reScoreRequest → send when signal_age > 20 days or portfolio manager wants different RSI/BB parameters |
| `fundamental-analyst` | Structured signal JSON: ticker, direction, confidence, valuation range, quality scores, red_flags | **PUSH:** Red flag detected (M-Score triggered). **PUSH:** Valuation range updated after earnings. **PULL:** valuationUpdateRequest sent when price moves >10% from base case | Red flag → IMMEDIATE position close + trading halt for that ticker. Valuation update → recalculate margin of safety; if now negative, reduce position |
| `algorithmic-trader` | Execution confirmations: fill price, slippage, partial fills, rejections, order status | **PUSH:** Execution alert (slippage > expected, partial fill, rejected). **PUSH:** Broker connectivity status change | Slippage pattern → update sizing model assumptions. Rejection pattern → investigate root cause before resubmitting |
| `market-data-engineer` | Corporate actions, data quality alerts, price feed status, dividend dates, earnings calendars | **PUSH:** Corporate action detected (split, dividend, merger). **PUSH:** Data quality degraded (stale feed). **PUSH:** Earnings date approaching | Corporate action → adjust position sizing, flag tax events. Data degraded → halt new orders, mark signals stale. Earnings approaching → apply 50% size reduction |
| `data-scientist` | Backtest results, strategy performance metrics, signal accuracy statistics, regime classification models | **PUSH:** Strategy backtest complete with Sharpe, max_drawdown, win_rate. **PULL:** requestBacktest sent for new strategy combinations | Backtest results → calibrate confidence scores (update calibration factors). Poor performance → deprecate strategy |

### Downstream (Decisions Flow Out)

| Downstream Skill | What You Send | Communication Trigger | Expected Response |
|---|---|---|---|
| `algorithmic-trader` | Sized, correlated, risk-managed order queue: [{ticker, direction, qty, limit_price, stop_loss, take_profit, idempotency_key}] | **PUSH:** Order queue ready after Phase 2 sizing. **PUSH:** Emergency close order (circuit breaker triggered) | Order confirmation with fill details. Rejection with reason code. Timeout notification |

### Lateral (Peer Coordination — Same Layer)

| Peer Skill | Coordination Scenario | Protocol |
|---|---|---|
| `technical-signals-engineer` ← → `fundamental-analyst` (mediated by you) | Signal conflict: tech says BUY, fund says SELL | PM mediates via Weighted Decision Matrix (Phase 1). PM may request re-score from either source with adjusted parameters. PM documents resolution rationale. Neither source overrides the other directly. |
| `observability-engineer` | Portfolio monitoring dashboard, alert pipeline, P&L tracking | PM pushes metrics: portfolio_value, VaR, drawdown, N_effective, margin_used. Observability pushes: alert thresholds breached, dashboard needs refresh. |

### Escalation Path

```

Issue detected by source skill
         │
         ▼
   PUSH notification to portfolio-signal-manager
         │
         ├── Minor (confidence change, parameter update) → Log + adjust with next rebalance
         ├── Moderate (regime change, signal conflict) → Immediate recalculation, document
         ├── Major (red flag, data quality degraded) → HALT affected positions, notify human
         └── Critical (broker disconnect, margin call, circuit breaker) → EMERGENCY shutdown

```

### Communication Contract (bidirectional integrity)

Every inter-skill message must include:

```json
{
  "message_id": "uuid",
  "source_skill": "portfolio-signal-manager",
  "target_skill": "technical-signals-engineer",
  "message_type": "reScoreRequest",
  "timestamp": "ISO8601",
  "correlation_id": "references_original_signal_id",
  "payload": {},
  "expected_response_type": "signalJSON",
  "timeout_seconds": 30
}

```

Response timeout handling:
├── < 5 seconds: Normal. Process response.
├── 5-30 seconds: Flag "Slow Response — {skill} may be overloaded."
└── > 30 seconds: TIMEOUT. Proceed without that source's input. Flag in final report.

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

<!-- STANDARD: 3min -->

Before deploying portfolio-signal-manager with live capital:

- [ ] **MCP broker connection tested in paper trading for 20+ trading sessions.** Live money should never touch a broker connection that hasn't survived paper trading through at least one volatility event (VIX > 25 day).
- [ ] **Every circuit breaker tested with simulated failure.** Rejected orders, stop-loss cascade, margin call, API disconnect — each tested individually and verified to halt appropriately.
- [ ] **Idempotency key system verified.** Submit the same order twice, confirm only one fill. Test during network latency spikes. This is the single most important protection against duplicate orders.
- [ ] **Position sizing validated against backtest.** Historical simulation confirms that position sizing would NOT have exceeded 10% per position or 25% per sector over the last 5 years of data.
- [ ] **Correlation matrix N_effective stays > 3 in all backtested regimes.** If N_effective drops below 3 in any historical period, portfolio construction needs more uncorrelated assets.
- [ ] **Stress tests run and worst-case drawdown < 40%.** If any stress scenario produces >40% drawdown, reduce leverage or add hedges until it passes.
- [ ] **Signal age tracking active.** No signal older than 20 trading days drives a position without refresh.
- [ ] **Regime detection active and tested.** Verify regime changes actually trigger position re-weighting within 5 minutes of detection.
- [ ] **All communication contracts validated.** Every upstream skill's JSON output passes schema validation before ingestion.
- [ ] **Alert pipeline tested.** Drawdown alert → human receives notification within 5 minutes of threshold breach.
- [ ] **Tax-lot tracking enabled (taxable accounts).** Prevent wash sales. Track holding periods for long-term vs short-term gain optimization.
- [ ] **Daily reconciliation script scheduled.** Broker positions vs local positions compared every day. Discrepancies > $100 flagged.

## Error Recovery

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Duplicate orders on broker despite idempotency keys | Network retry sent order before idempotency key lookup completed. Broker processed both because first wasn't in their idempotency cache yet | Add client-side dedup: maintain local set of submitted idempotency keys. Reject submission if key exists in local set (even if broker hasn't confirmed first order) | **Idempotency is two-sided.** Client and broker both need dedup. Client dedup catches the race condition where first order hasn't registered yet. |
| Portfolio shows 8 positions but N_effective = 1.2 | All 8 stocks have beta > 1.0 to SPY and correlation > 0.75 to each other. You own 8 tickets for the same ride | Replace correlated positions with sector ETFs OR add true diversifiers (bonds, commodities, REITs, international). 2 truly uncorrelated assets > 20 correlated ones | **Position count is not diversification.** Effective N is the metric. A portfolio with N_effective < 3 is pretending. |
| Signal conflict resolution keeps picking the same side (always technicals win) | Regime detection is stuck. ADX calculation uses stale data or the regime hasn't changed in weeks | Verify ADX is updating. Force equal weights (0.50/0.50) for 30 days to calibrate. If fundamentals never win even in ranging markets, fundamental confidence calibration is wrong | **Systematic bias toward one signal source is a calibration failure.** If one source wins >80% of conflicts, something is broken. |
| Position sizing produces tiny positions ($800 on a $100K portfolio) | Volatility-adjusted sizing over-penalizes volatile stocks. A stock with 2x median vol gets 1/12th the position of a median-vol stock | Cap vol adjustment: max 3x penalty (position ≥ 33% of 1/N). If position still < $1,000, skip with log. Some stocks are genuinely too volatile for meaningful positions | **Sizing should produce investable positions.** A $800 position on a $100K portfolio costs more in attention than it earns. |

## Proactive Triggers

<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---|---|---|
| New ticker added to watchlist | Request signals from both technical-signals-engineer AND fundamental-analyst within 1 hour. Do not trade without both. | Single-source signals are dangerous. Two independent analyses that agree = tradeable signal. One analysis = unchecked assumption. |
| Broker account value changes by >5% in one day | Pause all new orders. Recalculate VaR, drawdown, and N_effective. If still within limits, resume. If limits breached, follow Distress Decision Tree. | 5% daily moves are outliers (3+ sigma). The model wasn't calibrated for this regime. Verify model assumptions still hold before continuing. |
| 30 days pass since last rebalance | Run full portfolio review: refresh all signals, recalculate correlations, re-optimize weights. Even if no drift triggers, monthly review is mandatory. | Markets change. Yesterday's optimal portfolio is today's stale allocation. Monthly review catches drift that 20% thresholds miss. |
| Technical-signals-engineer changes indicator formula | Request re-score of ALL active signals within 24 hours. Old signals computed with old formulas are potentially invalid. | Formula changes shift signal outputs by 5-15%. A signal at 72 confidence with old EMA formula might be 45 with new. Don't trade on stale calculations. |
| Fundamental-analyst updates DCF methodology | Request re-score of ALL active fundamental signals. DCF methodology changes (discount rate, terminal value approach) can flip BUY to SELL. | Methodology changes are rare but high-impact. A 1% WACC change shifts valuation by 15-20%. Don't discover this through drawdown. |
| Correlation matrix shows emerging cluster (3+ stocks r > 0.80 suddenly) | Reduce position sizes in that cluster by 30%. Investigate: is there a sector rotation happening? A macro event? Model doesn't know why — just that diversification is degrading. | Emerging high correlations often precede sector-wide moves. Being early to reduce exposure is cheaper than being right about why. |
| Win rate drops below 40% over trailing 20 trades | HALT new positions. Strategy review required. Something changed — market regime, signal quality, execution, or all three. | A 40% win rate with typical reward/risk of 2:1 is breakeven at best. Below 40% = losing strategy. Continuing is gambling, not trading. |

## Anti-Rationalization

<!-- DEEP: 10+min -->

| Rationalization | Reality |
|---|---|
| "The signals mostly agree, so I'll skip the full conflict resolution matrix — it's just a formality." | "Mostly agree" means some disagree. Undetected signal conflicts silently accumulate: 3 BUY signals + 2 HOLD signals from different sources treated as "5 BUYS" → 40% of your positions have weaker conviction than you think. **Cost: $15K-$80K in positions that shouldn't have been entered. The matrix takes 2 minutes. Skipping it costs months of returns.** |
| "I know the MCP broker connection works — I tested it once last month." | Broker APIs change. Auth tokens expire. Rate limits get lowered. API versions get deprecated. A connection that worked last month can fail silently today — your first sign is "why didn't my stop-loss execute?" **Cost: $5K-$250K in orders that didn't execute or executed wrong. Broker connection is not infrastructure — it's a living contract that needs daily verification.** |
| "Equal weight is close enough. I'll fine-tune the sizing later." | A $10K position in TSLA (3% daily vol) has 9x the risk contribution of $10K in PG (1% daily vol). "Equal weight" means TSLA drives 90% of your P&L. You don't have 10 positions — you have 1 position and 9 rounding errors. **Cost: $20K-$100K in "diversified" portfolios that move like a single-stock bet. Volatility adjustment is not fine-tuning — it's the difference between diversified and concentrated.** |
| "The stocks I picked are in different sectors — that's diversification enough." | GICS sector classification lags economic reality. Amazon (Consumer Discretionary) gets half its profit from AWS (Tech). Google (Communication Services) is an advertising+cloud company. Apple (Technology) is a consumer hardware+services company. Sector labels are accounting artifacts, not economic truths. **Cost: $50K-$200K in "cross-sector" portfolios that all crash together because economic drivers (tech spending, consumer discretionary income) are correlated. Diversify by economic driver, not GICS code.** |
| "I'll rebalance when the signals tell me to — no need for calendar rebalancing." | Signal drift is silent. A position that starts at 8% of portfolio drifts to 14% over 6 months without triggering any signal — it's just the stock doing well. When it eventually corrects, you've lost 14% instead of the 8% you sized for. Calendar rebalancing catches silent drift that signals miss. **Cost: $10K-$50K in overweight positions that correct to their rightful weight the hard way.** |

## Gotchas

<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Portfolio P&L swings match SPY 1:1 despite "diversified" holdings | All positions have beta ~1.0. You built a closet index fund with higher fees and more volatility | Compute beta-weighted exposure. If beta_exposure/portfolio_value > 0.85, replace 50% of single-stock positions with SPY. You'll get the same return with less concentration risk and lower transaction costs | **Portfolio beta is the first thing to check, not the last.** A beta of 1.0 means your stock-picking added zero diversification. At that point, buy the index and save the effort. |
| Signal says BUY but stock has already moved 8% since signal generation | Signal ingestion latency. The signal was generated on yesterday's close. Today the stock gapped up 8% on earnings. The signal is stale | Check signal_age before acting. If price has moved >5% since signal timestamp, request signal refresh. A signal valid at $100 may be invalid at $108 — the opportunity has already been captured | **Signal freshness is as important as signal confidence.** A 95-confidence signal on stale data is worse than a 55-confidence signal on fresh data. Timestamp everything. |
| Idempotency key "works" in test but duplicate orders appear in production | Test uses sequential requests. Production has concurrent requests from multiple signals being processed simultaneously. Race condition: two threads check local dedup set simultaneously, both see key absent, both submit | Use atomic set operations: Redis SADD or database INSERT...ON CONFLICT. Check-and-insert must be a single atomic operation. Python set in memory is not atomic across threads | **Concurrency breaks everything that works sequentially.** Idempotency must be tested under concurrent load — 10 simultaneous submissions with identical keys should produce exactly 1 order. |
| Risk dashboard shows everything green but human trader sees concerning concentration | The risk dashboard computes sector exposure by GICS sector. Human sees economic concentration: Amazon (Consumer Disc) + Google (Comm Svc) + Microsoft (Tech) all depend on enterprise cloud spending | Add economic driver classification alongside GICS: "Cloud/Enterprise," "Consumer Discretionary," "Rates-Sensitive," "Commodity-Exposed." Flag when any economic driver exceeds 30% regardless of GICS labels | **GICS is not truth.** It's an accounting classification designed for comparability, not risk management. Build your own economic driver taxonomy for real risk assessment. |
| Position sizing works for 90% of signals but produces absurd sizes for penny stocks and mega-caps | Volatility-adjusted 1/N treats all volatilities equally. A stock with 0.5% daily vol (mega-cap utility) gets 6x the position of a 3% vol stock. The utility position may be too large for liquidity | Add liquidity constraint: max_position = min(sized_amount, 5% of 20-day average dollar volume). If a position can't be exited in 1 day without moving the price >2%, it's too large regardless of what sizing says | **Liquidity is a hard constraint.** A mathematically optimal position size that can't be exited without market impact is not optimal — it's a trap. |
| MCP broker sync takes 45 seconds but signals are 30 seconds old — gap creates stale state | Sync is synchronous and blocking. By the time positions are synced, the signals used to make decisions are based on prices that have moved | Make sync streaming: positions stream via WebSocket as they change. Don't query positions → let positions push to you. If streaming unavailable, sync before signal generation, not after | **Synchronous sync in async markets creates stale state.** Push-based sync (WebSocket) is required for intraday trading. REST polling is a batch process for overnight reconciliation. |

## Verification Guardrails

<!-- STANDARD: 3min -->

| Guard | Test | Failure Response |
|---|---|---|
| G1: EXECUTE-ONLY-AFTER-RESOLVE | Before submitting any order, verify signal has a conflict_resolution block OR is AGREED by both sources | "Order {id} for {ticker} blocked: signal {signal_id} has unresolved conflict. Run Phase 1 conflict resolution before submitting." |
| G2: NO-POSITION-WITHOUT-SIZING | Before placing order, verify position_size is computed by one of the approved sizing methods (vol-adjusted-1/N, Kelly, risk-parity). No manual "looks about right" sizes | "Order blocked: position_size not computed by approved method. Run Phase 2 sizing. Manual sizing is not allowed for live trading." |
| G3: SECTOR-LIMIT-ENFORCED | Before order submission, check: sector_exposure[sector] + new_position_pct ≤ 0.25 | "Order blocked: {ticker} would increase {sector} exposure to {pct}%, exceeding 25% sector limit." |
| G4: IDEMPOTENCY-KEY-MANDATORY | Every order submission must have idempotency_key present and unique. Reject submission otherwise. | "Order blocked: missing idempotency_key. Generate UUID before submission." |
| G5: STOP-LOSS-REQUIRED | Every position must have a stop-loss price set within 60 seconds of fill confirmation. No naked positions. | "Position {ticker} missing stop-loss. Set stop-loss at 1.5-2× ATR from entry within 60 seconds or auto-close position." |
| G6: FRESH-SIGNAL-ONLY | Before order submission, verify signal_age < 20 trading days. If older, require signal refresh. | "Order blocked: signal {signal_id} is {age} trading days old. Max age is 20. Request signal refresh from source skill." |
| G7: DRAWDOWN-HALT | Check current drawdown. If >15% from peak, block ALL new buy orders. Only allow sell/close orders. | "All buy orders blocked: portfolio drawdown at {pct}%. See DT4: Portfolio in Distress for recovery procedure." |

## What Good Looks Like

<!-- STANDARD: 3min -->

A world-class portfolio signal management system:

- **Every position has a documented reason for existing.** You can trace any position back: signal ID → conflict resolution (if any) → sizing method → order ID → fill confirmation. The audit trail is complete and machine-readable.
- **You are never surprised by correlation.** The effective N metric is always known. When N_effective drops, you see it before the correlated drawdown, not after. You diversify by economic driver, not GICS label.
- **Circuit breakers fire before humans notice.** A surge of rejected orders, a stop-loss cascade, a margin call — the system halts itself and alerts, rather than continuing to dig a deeper hole.
- **Confidence scores from different sources are comparable** because they're calibrated. An 80 from technical-signals-engineer and an 80 from fundamental-analyst mean the same thing in terms of historical accuracy.
- **The broker connection survives real-world failure modes.** Token expiry, WebSocket disconnect, rate limiting, API version deprecation — each has a tested handler. The state machine has 8 states and all transitions are defined.
- **You know the worst-case scenario before it happens.** Stress tests cover 2008, 2020, 2022, and flash-crash scenarios. Worst-case drawdown is known and accepted (or mitigated) before the first dollar is deployed.
- **Conflict resolution is documented, not assumed.** When technicals say BUY and fundamentals say SELL, the weighted decision matrix produces a documented resolution with rationale. Six months later, you can audit whether the resolution was right.
- **Position sizing is mechanical, not emotional.** No "conviction sizing." No "I really like this one" double-size. Every position is sized by formula, with caps that prevent any single position from dominating the portfolio.

## References

<!-- STANDARD: 3min -->

The following reference files are loaded on demand when deeper context is needed:

### Core Methodology References

| Reference | Path | Content |
|---|---|---|
| **Position Sizing Methods** | [position-sizing-methods.md](references/position-sizing-methods.md) | Detailed formulas for Kelly criterion, volatility-adjusted 1/N, risk-parity, fixed-fractional. Includes when each method is valid and common mistakes. |
| **Signal Conflict Resolution** | [signal-conflict-resolution.md](references/signal-conflict-resolution.md) | Weighted decision matrix derivation, calibration methodology, backtest validation of conflict resolution outcomes. Includes 50 real conflict cases with outcomes. |
| **MCP Broker Integration** | [mcp-broker-integration.md](references/mcp-broker-integration.md) | Full state machine specification (8 states), idempotency protocol, error handling per broker (Alpaca, IBKR, Schwab, Robinhood), WebSocket reconnect strategy. |
| **Portfolio Risk Metrics** | [portfolio-risk-metrics.md](references/portfolio-risk-metrics.md) | VaR computation methods (historical, parametric, Monte Carlo), CVaR, effective N derivation, stress testing scenarios with historical calibration. |
| **Correlation & Diversification** | [correlation-diversification.md](references/correlation-diversification.md) | PCA-based effective N, regime-dependent correlation matrices, economic driver taxonomy (vs GICS), minimum variance vs maximum diversification optimization. |
| **Circuit Breakers & Fail-Safes** | [circuit-breakers.md](references/circuit-breakers.md) | Complete circuit breaker catalog with thresholds, testing procedures, and recovery protocols. Includes production incident case studies. |
| **Tax-Aware Portfolio Management** | [tax-aware-management.md](references/tax-aware-management.md) | Wash sale rules, tax-loss harvesting algorithm, lot selection optimization, short-term vs long-term gain management. |
| **Backtesting & Validation** | [backtesting-validation.md](references/backtesting-validation.md) | How to backtest a multi-signal portfolio, out-of-sample validation, walk-forward optimization, overfitting detection, minimum backtest length requirements. |

### Related Skills

| Skill | Relationship | When to Invoke |
|---|---|---|
| `technical-signals-engineer` | Upstream — generates technical signals this skill ingests | Any time you need a technical signal for a ticker |
| `fundamental-analyst` | Upstream — generates fundamental signals this skill ingests | Any time you need a fundamental valuation or quality score |
| `algorithmic-trader` | Downstream — executes the orders this skill produces | When sized orders are ready for execution |
| `market-data-engineer` | Upstream — provides data quality alerts, corporate actions | When data pipeline health is questionable |
| `data-scientist` | Peer — provides backtesting and strategy validation | When evaluating strategy performance or calibrating models |
| `observability-engineer` | Peer — provides monitoring dashboards and alerts | When portfolio monitoring infrastructure needs setup |
| `financial-security` | Reference — security review of MCP broker integration | Before deploying with real money |
| `quantitative-analyst` | Reference — advanced risk models (GARCH, copula) | When standard VaR/correlation methods are insufficient |
| `devops-engineer` | Reference — deployment pipeline for automated trading | When setting up production trading infrastructure |
| `incident-responder` | Reference — incident response for trading failures | When circuit breakers fire or trading anomalies detected |

## Deliberate Practice

<!-- STANDARD: 3min -->

1. Construct a 10-position portfolio from scratch using only buy signals — then reconstruct with risk-parity sizing and compare drawdowns
2. Correlation audit: Take a real portfolio and compute N_effective monthly for 12 months. Identify when diversification silently degraded
3. Conflict simulation: Generate 50 signal pairs where technical and fundamental disagree. Run the weighted decision matrix. Compare outcomes
4. Circuit-breaker fire drill: Simulate a 20% drawdown. Does every breaker fire? Does the portfolio stop losing money?
5. Broker outage simulation: Disconnect the MCP broker mid-order. Can the portfolio recover without orphaned positions?
