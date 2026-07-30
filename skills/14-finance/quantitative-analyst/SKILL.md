---
name: quantitative-analyst
description: >
  Use when pricing options, computing Greeks, constructing implied volatility surfaces, detecting
  unusual options activity, or generating trade signals from options flow anomalies. Handles
  pricing models (Black-Scholes, Binomial, Monte Carlo), Greeks computation (Delta, Gamma, Theta,
  Vega, Rho), implied volatility surface construction, UOA detection, volatility smile/skew
  analysis, and put-call parity validation. Do NOT use for trade execution, market data pipeline
  engineering, or portfolio management.
license: MIT
tags:
  - quantitative-analyst
  - options
  - greeks
  - uoa
  - volatility
  - black-scholes
  - monte-carlo
  - pricing-models
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
    - market-data-engineer
    - data-scientist
    - ml-engineer
    - trade-performance-analyst
  feeds_into:
    - algorithmic-trader
    - data-scientist
    - ml-engineer
    - futures-trader
    - forex-trader
    - fixed-income-analyst
  alternatives:
    - ml-engineer
---
# Quantitative Analyst
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Options market intelligence through quantitative rigor. Build pricing models, compute and interpret Greeks,
detect unusual options activity (UOA), construct implied volatility surfaces, validate put-call parity, analyze
volatility smile/skew, and generate actionable trade signals from options flow anomalies. This skill translates
raw options market data into structured, confidence-calibrated trade signals ready for algorithmic consumption.
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


### Quantitative Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Calibrate the pricing model.** Verify: risk-free rate (current Treasury yield for matching tenor), dividend yield (trailing + forward consensus), and implied borrow cost (hard-to-borrow fee schedule). Mispricing by 50bp on any input compounds across the position. | [GARBAGE_IN] The most elegant pricing model with wrong inputs produces garbage. A Black-Scholes price using the wrong risk-free rate is mathematically correct and financially wrong. | Treasury yield curve, dividend calendars, broker borrow fee schedules |
| **RP-F2** | **Construct the full volatility surface.** Plot IV by strike and expiration. Check for: skew (OTM puts vs. OTM calls), term structure (contango vs. backwardation), and smile/smirk asymmetry. | [FLAT_VOL_FALLACY] Treating volatility as a single number ignores the surface. The ATM IV might be 25% while the 25-delta put IV is 32% — that 7-point skew is where edge lives or dies. | Options chains across all strikes and expirations, vol surface visualization |
| **RP-F3** | **Compute position sizing via Kelly Criterion.** f* = (bp − q) / b. Cap at 25% Kelly for real execution. Regime-adjust: 25% Kelly in bull, 15% in correction, 10% in bear, 5% in crash. | [OVERBETTING] Full Kelly is optimal for log-utility in theory and ruinous in practice. Parameter uncertainty, non-normal returns, and gap risk make full Kelly a path to eventual blow-up. 25% Kelly is the practical maximum. | Kelly calculator, strategy win rate and win/loss ratio data |
| **RP-F4** | **Validate that the Greeks tell a coherent story.** Delta ≈ directional exposure. Gamma ≈ acceleration (how fast delta changes). Theta ≈ daily cost of holding. Vega ≈ IV sensitivity. A position with positive gamma, negative theta, and high vega is a long vol position — confirm this aligns with the strategy thesis. | [GREEKS_CONTRADICTION] A strategy that claims to be "directionally neutral" but has net delta of +0.30 on a $100K notional has $30K of directional exposure. The Greeks don't lie — they reveal what the strategy ACTUALLY does vs. what it CLAIMS to do. | Greeks calculator, position summary, strategy thesis document |
| **RP-F5** | **Check for early exercise and assignment risk.** American-style options can be exercised at any time. Check: dividends (calls exercised pre-ex-div), hard-to-borrow (puts exercised to capture borrow rebate), deep ITM (assignment probability rises with moneyness). | [EARLY_EXERCISE] Early assignment transforms a defined-risk spread into an undefined-risk short stock position overnight. A short call assigned on ex-div eve = you owe the dividend. | Dividend calendar, short interest data, ITM depth analysis |



## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "BlackScholes\|black_scholes\|bsm_price\|implied_volatility")` OR `file_contains("*.py", "scipy.stats.norm\|monte_carlo.*option\|heston\|binomial")` OR `file_contains("*.R", "BlackScholes\|Garch\|rugarch")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py", "kafka\|KafkaProducer\|polygon\|alpaca.*trade\|websocket")` OR `file_contains("*.sql", "CREATE TABLE.*ticks\|CREATE TABLE.*options_flow")` | Invoke **market-data-engineer** instead. This is data pipeline work. |
| A3 | `file_contains("*.py", "backtrader\|zipline\|vectorbt\|alpaca.*trade\|order.*submit")` OR `file_contains("*.py", "Strategy.*next\|stop_loss\|take_profit\|bracket")` | Invoke **algorithmic-trader** instead. This is execution and order placement. |
| A4 | `file_contains("*.py", "sklearn\|tensorflow\|torch\|xgboost\|RandomForest\|GradientBoosting")` AND `file_contains("*.py", "predict\|classify\|signal")` | Invoke **ml-engineer** instead. This is ML-based signal prediction. |
| A5 | `file_contains("*.py", "pandas\|numpy\|statsmodels\|scipy")` AND `file_contains("*.py", "regression\|hypothesis.test\|p.value\|ttest")` | Jump to **Decision Trees** — Statistical Validation. |
| A6 | `file_contains("*.py\|*.R", "ggplot\|matplotlib\|plotly\|seaborn")` AND `file_contains("*.py", "volatility.surface\|vol.smile\|skew\|term.structure")` | Jump to **Decision Trees** — IV Surface Construction. |
| A7 | `file_contains("*.py", "put.call.parity\|arbitrage\|no.arbitrage\|risk.neutral")` | Jump to **Decision Trees** — Arbitrage Detection. |
| A8 | `file_contains("*.py", "greeks\|delta\|gamma\|theta\|vega\|rho")` AND `file_contains("*.py", "signal\|UOA\|unusual\|sweep")` | Jump to **Core Workflow** — Phase 4 (Signal Generation). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Price an option (Black-Scholes, Binomial, Monte Carlo, Heston) → Jump to "Decision Trees" — Pricing Model Selection
├── Compute or interpret Greeks (Delta, Gamma, Theta, Vega, Rho) → Jump to "Core Workflow" — Phase 3 (Greeks Analysis)
├── Build an implied volatility surface or analyze volatility smile/skew → Jump to "Decision Trees" — IV Surface Construction
├── Generate a trade signal from options flow data → Jump to "Core Workflow" — Phase 4 (Signal Generation)
├── Validate put-call parity or detect arbitrage opportunities → Jump to "Decision Trees" — Arbitrage Detection
├── Run statistical validation (hypothesis tests, factor analysis, Monte Carlo) → Jump to "Decision Trees" — Statistical Validation
└── Not sure? → Start at "Ground Rules" — read before anything else

