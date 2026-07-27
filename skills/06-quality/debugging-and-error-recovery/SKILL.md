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
<!-- QUICK: 30s -->

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

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
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

Debugging is not a talent -- it is a discipline. The best debuggers are not the smartest engineers; they are the most systematic. They treat every bug as a scientific investigation: form a hypothesis, design an experiment to test it, analyze the results, and iterate.


## Mental Models
<!-- STANDARD: 3min -->

| Model | Description |
|---|---|
| **The Scientific Method** | Debugging is hypothesis-driven experimentation. Every change you make is an experiment. If you change code without a hypothesis, you are not debugging -- you are gambling. |
| **Binary Search** | The most efficient search algorithm applies to code too. If a bug exists somewhere in a 1000-line module, you can find the offending line in at most 10 tests by halving the search space each time. |
| **Occam's Razor** | The simplest explanation is usually correct. If you find yourself constructing an elaborate theory involving cosmic rays or compiler bugs, stop. Check the basics first: typos, off-by-one errors, null values, incorrect config. |
| **5 Whys** | Keep asking \"why?\" until you reach the root cause. Symptom: \"The API returns 500.\" Why? \"Null pointer.\" Why null? \"Database returned no rows.\" Why no rows? \"The record was soft-deleted.\" Why soft-deleted? \"The cleanup job ran with wrong date filter.\" Root cause: cleanup job date filter. Fix: fix the filter. Symptom fix (null guard at API) would have masked the data loss. |


## Cognitive Biases That Sabotage Debugging
<!-- STANDARD: 3min -->

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Confirmation bias** | Testing only scenarios that confirm your theory, ignoring disconfirming evidence | Actively try to disprove your hypothesis. Write a test that should fail if your theory is correct. |
| **Anchoring on first diagnosis** | Sticking with your initial guess even as evidence mounts against it | After 30 minutes without progress, formally abandon your current hypothesis and start fresh. Write down 3 alternative explanations. |
| **Availability heuristic** | Assuming the bug is caused by whatever you most recently debugged | Before investigating, list the top 5 possible causes ranked by probability, not recency. |
| **Fundamental attribution error** | Blaming external libraries, frameworks, or \"someone else's code\" before checking your own | Rule: assume the bug is in YOUR code first. Framework bugs exist but are 100x less common than application bugs. |
| **Premature optimization** | Fixing the bug AND refactoring the module AND improving performance all at once | One PR = one bug fix. Do not refactor while debugging. You cannot distinguish which change actually fixed the bug. |


## What Masters Know That Others Don't
<!-- STANDARD: 3min -->

- **The first question is always: 'When did this start working correctly?'** Find the last known-good state. A bug that started today vs a bug that has existed for 6 months requires completely different investigation strategies.
- **Reproduction is 80% of the fix.** Once you can reliably reproduce a bug on demand, the fix is usually obvious. Invest aggressively in reproduction. Time spent reproducing is never wasted.
- **Logs lie. Metrics don't.** Application logs show what developers thought was important. Metrics and traces show what actually happened. When logs and metrics disagree, trust metrics.
- **The rubber duck is real.** Explaining the bug to someone else (or a rubber duck) forces you to articulate assumptions you didn't know you were making. At least 30% of debugging breakthroughs happen during the explanation, before the listener responds.

## Operating at Different Levels
<!-- STANDARD: 3min -->

- **Quick scan (30s):** Read the error message and stack trace. Identify: (1) the exact error type (NullPointerException, TypeError, TimeoutError), (2) the file and line number, (3) the operation that failed (DB query, API call, computation). Check if this is a known issue in your error tracking system (Sentry, Datadog, Bugsnag). If it is a duplicate, link it and move on.
- **Standard engagement (10min):** Full reproduction → narrow to module → identify root cause → write regression test → apply fix → verify. This is the standard debugging loop for 90% of bugs.
- **Deep dive (full session):** For bugs that resist standard debugging: git bisect across commits, delta debugging (binary search on inputs), log injection (add targeted logging at each layer), dependency isolation (does it happen without Redis? without the CDN?), and comparative analysis (what changed between working and broken states?).
- **Critical incident (SEV1/P0):** Stop-the-line protocol. All hands on deck. Goal: restore service, not find root cause. Mitigate first (rollback, feature flag off, traffic shift), then investigate. Post-incident: blameless postmortem with timeline, 5 Whys, and action items.

