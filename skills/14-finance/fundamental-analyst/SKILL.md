---
name: fundamental-analyst
description: >
  Use when performing equity valuation (DCF, comparable company analysis, Graham number),
  analyzing financial statements (income statement, balance sheet, cash flow), computing
  fundamental ratios (PE, PEG, PB, EV/EBITDA, ROE, ROIC, FCF yield), screening for
  undervalued stocks, assessing dividend quality and sustainability, evaluating ETF
  fundamentals (expense ratio, tracking error, AUM, holdings overlap), or generating
  fundamental buy/sell signals. Handles DCF modeling with sensitivity analysis, Piotroski
  F-Score (0-9 scale), Altman Z-Score bankruptcy risk, Beneish M-Score earnings manipulation
  detection, fair value estimation with margin of safety, quality scoring (profitability +
  growth + financial health + management), dividend analysis (payout ratio, growth rate,
  coverage), and ETF fundamental screening. Do NOT use for technical analysis (route to
  technical-signals-engineer), order execution (route to algorithmic-trader), or market data
  ingestion (route to market-data-engineer).
license: MIT
tags:
  - fundamental-analyst
  - equity-valuation
  - dcf
  - financial-ratios
  - piotroski-score
  - altman-z-score
  - dividend-analysis
  - etf-fundamentals
  - value-investing
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 4000
chain:
  consumes_from:
    - market-data-engineer
    - data-scientist
  feeds_into:
    - portfolio-signal-manager
    - algorithmic-trader
    - technical-signals-engineer
  alternatives:
    - data-scientist
    - business-strategist
---

# Fundamental Analyst
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Analyze companies through their financial statements — income, balance sheet, cash flow — to determine intrinsic value and generate fundamental buy/sell signals. This skill computes valuation ratios, builds DCF models, detects accounting manipulation, scores quality, and screens ETFs on fundamental merit. Every valuation is expressed as a range (bear/base/bull case), not a single number. Every signal is confidence-calibrated against historical accuracy of the methodology.
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


### Fundamental Analysis Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Verify financial statement quality.** Check: revenue recognition policy (aggressive vs. conservative), one-time items as % of earnings (>10% = red flag), accounts receivable growth vs. revenue growth (AR growing faster = channel stuffing risk). | [ACCOUNTING_FICTION] GAAP earnings can be legally manipulated through revenue recognition, capitalization of expenses, and reserve manipulation. Reported earnings and economic earnings can diverge by 20%+. | 10-K, 10-Q, earnings call transcripts, auditor opinion letters |
| **RP-F2** | **Compute normalized (cycle-adjusted) earnings.** Use 5-10 year average margins to smooth cyclicality. A cyclical at peak earnings trading at 8× P/E is expensive, not cheap — normalized P/E may be 18×. | [CYCLICAL_TRAP] Buying cyclicals at peak earnings on low P/E is the classic value trap. Normalized earnings reveal the true valuation. | Historical margin data, sector cycle analysis, normalized P/E calculations |
| **RP-F3** | **Assess competitive moat durability.** Porter's Five Forces on the specific business: barriers to entry, supplier power, buyer power, substitution threat, competitive intensity. A wide moat deteriorating is more dangerous than no moat at all — it means the market is overpaying for a fading advantage. | [MOAT_MIRAGE] "Wide moat" is not a permanent certification. Moats erode: technological disruption, regulatory change, new entrants, changing consumer behavior. A moat assessment from 2020 may be obsolete in 2025. | Industry reports, competitor analysis, technology disruption timelines |
| **RP-F4** | **Reverse-engineer the DCF assumptions.** What growth rate and terminal value are priced in at current market price? If the implied growth rate exceeds GDP growth + inflation by 3%+, the market is pricing in dominance that may not materialize. | [DCF_ASSUMPTION_BLINDNESS] A DCF is only as good as its assumptions. The market price IS a DCF — reverse it to see what assumptions are embedded. If those assumptions are unreasonable, the price is unreasonable. | Reverse DCF model, GDP growth forecasts, inflation expectations |
| **RP-F5** | **Cross-check against the three most dangerous words in investing: "this time is different."** For every bullish thesis, find the historical analog where the same thesis was applied and failed. If no analog exists, the thesis is either genuinely novel (rare) or the historical search was insufficient (common). | [HISTORICAL_AMNESIA] Every bubble has been accompanied by a "this time is different" narrative. The four most expensive words in finance. Historical analogs are the cheapest reality check available. | Financial history databases, bubble case studies, "This Time Is Different" (Reinhart & Rogoff) |



## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "PE\|eps\|revenue\|EBITDA\|free_cash_flow\|DCF\|discounted_cash")` OR `file_contains("*.py", "balance_sheet\|income_statement\|10-K\|10-Q\|annual_report")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.py", "SMA\|EMA\|RSI\|MACD\|bollinger\|crossover")` AND NOT `file_contains("*.py", "PE\|DCF\|balance_sheet")` | Invoke **technical-signals-engineer** instead. Technical analysis domain. |
| A3 | `file_contains("*.py", "options\|greeks\|implied_volatility\|BlackScholes")` | Invoke **quantitative-analyst** instead. Options domain. |
| A4 | `file_contains("*.py", "alpaca\|broker\|order\|execution\|backtest")` | Invoke **algorithmic-trader** instead. Execution domain. |
| A5 | `file_contains("*.py", "Polygon\|kafka\|tick\|stream\|ingest")` | Invoke **market-data-engineer** instead. Data pipeline domain. |

### Intent Route

```

What fundamental analysis task?
├── Valuing a company (DCF, comparables) → Phase 1
├── Analyzing financial statements → Phase 2
├── Computing quality scores (Piotroski, Altman) → Phase 3
├── Generating fundamental buy/sell signals → Phase 4
├── Screening multiple stocks → Phase 5
└── ETF fundamental analysis → Decision Trees: ETF Fundamentals

```

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to produce a single-point fair value. Every valuation must be a range: bear case, base case, bull case, with explicit assumptions for each. Single-point estimates create false precision and anchoring bias. | Trigger: output contains "fair value is $X" without at least two alternative scenarios with different assumptions | STOP. "Single-point valuation rejected. Produce bear/base/bull range with explicit assumptions for each scenario. See Phase 1 — DCF Range Construction." |
| R2 | REFUSE to value a company without reading at least 3 years of financial statements. Valuations based on a single year or trailing-twelve-months alone miss cyclical effects, one-time items, and trend direction. | Trigger: DCF or valuation output references < 3 fiscal years of data | STOP. "Insufficient history. Valuation requires ≥3 years of income statement, balance sheet, and cash flow data. Request 10-K/10-Q filings for at least 3 fiscal years." |
| R3 | REFUSE to compute PE ratio without checking for one-time items. Non-recurring gains/losses (asset sales, litigation settlements, restructuring charges) distort earnings and produce misleading PE ratios. Use adjusted/operating earnings. | Trigger: PE computed as `price / gaap_eps` without `adjusted_eps` or `operating_eps` alternative | STOP. "GAAP PE potentially distorted by one-time items. Also compute adjusted PE using operating earnings. If adjusted and GAAP PE differ by >15%, flag for investigation." |
| R4 | REFUSE to screen ETFs by past performance alone. Past returns are negatively correlated with future returns at the 3-5 year horizon. Screen ETFs on expense ratio, tracking error, AUM, and holdings quality — NOT trailing returns. | Trigger: ETF screen sorts by trailing_return without also sorting by expense_ratio or tracking_error | STOP. "Past-performance ETF screening is return-chasing. Primary screen criteria must be: (1) expense ratio, (2) tracking error, (3) AUM > $100M, (4) holdings quality. Add trailing returns only as a secondary tiebreaker." |
| R5 | REFUSE to rely on a single quality metric. Piotroski F-Score alone misses leverage risk. Altman Z-Score alone misses earnings quality. Beneish M-Score alone produces false positives on legitimate business model changes. Use all three. | Trigger: only one quality score (F-Score, Z-Score, or M-Score) output without the other two | STOP. "Single quality score insufficient. Run all three: Piotroski F-Score (profitability + efficiency + leverage), Altman Z-Score (bankruptcy risk), Beneish M-Score (earnings manipulation). Triangulate." |
| R6 | REFUSE to generate buy signals on stocks with negative free cash flow for 2+ consecutive years — unless explicitly analyzing a pre-revenue growth company with a documented thesis. FCF-negative companies dilute shareholders, take on debt, or both. | Trigger: buy signal generated for ticker with `fcf < 0` for past 2 fiscal years AND no `pre_revenue_growth_thesis=True` flag | STOP. "Company has burned cash for 2+ years. If this is a pre-revenue growth thesis, document it explicitly with TAM and runway analysis. Otherwise, FCF-negative = no buy." |
| R7 | NEVER rely on non-GAAP metrics without reconciling to GAAP. Companies increasingly use "adjusted EBITDA" that excludes stock-based compensation, restructuring, and "other" — inflating profits by 20-50%. | Trigger: uses `adjusted_ebitda` or `non_gaap_eps` without a reconciliation table mapping to GAAP equivalents | STOP. "Non-GAAP metric used without GAAP reconciliation. Produce a bridge: GAAP EPS → adjustments → Non-GAAP EPS. Flag adjustments exceeding 15% of GAAP as aggressive accounting." |

## Anti-Hallucination
**Admit uncertainty** when synthesizing across domains. **Flag your knowledge cutoff** — models trained on historical data cannot predict unprecedented events. **Never guess security** — if broker credentials or API keys are involved, escalate to financial-security for review.


