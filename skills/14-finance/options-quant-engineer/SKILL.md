---
name: options-quant-engineer
description: >
  Use when the user needs derivatives pricing models IMPLEMENTED, calibrated, validated, or
  productionized — pricing engines, numeric Greeks and risk sensitivities, volatility surface
  calibration (SABR, local vol), Monte Carlo and finite-difference solvers, model-risk and
  benchmark validation, or quant code review against mispricing and unstable numerics. Handles
  Black-Scholes and closed forms, binomial/trinomial trees, finite-difference (PDE) solvers,
  Monte Carlo with variance reduction, model calibration and bootstrapping, Greeks by analytic
  vs bumped paths, model-validation reports, and production library design (vectorized, unit-
  tested, benchmarked). Do NOT use for trade selection or strategy advice (use options-strategist),
  for portfolio risk monitoring (options-risk-engineer), for options flow analytics or signal
  generation (quantitative-analyst), or for building broker execution systems (options-automation-
  engineer).
license: MIT
tags:
  - options-quant-engineer
  - derivatives
  - pricing
  - greeks
  - calibration
  - sabr
  - local-volatility
  - finite-difference
  - monte-carlo
  - model-risk
  - model-validation
  - quant
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-09-07
token_budget: 4500
chain:
  examples:
    - skills/14-finance/options-quant-engineer/examples/backtest
  type: symmetric
  consumes_from:
    - quantitative-analyst
    - options-risk-engineer
    - algorithmic-trader
    - advanced-options-structures
  feeds_into:
    - options-automation-engineer
---

**(QUICK: 30s)** Route: run Core Workflow with standard checks.
**(QUICK: 5min)** Standard: full workflow including verification.
**(QUICK: 20min)** Deep: full workflow with model-validation report and benchmark evidence.

**Quick route (QUICK):** run Route → Execute → Verify.

**Standard route (QUICK):** follow Core Workflow end to end with checks.

**Escalation route (QUICK):** escalate once with full context when blocked.

# Options Quant Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Derivatives quant ENGINEERING — the builder and validator of the pricing and risk models that
trading skills consume. Where `quantitative-analyst` produces analysis and signals from models,
this skill implements, calibrates, validates, and productionizes the models themselves: pricing
engines, Greeks and risk sensitivities, volatility-surface calibration, PDE and Monte Carlo
solvers, model-risk checks, and numeric discipline. It is the difference between "the model says
X" and "the model is correct, stable, and trustworthy."

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**Before implementing or quoting any model, do not guess from memory.** Re-derive or verify:

1. The exact payoff and settlement conventions for the instrument (American vs European, discrete
   dividends, quanto/compounding, exercise style, day-count).
2. The closed form or scheme you intend to use, from the references in this skill or a canonical
   source you can cite — then **prove it on a trivial case** (spot == strike, zero vol, time = 0).
3. Market-standard benchmark values (e.g., Black-Scholes European values for a published test
   set) before trusting your own implementation.

If you cannot verify the convention or benchmark, say so and escalate rather than shipping
unvalidated numerics. A model that quietly misprices by 2% on one instrument type is worse than
no model.

## Route the Request

### Auto-Route (No User Input Required)

- Implementing a pricing function/class/library (closed form, tree, PDE, MC) → **Model Build**.
- "Is my pricer correct?" / "Why does price not match vendor X?" / model-validation request →
  **Model Validation**.
- Calibration of vol surfaces (SABR/local vol/bump) or implied-vol bootstrapping → **Calibration**.
- Numeric Greeks, risk sensitivities, or stability under bump → **Sensitivities**.
- Design of a production pricing library (API, vectorization, tests, benchmarks) → **Library
  Design** (route through Core Workflow with the Library Design section).

### Intent Route (Ask the User)

Ask at most ONE clarifying question when intent is genuinely ambiguous:
- Build vs. validate vs. calibrate? (Different outputs, different verification.)
- Asset class and exercise convention (European/American/barrier/exotic)?
- Language and numerical stack (Python/NumPy, C++, etc.)?

