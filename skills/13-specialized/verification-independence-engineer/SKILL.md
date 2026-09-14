---
name: verification-independence-engineer
description: >
  Use when designing who checks the work in an agent or workflow system — separating the
  producer from the verifier, making a validator genuinely independent, or diagnosing a system
  whose checks pass while its outcomes get worse. Handles the producer/verifier split, the
  information boundary a validator may see (conclusion and evidence, never the producer's
  reasoning), independence in model and context lineage, validator calibration against
  known-bad cases, rejection-rate monitoring so a rubber stamp is visible, and paired harm
  metrics that guard a target against the intent it can betray. Do NOT use for reviewing a
  specific code change (code-reviewer, doubt-driven-development), confirming a change is done
  (verification-before-completion), judge rubrics and eval datasets (agent-eval-pipeline),
  manifest authoring (workflow-graph-authoring), or run cost (cost-accounting).
author: Sandeep Kumar Penchala
license: MIT
type: specialized
status: stable
version: 1.0.0
updated: 2026-09-13
tags:
  - verification
  - validator
  - independence
  - self-verification
  - goodhart
  - goal-blindness
  - metric-gaming
  - reward-hacking
  - evaluator-optimizer
  - judge-calibration
  - agent-verification
token_budget: 3500
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  examples:
    - skills/13-specialized/verification-independence-engineer/examples/backtest
  consumes_from:
    - verifier-design
    - workflow-graph-authoring
    - multi-agent-orchestration
    - agent-eval-pipeline
    - system-architect
    - product-analyst
    - observability-engineer
    - cost-accounting
  feeds_into:
    - agent-eval-pipeline
    - multi-agent-orchestration
    - workflow-graph-authoring
    - agent-handoff-protocol
    - code-reviewer
    - tdd-guide
    - observability-engineer
    - contract-completeness-review
workflow:
  artifacts:
    inputs: [agent-system-design, quality-metric]
    outputs: [verification-independence-plan]
  completion:
    criteria:
      - Every check names a verifier that is not the producer of the artifact it judges
      - Every validator declares its information boundary — conclusion and evidence only, never the producer's chain of thought
      - Every validator declares how it differs from the producer (model, context lineage, or both)
      - Every validator is calibrated against known-bad cases, and its rejection rate is observed
      - Every optimised target has a paired harm metric that guards the intent the target can betray
    evidence: required
  escalate_to: [human-gate]
---

# Verification Independence Engineer

> **Portability target:** Spec-level. This skill encodes domain expertise, not tool-specific commands.

Design who checks the work, so the check is a real check rather than the producer agreeing with itself.

## Route the Request **(QUICK)**

### Auto-Route (No User Input Required)

| ID | Signal | Route to |
|----|--------|----------|
| A1 | `file_contains("*.yaml", "verdict\|evaluator\|reviewer\|judge")` in a workflow manifest | **Independence Audit** — read the graph, map producer→verifier pairs, then Decision Tree 1 |
| A2 | A node's inputs include its own outputs, or a loop whose `exit_when` reads the producing node's verdict | **Self-Verification** — Decision Tree 1, rule R1 |
| A3 | A validator node declared with the same model or context lineage as the producer | **Independence Gap** — Decision Tree 2 |
| A4 | A metric, KPI, or `exit_when` that has no paired guard against the harm it could cause | **Goal-Blindness Risk** — Decision Tree 4 |
| A5 | A validator with no recorded rejection rate, or a pass rate of 100% | **Rubber-Stamp Check** — Decision Tree 3 |
| A6 | Quality is passing while users, revenue, or retention are degrading | **Metric Betrayal** — Decision Tree 4, then Error Decoder |

### Intent Route (Ask the User)

```
├── "is the same agent allowed to check its own work?"   → Independence (Decision Tree 1)
├── "what should the reviewer see?"                      → Information boundary (Decision Tree 2)
├── "how do we know the checker is any good?"             → Calibration (Decision Tree 3)
├── "our metrics are green but the business is worse"     → Goal blindness (Decision Tree 4)
└── "review whether our verification is real"             → Full workflow, all four trees
```

## Anti-Rationalization **(QUICK)**

