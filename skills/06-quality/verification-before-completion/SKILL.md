---
name: verification-before-completion
description: >
  Use when completing a bug fix, feature implementation, or any code change; when a task is marked as "done" but hasn't been verified; when closing issues or pull requests; or when the cost of regression is high (production systems, financial software, healthcare). Handles explicit verification against original reproduction case, assertion confirmation (expected behavior confirmed), regression test suite execution, verification evidence documentation (screenshots, logs, test output), anti-rationalization checklist for false completion, and verification gate enforcement before status transitions. Do NOT use for writing tests (route to tdd-guide or qa-engineer), code review (route to code-reviewer), or CI/CD pipeline configuration (route to ci-cd-builder).
license: MIT
author: Sandeep Kumar Penchala
type: quality
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - verification
  - quality-assurance
  - bug-fix
  - regression
  - testing
  - completion-gate
  - anti-rationalization
token_budget: 4000
chain:
  consumes_from:
    - qa-engineer
    - tdd-guide
    - code-reviewer
  feeds_into:
    - release-manager
    - incident-responder
    - qa-engineer
  alternatives: []
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Verification Before Completion
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Before marking any bug fix, feature, or task as complete, explicitly verify the fix works. Run the reproduction case, check the assertion, verify no regression. The fix isn't done until you've proven it works.

## Route the Request

<!-- TWO-TIER ROUTING: Auto-Route table (machine) → Intent Route tree (human fallback) -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "verification-before-completion")` — this is your skill | Redirect: "I am Verification Before Completion. Route by intent matching below." |
| A2 | Issue or PR body contains `fixes #` or `closes #` but no verification evidence (screenshot, log, test output) attached | **BLOCK STATUS TRANSITION** — Require reproduction case re-run + evidence before closing. Gate: no evidence = no close. |
| A3 | Bug report includes reproduction steps (`Steps to Reproduce`, `STR`, `Reproduction`) | **REPRODUCTION-AVAILABLE** — Run the EXACT reproduction case. Verify it fails before fix, passes after. Document both states. |
| A4 | Task marked "done" or "complete" in tracker but tests were never run | **FALSE-COMPLETE RISK** — Reopen. Require full regression suite execution. Gate: all tests must pass before re-marking done. |
| A5 | Change touches `auth/`, `payment/`, `crypto/`, `migration/`, `data/`, or `admin/` paths | **HIGH-STAKES** — Additional verification layers: manual reproduction + automated regression + peer sign-off. Gate: all three before transition. |
| A6 | Hotfix or emergency patch with truncated process | **POST-HOTFIX VERIFICATION** — Allow deployment but schedule mandatory verification within 24 hours. File a verification ticket with reproduction case. |
| A7 | None of the above — general task completion | **STANDARD** — 5-phase workflow (Reproduce → Apply Fix → Verify Fix → Regression Check → Evidence Collection). |