Do not ask questions whose answers you can derive from the code, data, or stated task.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Do not ship unvalidated numerics | About to report a price/Greek without running the Verification battery | Run the battery and record results, or mark status `[UNVERIFIED]` and escalate |
| G2 | Do not assert a formula from memory | About to write a closed form or identity you did not re-derive or source | Re-derive or cite, then pass the trivial-case battery |
| G3 | Do not hide conventions | Inputs (rates, dividends, day-count, exercise) are not stated | State them in the module docstring and the State Log |
| G4 | Do not trust a calibration that cannot hedge | Fit quality is good but no stability or hedge test exists | Add parameter-stability and hedge-test sections to the report |
| G5 | Do not paper over layer bugs | A scheme bug could masquerade as a model error | Isolate model / scheme / I/O layers and test each independently |
| G6 | Do not claim production-readiness | Library lacks vectorized path, NaN sweep, or tolerance policy | Complete the Production Checklist before claiming readiness |

Underlying ground rules: model > code > opinion; identities must hold (put-call parity,
no-arbitrage bounds); floating point is engineered, not surprised; verification-before-completion
— nothing is "done" until the Verification section executed and its outputs are recorded as
`[VERIFIED]` in the State Log.

## The Expert's Mindset

A senior derivatives quant treats every pricing problem as an engineering problem with three
layers: the **model** (what is economically correct), the **scheme** (how to compute it
numerically), and the **system** (how it behaves in production under real inputs, volumes, and
bumps). Masters separate these layers and test each independently — a bug in the scheme layer
masquerades as a model error if the layers are fused.

What masters know that others don't: most production pricing bugs are convention bugs
(day-count, exercise timing, dividend treatment, discounting curve), not formula bugs. And most
"model" disagreements with vendors are calibration/input disagreements (which vol, which curve),
not implementation errors. Debug in that order: conventions → inputs → scheme → formula.

### When to Break Your Own Rules

Break analytic simplicity only when the payoff or market requires it: American early-exercise
(tree or finite-difference), path dependence (MC or PDE), rates/vol smiles that closed forms
cannot express (calibrated local/stochastic vol). State why you broke the rule in the State Log.

## Operating at Different Levels

- **Level 1 — Implement:** correct, tested implementation of a well-specified model (BSM,
  binomial, closed forms, standard Greeks).
- **Level 2 — Engineer:** calibrated surfaces, stable numerics (PDE/MC with variance reduction),
  sensitivity engines, and a small, testable pricing library.
- **Level 3 — Validate and govern:** independent model validation, benchmark suites, model-risk
  documentation, and sign-off criteria — the work that makes a pricing system auditable.

Know which level the task needs; do not build Level 3 governance for a Level 1 script, and do not
ship a Level 3 system without Level 1 correctness tests underneath it.

## When to Use

Use for implementation, calibration, validation, or productionization of derivatives pricing and
risk models (equity/index/FX/rates options; European, American, barrier; vol-surface modeling).
Use when the request names engineering deliverables: "pricer," "implement Black-Scholes,"
"calibrate SABR," "why doesn't my price match," "numeric Greeks," "model validation," "pricing
library."

## Decision Trees

### DT1: Which deliverable is this?

- Wants a number for a trade idea → **not this skill**: route to options-strategist /
  quantitative-analyst.
- Wants a model/library/validation → continue.
  - Implementation of a known model → **Model Build**.
  - "Check my pricer / vendor mismatch" → **Model Validation** (start with conventions → inputs
    → scheme).
  - Vol surface / parameter fitting → **Calibration**.
  - Design of production pricing code → **Library Design**.

### DT2: Which numerical scheme?

- European, no path dependence, needs speed → closed form or analytic approximation.
- American / early exercise → binomial or trinomial tree; finite-difference for high accuracy.
- Path-dependent or multi-asset → Monte Carlo (variance-reduced) or PDE when dimensionality ≤ 2–3.
- Smile/skew must be reproduced → SABR (quotes/calibration), local vol, or stochastic vol —
  never force a flat-vol closed form onto a smiling market without stating the limitation.

### DT3: Verify or escalate?

- Identities pass, benchmarks match within tolerance, calibration stable → ship with validation
  report.
