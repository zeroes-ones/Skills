---
name: consulting-effort-estimator
description: >
  Use when estimating effort, duration, or price-input for services and consulting engagements
  that are not a simple software build — discovery and advisory engagements, audits, options
  analyses, design/content/data/ML deliverables, training and documentation, and ongoing
  fractional or staff-augmentation roles — sized XS to XXL in consultant-days. Handles
  deliverable-based decomposition, engagement-shape choice (one-off, staged, retainer, monthly
  commitment), seniority mix, utilization, and assumption registers. Do NOT use for estimating
  code builds (software-project-estimator), for client-facing money (services-engagement-pricing
  turns this skill's range into a quote), or for post-launch support pricing
  (software-maintenance-support-estimator).
license: MIT
tags:
- consulting
- freelancing
- estimation
- discovery
- advisory
- retainer
- deliverable-based
- services
- fractional
- staff-augmentation
author: Sandeep Kumar Penchala
type: operations
status: stable
version: 1.0.0
updated: 2026-09-09
token_budget: 4000
chain:
  examples:
  - skills/12-operations/consulting-effort-estimator/examples/backtest
  consumes_from:
  - services-engagement-pricing
  feeds_into:
  - services-engagement-pricing
---
# Consulting Effort Estimator
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Estimate the effort behind services and consulting work that is not a simple software build:
discovery and audits, advisory retainers, deliverable-based projects (design, content, data,
ML, training, docs), and ongoing fractional or staff-augmentation commitments. Output is a
range of consultant-days with seniority mix, an assumption register, and a handoff to the
pricing skill.

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce an effort range without completing this research.**

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Define the deliverable, not the hours.** What artifact/decision/outcome is the client buying? | [CONTEXT_VIOLATION] Consulting hours without a deliverable contract are unbounded. | Proposal scope, meeting notes, prior reports |
| **RP2** | **Establish the engagement shape** (one-off, staged, retainer, monthly commitment). | [MISFIT] The shape decides utilization and buffer, which changes the range by 20–40%. | Client intent, payment cadence |
| **RP3** | **Fix seniority mix and rates basis** — consultant-days by level, then let pricing own money. | [HALLUCINATION_GUARD] Effort (days) and money ($) are separate; mixing them invites round-number lies. | Team roster, day-rate benchmarks (dated) |
| **RP4** | **Check utilization reality** — billable load 60–70% solo, 70–80% firm. | [STALE_RISK] Nominal weeks ≠ billable days; overhead eats 25–40% of calendar. | Past engagement logs, backtest |
| **RP5** | **Tag every figure [VERIFIED]/[COMPUTED]/[ESTIMATED]** and name the basis. | [HALLUCINATION_GUARD] Untagged days are indistinguishable from invented ones. | docs/estimation-research.md §5 |
| **RP6** | **Map what the estimate feeds** — pricing skill (money), engagement plan, and (if recurring) the retainer renewal loop. | [CASCADE_BLINDNESS] A day-range error multiplies into a wrong quote and a wrong renewal. | Cross-skill table below |

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

Re-check deliverable, shape, and seniority at each fork before committing the range.

## Anti-Hallucination

- Always output consultant-day ranges (low/base/high) with a seniority split — never bare
  hours-to-dollars conversions.
- Admit uncertainty: no comparable past engagement → widen the band and say why.
- Flag your knowledge cutoff: day-rate and utilization norms carry dates; re-check before use.
- Never guess security or compliance scope: regulated engagements get a compliance/legal review
  line, not improvised figures.

## Route the Request

### Auto-Route (No User Input Required)

- "How many days is a discovery/audit/advisory?" → this skill.
- "What does a design/content/data/ML deliverable take?" → this skill.
- "How do I price a monthly retainer / fractional role?" → estimate days here, then hand the
  range to `services-engagement-pricing`.
- "How long to build code X?" → `software-project-estimator`.

### Intent Route (Ask the User)

If unclear, ask up to 3 questions: (1) what is the concrete deliverable/decision? (2) one-off,
staged, or ongoing (retainer/monthly)? (3) what seniority mix do you plan to staff it with?

## Ground Rules — Read Before Anything Else

1. **Deliverable first.** Size the artifact/decision, not the calendar.
2. **Shape before numbers.** Retainer vs one-off changes utilization and buffer (20–40% swing).
3. **Days, not dollars.** This skill outputs effort; money lives in
   `services-engagement-pricing`.
4. **Seniority split is explicit** (e.g., 40% senior / 60% mid) so pricing can apply the right
   rates.
5. **Show the range and the register.** Same discipline as build estimation.
6. **Utilization is real:** solo ≈ 60–70% of nominal, firm ≈ 70–80%.
7. **Calibrate quarterly** from engagement logs (backtest).

## The Expert's Mindset

### What Masters Know That Others Don't

- Consulting value is in the *decision* you hand over, not the hours — scope the deliverable
  and the decision, and effort follows.
- Non-software deliverables size differently: a "report" ranges 3–15 days by depth; an audit
  5–25; a roadmap 4–10; training 2–5 per cohort plus prep.
- Retainers are capacity contracts: estimate *committed availability + expected burn*, then
  price availability as a premium.
- The biggest consulting miss is unbilled prep/admin/travel — effective days beat nominal days.

### When to Break Your Own Rules

- Tiny XS asks (< 2 days, e.g., a one-hour advisory call) are single-point with a floor —
  bands add noise.
- Discovery inside a bigger build engagement is often a fixed day-box (e.g., 5-day sprint)
  rather than a ranged estimate.

## Operating at Different Levels

| Level | Mode | Engagement | Signature move |
|---|---|---|---|
| L1 Apprentice | New consultant | hourly/advisory calls | track real days |
| L2 Practitioner | Freelancer | one-off deliverables | day-box discovery |
| L3 Senior | Consultant | staged + retainers | shape + utilization model |
| L4 Lead | Agency/firm | programs, teams | seniority mix + utilization engine |
| L5 Transformative | Strategic partner | outcome-based | metric-linked effort, guardrails |

## When to Use

| Use this skill | Instead use |
|---|---|
| Discovery/audit/advisory/options effort | `software-project-estimator` (code builds) |
| Design, content, data, ML, training, docs deliverables | `software-maintenance-support-estimator` (post-launch) |
| Ongoing/fractional/staff-augmentation planning | `project-manager`, `scrum-master` (team ops) |
| Turning the range into money | `services-engagement-pricing` |

## When NOT to Use

- Software build estimates (backend/API/DB/UI features) → `software-project-estimator`.
- Client-facing quotes/rate cards → `services-engagement-pricing` (this skill feeds it).
- Support/maintenance/SLA products → `software-maintenance-support-estimator`.
- Internal team capacity planning on an existing product team → `project-manager`/`scrum-master`.

## Decision Trees

### Decision Tree 1: Engagement shape

| Client situation | Shape | Effort effect |
|---|---|---|
| One clear question/artifact | one-off deliverable | fixed day-box range |
| Big program, phased buy-in | staged milestones | per-stage ranges + re-estimate trigger |
| Ongoing availability need | retainer | committed days + expected burn |
| Named individual for the team | fractional/staff-aug | monthly day commitment + ramp |
| Measurable business outcome | outcome-based | metric + floor (effort still modeled) |

### Decision Tree 2: Deliverable type → day ranges (base)

| Deliverable | Base consultant-days | Notes |
|---|---|---|
| Advisory call / mini-review | 0.5–2 | floor pricing |
| Options analysis / tech assessment | 3–8 | per option 1–2 |
| Roadmap / discovery | 4–10 | interviews + synthesis |
| Audit (security/compliance/architecture) | 5–25 | senior-heavy |
| Design or content deliverable | 3–15 | review cycles double days |
| Data/analytics or ML deliverable | 5–30 | data quality is the swing |
| Training + materials | 2–5 per cohort + 2–4 prep | repeatable |
| Documentation package | 3–10 | depends on source quality |
| Fractional role | monthly commitment 4–10 days/mo | + ramp and availability |

### Decision Tree 3: Seniority mix & utilization

| Mix signal | Default split | Utilization |
|---|---|---|
| Discovery/advisory | senior-heavy (60–80% senior) | solo 60–70% |
| Deliverable production | 40% senior / 60% mid | firm 70–80% |
| Ongoing/fractional | named senior | + availability premium |
| New-to-you domain | add +20–30% days | band wide |

## Core Workflow

### Phase 1 (~10 min): Deliverable & Shape

1. Write the deliverable/decision in one sentence; pick the shape (Tree 1).
   - **Complete when:** deliverable and shape are stated; out-of-scope listed.

### Phase 2 (~15 min): Decompose & Size

2. Break into work streams (interviews, analysis, production, reviews, handoff).
3. Size each stream with three-point days (Tree 2 anchors); apply seniority mix (Tree 3).
   - **Complete when:** each stream has low/base/high days and the seniority split is written.

### Phase 3 (~10 min): Utilization & Buffer

4. Convert to calendar with utilization; add review/rework buffer (20–30% for design/content).
5. Produce the range and assumption register.
   - **Complete when:** range (low/base/high), utilization, buffer, and register are explicit.

### Phase 4 (~10 min): Handoff

6. Hand the day-range to `services-engagement-pricing` for money; note renewal triggers for
   retainers.
   - **Complete when:** handoff target and renewal/re-estimation triggers are named.

## Best Practices

1. Scope the decision the client makes from your work.
2. Keep a deliverable-day log per engagement and calibrate quarterly.
3. Show the seniority mix — pricing and the client both need it.
4. Never discount days; discount scope (same law as pricing).
5. Day-box discovery (fixed 5-day sprint) before big fixed quotes.
6. Model review cycles explicitly (they double design/content days).
7. Price availability on retainers as a premium, not bulk hours.
8. Re-estimate at 15–20% scope change on staged engagements.
9. Track effective vs nominal days (prep/admin/travel).
10. Prefer two small staged engagements over one huge vague one.

## Error Decoder

| Symptom | Root cause | Fix |
|---|---|---|
| Retainer runs dry every month | Burn estimated from hope | Model expected burn from the log |
| Discovery quote always over | Under-scoped interviews/synthesis | Use Tree 2 day-box anchors |
| Design/content days double | Review cycles omitted | Add 20–30% rework buffer |
| Client disputes invoice | Deliverable not defined | One-sentence deliverable + out-of-scope |
| Fractional role bleeds hours | No ramp/availability model | Monthly day commitment + ramp |

## Error Recovery

1. Identify the broken assumption (deliverable? shape? utilization? seniority?).
2. Re-size only the affected streams and renegotiate the delta at the 15–20% trigger.
3. Update the engagement log with the lesson; widen the relevant Tree 2 anchor.

## Cross-Skill Coordination

### Decision Gates & Artifacts

| Artifact | Consumed by | Trigger |
|---|---|---|
| Day-range + seniority mix | `services-engagement-pricing` | Quote time |
| Deliverable/assumption register | engagement plan, client | SOW drafting |
| Recurring burn model | `software-maintenance-support-estimator` (ops flavor) | Retainer renewal |

### Cross-Skill Upstream Inputs

| Upstream Skill | Input artifact |
|---|---|
| services-engagement-pricing | rate/category context for calibration |
| project-manager (on a team) | prior delivery actuals |
| software-project-estimator | code-adjacent day estimates to combine |

### Communication Triggers — When to Proactively Notify

- Deliverable redefined mid-engagement → re-estimate before the next milestone.
- Burn exceeds the retainer model two months running → renegotiate the commitment.

### Escalation Path

Escalate the *scope decision*, never the days: name the choice the client must make.

### Route to Other Skills

Money → `services-engagement-pricing` · code work → `software-project-estimator` · post-launch →
`software-maintenance-support-estimator` · team ops → `project-manager`.

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Client asks "what will the whole program cost" | Run discovery day-box first | Fixed quotes without discovery are gambling |
| A deliverable is re-scoped | Re-estimate affected streams | 15–20% trigger applies to consulting too |
| New quarter begins | Calibrate day-anchors from the log | Fresh data beats last year's anchor |
| Retainer under-used two months | Flag capacity risk | Availability was bought; keep it valuable |

## State Log

Per engagement: deliverable sentence, shape, streams with L/B/H days, seniority split,
utilization, buffer, assumption register, handoff target, calibration note.

## Production Checklist

- [ ] Deliverable + out-of-scope written in one sentence
- [ ] Shape chosen (Tree 1) with reason
- [ ] Streams decomposed with low/base/high days
- [ ] Seniority mix explicit
- [ ] Utilization and buffer shown
- [ ] Assumption register present
- [ ] Handoff to pricing named (with renewal triggers for retainers)
- [ ] Complete when a stranger can recompute the range in < 10 minutes
- [ ] Complete when the register lists what would break the estimate
- [ ] Complete when calibration basis (log or anchor) is named

## What Good Looks Like

A one-page engagement estimate a client can act on: a one-sentence deliverable, a shape, a
stream table in consultant-days with a seniority split, a utilization note, a buffer line, an
assumption register, and a named handoff to pricing — so the quote that follows is traceable to
the work, not to a vibe.

## Deliberate Practice

- Size the same deliverable as discovery vs full audit to feel the depth spread.
- Log real days for 3 engagements and rebuild Tree 2 anchors from them.
- Model one retainer as expected-burn vs committed-availability to internalize the premium.

## Anti-Patterns

- Sizing the calendar, not the deliverable.
- Converting days to dollars inside this skill.
- Ignoring utilization (nominal weeks ≠ billable days).
- One senior + no mid on production work (rate mismatch).
- Retainer priced as bulk discounted hours.

## Anti-Rationalization

| Rationalization | Rebuttal |
|---|---|
| "Client needs one day number" | Give the range; a bare number with no register is a promise. |
| "Discovery is free; the build will pay" | Discovery is the riskiest deliverable to under-quote — a **$1,000–$5,000** day-box protects the whole deal. |
| "Retainers fill the calendar" | Unused committed capacity is still capacity you sold — model availability, price the premium. |
| "Skip the log, I remember" | Without the log, Tree 2 anchors drift and every quote repeats the **$2,000–$10,000** miss. |

## Ground-Rules Enforcement Matrix

| Rule | Mechanical Trigger | Violation Response |
|---|---|---|
| Deliverable first | Estimate with no one-sentence deliverable | Write deliverable + out-of-scope |
| Shape before numbers | Range without a chosen shape | Pick shape (Tree 1) first |
| Days not dollars | Money appears in the effort output | Strip to days; route to pricing |
| Seniority explicit | No seniority split | Add split before final range |
| Range + register | Bare point or no register | Rewrite before output |

## Failure Modes

- **Failure mode — scope of "consulting" undefined:** no deliverable sentence. When this fails,
  the worst case is **$2,000–$10,000** of unbilled scope per engagement. Known limitation of
  vague briefs — write the deliverable + out-of-scope first.
- **Failure mode — shape misfit:** retainer sized like a one-off. When that fails, utilization
  swings 20–40% (**$5,000–$25,000/yr** on a monthly commitment). Exit condition: match shape
  (Tree 1) to the client situation.
- **Failure mode — utilization fantasy:** nominal weeks used as billable days. Worst case:
  25–40% of calendar overhead unpriced. Edge case to re-check: travel/admin/prep-heavy
  engagements.
- **Failure mode — burn model missing:** retainer without an expected-burn model. When this
  fails, **$3,000–$12,000/yr** shows up at the true-up. Known limitation of availability-only
  pricing — model committed days + expected burn.

## Gotchas

- Discovery under-quoted by 2 days costs **$1,000–$5,000** and poisons the trust on the build
  that follows.
- Review/rework cycles double design and content days — skipping the buffer is a
  **$2,000–$8,000** miss per deliverable.
- Retainer capacity sold as bulk hours instead of availability is a **$6,000–$24,000/yr**
  hidden subsidy.
- B2B/B2G consulting carries 2–5× equivalent pricing but also 15–40% more unbilled prep —
  price the effective days, not the sticker days.
- A 15–20% scope-change trigger protects consulting exactly like build work; ignoring it costs
  **$3,000–$15,000** per staged engagement.

## Verification

| Check | Complete when |
|---|---|
| Deliverable | One-sentence deliverable + out-of-scope exists |
| Shape | Engagement shape chosen with reason |
| Decomposition | Streams listed with low/base/high consultant-days |
| Seniority | Split explicit (e.g., 60/40) |
| Utilization | Realistic utilization stated (60–80%) |
| Buffer | Review/rework buffer visible |
| Register | Assumptions + 15–20% re-estimate trigger present |
| Handoff | Pricing skill named as the money target |
| Calibrated | Log or named anchor cited for day ranges |
| Auditable | Recomputable from the stream table in < 10 minutes |

## Verification Guardrails

- No deliverable sentence → refuse a range; ask for the deliverable first.
- Money inside the effort output → strip to days and route to pricing.
- No utilization stated → add it (solo 60–70%, firm 70–80%) or widen the band.

## References

- [`references/patterns-catalog.md`](references/patterns-catalog.md) — day-range tables,
  shapes, seniority/utilization defaults, dollar context.
- `docs/estimation-research.md` §5 — services & consulting coverage matrix, segment playbooks.
- `services-engagement-pricing` / `software-project-estimator` / `software-maintenance-support-estimator` for the adjacent domains.

<!-- QUICK: 30s --> <!-- deliverable + shape before any range -->
<!-- QUICK: 30s --> <!-- days only here; money goes to pricing -->
<!-- QUICK: 30s --> <!-- seniority + utilization are not optional -->
