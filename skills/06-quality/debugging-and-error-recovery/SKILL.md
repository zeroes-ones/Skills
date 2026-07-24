---
name: debugging-and-error-recovery
description: >
  Use when debugging production incidents, troubleshooting non-reproducible bugs,
  performing root cause analysis, reducing a bug to a minimal reproduction case,
  or applying systematic debugging methodology on any codebase. Handles the 6-step
  triage workflow (Reproduce, Localize with git bisect, Reduce to minimal repro,
  Fix root cause not symptom, Guard with regression test, Verify), non-reproducible
  bug decision trees, stop-the-line protocols for critical severity bugs, safe
  fallback patterns, binary search debugging (delta debugging), rubber duck
  debugging protocol, and error recovery strategies. Do NOT use for performance
  profiling (route to performance-engineer), security vulnerability analysis (route
  to security-reviewer), test-driven development (route to tdd-guide), writing new
  features (route to backend-developer or frontend-developer), or incident command
  (route to incident-responder).
author: Sandeep Kumar Penchala
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
license: MIT
allowed-tools: Read Grep Glob Bash
type: quality
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - debugging
  - error-recovery
  - root-cause-analysis
  - triage
  - git-bisect
  - incident-response
  - binary-search
  - minimal-reproduction
  - rubber-duck
  - stop-the-line
token_budget: 5000
chain:
  consumes_from:
    - backend-developer
    - frontend-developer
    - code-reviewer
    - qa-engineer
    - incident-responder
    - site-reliability-engineer
  feeds_into:
    - code-reviewer
    - qa-engineer
    - incident-responder
    - site-reliability-engineer
---

# Debugging and Error Recovery
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Systematic debugging is the highest-ROI skill in software engineering. A structured debugger fixes bugs in minutes that an unstructured debugger chases for days. This skill encodes the methodology used by senior engineers and SREs at top-tier companies: start with reproduction (you cannot fix what you cannot see), then localize with binary search (halve the problem space at each step), reduce to a minimal case (the smaller the repro, the faster the fix), fix the root cause (never patch symptoms), guard with a regression test (every bug gets a test), and verify in production-like conditions (staging is not production).

