---
name: software-project-estimator
description: >
  Use when producing effort, duration, or cost estimates for software projects — from XS to
  XXL size classes — for quotes, bids, SOWs, or internal planning; when choosing a sizing
  method (t-shirt vs story points vs three-point vs reference-class); or when converting a
  scope description into a defensible effort range with a confidence band. Handles scope
  decomposition, size classification, velocity/rate calibration, estimate ranges
  (low/base/high), phase-level breakdown, assumptions registers, and estimation
  anti-patterns. Do NOT use for sprint-level backlog refinement (scrum-master), for
  client-facing price or rate cards (services-engagement-pricing), or for product roadmap
  prioritization (product-manager).
license: MIT
tags:
- estimation
- t-shirt-sizing
- story-points
- three-point
- reference-class
- sow
- quote
- effort
- cost-estimate
- xxs-xxl
author: Sandeep Kumar Penchala
type: operations
status: stable
version: 1.0.0
updated: 2026-09-09
token_budget: 4000
chain:
  examples:
  - skills/12-operations/software-project-estimator/examples/backtest
  consumes_from:
  - services-engagement-pricing
  - software-maintenance-support-estimator
  feeds_into:
  - services-engagement-pricing
  - software-maintenance-support-estimator
---
# Software Project Estimator
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Turn a scope description into a defensible effort/duration/cost estimate for software projects of any size class (XS→XXL), for quotes, bids, SOWs, and internal planning. The output is always a **range with an assumptions register** — a point estimate is a promise, and promises are how estimators get fired.

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce any estimate without completing this research.**

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify current scope reality.** Read the actual requirements, mockups, or codebase. Never estimate from a one-line ticket alone. | [CONTEXT_VIOLATION] Estimates are only as good as the decomposition; vague scope produces pretend precision. | Requirement docs, tickets, mockups, repo, ADRs |
| **RP2** | **Check the team's historical velocity/actuals.** What did the last 3–5 similar projects actually take? | [STALE_RISK] Industry benchmarks are anchors, not facts; your actuals beat generic data every time. | Sprint reports, timesheets, closed-project data |
| **RP3** | **Tag every figure [VERIFIED]/[COMPUTED]/[ESTIMATED]** and mark the basis (actuals vs benchmark vs guess). | [HALLUCINATION_GUARD] Untagged numbers are indistinguishable from invented ones. | This skill's references, docs/estimation-research.md |
| **RP4** | **List known failure modes** (integration, environment, 3rd-party, vague acceptance criteria) and where you've allowed for them. | [FAILURE_BLINDNESS] Optimism bias is the #1 killer; naming risks converts them from invisible to priced. | Postmortems, past project overruns |
| **RP5** | **Quantify with concrete units** — days/person, ranges, not "a few weeks". | [VAGUENESS_PENALTY] "~3 weeks" hides the spread; "12–18 engineer-days" is checkable later. | Past estimates vs actuals |
| **RP6** | **Map side effects** — who else consumes this estimate (pricing skill, maintenance skill, finance)? | [CASCADE_BLINDNESS] The estimate feeds a price and an annual support figure; errors compound downstream. | Cross-skill coordination table |

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

Estimation is not a single pass. At every fork (method choice, size class, contingency
percent, risk adjustment) re-verify the inputs behind that fork before committing the number.

## Anti-Hallucination

- Never output a point estimate ("this will cost $40K") without a range and basis. `[$35K–$52K],
  base-case basis: reference-class of 3 similar checkouts`.
- Never fabricate team velocity. If no actuals exist, say so and use benchmark ranges with a
  wider confidence band.
- Every assumption in the register must be traceable to an input or a stated default.
- If scope is one sentence and the ask is a fixed price, STOP: produce a discovery/options
  estimate instead, or refuse precision.

## Route the Request

### Auto-Route (No User Input Required)

- User asks "how long / how many days / how much effort for <project>" → this skill.
- User gives a size class and asks for effort → this skill (fast path via Decision Tree 1).
- User asks for a price to charge → route to `services-engagement-pricing` after estimating here.
- User asks about ongoing cost after launch → estimate here, then hand the build figure to
  `software-maintenance-support-estimator`.

### Intent Route (Ask the User)