<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "The DCF says fair value is $187.34 — that's the right price." | Your terminal growth rate of 3.5% vs 3.0% changes fair value by $22. Your WACC of 9% vs 10% changes it by $35. DCF is exquisitely sensitive to assumptions you guessed. The correct answer is "$140-$220, depending on terminal growth and WACC." **Cost of single-point thinking: $50K-$500K when your "precise" number is 30% wrong. Always present a range.** |
| "The company has a PE of 12 — it's cheap compared to the sector at 18." | The sector PE includes 3 companies with PE > 50 that drag the average up. The median PE is 14. Your stock at 12 is 14% below median, not 33% below average. Also, the company took a $2B restructuring charge last year that depressed earnings — normalized PE is actually 16. **Cost: $20K-$100K in "value trap" positions. Always use median, not mean. Always check for one-time items.** |
| "EPS grew 35% last year — this is a growth company." | Revenue grew 4%. The 35% EPS growth came entirely from $500M in share buybacks (shrinking denominator) and a one-time tax benefit. Organic EPS growth (constant share count, no one-timers) was 6%. Buybacks mask stagnation. **Cost: $30K-$150K in growth-at-a-reasonable-price (GARP) traps. Decompose EPS growth into revenue growth + margin expansion + buyback effect + one-time items.** |
| "Net income is $2.1B and FCF is $2.3B — the business is healthy." | FCF exceeds net income because capex is 40% below depreciation — the company is under-investing in its asset base. Maintenance capex should roughly equal D&A. The $800M gap between D&A and actual capex is deferred maintenance that will become a $2-3B catch-up expenditure within 3 years. **Cost: $100K-$1M in "cash flow value traps" — companies that look cheap on FCF because they're consuming their asset base. Always compare capex to D&A.** |
| "The Piotroski F-Score is 8 — this is a high-quality company." | Piotroski F-Score uses ROA, not ROE, so it misses leverage magnification. A company with F-Score 8 and debt/equity of 3.5x (hidden by high ROA from asset-light model) is one recession away from a liquidity crisis. F-Score was designed for deep value stocks with high BM ratios — not for growth companies. **Cost: $40K-$200K in "high quality" companies that collapse under leverage. Triangulate F-Score with Altman Z-Score and debt/equity.** |
| "The ETF has a 0.03% expense ratio and tracks the S&P 500 perfectly." | The ETF uses sampling (holds 480 of 500 stocks) and had a tracking error of 0.15% last year in volatile markets. The 0.03% expense ratio is real but the 0.15% tracking error is 5x larger and invisible in the prospectus. In a 20% up year, you lost 0.18% to costs, not 0.03%. **Cost: $5K-$50K in hidden tracking error drag compounded over years. Always verify tracking error against the stated benchmark, not just the expense ratio.** |


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
| ❌ **DCF with perpetual growth > GDP growth** | Terminal growth of 5% implies the company eventually outgrows the economy. This is the single biggest DCF error | ✅ Cap terminal growth at risk-free rate. If the valuation requires >3% terminal growth, the stock is expensive |
| ❌ **Quality score without sector normalization** | A bank with 85% gross margin would be incredible. A software company with 85% gross margin is average. Raw scores lie | ✅ Normalize every quality metric against sector peers. Quality is relative, not absolute |
| ❌ **Single DCF with point-estimate WACC** | Tweaking WACC from 8% to 9% can swing fair value 30%. A point estimate pretends precision doesn't exist | ✅ Run DCF with a range of WACC ±1.5%. Report fair value as a range, not a point. Flag your knowledge cutoff |
| ❌ **Comparing P/E across different capital structures** | Company A (D/E = 0.1) and Company B (D/E = 2.0) should not have directly compared P/E ratios. Leverage distorts earnings | ✅ Use EV/EBITDA or unlevered P/E for cross-company comparisons. Always check capital structure first |
| ❌ **Ignoring off-balance-sheet items** | Operating leases, purchase obligations, and SPV debt don't show in D/E ratio but are real liabilities | ✅ Capitalize operating leases (ASC 842). Check footnotes for commitments. Never guess security — verify every obligation |

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

### Phase 1: Valuation — Determine Intrinsic Value Range

