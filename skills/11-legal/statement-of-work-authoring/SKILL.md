---
name: statement-of-work-authoring
description: >
  Use when drafting a full Statement of Work (SOW) for a client engagement — converting an
  effort estimate and a pricing block into a contract-ready document with parties and
  background, scope and deliverables, milestones and dates, exclusions and assumptions,
  acceptance criteria, change control, payment schedule, client responsibilities, IP,
  warranties, liability and confidentiality clauses, and termination terms — for
  freelancers, agencies, and consultancies, before legal review. Handles fixed-bid,
  time-and-materials, retainer, and hybrid SOW structures. Do NOT use for estimating effort
  (software-project-estimator, consulting-effort-estimator), for pricing and rate cards
  (services-engagement-pricing — this skill consumes that output), or as a substitute for
  lawyer-reviewed terms in high-value or regulated deals.
license: MIT
tags:
- sow
- statement-of-work
- contract
- scope
- deliverables
- milestones
- acceptance
- change-control
- payment-terms
- proposal
author: Sandeep Kumar Penchala
type: legal
status: stable
version: 1.0.0
updated: 2026-09-09
token_budget: 4000
chain:
  examples:
  - skills/11-legal/statement-of-work-authoring/examples/backtest
  consumes_from:
  - services-engagement-pricing
  feeds_into:
  - services-engagement-pricing
---
# Statement of Work Authoring
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Turn an effort estimate + pricing block into a complete, contract-ready Statement of Work —
the document a client signs — with every commercial term visible: scope, deliverables,
milestones, acceptance, change control, payment schedule, responsibilities, and the legal
placeholders a lawyer then reviews. Freelancers and agencies use this so the SOW stops being
"the pricing email" and starts being the project's source of truth.

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not draft a SOW without completing this research.**

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Gather the real inputs**: effort range (estimator), pricing block (pricing skill), scope notes, prior emails. | [CONTEXT_VIOLATION] A SOW drafted from memory re-litigates scope that was already settled. | estimator + pricing outputs, notes, chat |
| **RP2** | **Know the client's procurement reality** (B2C invoice vs B2B PO vs B2G RFP terms, required clauses). | [MISFIT] A SOW the buyer's legal can't accept gets redlined to death or killed. | Procurement rules, master agreement, RFP |
| **RP3** | **Check for an existing MSA/DPA.** IP, liability, confidentiality may already live there. | [DUPLICATION] Copying terms that exist in the MSA creates conflicts; SOW should reference, not repeat. | Master agreement, data processing agreement |
| **RP4** | **Tag every number [VERIFIED]/[COMPUTED]/[ESTIMATED]** (price, dates, milestones). | [HALLUCINATION_GUARD] A wrong date in a signed SOW is a real breach risk. | estimator/pricing outputs (dated) |
| **RP5** | **List the failure modes of SOWs you have seen** (scope fights, acceptance ambiguity, milestone cash-flow). | [FAILURE_BLINDNESS] Every dispute traces to a vague SOW line; name them and close each one. | Past disputes, postmortems |
| **RP6** | **Map downstream consumers** — legal review, the delivery plan, the support contract that may follow. | [CASCADE_BLINDNESS] The SOW scope boundary feeds the support boundary and every re-quote. | Cross-skill table below |

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

Re-verify price, dates, and scope boundary at each fork (structure, milestones, acceptance,
change control) before finalizing a section.

## Anti-Hallucination

- Never invent numbers: every date, milestone payment, and cap must trace to an input or be
  marked TBD for negotiation.
- Admit uncertainty: unclear terms are written as open questions for the client, never as
  assumed facts.
- Flag your knowledge cutoff: legal norms vary by jurisdiction; boilerplate stays placeholder
  until lawyer review.
- Never guess security or compliance scope: regulated work references the DPA/compliance
  annex instead of improvising liability language.

## Route the Request

### Auto-Route (No User Input Required)

- "Draft a SOW for this project" → this skill (inputs from estimator + pricing first).
- "Turn the quote into a contract" → this skill.
- "What milestones/payment schedule should I propose?" → Decision Tree 2.
- Effort/price first → `software-project-estimator` / `consulting-effort-estimator` /
  `services-engagement-pricing`, then return here.

### Intent Route (Ask the User)

If unclear, ask up to 3 questions: (1) do you have the effort range and pricing block? (2) is
there an existing MSA/DPA to reference? (3) fixed-bid, T&M, retainer, or hybrid structure?

## Ground Rules — Read Before Anything Else

1. **Structure follows money:** fixed-bid, T&M, retainer, and hybrid produce different SOW
   skeletons (Decision Tree 1).
2. **Scope is a boundary, not a list of vibes:** deliverables + explicit exclusions + an
   assumptions register.
3. **Acceptance must be testable:** define what "done" means per deliverable and the review
   window.
