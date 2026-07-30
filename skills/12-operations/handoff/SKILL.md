---
name: handoff
description: >
  Use when a conversation is approaching context limits and needs compaction;
  when work needs to transfer between agents or sessions; when a long-running task
  spans multiple sessions; when preparing a status update for a stakeholder; or
  when pausing work that will resume later. Handles conversation-to-handoff
  compaction, progress ledger creation and maintenance, cross-session state
  preservation, decision capture with rationale, blocker documentation with next
  steps, exact file path and command recording, fresh-agent restartability
  (handoff must contain everything needed to continue), and git-ignored workspace
  for ledger files. Do NOT use for code documentation (route to
  documentation-engineer or technical-writer), issue tracking (route to
  project-manager), or meeting notes that don't involve agent work.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: operations
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - handoff
  - context-compaction
  - progress-ledger
  - cross-session
  - agent-transfer
  - workspace
token_budget: 4000
chain:
  consumes_from:
    - project-manager
    - technical-writer
  feeds_into:
    - project-manager
    - wayfinder
  alternatives: []
---
# Handoff

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Compact the current conversation into a handoff document so another agent (or session) can continue the work without losing context. The handoff captures what was being done, what's completed, what's remaining, key decisions made, current blockers, and next concrete steps — the "progress ledger" pattern from obra/superpowers.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
* [VERIFIED] before any production guidance: Verify assumptions. Verify compatibility. Verify correctness.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that detect handoff failures before they cost hours of rework.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to produce a handoff without exact file paths. A handoff that says "the auth module" instead of `src/auth/middleware.ts:42-78` costs the next agent 15-30 minutes of orientation. | Trigger: handoff document contains no file path containing a `/` or `\` separator AND handoff references code locations | STOP. Respond: "Every code reference in the handoff must include at least one file path with line numbers. Replace descriptions with paths before proceeding." |
| R2 | REFUSE to handoff mid-decision. An unresolved decision with no rationale recorded is context rot — the next agent will either re-litigate or guess. | Trigger: `grep -c "DECIDING:\|UNDECIDED:\|TBD:" handoff.md` returns > 0 AND no rationale recorded for why the decision was deferred | STOP. Respond: "Unresolved decisions detected. For each: record the options considered so far, the tradeoff, and a recommendation. Deferred decisions must include a trigger condition for when to revisit." |
| R3 | DETECT when a handoff is too vague to be restartable. A handoff must contain: current working directory, branch, exact command to resume, and next 3 concrete steps. | Trigger: handoff lacks at least 3 of: `cwd:`, `branch:`, `resume_command:`, `next_step_1:`, `file manifest` | STOP. Respond: "Handoff is not restartable. Minimum required fields: cwd, branch, resume command, and 3 concrete next steps with expected outcomes." |
| R4 | REFUSE to trust memory over the ledger. "I'll remember what to do next" is anti-rationalization — context windows are ephemeral. The ledger is the source of truth. | Trigger: handoff contains "we'll figure out", "I'll remember", "will revisit later", or "obvious next step" without a concrete action | STOP. Respond: "Replace every vague forward reference with a concrete action. 'We'll figure out the rate limit' becomes 'NEXT: Run `ab -n 1000 /api/health` and record p99 latency. Target: <50ms. File results to perf-testing/rate-limit-baseline.log.'" |
| R5 | DETECT when blocker description lacks a specific, testable resolution condition. "Blocked on API team" is not actionable. | Trigger: blocker statement contains "waiting on", "blocked by", "depends on" AND no resolution condition that can be verified with a command | STOP. Rewrite as: "BLOCKED: API team to expose `GET /users/:id/permissions` endpoint. RESOLUTION: `curl -s https://api.staging.example.com/users/42/permissions \| jq '.scopes'` returns non-empty array. ETA: 2026-07-25. ESCALATION: If not resolved by ETA + 1 day, ping #api-team Slack." |
| R6 | REFUSE to handoff without a ledger file in the git-ignored workspace directory. The progress ledger is the single source of truth that survives compaction. | Trigger: `ls .handoff/ledger.md 2>/dev/null` returns non-zero AND handoff claims to be a continuation of previous work | STOP. Respond: "No ledger file found in .handoff/workspace. Create one at .handoff/ledger.md with the session history, or note this as a fresh start with no prior ledger." |
| R7 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R8 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

* **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
* **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
* **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
* **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a context preservation specialist. Your job is to make the next agent's first 5 minutes maximally productive — they should understand the current state, the next action, and the rationale for all prior decisions without reading the full conversation history.