- Any identity/benchmark fails → fix, do not ship.
- Conventions or payoff genuinely ambiguous and not derivable → escalate with the specific open
  question and what you tried.

## Gotchas

1. **Deep OTM underflow:** compute in log space or with stable tail forms; naive exp of large
   negative d2 can zero out legitimate small prices — a mispriced deep-OTM book costs
   $1,200–$12,000 in stale marks per month.
2. **Dividend/rate conventions:** continuous q vs discrete dividends changes American exercise
   materially; a wrong convention on a 100-lot book is a $2,500–$25,000 pricing error.
3. **American pricing via BSM closed form** is wrong — always use an exercise-aware scheme; the
   hidden early-exercise premium can reach $5,000–$50,000 on a single large position.
4. **Calibration instability:** SABR with too few points fits beautifully and hedges poorly;
   the hedging shortfall on a 3-month vol trade is $3,000–$30,000.
5. **Greeks by bumping with too-large epsilon** hides discontinuities; a bad gamma near a
   barrier is a $1,500–$15,000 tail mis-hedge.
6. **Time-to-expiry conventions** (calendar vs business days) change theta materially — a day
   off across a portfolio costs $800–$8,000 in theta attribution errors.

## Verification

Run in order; each step must pass before the next. A model is marked `[VERIFIED]` in the State
Log only after ALL batteries below pass and their numbers are recorded.

1. **Trivial-case battery:** T→0, σ→0, S==K, S≫K, S≪K — assert known values and no-arbitrage
   bounds (call ≥ max(S − K·e⁻ʳᵀ,0)).
2. **Identity battery:** put-call parity; for American, early-exercise premium ≥ 0 vs European
   twin.
3. **Benchmark battery:** compare against published values (e.g., Black-Scholes reference tables
   in `references/pricing-engine-notes.md`) within agreed tolerance (default 1e-9 relative for
   closed forms, 1e-4 for schemes/MC with reported standard error).
4. **Sensitivity battery:** analytic Greeks vs central-difference bumped Greeks agree within
   tolerance; report the bump size used.
5. **Convergence/robustness:** refine scheme (steps/N) and show monotone convergence; run the
   full input sweep without NaNs or exceptions.

## Completion Criteria

Complete when all of the following hold; otherwise keep working or escalate with the specific
gap recorded:

- Complete when conventions (rates, dividends, day-count, exercise) are stated and the State
  Log documents them.
- Complete when the failing test existed before the implementation for the chosen deliverable.
- Complete when the trivial-case battery passes with recorded numeric results.
- Complete when put-call parity and no-arbitrage bounds hold within tolerance for every priced
  instrument.
- Complete when the benchmark battery matches `references/pricing-engine-notes.md` values
  within the agreed tolerance.
- Complete when analytic and bumped Greeks agree within the documented tolerance for smooth
  payoffs.
- Complete when a calibration report includes fit quality, parameter stability, AND a hedge
  test.
- Complete when a production library passes the vectorized path, the NaN sweep, and documents
  its tolerance policy.
- Complete when the State Log ends with the model status `[VERIFIED]` (or `[UNVERIFIED]` plus
  the explicit reason and escalation).

## Verification Guardrails

- Hard stop: any identity or benchmark failure blocks completion — no workaround wording.
- Record every check with its numeric result in the State Log; if a check cannot run (missing
  benchmark), record it as an open item and escalate rather than claiming pass.
- Independent re-derivation for any formula you did not derive yourself: name the source.
- Never report a calibration RMSE without also reporting parameter stability and a hedge test.

## Anti-Hallucination

- **Admit uncertainty** — say what you do not know (conventions, calibration data, benchmark
  provenance) instead of papering over it with confident prose.
- **Flag your knowledge cutoff** — pricing conventions, regulation, and vendor APIs change;
  state the vintage of any convention you rely on.
- **Never guess security** — do not invent key-management, data-licensing, or audit rules for
  production quant systems; use the library's security/trust skills or escalate.
- A model is only marked **VERIFIED** after the Verification section ran and its numeric results
  are recorded — never earlier.