| Rationalization | Why it is wrong | Required response |
|------------------|-----------------|-------------------|
| "It checks its own output before answering." | That is the producer grading itself with the reasoning that produced the output. If the reasoning was flawed, the check inherits the flaw. | Split the roles (R1); a self-check is a draft, not a verification. |
| "It is a different agent, so it is independent." | Two agents sharing a model, a context, or a prompt lineage share the blind spots. Separateness is not independence. | State and verify the independence properties: model, context, information (R3, R6). |
| "It is a different model, so it is definitely better." | A validator that has never rejected anything is a rubber stamp, whatever model runs it. | Calibrate against known-bad cases and watch the rejection rate (R5). |
| "The reviewer sees everything, so it has maximum context." | Giving the validator the producer's chain of thought makes it inherit the producer's reasoning — including its errors. | Enforce the information boundary: conclusion and evidence only (R2). |
| "Resolution rate is up, so the agent is working." | A metric alone is a target; the agent will satisfy it by whatever path is cheapest, including paths that betray why the metric existed. | Pair the target with a harm metric before optimising it (R4). |
| "Verification slows us down." | Verification that catches a failure before delivery is cheaper than the re-run, the rollback, or the churn that finds it later. | Cost the re-work the validator prevented, not the validator's own tokens. |

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| **R1** | **REFUSE to let a producer verify its own output.** The node that produced an artifact may not be the node that approves it. | Verifier reads the producer's outputs *and* is the same node, session, or role; or a loop's `exit_when` reads the producing node's own verdict | STOP. Respond: "This node is both the athlete and the referee. Its verdict is a restatement of its own reasoning, so a flawed producer produces a flawed approval. Name a separate verifier node, or accept that this is a draft and not a verified result." |
| **R2** | **REFUSE to give a validator the producer's chain of thought.** A validator must see the conclusion and the evidence — never the reasoning that produced them. | Verifier's inputs include the producer's reasoning trace, scratchpad, or full transcript rather than its artifact and evidence | STOP. Respond: "If the validator reads the reasoning, it inherits the reasoning's blind spots — it will agree for the same wrong reason. Give it the claim and the evidence that is supposed to support the claim. Withhold the reasoning." |
| **R3** | **REFUSE to call two agents independent when they share a model and a context lineage.** Independence requires a declared, verifiable difference. | Producer and verifier use the same model with no fresh context, or the verifier's context is seeded from the producer's session | STOP. Respond: "These two share blind spots, so agreement between them is weak evidence. State how the verifier differs — a different model, or at minimum a fresh context that never saw the producer's session. Prefer both." |
| **R4** | **REFUSE to optimise a metric that has no paired harm metric.** A target without a guard is an instruction to satisfy the number by any available path. | Metric used in a gate, `exit_when`, or reward with no counter-metric guarding the intent it could betray | STOP. Respond: "What does this number exist to protect, and what would go up if it were gamed? Name the harm metric that must not degrade while this improves. Without it, the loop optimises the metric against its own purpose." |
| **R5** | **REFUSE to trust a validator that has never rejected anything.** An uncalibrated validator is a rubber stamp with a verdict field. | Verifier's rejection rate is unmeasured, is zero, or is not observed over a known-bad set | STOP. Respond: "Has this validator ever failed something that was genuinely bad? Show its agreement with known-bad cases. A validator that approves everything provides no signal — it makes failure harder to see, not easier." |
| **R6** | **REFUSE to claim independence without stating and verifying the properties.** "It is a separate agent" is a description, not a proof. | Independence asserted in prose with no declared model, context, information boundary, or authority difference | STOP. Respond: "State the four properties — which model, which context, what the validator may see, and what authority its verdict has. Then show the check that enforces each. Unstated independence is assumed independence." |

## Anti-Hallucination

- **Admit uncertainty.** If you do not have the validator's rejection rate, its calibration results, or the harm metric's baseline, say so and mark derived figures ESTIMATED. Never present an assumed rejection rate as measured.
- **Flag your knowledge cutoff.** Model families, judge implementations, and framework APIs change. State that a specific validator implementation must be confirmed against the installed version rather than recalled from a description.
- **Never guess security.** If a validator's verdict is the only thing standing between a flawed artifact and a user, and that validator is uncalibrated, treat it as no protection at all. Escalate rather than approve.
- **[VERIFIED] provenance.** Tag every figure `[VERIFIED]` (measured, with the source named), `[COMPUTED]` (derived, with the formula), or `[ESTIMATED]` (assumed, with the assumption written down).

## The Expert's Mindset **(QUICK)**

The core failure this skill addresses is structural, not behavioural: **the producer is also the referee.** A system that executes a task and then evaluates its own execution is using the same reasoning for both. If that reasoning contains an error, the evaluation does not catch it — it reproduces it. Prompting the producer to "check your work" changes the wording, not the structure.