If it is unclear, ask up to 3 questions: (1) planning altitude — roadmap budget or committed
quote? (2) do you have team velocity/actuals from similar work? (3) is there a hard deadline or
budget cap that changes the confidence framing?

## Ground Rules — Read Before Anything Else

1. **Always return a range** (low/base/high) plus a confidence band and the assumptions that
   would break it. Single numbers are only allowed as the "base" of a range.
2. **Decompose before you estimate.** Size the whole by sizing parts (epics → workstreams →
   known unknowns), never by gut on the whole.
3. **Never map story points to fixed hours.** Use velocity (points/delivered per period), and
   only for sprint altitude. For quote altitude use t-shirt or three-point day ranges.
4. **Apply contingency explicitly**, not silently: show risk adjustment as a line item.
5. **Publish the assumptions register** with every estimate; re-estimate when assumptions break
   (scope change trigger ≈15–20%, see Gotchas).
6. **Calibrate to actuals** every quarter: compare past estimates to reals and fold the error
   into the next default ranges.
7. **Say "I don't know" with a plan** when inputs are missing — a discovery estimate, not a fake
   precise one.

## The Expert's Mindset

### What Masters Know That Others Don't

- Precision is a liability early: the Cone of Uncertainty starts at ~±4×. Spend effort on
  *narrowing the cone* (spec, spike, prototype), not on fancier arithmetic on garbage inputs.
- Typical projects overrun **30–40%** and 60–80% overrun in some dimension — so a "base" that
  ignores that is not a base, it is a floor.
- Large items carry disproportionate uncertainty: error bars should widen, not scale linearly.
- The most accurate teams use **relative sizing + tracked actuals**; formal models add no proven
  accuracy advantage over expert judgment used well.
- Estimation is a communication artifact: it exists to make trade-offs discussable, not to be
  right to the decimal.

### When to Break Your Own Rules

- Fixed-fee clients need a *number*; give the base-plus-contingency number but keep the range in
  your working notes and the assumptions in the SOW.
- Tiny XS tasks (< 1 engineer-day) can be single-point — the band adds nothing.

## Operating at Different Levels

| Level | Altitude | Method | Output |
|---|---|---|---|
| L1 Apprentice | Ticket/sprint | Story points + velocity | Points, not hours |
| L2 Practitioner | Epic/feature | Three-point days per workstream | Low/base/high engineer-days |
| L3 Senior | Project quote | T-shirt per workstream + decomposition | Effort range + contingency |
| L4 Lead | Program / portfolio | Reference-class + Monte-Carlo-ish scenarios | Probabilistic band |
| L5 Transformative | Bid / SOW | Calibrated model + risk register + pricing handoff | Defensible estimate + assumptions |

## When to Use

| Use this skill | Instead use |
|---|---|
| "How much effort to build an MVP?" / SOW bid / budget request | `scrum-master` (sprint refinement only) |
| Sizing a feature backlog for a roadmap | `product-manager` |
| Pricing the estimate for a client | `services-engagement-pricing` |
| Estimating post-launch support cost | `software-maintenance-support-estimator` |
| Planning/sequencing an approved estimate | `project-manager`, `technical-program-manager` |

## Decision Trees

### Decision Tree 1: Choose the sizing method by planning altitude

| Situation | Method | Notes |
|---|---|---|
| Roadmap budget, no stories yet | T-shirt (XS–XXL) per epic/workstream | Fast; coarse; map XS=1…XXL=13 for totals |
| Sprint/iteration plan, stable team | Story points + velocity | Never convert points→hours directly |
| Client quote / SOW / fixed price | Three-point (PERT) engineer-days + explicit contingency | Widest assumptions register |
| Repeat of similar past projects | Reference-class forecasting | Anchor to 3+ actuals; adjust for deltas |
| Huge/uncertain program | Reference-class + scenario ranges | Publish P50/P80-style bands |

### Decision Tree 2: Size classification (XS → XXL)

Estimate by total base effort, then adjust for uncertainty:

| Class | Base effort | Typical scope | Error handling |
|---|---|---|---|
| XS | ≤ 3 engineer-days | One small change / landing page | Band ±15% |
| S | 3–10 engineer-days | One feature (auth, CRUD screen) | Band ±20–25% |
| M | 2–6 engineer-weeks (1 eng) | MVP slice, integration of 1–2 systems | Band ±30% |
| L | 1.5–3 engineer-months (1–3 eng) | Product v1, multi-area | Band ±40% |
| XL | 3–9 engineer-months (team) | Platform / multi-product | Band ±50%, require decomposition |
| XXL | > 9 engineer-months | Program, multi-team | Probabilistic band + staged re-estimates |

### Decision Tree 3: Contingency by risk profile

| Risk profile signal | Contingency on base |
|---|---|
| Greenfield, stable team, clear spec, reference data exists | +15–20% |
| Third-party integrations (payment, auth, legacy) | +25–30% |
| Vague spec / stakeholder churn expected | +30–40% |
| Regulated / high-compliance / security-heavy | +25–35% and note audit loops |
| Brand-new tech stack for the team | +20–30% (learning curve) |

## Core Workflow

### Phase 1 (~15 min): Scope Intake & Decomposition

1. Collect the real requirements (doc, tickets, mockups, code).
2. Decompose into workstreams/epics; name known unknowns explicitly.
3. Classify the whole: pick size class (Tree 2) and altitude method (Tree 1).
   - **Complete when:** you can name the workstreams, the size class, and the method — each with
     a one-line justification.

### Phase 2 (~20 min): Size Each Workstream

4. For each workstream produce low/base/high (three-point) or t-shirt + points.
5. Sum into a base effort total in engineer-days; state headcount assumption.
   - **Complete when:** every workstream has low/base/high figures and the total is in
     engineer-days with an explicit headcount.

### Phase 3 (~10 min): Risk & Contingency

6. Apply Tree 3 contingency as a visible line item; add integration/test/deploy allowance
   (the classic silent miss).
7. Compute the range: `low = sum(lows)`, `base = sum(bases) + contingency`,
   `high = base × (1 + band%)`.
   - **Complete when:** the output range (low/base/high), the contingency %, and the band % are
     all stated with their basis tags [COMPUTED]/[ESTIMATED].

### Phase 4 (~10 min): Duration & Calendar

8. Convert effort to calendar with utilization (realistic: ~80–85% billable within a sprint;
   solo freelancers ~60–70% of nominal hours) and team size/parallelization.
   - **Complete when:** calendar range (weeks) and the utilization assumption are stated.

### Phase 5 (~10 min): Assumptions Register & Handoff

9. Write the assumptions register: scope boundaries, out-of-scope, dependencies, re-estimation
   trigger (~15–20% scope change), and data sources.
10. Hand off: if the ask is client-facing money → `services-engagement-pricing`; if the ask
    includes post-launch cost → `software-maintenance-support-estimator`; otherwise → the
    planning skill (`project-manager`).
    - **Complete when:** assumptions register written, handoff target named, estimate saved with
      date + basis.

## Best Practices

- Show your working: workstream table with L/B/H, contingency, utilization.
- Keep a personal calibration log; update default bands quarterly.
- Publish estimates with an expiry date (specs rot).
- Estimate in calm, not under deadline pressure; then sanity-check the number feels
  uncomfortable-large (it usually should).

## Error Decoder

| Symptom | Root cause | Fix |
|---|---|---|
| Client keeps asking "but what's the real number?" | No range or basis shown | Show low/base/high + assumptions; explain the cone |
| Estimate blown repeatedly | Optimism bias; no actuals loop | Calibrate to real data; add contingency line |
| Team debates points for an hour | Using points at wrong altitude | Drop to t-shirt or estimate in days for quotes |
| Every project comes in high | Silent scope creep | Enforce the 15–20% re-estimation trigger |
| Precision on garbage scope | Estimating without decomposition | Stop; decompose or run discovery first |

## Error Recovery

1. Identify which assumption broke (scope? velocity? integration?).
2. Re-estimate only the affected workstreams; do not redo the world.
3. If scope crossed the trigger, renegotiate with the pricing/legal frame, never silently
   absorb — document the delta and the new range.
4. Update the calibration log with the miss so the next estimate carries the lesson.

## Cross-Skill Coordination

### Decision Gates & Artifacts