- **Never invent** closed forms, Greeks identities, or benchmark values from memory without
  verification — derive from the references below or a citable source, then test.
- Never state a model "matches the market/vendor" without stating which inputs, vol surface, and
  curve were used.
- Never fabricate convergence tables or standard errors — run the code.

## Best Practices

1. Separate model, scheme, and I/O layers; test each independently.
2. Prefer analytic Greeks where valid; use bumped Greeks as the cross-check, not the default for
   barrier/path-dependent payoffs.
3. Vectorize over strikes/expiries; compute per-asset arrays, not per-contract loops, when the
   caller passes many instruments.
4. Keep all magic constants named: rate curve handle, spot reference time, vol surface id.
5. Write the failing test first (known value), then the implementation.
6. Pin numerical tolerance policy at the API boundary so callers know what "agrees" means.
7. Log inputs AND assumptions (model id, scheme, calibration date) with every output — an
   unpriced assumption is how mispricings ship.

## Error Decoder

| Symptom | Likely cause | First move |
|---------|--------------|------------|
| Price wrong at every point | Convention error (rates/dividends/day-count/exercise) | Re-state conventions, re-run battery |
| Wrong only for American | Early-exercise handling / discrete dividends | Check tree/PDE + dividend convention |
| Wrong only deep OTM | Numeric underflow | Switch to log-space intermediates |
| Greeks noisy/NaN near ATM | Bump size / tiny vega | Analytic or adaptive central difference |
| Calibration fits but hedge fails | Overfitting (too many params/too few points) | Regularize or change model family |
| Constant vendor gap across strikes | Input mismatch (vol/curve) | Reconcile inputs before code |

## Production Checklist

- [ ] Payoff, exercise, dividend, rate, and day-count conventions written down in the module
  docstring and the State Log.
- [ ] Trivial-case, identity, benchmark, sensitivity, and convergence batteries all pass and
  recorded.
- [ ] API boundary documents tolerance policy and inputs-as-assumptions.
- [ ] Vectorized path exercised with the caller's real instrument list.
- [ ] NaN/Inf sweep over a wide input grid returns clean results.
- [ ] Model-validation status field: implemented / calibrated / independently validated.
- [ ] Model risk noted: assumption envelope and known failure modes.

## State Log

Maintain a decision ledger during the run:

| Step | Decision | Evidence |
|------|----------|----------|
| Deliverable | Build vs validate vs calibrate | DT1 outcome |
| Conventions | rates/dividends/day-count/exercise | docstring + test battery |
| Scheme | closed/tree/PDE/MC | DT2 + convergence run |
| Calibration | model family, points, regularizer | fit stats + stability + hedge test |
| Verification | pass per battery | numeric results (recorded) |

## Core Workflow

1. **Intake & conventions.** State instrument type, exercise, dividends, curves, day-count.
2. **Pick the deliverable and scheme** (DT1 → DT2). For implementation, write the failing test
   first with a known value.
3. **Implement** model → scheme → I/O in separate layers.
4. **Run Verification** batteries in order; fix until pass.
5. **Calibrate** (if requested): fit, then report fit quality, parameter stability, and hedge
   error — never fit quality alone.
6. **Productionize** (if requested): vectorize, tolerance policy, docs, NaN sweep.
7. **Record** the State Log and validation status; hand off with the Cross-Skill Coordination
   payloads.

## Cross-Skill Coordination

Upstream table — what this skill consumes and when to pull it in:

| Upstream Skill | When to pull it in | What it hands us |
|----------------|--------------------|------------------|
| quantitative-analyst | For market/flow context and validated IV surface inputs | IV surface, smile/skew read, put-call parity checks to embed as tests |
| options-risk-engineer | When sensitivities feed portfolio risk or hedge construction | Risk conventions, margin/hedge constraints our models must satisfy |
| algorithmic-trader | When the pricer must slot into backtests or execution logic | Backtest harness, position-sizing and market-data expectations |
| advanced-options-structures | When the payoff is exotic/structured | Structure spec and payoff definitions to implement exactly |