```

1. GATHER FINANCIAL DATA (3+ years)
   ├── Income Statement: Revenue, Gross Profit, Operating Income, Net Income, EPS (GAAP + Adjusted)
   ├── Balance Sheet: Total Assets, Total Liabilities, Debt (short + long), Equity, Working Capital
   ├── Cash Flow: Operating CF, Capex, FCF (= OCF - Capex), Share Buybacks, Dividends
   └── Footnotes: One-time items, segment breakdowns, related-party transactions, off-balance-sheet obligations

   Complete when: 3+ fiscal years of all 3 statements collected. One-time items identified and isolated.

2. BUILD DCF MODEL (3 scenarios)
   ├── Revenue Projection (5 years): based on historical CAGR, industry growth, market share
   ├── FCF Projection: Revenue × FCF margin (historical avg ± sensitivity)
   ├── Terminal Value: Gordon Growth Model (FCF_year5 × (1+g) / (WACC - g))
   │   └── g = risk-free rate (10Y Treasury) to risk-free + 2% (no higher)
   ├── WACC: CAPM → Rf + β × ERP + size premium + company-specific risk
   │   └── ERP default 5.0%, β from 5Y monthly regression against SPY
   └── DISCOUNT: FCF_t / (1+WACC)^t + TV / (1+WACC)^5

   SCENARIOS:
   ├── BEAR: Revenue growth -30% below base, FCF margin -200bps, WACC +100bps
   ├── BASE: Revenue growth = conservative estimate, FCF margin = 3Y avg, WACC = computed
   └── BULL: Revenue growth +30% above base, FCF margin +200bps, WACC -100bps

   Complete when: DCF range produced (bear/base/bull). All assumptions documented.

3. COMPARABLE COMPANY ANALYSIS
   ├── Select 5-8 comparable companies (industry, size, growth rate, margins)
   ├── Compute multiples: EV/EBITDA, PE (adjusted), PB, EV/Revenue, PEG, FCF Yield
   ├── Apply MEDIAN multiples (NOT mean — outliers skew mean)
   └── Range: 25th percentile to 75th percentile of implied values

4. GRAHAM NUMBER (value floor — for mature, profitable companies only)
   Graham Number = √(22.5 × EPS × BVPS)
   Valid only when: PE < 15, PB < 1.5. Do NOT use for growth companies or negative-earnings companies.

   Complete when: Valuation range triangulated from DCF + comparables + Graham floor.

```

### Phase 2: Financial Statement Analysis

```

1. PROFITABILITY ANALYSIS
   ├── Gross Margin trend (3-5 years): expanding = pricing power, contracting = competition
   ├── Operating Margin trend: expanding = operating leverage, contracting = cost pressure
   ├── Net Margin: check for one-time items distorting bottom line
   ├── ROE (DuPont): Net Margin × Asset Turnover × Equity Multiplier
   │   └── ROE rising from leverage alone (equity multiplier ↑) = WARNING
   ├── ROIC = NOPAT / Invested Capital: must exceed WACC for value creation
   └── FCF Yield = FCF / Market Cap: > 5% = cheap, > 8% = very cheap, > 10% = investigate why

2. FINANCIAL HEALTH ANALYSIS
   ├── Current Ratio: current assets / current liabilities > 1.5
   ├── Debt/Equity < 2.0 (ex-financials); Debt/EBITDA < 3.0
   ├── Interest Coverage: EBIT / Interest Expense > 3.0
   ├── FCF / Debt: ability to pay down debt from operations
   └── Altman Z-Score: > 3.0 safe, 1.8-3.0 gray, < 1.8 distress

3. EARNINGS QUALITY ANALYSIS
   ├── Accruals Ratio: (Net Income - FCF) / Total Assets — persistent negative = red flag
   ├── Revenue vs Receivables: receivables growing faster than revenue = channel stuffing
   ├── Depreciation / Capex ratio: < 1.0 = under-investing (consuming assets)
   └── Beneish M-Score: > -2.22 = potential manipulation

   Complete when: All ratios computed. Red flags documented with specific numbers.

```

### Phase 3: Quality Scoring

```

1. PIOTROSKI F-SCORE (0-9) — for value stocks (high B/M ratio)
   PROFITABILITY (0-4):
   ├── +1: Positive Net Income
   ├── +1: Positive Operating Cash Flow
   ├── +1: ROA increased vs prior year
   └── +1: OCF > Net Income (earnings quality)

   LEVERAGE/LIQUIDITY (0-3):
   ├── +1: Long-term Debt/Assets decreased vs prior year
   ├── +1: Current Ratio increased vs prior year
   └── +1: No new share issuance (dilution)

   OPERATING EFFICIENCY (0-2):
   ├── +1: Gross Margin increased vs prior year
   └── +1: Asset Turnover increased vs prior year

   SCORE: 0-3 = weak, 4-6 = average, 7-9 = high quality

2. ALTMAN Z-SCORE (bankruptcy risk within 2 years)
   Z = 1.2×WC/TA + 1.4×RE/TA + 3.3×EBIT/TA + 0.6×MVE/TL + 1.0×Sales/TA
   ├── Z > 3.0: Safe zone
   ├── 1.8 < Z < 3.0: Gray zone (monitor)
   └── Z < 1.8: Distress zone (high bankruptcy probability)

3. BENEISH M-SCORE (earnings manipulation)
   M = -4.84 + 0.92×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI + 0.115×DEPI
       - 0.172×SGAI - 0.327×LVGI + 4.679×TATA
   ├── M > -2.22: Likely manipulator
   └── M < -2.22: Unlikely manipulator

4. TRIANGULATION RULE
   F-Score ≥ 7 AND Z-Score > 3.0 AND M-Score < -2.22 = HIGH QUALITY
   F-Score ≤ 3 OR Z-Score < 1.8 OR M-Score > -1.78 = HIGH RISK — do not buy regardless of valuation

   Complete when: All three scores computed. Quality label assigned.

```

### Phase 4: Fundamental Buy/Sell Signal Generation

