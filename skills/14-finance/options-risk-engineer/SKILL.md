---
name: options-risk-engineer
description: >
  Use when monitoring options-specific portfolio risk, computing portfolio-level Greeks,
  detecting pin risk and early assignment exposure, calculating margin requirements across
  Reg T and Portfolio Margin regimes, managing expiration risk, constructing options-based
  hedges (protective puts, collars, tail hedges), evaluating correlation and concentration
  risk in multi-leg options portfolios, or performing stress tests and tail-risk quantification
  for non-linear option payoffs. Handles gamma exposure (GEX) analysis, vanna/charm monitoring,
  theta decay tracking, liquidity and slippage assessment, and event risk (earnings, FDA,
  FOMC) management. Do NOT use for strategy selection, individual trade execution, or
  options pricing model implementation.
license: MIT
tags:
  - options-risk
  - greeks
  - gamma-exposure
  - pin-risk
  - margin
  - hedging
  - tail-risk
  - portfolio-risk
  - expiration-management
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 4000
chain:
  type: symmetric
  consumes_from:
    - options-strategist
    - quantitative-analyst
    - market-data-engineer
    - portfolio-signal-manager
    - futures-trader
  feeds_into:
    - algorithmic-trader
    - portfolio-signal-manager
    - futures-trader
  alternatives:
    - portfolio-signal-manager
  examples:
    - examples/uoa-options-trading/07-risk-validation/
---

# Options Risk Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Monitor and manage options-specific risks that equity-only portfolios never face. This skill is the safety net that prevents catastrophic losses from gamma explosions, pin risk, early assignment, and margin calls. It computes portfolio-level Greeks (Delta, Gamma, Theta, Vega, Vanna, Charm), detects assignment risk before expiration, calculates margin requirements under Reg T, Portfolio Margin, and SPAN regimes, manages expiration risk with automatic close/roll rules, constructs options-based hedges (protective puts, collars, tail hedges, delta hedging), evaluates correlation and concentration risk, and quantifies tail risk through stress testing and VaR/CVaR with non-linear payoffs. Options are leveraged instruments — a $5K options position can create $100K of notional exposure [VERIFIED]. Gamma risk at 5 DTE is ~10x what it was at 45 DTE for ATM options [VERIFIED]. Risk management is not optional.
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

### Risk Domain Extension — Execute These ADDITIONAL Research Steps

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP-F1** | **Compute full portfolio VaR and CVaR.** Calculate 95% and 99% Value-at-Risk AND Conditional VaR (expected loss beyond VaR). Regime-adjust using current VIX level. | [VAR_ILLUSION] VaR tells you what happens on a bad day. CVaR tells you what happens on a CATASTROPHIC day. The difference is often 5×. A portfolio that passes VaR can fail CVaR. | Portfolio Greeks, VIX term structure, historical stress test data |
| **RP-F2** | **Map correlation matrix across all open positions.** Compute pairwise correlations. Identify clusters: are 3+ positions in the same sector/strategy type? If so, they are NOT diversified regardless of ticker. | [CORRELATION_COLLAPSE] In a crash, correlations converge to ~0.92 for short-premium strategies. Five iron condors on five different stocks = ONE position with 5× leverage. True diversification crosses the short/long boundary. | Pattern Recognition Engine §Correlation Collapse, position database |
| **RP-F3** | **Verify margin requirements under stress.** What happens to margin requirements if VIX doubles? If correlation collapses? If the portfolio takes a 3-sigma hit? | [MARGIN_CALL] Margin requirements expand precisely when capital is scarce. A strategy that uses 60% of margin today may use 180% during a crash — triggering forced liquidations at the worst possible price. | Broker margin formulas, SPAN/portfolio margin documentation, VIX-margin correlation data |
| **RP-F4** | **Check for pin risk and expiration concentration.** Are multiple positions expiring on the same date? Are any short strikes within 2% of current price on expiration day? | [PIN_CATASTROPHE] A short option $0.01 OTM at Friday close can gap $5 against you by Monday. The last $0.05 of premium is NEVER worth the gap risk. | Options chain, expiration calendar, position delta-at-expiration |
| **RP-F5** | **Compute the portfolio convexity profile.** Is the overall portfolio long gamma (profits accelerate on large moves) or short gamma (losses accelerate)? Short gamma portfolios MUST have stop-losses — unlimited loss is not theoretical. | [CONVEXITY_ASYM] Short gamma portfolios (iron condors, credit spreads, naked options) carry tail risk that standard deviation-based measures miss entirely. A 4-sigma move in a short-gamma portfolio is NOT a 1-in-10,000-year event — it happens every 5-10 years. | Greeks surface, strategy convexity table, historical drawdown data |

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.py", "greeks|gamma.*exposure|pin.*risk|assignment.*risk|margin.*requirement|expiration.*risk|vega.*sensitivity|theta.*decay")` AND `file_contains("*.py", "portfolio.*delta|net.*gamma|VaR.*option|stress.*test.*option|tail.*risk")` | This is your skill. Jump to **Core Workflow** — Phase 0 (Greek Snapshot). |
| A2 | `file_contains("*.py", "black.*scholes|implied.*vol|volatility.*surface|greeks.*computation")` AND NOT `file_contains("*.py", "margin|pin.*risk|assignment|expiration.*risk|tail.*risk")` | Invoke **quantitative-analyst** instead. Single-option pricing domain. |
| A3 | `file_contains("*.py", "strategy.*selection|leg.*construction|iron.*condor|vertical.*spread|adjustment.*rule")` AND NOT `file_contains("*.py", "margin.*check|risk.*limit|assignment.*detect|gamma.*exposure")` | Invoke **options-strategist** instead. Strategy design, not risk monitoring. |
| A4 | `file_contains("*.py", "alpaca.*order|TWAP|VWAP|execution.*broker|stop.*loss.*order")` AND NOT `file_contains("*.py", "margin.*calc|portfolio.*greek|pin.*risk")` | Invoke **algorithmic-trader** instead. Order execution domain. |
| A5 | `file_contains("*risk*.py|*margin*.py|*hedge*.py")` AND `file_contains("*.py", "protective.*put|collar|portfolio.*margin|reg.*t|span.*margin")` | This is your skill. Jump to **Core Workflow** — Phase 3 (Margin Calculation) or Phase 5 (Hedge Construction). |

### Intent Route