* **The ledger is the source of truth, not your memory.** Every decision, blocker, and next step goes into the ledger. Trust the ledger and git log over your own recollection.
* **Fresh agents know nothing.** Write as if the next agent has never seen this conversation. Assume zero prior context. Every reference must be self-contained and resolvable.
* **Concrete over abstract.** "Fix the rate limit bug" is useless. "In `src/middleware/rate-limiter.ts:47`, the sliding window reset uses `Date.now()` instead of a monotonic clock — fix by importing `performance.now()` from `perf_hooks`" is actionable.
* **Decisions decay.** A decision recorded without its rationale will be questioned and possibly reversed by the next agent. Every decision needs: options considered, chosen option, why, and tradeoffs accepted.
* **Blockers are not parking lots.** A blocker without an escalation path and a resolution condition is just a way to abandon work politely. Every blocker gets: resolution condition, ETA, and escalation trigger.

## Operating at Different Levels
<!-- STANDARD: 3min -->

* **Quick handoff (5 min):** For short pauses between sessions (same day, same agent). Capture: current branch, exact file being edited, line number, next 1-2 edits. Minimal — just enough to resume without re-orientation.
* **Session handoff (15 min):** For end-of-day or compaction-triggered handoffs. Full progress ledger update: completed items, remaining work, decisions made, blockers, next 3 steps, file manifest.
* **Cross-agent handoff (30 min):** For transferring work to a different agent or team. Includes everything in session handoff PLUS: project context summary, architecture decisions, dependency graph, testing strategy, and a 5-minute orientation section.
* **Stakeholder handoff (20 min):** For status updates to non-agent consumers (PMs, tech leads). Progress summary with milestone tracking, risk register, and resource needs. Less technical detail, more decision context.

## When to Use
<!-- STANDARD: 3min -->

Use handoff when the conversation context needs to survive beyond the current session or agent.

* Context window is approaching limits and conversation will be compacted
* Work needs to transfer from one agent session to another
* A long-running task spans multiple sessions (multi-day feature, migration, investigation)
* Preparing a status update for a stakeholder (PM, tech lead, team)
* Pausing work that will resume after interruption (end of day, weekend, context switch)
* Pairing with wayfinder to track investigation ticket progress across sessions

Do NOT use handoff for code documentation (route to documentation-engineer or technical-writer). Do NOT use for issue tracking or sprint backlog (route to project-manager). Do NOT use for meeting notes that don't involve agent-executed work.

## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists(".handoff/ledger.md")` AND `file_contains(".handoff/ledger.md", "SESSION_ACTIVE\|IN_PROGRESS")` | Resume existing handoff -> Go to **Core Workflow: Phase 2 — Update Ledger** |
| A2 | `file_exists(".handoff/ledger.md")` AND `file_contains(".handoff/ledger.md", "COMPLETED\|ARCHIVED")` | Previous work completed -> Go to **Core Workflow: Phase 1 — Fresh Handoff** |
| A3 | `file_exists(".handoff/ledger.md")` AND `file_contains(".handoff/ledger.md", "BLOCKED:")` | Blocked work -> Jump to **Decision Trees: Blocker Resolution** |
| A4 | No ledger file found | Fresh handoff -> Go to **Core Workflow: Phase 1 — Initialize Workspace** |
| A5 | `file_exists("*.handoff*.md")` outside .handoff/ directory | Migrate legacy handoff -> Go to **Decision Trees: Migration** |

### Intent Route (Ask the User)

```
What kind of handoff do you need?
|-- Saving progress before compaction -> Jump to "Core Workflow: Phase 2 — Compaction Handoff"
|-- Transferring to another agent -> Jump to "Decision Trees: Cross-Agent Handoff"
|-- Preparing stakeholder status update -> Jump to "Decision Trees: Stakeholder Handoff"
|-- Documenting a blocker for handoff -> Jump to "Decision Trees: Blocker Documentation"
|-- First time setting up handoff workspace -> Start at "Core Workflow: Phase 1"
```

## Core Workflow
<!-- STANDARD: 3min -->

**(STANDARD)**

### Phase 1: Initialize Workspace

Execute in order. Do not skip steps.

```
1. CREATE WORKSPACE DIRECTORY
   |-- mkdir -p .handoff/
   |-- echo ".handoff/" >> .gitignore (if not already present)
   |-- Purpose: ledger files survive session compaction, are git-ignored

2. CAPTURE SESSION CONTEXT
   |-- Record: git branch, current commit hash, working directory
   |-- Record: task description (1-2 sentences of what we're trying to accomplish)
   |-- Record: session start timestamp

3. INITIALIZE LEDGER
   |-- Create .handoff/ledger.md with sections:
   |   - # Session Ledger: [task-name]
   |   - ## Context (branch, commit, cwd, task description)
   |   - ## Completed (empty initially)
   |   - ## In Progress (current focus, file, line)
   |   - ## Remaining (ordered task list)
   |   - ## Decisions (decision log with rationale)
   |   - ## Blockers (empty initially)
   |   - ## Next Steps (concrete, ordered, with expected outcomes)
   |-- Format: markdown with machine-parseable prefixes (DONE:, DOING:, TODO:, DECIDED:, BLOCKED:)
```

  Complete when: Workspace directory created, session context captured, and ledger initialized with all required sections.