The fix is equally structural: **separate the producing node from the verifying node.** Once they are separate, the interesting questions are all about *how separate*. Three properties decide whether a check is real, and they are independent of each other:

1. **Model independence** — a different model has different blind spots. Same model, same blind spots, and the check is weak.
2. **Context independence** — a verifier with a fresh context has not been led by the producer's framing. This is the cheapest form of independence and the one most often missing.
3. **Information independence** — the verifier sees the claim and the evidence, not the reasoning. A verifier that reads the producer's chain of thought inherits its errors and will agree for the same wrong reason.

The second half of the discipline is about the **target**, not the checker. A system optimised to move a number will move that number — by any path the environment permits. This is not malice; it is the metric working exactly as specified. The failure is that the metric was specified as a *proxy* for something the specifier cared about, and the proxy and the intent diverge as soon as the proxy becomes the target. The discipline is therefore: **for every optimised metric, name the harm it could cause and measure that too.** The number that matters is not "did the metric improve" but "did the metric improve while the thing it stood for did not get worse".

## What Verification Masters Know **(STANDARD)**

- **A pass rate is not a quality signal until you know the rejection rate.** A validator that approves 100% of artifacts is indistinguishable from a validator that is not running.
- **Calibration is what makes a verdict evidence.** Feed the validator cases you already know are bad; if it approves them, its approvals mean nothing everywhere else.
- **The strongest validator is the one that can be wrong on purpose.** A validator whose only job is to find fault, and which is rewarded for correct rejections, behaves differently from one rewarded for agreement.
- **The information boundary is the whole game.** Most "independent" validators are independent in name only because they were handed the producer's transcript.
- **Metrics are proxies, and every proxy leaks.** The leak is invisible until you measure what the proxy was standing in for.
- **Re-work cost is the honest comparison, not validator cost.** A validator that costs 5% more per run and removes one full re-run per ten is not expensive.

### When to Break Your Own Rules **(DEEP)**

- **A genuinely trivial artifact may need no independent verifier** — a deterministic transformation with a code assertion checks itself. Say so; do not let "we skipped verification here" become a habit for artifacts that are not trivial.
- **A deterministic check may legitimately replace a model validator** — a test suite, a schema assertion, or a type check is fully independent and free of shared blind spots. Prefer code over a judge wherever the property is mechanically checkable.
- **A validator may share the model when the property checked is mechanical** — if the check is "does this field exist", model diversity adds nothing. State that the property is mechanical, not judgmental.
- **A target may be optimised alone when a harm metric is genuinely not measurable.** Record the gap explicitly as an accepted risk with an owner, rather than pretending the guard exists.

## Deliberate Practice **(STANDARD)**

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Take a checklist you use and mark which items are self-checked versus independently checked | 20 min | Every item labelled producer or verifier |
| Intermediate | Build a known-bad set of 10 artifacts your validator must reject | 1 h | The validator rejects all 10, and you know its rejection rate |
| Advanced | Take a system whose checks pass and find one target with no harm metric | 2 h | A paired harm metric, with a baseline and a threshold |
| Expert | Prove a validator's independence on all three axes and show the enforcement for each | 1 day | A written independence statement plus a test per property |

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
- **Scope:** Adds a review step after generation
- **Autonomy:** Runs a check when told to
- **Impact:** Catches the obvious; approval is still producer-shaped
- **Craft:** Knows a check exists and is separate

### L2: Practitioner
- **Scope:** Fresh-context verifier on the artifact and evidence only
- **Autonomy:** Designs the split for a feature
- **Impact:** Verifier is not led by the producer's framing
- **Craft:** Enforces the information boundary; withholds the reasoning

### L3: Senior
- **Scope:** Different-model validator, calibrated against known-bad cases
- **Autonomy:** Owns verification for a system
- **Impact:** Validator approvals are evidence, not ceremony
- **Craft:** Measures rejection rate; recalibrates on model changes

### L4: Staff / Principal
- **Scope:** Paired harm metrics, verifier authority, escalation design
- **Autonomy:** Sets verification standards across systems
- **Impact:** No optimised target can be gamed without a visible harm signal
- **Craft:** Designs the metric pair before the optimisation begins

### L5: Transformative
- **Scope:** Verification and objective design co-designed; independence is a system property
- **Autonomy:** Owns how the organisation decides what "good" means
- **Impact:** Improvement in a number is trusted because the intent is measured alongside it
- **Craft:** Turns "did we improve" into a question with a defensible answer

## When to Use **(QUICK)**

