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
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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

### Solo (Single-line fix)
- Reproduce bug with reporter's exact steps; capture screenshot before fix
- Apply minimal fix; verify reproduction case now passes; capture screenshot after fix
- Run the test file covering the changed function; verify all pass
- Attach BEFORE/AFTER evidence to issue closure comment
- Self-review checklist: "Did I reproduce? Did I verify? Did I check for regressions? Did I attach evidence?"

### Small Team (Feature implementation)
- Map each acceptance criterion to a verification action — one test or manual check per criterion
- Run full module test suite + dependent module suites
- Cross-browser/platform check if applicable (Chrome, Firefox, Safari, mobile)
- Document with test output + screenshots in PR description
- Peer review sign-off on verification evidence before merge

### Medium Team (Cross-module change)
- Staged verification: reproduction → full regression suite → performance benchmark → API compatibility
- Run contract tests between affected services; verify backward compatibility
- Performance regression check: compare p95 latency before/after; fail if >20% degradation
- CI pipeline as verification gate: all suites pass, coverage thresholds met, lint clean
- Verification evidence packaged as release verification report

### Enterprise (Platform-wide release)
- Staged verification: dev → staging → canary → production — smoke tests at each stage
- A/B metric comparison: canary vs baseline for error rate, latency, business metrics
- Rollback plan verified: canary rollback tested before full rollout
- Production verification window: 24-72 hour monitoring with automated rollback on anomaly detection
- Verification audit trail: every stage logged with timestamps, evidence, and approver identity
- Compliance verification: SOC2, PCI, HIPAA evidence collected automatically from verification pipeline

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

## Core Workflow **(STANDARD)**

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


## Best Practices

1. **The self-verification checklist runs before you declare "done."** Before transitioning any task, run through: (a) Does the reproduction case pass? (b) Does the test suite pass? (c) Is evidence attached? (d) Did I check for regressions? If any answer is "no," you're not done — you're rationalizing. The checklist is not a suggestion; it's the gate between "works on my machine" and "verified."
2. **Output validation: match the exact expected behavior, not approximate.** "The output looks right" is not verification. Compare the actual output against the expected output from the bug report or spec — character by character, pixel by pixel, field by field. An off-by-one, a missing field, or a slightly different error message means the fix is incomplete, even if it "looks about right."
3. **Edge case testing is not optional — it's the difference between "fixed" and "actually fixed."** Every fix must be tested against: null/undefined inputs, empty collections, boundary values (0, -1, MAX_INT), invalid types, concurrent access, and timeout scenarios. The bug report describes one failure; edge cases describe the class of failures. Fix the class, not the instance.
4. **Regression verification: run tests in modules that import the changed file.** Use `grep -r "import.*from.*'changed-file'"` to find all dependents and run their test suites. A one-line change in a shared utility can break 20 downstream modules. If you didn't run their tests, you didn't verify.
5. **Peer review readiness: verification evidence is what the reviewer uses to approve.** Attach BEFORE/AFTER evidence to every PR and issue closure. A reviewer should be able to confirm the fix works without pulling the branch. Screenshots, test output, and CI links are auditable proof. "Verified locally" in a comment is not evidence — it's a claim.
6. **Environment parity: verify in the environment closest to production you can access.** A fix verified on Node 20 with a fresh database may fail on Node 18 with a 2TB production database. Staging verification is the minimum for any change touching data, auth, payments, or infrastructure. "Works on my machine" is the most expensive four words in software.
7. **Time-bound verification windows catch late-breaking regressions.** After deploying, monitor production metrics for 24-72 hours. Set alerts for error rate changes, latency spikes, and business metric deviations in the changed code path. If the fix causes a regression that appears 48 hours later under specific traffic patterns, you catch it in the verification window — not in the next incident.
8. **Evidence must be immutable and auditable.** Attach screenshots, test output, and CI links directly to the issue tracker — not via links that can rot, expired CI artifacts, or Slack threads that scroll away. Six months later, when someone asks "was this actually fixed?", the evidence should still be there. Screenshots embedded in the issue body. Test output pasted as a code block. CI run permalink.
9. **The anti-rationalization check is a mandatory phase gate.** Before closing any task, ask: "Am I making any of the classic excuses?" — "It's obviously correct," "I already tested it manually," "The CI will catch issues," "It's just a one-line change." If any excuse applies, you're rationalizing. Go back to Phase 1 and verify properly. Rationalization is the #1 cause of regressions that "should have been caught."
10. **Verification scales with blast radius.** A CSS color change verifies with a screenshot. A shared utility change verifies with the full project test suite. A database migration verifies with integration tests + rollback test + staging smoke test. Match your verification effort to the risk: ask "what's the worst thing that happens if this is wrong?" and verify against that scenario.