### Phase 2: Capture Progress (Continuous)

Throughout the session, update the ledger as work happens. Do not batch at the end — batch defeats the purpose.

```
1. ON TASK COMPLETION:
   |-- Move item from "Remaining" to "Completed" with timestamp
   |-- Add DONE: prefix with verification evidence
   |-- Example: "DONE: Added rate limiter middleware | src/middleware/rate-limiter.ts | Verified: `npm test -- rate-limiter` passes"

2. ON DECISION MADE:
   |-- Add DECIDED: entry with options, choice, rationale, tradeoffs
   |-- Example: "DECIDED: Use Redis over PostgreSQL for rate limit counters.
   |   Options: (a) PostgreSQL with UPDATE...RETURNING, (b) Redis with INCR + EXPIRE.
   |   Chose (b): sub-millisecond increments, automatic TTL-based cleanup, no migration needed.
   |   Tradeoff: adds Redis dependency; acceptable given existing Redis for session store."

3. ON BLOCKER ENCOUNTERED:
   |-- Add BLOCKED: entry with condition, resolution criteria, ETA, escalation path
   |-- Set RESOLUTION: with a verifiable command
   |-- Set ESCALATION: with trigger condition and contact

4. ON FILE CREATED/MODIFIED:
   |-- Maintain a FILE MANIFEST section listing all files touched
   |-- Include: path, operation (create/edit/delete), purpose (1 line)
```

  Complete when: All completed tasks, decisions, blockers, and file changes recorded in ledger with timestamps and verification evidence.

### Phase 3: Produce Handoff Document

When compaction is imminent or session is ending:

```
1. FREEZE LEDGER
   |-- Add SESSION_END timestamp
   |-- Mark current IN_PROGRESS items with exact line number and mental state
   |-- Example: "DOING: Refactoring token validation in src/auth/validator.ts:142
   |   State: Extracted JWT decode to separate function, mid-edit on verify() wrapper.
   |   Resume: Complete verify() wrapper, then update callers in auth-router.ts and middleware.ts."

2. GENERATE HANDOFF SUMMARY (.handoff/handoff-YYYYMMDD-HHMM.md)
   |-- One-paragraph executive summary
   |-- What was accomplished (copy from Completed section)
   |-- What remains (copy from Remaining section)
   |-- Current blocker status
   |-- RESUME COMMAND: exact command to continue (e.g., "cd /project && git checkout feat/rate-limit && nvim src/middleware/rate-limiter.ts:142")
   |-- Next 3 concrete steps with expected outcomes

3. APPEND TO LEDGER INDEX
   |-- .handoff/index.md: chronological list of all handoff documents with date, summary, status
```

  Complete when: Handoff document reviewed by receiving team lead or next session, and all open items have owners.
Complete when: All deliverables verified against acceptance criteria, stakeholder sign-off obtained, and documentation updated with final decisions and rationale.
Complete when: Risk register reviewed with mitigation owners assigned, residual risk levels within acceptable thresholds, and escalation paths documented for all identified risks.
Complete when: Quality gates passed: peer review completed, automated checks green, test coverage meets minimum thresholds, and no blocking issues remain open.
Complete when: Implementation validated against requirements with traceability matrix updated, edge cases tested, and rollback plan documented and rehearsed.
Complete when: Performance metrics baselined and monitored: key indicators within expected ranges, alerts configured for threshold breaches, and dashboard accessible to stakeholders.

## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

### Cross-Agent Handoff Depth

```
                     ┌──────────────────────┐
                     │ Is the receiving agent   │
                     │ the SAME agent type?     │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐     ┌──────────▼──────────┐
                     │ YES                   │     │ NO                    │
                     └──────────┬───────────┘     └──────────┬───────────┘
                                │                            │
                     ┌──────────▼──────────┐     ┌──────────▼──────────┐
                     │ STANDARD HANDOFF       │     │ Does the receiving     │
                     │ Ledger + resume cmd    │     │ agent understand the   │
                     │ Trust shared context   │     │ domain?                │
                     └──────────────────────┘     └──────┬───────────┬─────┘
                                                        │YES         │NO
                                                        ▼            ▼
                                                 ┌──────────┐ ┌──────────────┐
                                                 │ ENRICHED  │ │ DEEP HANDOFF │
                                                 │ HANDOFF   │ │ Full context  │
                                                 │ + domain  │ │ + domain      │
                                                 │ glossary  │ │ intro + arch  │
                                                 │ + arch    │ │ diagram +     │
                                                 │ summary   │ │ glossary +     │
                                                 └──────────┘ │ file map       │
                                                              └──────────────┘
```