| Use this skill | Use a neighbour instead |
|----------------|------------------------|
| Splitting producer and verifier in an agent system | `multi-agent-orchestration` — topology selection and shared state |
| Deciding what a validator may see | `agent-handoff-protocol` — payload and state transfer mechanics |
| Making a validator's verdict trustworthy | `agent-eval-pipeline` — judge rubrics, datasets, statistical gates |
| Pairing a metric with a harm guard | `product-analyst` — designing and reading the business metric |
| Reviewing one specific code change | `code-reviewer`, `security-reviewer` |
| Adversarial review of high-stakes code | `doubt-driven-development` |
| Confirming a change is actually done | `verification-before-completion` |
| Authoring the manifest once the shape is chosen | `workflow-graph-authoring` |
| Costing the verification versus the re-work | `cost-accounting` |

## When NOT to Use **(QUICK)**

1. **The question is which topology to use (supervisor, debate, swarm)** — use `multi-agent-orchestration`; this skill assumes the nodes exist and asks whether the check between them is real.
2. **The question is how state moves between agents** — use `agent-handoff-protocol`; payload design is a different concern from independence.
3. **The task is designing a judge rubric, eval dataset, or statistical gate** — use `agent-eval-pipeline`; this skill produces the *independence requirements* that pipeline must satisfy.
4. **The task is reviewing one artifact** — use `code-reviewer` / `security-reviewer` / `doubt-driven-development`; this skill designs the reviewing role, it does not perform a review.
5. **The property is mechanically checkable** — write a test, a schema assertion, or a type check instead. A code check is more independent and cheaper than any model validator.

## Decision Trees **(STANDARD)**

### Decision Tree 1: How much verification structure does this need?

```
Is the artifact's correctness mechanically checkable (test, schema, type, assertion)?
├── Yes → DETERMINISTIC CHECK. Fully independent, free of shared blind spots. Prefer this.
└── No ↓
    Is the artifact consequential (ships to users, moves money, changes state irreversibly)?
    ├── No → SELF-CHECK is acceptable. Record that it is a draft, not a verification.
    └── Yes ↓
        Is a single judgment enough, or does the decision warrant disagreement?
        ├── Single judgment → INDEPENDENT VALIDATOR NODE
        │     • different producer node (R1)
        │     • fresh context (R3)
        │     • conclusion + evidence only (R2)
        │     • calibrated against known-bad cases (R5)
        └── Warrants disagreement → ADVERSARIAL VALIDATOR
              • one node whose only job is to find fault
              • rewarded for correct rejections (R5)
              • plus the independent validator above
              And if the outcome is irreversible → HUMAN GATE
```

### Decision Tree 2: What may the validator see?

```
Does the property require judging the CLAIM against the EVIDENCE?
├── Yes → CLAIM + EVIDENCE ONLY.
│         Withhold: producer's reasoning, scratchpad, transcript, prior self-assessment.
│         Test: re-run the validator with the reasoning attached — if its verdict moves,
│               the boundary is not enforced (R2).
└── No, it requires judging the PROCESS (was the method sound?) ↓
    Judging a process from a transcript is only valid if the transcript IS the artifact
    (e.g. a compliance record).
    ├── The transcript is the artifact → the producer's reasoning is in scope. State this
    │     explicitly and accept that shared blind spots are possible (R3).
    └── The transcript is not the artifact → you are asking the validator to grade the
          producer's thinking, which is the producer's job. Return to claim + evidence.
```

### Decision Tree 3: How do we know the validator works?

```
Do we have cases we already know are bad?
├── No → BUILD THE KNOWN-BAD SET FIRST.
│         Collect ≥10 historical failures, near-misses, or seeded defects.
│         A validator cannot be calibrated without something it should reject.
└── Yes ↓
    Does the validator reject them?
    ├── No → the validator is a rubber stamp (R5).
    │     Check, in this order:
    │       1. Does it actually see the artifact? (wiring)
    │       2. Are its criteria specific enough to fail anything?
    │       3. Is its information boundary so wide it adopted the producer's reasoning? (R2)
    └── Yes ↓
        Is the rejection rate observed in production?
        ├── No → instrument it. Track rejections per artifact class, not a single total.
        └── Yes → is the rate plausible?
              • ~0% on consequential work → the producer is either perfect or the validator is blind
              • ~100% on consequential work → the criteria are wrong, or the producer is not trying
              • stable and non-trivial → this is what a working validator looks like
```

### Decision Tree 4: Is this metric safe to optimise?