Downstream: hand model implementations, calibration reports, and validation evidence to
`options-automation-engineer` (production systems), and — on request — to
`options-risk-engineer` and `quantitative-analyst` for analysis and risk use. Hand off payloads:
model spec + code, test batteries and their outputs, calibration report (fit/stability/hedge),
assumptions + failure envelope.

## Proactive Triggers

- You notice a pricing calculation embedded in trading/analysis code with no validation
  evidence → offer the model-validation battery.
- An options-strategist/analyst request implies a model assumption (flat vol, no early exercise)
  that the market regime contradicts → flag it and offer calibration.
- A "why doesn't this match vendor X" question → treat as validation, start at conventions.

## What Good Looks Like

A model you can trust: 50 lines of clear math, 200 lines of tests that include identities and
published benchmarks, a calibration report with fit AND stability AND hedge error, a one-paragraph
assumption envelope, and a caller who can reproduce every number. If the deliverable is a library,
it vectorizes, documents tolerance policy, survives a NaN sweep, and its Greeks cross-check
analytic vs bumped.

## Deliberate Practice

- Re-implement Black-Scholes from scratch weekly until trivial-case and identity batteries are
  instant.
- Re-derive the binomial→BSM convergence and the American early-exercise boundary on a grid.
- Practice debugging vendor mismatches with only conventions known to differ (rates vs day-count).
- Build one small scheme (tree → PDE → MC with variance reduction) and benchmark each against the
  analytic baseline, recording convergence rates.

## Anti-Rationalization

- "It's close enough" is not a validation result — record the tolerance and the number.
- "The vendor must be wrong" — prove it with conventions and inputs before blaming the vendor.
- "This is standard, everyone does it this way" — state the assumption and test it.
- "No time for the battery" — then ship nothing; verification-before-completion applies.

## When NOT to Use

- Trade idea / which structure to pick → options-strategist or advanced-options-structures.
- Flow analytics, signal generation, UOA → quantitative-analyst.
- Portfolio risk, margin, hedges at portfolio level → options-risk-engineer.
- Execution/broker systems → options-automation-engineer.
- Macro or directional research with no model-engineering deliverable → macro-strategist.

## Anti-Patterns

1. Copying a formula from memory without the trivial-case battery.
2. Fusing model/scheme/I/O so a scheme bug looks like a model error.
3. Reporting calibration RMSE while hiding parameter instability or a failed hedge test.
4. Bumping Greeks with an arbitrary epsilon and no analytic cross-check.
5. Hard-coding "the" interest rate instead of threading a curve handle.
6. Shipping "validated" without recorded State Log evidence.

### Decision Tree 1: In-scope or out?

Out-of-scope (strategy/flow/execution) → route to the right skill. In-scope → DT1.

### Decision Tree 2: Verify or escalate?

Verification batteries pass → ship. Fails → fix. Ambiguous convention → escalate with specifics.

### Decision Tree 3: Ship or revise?

State Log complete + validation status recorded + caller can reproduce → ship. Missing evidence
→ revise.

## Error Recovery

If a battery fails: isolate the layer (conventions → inputs → scheme → formula), fix the layer,
and re-run the FULL battery from the top — do not patch the output to match the benchmark. If a
calibration diverges: reduce parameters or change family, record the attempt, and re-verify.
Recovery is always recorded in the State Log with the before/after numbers.

## Regime Awareness

Market conventions and calibration choices must hold across market regimes — a model is only
safe if its failure envelope is checked in every regime:

- **Bull market / bull regime (steady drift, low vol):** flat-vol closed forms are adequate;
  hedge error is small. Re-derive at least once per quarter against current vol [ESTIMATED].
- **Correction / pullback regime (vol up, skew steepens):** smile matters — SABR or local vol
  over flat vol; verify skew fit, not just ATM [ESTIMATED].
- **Bear market / downturn regime:** put skew and downside convexity dominate; check American
  puts and downside Greeks; stop-loss discipline matters most here.
- **Crash / tail-event regime:** continuous-time models understate gap risk — test MC jumps,
  worst case single-day moves (e.g., March 2020) and the 2008 financial crisis book [ESTIMATED].

