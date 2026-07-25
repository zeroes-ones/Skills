---
name: doubt-driven-development
description: >
  Use when building safety-critical or high-stakes software where defects have
  disproportionate cost. Handles adversarial fresh-context code review, claim
  extraction and verification, doubt injection cycles, and reconciliation
  tracking. Do NOT use for prototyping, spike solutions, or throwaway code
  where the cost of review exceeds the cost of defects.
license: MIT
author: Sandeep Kumar Penchala
type: ai-engineering
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - adversarial-review
  - claim-extraction
  - doubt-injection
  - code-review
  - safety-critical
  - defect-prevention
token_budget: 4800
chain:
  consumes_from:
    - code-reviewer
    - security-reviewer
    - system-architect
    - qa-engineer
  feeds_into:
    - code-reviewer
    - security-reviewer
    - incident-responder
    - release-manager
    - compliance-officer
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---
# Doubt-Driven Development
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "We already do code review — adversarial review is redundant." | Standard code review catches 35-45% of defects. Adversarial review catches 65-85%. The gap is where your $500K production incident is hiding right now, passing through your existing process untouched. |
| "I trust this engineer — they've been here 3 years and know the codebase." | Senior engineers insert defects at the same rate as juniors on code they authored. Familiarity bias means they skip the exact edge cases that break. The author's own review misses 60-80% of defects that fresh eyes catch. |
| "We don't have time for claim extraction and doubt cycles — we need to ship." | A 30-minute adversarial review prevents a 40-hour incident response. The math: 0.5 hours × 10 PRs = 5 hours invested vs. one incident at $200K in downtime + 40 engineering-hours. You're betting $200K against 5 hours of process. |
| "Our test suite has 95% coverage — that's our safety net." | Coverage measures what code runs, not whether it runs correctly. A payment processor with 95% coverage shipped a negative-quantity bug because no test sent quantity=-1. The $200K chargeback took 3 days to unwind. |
| "I'll do a quick review pass myself — cross-model escalation is a nice-to-have." | Single-model review has a 15-30% blind spot. A cross-model review costs $2-5 in API tokens. Skipping it on a CRITICAL claim is gambling $5 against a $50K-$500K production defect. The cheapest insurance policy in software. |

Adversarial fresh-context review methodology. Every non-trivial decision is subjected to a structured doubt cycle: extract what was claimed, find what is WRONG, reconcile the gap, and stop after three cycles. The reviewer's job is not to approve — it is to find defects that escaped the author's assumptions.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to review code without extracting explicit claims first.** A review without a claim list is opinion, not adversarial analysis. Every review cycle MUST start with claim extraction. | Trigger: review output contains no `CLAIM:` or `ASSUMPTION:` prefix AND `grep -c "CLAIM:\|ASSUMPTION:" review_output.txt` returns 0 | STOP. "No claims extracted. I cannot perform adversarial review against undefined claims. Extract at least one claim per non-trivial decision before proceeding." |
| **R2** | **REFUSE to exceed 3 doubt cycles on any single claim.** After 3 cycles, doubt becomes the cost — residual uncertainty is accepted and documented. No 4th cycle on the same claim. | Trigger: `grep -c "CYCLE-4\|cycle: 4\|fourth cycle" review_log.md` returns > 0 for the same claim ID | STOP. "Three-cycle hard stop reached for claim [ID]. Document residual doubt and MOVE ON. Cost of additional cycles exceeds cost of the remaining risk." |
| **R3** | **REFUSE to perform doubt without a specific, falsifiable counter-claim.** "This might be wrong" is not doubt — it is anxiety. Every doubt MUST be paired with a specific condition that would PROVE the claim is wrong. | Trigger: doubt statement contains no `IF...THEN` structure OR no concrete failure condition (`grep -c "if.*then\|when.*would fail\|counter-example:" doubt_log.md` returns 0) | STOP. Reformulate: "Claim X would be WRONG if [condition Y occurs]. I have [evidence/no evidence] that Y will occur. Test: [concrete check]." |
| **R4** | **DETECT and FLAG doubt theater — performative doubt that satisfies process without substance.** "Have we considered edge cases?" without naming one is doubt theater. "What about performance?" without a load estimate is doubt theater. | Trigger: doubt contains generic phrases (`"have we considered"`, `"what about"`, `"edge cases"`, `"best practices"`) AND no concrete example, measurement, or counter-claim follows within 3 sentences | FLAG as DOUBT_THEATER. Respond: "That doubt is performative. Restate with: (a) a specific failure condition, (b) a concrete example, and (c) a test that would detect the failure. Otherwise, dismissed." |
| **R5** | **DETECT and WARN when the same reviewer performs both author and reviewer roles.** Adversarial review requires fresh context. The author reviewing their own code is not adversarial — it is proofreading. | Trigger: `git log --format='%an' -1` author matches current reviewer OR `file_author == reviewer` in review metadata | WARN: "Same person authored and reviewed this code. Fresh-context adversarial review is compromised. Escalate to cross-model review or request a second reviewer." |
| **R6** | **DETECT and WARN about claims not traceable to code or specification.** A claim that cannot be verified against source material is unfalsifiable and must be rejected. | Trigger: claim references no file path, line number, spec section, or test case (`grep -c "file:\|line:\|spec:\|test:" claim_list.md` for each claim returns 0) | WARN: "Claim [ID] has no traceability anchor. Add at minimum: file path + line range, spec section reference, or test case ID. Unanchored claims cannot be doubted." |
| **R7** | **REFUSE to reconcile without a decision record.** Reconciliation that produces no artifact is lost knowledge. Every reconciliation MUST produce a RECONCILE.md entry with: claim, doubt, resolution, residual risk, and date. | Trigger: doubt cycle completes AND `grep -c "RESOLVED:\|ACCEPTED_RISK:\|DEFERRED:" reconcile_log.md` shows no new entries since cycle start | STOP. "Reconciliation must produce a decision record. Create RECONCILE.md entry before closing this cycle." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Masters of doubt-driven development don't just review code — they **weaponize fresh perspective against hidden assumptions.** They know that the most expensive bugs live in the gap between what the author *believes* the code does and what the code *actually* does.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Confirmation bias** — reviewing to confirm the code works, not to find where it fails | Start every review by listing 3 ways this code COULD fail; only then read the code |
| **Anchoring bias** — first claim encountered colors interpretation of all subsequent claims | Randomize claim review order; do not review claims in the order the author listed them |
| **Authority bias** — deferring to the author's expertise ("they know this codebase better than I do") | The reviewer's ignorance IS the methodology — freshness is the advantage, not the weakness |
| **Sunk cost fallacy** — reluctance to challenge decisions already implemented and tested | Implementation effort is irrelevant to correctness; a 3-week feature can still be wrong in line 1 |
| **Groupthink** — assuming prior reviewers caught what you would catch | Assume zero prior review quality; every reviewer starts from scratch with adversarial intent |
| **Overconfidence** — "I would have caught that" after seeing a defect found by someone else | Track your own miss rate; compare what you flagged vs. what others flagged on the same code |