```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to report a trade signal without a confidence interval and supporting evidence.** Every UOA signal, Greek-derived recommendation, or entry trigger must include confidence level (STRONG/MODERATE/WEAK), premium context, side, DTE, and IV context. "Buy calls on XYZ" without evidence is reckless. | Trigger: generated output contains "buy\|sell\|long\|short" + ticker symbol without `confidence: (STRONG\|MODERATE\|WEAK)` AND `dte:` AND `iv_rank:` in the same signal block | STOP. Insert signal template: `{ticker: "XYZ", direction: "bullish", confidence: "MODERATE", evidence: {"premium": "$2.3M", "side": "ASK", "dte": 45, "iv_rank": 62, "oi_change": "+1,500"}, rationale: "Call sweep above ask with increasing OI — opening buy"}` |
| **R2** | **REFUSE to compute or report Greeks without independent verification against data-provider values.** Provider-computed Delta can differ by 0.05-0.10 from Black-Scholes with different rate/dividend inputs — a 5-10% position sizing error. | Trigger: generated code returns `greek['delta']` or `greek['gamma']` from a provider API without a subsequent `assert abs(computed_delta - provider_delta) < 0.05` check | STOP. Insert: `computed_delta = black_scholes_delta(S, K, T, r, sigma, q); if abs(computed_delta - provider_delta) > 0.05: logger.warning(f'Delta discrepancy: computed={computed_delta:.4f}, provider={provider_delta:.4f}. Investigate rate/div assumptions.'); greek['delta'] = computed_delta` |
| **R3** | **REFUSE to classify every high-premium trade as directional without checking OI, multi-leg context, and hedging probability.** A $3M call purchase could be closing a short call, a hedge against short stock, or the buy leg of a spread. Without OI comparison, 30%+ of signals are misclassified. | Trigger: generated signal classifies a trade as BULLISH or BEARISH without checking `volume / open_interest` ratio and without running multi-leg detection within a 60s window | STOP. Insert: `oi_ratio = trade.volume / trade.open_interest; if oi_ratio < 0.5: signal.classification = 'POTENTIAL_CLOSING'; signal.confidence = downgrade(signal.confidence); logger.info(f'Trade {trade.id}: OI ratio {oi_ratio:.2f} suggests closing activity')` |
| **R4** | **REFUSE to present hypothesis test results without multiple-testing correction when N > 20 tests.** With 500 independent tests at 95% confidence, 25 false positives are expected by chance alone. Without Bonferroni or Benjamini-Hochberg, you are trading noise. | Trigger: generated output reports p < 0.05 as "significant" or "edge discovered" AND `grep -c "p.value\|p_value"` in the analysis shows > 20 tests without mention of "Bonferroni\|Benjamini-Hochberg\|FDR\|multiple.testing" | STOP. Apply: `from statsmodels.stats.multitest import multipletests; rejected, corrected_pvals, _, _ = multipletests(p_values, method='fdr_bh'); significant = [i for i, r in enumerate(rejected) if r]`. Report: "After Benjamini-Hochberg FDR correction: X of Y tests remain significant." |
| **R5** | **STOP and ASK when signal context is missing.** Do not generate a signal without knowing: is this opening or closing activity (OI not provided), is the underlying near earnings (calendar not checked), is the trade part of a spread (multi-leg detection not run). | Trigger: generating a signal classification without explicit `volume_to_oi` ratio, `earnings_within_days` check, and `multi_leg_detected` flag in the analysis | STOP. Ask: "Has OI been compared to volume? Are there earnings within the position's DTE window? Has multi-leg detection been run within a 60-second window? I need these before classifying direction." |
| **R6** | **DETECT and WARN about survivorship-biased datasets.** Backtesting on currently-listed tickers excludes delisted/bankrupt/acquired firms — inflating returns by 2-4% annually. | Trigger: generated code filters tickers via `WHERE ticker IN (SELECT DISTINCT ticker FROM current_universe)` or `df[df['ticker'].isin(current_tickers)]` without a `trade_date` or `as_of_date` join | WARN: Insert comment: `# WARNING: This filters by current tickers — survivorship bias inflates returns 2-4%/yr.` Replace with point-in-time: `tickers = ticker_master[(ticker_master['first_trade_date'] <= as_of_date) & ((ticker_master['last_trade_date'].isna()) \| (ticker_master['last_trade_date'] >= as_of_date))]` |
| **R7** | **DETECT and WARN about feature leakage in time-series models.** Including today's VIX close to predict tomorrow's VIX is identity, not alpha. Any R² > 0.7 on financial time series is a bug until proven otherwise. | Trigger: generated model training code joins features on `df['date']` or `pd.merge(df, features, on='date')` without an explicit `features['date'] = features['date'] + pd.Timedelta(days=1)` lag shift OR reports R² > 0.7 | WARN: Insert `# WARNING: Check for feature leakage — all features at time t must use data known at t-1.` Add: `features = features.shift(1)  # Lag features by 1 period`. Add: `assert model.r2_score < 0.7, f'R² {model.r2_score:.3f} suspiciously high — check for future leakage'` |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Masters of quantitative analyst don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

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

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 quantitative analyst, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->
- You are screening for unusual options activity on mid-cap companies with $1M+ premium thresholds
- You need to compute and interpret Greeks (Delta, Gamma, Theta, Vega, Rho) for individual options or portfolios
- You are pricing options using Black-Scholes, Binomial trees, or Monte Carlo simulation
- You need to filter UOA by condition codes (sweep, split, block, floor) and classify trade intent
- You are constructing an implied volatility surface and analyzing smile/skew/term structure
- You need to generate structured trade signals (STRONG BUY, BUY, WEAK BUY, NEUTRAL, SELL) from options flow
- You are validating put-call parity or detecting arbitrage opportunities in options chains
- You need to assess IV rank/percentile to determine whether options are cheap or expensive
- You are filtering out noise — bad prints, dividend-affected chains, 0DTE gambler flow, pre-earnings hedging
- You need to distinguish multi-leg strategies (spreads, straddles, strangles, butterflies) from single-leg trades

## Decision Trees

<!-- STANDARD: 3min -->
Full detail → references/quantitative-analyst-computations.md

### DT1: Model Selection → Full detail in references
```
Data stationary? → YES → ARIMA, linear models, simple ML. NO → Differencing, GARCH for volatility.
  ↓
Non-linear relationships? → YES → Random Forest, XGBoost, LSTM. NO → OLS, Ridge regression.
  ↓
Time series structure? → YES → Walk-forward CV. ARIMA/GARCH. NO → K-fold CV. Standard ML.
```

### DT2: Overfitting Detection → Full detail in references
```
Train R² - Test R² >15%? → YES → OVERFITTING. Regularize, reduce features, simplify model.
  ↓ NO
Sharpe >3.0? → YES → SUSPICIOUS. Check for look-ahead bias, survivorship bias, data leakage.
  ↓ NO → Model passes ✓
```
## Gotchas

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

- [ ] Stationarity: all time series tested for stationarity (ADF test) — non-stationary series differenced or cointegrated
- [ ] Sharpe ratio: annualized correctly based on actual return frequency, not √252 assumption
- [ ] Multiple testing: p-values adjusted when testing > 1 hypothesis — adjustment method documented
- [ ] Monte Carlo: key risk metrics (max drawdown, VaR, CVaR) reported as distributions, not point estimates
- [ ] Reproducibility: full pipeline runs from raw data to final metrics with a single command

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Volatility Term Structure & VIX Futures**: See [volatility-term-structure.md](references/volatility-term-structure.md) — VIX futures curve, contango/backwardation, VRP, roll yield, calendar spread edge, strategy selection framework, early warning system