4. **Change control is the profit-protector:** 15–20% scope-change trigger + written change
   request flow.
5. **Payment schedule ties to milestones you can prove:** demo, sign-off, deploy.
6. **Reference the MSA/DPA; don't duplicate it.**
7. **Boilerplate stays placeholder until legal review** — never sign unreviewed terms.

## The Expert's Mindset

### What Masters Know That Others Don't

- The SOW is the single source of truth for scope fights — every hour of dispute costs
  **$500–$5,000** in unplanned work, and most trace to one vague sentence.
- Acceptance ambiguity is the #1 cause of "done" disputes: define acceptance criteria per
  deliverable and a written review window (e.g., 5 business days).
- Milestone billing is cash-flow engineering: align payments to spend (e.g., 30/30/30/10 or
  50/40/10) so you are never financing the client.
- The best SOWs are short enough to read and precise enough to enforce — one page of scope
  beats ten pages of boilerplate.

### When to Break Your Own Rules

- Small fixed engagements (< $5,000): a proposal + acceptance email may be enough; full SOW is
  overhead.
- Under an existing MSA: the SOW shrinks to scope + milestones + price; terms live in the MSA.

## Operating at Different Levels

| Level | Mode | SOW style | Signature move |
|---|---|---|---|
| L1 Apprentice | Freelancer | proposal + simple SOW | acceptance + payment terms written |
| L2 Practitioner | Freelancer | standard SOW | milestone billing + change control |
| L3 Senior | Agency | MSA-anchored SOW | deliverables + acceptance table |
| L4 Lead | Firm | multi-workstream SOWs | structure by money + risk register |
| L5 Transformative | Strategic partner | outcome-based annex | metric-linked milestones + guardrails |

## When to Use

| Use this skill | Instead use |
|---|---|
| Full SOW / contract-ready engagement doc | `services-engagement-pricing` (price block only) |
| Effort/price inputs | estimator + pricing skills |
| Independent contractor agreement / employment | legal-advisor, jurisdiction counsel |
| Product license/terms | legal-advisor / product counsel |
| Support annex | `software-maintenance-support-estimator` terms |

## When NOT to Use

- Negotiating price/rates → `services-engagement-pricing`.
- Estimating effort → estimator skills.
- A signed legal contract without lawyer review — this skill drafts for review, never for
  signing alone in regulated/high-value deals.
- Employment/independent-contractor classification matters → dedicated legal counsel.

## Decision Trees

### Decision Tree 1: SOW structure by money model

| Model | SOW skeleton |
|---|---|
| Fixed-bid | fixed price + deliverables + acceptance + change control + milestone payments |
| T&M | rates + estimate range + not-to-exceed + burn reporting cadence |
| Retainer | monthly commitment + hours/deliverables bucket + overflow T&M + availability terms |
| Hybrid | fixed slice (scoped) + T&M lane (iteration) — two price sections |
| Outcome-based | metric + measurement method + floor + milestone tied to metric |

### Decision Tree 2: Milestone & payment schedule

| Situation | Milestones | Payment split |
|---|---|---|
| Small fixed (< $10K) | kickoff, delivery | 50/50 or 100% on acceptance |
| Medium fixed | kickoff / alpha / acceptance | 30/30/40 |
| Large fixed | design / build / UAT / go-live | 30/30/30/10 |
| T&M | monthly burn | monthly invoice, net-15/30 |
| Retainer | monthly | monthly in advance (premium) |
| B2G | per deliverable milestone | tied to accepted deliverables + lag priced |

### Decision Tree 3: Acceptance criteria style

| Deliverable type | Acceptance definition |
|---|---|
| Code/feature | acceptance tests pass + demo sign-off, review window 5 business days |
| Design/content | 2 review rounds included; extra rounds billed |
| Discovery/audit | report delivered + findings walkthrough |
| Ongoing support | SLA metrics + monthly report accepted by month close |

## Core Workflow

### Phase 1 (~10 min): Collect Inputs

1. Pull effort range + assumptions (estimator) and pricing block (pricing skill).
2. Confirm MSA/DPA existence and client procurement rules.
   - **Complete when:** inputs are assembled with basis tags; MSA/DPA status recorded.

### Phase 2 (~15 min): Scope & Deliverables

3. Write the scope boundary (one sentence) + deliverables table (deliverable, description,
   acceptance definition, date/milestone).
4. Write exclusions and the assumptions register.
   - **Complete when:** scope sentence, deliverables table, exclusions, and assumptions exist
     and are internally consistent with the price.

### Phase 3 (~15 min): Commercial Terms

5. Choose the skeleton (Tree 1); write price section, milestone/payment schedule (Tree 2),
   and change control (15–20% trigger + written change-request flow).
   - **Complete when:** price, schedule, and change control match the pricing block exactly.