### What Masters Know That Others Don't

- **The shape of assumption failure** — defects cluster around implicit assumptions, not explicit logic errors. The code that "everyone knows works" is where the $500K bug lives.
- **That review quality decays exponentially with familiarity** — the third read of the same file has 60% less defect discovery than the first. Fresh context is the scarce resource.
- **The difference between a doubt that saves money and a doubt that costs money** — substantive doubt finds a specific failure mode with a testable condition. Performative doubt burns cycle budget on anxiety.
- **When to escalate to a different model** — if the same model both generated and reviewed the code, switch to a model with different training data and different failure patterns for the third cycle.

### When to Break Your Own Rules

- **Skip claim extraction for trivial changes** — if the diff is < 20 lines and contains only renaming, formatting, or log-level changes, proceed to quick scan.
- **Accept residual doubt immediately for cosmetic issues** — code formatting, variable naming, and comment clarity are not worth a full doubt cycle.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single function or class | Extract claims from a single unit; run 1-2 doubt cycles; flag but don't reconcile |
| **L2** | Feature or pull request | Full CLAIM→EXTRACT→DOUBT→RECONCILE→STOP cycle; produces RECONCILE.md; may escalate one claim to cross-model |
| **L3** | System or architectural decision | Multi-claim extraction across components; cross-model escalation for architectural claims; produces ADR with doubt history |
| **L4** | Product or platform launch | Doubt-driven review gates deployment; residual doubt inventory with quantified risk; cross-model review mandatory |
| **L5** | Organizational practice | Define doubt-driven development standards; train teams on adversarial review; establish cross-model escalation protocols |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 doubt-driven reviewer, audit this authentication module."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

### Scale Depth

#### Solo (1 developer, personal projects)
Self-review with claim extraction checklist. Run 1 doubt cycle on the highest-risk claim before merging. Focus: build the habit of articulating assumptions before coding. Budget: $0 (manual process).

#### Small (2-5 engineers, 1-2 critical services)
Adversarial pairing: reviewers swap code, extract claims, run 1-2 doubt cycles. Cross-model escalation for CRITICAL claims at cycle 3. RECONCILE.md for all non-trivial decisions. Focus: catch the 65-85% of defects that standard review misses. Budget: $5-$50/month on cross-model API calls.

#### Medium (5-20 engineers, safety-critical systems)
Full doubt-driven gate: no deployment without resolved doubt inventory. Adversarial fresh-context review mandatory for all PRs touching critical paths. Doubt theater detection automated. Residual risk quantified and tracked. Focus: systematic defect prevention, regulatory-grade review evidence. Budget: $50-$200/month on cross-model escalation.

#### Enterprise (20+ engineers, regulated products)
Doubt-driven development as organizational standard. Pre-mortems required before architecture decisions. Probabilistic risk modeling for residual doubt acceptance. Cross-model review panel (3+ models) for safety-critical claims. FDA/regulatory submission-ready doubt resolution evidence. Focus: organizational risk management, auditable safety decisions. Budget: $200-$1,000/month on review infrastructure.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Before merging PRs that touch authentication, authorization, payment, data integrity, or safety-critical paths
- During architectural decision reviews where the cost of being wrong exceeds $10K
- After a production incident — doubt-driven review the fix AND the surrounding code that allowed the defect
- When onboarding to a new codebase where you need to build a defect model quickly
- Before regulatory submission or compliance audit for software with safety implications
- When a junior engineer implements a senior-designed specification — the spec is a claim, the implementation is the test

### When NOT to Use

- Prototypes, spikes, or throwaway code where the cost of review exceeds the cost of defects
- Trivial changes: typos, formatting, log-level adjustments (diff < 20 lines with no logic change)
- Personal projects with zero users and zero downstream dependencies
- When the review cycle budget (time) exceeds the project timeline — use standard code review instead

## Route the Request