## Decision Trees **(QUICK)**

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


## Error Recovery **(STANDARD)**

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

Verification doesn't happen in isolation. It integrates with the broader quality and delivery pipeline.

| Skill | Relationship | Handoff Pattern |
|---|---|---|
| **qa-engineer** | Consumes test strategies and coverage reports | Before verification: "QA Engineer, what tests should I run for this change?" After verification: "QA Engineer, here's the verification evidence — does it meet the quality bar?" |
| **tdd-guide** | Consumes test-first workflow | If no reproduction test exists: "TDD Guide, help me write a failing test for this reproduction case." Then verify against that test. |
| **code-reviewer** | Consumes code review findings | After code review: "Code Reviewer flagged [N] issues. I've addressed them. Verification confirms: (1) original bug fixed, (2) reviewer concerns resolved, (3) no regressions." |
| **release-manager** | Feeds verification gates into release readiness | Before release: "Release Manager, verification for [ticket IDs] is complete. Evidence attached. All gates passed. Ready for release." |
| **incident-responder** | Feeds post-incident verification | After incident: "Incident Responder, hotfix verified: reproduction case resolved, no regressions. Post-incident verification ticket filed for [date]." |


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `code-reviewer` | Code quality assessment, security patterns, testing gaps | Before finalizing implementation or shipping to production |


## Proactive Triggers

| Trigger Pattern | Automatic Response |
|---|---|
| Commit message contains "fix" or "fixes" | Check: is there a linked issue with reproduction steps? If not, flag. |
| PR body contains "fixes #[number]" but no verification section | Add a verification checklist to the PR: "Did you: [ ] Reproduce the bug [ ] Verify the fix [ ] Run regression tests [ ] Attach evidence?" |
| Issue closed without comment | Flag for reopen. Silent closure = unverified closure. |
| Task moved to "Done" column without linked test run | Check CI for a passing test run on the relevant commit. If none, flag. |
| "Works for me" response on a bug report | Challenge: "Could not reproduce" is not the same as "fixed." Request the reporter's environment details. |
| Merge to main without associated test run | Check if the merge commit has a passing CI run. If CI was skipped, flag for post-merge verification. |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "It's obviously correct — I can see the fix is right." | The "obvious" null-guard addition changes the return type from `User` to `User \| null`. Every caller that didn't handle null now has a latent bug. Cost: **$50K+** in cascading failures from an "obviously correct" change that shipped without verification. |
| "I verified it manually — it works on my screen." | Manual verification cannot be reproduced. Three months later the same bug resurfaces, nobody remembers how to repro or what the fix was, and the team spends **$15K** in engineering time rediscovering and re-fixing it. Manual-only testing is not verification — it's hope. |
| "I'll verify in production — that's the real test anyway." | Friday deploy, "check on Monday." Over the weekend the fix causes a regression affecting 5,000 users. Monday morning, the support queue is flooded. Cost: **$75K** in support hours, emergency engineering time, and reputational damage from a weekend outage. |
| "The code review will catch any issues — that's what reviewers are for." | Reviewers catch ~60% of defects at best. They don't run the code, test edge cases, or verify against the original bug report. Code review augments verification — it does not replace it. Cost: **$25K-$50K** per incident that passed review but failed in production. |
| "This sprint is ending — just move the tickets to Done, we'll verify next sprint." | 15 issues moved to "Done" because the sprint ended, not because verification happened. Two sprints later, 8 are reopened with "Actually, this still doesn't work." Cost: **$40K** in wasted sprint capacity and a team that learns "done" means nothing. |