### Phase 4 (~15 min): Legal & Administrative

6. Add parties/background, client responsibilities, IP, warranties, liability caps,
   confidentiality, termination — referencing the MSA/DPA where they exist, placeholders
   otherwise.
7. Add signature/version block and the legal-review handoff note.
   - **Complete when:** every commercial term is present and legal items are clearly marked
     "placeholder — review".

### Phase 5 (~10 min): Review & Handoff

8. Self-review against the Verification table; route to legal review; save versioned draft.
   - **Complete when:** the SOW passes its own Verification checklist and legal handoff is
     named.

## Best Practices

1. Keep the scope boundary to one enforceable sentence.
2. Tie every payment to a provable milestone.
3. Define acceptance per deliverable with a review window.
4. Write change control before scope grows.
5. Reference, don't duplicate, the MSA.
6. Version and date every draft; track redlines.
7. Include client responsibilities (access, feedback, decisions).
8. Mark all boilerplate as legal-review placeholders.
9. Keep the SOW readable (short scope + precise tables).
10. Hand every SOW to legal review before signature on material deals.

## Error Decoder

| Symptom | Root cause | Fix |
|---|---|---|
| "That wasn't in scope" disputes | Vague scope boundary | One-sentence boundary + exclusions |
| "Done" fights | No acceptance criteria | Acceptance per deliverable + review window |
| Cash-flow gaps | Milestones ≠ spend | Align payments to cost curve |
| Change requests go unpaid | No change control | 15–20% trigger + written change flow |
| Legal redlines everything | Boilerplate improvised | Keep placeholders; reference MSA |

## Error Recovery

1. Identify the disputed clause (scope? acceptance? payment?).
2. Amend via the change-control flow in writing — never silently.
3. Update the assumptions register and the price if the trigger was crossed.
4. Log the clause that failed into the next SOW template so it is pre-closed.

## Cross-Skill Coordination

### Decision Gates & Artifacts

| Artifact | Consumed by | Trigger |
|---|---|---|
| Effort range + assumptions | this skill | from estimator skills |
| Pricing block | this skill | from services-engagement-pricing |
| Draft SOW | legal-advisor / client legal | signature |
| Scope boundary | software-maintenance-support-estimator | support annex later |

### Cross-Skill Upstream Inputs

| Upstream Skill | Input artifact |
|---|---|
| software-project-estimator / consulting-effort-estimator | effort low/base/high + assumptions |
| services-engagement-pricing | price, buffer, payment terms |
| legal-advisor | MSA/DPA context + review |

### Communication Triggers — When to Proactively Notify

- Scope or price changes ≥ 10% between quote and draft → re-sync with pricing before sending.
- Client asks to add legal terms not in the MSA → flag to legal review.
- Acceptance criteria disputed at kickoff → resolve in writing before work starts.

### Escalation Path

Escalate the *decision*, not the document: name the clause and the choice the client/lawyer
must make. Never sign an unreviewed SOW in regulated or high-value deals.

### Route to Other Skills

Money/price → `services-engagement-pricing` · effort → estimator skills · legal →
`legal-advisor` · support annex → `software-maintenance-support-estimator`.

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Quote accepted verbally | Send the SOW draft same day | Momentum closes deals; scope memory decays fast |
| Scope grows mid-project | Run change control now | The 15–20% trigger loses meaning if you wait |
| New engagement repeats an old shape | Reuse + improve the last SOW template | Each dispute closes a clause for the next one |
| Client has an MSA you haven't read | Read it before drafting | Duplicate terms become contradictions |

## State Log

Per SOW: inputs (estimate/pricing versions), structure model, scope sentence, deliverables
table hash, price/schedule, change-control trigger, MSA reference, version + date, legal
review status.

## Production Checklist

- [ ] Effort range + pricing block attached (versioned)
- [ ] Scope boundary = one enforceable sentence
- [ ] Deliverables table with acceptance definition per item
- [ ] Exclusions written
- [ ] Assumptions register present
- [ ] Price/schedule matches the pricing block exactly
- [ ] Change control (15–20% trigger + written flow) included
- [ ] MSA/DPA referenced (or "no MSA" stated)
- [ ] Legal boilerplate marked placeholder for review
- [ ] Version + signature block present
- [ ] Complete when every number in the SOW traces to an input or is TBD
- [ ] Complete when acceptance is testable per deliverable
- [ ] Complete when the draft has a named legal-review handoff
- [ ] Complete when a stranger could run the project from this document alone

## What Good Looks Like

A SOW a client's lawyer can act on and a delivery team can run from: parties and background
in two lines, one enforceable scope sentence, a deliverables table with testable acceptance,
milestone payments tied to provable events, a change-control clause with a real trigger, client
responsibilities, and clean placeholders for IP/warranty/liability that reference the MSA —
short enough to read, precise enough to enforce.