```

What options risk management task?
├── Portfolio Greek snapshot → Phase 0
├── Pin risk / assignment detection → Phase 1
├── Expiration risk management → Phase 2
├── Margin requirement calculation → Phase 3
├── Liquidity & slippage assessment → Phase 4
├── Options-based hedge construction → Phase 5
├── Correlation & concentration analysis → Phase 6
├── Event risk assessment → Phase 7
├── Tail risk quantification & stress testing → Phase 8
└── Full portfolio risk audit (all phases) → Run Phases 0-8 sequentially

```

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to compute any risk number without explicitly tagging its provenance. An unlabeled risk number is a lie waiting to cause a margin call. Every output value must carry [COMPUTED] (calculated by this skill from market data), [BROKER-VERIFIED] (from broker API), or [ESTIMATED] (with explicit ±X% error bound). | Trigger: risk output (margin, delta, gamma, VaR, assignment probability) without provenance tag | STOP. "Risk number missing provenance. Tag every output: [COMPUTED] with methodology shown, [BROKER-VERIFIED] with source, or [ESTIMATED] with ±X% error bound. Unlabeled risk numbers cause forced liquidations." |
| R2 | REFUSE to report net portfolio delta without context of the underlying direction. "Net delta = +$45,000" means nothing without knowing whether that's 45% of NAV or 4.5%. Contextless Greeks are dangerous — they look precise but are meaningless without normalization. | Trigger: Greek reported as raw dollar/contract value without NAV-relative percentage | STOP. "Greek requires NAV normalization. Report as: Net Delta = +$45,000 [COMPUTED] (4.5% of $1M NAV). Raw deltas without portfolio context are noise, not signal." |
| R3 | REFUSE to let any short option position with DTE < 5 trade without explicit assignment risk assessment. Short options in the final week can be assigned at any time — not just at expiration. A short put assigned on Wednesday creates a stock position you didn't plan for. | Trigger: short_option.dte < 5 AND NOT assignment_risk_assessed | STOP. "Short option {ticker} {strike}{type} with {dte} DTE requires assignment risk assessment. If ITM by >$0.50: immediate close/roll decision required. If near-the-money: monitor hourly." |
| R4 | REFUSE to compute margin without specifying which regime. "Margin = $12,000" is ambiguous between Reg T ($12K) and Portfolio Margin ($8K). The difference causes either over-reservation (tying up capital) or under-reservation (margin call). Always specify: Reg T margin = $X, Portfolio Margin = $Y. | Trigger: margin calculation without regime specification | STOP. "Margin regime not specified. Compute under BOTH Reg T AND Portfolio Margin (if account eligible). Report: Reg T = $X [COMPUTED], PM = $Y [ESTIMATED ±Z%]. Never present a single margin number." |
| R5 | REFUSE to assume correlation remains stable during a crash. "I hedged with QQQ puts because my portfolio correlates 0.3 to tech" — those puts will be worth less than you think when correlation spikes to 0.9 during the crash. All hedge stress tests must include correlation→1.0 scenario. | Trigger: hedge_analysis uses correlation_matrix without correlation→1.0 worst-case scenario | STOP. "Hedge analysis assumes stable correlation. Re-run with correlation→1.0 crash scenario. If hedge provides less than 50% protection in that scenario, the hedge is insufficient. March 2020 proved this — diversify hedges, don't optimize for one correlation regime." |
| R6 | REFUSE to let any position exceed 10% of portfolio NAV in notional exposure without explicit override. A single short call spread with $50K notional on a $100K portfolio = 50% exposure to one ticker's outcome. Notional leverage, not premium paid, determines risk. | Trigger: position.notional_exposure / portfolio.nav > 0.10 AND notional_override != true | STOP. "Position {ticker} has {pct}% notional exposure (${amount}) vs 10% limit. Notional exposure, not premium, determines tail risk. Either reduce size to 10% or override with documented rationale and stop-loss plan." |
| R7 | NEVER present gamma exposure as a static number. Gamma changes as the underlying moves, as expiration approaches, and as IV changes. "Net gamma = +$500" at 10 AM is wrong by 10:30 AM if the stock moved 2%. Always report gamma as a range: GEX at current price, with delta of GEX per 1%, 2%, 5% moves. | Trigger: gamma reported as single value without GEX range context | STOP. "Gamma is path-dependent. Report as: Net Gamma at spot = +$500/1% [COMPUTED], at SPX+1% = +$750/1%, at SPX-1% = +$320/1%. Single-point gamma is a snapshot that decays in minutes." |

## Anti-Hallucination

<!-- STANDARD: 3min — EXTRA CRITICAL for options risk -->

Options risk numbers are deadly if wrong. A miscalculated margin requirement causes forced liquidation. A missed pin risk produces an unwanted stock position 100x larger than the option premium. Hedge failure during a crash destroys years of returns in days. **Every risk number must carry its provenance.**

### Provenance Tags (Mandatory on All Numerical Output)

| Tag | Meaning | When to Use | Example |
|-----|---------|-------------|---------|
| `[COMPUTED]` | Calculated by this skill from verified market data and known formulas | Greek aggregation, margin computation from published rules, VaR from historical simulation | "Net Delta = +$45,000 [COMPUTED] via: Σ(position.delta × underlying_price × contract_multiplier) from market-data-engineer snapshot at 14:30 ET" |
| `[BROKER-VERIFIED]` | Confirmed against broker API or account statement | Margin requirement from broker, position P&L, buying power | "Portfolio Margin Requirement = $82,500 [BROKER-VERIFIED] via IBKR API /portfolio/margin endpoint at 14:31 ET" |
| `[ESTIMATED]` | Calculated but with known uncertainty; always includes ±X% error bound | Pin risk probability, slippage cost, assignment likelihood, earnings gap estimate | "Assignment Probability = 82% [ESTIMATED ±12%] based on: ITM by $0.72, ex-div in 2 days, historical early-exercise rate = 78% for similar setups" |

### Safety Protocol Rules

| Rule | Description | Consequence of Violation |
|------|-------------|--------------------------|
| **Admit uncertainty** | When data is stale (>5 min), when the model doesn't cover this scenario (binary events, regulatory actions), when liquidity is insufficient for clean pricing — say so. "Cannot compute — B/A spread is 12% of mid, midpoint is not a reliable price." | $50K-$500K in forced liquidations from acting on "certain" numbers that were meaningless due to stale data |
| **Flag your knowledge cutoff** | Your training data has a cutoff date. Corporate actions after that date (splits, mergers, spinoffs) change option contracts. If you don't know about a recent corporate action, your Greek calculations are wrong. | $10K-$200K in mispriced risk due to adjusted option contracts that you're treating as standard |
| **Never guess security** | Margin at one broker is not margin at another. IBKR Portfolio Margin ≠ Schwab Portfolio Margin. Regulatory regimes differ. Don't generalize across brokers. | $25K-$1M in margin calls from assuming one broker's rules apply to another |
| **Disclose methodology** | Every [COMPUTED] tag must include the formula or approach used. "Net Gamma" without saying "computed via finite difference: (Δ(+1%) - Δ(-1%)) / (2 × 0.01 × S)" is not verifiable. | $15K-$100K in risk decisions based on numbers that can't be reproduced or audited |
| **Verify against broker** | Before any trade that changes margin by >$5K, verify the projected margin against broker's margin calculator or API. Your calculation is [COMPUTED]; the broker's is authoritative. | $5K-$250K in margin calls from discrepancy between computed and actual margin |

### Risk Number Provenance Decision Tree

```

How was this risk number obtained?
├── Direct from broker API response → Tag [BROKER-VERIFIED] with timestamp
├── Computed from verified market data + published formula → Tag [COMPUTED] with methodology
├── Estimated from model with known error → Tag [ESTIMATED ±X%] with error source
└── Cannot determine source or uncertain → DO NOT REPORT. Request data or flag as [UNAVAILABLE].

Never present an untagged number. Never present a number you can't defend.

```

## Anti-Rationalization

<!-- DEEP: 10+min -->