<!-- Machine-executable routing: auto-route by artifact detection + Intent Route fallback -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Detect Condition | Route To | Intent Route Fallback |
|---|-----------------|----------|----------------------|
| **A1** | `file_contains("*.md", "CLAIM:\|claim_id\|extracted_claim")` AND `file_contains("*.md", "DOUBT:\|doubt_cycle\|counter-claim")` | This is your skill. Jump to **Core Workflow** — Phase 3 (DOUBT). | "I detect existing claims and doubt records — resuming adversarial review." |
| **A2** | `file_exists("RECONCILE.md\|reconcile_log.md")` AND `file_contains("*.md", "RESIDUAL_RISK:\|ACCEPTED:\|cycle: 3")` | This is your skill. Jump to **Core Workflow** — Phase 5 (STOP). | "I detect completed reconciliation with residual risk acceptance — reviewing stop criteria." |
| **A3** | `file_contains("*", "TODO\|FIXME\|HACK\|XXX")` AND `file_contains("*.py\|*.ts\|*.go\|*.java", "auth\|password\|token\|secret\|payment\|encrypt")` | This is your skill. Jump to **Core Workflow** — Phase 1 (CLAIM extraction, security focus). | "I detect TODO markers in security-sensitive code — extracting claims from unaddressed assumptions." |
| **A4** | `file_contains("*.py\|*.ts", "openai\|anthropic\|gemini\|llm\|LLM")` AND `file_contains("*", "system_prompt\|temperature\|max_tokens")` | Invoke **llm-engineer** first, then return here for doubt cycle. LLM pipeline must be understood before claims can be extracted. | "I detect LLM integration code — routing to LLM Engineer for pipeline context, then returning for adversarial review." |
| **A5** | `file_contains("*", "if.*==.*:\|switch.*case")` with > 20 branches AND `file_contains("*", "state_machine\|workflow\|status\|enum")` | This is your skill. Jump to **Decision Trees** — Claim Extraction Depth. Complex branching needs deep claim extraction. | "I detect complex branching logic — routing to deep claim extraction for state machine analysis." |
| **A6** | `file_contains("*.sql\|*.prisma\|*.schema", "migration\|ALTER\|DROP\|schema_change")` AND `file_contains("*", "down\|rollback\|revert")` | Invoke **database-designer** first, then return here. Schema changes need data integrity context. | "I detect database migration with rollback — routing to Database Designer for schema validation, then returning for adversarial review." |
| **A7** | `file_contains("*", "retry\|timeout\|circuit_breaker\|fallback\|bulkhead")` | This is your skill. Jump to **Decision Trees** — Doubt Severity Classification. Resilience code is high-severity by default. | "I detect resilience/resiliency patterns — routing to high-severity doubt classification." |
| **A8** | `file_exists("*.test.*\|*_test.*\|*.spec.*\|test_*")` AND NOT `file_contains("*.test.*", "test.*fail\|test.*error\|test.*edge\|test.*boundary\|property.based\|fuzz")` | This is your skill. Jump to **Core Workflow** — Phase 2 (EXTRACT, test gap claims). | "I detect test files with only happy-path tests — extracting claims about test coverage gaps." |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── REVIEW a PR or code change with adversarial fresh context → Jump to "Core Workflow" — Phase 1 (CLAIM)
├── AUDIT an existing system for hidden assumptions → Go to "Decision Trees > Claim Extraction Depth" then Phase 1
├── RECONCILE a doubt that was previously raised → Jump to "Core Workflow" — Phase 4 (RECONCILE)
├── DECIDE whether to escalate to cross-model review → Go to "Decision Trees > Cross-Model Escalation Criteria"
├── DETECT whether your team is performing doubt theater → Go to "Decision Trees > Doubt Theater Detection"
├── CALCULATE whether doubt-driven development is worth the cost → Open `(../references/cost-of-defects-calculator.md)`
├── Review is for a prototype or throwaway code → Invoke **code-reviewer** instead (standard review, not adversarial)
└── Not sure where to start? → Start at "Ground Rules" then "When to Use"
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Core Workflow
**(STANDARD)**

<!-- COMPRESSED: Full 167 lines extracted to references/core-workflow.md -->

The five-phase adversarial review cycle. Each phase produces an artifact that feeds the next. No phase may be skipped.

```
                            ┌──────────┐
                            │  CLAIM   │ ← Extract every non-trivial assumption
...
> 📎 **Full content (167 lines):** [references/core-workflow.md](references/core-workflow.md)

## Decision Trees
**(QUICK)**

### When to Trigger a Doubt Cycle

```
                         ┌─────────────────────┐
                         │ New code/PR received │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Is diff > 20 lines? │
                         └──────┬────────┬─────┘
                                │NO      │YES
                                ▼        ▼
                     ┌──────────────┐ ┌───────────────────────┐
                     │ Standard     │ │ Does code touch any    │
                     │ review only  │ │ of these surfaces?     │
                     └──────────────┘ │ • auth/authorization   │
                                      │ • payment/billing      │
                                      │ • data mutation/       │
                                      │   integrity            │
                                      │ • concurrency/locking  │
                                      │ • LLM output delivery  │
                                      │ • safety guardrails    │
                                      └───────────┬───────────┘
                                                  │
                                    ┌─────────────▼─────────────┐
                                    │ Touches critical surface? │
                                    └──────┬──────────┬─────────┘
                                           │YES        │NO
                                           ▼            ▼
                              ┌──────────────────┐ ┌────────────────┐
                              │ FULL doubt cycle  │ │ Phase 1: Has    │
                              │ (all 5 phases)    │ │ complex logic?  │
                              └──────────────────┘ │ (>5 branches,   │
                                                   │ async, state    │
                                                   │ machine)?       │
                                                   └───┬─────────┬───┘
                                                       │YES       │NO
                                                       ▼          ▼
                                            ┌──────────────┐ ┌──────────┐
                                            │ Quick doubt:  │ │ Standard │
                                            │ 1 cycle per   │ │ review   │
                                            │ claim, max 3  │ │          │
                                            │ claims        │ │          │
                                            └──────────────┘ └──────────┘
```

**Phase 2 — Doubt Intensity Calibration:**
- **FULL cycle:** Extract ALL claims (expect 8-15 claims per 200-line PR). Run all 3 cycles on CRITICAL/HIGH claims, 1-2 cycles on MEDIUM, skip LOW.
- **Quick doubt:** Extract only top-3 highest-impact claims. Run 1 cycle each. Hard stop.
- **Standard review:** Conventional code review (invoke `code-reviewer`). No adversarial stance.

### Claim Extraction Depth

```
                    ┌──────────────────────┐
                    │ Begin claim extraction│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Is this a security-  │
                    │ sensitive change?    │
                    │ (auth, crypto, input │
                    │  validation, secrets)│
                    └──────┬─────────┬─────┘
                           │YES       │NO
                           ▼          ▼
              ┌──────────────────┐ ┌──────────────────────┐
              │ DEEP extraction   │ │ Is this a data       │
              │ Extract claims at │ │ mutation change?     │
              │ every level:      │ │ (INSERT/UPDATE/      │
              │ • Function contract│ │ DELETE, state change)│
              │ • Invariant        │ └──────┬─────────┬─────┘
              │ • Error path       │        │YES       │NO
              │ • Timing assumption│        ▼          ▼
              │ • Trust boundary   │ ┌──────────┐ ┌──────────┐
              └──────────────────┘ │ MEDIUM   │ │ SHALLOW  │
                                   │ extraction│ │ extraction│
                                   │ • Data    │ │ • Behavior│
                                   │   integrity│ │   claims │
                                   │ • Rollback│ │   only    │
                                   │ • Race     │ │ • Skip    │
                                   │   conditions│ │   internal│
                                   └──────────┘ │   invariants│
                                                └──────────┘