## Deliberate Practice

- Draft the same project as fixed-bid, T&M, and retainer to internalize the structural shifts.
- Re-read two past SOWs that produced disputes and rewrite the offending clauses.
- Time-box drafting: 45 minutes to a reviewable draft on a familiar shape.

## Anti-Patterns

- Sending the pricing email as the SOW.
- Scope as a paragraph of features with no boundary.
- Acceptance defined as "client happy".
- Milestones that don't cover your costs.
- Copying another firm's boilerplate without review.

## Anti-Rationalization

| Rationalization | Rebuttal |
|---|---|
| "The client trusts me; we don't need a SOW" | A one-page SOW protects both of you; scope fights cost **$1,000–$10,000** each. |
| "Acceptance criteria slow us down" | Unwritten acceptance is how "done" disputes start — a **$2,000–$8,000** argument per project. |
| "Legal boilerplate is standard" | Jurisdiction-specific terms signed blind can cost **$5,000–$50,000** in exposure. |
| "We'll add change control if scope grows" | Without a written trigger, scope grows first and the clause arrives too late. |

## Ground-Rules Enforcement Matrix

| Rule | Mechanical Trigger | Violation Response |
|---|---|---|
| Structure follows money | No model chosen before drafting | Pick Tree 1 skeleton first |
| Scope is a boundary | No one-sentence scope or exclusions | Write both before continuing |
| Acceptance testable | "Client happy" style acceptance | Define criteria + review window |
| Change control present | No 15–20% trigger / change flow | Add clause before finalizing |
| Numbers traceable | Untagged or invented figure | Tag [COMPUTED]/[TBD] or remove |
| Legal marked placeholder | Boilerplate presented as final | Mark "review" + route to legal |

## Failure Modes

- **Failure mode — vague scope boundary:** no one-sentence boundary + exclusions. When this
  fails, the worst case is **$1,000–$10,000** of scope disputes per engagement. Edge case:
  feature-by-feature lists without a boundary sentence.
- **Failure mode — untestable acceptance:** "done when client is happy." When that fails,
  acceptance fights stall payment by weeks (cash-flow impact **$2,000–$8,000**). Exit
  condition: acceptance criteria + review window per deliverable.
- **Failure mode — milestone/cash-flow mismatch:** payments land after costs. Worst case: you
  finance the project (**10–30% of contract value** tied up). Known limitation of 100%
  back-loaded billing — align schedule to spend.
- **Failure mode — no change control:** scope grows past 15–20% unpaid. When this fails,
  absorbed scope hits **$3,000–$15,000**. Known limitation of verbal change agreements —
  written change-request flow required.

## Gotchas

- A missing scope boundary sentence is the **$1,000–$10,000** mistake per project.
- Acceptance without a review window lets "done" float for weeks — worth **$2,000–$8,000** in
  stalled cash per milestone.
- Copying boilerplate from another jurisdiction can cost **$5,000–$50,000** if enforced
  wrongly — keep placeholders until lawyer review.
- Ignoring an existing MSA creates contradictions that lawyers bill **$1,000–$5,000** to
  untangle.
- Back-loaded payment schedules (100% at the end) make you the client's bank — finance
  10–30% of contract value until acceptance.

## Verification

| Check | Complete when |
|---|---|
| Inputs | Effort + price attached with versions |
| Structure | Money model chosen (Tree 1) and skeleton matches |
| Scope | One-sentence boundary + exclusions written |
| Deliverables | Table with per-item acceptance + dates |
| Assumptions | Register present and consistent with price |
| Money | Price/milestones match the pricing block exactly |
| Change control | 15–20% trigger + written change flow present |
| MSA/DPA | Referenced or "no MSA" stated |
| Legal | Boilerplate marked placeholder; legal handoff named |
| Versioned | Version + date + signature block present |
| Traceable | Every number traces to input or is TBD |
| Runnable | A stranger could execute the project from this SOW |

## Verification Guardrails

- No effort/price inputs → return an outline with TBD blocks, never a priced draft.
- Acceptance not testable → rewrite before output.
- Boilerplate not marked for review → mark it and name legal review before sending.

## References

- [`references/patterns-catalog.md`](references/patterns-catalog.md) — SOW section templates,
  milestone tables, acceptance definitions, clause guidance, dollar context.
- `services-engagement-pricing` (price block), estimator skills (effort), `legal-advisor`
  (review), `docs/client-request-playbook.md` (engagement routing).

<!-- QUICK: 30s --> <!-- structure follows money (Tree 1) -->
<!-- QUICK: 30s --> <!-- scope = boundary + exclusions, not a feature list -->
<!-- QUICK: 30s --> <!-- every number traces to an input or is TBD -->