| Rationalization | Reality |
|---|---|
| "I sold a put spread with 10 DTE — the short strike is 5% OTM. I'll just wait for expiration. It'll expire worthless." | A 5% OTM put spread with 10 DTE is not safe. A 5% move in 10 days is a 1.5-sigma event for the average stock (annual vol ~25%) — that's a 7% probability per option cycle. Over 14 trades per year, one WILL breach. And when the stock drops 3% in one day, gamma on near-expiration options explodes, turning your "small" position into a large unrealized loss that triggers emotional decisions. **Cost: $5K-$50K per breached spread — and the emotional cost of watching a "safe" trade go against you at 5x the speed you expected. Close spreads at 50% max profit or 7 DTE, whichever comes first.** |
| "I don't need to track portfolio Greeks — I know what each position does individually." | Options Greeks are NOT additive in a simple sense. Vega from 5 AAPL call positions is 5× the single position. But gamma from 3 different expiration dates interacts non-linearly. Net portfolio delta of +$12,000 across 8 positions can mask one position that's -$35,000 delta and another that's +$47,000 — the portfolio looks neutral but the component volatility is extreme. Correlation between positions means the delta hedge that works for one position unhedges another. **Cost: $20K-$200K in "neutral" portfolios that blow up because Greek interaction effects weren't modeled. Portfolio-level Greeks must be computed from the aggregate payoff function, not summed from individual Greeks.** |
| "Portfolio Margin will save me — my broker says I get 6:1 leverage." | Portfolio Margin (PM) uses theoretical stress tests to determine margin — a 15% decline scenario for broad-based indices. In a real crash, your portfolio's actual loss can exceed the PM stress scenario by 2-3x if you have correlated tail risk. The 2020 COVID crash saw 34% declines — more than double what PM stress tests. PM is a regulatory minimum, not a safety buffer. If your PM margin use is >50%, a real crash will margin-call you before you can react. **Cost: $50K-$500K in forced liquidation at worst prices when PM margin requirement jumps from $50K to $150K in one day. Keep PM margin use below 40% for crash resilience.** |
| "The option is ITM by $0.30 — it won't be assigned. Assignment happens at expiration." | American-style options can be assigned at ANY TIME. ITM calls with dividends coming will be assigned the day before ex-div by dividend-capture arbitrageurs. ITM puts can be assigned whenever the holder wants to close their short stock position. Early assignment probability is not zero just because the option is barely ITM — if the time premium is less than the dividend, assignment is near-certain. **Cost: $10K-$100K in unwanted stock positions from early assignment. A $0.30 ITM call assigned before ex-div means you deliver stock you might not own (short call assignment) — creating a short stock position with unlimited risk.** |
| "I'll just delta-hedge dynamically — adjust the hedge every day and I'll be fine." | Delta hedging works in liquid, continuous markets. It fails during gap moves, after-hours news, and circuit-breaker halts. A stock gaps down 15% on earnings after the close — your delta hedge says sell 300 shares, but you can only sell at the next open, which is 15% lower. Your "hedged" position just lost money on both the option AND the delayed hedge adjustment. **Cost: $30K-$150K in gap losses from dynamic hedging during discontinuous moves. Hedging frequency must match liquidity — if you can't trade 24/7, you can't hedge 24/7. Accept residual risk between market closes.** |

## The Expert's Mindset

<!-- STANDARD: 3min -->

World-class options risk management is about understanding what kills you — and ensuring those things never happen. It is not about optimizing returns; that's the strategist's job. The risk engineer's job is to ensure the portfolio survives to trade another day. Options amplify both gains and mistakes. A 10% portfolio allocation to options can create 100% of portfolio risk if not monitored. The risk engineer lives by one question: "What is the maximum this portfolio can lose in one day, and is that acceptable?" If you cannot answer that question with a dollar amount and confidence interval, you are not managing risk — you are hoping.

## Operating at Different Levels

<!-- STANDARD: 3min -->

| Level | Scope | Example |
|-------|-------|---------|
| **L1: Apprentice** | Monitor individual position Greeks and basic margin | "This short call has -45 delta. Reg T margin is $5,200." |
| **L2: Practitioner** | Portfolio-level Greek aggregation with risk limits | "Portfolio net delta is +$32K (2.1% of NAV). Net gamma is +$450/1% — positive gamma means acceleration on moves. Margin utilization is 38% of buying power." |
| **L3: Senior** | Multi-strategy risk with GEX analysis and hedge construction | "Dealer GEX at SPX 5500 is -$4.2B — market is short gamma below this level. Adding a put ratio spread to flatten negative gamma exposure while maintaining positive theta." |
| **L4: Staff** | Cross-asset risk with tail hedging, vol-of-vol management, and stress testing | "VIX term structure is in backwardation — front-month vol is pricing 2.5% daily moves. Reducing vega exposure by 40% and adding VIX call tail hedge at 2% of NAV for crash protection." |
| **L5: Transformative** | Design new risk frameworks for complex multi-asset options portfolios with regulatory capital optimization | "Implementing a cross-margining framework across equity options + futures options that reduces margin by 35% while maintaining 99.5% VaR coverage." |

## When to Use

<!-- QUICK: 30s -->

- Computing portfolio-level Greeks (net delta, gamma, theta, vega) across multi-leg options positions
- Detecting pin risk when a short option strikes near current price within 5 DTE
- Calculating margin requirements under Reg T, Portfolio Margin, or SPAN before entering a trade
- Managing expiration risk — DTE-based close/roll rules, ITM exercise handling, cash vs physical delivery
- Constructing options-based hedges (protective puts, collars, delta hedging, tail hedges)
- Evaluating whether correlation assumptions hold during stress scenarios
- Stress testing the portfolio against historical crashes (1987, 2008, 2020) with non-linear option payoffs
- Monitoring gamma exposure (GEX) and second-order Greeks (vanna, charm) for large positions

## When NOT to Use

<!-- QUICK: 30s -->

- Selecting an options strategy (iron condor vs vertical spread) — use **options-strategist**
- Computing individual option Greeks or IV surfaces — use **quantitative-analyst**
- Executing orders or connecting to broker APIs — use **algorithmic-trader**
- Pricing exotic options or implementing stochastic vol models — use **quantitative-analyst**
- Resolving equity signal conflicts or position sizing for stocks — use **portfolio-signal-manager**
- Portfolio construction for non-options assets — use **portfolio-signal-manager**

## Best Practices

<!-- STANDARD: 3min -->

1. Normalize all Greeks to portfolio NAV — a $50K delta on a $100K portfolio (50%) is very different from $50K on a $1M portfolio (5%)
2. Compute GEX at multiple underlying levels (±1%, ±2%, ±5%) — gamma at spot tells you nothing about gamma after a move
3. Run pin risk detection daily starting at 7 DTE, hourly at 3 DTE, and continuously on expiration day
4. Always verify margin against broker API before trade entry — computed margin and broker margin can diverge
5. Test every hedge in correlation→1.0 scenario — if the hedge fails when everything crashes together, it's not a real hedge
6. Track theta decay as % of NAV daily — theta should be positive (you collect premium) unless you're hedged long
7. Keep a "risk event log" — every margin call, assignment, or gamma event gets documented with root cause
8. Diversify expiration dates — all options expiring same week creates correlated gamma risk
9. Never let any single ticker's notional exposure exceed 10% of NAV — option notional, not premium, is the true exposure
10. Run full stress tests monthly and after any position that changes portfolio risk by >20%