```
What are you trying to do?
├── Verify a bug fix → Start at "Core Workflow > Phase 1" (Reproduce from bug report)
│   ├── I have reproduction steps → "Phase 1: Reproduce" — run exact case, confirm failure
│   ├── No reproduction steps available → "Decision Trees > Reproduction Case Adequacy Check"
│   └── Reproduction passes (fix already applied)? → "Decision Trees > Anti-Rationalization Detection"
├── Verify a feature implementation → Start at "Core Workflow > Phase 3" (Verify against acceptance criteria)
│   ├── Feature has acceptance criteria → Map each criterion to a verification action
│   └── No acceptance criteria documented → STOP. Cannot verify. Request criteria from product owner.
├── Mark a task as "done" → Start at "Decision Trees > Status Transition Gate"
│   ├── All tests passing? → Continue to "Evidence Sufficiency Decision"
│   ├── Some tests failing? → STOP. Cannot transition. File bug for each failure.
│   └── Tests were never run? → STOP. Run them first. "Done" without verification is a lie.
├── Close an issue or PR → Start at "Core Workflow > Phase 4" (Regression Check)
│   ├── Fix is in production? → Monitor production metrics for the specific error rate
│   ├── Fix needs deploy → Verify in staging first, then production
│   └── Issue is "works for me" → STOP. Cannot close. Request reproduction from reporter.
├── Need to write tests → Invoke tdd-guide or qa-engineer skill instead
├── Need code review → Invoke code-reviewer skill instead
├── Need CI/CD config → Invoke ci-cd-builder skill instead
└── Not sure where to start? → "Core Workflow > Phase 1" (Reproduce) — always start by proving it's broken
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable. They detect the most common verification failures before they become production incidents.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to mark complete without running exact reproduction case | Trigger: Task status = "done" OR issue status = "closed" without a log entry, screenshot, or test output showing the EXACT reproduction case from the bug report being executed and passing | STOP. Respond: "Cannot mark complete. The reproduction case from [bug report ID] has not been re-run. The fix is unproven until you execute the exact steps the reporter used and confirm they now produce the expected result. Re-run those steps now." |
| R2 | DETECT anti-rationalization excuses that bypass verification | Trigger: Text matching patterns: "obviously correct", "trivial change", "can't break", "should work", "I tested manually", "CI will catch", "just a one-liner", "no way this fails" — in commit messages, PR comments, or task updates | STOP. Respond: "ANTI-RATIONALIZATION DETECTED: '[matched phrase]'. This is a known cognitive bias. Trivial changes cause the highest rate of regressions (proportional to their volume). Manual testing is not reproducible. Run the automated verification now." |
| R3 | REFUSE to close an issue without verifiable evidence of the fix | Trigger: Issue closure with no attachment (screenshot, log, test output, video) demonstrating the fix working — check for `![screenshot]`, ` ``` ` code block with test output, or file attachments in the closing comment | STOP. Respond: "Cannot close [issue ID]. No verification evidence attached to the closing comment. Minimum: (1) screenshot of the fixed behavior, (2) test output showing the reproduction case passing, or (3) log excerpt confirming the expected result. Attach evidence before closing." |
| R4 | DETECT when the reproduction case passes for the wrong reason | Trigger: Reproduction case output shows success, but the output does not match the EXPECTED behavior from the bug report, acceptance criteria, or specification — compare actual output string against expected output | STOP. Respond: "FALSE POSITIVE: The reproduction case passes, but the output does not match the expected behavior. Expected: '[expected from spec]'. Got: '[actual output]'. The test may be testing the wrong thing. Re-examine: is the assertion checking the correct condition?" |
| R5 | REQUIRE regression suite execution before status transition | Trigger: Git diff touches files outside the immediate fix area OR modifies shared utility/library code used by other modules — any file changed that is imported by ≥2 other files (check `grep -r "import.*from.*changed-file"` count) | STOP. Respond: "REGRESSION RISK: [changed-file] is imported by [N] other modules. Run the full regression suite for those dependents before transitioning. Scope: run tests in [list dependent test files]. Gate: all must pass." |
| R6 | DETECT silent failures — test passes but expected behavior absent | Trigger: Test assertion uses weak matchers (`toBeTruthy()`, `not.toBeNull()`, `toBeDefined()`), OR test only checks "no error thrown" without asserting the correct output, OR test passes but the feature is observably not working in production | STOP. Respond: "SILENT FAILURE RISK: The test at [file:line] uses weak matchers that cannot distinguish correct from incorrect behavior. Replace with specific assertions: expected value, expected output format, expected side effect. A test that only checks 'no crash' is not verification." |

## The Expert's Mindset

Verification masters think differently about "done." They know that the human brain is wired to declare victory prematurely — cognitive closure is rewarding. The master's job is to resist that urge long enough to prove the work is actually correct.

### Core Beliefs of Verification Masters

| Belief | Why It Matters |
|---|---|
| "Done" is a hypothesis, not a fact — until verified | Every status transition is a claim. Verification is the experiment that tests the claim. |
| The original reproduction case is sacred | If you don't reproduce with the reporter's exact steps, you haven't tested their problem. Different inputs = different test. |
| Regression is the silent killer | Your fix works. But does the rest of the system still work? Every change is a butterfly effect candidate. |
| Evidence outlasts memory | In six months, nobody will remember that you "tested it manually." But the screenshot in the issue will still be there. |
| Verification is a gate, not a checkbox | It's not paperwork. It's the last line of defense before a bug reaches users. Treat it accordingly. |