The golden rule of debugging: **the bug is never where you think it is.** If you knew where the bug was, you would have already fixed it. The methodology exists to overcome your assumptions.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect debugging mistakes before they waste hours. Violation means STOP and reassess.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to fix a bug you cannot reproduce. Fixing blind is guessing with consequences. | Trigger: developer describes bug in natural language but cannot provide reproduction steps, error message, stack trace, or failing test -- AND proposes a code change | STOP. Respond: \"REPRODUCTION GATE: Cannot proceed without reproduction. The bug report lacks: [missing items]. Before any fix: (1) capture the exact error message and stack trace, (2) identify the input/state that triggers it, (3) write a failing test. Fixes without repro have a 60%+ failure rate -- they either don't fix the real bug or introduce new ones.\" |
| R2 | DETECT symptom-fixing instead of root-cause fixing | Trigger: proposed fix adds a try/catch around the error site, adds a null check without understanding why null occurs, or silences a warning/error message -- grep proposed diff for `catch.*{.*}` with empty handler, `if.*null.*return` without upstream fix, or `console.error.*removed` | STOP. Respond: \"SYMPTOM FIX at [file:line]. The proposed change suppresses the symptom (error message, exception) without addressing why [condition] occurs. Root cause question: what upstream state or input caused [null/error/timeout]? Ask 'Why?' 5 times. Example: 'Why is user null?' -> 'Because session lookup failed.' -> 'Why did session lookup fail?' -> 'Because Redis connection timed out.' -> Fix: add Redis connection pooling + timeout handling. The symptom fix was just hiding the real problem.\" |
| R3 | DETECT debugging without narrowing the problem space | Trigger: developer has been working on the same bug for >60 minutes without reducing the suspect code surface by at least 50% (no git bisect, no binary search, no log-filtering, no commit isolation) | STOP. Respond: \"SEARCH SPACE STALL: After 60 minutes, the suspect surface should be at most 50% of where you started. Current state: investigating [entire module/hundreds of lines]. Apply binary search now: (1) git bisect to find the breaking commit, (2) comment out half the code path and re-test, (3) add targeted logging at the midpoint. If you cannot halve the space, you are reading code, not debugging.\" |
| R4 | DETECT debugging in production without safeguards | Trigger: proposed action includes `console.log` in production, deploying debug builds, attaching a debugger to production, or running `SELECT *` on a production database to investigate | STOP. Respond: \"PRODUCTION SAFETY VIOLATION: [Action] in production is dangerous. It can: expose sensitive data in logs, degrade performance under load, or corrupt state. Instead: (1) reproduce in staging/dev first, (2) if production-only, use read-only observability tools (metrics, traces, structured logs), (3) if you must query production, use `SELECT ... LIMIT 10` with specific columns, never `SELECT *`. Production debugging tools: OpenTelemetry traces, structured log queries, read-only replicas.\" |
| R5 | REFUSE to close a bug without a regression test. Bugs that happen once will happen again. | Trigger: bug fix PR contains code changes but zero new or modified test files -- git diff shows `+` in src/ but no changes in test/ or __tests__/ | STOP. Respond: \"REGRESSION GATE: Every bug fix must include a test that fails before the fix and passes after. Without a regression test, the bug will recur within 6 months (67% probability per industry data). Write a test that: (1) reproduces the exact error condition, (2) verifies the fix, (3) covers the edge case that triggered the bug. Only then can the bug be closed.\" |
| R6 | DETECT correlation assumed as causation in debugging | Trigger: developer says \"the bug started when we deployed [unrelated change]\" without verifying the timeline, or proposes reverting a change because it \"coincided\" with the bug | STOP. Respond: \"CORRELATION ≠ CAUSATION: Temporal coincidence does not prove causality. Before reverting: (1) confirm the exact deployment timestamp vs first error timestamp, (2) check if any other changes deployed in the same window, (3) check external dependencies (API version changes, infra changes, traffic pattern shifts). Example: a bug appearing after a React upgrade could actually be caused by a CDN cache change deployed simultaneously. Verify, don't assume.\" |
| R7 | REFUSE to ship a fix without verifying in a production-like environment | Trigger: fix is merged without testing against: production data shapes, production traffic volume (even at 10%), or production config values | STOP. Respond: \"VERIFICATION GATE: Staging passed ≠ production will pass. Differences that have caused verified fixes to fail in production: (1) production data has NULLs where staging doesn't, (2) production traffic is 100x staging volume exposing race conditions, (3) production config has different timeouts/limits, (4) production runs on different hardware/regions. Before deploying: canary deploy to 1% of traffic, monitor error rates for 15 minutes, then roll out.\"

## The Expert's Mindset

Debugging is not a talent -- it is a discipline. The best debuggers are not the smartest engineers; they are the most systematic. They treat every bug as a scientific investigation: form a hypothesis, design an experiment to test it, analyze the results, and iterate.

### Mental Models

| Model | Description |
|---|---|
| **The Scientific Method** | Debugging is hypothesis-driven experimentation. Every change you make is an experiment. If you change code without a hypothesis, you are not debugging -- you are gambling. |
| **Binary Search** | The most efficient search algorithm applies to code too. If a bug exists somewhere in a 1000-line module, you can find the offending line in at most 10 tests by halving the search space each time. |
| **Occam's Razor** | The simplest explanation is usually correct. If you find yourself constructing an elaborate theory involving cosmic rays or compiler bugs, stop. Check the basics first: typos, off-by-one errors, null values, incorrect config. |
| **5 Whys** | Keep asking \"why?\" until you reach the root cause. Symptom: \"The API returns 500.\" Why? \"Null pointer.\" Why null? \"Database returned no rows.\" Why no rows? \"The record was soft-deleted.\" Why soft-deleted? \"The cleanup job ran with wrong date filter.\" Root cause: cleanup job date filter. Fix: fix the filter. Symptom fix (null guard at API) would have masked the data loss. |