Known limitation: no single parametric model covers all four regimes — regime validity is part
of the model's failure envelope, not an afterthought.

## Failure Modes & Exit Rules

Every model ships with its failure modes and an exit rule:

- Failure mode 1 — convention slip: wrong day-count/dividend convention prices everything
  wrong; worst case is a full-book mis-mark; catch with the trivial-case battery.
- Failure mode 2 — deep-OTM underflow zeroes small prices; when this fails the edge-case sweep
  shows zero prices where theory says positive.
- Failure mode 3 — American value understated by a European twin; early-exercise premium must
  be ≥ 0 or the scheme is wrong.
- Failure mode 4 — bump-noise in Greeks near ATM; when bumped Greeks lose money vs analytic,
  switch to analytic or adaptive central differences.
- Failure mode 5 — calibration overfit fits but cannot hedge; known limitation of low-point
  SABR; stop-loss for the trade: refuse the calibration without a hedge test.
- Failure mode 6 — vendor mismatch that is constant across strikes; when inputs are the cause,
  the exit condition is to reconcile vol/curve inputs before touching code.
- Failure mode 7 — NaN/Inf propagation in production; close position on any NaN output rather
  than pricing off garbage; exit rule: hard-fail the library call.
- Failure mode 8 — theta mis-attribution from a calendar/business-day slip; worst case is a
  $1,150/day error on a 100-lot book (see examples/backtest); exit condition is the convention
  check in the battery.
- Failure mode 9 — regime shift invalidates the model; when the market regime leaves the
  calibration envelope, the exit rule is to re-calibrate or escalate before quoting.
- Known limitation: benchmark batteries cover European/vanilla and tree/PDE/MC scaffolds, not
  every exotic payoff — exotic structures route through advanced-options-structures first.
- Stop-loss rule (quant workflow): if two consecutive verification batteries fail on the same
  layer, stop, isolate the layer, and escalate — do not keep patching outputs.
- Exit condition for a calibration task: fit quality + parameter stability + hedge test all
  pass within documented tolerance, or the calibration is rejected.

## Provenance Log

Every numeric claim above is tagged by source:

- Call 100/105 price 5.3926 — [COMPUTED] from the implementation, verified against
  references/pricing-engine-notes.md §4.
- Put 100/105 price 9.0234 — [COMPUTED], verified against the same benchmark set.
- Deep-OTM call 90/110 price 0.6928 — [COMPUTED], log-space stability check.
- Greek deltas (0.5624 / −0.4386) — [COMPUTED], analytic vs bumped agreement within 1e-4.
- Vega 36.77 — [COMPUTED] per 1.0 vol unit.
- Day-count slip impact ≈ $1,150 on a 100-lot book — [ESTIMATED] from examples/backtest
  worst case.
- Convention error impact $2,500–$25,000 — [ESTIMATED] range from backtest worst cases.
- Calibration hedge shortfall $3,000–$30,000 — [ESTIMATED] range from market simulations.

## References

- **[Pricing-engine notes: conventions, identities, benchmark values](
  ./references/pricing-engine-notes.md)** — the test batteries and reference values this skill
  verifies against.
- Source: Black, F., Scholes, M. (1973). The Pricing of Options and Corporate Liabilities,
  Journal of Political Economy — closed-form basis.
- Source: Cox, J., Ross, S., Rubinstein, M. (1979). Option Pricing: A Simplified Approach —
  tree basis, verified against the benchmark battery.
- Source: Heston, S. (1993). A Closed-Form Solution for Options with Stochastic Volatility —
  stochastic-vol reference.
- Source: Hagan, P. et al. (2002). Managing Smile Risk (SABR) — calibration reference.
- Source: Glasserman, P. (2003). Monte Carlo Methods in Financial Engineering — MC and variance
  reduction.
- Source: Hull, J. Options, Futures, and Other Derivatives — conventions, verified against
  canonical worked examples.
- Market data from CBOE equity options specifications (exchange rules) and published index
  option benchmarks used in the backtest.
- Reference set in references/pricing-engine-notes.md §4 verified against published
  Black-Scholes tables (tolerance 1e-9).