### Anti-Rationalization Table

The brain generates excuses to avoid verification. Learn to recognize them. Every one of these has caused a production incident.

| Excuse | Reality |
|---|---|
| "The change is obviously correct" | Obvious changes are the ones that introduce regressions. The simpler it looks, the less anyone verifies it. |
| "I already tested it manually" | Manual testing is not reproducible, not auditable, and not reliable across environments. If it's not automated, it didn't happen. |
| "The CI will catch issues" | CI doesn't run the exact reproduction case. It runs a generic suite. The reproduction case tests a specific scenario that CI may not cover. |
| "It's just a one-line change" | One-line changes have caused billion-dollar outages. Complexity is not measured in lines — it's measured in blast radius. |
| "It works on my machine" | The reporter's machine, data, and configuration are different. Your machine passing proves nothing about their environment. |
| "I'll verify it after the release" | Post-release verification discovers bugs that are already in production. The cost of a post-release fix is 10-100x higher. |
| "The test coverage is 95%, we're fine" | Coverage measures lines executed, not behaviors verified. 95% coverage with weak assertions is 0% verification. |
| "Nobody else verifies their fixes this thoroughly" | Nobody else catches the regressions you'll prevent. Verification is a competitive advantage for the team that does it. |

### What Masters Know That Others Don't

- **The reproduction case is worth more than the fix.** Understanding the EXACT reproduction beats any amount of code reading. If you can't reproduce it, you don't understand it.
- **Every verification should answer two questions:** (1) Does the fix solve the original problem? (2) Does the fix create any new problems? Skip either question and you haven't verified.
- **Silent failures are more dangerous than loud ones.** A test that passes for the wrong reason creates a false sense of security. A crashing test at least tells you something is wrong.
- **Verification evidence compounds.** A screenshot today saves 30 minutes of re-investigation next quarter. Document what you proved and how you proved it.
- **The best verifiers are paranoid about "it works now."** They immediately ask: "But does it work for the right reason? And will it still work tomorrow?"

### When to Break Your Own Rules

- **Hotfix in a P0 incident**: Verify the fix stops the bleeding. Deploy. Then file a mandatory post-incident verification ticket with a 24-hour SLA. Never skip verification — defer it.
- **Truly unreproducible heisenbugs**: Document every attempt to reproduce (dates, environments, inputs tried). Add observability (logging, metrics) at the suspected failure point. Close only when instrumentation is in place to capture the next occurrence.
- **Third-party dependency fix**: Verify the dependency upgrade resolves the issue. Add a regression test that would catch a regression if the dependency reintroduces the bug. Trust but verify.

## Operating at Different Levels

Verification scales with the blast radius of the change. A CSS fix verifies differently than a database migration.

| Level | Verification Output Characteristics |
|---|---|
| **L1 — Single-line fix** | Run reproduction case. Run the test file covering the changed function. Verify no console errors. Document with one screenshot. |
| **L2 — Feature implementation** | Map each acceptance criterion to a verification action. Run full module test suite. Cross-browser/platform check if applicable. Document with test output + screenshots. |
| **L3 — Cross-module change** | Run reproduction case. Run full regression suite for all affected modules. Check for performance regression. Verify API compatibility. Document with test suite output + performance comparison. |
| **L4 — Platform-wide release** | Staged verification: dev → staging → canary → production. Smoke tests at each stage. A/B metric comparison. Rollback plan verified. Document with dashboard screenshots + metric comparisons. |

**Usage**: Say "verify this at L2" or "I need L3 verification on this migration." Default: **L2** (feature-level verification).

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Completing a bug fix and about to mark the issue as resolved
- Implementing a feature and transitioning the task to "done"
- Closing a pull request that "fixes #issue-number"
- About to merge a change that touches shared infrastructure or utilities
- Working on a production system where regression cost is high (financial, healthcare, auth)
- Preparing a release candidate and need verification gates
- Responding to a "works for me" closure with insufficient evidence
- Auditing completed work for verification completeness