```
What does this metric stand for? (write the intent, not the number)
├── If you cannot state the intent → STOP. You are about to optimise a number nobody owns.
└── Stated ↓
    What path could satisfy the number while betraying the intent?
    ├── Cannot find one → look harder. Every proxy has a leak; a proxy with no known leak
    │     means the search was shallow.
    └── Found one or more ↓
        Is that path measurable?
        ├── Yes → PAIRED HARM METRIC. Gate on both:
        │     the target improves AND the harm metric does not degrade.
        └── No → record it as an accepted risk with a named owner and a review date.
              Do not let "unmeasurable" read as "not happening".
```

## Core Workflow **(STANDARD)**

| Phase | Time | What you do | Complete when |
|-------|------|-------------|---------------|
| **1. Map the split** | 20 min | List every artifact and who produces it; mark who approves it | Complete when every artifact has a named producer and a named verifier (R1) |
| **2. Find the self-checks** | 15 min | Locate nodes whose verdict reads their own output | Complete when each self-check is either replaced by a verifier or recorded as a draft |
| **3. Declare independence** | 25 min | For each producer→verifier pair, state model, context, information boundary and authority | Complete when all four properties are declared (R6) |
| **4. Enforce the boundary** | 20 min | Restrict verifier inputs to the artifact and evidence; withhold reasoning | Complete when a test shows the verdict does not move when reasoning is hidden (R2) |
| **5. Calibrate** | 30 min | Build a known-bad set and measure the rejection rate | Complete when the validator rejects the known-bad set and the rate is instrumented (R5) |
| **6. Find the targets** | 20 min | List every gate, `exit_when`, and reward metric | Complete when each target has a stated intent |
| **7. Pair the guards** | 25 min | For each target, name the harm it could cause and measure it | Complete when every optimised target has a paired harm metric or a recorded accepted risk (R4) |
| **8. Verify the verification** | 30 min | Run the verification sequence | Complete when all six checks pass |
| **9. Record** | 10 min | Log the independence statement and the metric pairs | Complete when each verdict's authority and each metric's guard are recorded |

## Best Practices **(STANDARD)**

1. **Prefer a code check to a model check.** Determinism has no blind spots to share, and it is cheaper.
2. **Withhold the reasoning, not the evidence.** The validator needs the claim and its support; it does not need the story.
3. **Make the verifier's job to falsify.** A verifier asked "is this good?" agrees; a verifier asked "find the flaw" works.
4. **Calibrate before trusting.** A validator's verdicts are only evidence after it has rejected things you know are bad.
5. **Instrument the rejection rate per artifact class.** A single aggregate passes the same way a single hit rate does — by hiding the class that matters.
6. **State independence as four properties, not as a word.** Model, context, information, authority (R6).
7. **Give the validator authority proportional to its independence.** A fresh-context reviewer cannot block a ship; an independent, calibrated validator can.
8. **Write the intent before the number.** A metric whose purpose is unwritten cannot be guarded.
9. **Gate on the pair, never the target alone.** "Resolution rate up AND churn flat" is a decision; "resolution rate up" is a trap.
10. **Re-verify on model change.** Validator agreement is model-specific; a model swap invalidates the calibration.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Verifier approves nearly everything | Same model and context as the producer; or criteria too vague to fail anything | Fresh context, different model, specific criteria; calibrate against known-bad cases (R3, R5) | Independence is a property, not a label |
| Verdict changes when you hide the reasoning | The validator was reading the producer's chain of thought and adopting it | Enforce claim + evidence only; add the hiding test (R2) | A validator that inherits reasoning inherits its errors |
| Quality gates green, users leaving | A target optimised with no harm metric; the cheapest path betrayed the intent | Name the intent, find the leak, add the paired harm metric (R4) | The metric worked exactly as specified |
| Checks pass, then the same defect ships | The "check" is the producer's own output, restated | Split into a distinct verifier node with its own verdict (R1) | Self-verification is a draft |
| Two agents agree, both wrong | Shared model and shared context lineage | Declare and verify model and context difference; prefer both (R3, R6) | Agreement between twins is one opinion |
| Verifier rejects almost everything | Criteria mis-specified, or the producer is not attempting the task | Inspect the criteria against the intent; fix the upstream, not the threshold | 100% rejection is as uninformative as 0% |
| Cannot prove the validator is independent | Independence was asserted in prose only | Write the four properties and one test per property (R6) | Unstated independence is assumed independence |
| Validator silently stopped being called | Wiring drift; no assertion that the verifier ran | Assert the verifier executed and produced a verdict; alert on absence | An unrun validator reports nothing, including failure |