```

1. VALUATION SIGNAL
   Compare current price to intrinsic value range:
   ├── Price < Bear Case: STRONG BUY (margin of safety even in worst scenario) — confidence 80
   ├── Price < Base Case: BUY (margin of safety in base scenario) — confidence 60
   ├── Price between Base and Bull: HOLD (fairly valued) — confidence 50
   ├── Price > Bull Case: OVERVALUED — confidence 40
   └── Price > 1.5x Bull Case: STRONG SELL — confidence 75

2. QUALITY SIGNAL
   Quality score modifies valuation signal:
   ├── High Quality: reinforce buy, dampen sell
   ├── Average Quality: neutral
   └── Low Quality: dampen buy (value trap risk), reinforce sell

3. DIVIDEND SIGNAL (for dividend-paying stocks)
   ├── Dividend Yield > 3% AND Payout Ratio < 60% AND 5Y Dividend Growth > 5% → DIVIDEND BUY
   ├── Payout Ratio > 80% → UNSUSTAINABLE — cut risk high
   ├── Dividend cut in past 3 years → DIVIDEND RISK — reduce confidence 20
   └── FCF < Dividend Payments → FINANCING DIVIDENDS WITH DEBT — red flag

4. MOMENTUM OVERLAY (business momentum, not price momentum)
   ├── Revenue Growth Accelerating (3Y CAGR > 5Y CAGR): +10 confidence
   ├── Margin Expanding (last year > 3Y avg): +10 confidence
   ├── Revenue Growth Decelerating: -10 confidence
   └── Margin Contracting: -10 confidence

5. FINAL SIGNAL OUTPUT
   {
     "ticker": "AAPL",
     "signal_type": "BUY",
     "confidence": 68,
     "valuation": {
       "method": "DCF + Comparables",
       "bear_case": 155,
       "base_case": 185,
       "bull_case": 220,
       "current_price": 170,
       "margin_of_safety": "8.8% below base case"
     },
     "quality": {
       "piotroski_f_score": 7,
       "altman_z_score": 5.2,
       "beneish_m_score": -2.8,
       "quality_label": "HIGH"
     },
     "key_ratios": {
       "pe_trailing": 28.5,
       "pe_forward": 24.1,
       "peg_ratio": 1.8,
       "ev_ebitda": 18.2,
       "fcf_yield": 0.041,
       "roe": 0.52,
       "debt_equity": 1.4
     },
     "red_flags": [],
     "earnings_date": "2026-10-27"
   }

   Complete when: Signal generated with all required fields.

```

### Phase 5: Multi-Stock Screening

```

1. SCREEN PARAMETERS (user-specified or defaults)
   ├── Market Cap: > $2B (avoid micro-cap manipulation)
   ├── Avg Volume: > $10M/day (liquidity)
   ├── FCF Yield: > 3% (positive cash generation)
   ├── Debt/Equity: < 2.0 (financial health)
   ├── ROIC > WACC (value creation)
   └── Piotroski F-Score: ≥ 5 (quality floor)

2. RANK METHODOLOGY
   Composite Score = normalized(FCF_Yield) + normalized(ROIC) + normalized(F_Score) - normalized(Debt_Equity)

3. OUTPUT
   Top 20 ranked by composite score with:
   ├── Composite Score, FCF Yield, ROIC, PE, EV/EBITDA, Debt/Equity, F-Score, Z-Score
   └── Sorted by composite score descending

   Complete when: Screen results ranked and output with all columns.

```


   Complete when: [VERIFIED] All positions sized within capital constraints.
   Complete when: [VERIFIED] Correlation matrix checked and N_effective > 3.
   Complete when: [VERIFIED] Circuit breakers armed and tested.
   Complete when: [VERIFIED] Broker connection in READY state.
   Complete when: [VERIFIED] No sector exceeds 25% exposure.
   Complete when: [VERIFIED] Stop-losses set for all open positions.
## Decision Trees

<!-- STANDARD: 3min -->

### Valuation Method Selection

```

What type of company?
├── Mature, profitable, predictable cash flows → DCF (primary) + Comparables (check)
├── High growth, negative earnings → Reverse DCF (what growth is priced in?) + Revenue multiples
├── Financial (bank, insurance) → P/B + ROE analysis + Dividend Discount Model
│   └── Do NOT use DCF for financials — capex/working capital meaningless for banks
├── Cyclical (energy, materials, semi) → Mid-cycle normalized earnings + EV/EBITDA
│   └── Do NOT use peak or trough earnings — normalize across the cycle
├── Asset-heavy (REITs, pipelines) → P/FFO or P/AFFO + NAV
└── Pre-revenue (biotech, exploration) → rNPV (risk-adjusted NPV) + comparable transactions

```

### Red Flag Triage