### Blocker Documentation Quality

```
                     ┌──────────────────────┐
                     │ Blocker statement       │
                     │ received                │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Has specific RESOLUTION │
                     │ condition?              │
                     │ (verifiable with cmd)   │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Has ETA? │ │ INCOMPLETE BLOCKER │
                     └──┬───┬───┘ │ ASK: When will     │
                       │YES │NO   │ this unblock? What  │
                       ▼    ▼     │ command proves it?  │
                 ┌──────┐ ┌──────────┐ └──────────────────┘
                 │ Valid│ │ SOFT     │
                 │Blocker│ │ BLOCKER │
                 └──┬───┘ │ Add ETA  │
                    │      │ + escalate│
                    ▼      │ condition │
              ┌──────────┐ └──────────┘
              │HANDOFF   │
              │READY     │
              └──────────┘
```

### Handoff Compaction vs Fresh Start

```
                     ┌──────────────────────┐
                     │ Context window          │
                     │ approaching limit       │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Is there an EXISTING    │
                     │ ledger file in          │
                     │ .handoff/?              │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Is ledger│ │ FRESH HANDOFF      │
                     │ < 7 days │ │ Create .handoff/    │
                     │ old?     │ │ Initialize ledger   │
                     └──┬───┬───┘ └──────────────────┘
                       │YES │NO
                       ▼    ▼
                 ┌──────┐ ┌──────────┐
                 │RESUME│ │ Does work│
                 │Update│ │ still     │
                 │ledger│ │ matter?   │
                 └──────┘ └──┬───┬────┘
                            │YES │NO
                            ▼    ▼
                      ┌──────────┐ ┌──────────┐
                      │ FRESH     │ │ ARCHIVE  │
                      │ HANDOFF   │ │ Move to  │
                      │ reference │ │ .handoff/ │
                      │ old ledger│ │ archive/  │
                      └──────────┘ └──────────┘
```

### Restartability Assessment

```
                     ┌──────────────────────┐
                     │ Handoff document        │
                     │ produced                │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ SELF-TEST: Can a fresh   │
                     │ agent resume in <5 min?  │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ HANDOFF  │ │ MISSING:            │
                     │ COMPLETE │ │ Identify which of:  │
                     └──────────┘ │ [] cwd              │
                                  │ [] branch           │
                                  │ [] resume command   │
                                  │ [] file manifest    │
                                  │ [] next 3 steps     │
                                  │ [] blocker status   │
                                  │ [] decision log     │
                                  └──────┬─────────────┘
                                         │
                                  ┌──────▼─────────────┐
                                  │ ADD missing fields   │
                                  │ RE-TEST restartability│
                                  └────────────────────┘
```

### Ledger Health Check

```
                     ┌──────────────────────┐
                     │ Run ledger health check │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ All TODO items have     │
                     │ concrete next action?   │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ All      │ │ FLAG: Convert       │
                     │ DECIDED  │ │ "Investigate X" to  │
                     │ have     │ │ "Run grep for X in  │
                     │ rationale│ │ src/*.ts, document  │
                     │?         │ │ findings"           │
                     └──┬───┬───┘ └──────────────────┘
                       │YES │NO
                       ▼    ▼
                 ┌──────┐ ┌──────────────────┐
                 │ All  │ │ FLAG: Add "Why?"    │
                 │BLOCKED│ │ to each DECIDED    │
                 │have   │ │ without rationale  │
                 │ETA?   │ └──────────────────┘
                 └──┬───┬───┘
                   │YES │NO
                   ▼    ▼
              ┌──────────┐ ┌──────────────────┐
              │ LEDGER   │ │ ADD: ETA +          │
              │ HEALTHY  │ │ escalate condition  │
              └──────────┘ └──────────────────┘
```

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

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

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Large investigation spanning multiple sessions | wayfinder | Wayfinder creates investigation tickets; handoff preserves progress between ticket resolutions |
| Handoff contains feature implementation details | project-manager | Project manager tracks milestone progress; handoff provides granular completion data |
| Handoff to documentation team | technical-writer, documentation-engineer | Technical decisions in handoff become architecture decision records |
| Multi-agent pipeline handoff | All downstream skills involved | Chain handoffs together: each agent appends to ledger, passes to next |
| Handoff reveals process gap | scrum-master | Recurring blocker patterns in handoffs signal process improvement opportunities |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `project-manager` | Timeline, resource allocation, stakeholder map, risk register | Before operational planning or execution |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | Session approaching context limit (80%+ tokens consumed) AND `.handoff/ledger.md` is stale (>10 turns since last update) | [ALERT] Update ledger NOW — compaction is imminent. Capture current file, line, mental state. |
| P2 | `git branch --show-current` differs from ledger's recorded branch | [WARN] Branch mismatch. Update ledger context or confirm intentional branch switch. |
| P3 | `.handoff/ledger.md` has BLOCKED: entry older than 48 hours with no update | [ALERT] Stale blocker detected. Check resolution status, escalate per escalation path. |
| P4 | `.handoff/` directory exists but not in `.gitignore` | [FIX] Add `.handoff/` to `.gitignore` — ledger files must not be committed. |
| P5 | Ledger has >20 TODO items with no priority ordering | [WARN] Ledger is a backlog, not a plan. Prioritize: top 3 items only. Archive rest to `backlog.md`. |
| P6 | Handoff document produced but missing 2+ restartability fields | [BLOCK] Handoff not restartable. Add missing fields before session ends. |