## Error Recovery **(QUICK)**

| Symptom | First Action | If That Fails | Last Resort |
|---------|--------------|--------------|------------|
| Approvals look like a rubber stamp | Build a known-bad set and measure the rejection rate (R5) | Replace the validator with a different model and a fresh context (R3) | Replace judgment with a deterministic check where the property allows |
| Reasoning leakage suspected | Run the hiding test: hide the reasoning, re-run, compare verdicts (R2) | Restrict the verifier's inputs at the graph edge, not in the prompt | Rebuild the verifier as a separate node with no producer context |
| Metric green, outcome bad | Write the metric's intent, then hunt the cheapest satisfying path (R4) | Add the paired harm metric and re-read history with both | Escalate the objective itself — the metric may be the wrong proxy |
| Cannot show independence | Declare the four properties for the pair (R6) | Add model diversity where it is absent (R3) | Downgrade the verdict to advisory and add a human gate |
| Verifier disagrees with the human reviewer | Calibration drift, or the criteria encode the wrong intent | Re-calibrate on the disputed cases with the human as the anchor | Raise to `human-gate` and record the dispute; do not silently override either |

**Hard failure boundary:** After 3 failed recovery attempts, escalate to a human. Do not loop.

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|---------------|----------------|----------------------|
| `workflow-graph-authoring` | The manifest: nodes, edges, `exit_when` conditions | Locate producer→verifier pairs and self-reading gates |
| `multi-agent-orchestration` | Topology and role assignment | Know which agents exist before asking whether the check between them is real |
| `agent-eval-pipeline` | Judge configuration and calibration results | Reuse existing calibration rather than duplicating it |
| `system-architect` | Service topology and authority boundaries | Place the verifier where its authority can actually block |
| `product-analyst` | The business metric and its stated intent | Pair the target with the harm it can cause |
| `observability-engineer` | Existing metrics and alerting | Instrument rejection rate by artifact class |
| `cost-accounting` | Per-run and per-node cost | Cost the verification against the re-work it prevents |

### Downstream (What This Skill Produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|-----------------|------------|------------------------|
| `agent-eval-pipeline` | Independence requirements for the judge | Calibrate the judge and honour the information boundary |
| `multi-agent-orchestration` | Producer/verifier split and authority | Wire the roles as distinct nodes |
| `workflow-graph-authoring` | Independence assertions per edge | Enforce the information boundary in the manifest |
| `agent-handoff-protocol` | The exact payload a verifier may receive | Build the payload so reasoning is excluded by construction |
| `code-reviewer` | The reviewing role's independence properties | Run reviews that do not inherit the author's framing |
| `tdd-guide` | The property list that should be mechanically checked | Turn judgment-shaped checks into deterministic tests |
| `observability-engineer` | Rejection-rate and paired-harm metrics | Alert on a validator that stops rejecting |

## Proactive Triggers **(STANDARD)**

- **A node's verdict reads its own output** → Flag self-verification before the run ships (R1). 🔴
- **A validator is declared with the producer's model and no fresh context** → Flag the independence gap (R3). 🔴
- **A verifier's inputs include a reasoning trace or full transcript** → Flag the boundary breach (R2). 🔴
- **A gate, `exit_when`, or reward metric has no paired harm metric** → Flag goal-blindness risk (R4). 🟡
- **A validator's rejection rate is unmeasured or zero** → Flag the rubber stamp (R5). 🟡
- **Independence is asserted without the four properties** → Require the statement and the tests (R6). 🟠

## Anti-Patterns **(STANDARD)**

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ **Self-verification** — the producer approves its own output | ✅ A separate verifier node with its own verdict (R1) |
| ❌ **Transcript hand-off** — the validator reads the producer's reasoning | ✅ Conclusion and evidence only (R2); test it by hiding the reasoning |
| ❌ **Twin agents** — "independent" verifier sharing model and context | ✅ Declared model and context difference; prefer both (R3) |
| ❌ **Uncalibrated judge** — a validator that has never rejected anything | ✅ A known-bad set, a measured rejection rate (R5) |
| ❌ **Bare target** — optimising a metric with no harm guard | ✅ Paired harm metric, gated together (R4) |
| ❌ **Prose independence** — "it is a separate agent, so it is unbiased" | ✅ Four declared properties with a test each (R6) |
| ❌ **Reasoning-shaped checks** — using a judge where a test would do | ✅ A deterministic check: schema, type, assertion |
| ❌ **Advisory verifier** — a verdict with no authority to block | ✅ Authority proportional to independence; human gate for irreversible |