### Do NOT Use

- **Writing tests for new code** — route to `tdd-guide` (test-first development) or `qa-engineer` (test strategy)
- **Performing code review** — route to `code-reviewer`
- **Setting up CI/CD verification gates** — route to `ci-cd-builder`
- **Debugging a live issue** — route to `debugging-and-error-recovery`
- **Security penetration testing** — route to `security-reviewer`
- **Performance benchmarking** — route to `performance-engineer`

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1: Reproduce (~5 min)

**Goal**: Prove the bug exists using the reporter's EXACT steps.

1. Locate the reproduction case in the bug report, issue, or ticket.
2. Execute every step EXACTLY as written. Do not skip, abbreviate, or "optimize" steps.
3. Confirm the bug manifests — the actual output matches the reported incorrect behavior.
4. Capture evidence of the failure: screenshot, log output, or test failure output.

**Gate**: Cannot proceed to Phase 2 until reproduction is confirmed. If reproduction fails:
- The environment may differ from the reporter's — investigate.
- The bug may be intermittent — try multiple times, vary timing.
- The reproduction steps may be incomplete — request clarification from the reporter.

**Output**: Evidence of the bug BEFORE the fix (screenshot, log, test failure).

### Phase 2: Apply Fix (~10-30 min)

**Goal**: Implement the change that resolves the bug or completes the feature.

1. Write the fix. If using TDD, write the failing test first (route to `tdd-guide`).
2. Keep the fix minimal — change only what's necessary to resolve the issue.
3. If the fix touches code imported by other modules, flag for regression testing in Phase 4.

**Gate**: The fix must be the smallest change that resolves the reproduction case. Over-engineered fixes introduce their own regressions.

**Output**: Code change (diff) ready for verification.

### Phase 3: Verify Fix (~5 min)

**Goal**: Prove the fix resolves the original issue.

1. Run the EXACT same reproduction case from Phase 1.
2. Confirm the output now matches the EXPECTED behavior from the bug report.
3. Verify the fix works for the right reason — not just that the test passes, but that the correct logic path executes.
4. Capture evidence of success: screenshot, log output, or test pass output.

**Gate**: Cannot proceed to Phase 4 until the reproduction case passes with correct output. If it passes but the output is wrong, the fix is incomplete.

**Output**: Evidence of the bug AFTER the fix, showing correct behavior.

### Phase 4: Regression Check (~10 min)

**Goal**: Prove the fix didn't break anything else.

1. Run the full test suite for the module containing the fix.
2. If the changed file is imported by other modules, run their test suites too.
3. Run any integration or end-to-end tests that exercise the affected code path.
4. Check for new warnings, deprecation notices, or console errors.

**Gate**: All existing tests must pass. Any new failure is a regression and must be investigated before status transition.

**Output**: Test suite results (pass/fail counts, any new failures).

### Phase 5: Evidence Collection (~5 min)

**Goal**: Document verification so future readers can confirm the fix was verified.

1. Compile evidence into the issue/PR closing comment:
   - **Before**: Screenshot/log of the bug reproducing (from Phase 1)
   - **After**: Screenshot/log of the fix working (from Phase 3)
   - **Tests**: Test suite output showing all passing (from Phase 4)
2. If using an issue tracker, attach evidence files directly (not links that can rot).
3. Add a verification summary line: "Verified on [date] by [method] against reproduction case [link]."

**Gate**: No issue or PR should be closed without at least one piece of verifiable evidence attached.

**Output**: Closing comment with verification evidence.

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Reproduction Case Adequacy Check

```
Bug report has reproduction steps?
├── YES, complete → Use them EXACTLY. Proceed to Phase 1.
├── YES, but incomplete → Request missing details from reporter. Cannot verify without full steps.
│   ├── Missing environment? → Ask: "What browser/OS/version?"
│   ├── Missing input data? → Ask: "What specific data triggers this?"
│   └── Missing expected behavior? → Ask: "What should happen instead?"
├── NO reproduction steps → STOP. Cannot verify. Respond:
│   "Without reproduction steps, I cannot verify this fix. Please provide:
│    1. Exact steps to trigger the bug
│    2. What you expected to happen
│    3. What actually happened
│   I cannot close this issue until I can reproduce and verify the fix."
└── "Steps" are a video/GIF only → Transcribe key steps into text. Videos are not reproducible (can't copy-paste inputs).
```