## What Good Looks Like
<!-- STANDARD: 3min -->

### Before (Vague Handoff)

```
TODO:
* Fix the auth bug
* Add rate limiting
* Update docs

Blocked on: API team

Decisions: Used Redis.
```

Problems: No file paths, no line numbers, no rationale, no resolution condition for blocker, no resume command, no next steps.

### After (Restartable Handoff)

```markdown
# Session Ledger: Rate Limiter Implementation
## Context
<!-- STANDARD: 3min -->
* branch: feat/rate-limit
* commit: a1b2c3d
* cwd: /project/backend
* task: Add per-user rate limiting to API gateway

## Completed
<!-- STANDARD: 3min -->
* DONE: Rate limiter middleware scaffold | src/middleware/rate-limiter.ts | Tests: `npm test -- rate-limiter` (12/12 pass)
* DONE: Redis client configuration | src/config/redis.ts:15-32 | Verified: `redis-cli PING` → PONG

## In Progress
<!-- STANDARD: 3min -->
* DOING: Token bucket refill logic | src/middleware/rate-limiter.ts:47
  State: Bucket decrement working, refill rate calculation in progress.
  Resume: Implement `refillTokens()` using `performance.now()` for monotonic timing.

## Remaining
<!-- STANDARD: 3min -->
1. TODO: Implement refillTokens() — src/middleware/rate-limiter.ts:47
2. TODO: Add rate limit headers (X-RateLimit-*) — src/middleware/rate-limiter.ts:89
3. TODO: Integration test with concurrent requests — tests/integration/

## Decisions
<!-- STANDARD: 3min -->
* DECIDED: Token bucket over sliding window log
  Options: (a) sliding window log (precise but high memory), (b) token bucket (approximate, constant memory).
  Chose (b): acceptable 5% over-limit tolerance, constant O(1) memory per user, simpler Redis operations.
  Tradeoff: burst allowance may exceed configured rate by up to bucket capacity (100 requests).

## Blockers
<!-- STANDARD: 3min -->
* BLOCKED: Redis cluster connection pool exhausted at 1000 concurrent users
  RESOLUTION: `redis-cli -h staging-redis CLIENT LIST | grep -c "rate-limiter"` returns < 50
  ETA: 2026-07-25 (ops team provisioning larger instance)
  ESCALATION: If not resolved by 2026-07-26 10:00, ping #infra in Slack

## Next Steps
<!-- STANDARD: 3min -->
1. Complete refillTokens() — expected: unit test passes with simulated time
2. Add response headers — expected: `curl -I /api/test` shows X-RateLimit-* headers
3. Run load test at 500 req/s — expected: p99 < 10ms additional overhead

## Resume Command
<!-- STANDARD: 3min -->
cd /project/backend && git checkout feat/rate-limit && nvim src/middleware/rate-limiter.ts:47

```

## Deliberate Practice
<!-- STANDARD: 3min -->

### Exercise 1: Vague-to-Concrete Conversion (10 min)
Take 3 TODO items from your current project that are vague ("investigate", "look into", "figure out"). Rewrite each as a concrete action with: exact file path, tool/command to run, expected output.

### Exercise 2: Blocker Audit (15 min)
Review your last 5 blocker statements. For each, check: specific resolution condition? ETA? Escalation path? Verifiable with a command? Rewrite any that fail 2+ checks.

### Exercise 3: Restartability Test (20 min)
Produce a handoff for your current work. Swap with a teammate. Time how long it takes them to make their first productive edit. Target: <5 minutes. If longer, identify which handoff field was missing.