## State Log **(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Producer/verifier split | Deterministic check for the schema-shaped properties; independent validator node for the judgment-shaped ones | Judgment-shaped checks still depend on a model | Validator calibrated against a known-bad set; rejection rate instrumented |
| 2 | Metric pairing | Resolution rate gated with churn and reopen rate, not alone | The harm metric may lag the target | Read both on the same cadence; no gate on a single number |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still within scope?
3. Has any new information invalidated prior decisions?
4. Has a verifier's inputs, model, or authority changed without a new State Log row? If so, the independence claim has drifted from its basis.

## Production Checklist **(STANDARD)**

- [ ] **CR1: Producer/verifier split declared** — Verification: every consequential artifact names a verifier that is not its producer (R1)
- [ ] **CR2: No self-reading verdict** — Verification: no gate or `exit_when` reads the producing node's own verdict
- [ ] **CR3: Information boundary enforced** — Verification: verifier inputs exclude reasoning traces; the hiding test does not move its verdict (R2)
- [ ] **CR4: Model difference declared** — Verification: every validator states its model relative to the producer's (R3)
- [ ] **CR5: Fresh context verified** — Verification: the validator's context is not seeded from the producer's session (R3)
- [ ] **CR6: Known-bad set exists** — Verification: ≥10 known-bad artifacts the validator is expected to reject (R5)
- [ ] **CR7: Rejection rate instrumented** — Verification: rejections are tracked per artifact class, with an alert on a validator that stops rejecting
- [ ] **CR8: Independence properties written** — Verification: model, context, information and authority stated per pair, with a test each (R6)
- [ ] **CR9: Target intents stated** — Verification: every optimised metric has a written intent, not just a formula (R4)
- [ ] **CR10: Harm metrics paired** — Verification: every optimised target is gated together with its harm metric, or the gap is a recorded accepted risk with an owner (R4)
- [ ] **CR11: Verifier authority defined** — Verification: each verdict states what it can block, and irreversible outcomes route to a human gate
- [ ] **CR12: Re-calibration trigger defined** — Verification: a model change forces re-calibration of the affected validator

## What Good Looks Like **(QUICK)**

A system where every consequential artifact is approved by a node that did not produce it, the approving node sees the claim and the evidence but never the producer's reasoning, its independence is stated as four verifiable properties rather than asserted, it has rejected things known to be bad so its approvals carry signal, and every optimised metric is gated together with a measure of the harm that metric could cause. The team can answer "who checked this, why is their check real, and what could this number be hiding?" for any gate in the system.

**Signs of Excellence:**
- No artifact is approved by its producer
- A validator's rejection rate is a watched number, not an assumption
- Hiding the producer's reasoning does not change the validator's verdict
- Every green metric has a named intent and a paired guard

**Signs of Dysfunction:**
- "It reviews its own output before answering"
- A validator that has never said no
- A metric optimised with nobody able to state what it was protecting
- Approval rate described as quality

## Verification

Run this sequence. Do not proceed past a failure.

1. **Split check.** Does every consequential artifact have a verifier that is not its producer? If any gate reads the producing node's own verdict, stop and fix R1.
2. **Boundary check.** Does the verifier receive the claim and the evidence only? Hide the producer's reasoning and re-run — if the verdict moves, stop and fix R2.
3. **Independence check.** Are model, context, information and authority declared for each pair, each with a test? If independence is prose only, stop and fix R6.
4. **Calibration check.** Does a known-bad set exist, and does the validator reject it? If the rejection rate is unmeasured or zero, stop and fix R5.
5. **Intent check.** Does every optimised metric have a written intent? If not, stop and write it before the metric is gated on.
6. **HARM-PAIR check.** Is every optimised target gated together with a harm metric, or a recorded accepted risk with an owner? If neither, stop and fix R4.

**Pass criteria:** All six checks pass before the system is trusted.

## Verification Guardrails **(STANDARD)**

### Pre-Generation
- [ ] The artifact list and its producers are known
- [ ] Existing calibration data for any judge is located, not duplicated
- [ ] The business metric and its stated intent are available

### Post-Generation
- [ ] No verdict belongs to the producer of the artifact it judges
- [ ] No validator input includes a reasoning trace
- [ ] No optimised target is gated without its harm metric or a recorded accepted risk
- [ ] Independence is stated as four properties with a test each

## References **(QUICK)**