### Anti-Rationalization Detection

```
Hear yourself or others say...
├── "The change is obviously correct"
│   └── COUNTER: "Obvious changes cause the most regressions. Verify anyway."
├── "I already tested it manually"
│   └── COUNTER: "Manual testing is not reproducible. Run the automated case."
├── "The CI will catch issues"
│   └── COUNTER: "CI doesn't run the reporter's exact reproduction case."
├── "It's just a one-line change"
│   └── COUNTER: "One-line changes have caused billion-dollar outages."
├── "It works on my machine"
│   └── COUNTER: "The reporter's machine is different. Verify in their environment."
├── "I'll verify it after the release"
│   └── COUNTER: "Post-release bugs cost 10-100x more to fix. Verify now."
├── "The test coverage is X%, we're fine"
│   └── COUNTER: "Coverage measures lines, not behavior. Weak assertions = false confidence."
└── "Nobody else does this"
    └── COUNTER: "Nobody else catches the regressions we will. This is our edge."
```

### Regression Scope Selection

```
What did the change touch?
├── Single file, no imports from other modules → Run that file's test suite only.
├── Single file, imported by N other modules → Run all N dependent test suites.
│   └── FIND dependents: grep -r "import.*from.*'changed-file'" --include="*.ts" --include="*.js"
├── Shared utility or library code → Run FULL project test suite. No exceptions.
├── Database schema or migration → Run integration tests + verify rollback works.
├── API endpoint or contract → Run contract tests + verify backward compatibility.
├── Configuration or environment variable → Run tests in all affected environments.
├── UI component → Run component tests + visual regression tests + cross-browser check.
└── Infrastructure (Docker, K8s, Terraform) → Run infrastructure tests + verify in staging first.
```

### Evidence Sufficiency Decision

```
What evidence do you have?
├── Reproduction case failing BEFORE fix → REQUIRED. Minimum: one screenshot or log.
├── Reproduction case passing AFTER fix → REQUIRED. Minimum: one screenshot or log.
├── Full test suite passing → REQUIRED for L2+. Attach test output or CI link.
├── Peer review sign-off → REQUIRED for high-stakes changes (auth, payments, data).
├── Staging environment verification → REQUIRED for L4 platform releases.
├── Production metric monitoring → REQUIRED for post-deploy verification window (24-72 hours).
└── None of the above → STOP. Cannot close. Minimum bar: BEFORE + AFTER + TEST SUITE.
```

### Status Transition Gate

```
Ready to mark this task as "done"?
├── Phase 1 complete? (Bug reproduced before fix) → Continue
│   └── NO → STOP. Cannot verify what you haven't reproduced.
├── Phase 2 complete? (Fix applied) → Continue
├── Phase 3 complete? (Bug verified fixed) → Continue
│   └── NO → STOP. Fix hasn't been proven to work.
├── Phase 4 complete? (Regression suite passing) → Continue
│   └── NO → STOP. Fix may have broken something else.
├── Phase 5 complete? (Evidence attached) → Continue
│   └── NO → STOP. No auditable record of verification exists.
├── Anti-rationalization check passed? (No excuses detected) → Continue
│   └── NO → STOP. You're rationalizing. Verify properly.
├── All gates passed → TRANSITION TO DONE.
└── Any gate failed → Return to the failed phase. Do not mark done.
```

## Cross-Skill Coordination

Verification doesn't happen in isolation. It integrates with the broader quality and delivery pipeline.