```

Red flag detected → classify severity
├── FCF negative 2+ years → HIGH — company consuming cash
│   └── Exception: pre-revenue growth with documented TAM + runway > 24 months
│
├── Debt/EBITDA > 5x → HIGH — default risk elevated
│
├── Beneish M-Score > -1.78 → HIGH — likely earnings manipulation
│
├── Revenue growth < Receivables growth → MEDIUM — possible channel stuffing
│
├── Depreciation/Capex < 0.7 → MEDIUM — under-investing in assets
│
├── ROE > 30% driven by leverage (Equity Multiplier > 5x) → MEDIUM — leverage mirage
│
├── Share count increasing > 2%/year → MEDIUM — dilution
│
└── Auditor changed in past 12 months → MEDIUM — investigate reason

Decision:
├── Any HIGH flag → DO NOT BUY — walk away, there are 10,000+ other stocks
├── 2+ MEDIUM flags → DO NOT BUY without documented thesis addressing each flag
└── 0-1 MEDIUM flags → Proceed to valuation with flags documented in signal warnings

```

### ETF Fundamental Screening

```

ETF type?
├── Index ETF (SPY, QQQ, IWM)?
│   ├── Expense Ratio < 0.10%: PASS
│   ├── Tracking Error (1Y) < 0.10%: PASS
│   ├── AUM > $500M: PASS (liquidity, low closure risk)
│   ├── Holdings: full replication > sampling
│   └── Premium/Discount < 0.10%: PASS (no NAV dislocation)
│
├── Thematic ETF (ARKK, ICLN, TAN)?
│   ├── Expense Ratio < 0.75%: PASS
│   ├── AUM > $100M (closure risk: thematic ETFs close at 3x rate of index)
│   ├── Holdings overlap with broad market < 60% (otherwise buy the cheaper index fund)
│   └── WARNING: thematic ETFs launched after the theme's 100%+ rally underperform by 6-8%/year
│       └── If ETF launched < 2 years ago and theme rallied 50%+ pre-launch → HIGH RISK
│
├── Leveraged/Inverse ETF?
│   ├── Expense Ratio + decay drag = real cost (1.0-2.0%/year beyond stated ER)
│   ├── Hold period MUST be < 1 day for 3x, < 1 week for 2x
│   └── NOT suitable for fundamental buy-and-hold — decay destroys long-term returns
│
└── Bond ETF (AGG, LQD, HYG)?
    ├── Yield to Maturity > Expense Ratio + 0.50%: net positive carry
    ├── Duration: match to investment horizon (duration ≤ years to need money)
    ├── Credit Quality: % below investment grade < tolerance threshold
    └── Average Maturity: match to rate outlook

```

## Gotchas

<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Using mean instead of median for comparable company multiples. One outlier with PE of 200 drags the mean to 35 while the median is 18. Your stock at PE 15 looks cheap against mean 35 but is only 17% below median 18 — barely a discount. | $25K-$100K in "value trap" positions. Mean-distorted valuations are the #1 cause of buying "cheap" stocks that are actually fairly valued. | Always use median for comparable multiples. Report both mean and median; flag when they diverge >20% as "outlier distortion." |
| Ignoring share-based compensation (SBC) when computing FCF. A tech company reports $5B FCF but paid $3B in SBC (not a cash expense in GAAP FCF). Real FCF available to shareholders is $2B — 60% lower. The stock at 10x FCF is actually 25x real FCF. | $50K-$500K in overvalued tech positions. SBC is real dilution — it transfers value from existing shareholders to employees. Treat SBC as a cash expense for FCF purposes. | Compute Owner Earnings: FCF - SBC. This is the real cash available to shareholders. If Owner Earnings / GAAP FCF < 0.7, the company is dilution-funding its operations. |
| DCF terminal value exceeding 70% of total enterprise value. A 5-year DCF where TV = 85% of EV means you're valuing the company on a guess about year 6-infinity, not on the 5 years you actually forecasted. The terminal growth rate assumption dominates the entire valuation. | $100K-$2M in misvalued acquisitions. An 85% TV DCF means a 0.5% change in terminal growth rate changes valuation by 15-20%. Your "precise" DCF is 85% assumption, 15% analysis. | If TV > 70% of total EV: (a) extend forecast period to 7-10 years, (b) use an EV/EBITDA exit multiple instead of Gordon Growth, or (c) admit this is too uncertain for DCF and use comparables. |
| Comparing PE ratios across different industries. A utility at PE 18 is expensive (sector median 16). A SaaS company at PE 50 is cheap (sector median 70). Cross-industry PE comparison is like comparing baseball batting averages to cricket batting averages. | $15K-$75K in misinformed "value" decisions. Every industry has a different earnings growth rate, risk profile, and capital intensity that justifies different PE levels. | Always compare PE to (a) the company's own 5-year historical range and (b) direct industry peers. Never compare a tech PE to an industrial PE. Use EV/EBITDA for cross-sector comparisons — it's capital-structure neutral. |
| Treating all revenue growth equally. A company growing revenue 20% through acquisition (buying competitors) is fundamentally different from 20% organic revenue growth. The acquirer is spending cash + issuing debt/equity; the organic grower is compounding internally. | $30K-$200K in acquisition-heavy positions that crash when the M&A pipeline dries up. Post-acquisition, EPS often declines as purchase accounting amortization hits. | Decompose revenue growth into: organic (same-store, constant currency) + acquisition contribution + FX impact. Only organic growth compounds without additional capital. |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|---|
| `market-data-engineer` | SEC filing feeds, financial statement data, earnings calendars | Before any DCF or quality score — stale filings produce stale valuations |
| `quantitative-analyst` | Statistical significance testing, factor model validation, sector benchmarking | When building multi-factor quality models or validating valuation accuracy |
| `financial-security` | Data source integrity checks, insider trading screens, material non-public information guardrails | Before incorporating any non-public data or pre-release filings |