- `references/additional-resources.md` — index of the focused reference files (independence
  properties, the metric-leak catalogue, calibration recipes, failure narratives, verification
  recipes, sources, related reading)
- `scripts/verify-skill.sh` — runnable verification harness for this skill
- Related: `agent-eval-pipeline`, `multi-agent-orchestration`, `workflow-graph-authoring`, `doubt-driven-development`, `verification-before-completion`

## Failure Modes **(STANDARD)**

The ways verification loses its signal, in the order they usually appear. Each is a failure mode of
the *check*, not of the work being checked — the dangerous direction, because a broken check reports
success.

| Failure mode | What it looks like | Why it happens | Detection | Fix |
|--------------|--------------------|----------------|-----------|-----|
| **Rubber stamp** | Approvals near 100%; every escaped defect had been approved | Same model and context as the producer, or criteria too vague to fail anything | Rejection rate per artifact class, observed over time | Known-bad set, fresh context, different model (R3, R5) |
| **Inherited reasoning** | The verdict changes when the reasoning is hidden | The validator was handed the producer's chain of thought | The hiding test — hide the reasoning, re-run, compare verdicts | Enforce claim + evidence only (R2) |
| **Twin agreement** | Two agents agree closely and are both wrong | Shared model family *and* shared context lineage | Declare model and context per pair; measure divergence | Model diversity plus a fresh context (R3) |
| **Goal blindness** | Gate green while the outcome it stood for degrades | A target optimised with no paired harm metric | Read the metric's intent; look for the cheapest satisfying path | Pair the target with a harm metric (R4) |
| **Ornamental gate** | A verdict with no authority to block, ignored under pressure | Authority not matched to independence | Ask what the verdict has ever blocked | Proportional authority; human gate for irreversible outcomes |
| **Decayed calibration** | Approval quality quietly drops after a model change | Calibration is model-specific and is not re-run | Compare the calibration record's model to the live one | Re-calibrate on model change (CR12) |
| **Unrun verifier** | Checks pass because nothing executed | Wiring drift; no assertion that the verifier ran | Assert a verdict exists; alert on its absence | Fail closed when a verifier produces no verdict |
| **False alarm inflation** | Engineers re-run until it passes; a real defect slips through | Precision never measured; criteria too strict | Track false-reject rate, not just rejection rate | Calibrate precision; fix the criteria, not the threshold |

**The worst of these is the one that looks healthiest.** Every failure mode above reports success
while correctness degrades — which is why the response is never "raise the pass rate" but "make the
verdict mean something" (R5) and "gate on the pair, not the target" (R4).

## Gotchas **(STANDARD)**

| Gotcha | Cost if missed | Fix |
|--------|----------------|-----|
| Verifier reads the producer's reasoning | It agrees for the same wrong reason; failures are invisible. An escaped defect of this class typically costs **$100,000–$1,000,000+** in incident response and remediation | Claim + evidence only; the hiding test (R2) |
| "Independent" verifier shares model and context | Agreement between twins is one opinion, counted twice — the class of defect that survives review, commonly **$50,000–$500,000** per escaped release | Declare and verify model and context difference (R3) |
| Validator never rejects anything | Failure becomes harder to see; approvals carry no signal. Diagnosis and rework typically **$10,000–$75,000** | Known-bad set, rejection rate (R5) |
| Bare target with no harm metric | The loop optimises the number against its own purpose; the correction is measured in lost revenue, not tokens | Paired harm metric, gated together (R4) |
| Independence asserted in prose | Unverifiable, so it decays at the first model swap — re-auditing a fleet typically costs **$25,000–$150,000** | Four properties, one test each (R6) |
| Judge used where a test would work | Shared blind spots where none were necessary; every affected decision inherits them | Deterministic check: schema, type, assertion |
| Verifier with no authority to block | Advisory reviews are ignored under delivery pressure; the check is paid for and not used | Authority proportional to independence; human gate for irreversible |
| Calibration not re-run after a model change | Stale calibration silently invalidates every approval — a silent-recall failure, not a crash | Re-calibrate on model change (CR12) |
| Rejection rate aggregated | The class that matters is hidden, exactly as with a global hit rate | Track per artifact class |
| Harm metric added but not gated | It is reported, read, and ignored when the target is green; support cost **$5,000–$50,000** per incident | Gate on the pair, never the target alone |

> **Cost figures are [ESTIMATED]** — order-of-magnitude incident-cost ranges synthesised from
> incident-response cost reporting, not audited per-organisation figures. Measure on your own
> workload before quoting them.