### Solo Developer
- Reproduce locally with exact inputs; use `console.log`/`print` for quick local debugging (never in production)
- Git bisect for regression introduction; binary search on code sections for isolation
- Rubber duck debugging: explain the code line by line to a colleague or write it out
- Stack traces as primary navigation tool; grep codebase for error messages
- Root cause documented in commit message with "why" not just "what"

### Small Team (2-5)
- Structured logging with correlation IDs across services
- Centralized error tracking (Sentry, DataDog) with alert rules on error rate spikes
- Blameless postmortem template for all SEV2+ incidents
- Debugging runbooks per service: common failure modes, diagnostic commands, rollback procedures
- Weekly bug triage: prioritize by user impact, assign with reproduction requirements

### Medium Team (5-20)
- Distributed tracing (OpenTelemetry, Jaeger) across all services — trace ID propagation mandatory
- Git bisect automated in CI for regression detection on performance/latency regressions
- Chaos engineering in staging: regular fault injection (latency, packet loss, service kill) to validate debugging tooling
- Production-safe diagnostics: read-only debug endpoints, sampled verbose logging, feature-flagged instrumentation
- Incident command training for all senior engineers; quarterly fire drills

### Enterprise (20+)
- Automated root cause analysis (RCA) pipelines: anomaly detection → correlated events → suspected commit → auto-rollback
- Centralized debugging platform: unified log search, trace viewer, metrics correlation across all services
- Chaos engineering in production: controlled experiments with automated abort criteria
- Bug tax budget: 15% of engineering capacity allocated to bug fixing and test gap closure
- Postmortem culture: every incident produces dated action items; quarterly review of recurrence patterns
- Debugging certification: L1 (local) → L2 (distributed) → L3 (incident command) training tracks

## When to Use
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->