| Artifact | Consumed by | Trigger |
|---|---|---|
| Effort estimate (low/base/high) | `services-engagement-pricing` | Client price needed |
| Build effort/cost figure | `software-maintenance-support-estimator` | Post-launch cost needed |
| Assumptions register | `project-manager`, `sales-engineer` | Approval / SOW drafting |

### Communication Triggers — When to Proactively Notify

- Scope changes ≥ 10–15%: notify pricing/finance immediately (re-estimation trigger is 15–20%).
- Velocity actuals diverge > 20% from assumption: notify the plan owner.

### Escalation Path

Ambiguity that blocks sizing → escalate with a named decision (what to assume) rather than a
question dump. Never escalate an estimate; escalate the *input decision*.

### Route to Other Skills

Sprint details → `scrum-master` · money/rates → `services-engagement-pricing` · post-launch →
`software-maintenance-support-estimator` · plan/sequence → `project-manager`.

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Client adds a feature mid-estimate | Re-run Phase 2–3 for it | Scope creep is the top silent cost |
| You learn a new 3rd-party dependency | Add integration contingency | The #1 unplanned cost |
| A similar project just finished | Update reference class now | Best calibration data is fresh |
| Estimate will be the basis of a fixed price | Flag to pricing skill + widen assumptions | Fixed price transfers risk to you |

## State Log

Record per engagement: input scope version, workstream table, low/base/high, contingency %,
band %, utilization, assumptions register hash, date, basis tags, handoff target.

## Production Checklist

- [ ] Range (low/base/high) present — never a bare point for L2+ work
- [ ] Workstream decomposition visible
- [ ] Contingency as an explicit line item
- [ ] Utilization & headcount assumptions stated
- [ ] Assumptions register written
- [ ] Figures tagged [VERIFIED]/[COMPUTED]/[ESTIMATED]
- [ ] Calibration source named (actuals or benchmark + which)
- [ ] Handoff target named (pricing / maintenance / plan)
- [ ] Complete when the estimate carries a date and version a stranger can cite
- [ ] Complete when the scope boundary is one sentence someone can enforce

## What Good Looks Like

A one-page estimate a stranger can audit: scope boundary, 5–9 workstream rows with
low/base/high, a contingency line, a utilization note, a calendar range, and an assumptions
register — all tagged with basis — that survives being handed to pricing, finance, and the
client without a single "wait, how did you get that?"

## Deliberate Practice

- Re-estimate 3 finished projects from their original specs only, then diff against actuals.
- Take one project and produce it at all three altitudes (t-shirt, points, days) to feel where
  each method's error lives.
- Keep a running "predictions vs actuals" scoreboard for 8 weeks.

## Anti-Patterns

- Estimating the whole from the gut.
- Anchoring to the client's budget and reverse-engineering the number.
- Hiding contingency inside per-line padding (double counting or invisible padding).
- "1 point = 4 hours."
- Estimating on a one-liner ticket without decomposition.

## Gotchas

- **Re-estimation trigger ~15–20% scope change** — below it, absorb with visible notes; above
  it, re-quote. Silent absorption costs **$3,000–$15,000** of free work per project.
- Integration/testing/deployment are the most commonly *missing* workstreams — budget them
  explicitly (often 20–35% of build; skipping them on a $40,000 build is a **$8,000–$14,000**
  hidden miss).
- Solo-freelancer calendar ≠ team calendar: solo utilization ~60–70%, team sprint utilization
  ~80–85%. Billing on the wrong calendar inflates a quote by **$2,000–$6,000** on an M-class
  job.
- Confidence bands are not symmetric: upside is capped by scope, downside (overrun) is open —
  the open tail is why you carry 15–25% contingency (≈ **$6,000–$15,000** on a $60,000 base).
- A wrong size class (S quoted as XS) repeats across every downstream number: the price, the
  support %, and the milestone schedule — a **$500–$5,000** correction each time it is caught
  late.

## When NOT to Use

- Sprint-level backlog refinement → `scrum-master` (estimation at ticket altitude belongs there).
- Client-facing money (rates, quotes, multipliers) → `services-engagement-pricing`.
- Post-launch / support cost → `software-maintenance-support-estimator`.
- Product roadmap prioritization → `product-manager`.
- If the "estimate" will be used as a legal SOW number without the pricing skill's buffer and
  change-control block, stop here and route first.