| Skill | Relationship | Handoff Pattern |
|---|---|---|
| **qa-engineer** | Consumes test strategies and coverage reports | Before verification: "QA Engineer, what tests should I run for this change?" After verification: "QA Engineer, here's the verification evidence — does it meet the quality bar?" |
| **tdd-guide** | Consumes test-first workflow | If no reproduction test exists: "TDD Guide, help me write a failing test for this reproduction case." Then verify against that test. |
| **code-reviewer** | Consumes code review findings | After code review: "Code Reviewer flagged [N] issues. I've addressed them. Verification confirms: (1) original bug fixed, (2) reviewer concerns resolved, (3) no regressions." |
| **release-manager** | Feeds verification gates into release readiness | Before release: "Release Manager, verification for [ticket IDs] is complete. Evidence attached. All gates passed. Ready for release." |
| **incident-responder** | Feeds post-incident verification | After incident: "Incident Responder, hotfix verified: reproduction case resolved, no regressions. Post-incident verification ticket filed for [date]." |

## Proactive Triggers

| Trigger Pattern | Automatic Response |
|---|---|
| Commit message contains "fix" or "fixes" | Check: is there a linked issue with reproduction steps? If not, flag. |
| PR body contains "fixes #[number]" but no verification section | Add a verification checklist to the PR: "Did you: [ ] Reproduce the bug [ ] Verify the fix [ ] Run regression tests [ ] Attach evidence?" |
| Issue closed without comment | Flag for reopen. Silent closure = unverified closure. |
| Task moved to "Done" column without linked test run | Check CI for a passing test run on the relevant commit. If none, flag. |
| "Works for me" response on a bug report | Challenge: "Could not reproduce" is not the same as "fixed." Request the reporter's environment details. |
| Merge to main without associated test run | Check if the merge commit has a passing CI run. If CI was skipped, flag for post-merge verification. |

## What Good Looks Like

### Before (Premature "Done")

```
Issue #247: "Checkout fails with 'Cannot read property price of undefined'"

Status: Closed
Closing comment: "Fixed in commit a1b2c3d. The null check was missing."
Attachments: None
Test run: Not linked
```

**Problems**: No evidence the bug was reproduced. No evidence the fix works. No regression check. The issue could still be broken — nobody will know until a user reports it again.

### After (Verified Completion)

```
Issue #247: "Checkout fails with 'Cannot read property price of undefined'"

Status: Closed
Closing comment:
  **Verified on 2026-07-23 against reproduction case from the issue.**

  BEFORE (reproduced):
  ```
  Steps: Add item to cart → Proceed to checkout → Click "Place Order"
  Result: TypeError: Cannot read property 'price' of undefined at checkout.ts:142
  ```

  AFTER (verified fixed):
  ```
  Steps: Add item to cart → Proceed to checkout → Click "Place Order"
  Result: Order confirmed. Order ID: #89241
  ```

  **Regression suite**: 247 tests passing, 0 failing. Full suite run: [CI link]
  **Evidence**: [screenshot-before.png] [screenshot-after.png] [test-output.log]
```

**Strengths**: Exact reproduction steps documented. Before and after evidence. Regression suite results attached. Auditable by anyone — today or six months from now.

## Deliberate Practice

### Exercise 1: The False-Positive Reproduction
Find a closed bug in your project. Re-run the reproduction steps from the issue. Does the bug still occur? If yes, the "fix" was never verified — it was a false close. Document your findings.

### Exercise 2: Anti-Rationalization Audit
Review the last 10 issues your team closed. Count how many have verification evidence (screenshot, log, test output) in the closing comment. Calculate your team's verification rate. Target: >80%.

### Exercise 3: Weak Assertion Hunt
Search your test suite for weak matchers: `toBeTruthy()`, `not.toBeNull()`, `toBeDefined()`. For each one, ask: "Could this test pass while the feature is broken?" Replace weak assertions with specific expected values.

### Exercise 4: Regression Blast Radius
Pick a shared utility in your codebase. Change one line. Run `grep -r "import.*from.*'utility-name'"` to find all dependents. Run ALL their tests. How many would have caught a subtle breakage? How many wouldn't?

### Exercise 5: The 24-Hour Verification Challenge
For one week, require verification evidence (BEFORE + AFTER + TEST SUITE) on every closed issue. At week's end, count: how many issues were reopened because verification caught an incomplete fix? This number is your return on the verification investment.

## Gotchas