### Cognitive Biases That Sabotage Debugging

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Confirmation bias** | Testing only scenarios that confirm your theory, ignoring disconfirming evidence | Actively try to disprove your hypothesis. Write a test that should fail if your theory is correct. |
| **Anchoring on first diagnosis** | Sticking with your initial guess even as evidence mounts against it | After 30 minutes without progress, formally abandon your current hypothesis and start fresh. Write down 3 alternative explanations. |
| **Availability heuristic** | Assuming the bug is caused by whatever you most recently debugged | Before investigating, list the top 5 possible causes ranked by probability, not recency. |
| **Fundamental attribution error** | Blaming external libraries, frameworks, or \"someone else's code\" before checking your own | Rule: assume the bug is in YOUR code first. Framework bugs exist but are 100x less common than application bugs. |
| **Premature optimization** | Fixing the bug AND refactoring the module AND improving performance all at once | One PR = one bug fix. Do not refactor while debugging. You cannot distinguish which change actually fixed the bug. |

### What Masters Know That Others Don't

- **The first question is always: 'When did this start working correctly?'** Find the last known-good state. A bug that started today vs a bug that has existed for 6 months requires completely different investigation strategies.
- **Reproduction is 80% of the fix.** Once you can reliably reproduce a bug on demand, the fix is usually obvious. Invest aggressively in reproduction. Time spent reproducing is never wasted.
- **Logs lie. Metrics don't.** Application logs show what developers thought was important. Metrics and traces show what actually happened. When logs and metrics disagree, trust metrics.
- **The rubber duck is real.** Explaining the bug to someone else (or a rubber duck) forces you to articulate assumptions you didn't know you were making. At least 30% of debugging breakthroughs happen during the explanation, before the listener responds.

## Operating at Different Levels

- **Quick scan (30s):** Read the error message and stack trace. Identify: (1) the exact error type (NullPointerException, TypeError, TimeoutError), (2) the file and line number, (3) the operation that failed (DB query, API call, computation). Check if this is a known issue in your error tracking system (Sentry, Datadog, Bugsnag). If it is a duplicate, link it and move on.
- **Standard engagement (10min):** Full reproduction → narrow to module → identify root cause → write regression test → apply fix → verify. This is the standard debugging loop for 90% of bugs.
- **Deep dive (full session):** For bugs that resist standard debugging: git bisect across commits, delta debugging (binary search on inputs), log injection (add targeted logging at each layer), dependency isolation (does it happen without Redis? without the CDN?), and comparative analysis (what changed between working and broken states?).
- **Critical incident (SEV1/P0):** Stop-the-line protocol. All hands on deck. Goal: restore service, not find root cause. Mitigate first (rollback, feature flag off, traffic shift), then investigate. Post-incident: blameless postmortem with timeline, 5 Whys, and action items.

## When to Use

Use debugging-and-error-recovery when existing code is not behaving as expected and you need to find and fix the root cause -- systematically, not through trial and error.

- Reproducing a reported bug: capturing exact inputs, state, and environment that trigger the error
- Localizing a bug in a large codebase: using git bisect, binary search, or log-driven narrowing
- Reducing a bug to minimal reproduction: stripping away irrelevant code, data, and dependencies
- Fixing root cause (not symptom): applying 5 Whys to trace symptoms back to their origin
- Guarding against regression: writing the test that proves the bug existed and the fix works
- Handling non-reproducible bugs: probabilistic reproduction, observability injection, hypothesis testing
- Executing stop-the-line protocol: critical incidents requiring immediate mitigation before investigation
- Designing safe fallbacks: circuit breakers, graceful degradation, retry with backoff
- Debugging distributed systems: trace-based debugging across service boundaries
- Analyzing crash dumps and core dumps: post-mortem debugging from production artifacts