<!-- STANDARD: 2min -->

| Upstream | What You Receive | When to Involve |
|---|---|---|
| `market-data-engineer` | Clean fundamental data: income statement, balance sheet, cash flow, filings | Before any analysis — data must be GAAP-consistent and restatement-aware |
| `data-scientist` | Sector/industry aggregate metrics, statistical validation of screening factors | When designing multi-factor screens or validating signal efficacy |

| Downstream | What You Provide | Handoff Artifact |
|---|---|---|
| `portfolio-signal-manager` | Fundamental signals with valuation ranges, quality scores, red flags | Full signal JSON (Phase 4 format) with all fields |
| `algorithmic-trader` | Fundamental buy/sell decisions ready for execution sizing | Signal JSON + target price range + red flag warnings |
| `technical-signals-engineer` | Earnings dates for signal suppression, fundamental quality overlay | Earnings calendar + quality labels per ticker |

## Verification Guardrails

<!-- STANDARD: 2min -->

Before delivering work, verify:

- [ ] **Valuation is a range, not a point:** Bear/Base/Bull scenarios with explicit assumptions for each
- [ ] **3+ years of financials analyzed:** Minimum 3 fiscal years of all three statements
- [ ] **GAAP EPS reconciled to Adjusted EPS:** One-time items isolated, difference quantified
- [ ] **All three quality scores computed:** Piotroski F-Score, Altman Z-Score, Beneish M-Score
- [ ] **Medians used for comparables:** Mean reported alongside median; >20% divergence flagged
- [ ] **Red flags investigated:** FCF-negative, high leverage, earnings manipulation checked
- [ ] **Terminal value < 70% of total EV:** If exceeded, forecast extended or exit multiple used
- [ ] **SBC treated as expense:** Owner Earnings = FCF - SBC reported alongside GAAP FCF
- [ ] **Organic growth decomposed:** Revenue growth split into organic + acquisition + FX
- [ ] **ETF screening uses fundamentals:** Expense ratio + tracking error primary, not trailing returns

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