- **The "obviously correct" change that introduces a regression**: A developer adds a null check to `getUser()`. The null check is correct, but it changes the return type from `User` to `User | null`. Every caller that didn't handle null now has a latent bug. Cost: **$50,000+** in debugging, hotfix, and customer compensation for a payment-processing outage caused by an unhandled null in the checkout flow.

- **Manual-only testing that can't be reproduced**: A bug is "fixed" and "tested manually" but no reproduction case is documented. Three months later, the same bug resurfaces. Nobody remembers how to reproduce it or what the fix was. The team spends **$15,000** in engineering time rediscovering the bug and re-fixing it.

- **Skipping the exact reproduction case**: The developer writes a test that exercises the general area of the bug but not the EXACT scenario from the report. The test passes, the issue is closed. Two weeks later, the reporter comments: "Still broken." The fix addressed a different code path. Cost: **$10,000** in rework and lost trust from the reporter.

- **False-positive verification from weak assertions**: A test checks `expect(result).toBeTruthy()` and passes. But `result` is `{}` (empty object, truthy) when it should be `{ price: 19.99 }`. The bug ships to production. Cost: **$25,000** in incorrect invoices that require manual correction and customer apologies.

- **Unverified status transitions in issue trackers**: A project manager moves 15 issues to "Done" because the sprint ended, not because verification happened. Two sprints later, 8 of those issues are reopened with "Actually, this still doesn't work." Cost: **$40,000** in wasted sprint capacity and demoralized teams discovering that "done" meant nothing.

- **Deferred verification ("I'll check later")**: A developer merges a fix on Friday, planning to verify on Monday. Over the weekend, the fix causes a regression that affects 5,000 users. Monday morning, the support queue is flooded. Cost: **$75,000** in support hours, emergency engineering time, and reputational damage from a weekend outage.

- **Verification in the wrong environment**: A fix is verified in the developer's local environment (Node 20, fresh database). In production (Node 18, 2TB database with specific data), the fix fails because of a runtime API difference. Cost: **$100,000+** in production incident response, rollback, and post-mortem process.

## Verification

Run these checks to verify this skill file itself:

```bash
# Check required sections exist
grep -n "^## Ground Rules — Read Before Anything Else" SKILL.md
grep -n "^## The Expert's Mindset" SKILL.md
grep -n "^## Operating at Different Levels" SKILL.md
grep -n "^## When to Use" SKILL.md
grep -n "^## Route the Request" SKILL.md
grep -n "^## Core Workflow" SKILL.md
grep -n "^## Decision Trees" SKILL.md
grep -n "^## Cross-Skill Coordination" SKILL.md
grep -n "^## Proactive Triggers" SKILL.md
grep -n "^## What Good Looks Like" SKILL.md
grep -n "^## Deliberate Practice" SKILL.md
grep -n "^## Gotchas" SKILL.md
grep -n "^## Verification" SKILL.md
grep -n "^## References" SKILL.md

# Check 5+ decision tree subsections
grep -c "^### " SKILL.md

# Check 5+ dollar-quantified gotchas
grep -c '\$[0-9]' SKILL.md

# Check reference links
grep -oh 'references/[^)]*\.md' SKILL.md | sort -u
```

## References

1. [Reproduction Verification Guide](references/reproduction-verification.md) — How to run and document the exact reproduction case from a bug report.
2. [Assertion Checklist](references/assertion-checklist.md) — Criteria for strong vs. weak assertions; ensures tests actually verify correct behavior.
3. [Regression Detection](references/regression-detection.md) — Strategies for scoping and executing regression test suites after a fix.
4. [Evidence Documentation](references/evidence-documentation.md) — Standards for what constitutes verifiable, auditable evidence of a fix.
5. [Anti-Rationalization Table](references/anti-rationalization-table.md) — Complete catalog of cognitive biases that lead to false completion with counter-strategies.
6. [Verification Gates](references/verification-gates.md) — Gate definitions, pass/fail criteria, and enforcement mechanisms for each verification phase.
7. [False Completion Patterns](references/false-completion-patterns.md) — Recurring patterns where tasks are marked done without actual verification.
8. [Status Transition Rules](references/status-transition-rules.md) — Rules governing when an issue or task can transition from "in progress" to "done" or "closed."