## Gotchas

- **The "obviously correct" change that introduces a regression**: A developer adds a null check to `getUser()`. The null check is correct, but it changes the return type from `User` to `User | null`. Every caller that didn't handle null now has a latent bug. Cost: **$50,000+** in debugging, hotfix, and customer compensation for a payment-processing outage caused by an unhandled null in the checkout flow.

- **Manual-only testing that can't be reproduced**: A bug is "fixed" and "tested manually" but no reproduction case is documented. Three months later, the same bug resurfaces. Nobody remembers how to reproduce it or what the fix was. The team spends **$15,000** in engineering time rediscovering the bug and re-fixing it.

- **Skipping the exact reproduction case**: The developer writes a test that exercises the general area of the bug but not the EXACT scenario from the report. The test passes, the issue is closed. Two weeks later, the reporter comments: "Still broken." The fix addressed a different code path. Cost: **$10,000** in rework and lost trust from the reporter.

- **False-positive verification from weak assertions**: A test checks `expect(result).toBeTruthy()` and passes. But `result` is `{}` (empty object, truthy) when it should be `{ price: 19.99 }`. The bug ships to production. Cost: **$25,000** in incorrect invoices that require manual correction and customer apologies.

- **Unverified status transitions in issue trackers**: A project manager moves 15 issues to "Done" because the sprint ended, not because verification happened. Two sprints later, 8 of those issues are reopened with "Actually, this still doesn't work." Cost: **$40,000** in wasted sprint capacity and demoralized teams discovering that "done" meant nothing.

- **Deferred verification ("I'll check later")**: A developer merges a fix on Friday, planning to verify on Monday. Over the weekend, the fix causes a regression that affects 5,000 users. Monday morning, the support queue is flooded. Cost: **$75,000** in support hours, emergency engineering time, and reputational damage from a weekend outage.

- **Verification in the wrong environment**: A fix is verified in the developer's local environment (Node 20, fresh database). In production (Node 18, 2TB database with specific data), the fix fails because of a runtime API difference. Cost: **$100,000+** in production incident response, rollback, and post-mortem process.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| The "obviously correct" one-line change that skips verification — introduces a regression from unhandled null that breaks the payment pipeline | Every change, no matter how small, follows the 5-phase verification workflow. One-line changes have caused billion-dollar outages. Verify proportionally to blast radius, never zero. |
| Manual-only testing with no documented reproduction case — 3 months later, same bug resurfaces, nobody remembers how to reproduce or fix it | Attach BEFORE/AFTER screenshots, test output, and reproduction steps to every closed issue. Evidence must survive team turnover. |
| Skipping the EXACT reproduction case — writing a test that exercises the general area but not the reporter's specific scenario | Use the reporter's EXACT steps. Same inputs, same environment, same expected output. A test that misses the exact failure path gives false confidence. |
| Weak assertions that pass for wrong output — `expect(result).toBeTruthy()` passes for `{}` when it should be `{ price: 19.99 }` | Assert specific values, types, and structures. If the assertion doesn't distinguish between correct and incorrect output, it's not verification — it's ceremony. |
| Unverified status transitions — moving issues to "Done" because the sprint ended, not because verification happened | Every status transition requires evidence. "Done" means "verified with BEFORE/AFTER evidence + passing test suite + regression check." No exceptions for sprint deadlines. |
| Deferred verification — merging on Friday, planning to verify on Monday, 5,000 users hit the regression over the weekend | Verify BEFORE merge, not after. If merge is unavoidable, schedule a verification window within 2 hours of deploy with alerting on the changed code path. |
| "It works on my machine" as verification — ignoring environment differences in Node version, database size, config values, and traffic patterns | Verify in staging with production-like data and config. The developer's machine is the least representative environment in the pipeline. |

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

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Production Checklist **(STANDARD)**