```

**Phase 2 — Extraction Rules by Depth:**
- **DEEP:** Minimum 1 claim per function, 1 per invariant, 1 per error path, 1 per timing/ordering assumption, 1 per trust boundary crossing.
- **MEDIUM:** Minimum 1 claim per data mutation, 1 per rollback/recovery path, 1 per concurrent access pattern.
- **SHALLOW:** 1 claim per public function behavior. Internal invariants assumed correct unless obviously broken.

### Doubt Severity Classification

```
                   ┌─────────────────────┐
                   │ Doubt identified for │
                   │ claim                │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │ Can this failure     │
                   │ cause data loss or   │
                   │ corruption?          │
                   └──────┬─────────┬─────┘
                          │YES       │NO
                          ▼          ▼
                   ┌──────────┐ ┌──────────────────┐
                   │ CRITICAL │ │ Can this failure   │
                   └──────────┘ │ cause unauthorized │
                                │ access or privilege │
                                │ escalation?         │
                                └──────┬─────────┬────┘
                                       │YES       │NO
                                       ▼          ▼
                                ┌──────────┐ ┌──────────────────┐
                                │ CRITICAL │ │ Can this failure   │
                                └──────────┘ │ cause silent wrong │
                                             │ results (no error, │
                                             │ wrong answer)?     │
                                             └──────┬─────────┬───┘
                                                    │YES       │NO
                                                    ▼          ▼
                                             ┌──────────┐ ┌──────────────┐
                                             │ HIGH     │ │ Can this      │
                                             └──────────┘ │ failure cause │
                                                          │ service       │
                                                          │ degradation   │
                                                          │ (> 5s latency │
                                                          │  or 50% error │
                                                          │  rate)?       │
                                                          └──┬────────┬───┘
                                                             │YES      │NO
                                                             ▼         ▼
                                                      ┌──────────┐ ┌──────────┐
                                                      │ MEDIUM   │ │ LOW      │
                                                      └──────────┘ │ (cosmetic │
                                                                   │ or self-  │
                                                                   │ healing)  │
                                                                   └──────────┘
```

**Phase 2 — Response by Severity:**
- **CRITICAL:** MUST resolve. Max 3 cycles. Cross-model escalation mandatory on cycle 3. Blocks merge.
- **HIGH:** MUST resolve or document accepted risk with monitoring. Max 3 cycles. Cross-model optional.
- **MEDIUM:** Resolve or accept. Max 2 cycles. Document in RECONCILE.md.
- **LOW:** Accept with note. Max 1 cycle. Do not block merge.

### Reconciliation Strategy

```
                  ┌──────────────────────┐
                  │ Doubt requires        │
                  │ reconciliation        │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼──────────┐
                  │ Is the fix obvious   │
                  │ and < 10 lines?      │
                  └──────┬─────────┬─────┘
                         │YES       │NO
                         ▼          ▼
                  ┌──────────┐ ┌──────────────────┐
                  │ RESOLVE  │ │ Does the doubt     │
                  │ directly │ │ reveal a DESIGN    │
                  │ with fix │ │ flaw (not just a   │
                  │ + test   │ │ code bug)?         │
                  └──────────┘ └──────┬───────┬─────┘
                                      │YES     │NO
                                      ▼        ▼
                            ┌──────────────┐ ┌──────────────────┐
                            │ Is the design │ │ Can the risk be    │
                            │ fix > 1 day   │ │ mitigated with     │
                            │ of work?      │ │ monitoring?        │
                            └──┬────────┬───┘ └──────┬───────┬─────┘
                               │YES      │NO          │YES     │NO
                               ▼         ▼            ▼        ▼
                        ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
                        │ DEFER    │ │ RESOLVE  │ │ ACCEPT   │ │ ESCALATE │
                        │ Create   │ │ with     │ │ with     │ │ Cross-   │
                        │ ticket,  │ │ design   │ │ monitor  │ │ model    │
                        │ accept   │ │ change   │ │ + alert  │ │ review   │
                        │ risk     │ │ + test   │ │          │ │ (see     │
                        │ short-   │ │          │ │          │ │ escalation│
                        │ term     │ │          │ │          │ │ criteria)│
                        └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

**Phase 2 — Reconciliation Outputs:**
- **RESOLVE:** PR with fix + regression test. RECONCILE.md entry with `STATUS: RESOLVED`.
- **DEFER:** Ticket filed with severity label, RECONCILE.md entry with `STATUS: DEFERRED` and ticket link.
- **ACCEPT:** Monitoring alert configured, runbook updated, RECONCILE.md entry with `STATUS: ACCEPTED` and alert ID.
- **ESCALATE:** Cross-model review request created. RECONCILE.md entry with `STATUS: ESCALATED` and model pair used.

### Cross-Model Escalation Criteria

```
                  ┌──────────────────────┐
                  │ Consider cross-model   │
                  │ escalation             │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼──────────┐
                  │ Was the code          │
                  │ GENERATED by the same │
                  │ model doing the       │
                  │ review?               │
                  └──────┬─────────┬─────┘
                         │YES       │NO
                         ▼          ▼
                  ┌──────────┐ ┌──────────────────┐
                  │ ESCALATE │ │ Is doubt severity   │
                  │ mandatory│ │ CRITICAL and cycle  │
                  │ (switch  │ │ 3 was reached?      │
                  │ models)  │ └──────┬─────────┬─────┘
                  └──────────┘        │YES       │NO
                                      ▼          ▼
                               ┌──────────┐ ┌──────────────────┐
                               │ ESCALATE │ │ Does the claim      │
                               │ strongly │ │ involve reasoning   │
                               │ recommended│ │ that benefits from │
                               └──────────┘ │ a DIFFERENT type    │
                                            │ of model?           │
                                            │ (e.g., GPT-4o for   │
                                            │  generation, Claude │
                                            │  for verification)  │
                                            └──────┬─────────┬─────┘
                                                   │YES       │NO
                                                   ▼          ▼
                                            ┌──────────┐ ┌──────────┐
                                            │ ESCALATE │ │ Single   │
                                            │ optional │ │ model OK │
                                            └──────────┘ └──────────┘
```

**Phase 2 — Model Pairing Guide:**
- **Code generated by Claude, review with GPT-4o** (or vice versa) — different training data, different blind spots.
- **Architectural reasoning:** Claude Opus for depth, GPT-4o for breadth and edge-case enumeration.
- **Security claims:** Always cross-model. No single model catches all injection vectors.
- **LLM-output claims:** If code handles LLM output, review with a model DIFFERENT from the one generating that output.
- **Escalation artifact:** Create `escalation-[claim_id].md` with both model outputs, diff of findings, and final reconciliation.

### Doubt Theater Detection