## Error Decoder

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| Margin requirement jumps 3x overnight | Expiration approaching — short options near expiration have higher margin due to increased gamma risk and assignment probability | Roll positions to >21 DTE before margin acceleration begins (typically at 10 DTE). Brokers increase margin on short options exponentially in final week |
| Portfolio delta is "neutral" but P&L swings wildly | Delta neutrality at current spot hides large gamma — a 2% move changes delta by $20K+. You are not delta neutral — you are gamma exposed | Compute delta across ±3% range. If delta range exceeds 2% of NAV, you have a gamma problem, not a delta problem. Add delta-hedging schedule or reduce gamma exposure |
| Hedge didn't work during crash | Correlation breakdown — the hedge instrument and portfolio moved together in normal times but diverged during stress. Index puts on SPY don't protect a tech-heavy portfolio when QQQ drops 2x SPY | Diversify hedges across multiple instruments. Beta-weight the hedge to actual portfolio composition. Test hedge effectiveness in sector-specific crash scenarios, not just broad market declines |
| Theta decay is positive but portfolio loses money | Vega is highly negative — you're short options, collecting theta, but vol expansion is costing more than theta earns. Net P&L = theta gain + vega loss (±gamma, delta) | Monitor vega/theta ratio. If vega > 3× daily theta, a 1-point IV increase costs 3 days of theta. In rising vol environments, reduce short vega exposure or add long vega positions |
| Assignment happened on a "barely ITM" option | Dividend arbitrage — the option's time premium was less than the upcoming dividend, making early exercise optimal for the holder | Check ex-div dates for all short call positions. If dividend > remaining time premium, expect assignment day before ex-div. Close or roll before this happens |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| ❌ **Summing individual Greeks for portfolio view** | Greeks don't add linearly when positions have different expirations, different underlyings, or correlated movements. 5 AAPL calls + 5 AAPL puts with different strikes = not zero gamma | ✅ Compute Greeks from the aggregate payoff function across all strikes and expirations. Use scenario analysis: what is P&L at ±1%, ±2%, ±5% moves? The shape of that curve IS your portfolio risk |
| ❌ **Using one margin regime for all calculations** | "I'm on Portfolio Margin so Reg T doesn't matter" — but PM rules can change overnight. Brokers can increase PM requirements during high volatility without notice. Reg T is the statutory floor | ✅ Always compute both Reg T and PM. Use PM for capital efficiency but maintain Reg T awareness as the fallback. If broker tightens PM during a crisis, you need to know your Reg T margin requirement |
| ❌ **Ignoring expiration concentration** | Three different tickers with options all expiring same Friday = gamma event cluster. If the market moves sharply that week, all three positions experience gamma explosion simultaneously | ✅ Spread expirations across at least 3 different weeks. No more than 30% of positions expiring any single week. Track "gamma-at-expiration" as a separate risk metric |
| ❌ **Hedging tail risk with OTM puts and forgetting to roll** | OTM puts decay to zero — theta is working against the hedge. A 60-DTE 20% OTM put loses 60% of its value in the first 30 days. By the time the crash comes, the "hedge" is worth pennies | ✅ Roll tail hedges at 30 DTE. Budget 2-4% of NAV annually for hedge cost. If you can't afford the premium bleed, use put spreads or VIX calls instead — cheaper but with capped protection |
| ❌ **Trusting bid-ask midpoint for illiquid options** | A $0.10 bid / $0.90 ask with $0.50 mid implies a position that costs $0.40 to enter AND $0.40 to exit — 80% round-trip cost. But the midprice is just a convention, not a tradeable price | ✅ Always compute slippage: use bid for sells, ask for buys. If spread > 10% of mid, the option is effectively untradeable at size. Position sizing must account for round-trip slippage cost |

## State Log

<!-- STANDARD: 3min -->

| State Field | Type | Persists Across | Description |
|---|---|---|---|
| `greeks.portfolio` | PortfolioGreeks | Realtime | Net delta, gamma, theta, vega, vanna, charm — all normalized to NAV |
| `greeks.gex_profile` | GEXProfile | Realtime | Gamma exposure at spot and at ±1%, ±2%, ±5% underlying moves |
| `greeks.limits` | GreekLimits | Session | Configurable thresholds: max_net_delta_pct, max_gamma_pct, max_vega_pct, min_theta |
| `margin.current` | MarginSnapshot | Session → Daily | Current margin under Reg T, PM, and (if applicable) SPAN |
| `margin.utilization` | float | Realtime | Margin_used / margin_limit — triggers alerts at 50%, 70%, 85% |
| `margin.call_risk` | CallRisk | Realtime | Estimated margin call trigger distance: how much adverse move until margin call |
| `expiration.calendar` | [ExpirationEvent] | Session | All positions with expiration within 21 days, grouped by date |
| `expiration.pin_risk` | [PinRiskAlert] | Realtime | Positions where short strike is within 0.5% of spot with DTE ≤ 5 |
| `assignment.monitor` | [AssignmentRisk] | Realtime | ITM short options with assignment probability estimates |
| `hedge.positions` | [HedgePosition] | Session | Active hedges: type, cost, protection level, roll schedule |
| `hedge.effectiveness` | HedgeScore | Daily | Measured hedge performance: actual protection vs theoretical during recent moves |
| `concentration.expiration` | ExpConcentration | Session | % of positions expiring each week — max 30% per week rule |
| `concentration.ticker` | [TickerExposure] | Session | Notional exposure per ticker as % of NAV — max 10% per ticker rule |
| `concentration.sector` | [SectorExposure] | Session | Sector exposure considering options notional and equity positions |
| `liquidity.spreads` | [SpreadSnapshot] | Realtime | Bid-ask spreads for all positions; flagged if >10% of mid |
| `liquidity.oi_exposure` | [OIExposure] | Session | Position size relative to open interest; flagged if >10% of OI |
| `event.calendar` | [EventRisk] | Session | Upcoming earnings, FDA, FOMC, merger votes affecting held tickers |
| `stress.scenarios` | [StressResult] | Session → Archive | Results of latest stress test: P&L per scenario, max drawdown, margin call trigger |
| `risk.vaR` | VaRResult | Daily | 1-day VaR(95%, 99%), CVaR(95%, 99%) computed with non-linear payoff handling |
| `risk.max_drawdown_est` | float | Session | Estimated maximum drawdown in next 30 days based on current Greeks and IV |

## Core Workflow

### Phase 0: Portfolio Greek Snapshot (5min)

1. **Aggregate all Greeks** from quantitative-analyst output per position. Compute net Delta, Gamma, Theta, Vega, Vanna, Charm. Normalize to NAV. Profile GEX at ±1%, ±2%, ±5% underlying moves.
2. **Enforce Greek limits**: Net Delta ±50% NAV, Net Gamma ±5% NAV/1%, Net Vega ±5% NAV/1pt IV, Min Theta (positive preferred).
3. Complete when: All portfolio Greeks computed [COMPUTED] with NAV normalization. Greek limits checked. GEX profile charted.
   - Full formulas and examples → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-0-portfolio-greek-snapshot--full-detail)

### Phase 1: Pin Risk & Assignment Detection (5min)

1. **Compute Pin Risk Score** for all short options with DTE ≤ 7: `distance_component × dte_multiplier × position_factor`. Score ≥60 = close/roll immediately. Score 40-59 = close at next opportunity.
2. **Check assignment triggers**: Dividend arbitrage on calls, deep ITM puts with <$0.05 time premium, ITM >$2.00 near expiration. Apply pre-close rules.
3. Complete when: All short options ≤5 DTE scored. ITM shorts have assignment probability [ESTIMATED] with error bounds. Pre-close recommendations for scores ≥40.
   - Full scoring matrices and triggers → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-1-pin-risk--assignment-detection--full-detail)

### Phase 2: Expiration Risk Management (3min)

1. **Classify positions by DTE zone**: >21 (normal), 14-21 (plan), 7-14 (gamma acceleration), 3-7 (active), 0-3 (critical), 0 DTE (continuous). Apply DTE-appropriate actions.
2. **Classify by settlement type**: Physical delivery (most equity) vs cash-settled (SPX/NDX/VIX). Apply Friday expiration protocol. Enforce 0DTE rules (max 2% NAV, continuous monitoring, hard stops).
3. Complete when: DTE calendar populated. Settlement classification complete. All ≤3 DTE positions have close/roll/expire decision documented.
   - Full DTE rules, settlement guide, 0DTE rules → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-2-expiration-risk-management--full-detail)

### Phase 3: Margin & Capital Efficiency (5min)

1. **Detect margin regime**: Reg T (standard), Portfolio Margin (≥$110K), SPAN (futures). Compute margin per strategy. Calculate margin call distance = (NAV - maintenance) / NAV.
2. **Compute Buying Power Reduction**: BPR = margin_required / buying_power_total. Green <30%, Yellow 30-50%, Orange 50-70%, Red >70%.
3. Complete when: Margin computed [COMPUTED] and verified [BROKER-VERIFIED]. Margin call distance known. BPR known. For PM: stress scenarios simulated.
   - Full margin tables, formulas, examples → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-3-margin--capital-efficiency--full-detail)

### Phase 4: Liquidity & Slippage Assessment (3min)

1. **Score liquidity** per position: bid-ask spread (% of mid), open interest, position size vs OI. Estimate entry/exit slippage [ESTIMATED].
2. **Enforce position size caps**: `min(Kelly_vol_size, 5% of 20d dollar volume, 5% of OI)`. Flag illiquid positions (spread >10% or OI <100) — DO NOT TRADE.
3. Complete when: Liquidity score per position. Slippage estimated [ESTIMATED]. Positions adjusted for OI limits. Illiquid positions flagged.
   - Full scoring matrices, slippage tables → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-4-liquidity--slippage--full-detail)