### Exercise 4: Ledger Health Retro (10 min)
Run the Ledger Health Check decision tree on your current `.handoff/ledger.md`. Score each TODO, DECIDED, and BLOCKED entry. Fix all FLAG items. Track health score over 1 week.

### Exercise 5: Compaction Drill (15 min)
Simulate context compaction: set a 3-minute timer. Freeze the ledger, generate a handoff summary, and produce a resume command. Then start a fresh session and try to resume. What was missing?

## Best Practices
<!-- STANDARD: 3min -->

1. **Update the ledger after every decision, not at session end.** After 5 turns without an update, 60% of micro-decisions are lost — which dependency version, why approach A over B, what test case was considered. The ledger is the source of truth; trust it over memory.

2. **Write for a fresh agent with zero context.** Assume the receiving agent has never seen this conversation. Every reference must be self-contained: exact file paths with line numbers, complete commands, and rationale for decisions. "Fix the rate limit bug" is useless; "In `src/middleware/rate-limiter.ts:47`, replace `Date.now()` with `performance.now()` from `perf_hooks`" is actionable.

3. **Every decision record must include options, chosen option, rationale, and tradeoffs.** A decision without rationale will be questioned and possibly reversed. Format: "DECIDED: [choice]. Options: [A, B, C]. Chose [X] because [reason]. Tradeoff: [what we gave up]."

4. **Every blocker must have resolution condition, ETA, and escalation trigger.** "Blocked on API team" is not a blocker — it's an abandonment note. Format: "BLOCKED: [what]. RESOLUTION: [verifiable condition]. ETA: [date]. ESCALATION: [if not resolved by X, ping Y]." After 5 days without follow-up, blockers have <20% probability of resolution.

5. **Handoff must be restartable — minimum: cwd, branch, resume command, 3 concrete next steps.** A fresh agent should identify the next action in <60 seconds. Test: can a colleague resume your work from just the handoff document without asking questions?

6. **Cap active TODOs at 5.** A ledger with 40+ TODOs is not a progress tracker — it's a shame list. The receiving agent cherry-picks easy items or freezes. Everything beyond 5 goes to `backlog.md` with priority labels.

7. **Validate the ledger against reality before every handoff.** Run `git diff --stat $(ledger_commit)..HEAD`. If >50 lines changed since the ledger's recorded commit, flag as STALE and rebuild context. A stale ledger gives false confidence — the receiving agent spends 15 minutes orienting to code that has moved on.

8. **Test the resume command in the target environment.** When handing off between different agent types (Claude → Gemini, Copilot → Cursor), assume different tool preferences. A command that works in one agent's toolset may silently fail in another's. Test before finalizing.

9. **Every handoff starts with a 3-sentence context summary.** (1) What problem we're solving, (2) approach chosen and why, (3) current state. This takes 60 seconds to write and saves the receiving agent 15 minutes of orientation.

10. **Archive completed handoffs with a post-mortem note.** When work completes, add a final ledger entry: what shipped, what was deferred, what was learned. This closes the loop and builds institutional knowledge for future similar work.

## Anti-Patterns
<!-- STANDARD: 3min -->

* **The "I'll update the ledger later" trap.** Every turn you skip the ledger update is context that will evaporate on compaction. After 5 turns without a ledger update, 60% of micro-decisions are lost — which dependency version you chose, why you went with approach A over B, what test case you thought of but didn't write yet. **Total cost: $500-$2,000 in rework time per session when a fresh agent must re-discover 5+ lost decisions. Fix: update ledger after every decision, not at session end.**

* **The stale ledger deception.** A ledger last updated 3 days ago gives false confidence — the receiving agent assumes it's current, spends 15 minutes trying to resume, then discovers the code has moved on. A git diff between the ledger's recorded commit and HEAD showing 200+ changed lines means the ledger is archaeological, not operational. **Total cost: $300-$800 per stale-ledger handoff in wasted orientation time and incorrect assumptions. Fix: every handoff starts with `git diff --stat $(ledger_commit)..HEAD` — if >50 lines changed, flag as STALE and rebuild context.**

* **The "too many TODOs" quicksand.** A ledger with 40+ TODO items is not a progress tracker — it's a shame list. The receiving agent cannot prioritize, so they either cherry-pick easy items (ignoring critical path) or freeze (analysis paralysis). **Total cost: $1,000-$3,000 in misdirected effort when the receiving agent works on TODO #37 (low priority) while TODO #2 (blocker for launch) sits untouched. Fix: hard cap of 5 active TODOs. Everything else goes to `backlog.md` with priority labels.**