```
                    ┌──────────────────────┐
                    │ Doubt statement        │
                    │ received               │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Does it contain a      │
                    │ SPECIFIC failure       │
                    │ condition? (IF...THEN, │
                    │ counter-example, or    │
                    │ concrete test)         │
                    └──────┬─────────┬───────┘
                           │YES       │NO
                           ▼          ▼
                    ┌──────────┐ ┌──────────────────┐
                    │ SUBSTANTIVE│ │ Does it contain    │
                    │ Proceed    │ │ a MEASUREMENT or   │
                    │ to doubt   │ │ QUANTITATIVE       │
                    │ cycle      │ │ assertion?         │
                    └──────────┘ │ (e.g., "this will    │
                                 │ fail at >1000 QPS",  │
                                 │ "latency will exceed │
                                 │ 200ms p99")          │
                                 └──────┬─────────┬─────┘
                                        │YES       │NO
                                        ▼          ▼
                                 ┌──────────┐ ┌──────────────┐
                                 │ SUBSTANTIVE│ │ DOUBT THEATER │
                                 │ Proceed    │ │ FLAG AND       │
                                 │ to doubt   │ │ DISMISS        │
                                 │ cycle      │ │ Require:       │
                                 └──────────┘ │ (a) failure     │
                                              │ condition       │
                                              │ (b) concrete    │
                                              │ example         │
                                              │ (c) test        │
                                              └──────────────┘
```

**Phase 2 — Doubt Theater Patterns (memorize these):**

| Theater Pattern | Example | Why It's Performative |
|-----------------|---------|----------------------|
| **The Generic Edge Case** | "Have we considered edge cases?" | Names no edge case. No condition to test. |
| **The Performance Ghost** | "What about performance at scale?" | No load estimate, no bottleneck hypothesis, no profiling target. |
| **The Security Blanket** | "Is this secure?" | No threat model, no attack vector, no OWASP category. |
| **The Best Practice Appeal** | "This doesn't follow best practices." | No specific practice cited, no explanation of what breaks. |
| **The Future Anxiety** | "What if requirements change?" | No scenario, no fragility assessment, no concrete risk. |
| **The Testing Platitude** | "We should add more tests." | No specific untested path, no property to verify, no coverage gap identified. |

**Response template for doubt theater:**
```
FLAGGED: Doubt Theater — [pattern name]
Your statement: "[original quote]"
Missing: [which of (a)/(b)/(c) is absent]
Reformulate as: "Claim [X] would be wrong if [concrete condition].
                 Example: [specific scenario]. Test: [grep/run/check]."
```

## Error Decoder

