# Adversarial Review Checklist

## Reviewer's Pre-Flight and In-Flight Checklist

This checklist enforces the adversarial stance. Run through it before starting any review
and at each phase transition. The goal is not to catch everything — it's to catch what the
author couldn't see because they were too close to the code.

---

## Pre-Flight: Context Reset Protocol

Before opening the code, reset your context:

- [ ] **Clear author identity.** Hide git blame. Do not look at who wrote the code until after
      the review. Use `git diff --no-color | grep -v "^Author:"` to strip authorship.
- [ ] **State your adversarial intent aloud or in writing:** "My job is to find what is WRONG
      with this code. Every line is a claim that I will try to falsify."
- [ ] **Set your bias expectations:** List 3 cognitive biases you're prone to (see Expert's
      Mindset). Actively check for them during review.
- [ ] **Set cycle budget:** How many claims do you estimate? Budget 2-3 minutes per claim for
      cycle 1, 5 minutes per claim for cycles 2-3. Total review time = claims × 8 min.
- [ ] **Identify critical surfaces:** Before reading code, list which security/auth/data
      surfaces this diff touches (check file paths against known critical paths).

---

## Phase 1: Claim Extraction Checklist

- [ ] **Every branching point examined:** if/else, switch, ternary, guard clause, try/catch
- [ ] **Every function call with arguments examined:** what does it assume about return values?
- [ ] **Every async operation examined:** ordering, timing, failure, and timeout assumptions
- [ ] **Every trust boundary crossing examined:** input validation, auth check, output encoding
- [ ] **Every data mutation examined:** integrity, rollback, idempotency, concurrency
- [ ] **Implicit claims extracted:** the "else" that isn't written, the default that's assumed
- [ ] **Claims labeled and numbered:** CLAIM-NNN with type tag and file:line reference
- [ ] **Minimum claim count met:** claims ≥ number of functions changed

---

## Phase 2: Extraction/Anchoring Checklist

- [ ] **Every claim has file:line or spec reference** (no untethered claims)
- [ ] **FOR evidence listed:** test cases, documentation, or prior review that supports claim
- [ ] **AGAINST evidence listed:** missing tests, uncovered paths, unhandled states
- [ ] **Testability confirmed:** can you write a test that would DISPROVE each claim?
- [ ] **Chain claims identified:** claims that depend on other claims being true — flag as
      compound risk

---

## Phase 3: Doubt Cycle Checklist

### Per Cycle
- [ ] **Doubt is falsifiable:** "Claim would be WRONG if [condition]" — not "might be wrong"
- [ ] **Test is concrete:** grep command, curl request, test case, or benchmark — not "we should check"
- [ ] **Evidence is recorded:** command output, test result, or file inspection finding
- [ ] **Severity assigned:** CRITICAL/HIGH/MEDIUM/LOW using the severity decision tree
- [ ] **Cycle count tracked:** cycle number recorded in doubt_log.md
- [ ] **Doubt theater scanned:** search for generic patterns (DT-1 through DT-15)

### After Cycle 3
- [ ] **Hard stop enforced:** no 4th cycle unless new evidence or regulatory requirement
- [ ] **Residual doubt documented:** probability, impact, monitoring plan, re-evaluation date

---

## Phase 4: Reconciliation Checklist

- [ ] **Every non-HOLDS doubt has a status:** RESOLVED, ACCEPTED, DEFERRED, or ESCALATED
- [ ] **RESOLVED doubts have:** code change + regression test + verification
- [ ] **ACCEPTED doubts have:** risk quantification + monitoring alert + runbook + review date
- [ ] **DEFERRED doubts have:** ticket link + short-term mitigation + auto-escalation trigger
- [ ] **ESCALATED doubts have:** cross-model review report + deadline + fallback plan
- [ ] **CRITICAL doubts:** all RESOLVED (no ACCEPTED CRITICAL)
- [ ] **HIGH doubts:** RESOLVED or ACCEPTED with director-level sign-off if risk > 0.5×HIGH

---

## Phase 5: Stop Checklist

- [ ] **Merge decision rendered:** CLEAR TO MERGE / MERGE WITH MONITORING / DO NOT MERGE
- [ ] **STOP report complete:** claims extracted, cycles run, reconciled, residual risks cataloged
- [ ] **Artifacts archived:** claims.md, doubt_log.md, RECONCILE.md committed or attached to PR
- [ ] **Cross-model escalation records attached** (if any)
- [ ] **Residual risk monitoring configured** before merge (if MERGE WITH MONITORING)

---

## Defect Discovery Rate Tracking

Track your own performance to calibrate your adversarial intuition:

```
SESSION: [date] — PR #[number] — [component]
Claims extracted:  [N]
Doubt cycles run:   [M]
Doubts substantiated (claim failed): [S]
Doubts unsubstantiated (claim held): [U]
Doubt theater flagged: [T]
Discovery rate: [S / N] — target > 15% for adversarial review
Time spent: [minutes]
```

**Calibration targets:**
- Discovery rate < 5%: You may be performing theater, not adversarial review
- Discovery rate 15-30%: Healthy adversarial stance
- Discovery rate > 50%: Code may have systemic issues — escalate to team discussion