* **The blocker without teeth.** "Blocked on design review" with no date, no contact, and no escalation path is not a blocker — it's an abandonment note. After 5 business days without follow-up, the probability that anyone remembers what was blocked drops below 20%. **Total cost: $2,000-$10,000 in delayed launches and context-switching when blockers silently expire. Fix: every blocker must have an auto-escalation trigger (e.g., "If no response in 48 hours, escalate to #team-leads").**

* **The "obvious context" assumption.** Writing "continuing the auth refactor" assumes the next agent knows there IS an auth refactor, why it started, what pattern is being followed, and what was tried and rejected. A fresh agent reading that phrase has zero of that context. **Total cost: $400-$1,500 per handoff in re-orientation when the receiving agent must reconstruct the "why" from git history and file comments. Fix: every handoff starts with a 3-sentence context: (1) what problem we're solving, (2) approach chosen and why, (3) current state.**

* **The cross-agent trust gap.** When handing off between different agent types (e.g., Claude → Gemini), assume different training data, different reasoning patterns, and different tool preferences. A command that works in one agent's toolset may silently fail in another's. **Total cost: $500-$2,500 in debugging when the receiving agent runs a handoff command that fails due to tool incompatibility. Fix: test the resume command in the receiving agent's environment before finalizing the handoff.**

## Error Decoder
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Receiving agent spends 20+ minutes orienting before first productive edit | Handoff lacks restartability fields: no cwd, branch, resume command, or concrete next steps. Agent must reconstruct context from git history | Add minimum restartability fields: cwd, branch, resume command with exact file and line, 3 next steps with expected outcomes. Target: <5 minutes to first edit | A handoff without restartability fields is a conversation log, not a handoff. The difference is measured in orientation time — every missing field costs 5 minutes |
| Ledger claims work is in progress but git diff shows 200+ changed lines since recorded commit | Ledger is stale — last updated before significant code changes. The recorded state no longer matches reality | Run `git diff --stat $(ledger_commit)..HEAD` at start of every handoff. Flag as STALE if >50 lines changed. Rebuild context: new commit hash, updated file manifest, current blocker status | A stale ledger is worse than no ledger — it provides false confidence. The receiving agent assumes accuracy and makes incorrect decisions based on outdated state |
| Blocker unresolved after 7+ days with no update | Blocker lacks resolution condition, ETA, and escalation trigger. "Blocked on design review" with no contact is an abandonment note | Retrofit blocker: add specific resolution condition, ETA date, escalation contact. Set auto-reminder. After 5 days without resolution, probability of anyone remembering drops below 20% | Blockers without teeth are abandoned work. Every blocker needs: what must happen to resolve, by when, and who to escalate to if the deadline passes |
| Receiving agent works on low-priority TODOs while launch blocker sits untouched | Ledger has 40+ un-prioritized TODOs. Receiving agent cannot distinguish P0 from P4 without original context | Hard cap: 5 active TODOs with explicit priority (P0-P4). Everything else goes to `backlog.md`. Top 3 TODOs must be ordered by dependency and impact | Too many TODOs is analysis paralysis. The ledger is a progress tracker, not a backlog. Prioritization is the handoff author's responsibility, not the receiver's |
| Decision is reversed in next session because rationale wasn't recorded | Decision recorded as "DECIDED: Used Redis" without options, rationale, or tradeoffs. Receiving agent questions the choice and re-litigates | Format every decision: "DECIDED: [choice]. Options: [A, B, C]. Chose [X] because [reason]. Tradeoff: [what we accepted]." A decision without rationale will be reversed | Decisions decay without rationale. The receiving agent wasn't in the room when the tradeoff was made — if they can't reconstruct the reasoning, they'll make their own choice |
| Cross-agent handoff command fails with tool incompatibility | Resume command uses tool syntax specific to the originating agent (e.g., Claude-specific MCP tools, Copilot-specific flags) | Test the resume command in the target environment before finalizing. Use tool-agnostic commands (`git`, `npm`, `node`) instead of agent-specific wrappers. Document any agent-specific setup needed | Different agents have different tool palettes. A command that works flawlessly in one environment may fail silently in another. Cross-agent handoffs require cross-tool testing |

## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