## Auto-Route by Artifacts (Check Filesystem First)
<!-- STANDARD: 3min -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "debugging-and-error-recovery")` -- this is your skill | Redirect: \"I am Debugging and Error Recovery. Route by intent matching below.\" |
| A2 | `file_contains("error.log\|stacktrace\|crash", "panic\|segfault\|NullPointer\|TypeError\|500 Internal")` | **CRASH/ERROR** -- Stack trace available. Go to **Core Workflow: Phase 1 (Reproduce)** then trace-driven investigation. |
| A3 | `file_contains("bug_report.md\|issue", "intermittent\|sometimes\|flaky\|non-deterministic")` | **INTERMITTENT** -- Non-reproducible. Jump to **Decision Trees: Non-Reproducible Bug**. |
| A4 | `file_contains("incident\|postmortem", "SEV1\|SEV0\|P0\|P1\|critical\|outage")` | **CRITICAL INCIDENT** -- Stop-the-line protocol. Jump to **Decision Trees: Critical Incident Triage**. |
| A5 | `file_contains("git-log.txt", "")` OR `git log --oneline -50` available | **BISECT CANDIDATE** -- Recent commits may contain the bug. Go to **Core Workflow: Phase 2 (Localize)** with git bisect. |
| A6 | File has `console.log\|print(\|logger.` debugging statements scattered | **AD-HOC DEBUGGING** -- Developer was debugging manually. Jump to **Decision Trees: Structured Debugging Replacement**. |
| A7 | No artifacts -- verbal bug description only | **VERBAL REPORT** -- Start at **Core Workflow: Phase 0 (Clarify)**. Must extract reproduction steps before proceeding. |


## Intent Route (Ask the User)
<!-- STANDARD: 3min -->

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

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->
<!-- Full 168 lines extracted to references/core-workflow-1.md -->


## Phase 0: Clarify the Bug
<!-- STANDARD: 3min -->
Before touching any code, complete this template:
BUG TRIAGE TEMPLATE
===================
...
> 📎 **[references/core-workflow-1.md](references/core-workflow-1.md)** — 168 lines of detailed guidance

## Best Practices
<!-- STANDARD: 3min -->

1. **Reproduce before you investigate.** Every debugging session starts with reproduction. If you cannot reproduce the bug, you cannot confirm the fix. Capture exact inputs, environment state, and steps. A non-reproducible bug is not a debugging task — it's an observability gap. Instrument the code and wait for the next occurrence.
2. **Binary search narrows the search space exponentially.** Whether it's git bisect on commits, delta debugging on inputs, or commenting out half the code — each step eliminates 50% of possibilities. A 1024-commit range resolves to the exact commit in 10 bisect steps. A 500-line function resolves to the buggy line in 9 halvings. Never linearly scan when you can binary search.
3. **The 5 Whys trace symptoms to root causes.** "The app crashed" → Why? "NullPointerException in checkout" → Why? "User object was null" → Why? "Database returned no rows" → Why? "The user was deleted during checkout by a concurrent admin action" → Why? "No optimistic lock on the user row." Root cause found. Stop at the process or system level — not at "the developer made a mistake."
4. **Log analysis: timestamp correlation before content correlation.** When debugging distributed failures, align logs by timestamp across services before reading content. A 503 in Service A at 14:32:01.234 correlates with a connection timeout in Service B at 14:32:01.228 — 6ms earlier. Content confirms what timing suspected. Without timestamp alignment, you're reading 10,000 log lines hoping for a pattern.
5. **Rubber duck debugging works because it forces structured reasoning.** Explain the bug to a colleague (or a literal rubber duck) line by line. When you reach a line where you say "and then... it should..." — STOP. That "should" is an unverified assumption. Test it. 30-50% of bugs are found during the explanation phase alone, before the listener responds.
6. **Fix root cause, not symptom — then write the regression test that proves it.** A symptom fix (adding a null check) masks the root cause (why was it null in the first place?). After finding the root cause with 5 Whys, write a test that reproduces the exact failure chain, apply the minimal fix, and leave the test in the suite permanently. If the test suite didn't catch this bug, the test suite has a gap — fix the suite too.
7. **Critical incidents: mitigate first, investigate second.** The goal of incident response is restoring service, not finding root cause. Rollback, feature flag off, traffic shift — any action that restores service in under 5 minutes. Investigation begins after users stop experiencing the outage. Post-incident: blameless postmortem with timeline, 5 Whys, and dated action items.
8. **Never debug with `console.log` in production.** Logging PII violates GDPR/CCPA. Logging in hot paths 10x your log volume, drowning real signals and exceeding retention limits. Use structured logging (JSON, correlation IDs, sampling) and a debug-level log level that's disabled in production. If you must add temporary instrumentation, use a feature-flagged debug endpoint that auto-disables after 1 hour.
9. **The fix must be minimal — no refactoring mixed into a bug fix.** A bug fix PR that also renames 12 variables, extracts 3 helper methods, and reformats the module is a regression risk. The reviewer can't distinguish the fix from the refactoring. Ship the minimal fix first, verify it in production, then refactor in a separate PR. Separation of concerns applies to commits too.
10. **Close the loop: if the bug was non-reproducible, add instrumentation before closing.** A bug closed as "cannot reproduce" without added logging, metrics, or a Sentry alert will recur with zero additional data. Add structured logging at every decision point in the suspect code path. Set an alert for the error signature. The next occurrence should auto-create a ticket with a full trace — not another "cannot reproduce."

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

### Decision Tree 1: Bug Localization Strategy

        ┌── INPUT: Can you reproduce the bug?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Always]          [Sometimes]         [Never]
Reliable repro     Intermittent       Heisenbug
   │                 │                  │
   ▼                 ▼                  ▼
git bisect →     Add logging at     Binary search
narrow commits   decision points    the codebase:
                    │               comment out
               ┌────┴────┐          half → test
               ▼         ▼          → repeat
          Race cond?  Data-dep?
               │         │
               ▼         ▼
          Deterministic  Fuzz inputs
          ordering       property-based

### Decision Tree 2: Root Cause Analysis Depth

        ┌── INPUT: What is the bug's severity?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Critical/P0]    [High/P1]          [Medium/P2]
User-facing      Degraded           Cosmetic or
outage or data   functionality      edge case
loss
   │                 │                  │
   ▼                 ▼                  ▼
5 Whys +          3 Whys +          1 Why +
timeline          correlation       symptom check
analysis →        analysis →        → fix if <1h,
postmortem        regression test   backlog otherwise

### Decision Tree 3: Fix Validation Path

        ┌── INPUT: How was the bug discovered?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Customer Report] [Monitoring]      [Code Review]
External impact    Internal alert    Proactive find
   │                 │                  │
   ▼                 ▼                  ▼
1. Reproduce with  1. Correlate      1. Minimal fix
   customer data     with metrics    2. New test
2. Minimal fix     2. Test in staging 3. Verify no
3. Regression test 3. Canary deploy     similar patterns
4. Verify in prod  4. Monitor for 24h  4. Document
5. Close loop with                      in team wiki
   customer


## Decision Tree 1: Non-Reproducible Bug Strategy
<!-- STANDARD: 3min -->

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


## Decision Tree 2: Critical Incident Triage (Stop-the-Line)
<!-- STANDARD: 3min -->

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


## Decision Tree 3: Safe Fallback Patterns
<!-- STANDARD: 3min -->

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


## Decision Tree 4: Binary Search Debugging (Delta Debugging)
<!-- STANDARD: 3min -->

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


## Decision Tree 5: Distributed System Debugging
<!-- STANDARD: 3min -->

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


## Decision Tree 6: Memory Leak and Resource Exhaustion
<!-- STANDARD: 3min -->

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


## Decision Tree 7: Rubber Duck Debugging Protocol
<!-- STANDARD: 3min -->

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

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `code-reviewer` | Code quality assessment, security patterns, testing gaps | Before finalizing implementation or shipping to production |

## Proactive Triggers
<!-- STANDARD: 3min -->

These conditions automatically activate debugging scrutiny:

- **Trigger: any `console.error` or unhandled exception in production logs within the last hour.** Auto-initiate triage template. Do not wait for a bug report.
- **Trigger: error rate on a dashboard metric exceeds baseline by 3 standard deviations.** Auto-trigger: check recent deployments first.
- **Trigger: a bug report mentions "it was working yesterday" or "it broke after the deploy."** Auto-start git bisect between yesterday's deploy and the previous deploy.
- **Trigger: the same error signature appears in Sentry/Datadog >10 times in 5 minutes.** Auto-escalate to stop-the-line protocol if error rate is accelerating.
- **Trigger: a developer says "that's weird" or "I don't understand why this is happening."** Auto-trigger rubber duck protocol — the confusion itself is diagnostic data.

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "debugging-and-error-recovery",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }

   ```

3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.


## State Log Schema
<!-- STANDARD: 3min -->

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

1. **Git Bisect Drill:** Find a bug that was fixed in your codebase 1-3 months ago. Without looking at the fix, reproduce the bug and use git bisect to find the breaking commit. Time yourself. Goal: find the commit in under 10 minutes.
2. **Minimal Reproduction Challenge:** Take a complex bug report (long form, many steps). Reduce it to a reproduction in under 20 lines of code. Remove every dependency, every API call, every UI element that is not essential. The minimal repro should run in a single file.
3. **5 Whys Retrospective:** For the last 3 bugs your team fixed, apply the 5 Whys to each. Did the fix address the root cause or a symptom? Re-classify each fix. How many were actually root cause fixes?
4. **Rubber Duck Recording:** Next time you are stuck on a bug, record yourself (audio only) explaining the bug to an imaginary colleague. Listen to the recording. Identify the moment where you said "should" or "I assume" — that is your unverified assumption. Test it.
5. **Crash Dump Analysis:** Download a core dump or heap dump from a production crash. Use the appropriate tool (lldb, gdb, Chrome DevTools Memory, Eclipse MAT) to identify: (1) the crashing thread, (2) the exact line, (3) the state of relevant variables. Production debugging without a debugger is an essential skill.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "It works on my machine — the fix is correct." | Your machine lacks production data, traffic patterns, config, network latency, and scale. Race conditions, connection pool exhaustion, and OOM bugs pass locally every time. Cost: **$20K-$100K** in rollback + incident response for a fix that passes local but fails in prod. |
| "QA will catch it — that's what the QA phase is for." | QA finds ~30% of bugs. The other 70% ship to production and are discovered by users at 10x the fix cost. Offloading quality downstream is the most expensive testing strategy. Cost: **$50K-$200K/year** in production incidents that should have been caught earlier. |
| "I'll just add a try-catch and move on — the error is handled." | A try-catch that swallows the exception converts a visible error into silent data corruption. The error still occurs, but now nobody knows. Cost: **$15K-$75K** in silent data corruption discovered weeks later when reconciliation fails. |
| "It's a one-line fix — no need for a regression test." | The one-liner changes return type semantics, and every caller that didn't handle the new null/unexpected value now has a latent bug. Cost: **$50K+** in cascading failures from a "safe" fix that had no test coverage. |
| "I can't reproduce it — closing the bug as 'cannot reproduce.'" | A non-reproducible bug is not fixed — it is waiting. Without instrumentation at the suspect site, it will recur with zero additional data. Cost: **$5K-$25K** for each recurrence that could have been caught with structured logging or a Sentry alert. |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

- **Adding try/catch without understanding the error.** A try/catch that swallows the exception (empty catch block) converts a visible error into silent data corruption. The error still occurs, but now nobody knows. **Total cost: $15,000-$75,000 in silent data corruption discovered weeks later.**
- **Reverting the wrong commit during an incident.** In the panic of a SEV1, reverting a commit without verifying it is the cause can make things worse (reintroduce an old bug) without fixing the current one. **Total cost: $50,000-$200,000 in extended outage + compounding failures.**
- **Fixing a bug without understanding why the test suite didn't catch it.** If tests passed before the bug, the test suite has a gap. Fixing only the code and not the tests means the same class of bug will ship again. **Total cost: $10,000-$30,000 per recurrence in a 12-month period.**
- **Debugging with `console.log` in production.** Logging PII (emails, tokens, SSNs) violates GDPR/CCPA. Logging in hot paths can 10x your log volume, exceeding retention limits and drowning real signals. **Total cost: $25,000-$500,000 in compliance fines + $5,000/month in log storage overage.**
- **Assuming "it works on my machine" means the fix is correct.** Your machine does not have production data, production traffic patterns, production config, production network latency, or production scale. Bugs that only appear at scale (race conditions, connection pool exhaustion, OOM) will pass locally every time. **Total cost: $20,000-$100,000 in rollback + incident response for a fix that passes local but fails in prod.**
- **Closing a bug as "cannot reproduce" without instrumenting the code.** A non-reproducible bug is not fixed — it is waiting. Adding structured logging, metrics, or a sentry alert at the suspect site converts "cannot reproduce" into "will catch next time." Without instrumentation, the bug will recur with zero additional data. **Total cost: $5,000-$25,000 for each recurrence that could have been caught.**
- **Running a diagnostic query on a production database during peak traffic.** A `SELECT * FROM large_table` without `LIMIT` or on an unindexed column can cause a table scan that locks rows and blocks writes, turning a debugging session into a production outage. **Total cost: $30,000-$150,000 in downtime from a self-inflicted incident.**

## Anti-Patterns
<!-- STANDARD: 3min -->

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| Adding try/catch that swallows the exception (empty catch block) — converts a visible error into silent data corruption | Always log the error with full context. If the error is expected, handle it explicitly. If unexpected, re-throw or propagate to the error boundary. Empty catch = bug incubator. |
| Reverting the wrong commit during an incident panic — makes things worse without fixing the original issue | Verify the commit is the cause before reverting. Use `git bisect` to confirm. Rollback should be a deliberate action, not a panic reaction. |
| Fixing a bug without understanding why the test suite didn't catch it — same class of bug will ship again | After fixing, identify the test gap and add a regression test. If no test covers this code path, that's the real root cause. Fix the suite, not just the code. |
| Debugging with `console.log` in production — PII exposure, log volume explosion, signal drowning | Use structured logging (JSON, correlation IDs) with debug-level disabled in production. Temporary instrumentation via feature-flagged debug endpoint with 1-hour auto-disable. |
| Closing a bug as "cannot reproduce" without instrumenting the code — bug will recur with zero additional data | Add structured logging at every decision point. Set a Sentry/DataDog alert for the error signature. The next occurrence should auto-create a ticket with a full trace. |
| Fixing the symptom (null check) without finding root cause (why was it null?) — the same null appears elsewhere tomorrow | 5 Whys from symptom to system-level root cause. If the answer is "the developer made a mistake," ask why the mistake wasn't caught — missing test, missing lint rule, missing code review? |
| Mixing refactoring into a bug fix PR — reviewer can't distinguish fix from refactoring, regression risk multiplies | Ship the minimal fix first. Verify in production. Refactor in a separate PR. A 5-line fix with a 200-line refactor is a 200-line regression risk, not a 5-line fix. |

## Production Checklist

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Bug reproduction confirmed — exact steps, inputs, and environment state captured; reproduction test FAILS before the fix is applied | Reproduction test committed before fix; `git log` shows test commit with FAIL assertion before fix commit; re-run test on clean checkout to confirm |
| ☐ | Root cause identified via 5 Whys — traced past symptom to system/process level (not "developer made a mistake") | 5 Whys chain documented in the issue tracker; deepest why identifies a process, tool, or automation gap — not individual human error |
| ☐ | Fix is minimal — `git diff` shows only lines directly related to resolving the root cause; no refactoring, reformatting, or unrelated changes mixed in | `git diff main...fix-branch --stat` — file count and line count should match scope of the bug; reviewer confirms no scope creep |
| ☐ | Regression test covers the exact failure chain PLUS at least one edge-case variant — FAILS before fix, PASSES after fix | Regression test committed in same PR as fix; edge-case variant exercises a boundary condition of the original failure (null, empty, max, boundary value) |
| ☐ | All existing tests pass — no regressions introduced; dependent module test suites run if changed code is imported elsewhere | Full test suite passes (`npm test` / `pytest` / `go test ./...` ); grep import graph: `grep -r "import.*changedModule" --include="*.test.*"` and run those suites too |
| ☐ | Fix tested in production-like environment — matching data shapes, config values, concurrency patterns, and network latency | Deploy to staging or canary at 1% traffic; monitor error rate, latency, and business metric for ≥ 15 minutes; compare to pre-fix baseline |
| ☐ | Rollback plan documented and tested — can revert the fix without side effects if it causes downstream issues | Test rollback in staging: revert commit, verify system returns to pre-fix state (same errors return, same behavior restored); document revert command in issue |
| ☐ | If production bug: blameless postmortem scheduled with timeline, 5 Whys, and dated action items with individual owners | Postmortem doc created with all four components; calendar invite sent within 48 hours of incident resolution; action items tracked in issue tracker with sprint assignment |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Bug reproduction test written and FAILS before the fix — exact steps, inputs, and environment state captured | Reproduction test committed before fix; `git log` shows test commit before fix commit |
| ☐ | Complete when Root cause identified using 5 Whys — traced past symptom to system/process level (not "developer made a mistake") | 5 Whys chain documented in issue; deepest why identifies a process/tool gap, not individual error |
| ☐ | Complete when Fix is minimal — changes only what is necessary to resolve the root cause; no refactoring, reformatting, or unrelated changes mixed in | `git diff` shows only lines directly related to the fix; reviewer confirms no scope creep |
| ☐ | Complete when All existing tests pass — no regressions introduced; dependent module suites run if changed code is imported elsewhere | Full test suite passes; dependent module suites (identified via import graph) also pass |
| ☐ | Complete when Regression test covers the exact failure chain AND at least one edge case variant — FAILS before fix, PASSES after | Regression test committed; edge case variant exercises boundary condition of the original failure |
| ☐ | Complete when Fix tested in production-like environment: matching data shapes, config values, concurrency patterns, and network latency | Staging or canary deployment confirms fix under production-like load and data |
| ☐ | Complete when Rollback plan documented and tested — can revert the fix without side effects if it causes downstream issues | Rollback tested in staging: revert commit, verify system returns to pre-fix state |
| ☐ | Complete when If production bug: blameless postmortem scheduled with timeline, 5 Whys, and dated action items with owners | Postmortem doc created with all four components; calendar invite sent within 48 hours of incident |
| ☐ | Complete when If non-reproducible: instrumentation added (structured logging, metrics, alert) to catch next occurrence with full trace | Instrumentation deployed to production; alert configured with appropriate threshold; test trigger verified |
| ☐ | Complete when Test suite gap identified and documented: why didn't existing tests catch this? Gap scheduled for closure | Gap documented in issue tracker; remediation task has owner and sprint assignment |

## Verification Guardrails
<!-- STANDARD: 3min -->

- [ ] **[DB1]** Bug reproduction confirmed: exact steps, inputs, environment state captured — bug manifests before any fix is applied
- [ ] **[DB2]** Root cause identified via 5 Whys — traced past symptom to system/process level (not "developer made a mistake")
- [ ] **[DB3]** Fix is minimal — changes only what is necessary to resolve the root cause; no refactoring, reformatting, or unrelated changes mixed in
- [ ] **[DB4]** Regression test written that reproduces the exact failure chain and FAILS before the fix, PASSES after
- [ ] **[DB5]** All existing tests pass — no regressions introduced; dependent module suites run if changed code is imported elsewhere
- [ ] **[DB6]** Fix tested in production-like environment: matching data shapes, config values, concurrency patterns, and network latency
- [ ] **[DB7]** Rollback plan documented and tested — can revert the fix without side effects if it causes downstream issues
- [ ] **[DB8]** If production bug: blameless postmortem scheduled with timeline, 5 Whys, and dated action items with owners
- [ ] **[DB9]** If non-reproducible: instrumentation added (structured logging, metrics, alert) to catch next occurrence with full trace
- [ ] **[DB10]** Test suite gap identified: why didn't existing tests catch this? Gap documented and scheduled for closure
- [ ] **[DB11]** Debugging artifacts cleaned: temporary log statements, debug endpoints, feature flags removed or disabled
- [ ] **[DB12]** Root cause documented in issue tracker and/or code comment — future developers can understand why the fix exists, not just what it does
- [ ] **[DB13]** If database query changed: EXPLAIN plan verified, index usage confirmed, no full table scans on production-sized data
- [ ] **[DB14]** If distributed system bug: distributed tracing correlation verified; fix validated across all affected service boundaries

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Production bug: "Cannot read property 'name' of undefined." Stack trace points to minified line 1, column 438921 — useless | Source maps not uploaded to error tracking. Build pipeline generates source maps but they're stored in CI artifacts, not sent to Sentry/Datadog. Minified stack trace is a pointer to an opaque blob | Upload source maps to error tracking service in CI: `sentry-cli sourcemaps upload --org myorg ./dist`. Verify: trigger a test error and confirm the dashboard shows original source with line numbers. Alert if source map upload fails | A minified stack trace is worse than no stack trace — it gives the illusion of useful information. The "line 1, column 438921" is the difference between a 5-minute fix and a 5-hour investigation. |
| `git bisect` identifies the bad commit — but it's a merge commit touching 47 files. Still don't know which change caused it | Merge commit squashes 3 days of work into one commit. Bisect says "this commit broke it" but the commit contains the auth refactor, payment changes, AND the dashboard redesign | Never squash-merge feature branches. Rebase-merge to preserve individual commits. Require each commit to pass CI independently. Bisect should point to a single logical change, not a firehose of unrelated modifications | Merge commits are time bombs for debugging. When bisect lands on a merge commit with 47 files, you're back to manual inspection. Each commit should be a bisectable unit of change. |
| Error rate spikes at 2:17 AM, self-resolves at 2:19 AM. No alert fired (threshold was 5 minutes sustained). Nobody knows it happened | Monitoring alert configured for "sustained >5 minutes" to reduce noise. The 2-minute spike was a real issue but below the alert threshold. Only discovered during weekly metrics review | Dual alert thresholds: immediate alert on sudden spike (>3σ from baseline for 60 seconds) AND sustained alert (>2σ for 5 minutes). Short spikes get a P3 ticket automatically created — no page, but tracked. Weekly review of all P3 auto-tickets | The gap between "not alertable" and "not a problem" is where undetected incidents live. Short spikes that self-resolve are early warnings. If you don't track them, you discover them in the post-mortem of the big one. |
| `console.log("got here")` — the 47 debugging statements committed to main. Developer used logs to trace a bug, fixed it, forgot to remove the logs | No debugging hygiene discipline. Print-statement debugging is fast but has no cleanup step. The logs went through code review and nobody flagged them because they looked like legitimate logging | Use a debug library with namespaces: `debug('app:auth:login')`. Disable in production via env var. CI check: `grep -r "console\." src/ | grep -v "console.error\|console.warn"` blocks merge if non-error console statements found | Print-statement debugging works. The problem is cleanup. If your debugging tool doesn't force you to remove traces after fixing the bug, production becomes a museum of every bug ever fixed. |
| Database deadlock happening on 0.01% of requests — can't reproduce locally, can't add breakpoints in production | Race condition that only manifests under production concurrency levels. Local dev has 1 user. Production has 500 concurrent transactions fighting for the same row lock | Add structured logging around the deadlock zone: log transaction start time, lock acquisition time, and all queries with execution time. Use `SHOW ENGINE INNODB STATUS` (MySQL) or `pg_stat_activity` (Postgres) snapshots during incident. Replay production query patterns with `pgbench` at scale | Heisenbugs that only appear at production concurrency are the hardest class of bugs. You can't reproduce them; you can only instrument around them until the logs reveal the pattern. |
| "Fixed in commit abc1234" — 3 weeks later, same bug reported again. The fix was a workaround, not a root cause fix | Developer fixed the symptom (null check on the crashing line) but didn't trace back to why the value was null. The null came from a race condition 3 callers up — still present | Post-fix checklist: (1) Can I reproduce the original bug without the fix? (2) After applying fix, does the root cause still exist? (3) Is there a test that would have caught this? If answer to (3) is no, write the test. Document root cause in commit message body, not just title | Fixing the crash site without fixing the root cause is palliative care for software. The symptom returns. Always trace the null/undefined/error back to its origin — the crash is the messenger, not the problem. |

## References
<!-- STANDARD: 3min -->

- [Core Workflow](../references/core-workflow.md) — Detailed 6-phase workflow with extended code examples
- [Anti-Patterns](../references/anti-patterns.md) — Common debugging mistakes that waste hours
- [Best Practices](../references/best-practices.md) — Battle-tested debugging techniques from SRE teams
- [Calibration](../references/calibration.md) — When to stop debugging and escalate
- [Checklist](../references/checklist.md) — Pre-close bug verification checklist
- [Error Decoder](../references/error-decoder.md) — Common error messages decoded with root cause mappings
- [Footguns](../references/footguns.md) — Debugging techniques that frequently backfire