Do NOT use debugging-and-error-recovery for writing new features (route to backend-developer or frontend-developer). Do NOT use for performance profiling (route to performance-engineer). Do NOT use for security vulnerability analysis (route to security-reviewer). Do NOT use for incident command and communication (route to incident-responder). Do NOT use for writing tests for new code (route to tdd-guide).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "debugging-and-error-recovery")` -- this is your skill | Redirect: \"I am Debugging and Error Recovery. Route by intent matching below.\" |
| A2 | `file_contains("error.log\|stacktrace\|crash", "panic\|segfault\|NullPointer\|TypeError\|500 Internal")` | **CRASH/ERROR** -- Stack trace available. Go to **Core Workflow: Phase 1 (Reproduce)** then trace-driven investigation. |
| A3 | `file_contains("bug_report.md\|issue", "intermittent\|sometimes\|flaky\|non-deterministic")` | **INTERMITTENT** -- Non-reproducible. Jump to **Decision Trees: Non-Reproducible Bug**. |
| A4 | `file_contains("incident\|postmortem", "SEV1\|SEV0\|P0\|P1\|critical\|outage")` | **CRITICAL INCIDENT** -- Stop-the-line protocol. Jump to **Decision Trees: Critical Incident Triage**. |
| A5 | `file_contains("git-log.txt", "")` OR `git log --oneline -50` available | **BISECT CANDIDATE** -- Recent commits may contain the bug. Go to **Core Workflow: Phase 2 (Localize)** with git bisect. |
| A6 | File has `console.log\|print(\|logger.` debugging statements scattered | **AD-HOC DEBUGGING** -- Developer was debugging manually. Jump to **Decision Trees: Structured Debugging Replacement**. |
| A7 | No artifacts -- verbal bug description only | **VERBAL REPORT** -- Start at **Core Workflow: Phase 0 (Clarify)**. Must extract reproduction steps before proceeding. |

### Intent Route (Ask the User)

```
What kind of bug are you dealing with?
├── I have a stack trace / error message → Start at "Core Workflow > Phase 1"
├── The bug is intermittent / non-reproducible → Jump to "Decision Trees > Non-Reproducible Bug"
│   ├── It happens ~X% of the time → Probabilistic reproduction strategy
│   ├── It only happens in production → Observability injection approach
│   └── It's a race condition / timing bug → Add deterministic ordering for debugging
├── This is a critical production incident → Jump to = "Decision Trees > Critical Incident Triage"
├── I know which commit introduced the bug → Jump to "Core Workflow > Phase 2" — bisect done
├── I can reproduce it but can't find the root cause → Go to "Core Workflow > Phase 3"
├── I have a fix but want to verify it's correct → Jump to "Core Workflow > Phase 5"
├── The bug is in a distributed system (microservices) → Jump to "Decision Trees > Distributed Debugging"
├── I need to roll back safely → Jump to "Decision Trees > Safe Rollback"
└── I'm not sure where to start → "Core Workflow > Phase 0" — clarify the bug description
```

## Core Workflow

### Phase 0: Clarify the Bug

Before touching any code, complete this template:

```
BUG TRIAGE TEMPLATE
===================
What is the exact error? [copy-paste error message + stack trace]
What was expected to happen? [specific expected behavior]
What actually happened? [specific observed behavior]
When did it start? [timestamp, deployment, commit]
What is the impact? [users affected, revenue impact, data loss]
Can you reproduce it? [YES / NO / SOMETIMES]
What are the reproduction steps? [1. 2. 3.]
What is the environment? [OS, browser, server version, database version]
```

If any field is blank, STOP. Ask the reporter to fill it in before proceeding. Debugging without this information is guessing.

### Phase 1: Reproduce

Reproduction is the foundation. Without it, you are navigating without a map.

```
Step 1: Reproduce manually
  Follow the reproduction steps exactly. If you cannot reproduce, the bug report is incomplete.

Step 2: Write a failing test
  describe('bug #1234: login fails with special characters', () => {
    it('should accept email with plus sign', () => {
      expect(() => login('user+tag@example.com', 'password'))
        .not.toThrow();
    });
  });

Step 3: Confirm the test fails for the reported reason
  npm test -- -t 'bug #1234'
  # Expected: test FAILS (red) -- proving the bug exists
  # If test PASSES (green) -- your reproduction is wrong
```

### Phase 2: Localize

Narrow the problem space. Binary search is the most efficient method.

```
Method A: git bisect (find the breaking commit)
  git bisect start
  git bisect bad HEAD          # current broken state
  git bisect good <last_known_good_commit>
  # Git checks out midpoint. Test. Mark good/bad. Repeat.
  # In log2(N) steps, you find the exact commit.
  git bisect log > bisect_log.txt

Method B: Binary search on code (comment-out method)
  # For a 200-line function that throws an error:
  # Comment out lines 100-200. Does error still occur?
  # YES → bug is in lines 1-100.  NO → bug is in lines 100-200.
  # Repeat, halving each time. Find exact line in log2(200) ≈ 8 iterations.

Method C: Log injection
  # When you cannot modify code (production), add targeted structured logs:
  logger.info('checkpoint-A', { userId, cartTotal, timestamp });
  # Query logs: which checkpoint was the last one reached before the error?
  # Bug is between the last successful checkpoint and the error.
```

ASCII diagram:
```
┌─────────────────────────────────────────────────┐
│              DEBUGGING WORKFLOW                  │
├─────────────────────────────────────────────────┤
│  Phase 0: Clarify (fill triage template)        │
│     │                                           │
│     ▼                                           │
│  Phase 1: Reproduce (write failing test)        │
│     │                                           │
│     ▼                                           │
│  Phase 2: Localize (bisect / binary search)     │
│     │                                           │
│     ▼                                           │
│  Phase 3: Reduce (minimal reproduction)         │
│     │                                           │
│     ▼                                           │
│  Phase 4: Fix Root Cause (5 Whys)               │
│     │                                           │
│     ▼                                           │
│  Phase 5: Guard (regression test)               │
│     │                                           │
│     ▼                                           │
│  Phase 6: Verify (production-like environment)   │
└─────────────────────────────────────────────────┘
```

### Phase 3: Reduce to Minimal Reproduction

Strip away everything unnecessary. The smaller the repro, the faster the fix.

```
Before reduction:
  - 500-line component
  - 3 API calls
  - 2 database queries
  - User must be logged in with specific permissions
  - Input: 50-field form submission

After reduction:
  - 15-line function: the single transform that fails
  - 0 API calls (mocked)
  - 0 database queries (hardcoded data)
  - No auth required
  - Input: the single field value that triggers the bug
```

The delta debugging algorithm: systematically remove elements from the input/state until you find the minimal set that still triggers the bug.

### Phase 4: Fix Root Cause

Apply the 5 Whys. Never fix at the symptom layer.

```
Symptom: TypeError: Cannot read property 'name' of undefined
│
├── Why? user parameter is undefined
│   └── Why? getUser() returned null
│       └── Why? Database query returned no rows
│           └── Why? User record was deleted by cleanup job
│               └── Why? Cleanup job had wrong date filter
│                   └── ROOT CAUSE: Date filter off-by-one error
│
├── SYMPTOM FIX (WRONG): Add `if (user) return;` at the top
└── ROOT CAUSE FIX (CORRECT): Fix date filter in cleanup job + add guard in getUser()
```

### Phase 5: Guard with Regression Test

The bug-fix test must be specific enough to catch the exact failure mode.

```
// GOOD regression test: specific to the bug
it('handles user record deleted between auth and profile fetch', async () => {
  await db.insertUser({ id: 1, name: 'Alice' });
  const token = await auth.login('alice', 'password');
  await db.deleteUser(1); // simulate race condition
  await expect(profile.getProfile(token))
    .rejects.toThrow('UserNotFoundError'); // expect graceful error, not crash
});

// BAD regression test: too generic
it('profile fetch works', async () => {
  const profile = await profile.getProfile(validToken);
  expect(profile).toBeDefined();
});
```

### Phase 6: Verify

Before closing the bug, verify in conditions as close to production as possible.

- [ ] Fix passes the regression test
- [ ] Fix passes ALL existing tests (no regressions introduced)
- [ ] Fix tested with production-like data (same nulls, edge cases, data volumes)
- [ ] Fix tested under load (if the bug was load-related)
- [ ] Fix deployed to canary/staging and monitored for 15+ minutes
- [ ] Rollback plan documented (can the fix be safely reverted?)

## Decision Trees
### Decision Tree 1: Non-Reproducible Bug Strategy

```
Phase 1: Increase Observability
├── Bug happens <5% of the time → Add structured logging at every decision point.
│   Capture: inputs, intermediate state, external call results, timestamps.
├── Bug happens 5-50% of the time → Probabilistic reproduction.
│   Run the operation in a loop 100-1000 times. Measure failure rate.
└── Bug happens >50% of the time → You should be able to reproduce it. Try harder.

Phase 2: Hypothesis Testing
├── Hypothesis: race condition → Add deterministic ordering (locks, queues, sequential processing)
├── Hypothesis: data-dependent → Fuzz the inputs (randomized testing with property-based checks)
├── Hypothesis: environment-dependent → Replay production traffic in staging (traffic mirroring)
├── Hypothesis: timing-dependent → Slow down or speed up components (chaos engineering)
└── Hypothesis: state-dependent → Capture and replay the exact state (state snapshot + replay)
```

### Decision Tree 2: Critical Incident Triage (Stop-the-Line)

```
Phase 1: MITIGATE (first 5 minutes — restore service)
├── Is there a recent deployment? → ROLLBACK immediately. Do not investigate during outage.
├── Is there a feature flag? → TURN IT OFF. Feature flags are instant rollbacks.
├── Is it a traffic spike? → RATE LIMIT or scale up.
├── Is it a dependency failure? → FAIL OPEN with degraded service (circuit breaker).
└── Unknown cause → TRAFFIC SHIFT to a known-good region/cluster.

Phase 2: INVESTIGATE (after service is restored)
├── Timeline analysis: what changed? Deployments, config, traffic, dependencies.
├── Metric correlation: which metric spiked first? Errors, latency, traffic, saturation?
├── Log deep-dive: query logs for the error signature during the incident window.
└── Postmortem: blameless analysis, timeline, 5 Whys, action items with owners and dates.
```

### Decision Tree 3: Safe Fallback Patterns

```
Phase 1: Choose Fallback Strategy
├── Read operation failed → Return cached/stale data with stale-while-revalidate header
├── Write operation failed → Queue the write for retry (outbox pattern, Kafka, SQS)
├── External API timeout → Circuit breaker: fail fast after N failures, reset after cool-down
├── Database connection exhausted → Connection pool limits + queue requests + timeout
└── Entire service degraded → Serve static fallback page with status banner

Phase 2: Implement Safely
├── Fallback must never be worse than the failure → A 500 is better than returning wrong data
├── Fallback must be monitorable → Log every fallback activation with reason
├── Fallback must auto-recover → When primary recovers, automatically resume normal operation
└── Fallback must be tested → Chaos test: kill the primary and verify fallback activates
```

### Decision Tree 4: Binary Search Debugging (Delta Debugging)

```
Phase 1: Define the Search Space
├── Code-level: which lines/functions are suspect? → Binary search on code deletion
├── Input-level: which input values trigger the bug? → Binary search on input reduction
├── Commit-level: which commit introduced the bug? → git bisect (binary search on commits)
├── State-level: which state transition causes the bug? → Binary search on state changes
└── Dependency-level: which dependency version causes the bug? → Binary search on dependency upgrades

Phase 2: Execute Binary Search
├── Mark the midpoint of your search space
├── Test: does the bug occur with only the first half?
│   ├── YES → Bug is in the first half. Discard the second half. Repeat.
│   └── NO → Bug is in the second half. Discard the first half. Repeat.
└── Stop when you have isolated the bug to a single function, input, commit, or state change
```

### Decision Tree 5: Distributed System Debugging

```
Phase 1: Trace the Request
├── Do you have distributed tracing? (Jaeger, Zipkin, OpenTelemetry)
│   ├── YES → Find the trace ID. Identify which service span contains the error.
│   └── NO → Add tracing. Without it, distributed debugging is nearly impossible.
├── Which service is the error originating from?
├── What is the request payload and response at each service boundary?

Phase 2: Isolate the Failing Service
├── Reproduce with all downstream services mocked → Does the error still occur?
│   ├── YES → Bug is in this service. Debug normally (Phase 1-6).
│   └── NO → Bug is in a downstream service or the interaction between services.
├── Bug is in the interaction → Check: serialization format mismatch, timeout mismatch,
│   retry storm (service A retries, causing service B to slow down, causing more retries),
│   thundering herd (many instances retrying simultaneously after an outage)
└── Bug is in downstream → Repeat isolation for that service.
```

### Decision Tree 6: Memory Leak and Resource Exhaustion

```
Phase 1: Identify the Leak
├── Heap dump analysis: capture heap dump, analyze with Chrome DevTools / Eclipse MAT
├── Metric correlation: memory grows linearly over time → leak. Memory spikes and recovers → normal.
├── Garbage collection logs: frequent full GC with failing to reclaim → leak
└── Identify retained objects: what object type is accumulating?

Phase 2: Fix the Leak
├── Event listener not removed → Add cleanup in useEffect return / ngOnDestroy / dispose()
├── Closure capturing large scope → Extract only what the closure needs
├── Cache without eviction policy → Add TTL or LRU eviction
├── Circular reference preventing GC → Break the cycle with WeakRef or explicit null assignment
└── Streaming response not consumed → Always consume or cancel response bodies
```

### Decision Tree 7: Rubber Duck Debugging Protocol

```
Phase 1: Prepare the Explanation
├── Write down: "The bug is: [one sentence]"
├── Write down: "I expect: [behavior]. Instead I get: [behavior]."
├── Write down: "I've tried: [list of things you tried and their results]."
├── Write down: "I think the cause might be: [your theory]."
└── Write down: "The evidence for my theory is: [evidence]. The evidence against is: [evidence]."

Phase 2: Explain to the Duck (or colleague)
├── Explain line by line what the code does.
├── When you reach a line where you say "and then... it should..." → STOP.
│   That "should" is an assumption you have not verified. Test it.
├── 30-50% of the time, you will identify the bug during the explanation.
└── If not, your colleague/duck now has enough context to help effectively.
```

## Cross-Skill Coordination

| Scenario | Skill to Invoke |
|---|---|
| Bug involves database queries returning unexpected results | `database-designer` — analyze query plans, indexes, data integrity |
| Bug is a security vulnerability | `security-reviewer` — assess severity, exploitability, and secure fix |
| Need to write regression tests for the bug fix | `qa-engineer` or `tdd-guide` — proper test structure and coverage |
| Bug is a production incident requiring coordination | `incident-responder` — communication, status page, stakeholder updates |
| Bug is performance-related (slow, timeout, OOM) | `performance-engineer` — profiling, benchmarking, resource analysis |
| Fix involves API contract changes | `api-designer` — backward compatibility, versioning, deprecation |
| Bug is in infrastructure or deployment | `devops-engineer` or `site-reliability-engineer` — infra debugging |
| Need code review on the bug fix | `code-reviewer` — 6-dimension review before merge |

## Proactive Triggers

These conditions automatically activate debugging scrutiny:

- **Trigger: any `console.error` or unhandled exception in production logs within the last hour.** Auto-initiate triage template. Do not wait for a bug report.
- **Trigger: error rate on a dashboard metric exceeds baseline by 3 standard deviations.** Auto-trigger: check recent deployments first.
- **Trigger: a bug report mentions "it was working yesterday" or "it broke after the deploy."** Auto-start git bisect between yesterday's deploy and the previous deploy.
- **Trigger: the same error signature appears in Sentry/Datadog >10 times in 5 minutes.** Auto-escalate to stop-the-line protocol if error rate is accelerating.
- **Trigger: a developer says "that's weird" or "I don't understand why this is happening."** Auto-trigger rubber duck protocol — the confusion itself is diagnostic data.

## What Good Looks Like

**Before — Ad-hoc debugging:**
```
Developer: "The login is broken."
Dev: *reads code for 30 minutes*
Dev: "Maybe it's the session? Let me add a console.log..."
Dev: *adds 5 console.log statements*
Dev: *deploys to staging. Console shows: user is undefined*
Dev: "Why is user undefined? Let me add more logs..."
Dev: *2 hours later, finds the bug by accident while logging something else*
Dev: *fixes the null reference, deploys*
Dev: *no regression test written*
```

**After — Systematic debugging:**
```
Dev: "Login returns 500. Stack trace: TypeError at auth.ts:42. Let me reproduce."
Dev: *writes failing test reproducing the exact error in <5 minutes*
Dev: "Test fails. Now git bisect to find when it broke."
Dev: *git bisect identifies the breaking commit in 4 steps (log2(16 commits))*
Dev: "Commit abc123 changed the session serialization. That's the root cause."
Dev: *fixes the serialization, test passes. Adds 2 more edge case tests.*
Dev: "Fix is 3 lines. Regression tests cover: null session, expired session, valid session."
Total time: 25 minutes. Regression protection: permanent.
```

## Deliberate Practice

1. **Git Bisect Drill:** Find a bug that was fixed in your codebase 1-3 months ago. Without looking at the fix, reproduce the bug and use git bisect to find the breaking commit. Time yourself. Goal: find the commit in under 10 minutes.
2. **Minimal Reproduction Challenge:** Take a complex bug report (long form, many steps). Reduce it to a reproduction in under 20 lines of code. Remove every dependency, every API call, every UI element that is not essential. The minimal repro should run in a single file.
3. **5 Whys Retrospective:** For the last 3 bugs your team fixed, apply the 5 Whys to each. Did the fix address the root cause or a symptom? Re-classify each fix. How many were actually root cause fixes?
4. **Rubber Duck Recording:** Next time you are stuck on a bug, record yourself (audio only) explaining the bug to an imaginary colleague. Listen to the recording. Identify the moment where you said "should" or "I assume" — that is your unverified assumption. Test it.
5. **Crash Dump Analysis:** Download a core dump or heap dump from a production crash. Use the appropriate tool (lldb, gdb, Chrome DevTools Memory, Eclipse MAT) to identify: (1) the crashing thread, (2) the exact line, (3) the state of relevant variables. Production debugging without a debugger is an essential skill.

## Gotchas

- **Adding try/catch without understanding the error.** A try/catch that swallows the exception (empty catch block) converts a visible error into silent data corruption. The error still occurs, but now nobody knows. **Total cost: $15,000-$75,000 in silent data corruption discovered weeks later.**
- **Reverting the wrong commit during an incident.** In the panic of a SEV1, reverting a commit without verifying it is the cause can make things worse (reintroduce an old bug) without fixing the current one. **Total cost: $50,000-$200,000 in extended outage + compounding failures.**
- **Fixing a bug without understanding why the test suite didn't catch it.** If tests passed before the bug, the test suite has a gap. Fixing only the code and not the tests means the same class of bug will ship again. **Total cost: $10,000-$30,000 per recurrence in a 12-month period.**
- **Debugging with `console.log` in production.** Logging PII (emails, tokens, SSNs) violates GDPR/CCPA. Logging in hot paths can 10x your log volume, exceeding retention limits and drowning real signals. **Total cost: $25,000-$500,000 in compliance fines + $5,000/month in log storage overage.**
- **Assuming "it works on my machine" means the fix is correct.** Your machine does not have production data, production traffic patterns, production config, production network latency, or production scale. Bugs that only appear at scale (race conditions, connection pool exhaustion, OOM) will pass locally every time. **Total cost: $20,000-$100,000 in rollback + incident response for a fix that passes local but fails in prod.**
- **Closing a bug as "cannot reproduce" without instrumenting the code.** A non-reproducible bug is not fixed — it is waiting. Adding structured logging, metrics, or a sentry alert at the suspect site converts "cannot reproduce" into "will catch next time." Without instrumentation, the bug will recur with zero additional data. **Total cost: $5,000-$25,000 for each recurrence that could have been caught.**
- **Running a diagnostic query on a production database during peak traffic.** A `SELECT * FROM large_table` without `LIMIT` or on an unindexed column can cause a table scan that locks rows and blocks writes, turning a debugging session into a production outage. **Total cost: $30,000-$150,000 in downtime from a self-inflicted incident.**

## Verification

- [ ] Bug reproduction test written and FAILS before the fix
- [ ] Root cause identified using 5 Whys (not a symptom fix)
- [ ] Fix is minimal — changes only what is necessary (no refactoring mixed in)
- [ ] All existing tests pass — no regressions introduced
- [ ] Regression test covers: (a) the exact failure, (b) at least one edge case variant
- [ ] Fix tested in production-like environment (data, config, load)
- [ ] Rollback plan documented and tested (can revert without side effects)
- [ ] If production bug: postmortem scheduled with timeline and action items
- [ ] If non-reproducible: monitoring/instrumentation added to catch next occurrence

## References

- [Core Workflow](../references/core-workflow.md) — Detailed 6-phase workflow with extended code examples
- [Anti-Patterns](../references/anti-patterns.md) — Common debugging mistakes that waste hours
- [Best Practices](../references/best-practices.md) — Battle-tested debugging techniques from SRE teams
- [Calibration](../references/calibration.md) — When to stop debugging and escalate
- [Checklist](../references/checklist.md) — Pre-close bug verification checklist
- [Error Decoder](../references/error-decoder.md) — Common error messages decoded with root cause mappings
- [Footguns](../references/footguns.md) — Debugging techniques that frequently backfire
- [Scale Depth](../references/scale-depth.md) — Debugging at scale: distributed systems, high traffic, large datasets