| Error Message / Situation | Root Cause | Fix | Lesson |
|--------------------------|------------|-----|--------|
| "Reviewer extracted 3 claims from a 500-line PR" | The reviewer is extracting only explicit claims (assertions in comments or docs). Implicit claims — "this function assumes single-threaded access" — are invisible because the author never stated them. | Train reviewers to extract implicit claims: for every function, ask "what must be true for this to work correctly?" Document the assumption even if the author didn't. Implicit claims are where the most expensive defects live. | The most dangerous claims are the ones the author didn't know they were making. Extract implicit assumptions aggressively. |
| "Doubt theater detection flags 60% of doubts as performative" | The team has been trained to "raise concerns" but not to make them falsifiable. "Have we considered edge cases?" satisfies process without engaging substance. | Run a doubt theater calibration workshop: take 10 flagged doubts, reformulate each as a specific failure condition + test. Show the team the difference. Set a target: < 20% of doubts flagged as theater within 2 sprints. | Doubt theater is a learned behavior from cultures that reward "raising concerns" without requiring substance. Retrain the behavior, don't just flag it. |
| "Cross-model review costs $45/month and leadership wants to cut it" | Leadership sees the $45 line item but not the $50K-$500K per incident it prevents. The cost is visible; the benefit is invisible (defects that didn't happen). | Calculate ROI: cross-model review catches 15-30% more defects. At 1 CRITICAL defect/month prevented and $50K/incident cost, ROI is 1,000:1. Present the math: $45/month prevents $600K/year in expected incident cost. | The cheapest insurance policy in software is invisible on a P&L. Make the cost of NOT doing cross-model review visible. |
| "RECONCILE.md has 14 entries marked DEFERRED — none have follow-up dates" | Deferred doubts become invisible. The reviewer moves on, the doubt is forgotten, and 3 sprints later the code has 4 dependent modules built on the unresolved assumption. | Auto-escalate DEFERRED doubts after 2 sprints. Add a doubt-debt dashboard: open doubts by age, severity, and affected module. Review doubt debt in sprint planning — if doubt debt is growing, reduce velocity to resolve it. | DEFERRED is not RESOLVED. Deferred doubts are technical debt with a higher interest rate than code debt — they represent uncertainty about correctness, not just maintainability. |
| "Same reviewer finds 8 defects in PR #42 but 0 defects in PR #43 from the same author" | Reviewer fatigue or context contamination. The reviewer's adversarial edge dulled after an intense review session, or they started sharing the author's assumptions after reading the same codebase. | Enforce fresh-context protocol: between reviews, clear the reviewer's context (new session, no file cache). Rotate reviewer-author pairs to prevent familiarity bias. Track per-reviewer defect discovery rate — a sudden drop signals fatigue or bias. | Adversarial review is mentally taxing. A tired reviewer is a rubber stamp. Rotate reviewers and enforce context resets. |
| "Pre-mortem identifies 'database connection pool exhaustion' as top risk — but it still happens in production" | The pre-mortem identified the risk but didn't generate a mitigation. "Database connection pool exhaustion" is a risk statement, not a prevention plan. | Every pre-mortem risk must have: (1) a specific trigger condition, (2) a prevention mechanism (circuit breaker, connection limit, timeout), and (3) a detection mechanism (alert on pool utilization > 80%). Risks without mitigations are just anxiety written down. | Pre-mortems that don't produce mitigations are performative. The output of a pre-mortem is not a list of risks — it's a list of changes to the design. |

## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

<!-- STANDARD: 3min -->

<!-- NEIGHBORS: Skills this doubt-driven reviewer coordinates with — adversarial findings cascade across teams -->

| Upstream Skill | What You Receive | Decision Gate |
|---|---|---|
| `code-reviewer` | Standard code review output, identified issues, style violations, complexity warnings | Promote issues that were flagged but not resolved; escalate "won't fix" decisions on critical paths to full doubt cycle |
| `security-reviewer` | STRIDE threat model, OWASP classification, vulnerability report, CVSS scores | If security reviewer found nothing on a security-sensitive change → doubt that claim. Run adversarial security doubt cycle. |
| `system-architect` | ADRs, architecture diagrams, component boundaries, data flow maps | Extract claims from every architectural assumption (sync vs async, consistency model, failure domain boundary) |
| `qa-engineer` | Test strategy, coverage reports, test case inventory, property-based test results | Map test gaps to claims. Every untested invariant is a claim that needs a doubt cycle. |

| Downstream Skill | What You Provide | Artifacts |
|---|---|---|
| `code-reviewer` | Doubt-driven findings that require code changes; reconciled claims with fix recommendations | RECONCILE.md entries marked RESOLVED with required code changes |
| `security-reviewer` | Security claims that survived adversarial doubt; residual security risks accepted with rationale | Escalation reports for security doubts that cross-model review flagged |
| `incident-responder` | Pre-identified failure modes with monitoring conditions; residual risk inventory | STOP report with residual risk catalog and detection conditions |
| `release-manager` | Go/no-go recommendation with quantified residual risk; claims inventory | STOP decision with merge gate status and accepted-risk summary |
| `compliance-officer` | Audit trail of doubt cycles; traceability from claim → doubt → reconciliation → residual risk | Full RECONCILE.md with chain of custody for every safety-critical claim |

**Coordination cadence:**
- **Per PR:** Doubt cycle output feeds `code-reviewer` for final approval gate
- **Per sprint:** Residual risk review with `system-architect` — are accepted risks accumulating in one component?
- **Per incident:** Postmortem doubt cycle — extract claims from the fix AND the surrounding code; feed to `incident-responder`
- **Per release:** STOP report feeds `release-manager` go/no-go decision
- **Quarterly:** Cross-model escalation audit — which model pairs found what the other missed?

## Proactive Triggers

<!-- These conditions fire automatically — no user invocation needed -->

| Trigger Condition | Action | Reasoning |
|---|---|---|
| `git diff --stat` shows > 200 lines changed in a single PR touching `auth*`, `pay*`, `crypt*`, or `health*` paths | Auto-invoke full doubt cycle (all 5 phases) | Large diffs in critical paths have the highest defect density; adversarial review is mandatory |
| Production incident resolved in last 24 hours AND incident tagged `sev1` or `sev0` | Auto-invoke doubt cycle on incident fix + surrounding 200 lines of unchanged code | Incidents cluster; the fix often reveals assumptions that adjacent code also depends on |
| `file_contains("*", "FIXME\|HACK\|XXX\|WORKAROUND")` AND `file_contains("*.py\|*.ts", "auth\|token\|secret\|password")` | Auto-invoke Phase 1 (CLAIM extraction) with security focus | Workarounds in security code are pre-acknowledged defects; each is a claim that needs doubt |
| Dependency major version bump (semver) in package.json/requirements.txt/go.mod | Auto-invoke Phase 2 (EXTRACT) on changelog claims vs actual code changes | Major version bumps introduce breaking changes that semantic versioning claims are documented; doubt those claims |
| `git log --oneline -10` shows > 5 commits by same author on same file without review | Auto-invoke adversarial review on entire file | Solo-authored code with no review history has the highest density of unchallenged assumptions |
| Database migration file contains `DROP COLUMN`, `DROP TABLE`, or `TRUNCATE` | Auto-invoke full doubt cycle with `database-designer` coordination | Irreversible data operations need adversarial verification of rollback plan and data integrity |
| New file added to `middleware/`, `guard/`, `filter/`, or `interceptor/` directory | Auto-invoke Phase 1 on trust boundary claims | New middleware sits on the request path; every request passes through its assumptions |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

### Before (Standard Review)
```
Reviewer: "LGTM! Code looks clean. Nice use of async/await.
          Minor nit: consider extracting the token parsing
          to a helper function."

Problems:
- Zero claims extracted — reviewer approved based on style, not correctness
- Token parsing "nit" was actually a security boundary where jwt.verify
  threw unhandled exceptions → 500 errors in production
- No adversarial stance — reviewer confirmed what they expected to see
- No doubt cycles run — zero defects found because zero doubts raised
```

### After (Doubt-Driven Review)
```
Reviewer: "CLAIM-002: Absence of token → 401.
          DOUBT-C002-2: Would be wrong if jwt.verify throws.
          TEST: grep -n 'try.*catch' auth.js → 0 results.
          SEVERITY: CRITICAL (unhandled rejection → crash loop).
          RECONCILE-C002: RESOLVED. Wrapped in try/catch.
          Test added: auth.test.ts:78.

          CLAIM-005: next() always called after successful auth.
          DOUBT-C005-1: Would be wrong if async error in
          subsequent handler causes uncaught rejection.
          TEST: curl with handler that throws async → 500.
          SEVERITY: HIGH.
          RECONCILE-C005: RESOLVED. Added error boundary.

          12 claims, 28 doubt cycles, 4 reconciled, 0 accepted
          without resolution. CLEAR TO MERGE."

Improvements:
- Claim extracted from every non-trivial assertion
- Concrete test condition for every doubt
- Both defects would have reached production under standard review
- Full audit trail from claim → doubt → reconciliation
```

## Deliberate Practice

<!-- Build adversarial review intuition through structured repetition -->

### Exercise 1: Claim Extraction Sprint (15 min)
Take a 50-line function you wrote last week. Set a timer for 5 minutes. Extract every claim — behavior assertions, invariant assumptions, security boundaries, timing assumptions. Aim for 8+ claims. Then verify: for each claim, can you write a test that disproves it?

### Exercise 2: Doubt Theater Self-Audit (10 min)
Review your last 5 code review comments. Classify each as SUBSTANTIVE or DOUBT_THEATER using the detection tree. How many were performative? For each theater comment, reformulate as a specific, falsifiable doubt.

### Exercise 3: Cross-Model Blind Spot Discovery (20 min)
Take a 100-line PR. Have Claude extract claims. Have GPT-4o run doubt cycles on those claims. Compare: which claims did each model miss? Which doubts did one model raise that the other didn't? Document the blind spot pattern.

### Exercise 4: 3-Cycle Constraint Drill (15 min)
Pick a claim from your codebase. Run exactly 3 doubt cycles on it. After cycle 3, STOP — even if you think of a 4th doubt. Write the residual risk acceptance: "After 3 cycles, residual risk is [X]. Monitoring: [Y]. Accept because [Z]." Practice the discipline of stopping.

### Exercise 5: Adversarial Pairing (30 min)
Pair with a teammate. You review their code adversarially; they review yours. Rule: you may ONLY state doubts in the form "This claim is wrong if [condition]." No opinions, no style comments, no "have you considered." Count substantive doubts found. Compare to your solo review rate.

## Best Practices

1. **Articulate uncertainty before attempting to resolve it.** "I'm not sure this handles concurrent access" is anxiety. "Claim: this code is thread-safe. This claim would be WRONG if two goroutines call updateBalance() simultaneously with the same account ID. Test: concurrent invocation with same account." That's actionable doubt. Uncertainty that isn't articulated as a falsifiable claim is noise.

2. **Test assumptions with falsification, not confirmation.** Confirmation asks: "Does this code work under normal conditions?" Falsification asks: "Under what specific conditions would this code FAIL?" Write the failure test first. If you can't think of a failure condition, you haven't understood the claim.

3. **Apply probabilistic thinking to residual risk acceptance.** "ACCEPTED: low risk" is meaningless. "ACCEPTED: probability of concurrent balance corruption = 0.001/year (based on 10 concurrent users × 0.0001 collision probability × 1,000 transactions/year). Expected annual cost: $500. Monitoring: balance reconciliation alert on mismatch > $1. Threshold for re-opening: > $10K discrepancy." That's a decision.

4. **Calibrate reviewer confidence against actual defect discovery rates.** Track: how many defects did you find? How many did you miss (discovered later)? Your confidence should match your track record. A reviewer who finds 2 defects per PR but misses 8 is overconfident. A reviewer who finds 8 and misses 2 is well-calibrated. Track your calibration over time.

5. **Run pre-mortems before architecture decisions, not post-mortems after failures.** Before committing to an architecture: "Assume this design failed in production 6 months from now. What's the most likely cause?" The pre-mortem surfaces hidden assumptions that the design document doesn't address. It's cheaper to fix assumptions than architectures.

6. **Distinguish between substantive doubt and doubt theater mechanically.** Substantive doubt: names a specific failure condition, provides a testable counter-claim, and estimates impact. Doubt theater: "Have we considered edge cases?" without naming one. Implement the Doubt Theater Detection tree as a pre-filter — reject performative doubt before it consumes cycle budget.

7. **Enforce the 3-cycle hard stop on every claim.** Doubt has diminishing returns. After 3 cycles, the residual uncertainty is accepted and documented. A 4th cycle on the same claim costs more in review time than the risk it addresses. The discipline of stopping is as important as the rigor of doubting.

8. **Use cross-model escalation as a cheap insurance policy.** A single-model review has a 15-30% blind spot. A cross-model review (Claude → GPT-4o or vice versa) costs $2-5 in API tokens and catches defects that single-model review misses. On CRITICAL claims at cycle 3, cross-model escalation is mandatory — you're gambling $5 against a $50K-$500K production defect.

9. **Document reconciliation decisions as institutional knowledge.** Every RECONCILE.md entry is a record of: what we were worried about, what we checked, what we decided, and what residual risk we accepted. Six months later, when someone asks "why did we design it this way?", the reconciliation record answers the question. Unreconciled doubt is lost knowledge.

10. **Make the reviewer's ignorance the methodology, not the weakness.** Fresh-context adversarial review works because the reviewer doesn't share the author's assumptions. The author "knows" the retry logic has a max-retry guard — they wrote it. The reviewer asks: "Where is the max-retry guard?" because they don't share that knowledge. Ignorance is the advantage.

## Production Checklist
**(STANDARD)**

Before deploying any code that passed doubt-driven review, verify ALL of:

1. All non-trivial decisions have at least 1 extracted claim — claim count >= number of functions changed in diff
2. Every claim has traceability anchor: file path + line range, spec section reference, or test case ID
3. No claim exceeded 3 doubt cycles — hard stop enforced, residual doubt documented for all cycle-3 claims
4. Doubt theater filtered: all doubts are substantive (specific failure condition + testable counter-claim)
5. All CRITICAL severity doubts have RESOLVED or ACCEPTED_WITH_MONITORING status — no open CRITICAL doubts
6. Every ACCEPTED doubt has a monitoring plan with alert configuration and re-open threshold
7. Cross-model escalation completed for all CRITICAL claims that reached cycle 3
8. RECONCILE.md entries exist for all non-HOLDS doubt resolutions, with decision rationale and residual risk
9. Author ≠ reviewer enforced: git hook blocks self-review on critical paths, cross-model escalation triggered
10. Pre-mortem completed for architecture decisions: top-3 failure modes identified and mitigated
11. Reviewer calibration tracked: defect discovery rate, miss rate, and confidence calibration logged per reviewer
12. Doubt inventory quantified: total claims, resolved, accepted risk, deferred (with escalation deadline)
13. Verification script passes: `scripts/verify-skill.sh` — all checks green
14. Rollback plan documented: previous version artifact tagged, rollback procedure tested for any code changed during doubt resolution

## Anti-Patterns

- **The false confidence of passing tests.** A test suite with 95% coverage that only tests happy paths proves nothing. Every test is a claim that the code behaves correctly under that input. Doubt every test that doesn't include: null input, boundary value, concurrent access, timeout, and error propagation. A $200K payment processing bug at a major retailer passed all unit tests because no test sent a negative quantity. **Total cost: $150K-$500K per incident in refund processing, audit overhead, and reputation damage. Fix: add property-based testing for every CRITICAL claim.**

- **The cost of doubt theater in meetings.** A team of 5 senior engineers spending 30 minutes per PR on performative doubt ("have we considered edge cases?") across 10 PRs per sprint wastes 2.5 engineer-hours per sprint on theater. At $150/hr fully loaded, that's $375/sprint, $9,750/quarter in pure process waste — with zero defects actually found. **Total cost: $30K-$50K/year in wasted engineering time for a mid-size team. Fix: implement the Doubt Theater Detection tree as a pre-filter before any doubt is discussed.**

- **The "reviewed by author" blind spot.** When the same person who wrote the code marks it as reviewed, defect discovery drops 60-80% compared to fresh-context review. A startup lost $85K in AWS charges over a weekend when an author-reviewed infinite retry loop shipped to production — the author "knew" the retry logic was bounded because they wrote it, but the code had no max-retry guard. **Total cost: $50K-$200K per incident in cloud overage, downtime, and emergency fix deployment. Fix: enforce R5 mechanically — git hook that blocks self-review on critical paths.**

- **The escalating cost of unreconciled doubt.** Each unreconciled doubt that is "deferred to next sprint" becomes an invisible tax. After 3 sprints of deferral, the doubt is forgotten, the original reviewer has moved on, and the code is now depended upon by 4 other modules. Fixing it then costs 3-8x the original fix cost due to ripple effects. A fintech company spent $120K refactoring a transaction engine because a concurrency doubt deferred in sprint 3 became a cascade failure in sprint 12. **Total cost: $60K-$250K per deferred doubt that becomes a production incident, in refactoring, downtime, and lost engineering trust. Fix: RECONCILE.md entries auto-escalate if unresolved after 2 sprints.**

- **Cross-model review: the $5K insurance policy.** A single cross-model review (Claude → GPT-4o or vice versa) costs ~$2-5 in API tokens and 10 minutes of engineer time. It catches defects that single-model review misses 15-30% of the time. Skipping cross-model review on a CRITICAL claim that reaches cycle 3 is gambling $5 against the $50K-$500K cost of a production defect. An e-commerce platform skipped cross-model review on a checkout flow claim — the bug (race condition in inventory deduction) cost $340K in oversold inventory and customer compensation. **Total cost: $50K-$500K per missed cross-model opportunity on CRITICAL claims. Fix: cross-model escalation is mandatory at cycle 3 for CRITICAL severity.**

- **The "quiet acceptance" anti-pattern.** When a reviewer lacks confidence to challenge a senior engineer's code, they silently ACCEPT doubts without resolution. This is deference, not reconciliation. A medical device software team had 14 ACCEPTED doubts on a drug-dosage calculation module over 6 months — 3 of those doubts became actual patient-safety incidents. The FDA 483 observation cost $180K in remediation and delayed product launch by 4 months. **Total cost: $100K-$500K in regulatory remediation, launch delays, and potential liability. Fix: ACCEPTED doubts on safety-critical paths require a second reviewer's sign-off — never single-reviewer acceptance.**

- **The trust decay curve.** Every time a doubt-driven review finds a defect that standard review missed, team trust in standard review erodes. After 5 such incidents, engineers start running informal doubt cycles on every PR regardless of criticality — burning 40% more review time with no process guardrails. Without formal doubt-driven development, you get the cost of adversarial review without the structure. **Total cost: $80K-$200K/year in stealth process overhead for a 10-engineer team. Fix: formalize doubt-driven development as an explicit, opt-in process; don't let it become a shadow process.**

## Verification

<!-- Run this checklist before marking any doubt cycle complete -->

- [ ] **Ground Rules:** All 7 ground rules checked. No violations unaddressed. Run `grep -c "DOUBT_THEATER" doubt_log.md` — each flag must have a reformulation or dismissal note.
- [ ] **Claims extracted:** Every non-trivial decision in the diff has at least 1 claim. Run `grep -c "CLAIM-" claims.md` — count should exceed number of functions changed.
- [ ] **Claims anchored:** Every claim has file:line, test reference, or spec section. Run `grep -c "file:\|line:\|spec:\|test:" claims.md` — count must equal total claims.
- [ ] **Doubt cycles:** No claim exceeded 3 cycles. Run `grep -c "CYCLE-4\|cycle: 4" doubt_log.md` — must return 0.
- [ ] **Doubt theater filtered:** All doubts are substantive (specific failure condition + test). Run `grep -c "have we considered\|what about\|edge cases\|best practices" doubt_log.md` — each hit must have a resolution note within 3 lines.
- [ ] **Critical reconciled:** All CRITICAL severity doubts have RESOLVED status. Run `grep "CRITICAL" doubt_log.md | grep -v "RESOLVED"` — must return 0.
- [ ] **Residual risk documented:** Every ACCEPTED doubt has a monitoring plan with alert configuration. Run `grep "ACCEPTED" RECONCILE.md | grep -v "monitoring\|alert\|runbook"` — must return 0.
- [ ] **Cross-model considered:** Every CRITICAL doubt that reached cycle 3 has an escalation record. Run `grep "CRITICAL.*cycle: 3" doubt_log.md | grep -v "escalat"` — must return 0.
- [ ] **STOP report complete:** All phases produce output artifacts. RECONCILE.md has entries for every non-HOLDS doubt.
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`. All checks must pass.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

Core methodology references for deeper study:

- **(../references/claim-extraction-guide.md)** — How to extract falsifiable claims from code, design docs, and specifications. Includes claim taxonomy, extraction heuristics for 8 languages, and common claim blind spots.
- **(../references/doubt-injection-patterns.md)** — Catalog of 25+ adversarial doubt patterns organized by domain: security, concurrency, data integrity, error handling, performance, and distributed systems. Each pattern includes test generation template.
- **(../references/reconciliation-protocol.md)** — Structured reconciliation workflow with templates for RESOLVED, ACCEPTED, DEFERRED, and ESCALATED outcomes. Includes decision record format and residual risk quantification framework.
- **(../references/cross-model-escalation.md)** — When and how to escalate a doubt to a different model. Model pairing guide (GPT-4o ↔ Claude, Gemini ↔ Claude), cost estimation, and blind-spot coverage matrix.
- **(../references/cycle-termination-rules.md)** — Hard stop criteria, residual doubt acceptance framework, and the mathematics of diminishing returns on doubt cycles. When the 4th cycle costs more than the risk it addresses.
- **(../references/doubt-theater-detection.md)** — Taxonomy of performative doubt with 15+ patterns, detection heuristics, and the reformulation protocol. How to convert theater into substantive doubt without shaming the reviewer.
- **(../references/adversarial-review-checklist.md)** — Reviewer's pre-flight and in-flight checklist for fresh-context adversarial review. Includes context-reset protocol, bias calibration, and defect discovery rate tracking.
- **(../references/cost-of-defects-calculator.md)** — Quantitative framework for deciding when doubt-driven development is worth the investment. Includes defect cost curves by industry (fintech, healthtech, e-commerce, infrastructure), break-even analysis, and ROI calculator.