- [ ] **[VC1]** Phase 1 (Reproduce) complete: bug reproduced using the reporter's EXACT steps — evidence of failure captured BEFORE fix
- [ ] **[VC2]** Phase 2 (Apply Fix) complete: fix is minimal — changes only what's necessary, no refactoring or unrelated changes mixed in
- [ ] **[VC3]** Phase 3 (Verify Fix) complete: reproduction case now produces expected output — correct logic path confirmed, not just "test passes"
- [ ] **[VC4]** Phase 4 (Regression Check) complete: full test suite for the module passes; dependent module suites run if changed code is imported elsewhere
- [ ] **[VC5]** Phase 5 (Evidence Collection) complete: BEFORE/AFTER evidence attached to issue/PR — screenshots, test output, CI links (not rot-able URLs)
- [ ] **[VC6]** Anti-rationalization gate passed: none of the classic excuses detected — "obviously correct," "tested manually," "CI will catch," "one-line change"
- [ ] **[VC7]** Edge case testing completed: null/undefined, empty, boundary (0, -1, MAX), invalid type, concurrent, timeout — at least 3 edge cases beyond the reproduction scenario
- [ ] **[VC8]** Environment parity verified: fix tested in staging or closest production-like environment — not just local development machine
- [ ] **[VC9]** Output validation precise: actual output matches expected output character-by-character, field-by-field — not "looks about right"
- [ ] **[VC10]** Regression scope correct: dependent modules identified (`grep -r "import.*from") and their tests run — no skipped dependents
- [ ] **[VC11]** Evidence is immutable and auditable: screenshots embedded in issue body, test output pasted as code block, CI run permalink — no Slack-only or expiring links
- [ ] **[VC12]** Verification summary written: "Verified on [date] by [method] against reproduction case [link]" — included in closing comment
- [ ] **[VC13]** Post-deploy verification window defined: 24-72 hour monitoring with alerts on error rate, latency, and business metrics for the changed code path
- [ ] **[VC14]** Status transition gate passed: all 5 phases + anti-rationalization + evidence sufficiency — task transitions to DONE only after all gates pass

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| "Verified working" — marked DONE. 2 days later: "It's broken again." No evidence attached to verification | Verification was "I checked and it looked fine" — unauditable, unreproducible, and often wrong. No screenshot, no test output, no reproduction steps for the verifier to follow | Require verifiable evidence: screenshot of fixed behavior, test run output, CI pipeline permalink, or before/after metrics. Evidence is attached to the issue BEFORE status transitions to DONE. Gate check: "Would someone else reach the same conclusion from this evidence?" | "Looks good to me" is not verification — it's optimism with a status transition. Evidence survives memory, team changes, and the 72 hours between "verified" and "wait, it's broken again?" |
| Task marked "DONE" but deployment pipeline failed 3 hours earlier and nobody noticed | Verification step was "code merged" — assumed CI/CD would handle the rest. CI deployment was red due to infrastructure change. The ticket was closed while the feature wasn't actually in production | Verification checklist includes: (1) Code merged ✓, (2) CI passed ✓, (3) Deployed to production ✓, (4) Production smoke test passed ✓, (5) Monitoring dashboard shows expected behavior for 15+ minutes ✓. DONE status only after all 5 gates | "Merged" is not "deployed." "Deployed" is not "working." Each gate is a separate truth claim. Closing a ticket at "merged" means you've verified the merge, not the feature. |
| Production breaks 45 minutes after deploy. Rollback takes 30 minutes because "rollback" wasn't in the verification plan | Verification plan tested the feature, not the failure modes. "If this deploy goes wrong, how do we undo it?" was never asked. Rollback wasn't tested — it had bit-rotted | Every verification plan includes a rollback verification: (1) Run rollback procedure in staging, (2) Verify rollback completes in <5 minutes, (3) Verify system returns to pre-deploy metrics after rollback. Production deploy: rollback is the FIRST response, not the last resort | The time to test rollback is before you need it. A rollback procedure you haven't tested is a wish, not a plan. Verify rollback works, then deploy — and you'll deploy with confidence instead of fear. |
| 3-part migration: code change + DB migration + config change. Verification only checked step 1. Steps 2 and 3 weren't done | Multi-step change treated as a single atomic task. "Code is deployed" was enough to check DONE. Database migration was supposed to run in the next maintenance window — it was forgotten | Each independent step gets its own verification gate. Gate 1: code deployed + smoke tested ✓. Gate 2: migration ran + data integrity verified ✓. Gate 3: config pushed + feature flag toggled + monitored ✓. No gate can close until its predecessor is verified | Multi-step changes are not one task with many steps — they're many tasks pretending to be one. If step 2 requires a maintenance window next Tuesday, the ticket stays OPEN until next Tuesday. Partial verification is not verification. |
| Performance fix: "added index, query went from 2s to 50ms — DONE." Index wasn't used in production — query plan differed between dev and prod | Dev database has 10K rows. Production has 5M. PostgreSQL query planner uses different strategy at 10K vs 5M. The index reduced dev query time but production still table-scans | Verification at production scale: run `EXPLAIN ANALYZE` on production-sized data (anonymized copy or staging). Verify index is actually used: `EXPLAIN` output shows `Index Scan` not `Seq Scan`. Production verification: check slow query log 24 hours after deploy | The same query does not mean the same execution plan. The database planner optimizes for the data volume it sees. Dev-scale verification proves the query works at dev scale. Production-scale verification proves the query works at production scale. |
| "Edge case verified" — but the edge case was `user = null`. Actual edge case that broke production: `user` is a valid object but `user.preferences` is `undefined` | Verification tested the top-level null case but not the nested property access case. The null check `if (!user)` passed. The crash was `user.preferences.theme.toLowerCase()` where `user.preferences` existed but was `undefined` | Edge case checklist: null/undefined at every level, not just the top. Test: empty object `{}`, object with missing nested property, array with 0 elements, array with max elements, string with special characters, number at INT_MAX. Don't stop at the first null check | Null checking the root object is table stakes. The bugs live two levels deep in partially populated objects. Your edge case checklist should walk the entire property tree — every `?.` in your code is a question you need to ask and verify. |

## References

1. [Reproduction Verification Guide](references/reproduction-verification.md) — How to run and document the exact reproduction case from a bug report.
2. [Assertion Checklist](references/assertion-checklist.md) — Criteria for strong vs. weak assertions; ensures tests actually verify correct behavior.
3. [Regression Detection](references/regression-detection.md) — Strategies for scoping and executing regression test suites after a fix.
4. [Evidence Documentation](references/evidence-documentation.md) — Standards for what constitutes verifiable, auditable evidence of a fix.
5. [Anti-Rationalization Table](references/anti-rationalization-table.md) — Complete catalog of cognitive biases that lead to false completion with counter-strategies.
6. [Verification Gates](references/verification-gates.md) — Gate definitions, pass/fail criteria, and enforcement mechanisms for each verification phase.
7. [False Completion Patterns](references/false-completion-patterns.md) — Recurring patterns where tasks are marked done without actual verification.
8. [Status Transition Rules](references/status-transition-rules.md) — Rules governing when an issue or task can transition from "in progress" to "done" or "closed."