### Phase 5: Options as Hedging Instruments (5min)

1. **Match hedge to risk**: Single-stock downside → protective puts/collars. Portfolio decline → index puts. Tail risk → deep OTM puts/VIX calls. Calculate annual hedge cost as % NAV.
2. **Evaluate delta hedging**: Hedge when net delta > ±50% NAV. Choose frequency (daily/weekly/threshold) and instrument (shares/futures/options).
3. Complete when: Hedge strategy selected and sized. Annual cost quantified [COMPUTED]. Delta hedging frequency determined.
   - Full hedge comparison, cost examples, delta hedge guide → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-5-options-as-hedging-instruments--full-detail)

### Phase 6: Correlation & Concentration Risk (3min)

1. **Compute ticker-level notional**: Sum long + |short| option notional + stock value per ticker. Limit: <10% NAV per ticker.
2. **Check concentration**: Expiration week (<30% of positions), sector (<25% NAV). Simulate crash correlation (r → 1.0) — VaR increases 2-3×.
3. Complete when: Ticker notional computed. Expiration and sector concentration checked. Crash correlation scenario simulated.
   - Full concentration rules, crash correlation analysis → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-6-correlation--concentration--full-detail)

### Phase 7: Event Risk Assessment (3min)

1. **Map event calendar**: Earnings (±10 days), FDA decisions, FOMC, merger close dates. For each event on positions >2% NAV: compute implied move (straddle price / underlying) and event P&L impact = delta + gamma + vega + theta.
2. **Apply event responses**: Earnings >15% NAV → close/hedge. FDA on any position >2% NAV → close. FOMC → cut delta 50%, close short gamma.
3. Complete when: Event calendar populated. P&L impact computed [COMPUTED] for all material events. Response actions documented.
   - Full event calendar, P&L formula, response matrix → [portfolio-risk-computations.md](references/portfolio-risk-computations.md#phase-7-event-risk-assessment--full-detail)

## Decision Trees

<!-- STANDARD: 3min -->

### DT1: Should I Close This Position Before Expiration?

```
DTE ≤ 5?
├── NO → Normal monitoring. Revisit at 7 DTE.
└── YES → Short option?
    ├── NO (long) → ITM? YES+cash→let expire | YES-capital→close | NO→expires worthless (roll if tail hedge)
    └── YES (short) → Within 1% of strike?
        ├── YES → Pin Risk ≥60? YES→close market | NO→close limit, market if unfilled
        └── NO → ITM? NO→alert at strike-1% | YES→cash-settled? let expire | physical? want stock? YES→accept | NO→close 3PM Fri
```

### DT2: Margin Call Risk — Immediate Action Required

```
Margin utilization?
├── <50% → Normal.
├── 50-70% → Caution. Rank positions for liquidation priority.
├── 70-85% → Prepare plan. Close expensive low-benefit positions. No new positions.
└── >85% → IMMINENT CALL. PM available? YES→switch to PM (20-50% relief) | NO→LIQUIDATE:
    DTE<7 first → naked shorts → concentrated ticker → all >5% NAV until <50%.
    Call distance: <2% move=critical | 2-5%=dangerous | 5-10%=manageable | >10%=comfortable
```

### DT3: Is My Hedge Working?

```
Hedge appreciated vs expected (0.8 × hedge_delta × portfolio_decline)?
├── >0.8× → WORKING. Maintain. Rebalance if delta drift >20%.
├── 0.3-0.8× → PARTIAL. Diagnose: correlation breakdown? vol regime change? theta decay? Adjust.
└── <0.3× → FAILURE. Post-mortem: correlation→1.0 event? too far OTM? Document and fix.
```

### DT4: Volatility Regime — Should I Change Risk Limits?

```
VIX level?
├── <15 (Complacent) → Reduce short vega. Buy tail hedges (cheap). Normal sizing.
├── 15-25 (Normal) → Standard limits. Monitor VIX term structure.
├── 25-35 (Elevated) → Reduce size 30%. Tighten stops. Buffer >50%.
└── >35 (Extreme) → HALT new positions. Close DTE<7. Delta→near-zero. >50→consider cash.

### DT5: Which Margin Regime?

```
Account equity?
├── <$110K → Reg T only. Defined-risk strategies preferred.
├── ≥$110K, PM enabled → Use PM. Compare PM vs RegT: PM<70% RegT=good relief | >90%=doesn't help
├── ≥$110K, PM not enabled → Request PM. Use Reg T until approved.
└── Futures account → SPAN (16 scenarios). Cross-margining with futures.
```

## Cross-Skill Coordination

### Upstream (Data In)

| Skill | Receives | Triggers |
|---|---|---|
| `quantitative-analyst` | Individual option Greeks, IV surface, UOA alerts | PUSH: Greek update, IV surface change. PULL: requestRepricing → stress testing |
| `options-strategist` | Strategy recommendations with strikes/expirations/sizes | PUSH: New/adjustment rec. PULL: requestRiskCheck before finalizing |
| `market-data-engineer` | Prices, chains, corporate actions, earnings, data quality | PUSH: Price/corp action/earnings/data degradation. React per Phase 7 |
| `portfolio-signal-manager` | Equity portfolio, sector exposure, correlation matrix, drawdown | PUSH: Rebalance signal, drawdown alert. PULL: requestPortfolioState |

### Downstream (Risk Out)

| Skill | Sends | Triggers |
|---|---|---|
| `algorithmic-trader` | Close/roll orders, hedge trades, liquidation orders | PUSH: Pin risk≥60, delta drift>limit, margin call imminent |
| `options-strategist` | Risk constraints: max notional, margin budget, concentration limits | PUSH: Updated risk budget, limit breach |
| `portfolio-signal-manager` | Combined equity+options risk: notional, sector, VaR/CVaR, hedge score | PUSH: Risk snapshot, hedge effectiveness report |

### Escalation

```
LOW (near threshold) → Log + flag report
MODERATE (pin 40-59, margin>60%) → Notify portfolio-signal-manager
HIGH (pin≥60, margin call<5%, event risk>15% NAV) → Close/roll to algorithmic-trader. Notify human.
CRITICAL (call imminent, hedge failure, liquidation) → Liquidate per priority. Halt trading. Post-mortem required.
```

### Communication Contract

Every inter-skill message: `{message_id, source_skill, target_skill, message_type, timestamp, correlation_id, payload: {risk_level, risk_numbers: [{value, unit, description, provenance}, ...], recommended_action, urgency}, expected_response_type, timeout_seconds}`

## Production Checklist

<!-- STANDARD: 3min -->

Before deploying options-risk-engineer with live positions:

- [ ] **CR1: Greek computation validated against broker Greeks.** Compute portfolio Greeks independently, then compare against broker-provided Greeks. Discrepancy >5% requires investigation. Brokers compute Greeks with proprietary models that may differ from standard Black-Scholes.
- [ ] **CR2: Margin computation verified against broker API for every strategy type in the portfolio.** Short naked put, iron condor, calendar spread — each strategy's margin must be verified independently. One wrong margin calculation causes forced liquidation.
- [ ] **CR3: Pin risk detection tested on 20+ historical expiration events.** Backtest: would the system have flagged the pin risk before it caused problems? False negative rate must be <5%.
- [ ] **CR4: Assignment risk model calibrated against historical early-exercise data.** Dividend-capture assignment predictions verified against actual early assignments. If model predicted 85% and actual was 40%, recalibrate.
- [ ] **CR5: Expiration calendar populated and accurate for all positions.** Missed expiration dates are catastrophic. Verify against exchange calendars (not all Fridays are expiration — triple witching, holidays).
- [ ] **CR6: Stress tests run on ACTUAL portfolio, not hypothetical.** Each stress scenario must reprice every position at stressed underlying levels. No shortcuts.
- [ ] **CR7: VaR backtested — actual daily losses compared to VaR predictions.** If VaR(95%) is exceeded on more than 5% of days, the model is wrong. Recalibrate.
- [ ] **CR8: Liquidity scores updated weekly.** Open interest and volume change. A liquid option last month may be illiquid today.
- [ ] **CR9: Event calendar synced daily.** Earnings dates change. FDA decision dates are announced. FOMC schedule is published quarterly.
- [ ] **CR10: Hedge effectiveness measured monthly.** Is the hedge actually reducing drawdowns? If a 3% NAV annual hedge cost reduces max drawdown by only 2%, the hedge is not cost-effective.
- [ ] **CR11: All risk alerts tested end-to-end.** Pin risk alert → notification received within 5 minutes. Margin call warning → liquidation plan triggered. Test with simulated events.
- [ ] **CR12: Anti-hallucination guardrails verified.** Every risk number in output carries [COMPUTED], [BROKER-VERIFIED], or [ESTIMATED] tag. Spot-check 20 numbers — all must have provenance.

## Error Recovery

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Portfolio Greeks show delta neutral but P&L swings $5K on a 1% move | Gamma is large and being ignored. Delta neutrality at one point means nothing when gamma is $500/1% — a 2% move changes delta by $1,000, creating a $2,000 delta exposure that wasn't there before | Report GEX range (gamma at ±1%, ±2%, ±5%) alongside point-in-time delta. If gamma range exceeds 2% of NAV, you are not delta neutral — you are gamma exposed. Either delta-hedge more frequently or reduce gamma | **Delta neutrality is a snapshot, not a state.** Gamma determines how long delta neutrality lasts. A "neutral" portfolio with high gamma is neutral for minutes, not days |
| Margin computed as $35K but broker shows $52K | Broker uses a different stress scenario or adds a concentration charge. PM brokers add margin add-ons for concentrated positions, illiquid options, or positions > certain % of OI | Query broker margin API directly. Never assume your calculation matches the broker's. Flag discrepancy >10% for investigation. Maintain margin buffer >20% above computed margin to absorb these surprises | **Broker margin is authoritative, not your calculation.** Your [COMPUTED] margin is educational; the broker's margin determines whether you get a call. Always verify |
| Pin risk score was 35 but option still got assigned | Distance-to-strike was 0.8% but the stock moved 1.2% in the final hour of expiration day. Pin risk scoring based on morning prices missed the afternoon move | Update pin risk scores hourly on expiration day. At 3:00 PM ET, if any short strike is within 1% of spot, close immediately regardless of score. The final hour can move any stock 1%+ | **Pin risk is a dynamic condition, not a morning calculation.** On expiration day, the only safe position is no position |
| Tail hedge cost 3% of NAV annually but provided zero protection in a 15% drawdown | Hedge was 25% OTM puts — market only dropped 15%. Hedge didn't activate. The protection threshold was set too far out. The cost was spent with zero benefit | Set hedge activation at 10-15% OTM for practical protection. Yes, it costs more (4-6% annually). Either you want protection that works in realistic drawdowns, or you're buying lottery tickets, not hedges | **"Tail hedge" that never activates is a donation to options sellers.** If you can't afford a hedge that activates in a 15% drawdown, you can't afford tail risk — reduce portfolio risk instead |

## Proactive Triggers

<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---|---|---|
| Any position DTE drops below 7 | Activate daily (then hourly at 3 DTE) pin risk monitoring. Compute assignment probability if short option. Review close/roll decision. | Options gamma accelerates exponentially below 7 DTE. Risk changes faster than you think — a position that was "safe" at 10 DTE is dangerous at 5 DTE |
| Portfolio net delta exceeds ±40% of NAV | Reduce delta to <40% by closing directional positions or adding delta hedge. If delta is intentional (directional bet), document thesis with stop-loss at -20% of NAV | Options amplify delta — a 40% NAV delta means a 5% market move changes portfolio value by 2% just from delta alone. Add gamma impact and the move is larger |
| VIX rises 10+ points in one week | Reduce ALL position sizes by 30%. Close positions with DTE < 7. Activate or increase tail hedges. Increase margin buffer to >50% unused | A 10-point VIX spike signals regime change. What was "normal" risk yesterday is "extreme" risk today. Reduce before the market forces reduction through margin calls |
| Two consecutive trading days with >3% portfolio loss | HALT new positions. Run full risk audit (all 8 phases). Identify: was this correlation risk? Gamma explosion? Vol expansion? Sector-specific? Fix the root cause before resuming | Consecutive large losses signal that something in the risk model is wrong. Continuing to trade through losses hoping they reverse is gambling, not risk management |
| Short option open interest shows >50% decline in one day | CHECK liquidity immediately. Large OI decline suggests position liquidation by a large player. If you're on the same side, exit may become difficult. If opposite side, pin risk may increase | OI changes precede liquidity changes. A sudden OI drop means someone big got out — the market for that option just got thinner |
| Broker announces margin requirement changes for options | Recompute ALL margin requirements immediately. The change may make previously acceptable positions now in violation. If margin increases >20%, reduce positions to maintain 30%+ buffer | Brokers change margin rules during volatility events. What was 20% margin yesterday may be 35% tomorrow. You find out when the margin call arrives — unless you proactively check |
| Earnings date announced less than 2 weeks out for a held ticker | Apply earnings risk protocol: reduce position by 50% OR purchase straddle to hedge. Do not hold short options through earnings on >5% NAV positions | Earnings are binary events with known dates. There is no excuse for being surprised by earnings risk. The only question is whether you chose to accept it |
| Any position's bid-ask spread widens >3× normal | HALT trading in this option. Investigate: is this a temporary condition (market open, news) or structural (declining OI, delisting risk)? If structural, plan exit NOW while some liquidity remains | Widening spreads are the market's early warning system. When spreads gap wider, market makers are signaling that risk has increased. Listen to the signal |

| Rationalization | Reality |
|---|---|
| "The option is only $0.50 ITM — it probably won't be assigned. I'll just wait." | ITM options near expiration have near-certain exercise. The OCC auto-exercises ALL options that are $0.01+ ITM at expiration unless the holder explicitly opts out. Your "probably won't" is the exact opposite of reality — it WILL be exercised. For American options, dividend arbitrageurs WILL exercise ITM calls the day before ex-div. The only question is whether YOU have a plan for the resulting stock position. **Cost: $10K-$100K in unwanted stock positions. A $0.50 ITM short call on a $250 stock delivers $25K of stock you might not own — creating a short position with unlimited risk.** |
| "I computed the margin at $15K. The broker showing $22K must be wrong — I'll trust my calculation." | Brokers add undocumented margin add-ons: concentration charges (your position >5% of OI), liquidity charges (spread >10% of mid), volatility risk premiums (VIX > 30), and house margin requirements above regulatory minimum. Your calculation is [COMPUTED]; the broker's margin determines whether you can hold the position. The broker is never "wrong" about their own margin requirement — they set it, they enforce it. **Cost: $25K-$500K in forced liquidations from "correct" margin calculations that don't match the broker's rules. Verify against broker API. Always.** |
| "I'll sell this put spread for $0.50 credit with $5 wide strikes. 10% return in 30 days — it's almost free money." | A $5-wide put spread collecting $0.50 has $4.50 at risk per $0.50 earned — a 9:1 risk/reward ratio. You need a 90% win rate just to break even. The "10% return" is return on margin, not return on risk. If the stock drops through both strikes (a 2-3 sigma event that happens 2-5% of the time per cycle), you lose 9× what you collected. Over 20 trades, probability says you lose money if win rate < 90%. Most "high probability" spreads have win rates of 80-85% — which means they lose money over time. **Cost: $4,500 per blown spread × 3-4 blow-ups per year = $13,500-$18,000 in losses that "shouldn't have happened." The market prices these spreads correctly — you are being compensated for tail risk, not collecting free money.** |
| "My portfolio has positive theta — I'm making money every day from time decay. The risk is minimal." | Positive theta means you're net short options (selling premium). Short options have NEGATIVE gamma and NEGATIVE vega — you lose money when the market moves (gamma) AND when volatility rises (vega). Positive theta is the premium you collect for accepting these risks. In a 2% market down day with VIX +5 points, your -$500/day theta position loses $3,000 in gamma + $2,400 in vega — 11 days of theta wiped out in one afternoon. **Cost: $5K-$50K in "theta farming" portfolios that collapse on volatility events. Theta is not free money — it's payment for accepting tail risk. If you don't understand what risk you're being paid to accept, you're the product, not the trader.** |
| "I bought protective puts — my portfolio is hedged. I can sleep well." | Protective puts hedge delta risk. They do NOT hedge: vega risk (if you're also short options), correlation breakdown (if puts are on SPY but portfolio is tech-heavy), gap risk (puts protect below strike; gap through strike overnight still loses), or theta decay (puts cost money every day). A 5% OTM put costs ~2% annually and only protects losses below 5%. If the market drops 4.9%, your hedge paid out ZERO. **Cost: $10K-$30K annually in put premium on a $500K portfolio with protection that doesn't activate in moderate drawdowns. Understand exactly what your hedge protects against — and what it doesn't.** |

## Gotchas

<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Net delta = $0 but portfolio lost $15K on a 3% up move | The portfolio was short gamma on the upside — delta went from 0 to -$12K as the market rose. The "delta neutral" portfolio became directionally short as it moved. Gamma asymmetry: long OTM calls have little gamma until they go ITM; short ATM options have high gamma always | Map the full delta profile across ±5% underlying moves. If delta changes by >2% of NAV per 1% move, you have a gamma problem. Reduce short gamma positions or delta-hedge dynamically with threshold-based rebalancing | **Delta neutrality is a point on a curve, not a line.** The curve's shape (gamma) determines whether "neutral" means anything. A portfolio with zero delta but high gamma is a spring-loaded trap — neutral until it moves, then aggressively directional |
| Margin requirement doubled overnight without any trading | Expiration week acceleration — short options 3-5 DTE have margin calculated with higher stress factors. Additionally, IV increased 3 points, raising short option margin. Combined effect: margin doubled | Track "projected margin at DTE=3" for all positions when they're at 14 DTE. If projected margin exceeds buffer, plan adjustments BEFORE the acceleration. Don't wait for the broker's margin increase — anticipate it | **Margin is dynamic, not static.** A position that uses $10K margin at 21 DTE may use $25K at 3 DTE. If you sized based on the 21-DTE margin, you're overextended at expiration |
| Bought 30% OTM SPY puts for crash protection. Market dropped 25%, puts only gained 60% of expected | Volatility skew changed — demand for OTM puts spiked, making them MORE expensive to buy (good for owners). But IV didn't rise as much as historical crashes because the decline was orderly (2022-style), not panicked (2020-style). Vega gain was less than modeled | Use VIX calls for panic-independent crash protection. Puts protect against price declines; VIX calls protect against panic. Different crashes have different vol responses. Diversify your tail hedges across instruments | **Tail hedges are regime-dependent.** A put hedge works best in panicked crashes (2008, 2020). In orderly declines (2022), VIX calls and put backspreads work better. One hedge does not fit all crashes |
| Assigned on a short call the day before a $1.50 dividend | The call's time premium ($0.08) was less than the dividend ($1.50). Exercising the call to capture the dividend yielded $1.42 in risk-free profit for the call holder. This was entirely predictable | Check every short call's ex-div date against expiration. If dividend > remaining time premium, assignment probability >85% [ESTIMATED]. Close or roll before the ex-div date. The market knows about dividends — option prices reflect it, but early exercise is path-dependent | **Dividends drive early assignment, not moneyness.** An OTM call won't be exercised for dividends. An ITM call will be exercised if the dividend exceeds the time premium. Track ex-div dates as carefully as expiration dates |
| Portfolio VaR(95%) = $8,500. Actual loss on a bad day = $31,000 | VaR was computed assuming normal distribution and linear instruments. Options have non-linear payoffs — a 3-sigma move causes 5-10× the loss that normal VaR predicts. The portfolio had short gamma and short vega — both amplify losses in extreme moves | Use historical simulation VaR with full option repricing. For portfolios with significant short gamma or short vega, report Stress VaR (worst case from historical scenarios) alongside statistical VaR. If Stress VaR > 3× statistical VaR, you have tail risk that statistical VaR misses | **VaR lies about options risk.** Normal-distribution VaR understates options portfolio risk by 30-60%. If you're managing options risk with standard VaR, you're driving with a speedometer that reads half of actual speed |
| Closed a pin-risk position at 3:55 PM ET with a limit order at mid. Order didn't fill. Assigned over the weekend | Market makers widen spreads in the final minutes of expiration day. A limit order at mid in a 0.30/1.20 market has near-zero fill probability. You "tried" to close but didn't actually close — the outcome is the same as not trying | For pin-risk closures on expiration day: use market orders after 3:30 PM ET. The slippage cost ($30-60 on a $0.30/1.20 spread) is less than the cost of assignment ($5K-$50K unwanted stock position). Accept the slippage as insurance cost | **"Trying to close" is not the same as closing.** In the final 30 minutes, fills are all that matter. A limit order that doesn't fill provides zero protection. Use market orders or accept assignment |

## Verification Guardrails

<!-- STANDARD: 3min -->

| Guard | Test | Failure Response |
|---|---|---|
| G1: PROVENANCE-REQUIRED | Every risk number in any output must carry [COMPUTED], [BROKER-VERIFIED], or [ESTIMATED ±X%]. Scan all numerical outputs before presenting to user. | "Risk output blocked: number '{value}' for '{metric}' missing provenance tag. Tag all risk numbers. Untagged risk numbers cause forced liquidations." |
| G2: MARGIN-DUAL-REGIME | Before any margin-dependent decision, compute margin under applicable regimes. For accounts >$110K, compute BOTH Reg T and PM. For futures options, compute SPAN. | "Margin decision blocked: only one regime computed. Compute Reg T = $X [COMPUTED] and Portfolio Margin = $Y [ESTIMATED] before proceeding. Single-regime margin is dangerous." |
| G3: GREEK-NORMALIZATION | All portfolio Greeks must be reported normalized to NAV (as % of portfolio value). Raw dollar Greeks without NAV context are rejected. | "Greek output blocked: Net Delta = $X reported without NAV normalization. Report as: Net Delta = $X [COMPUTED] (Y% of $Z NAV). Raw Greeks without context are noise." |
| G4: PIN-RISK-PRE-CLOSE | Any short option with DTE < 5 AND Pin Risk Score ≥ 40 must generate an explicit close/roll recommendation. "Monitor" is insufficient. | "Pin risk blocked: position {id} with score {score} and {dte} DTE requires explicit action (close or roll). 'Monitor' is not an acceptable response to elevated pin risk." |
| G5: EXPIRATION-CONCENTRATION | Before allowing any new position with same-week expiration that would push weekly concentration >30%, block and require expiration diversification. | "New position blocked: adding {ticker} {expiry} would increase {week} expiration concentration to {pct}% (>30% limit). Choose a different expiration week or close an existing position expiring that week." |
| G6: NOTIONAL-LIMIT | Before approving any position, verify notional_exposure / NAV ≤ 10%. Block if exceeded without explicit override. | "Position blocked: {ticker} notional exposure {pct}% exceeds 10% per-ticker limit. Reduce size to {max_contracts} contracts or override with documented rationale and hard stop-loss." |
| G7: STRESS-TEST-MONTHLY | Portfolio must pass stress test acceptance criteria. If any historical scenario produces drawdown >40% or triggers margin call, flag as UNACCEPTABLE. | "Stress test FAILED: {scenario} produces {pct}% drawdown (>40% limit). Reduce short gamma, add protective hedges, or decrease leverage until all scenarios pass. Do not deploy with failing stress tests." |
| G8: HEDGE-EFFECTIVENESS | After any market decline >3%, measure hedge performance. If hedge provided <30% of expected protection, flag hedge effectiveness failure. | "Hedge effectiveness FAILED: {hedge_type} provided {actual_pct}% protection vs {expected_pct}% expected. Diagnose: correlation breakdown, vol regime change, or strike distance issue. Reconfigure hedge before next decline." |

## What Good Looks Like

- **Every risk number traceable to source:** Audit trail from position-level Greeks → portfolio aggregation → provenance tag
- **Never surprised by gamma:** GEX profile known at ±1%/±2%/±5% moves before they happen
- **Pin risk detected early:** 7 DTE monitoring, 3 DTE hourly updates, nothing near short strike at 3PM expiration day
- **Margin known, not discovered:** Both Reg T and PM computed pre-trade. Projected DTE=3 margin known at DTE=30. Call distance monitored continuously
- **Hedges tested before needed:** Every hedge stress-tested in correlation→1.0 scenario. Effectiveness measured after >3% declines
- **Stress tests use real option repricing:** Full Greek recalculation per scenario, not linear approximations
- **Liquidity priced into sizing:** No position >5% ADV or >5% OI. Exit feasibility confirmed before entry
- **Maximum daily loss answerable:** "What's the max this portfolio can lose in one day?" — dollar amount, confidence interval, scenario, recovery plan

## References

<!-- STANDARD: 3min -->

The following reference files are loaded on demand when deeper context is needed:

### Core Methodology References

| Reference | Path | Content |
|---|---|---|
| **Portfolio Greeks Aggregation** | [portfolio-greeks-aggregation.md](references/portfolio-greeks-aggregation.md) | Detailed methodology for aggregating individual position Greeks into portfolio-level metrics. GEX (Gamma Exposure) computation with dealer positioning analysis. Vanna and charm computation and interpretation. Greek limit setting framework. |
| **Pin Risk Detection** | [pin-risk-detection.md](references/pin-risk-detection.md) | Pin risk scoring algorithm with distance-to-strike and DTE acceleration factors. Assignment probability models for calls (dividend-driven) and puts (deep-ITM). Automatic pre-close rules with decision thresholds. Historical early exercise data for calibration. |
| **Margin Requirements** | [margin-requirements.md](references/margin-requirements.md) | Complete Reg T margin formulas for every options strategy type. Portfolio Margin stress test methodology. SPAN margin overview for futures options. Cross-margining opportunities. Broker-specific differences (IBKR, Schwab, TDA, Tastytrade). |
| **Expiration Management** | [expiration-management.md](references/expiration-management.md) | DTE-based action rules with gamma acceleration curves. ITM expiration handling for physical vs cash-settled options. Friday expiration protocol with timeline. 0DTE risk management with extreme gamma monitoring. |
| **Hedging with Options** | [hedging-with-options.md](references/hedging-with-options.md) | Protective put strike selection and rolling strategies. Collar construction (zero-cost, put-spread collar). Tail risk hedging (OTM puts, VIX calls, put backspreads). Delta hedging with dynamic rebalancing schedules and frequency optimization. Hedge cost budgeting. |
| **Correlation & Concentration** | [correlation-concentration.md](references/correlation-concentration.md) | Options-specific correlation risks (same underlying, same expiration, sector). Notional exposure aggregation across options + equity positions. Expiration concentration limits and gamma event clustering. Crash correlation analysis with →1.0 stress testing. |
| **Liquidity & Slippage** | [liquidity-slippage.md](references/liquidity-slippage.md) | Bid-ask spread analysis and round-trip cost estimation. Open interest-based position sizing limits. Slippage estimation for market vs limit orders at different liquidity tiers. Fill probability modeling for illiquid options. |
| **Stress Testing & Tail Risk** | [stress-testing-tail-risk.md](references/stress-testing-tail-risk.md) | Historical scenario definitions (1987, 2008, 2020, 2022, 2018 volmageddon, flash crash). Option repricing methodology for stress scenarios. VaR/CVaR computation with non-linear payoff handling. Monte Carlo max drawdown estimation. Stress test acceptance criteria. |

### Related Skills

| Skill | Relationship | When to Invoke |
|---|---|---|
| `options-strategist` | Upstream — provides strategy recommendations this skill validates for risk | When designing new options positions or adjusting existing ones |
| `quantitative-analyst` | Upstream — provides individual option Greeks and IV surfaces for risk computation | When computing portfolio Greeks, repricing options for stress tests, or analyzing vol surface changes |
| `market-data-engineer` | Upstream — provides real-time prices, options chains, corporate actions, earnings dates | When risk computations need current market data or corporate action adjustments |
| `portfolio-signal-manager` | Peer/Lateral — provides equity portfolio context for combined risk assessment | When options risk needs equity context or when combined equity+options risk must be assessed |
| `algorithmic-trader` | Downstream — executes close/roll orders, hedge adjustments, and liquidation orders | When risk decisions require trade execution (pin risk close, margin reduction, hedge rebalancing) |
| `financial-security` | Reference — security review of risk management processes | Before deploying automated risk management with real money |
| `incident-responder` | Reference — incident response for trading failures | When margin calls, forced liquidations, or risk model failures occur |
| `observability-engineer` | Reference — risk monitoring dashboards and alerts | When setting up real-time risk monitoring infrastructure |
| `data-scientist` | Reference — backtesting risk models and calibrating parameters | When validating risk model accuracy or calibrating assignment probability models |

## Deliberate Practice

<!-- STANDARD: 3min -->

1. **Greek Aggregation Drill:** Take a 5-position options portfolio. Compute net delta, gamma, theta, vega by hand (or script). Then compute GEX at ±1%, ±2%, ±5%. Verify: does net gamma at spot differ from gamma at ±2%? By how much?
2. **Pin Risk Simulation:** Pick 10 historical expiration Fridays. For each, identify which short options would have been within 1% of spot at 3:00 PM. Would the pin risk scoring system have flagged them at 7 DTE? At 3 DTE? On expiration day morning?
3. **Margin Comparison:** Take 5 different strategy types (naked put, iron condor, calendar spread, covered call, short strangle). Compute Reg T margin for each. If Portfolio Margin eligible, compute PM margin. What's the PM/Reg T ratio for each? Which strategies benefit most from PM?
4. **Stress Test Your Own Portfolio:** Run your actual portfolio (or a simulated one) through the 6 stress scenarios. Does any scenario trigger a margin call? Produce >40% drawdown? What's the single change that would most reduce worst-case scenario loss?
5. **Hedge Effectiveness Audit:** Track your tail hedges for 3 months. How much did they cost? How much protection did they actually provide during drawdowns? Was the cost worth the protection? If not, redesign the hedge.
6. **Assignment Risk Backtest:** Find 20 historical instances of early assignment (dividend-capture on calls, deep-ITM puts). Would the assignment risk detection algorithm have flagged them? What was the false negative rate?
7. **Liquidity Failure Drill:** Pick an illiquid option in your portfolio (spread >10%). Simulate needing to exit the entire position in one day. What's the estimated slippage? Could you actually exit? If not, why is the position this size?
8. **0DTE Gamma Experience:** On an expiration Friday (paper trading only), track an ATM option in the final hour. Watch gamma explode as DTE→0. Map the delta change per $0.10 underlying move. This visceral experience teaches more than any formula.