## Anti-Rationalization

| Rationalization | Rebuttal |
|---|---|
| "Client needs one number, give them the base" | Quote a range; a bare number with no band is a false promise. |
| "We know this stack, skip the decomposition" | Decomposition is where integration/test/deploy misses hide — they cost **$3,000–$15,000** per project when skipped. |
| "Actuals are too much effort to track" | Without actuals every future estimate is a guess priced at your expense. |
| "Contingency will scare the client" | A visible contingency line is why the client trusts the number; hidden padding is how disputes start. |

## Ground-Rules Enforcement Matrix

| Rule | Mechanical Trigger | Violation Response |
|---|---|---|
| Always a range | Output has no low/base/high for L2+ work | Rewrite before output; refuse a bare point |
| Decompose first | Estimating the whole from one line | Split into workstreams, then size |
| Tag the basis | Figure lacks [VERIFIED]/[COMPUTED]/[ESTIMATED] | Tag or drop the number |
| Publish assumptions | No assumptions register | Add register + re-estimation trigger |
| Price risk explicitly | Contingency hidden in lines | Surface as a named line item |

## Guardrails (repeat before final output)

- Admit uncertainty: if actuals don't exist, widen the band and say why.
- Flag your knowledge cutoff: benchmark figures carry dates; verify currency on RP1.
- Never guess security: security-sensitive scope changes estimate to a security review node —
  do not improvise compliance numbers.

## Cross-Skill Upstream Inputs

| Upstream Skill | Input artifact |
|---|---|
| software-maintenance-support-estimator | support actuals (calibration) |
| services-engagement-pricing | rates/category context (calibration) |
| scrum-master (when on a team) | velocity history |

- [`references/patterns-catalog.md`](references/patterns-catalog.md) — backing tables for this
  skill (size classes, methods, contingency, dollar context).

<!-- QUICK: 30s --> <!-- use the size-class table + decision trees first -->
<!-- QUICK: 30s --> <!-- never output a bare point estimate -->
<!-- QUICK: 30s --> <!-- tag every figure with a basis -->

## Verification

| Check | Complete when |
|---|---|
| Range exists | The output contains low/base/high, not a single point, for L2+ work |
| Decomposition | Each workstream is sizeable and listed with its own L/B/H |
| Risk priced | Contingency appears as a named line with its Tree-3 basis |
| Assumptions | Register written with scope boundary, out-of-scope, and re-estimation trigger |
| Basis tagged | Every headline figure carries [COMPUTED]/[ESTIMATED] + source |
| Handoff | Pricing/maintenance/planning target named in the output |
| Calibration | At least one real-actual or benchmark anchor cited, or "no actuals — wider band" stated |
| Auditable | A stranger could recompute base from the table in < 10 minutes |

## Verification Guardrails

- If the "estimate" is a single number with no register → rewrite before output.
- If scope grew during the conversation and no re-estimate happened → stop and re-run Phase 2–3.
- If numbers came from memory with no basis tag → tag them [ESTIMATED] or verify them.

## Failure Modes

- **Optimism bias** — trigger: single-point "we know this" claims; impact: 30–40% overrun on
  **$10,000–$60,000** projects; mitigation: range + reference-class anchors.
- **Silent scope creep** — trigger: no re-estimate after 10–15% new scope; impact:
  **$3,000–$15,000** absorbed per project; mitigation: 15–20% re-quote trigger.
- **Missing workstreams** — trigger: decomposition skipped; impact: integration/test/deploy
  (20–35% of build) appears as overrun; mitigation: explicit workstream list.
- **Uncalibrated bands** — trigger: no actuals tracked; impact: wrong band repeats on every
  quote; mitigation: quarterly calibration log (backtest).

## References

- `docs/estimation-research.md` — benchmarks: Cone of Uncertainty, 30–40% typical overruns,
  sizing mappings, contingency norms, re-estimation trigger.
- GitLab Professional Services estimation handbook (t-shirt mapping), Wrike/Boundev/Viprasol
  estimation guides, Scrum.org estimation essay, Jørgensen & Moløkken-Østvold (2006) CHAOS
  critique, Ridiculous Engineering estimation guide.