- [ ] **[R1]** Fair value expressed as bear/base/bull range, not single point
- [ ] **[R2]** Minimum 3 years of financial statements analyzed
- [ ] **[R3]** Adjusted PE computed alongside GAAP PE; one-time items flagged
- [ ] **[R4]** ETF screens use expense ratio + tracking error as primary sort
- [ ] **[R5]** F-Score, Z-Score, M-Score all computed (quality triangulation)
- [ ] **[R6]** FCF-negative for 2+ years → no buy without documented thesis
- [ ] **[R7]** Non-GAAP metrics reconciled to GAAP with bridge table
- [ ] **[R8]** Comparables use median, not mean; outlier distortion flagged
- [ ] **[R9]** Owner Earnings (FCF - SBC) reported for tech companies
- [ ] **[R10]** Terminal value < 70% of EV; if not, methodology adjusted
- [ ] **[R11]** Revenue growth decomposed into organic + acquisition + FX
- [ ] **[R12]** All red flags documented in signal output warnings

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| DCF valuation 50%+ above market price | Terminal growth rate too high (3.5%+) or WACC too low | Cap terminal growth at risk-free rate + 1%. Use exit multiple EV/EBITDA as cross-check. If DCF still >50% above market, market knows something your model doesn't. | **The market is usually right about something you missed.** A >50% gap between DCF and market price is a red flag on your assumptions, not a buying opportunity. |
| PE looks cheap but company keeps falling | One-time gain inflated last year's earnings or cyclical peak earnings | Normalize earnings: use 5-year average EPS or mid-cycle earnings. Compute PE on normalized, not trailing. | **Cyclical peak earnings make PE look artificially low.** The stock isn't cheap — earnings are about to mean-revert down. |
| F-Score 8 but Z-Score 1.5 | Piotroski uses ROA (asset-light = high ROA). Altman uses EBIT/TA (asset-light doesn't help if earnings collapse). | Trust Z-Score for bankruptcy risk. F-Score measures operational quality, Z-Score measures financial survival. They measure different things. | **Quality and solvency are different dimensions.** A high-quality business can still be overleveraged into distress. |
| Great fundamentals but stock down 40% in 3 months | You're looking at stale data. The last 10-Q is 4 months old and something changed. | Check for: insider selling in past 90 days, analyst downgrades, short interest change, recent 8-K filings. Stale fundamental data is more dangerous than no fundamental data. | **Fundamental data has a shelf life.** 10-Qs are quarterly. Between filings, track: insider transactions, short interest, analyst revisions, 8-Ks. |

## What Good Looks Like

**Before (Novice):**

```python
pe = price / eps  # GAAP EPS, no adjustments
if pe < 15:
    signal = "BUY"  # single metric, no quality check, no range
print(f"Fair value is ${dcf_result:.2f}")  # single point

```

**After (This Skill):**

```python
# Multi-metric, quality-triangulated, range-based valuation
adjusted_eps = remove_one_time_items(gaap_eps, one_time_items)
norm_eps = five_year_average(adjusted_eps)
pe_trailing = price / gaap_eps
pe_adjusted = price / adjusted_eps
pe_normalized = price / norm_eps
pe_peer_median = sector_median_pe(peers)  # median, not mean

f_score = piotroski(ni, ocf, roa, lt_debt, current_ratio, gross_margin, asset_turnover, shares)
z_score = altman_z(wc_ta, re_ta, ebit_ta, mve_tl, sales_ta)
m_score = beneish(dsri, gmi, aqi, sgi, depi, sgai, lvgi, tata)

dcf_range = {
    "bear": dcf(growth=base_growth*0.7, fcf_margin=avg_margin-0.02, wacc=base_wacc+0.01),
    "base": dcf(growth=base_growth, fcf_margin=avg_margin, wacc=base_wacc),
    "bull": dcf(growth=base_growth*1.3, fcf_margin=avg_margin+0.02, wacc=base_wacc-0.01)
}

owner_earnings = fcf - stock_based_comp
if dcf_range["tv_pct"] > 0.70:
    dcf_range = recalculate_with_exit_multiple()

signal = build_fundamental_signal(valuation_range=dcf_range, quality=(f_score, z_score, m_score), ...)

```

Problems solved: adjusted/normalized earnings, median comparables, quality triangulation, DCF range not point, TV% check, SBC adjustment.

## References

- [valuation-methods.md](references/valuation-methods.md) — DCF construction, comparable analysis, Graham Number, sector-specific methods
- [financial-ratios.md](references/financial-ratios.md) — Complete ratio catalog: profitability, health, efficiency, valuation with formulas
- [quality-scores.md](references/quality-scores.md) — Piotroski F-Score, Altman Z-Score, Beneish M-Score: computation and interpretation
- [earnings-quality.md](references/earnings-quality.md) — Detecting manipulation: accruals, revenue recognition, SBC, one-time items
- [dividend-analysis.md](references/dividend-analysis.md) — Dividend sustainability, payout ratios, growth modeling, cut risk
- [etf-fundamentals.md](references/etf-fundamentals.md) — Expense ratios, tracking error, AUM, holdings analysis, thematic ETF risks
- [red-flags-checklist.md](references/red-flags-checklist.md) — Catalog of accounting red flags with historical case studies (Enron, Wirecard, Luckin)
- [screening-methodology.md](references/screening-methodology.md) — Multi-factor screening design, composite scoring, sector-specific adjustments

## Deliberate Practice

<!-- STANDARD: 3min -->

1. Build a full DCF model for a single company from scratch using only 10-K/10-Q filings
2. Compare your quality score against Morningstar's moat rating for 10 companies — trace every disagreement
3. Run DuPont analysis on 5 companies in the same sector and rank them by quality of ROE decomposition
4. Backtest: Take fundamentals from 3 years ago and predict today's stock price — measure your error rate
5. Red-flag drill: Find 10 companies that later had accounting scandals. Would your checks have caught them?


## Proactive Triggers

<!-- STANDARD: 3min -->

| Trigger | Action | Window |
|---------|--------|--------|
| SEC filing posted for a tracked company | Parse and update quality score within 1 hour | 1h |
| Earnings surprise >10% | Re-run DCF with new assumptions; flag if fair value changes >15% | 4h |
| Auditor change announced | Downgrade quality score 2 points pending review; flag for risks | Immediate |
| Peer company flagged for accounting issues | Audit tracked companies in same sector with same auditor | 48h |
| No signal generated for 30 days | Scan for stale data; verify financial data sources are current | 7 days |


## Anti-Rationalization

<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "Management said earnings would recover" | Forward guidance is marketing. Discount it to 0. Model only from reported financials and verifiable data |
| "The DCF says fair value is $X so it must converge" | DCF is a range, not a point. If the discount rate needs 8% to justify the price, the stock is expensive, not undervalued |
| "We'll use the same multiples as peers" | Peer multiples embed the same market sentiment you're trying to validate against. Use historical range AND peer comparison |
| "This quarter was a one-off — exclude it" | Every quarter is a one-off until it's a trend. Exclusion requires documented justification and a counterfactual model |
| "The balance sheet looks clean enough" | Off-balance-sheet items destroyed Enron, GE, and countless others. "Clean enough" means you haven't looked hard enough |