* [ ] **Workspace exists:** `.handoff/` directory present and git-ignored. Run `ls .handoff/ && grep -q ".handoff/" .gitignore`
* [ ] **Ledger initialized:** `.handoff/ledger.md` has all required sections: Context, Completed, In Progress, Remaining, Decisions, Blockers, Next Steps
* [ ] **Restartability verified:** Handoff contains cwd, branch, resume command, file manifest, and 3 concrete next steps with expected outcomes
* [ ] **Decision coverage complete:** Every non-trivial decision has DECIDED: entry with options, rationale, and tradeoffs
* [ ] **Blocker quality verified:** Every BLOCKED: entry has resolution condition, ETA, and escalation path. Run `grep "BLOCKED:" .handoff/ledger.md | grep -v "RESOLUTION:\|ETA:"` — must return 0
* [ ] **No vague TODOs:** Zero TODOs use "investigate", "look into", "figure out" without concrete commands. Run verification grep
* [ ] **Fresh agent test passed:** A colleague can read the handoff and identify the next action in <60 seconds
* [ ] **Ledger staleness checked:** `git diff --stat $(ledger_commit)..HEAD` shows <50 changed lines. If >50, flag as STALE
* [ ] **Active TODOs capped at 5:** Run `grep -c "TODO:" .handoff/ledger.md` — must be ≤ 5. Overflow goes to `backlog.md`
* [ ] **Decisions include tradeoffs:** Every DECIDED: entry documents what was given up, not just what was chosen
* [ ] **Cross-agent compatibility tested:** Resume command tested in target agent's environment if cross-agent handoff
* [ ] **Ledger committed to session state:** Decision ledger entries synced to `.copilot/session-state/decision-ledger.json` for cross-skill coordination
* [ ] **Verification script passes:** Run `scripts/verify-skill.sh`

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Cramming the handoff into the last 15 minutes of a session | $30K-$100K in duplicate effort and rework | Update the ledger continuously — a 2-minute update after each task prevents 2-hour handoff fire drills |
| Missing context that the next person needs to resume work | $20K-$80K in onboarding delays | Always include the resume command with exact file path and line number plus mental state |
| No decision log leading to repeated debates | $10K-$40K in wasted re-discussion time | Every decision gets a DECIDED: entry with options, choice, rationale, and tradeoffs — even "obvious" ones |

## Verification
<!-- STANDARD: 3min -->

* [ ] **Workspace exists:** `.handoff/` directory present and git-ignored. Run `ls .handoff/ && grep -q ".handoff/" .gitignore`.
* [ ] **Ledger initialized:** `.handoff/ledger.md` has all required sections: Context, Completed, In Progress, Remaining, Decisions, Blockers, Next Steps.
* [ ] **Restartability check:** Handoff contains: cwd, branch, resume command, file manifest, next 3 concrete steps with expected outcomes.
* [ ] **Decision coverage:** Every non-trivial decision has a DECIDED: entry with options, rationale, and tradeoffs. Run `grep -c "DECIDED:" .handoff/ledger.md` — should be >= number of architectural choices made.
* [ ] **Blocker quality:** Every BLOCKED: entry has resolution condition, ETA, and escalation path. Run `grep "BLOCKED:" .handoff/ledger.md | grep -v "RESOLUTION:\|ETA:"` — must return 0.
* [ ] **No vague TODOs:** Zero TODOs use "investigate", "look into", "figure out" without a concrete command. Run `grep -iE "(investigate|look into|figure out)" .handoff/ledger.md | grep -v "grep\|curl\|npm\|cargo\|go "` — must return 0.
* [ ] **Fresh agent test:** A colleague can read the handoff and identify the next action in <60 seconds. If not, add missing context.
* [ ] **Verification script passes:** Run `scripts/verify-skill.sh`. All checks must pass.

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

* [progress-ledger.md](references/progress-ledger.md) — The progress ledger pattern: structure, conventions, and the "trust the ledger over memory" principle
* [handoff-template.md](references/handoff-template.md) — Reusable handoff document template with all required sections and machine-parseable prefixes
* [context-compaction.md](references/context-compaction.md) — What happens during context compaction, what survives, and how to prepare
* [restart-protocol.md](references/restart-protocol.md) — Step-by-step protocol for a fresh agent to resume from a handoff in under 5 minutes
* [decision-capture.md](references/decision-capture.md) — Decision record format: options, rationale, tradeoffs, and the anti-rationalization checklist
* [blocker-documentation.md](references/blocker-documentation.md) — Blocker specification: resolution conditions, ETA enforcement, and escalation paths
* [workspace-setup.md](references/workspace-setup.md) — Setting up `.handoff/` workspace with gitignore, ledger initialization, and directory conventions
* [cross-session-state.md](references/cross-session-state.md) — State preservation across sessions: what to persist, what to rebuild, and ledger index maintenance

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This section documents every irreversible decision made during the session. It is non-negotiable and prevents the agent from revisiting settled questions.

| # | Decision | Rationale | Alternatives Considered | Timestamp |
|---|----------|-----------|------------------------|-----------|
| 1 | *[no decisions logged yet]* | — | — | — |

**Rules:**
* Append a new row for each irreversible or hard-to-reverse decision
* Never modify past rows — only append
* If revisiting a decision, add a NEW row (do not edit the old one)
