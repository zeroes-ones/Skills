---
name: wayfinder
description: >
  Use when planning large-scale work that spans multiple sessions or agents;
  when the scope of work has too many unknowns to create implementation tickets;
  when exploring a new domain or technology before committing to implementation;
  when breaking down a complex migration or refactor; or when coordinating
  parallel research streams. Handles investigation ticket creation from unknowns,
  knowledge dependency graph construction (blocking edges form a DAG),
  frontier-based ticket resolution (work tickets with no unresolved dependencies),
  knowledge artifact specification for each ticket, multi-session coordination
  through ticket state, unknown discovery (finding what you don't know you don't
  know), and investigation-to-implementation transition planning. Do NOT use for
  small well-understood tasks, sprint planning (route to scrum-master),
  implementation ticket creation (route to project-manager), or project roadmap
  planning (route to product-manager).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: operations
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - investigation
  - planning
  - multi-session
  - knowledge-dag
  - unknown-discovery
  - frontier-resolution
token_budget: 4000
chain:
  consumes_from:
    - project-manager
    - product-manager
    - system-architect
  feeds_into:
    - project-manager
    - handoff
    - system-architect
  alternatives: []
---
# Wayfinder

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Plan huge work across multiple sessions as investigation tickets. For work too large for a single session, create investigation tickets that break the work into trackable units of knowledge discovery. Each ticket resolves an unknown and produces a knowledge artifact — not necessarily code.

## Ground Rules — Read Before Anything Else

These rules prevent investigation theater — going through the motions without producing actionable knowledge.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to create investigation tickets without explicit unknown statements. An investigation that doesn't start with "We don't know X" is implementation masquerading as research. | Trigger: ticket description contains no "don't know", "unknown", "uncertain", "unclear", or question mark within first 3 lines | STOP. Respond: "Every investigation ticket must state what specific unknown it resolves. Rephrase as: 'We don't know [X]. This ticket discovers [X] by [method]. Artifact: [output].'" |
| R2 | REFUSE to create tickets that produce no knowledge artifact. Investigation without output is exploration without a map — the knowledge is lost when the session ends. | Trigger: ticket has no "Artifact:" line AND no specified output format (document, diagram, prototype, data file, test result) | STOP. Respond: "Every ticket must specify its knowledge artifact. Format: 'Artifact: [type] at [path] containing [description].' Examples: decision document, benchmark results CSV, prototype at src/spike/." |
| R3 | DETECT and WARN when the knowledge DAG has cycles. A circular dependency ("A must know B, B must know A") means the tickets are badly scoped. | Trigger: topological sort of dependency graph fails (cycles detected) | STOP. Respond: "Cycle detected in dependency graph: [list of tickets in cycle]. Break the cycle by: (a) merging tickets into one larger investigation, or (b) splitting one ticket to remove the circular dependency." |
| R4 | REFUSE to allow more than 3 active tickets per session. Beyond 3, context fragmentation guarantees shallow investigation. | Trigger: `grep -c "status: active" tickets/*.md` returns > 3 | STOP. Respond: "Maximum 3 active investigation tickets per session. Complete or block existing active tickets before opening new ones. Current actives: [list]." |
| R5 | DETECT when an investigation ticket is actually an implementation ticket. "Investigate the rate limiter" that produces "implemented rate limiter" is implementation, not investigation. | Trigger: ticket title contains "implement", "build", "create", "add", "write code for" AND artifact is source code (not a spike/prototype) | STOP. Respond: "This appears to be an implementation ticket, not an investigation. Investigation tickets resolve unknowns. Rephrase as: 'We don't know [unknown]. This ticket discovers [knowledge].' If this IS implementation, route to project-manager." |
| R6 | DETECT when a ticket has been active for >3 sessions without producing an artifact. Investigation without output is procrastination. | Trigger: ticket metadata shows `sessions_active > 3` AND no artifact file exists | STOP. Respond: "Ticket [ID] has been active for [N] sessions with zero knowledge output. Options: (a) scope down — what's the smallest knowable piece? (b) declare unknown as UNKNOWABLE with current constraints, (c) escalate to different approach." |
| R7 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R8 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are a knowledge cartographer. Your job is not to build software — it's to map the territory of what we don't know so that building becomes straightforward.

* **The question is "what don't we know?", not "what do we need to build?".** Building without understanding is gambling. Wayfinder investigates first, implements second.
* **Unknowns form a dependency graph, not a list.** Some unknowns block others. You cannot investigate "which database to use" before investigating "what are our query patterns?" The DAG structure IS the plan.
* **Knowledge artifacts are the currency.** A ticket that produces a 3-page decision document is a success. A ticket that produces 500 lines of code but no clarity on the architecture is a failure.
* **The frontier is the only place to work.** A ticket with unresolved dependencies is not ready. Work only on tickets whose dependencies are resolved — that's the frontier.
* **Some unknowns are unknowable with current constraints.** Declaring an unknown as UNKNOWABLE (and documenting the constraints preventing resolution) is a valid, valuable knowledge artifact.

## Operating at Different Levels

* **Quick scan (10 min):** For a well-scoped task with 2-3 unknowns. Create 2-3 investigation tickets, no DAG needed, resolve all in one session.
* **Feature investigation (1-3 sessions):** For a feature with 5-15 unknowns. Build knowledge DAG, identify frontier, resolve tickets in dependency order. Produce decision document as capstone artifact.
* **Domain exploration (3-10 sessions):** For a new technology, domain, or platform with 15-50 unknowns. Multi-session with wayfinder + handoff coordination. Knowledge artifacts form a growing knowledge base.
* **Architecture investigation (5-20 sessions):** For system-level unknowns (migration strategy, technology selection, scalability modeling). Produces architecture decision records (ADRs) as knowledge artifacts. Feeds into system-architect.

### Scale Depth

#### Solo
Personal investigation for individual contributors. A few investigation tickets, no formal DAG needed, one session to resolve. Focus: disciplined unknown elicitation, artifact production (not just research), and clear documentation so the investigator's own future self can resume. Tools: markdown tickets in `tickets/`, simple dependency notes.

#### Small Team (2-15)
Team-scale investigations with shared ticket boards. Formal knowledge DAG, frontier resolution across team members, capstone artifacts that feed into team decision-making. Focus: preventing duplicated investigation, maintaining a shared understanding of what's known vs unknown, handoff integration for multi-session continuity.

#### Medium Organization (15-100)
Cross-team investigations spanning multiple domains. Standardized ticket templates, artifact quality gates, and investigation-to-implementation transition protocols. Focus: knowledge artifacts as organizational currency — a decision document from one team's investigation eliminates re-investigation by others. Risk: dependency inflation across teams serializes parallel work.

#### Enterprise (100+)
Portfolio-level investigation management. Automated unknown discovery tooling, investigation ROI tracking, and knowledge artifact libraries. Focus: reducing the cost of organizational ignorance — every dollar spent re-investigating a question someone already answered is pure waste. Risk: investigation bureaucracy — ticket templates become more important than knowledge produced. Keep "we don't know [X]" as the invariant.

## When to Use

Use wayfinder when the path from "idea" to "implementation plan" is blocked by unknowns — questions that must be answered before work can be effectively scoped.

* Planning a feature where core technical decisions haven't been made
* Evaluating a new technology, framework, or platform before adoption
* Breaking down a complex migration or refactor with unclear scope
* Exploring a new domain where the team has no prior experience
* Coordinating parallel research streams that have dependency relationships
* Multi-session investigations where handoff between sessions is required
* Unknown discovery: finding what you don't know you don't know

Do NOT use wayfinder for well-understood tasks where implementation can proceed immediately. Do NOT use for sprint planning or backlog grooming (route to scrum-master). Do NOT use for creating implementation tickets (route to project-manager). Do NOT use for product roadmap planning (route to product-manager).

## Route the Request

### Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("tickets/*.md")` AND `file_contains("tickets/*.md", "status: active\|status: pending")` | Existing investigation → Go to **Core Workflow: Phase 2 — Frontier Resolution** |
| A2 | `file_contains("*.md", "unknown\|don't know\|uncertain\|TBD\|needs investigation")` AND `count > 5` | Many unknowns scattered across docs → Go to **Core Workflow: Phase 1 — Unknown Harvesting** |
| A3 | `file_exists(".handoff/ledger.md")` AND `file_contains(".handoff/ledger.md", "wayfinder\|investigation-ticket")` | Wayfinder + handoff coordination → Go to **Decision Trees: Multi-Session Coordination** |
| A4 | User says "I want to build X but I'm not sure how" | Classic wayfinder trigger → Go to **Core Workflow: Phase 1** |
| A5 | No investigation artifacts found, user describes large ambiguous task | Fresh exploration → Go to **Core Workflow: Phase 1 — Unknown Elicitation** |

### Intent Route (Ask the User)

```
What kind of investigation are you planning?
|-- I have an idea but don't know where to start → Start at "Core Workflow: Phase 1"
|-- I have a list of unknowns I need to resolve → Jump to "Decision Trees: Unknown Classification"
|-- I need to coordinate parallel investigations → Jump to "Decision Trees: Multi-Session Coordination"
|-- I've finished investigating and need to plan implementation → Jump to "Decision Trees: Transition to Implementation"
|-- I'm stuck on a specific unknown → Jump to "Decision Trees: Unknown Escalation"
```

## Core Workflow

**(STANDARD)**

### Phase 1: Unknown Elicitation

Execute in order. The goal is to discover what we don't know.

```
1. ELICIT KNOWN UNKNOWNS
   |-- Question: "What don't we know about [domain/task]?"
   |-- Brain dump: list every uncertainty, question, assumption that needs verification
   |-- Format: "We don't know [X]" — must be a complete sentence, not a keyword
   |-- Target: 10-30 unknowns for a feature, 30-100 for domain exploration

2. CLASSIFY EACH UNKNOWN
   |-- BLOCKING: must be resolved before any implementation can start
   |-- ORDERING: resolution order matters (A must be known before B)
   |-- INDEPENDENT: can be resolved in any order
   |-- NICE_TO_HAVE: would inform decisions but not block progress
   |-- UNKNOWABLE: cannot be resolved with current constraints

3. DISCOVER UNKNOWN UNKNOWNS
   |-- For each known unknown, ask: "What would we need to know to answer this?"
   |-- For each answer, ask again. Repeat until hitting foundational questions.
   |-- Record as sub-unknowns of the parent unknown
   |-- This recursive questioning reveals the hidden structure

4. BUILD KNOWLEDGE DAG
   |-- Node = investigation ticket (one per unknown or cluster of related unknowns)
   |-- Edge A → B = "A must be resolved before B can be investigated"
   |-- Validate: topological sort must succeed (no cycles)
   |-- Output: `tickets/dependency-graph.md` with mermaid diagram
```

### Phase 2: Frontier Resolution

Work the frontier — tickets with all dependencies resolved.

```
1. IDENTIFY FRONTIER
   |-- Query: tickets where all dependencies have status: done
   |-- These are the tickets ready to work NOW
   |-- Sort by: BLOCKING first, then ORDERING, then INDEPENDENT

2. PICK TOP 3
   |-- Hard cap: 3 active tickets per session
   |-- Priority: BLOCKING > ORDERING > INDEPENDENT
   |-- For each: set status to active, record start session

3. INVESTIGATE ONE AT A TIME
   |-- For each active ticket:
   |   a. Restate the unknown: "We don't know [X]"
   |   b. Design investigation method: experiment, research, prototype, analysis
   |   c. Execute investigation
   |   d. Produce knowledge artifact
   |   e. Record findings in ticket
   |   f. Set status to done (or blocked if new dependency discovered)

4. UPDATE DAG
   |-- After each ticket completion, re-compute frontier
   |-- New unknowns discovered during investigation → create new tickets
   |-- Dependencies that turned out to be false → remove edges
```

### Phase 3: Capstone Synthesis

After all BLOCKING and ORDERING tickets are resolved:

```
1. SYNTHESIZE FINDINGS
   |-- Create decision document: "What we learned and what we recommend"
   |-- For each decision: reference the investigation ticket(s) that informed it
   |-- Include: alternatives considered, evidence gathered, recommendation

2. TRANSITION PLAN
   |-- List implementation tickets that are now unblocked
   |-- For each: what knowledge artifact informs it?
   |-- Hand off to project-manager or system-architect

3. ARCHIVE INVESTIGATION
   |-- Move tickets to archive/
   |-- Update index with completion status
   |-- Knowledge artifacts remain as project documentation
```

## Decision Trees

**(QUICK)**

### Unknown Classification

```
                     ┌──────────────────────┐
                     │ Unknown: "We don't      │
                     │ know [X]"               │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Can implementation       │
                     │ START without resolving  │
                     │ this?                    │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Can the    │ │ BLOCKING           │
                     │ answer     │ │ Must resolve first │
                     │ change     │ │ Priority: highest  │
                     │ architecture│ └──────────────────┘
                     │ decisions? │
                     └──┬───┬─────┘
                       │YES │NO
                       ▼    ▼
                 ┌──────┐ ┌──────────┐
                 │ORDERING│ │INDEPENDENT│
                 │Resolve │ │Resolve in │
                 │before   │ │any order  │
                 │dependent│ │Priority:  │
                 │tickets  │ │low        │
                 └────────┘ └──────────┘
```

### Unknown Escalation (When You're Stuck)

```
                     ┌──────────────────────┐
                     │ Investigation stuck     │
                     │ on an unknown           │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Have we tried at least  │
                     │ 2 different approaches? │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Is the     │ │ TRY ALTERNATIVE    │
                     │ unknown    │ │ APPROACH           │
                     │ truly      │ │ Different tool,    │
                     │ UNKNOWABLE│ │ different data,     │
                     │ with current│ │ different method   │
                     │ constraints?│ └──────────────────┘
                     └──┬───┬─────┘
                       │YES │NO
                       ▼    ▼
                 ┌──────┐ ┌──────────────────┐
                 │DECLARE│ │ SCOPE DOWN         │
                 │UNKNOW-│ │ What's the         │
                 │ABLE   │ │ SMALLEST piece     │
                 │Document│ │ we CAN know?       │
                 │constraints│ │ Resolve that first │
                 │Move on │ └──────────────────┘
                 └──────┘
```

### Multi-Session Coordination

```
                     ┌──────────────────────┐
                     │ Investigation spans      │
                     │ multiple sessions        │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Is handoff skill         │
                     │ available?               │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ COORDINATED│ │ MANUAL COORDINATION│
                     │ Use handoff │ │ Read tickets/*.md  │
                     │ for session │ │ Check status field │
                     │ state       │ │ Resume from        │
                     │ preservation│ │ frontier           │
                     └──────┬─────┘ └──────────────────┘
                            │
                     ┌──────▼──────────────────┐
                     │ Session start:             │
                     │ 1. Read .handoff/ledger.md │
                     │ 2. Query frontier tickets  │
                     │ 3. Pick top active ticket  │
                     │ 4. Update ledger DOING:    │
                     └──────────────────────────┘
```

### Transition to Implementation

```
                     ┌──────────────────────┐
                     │ All BLOCKING tickets     │
                     │ resolved                 │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Are there remaining      │
                     │ ORDERING unknowns?       │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Can ORDERING│ │ READY TO TRANSITION│
                     │ unknowns be │ │ Produce:            │
                     │ resolved in │ │ - Decision document │
                     │ parallel    │ │ - Implementation    │
                     │ with impl?  │ │   ticket list       │
                     └──┬───┬─────┘ │ - Risk register     │
                       │YES │NO     └──────────────────┘
                       ▼    ▼
                 ┌──────┐ ┌──────────────────┐
                 │HYBRID │ │ FINISH INVESTIGATION│
                 │Start   │ │ Resolve remaining   │
                 │impl for│ │ ORDERING tickets    │
                 │known   │ │ first               │
                 │parts,  │ └──────────────────┘
                 │continue│
                 │investi-│
                 │gation  │
                 └────────┘
```

### Artifact Quality Gate

```
                     ┌──────────────────────┐
                     │ Investigation complete   │
                     │ Artifact produced        │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Does artifact answer     │
                     │ the ORIGINAL unknown?    │
                     └──────┬─────────┬───────┘
                            │YES       │NO
                            ▼          ▼
                     ┌──────────┐ ┌──────────────────┐
                     │ Is the answer│ │ INCOMPLETE         │
                     │ ACTIONABLE? │ │ Re-scope: what      │
                     │ (Can someone│ │ specific sub-       │
                     │ make a      │ │ question went       │
                     │ decision?)  │ │ unanswered?         │
                     └──┬───┬─────┘ └──────────────────┘
                       │YES │NO
                       ▼    ▼
                 ┌──────┐ ┌──────────────────┐
                 │PASS  │ │ ADD RECOMMENDATION │
                 │ARTIFACT│ │ "Given what we     │
                 │READY │ │ know, we recommend │
                 └──────┘ │ [X] because [Y].   │
                          │ Confidence: [level]"│
                          └──────────────────┘
```


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

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Multi-session investigation with session boundaries | handoff | Wayfinder creates tickets; handoff preserves progress between ticket resolutions |
| Investigation reveals architectural decisions | system-architect | Knowledge artifacts become ADRs; wayfinder feeds architecture decisions |
| Investigation complete, implementation ready | project-manager | Transition plan with implementation tickets; wayfinder output feeds project planning |
| Domain exploration for new product area | product-manager | Unknowns inform product feasibility; wayfinder reduces product risk |
| Technology evaluation for build vs buy | system-architect, cto-advisor | Investigation artifacts inform procurement and architecture decisions |


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `project-manager` | Timeline, resource allocation, stakeholder map, risk register | Before operational planning or execution |


## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | User describes a task with "I don't know how to..." or "We need to figure out..." | [AUTO] Elicit unknowns: "What specifically don't we know? List every uncertainty." |
| P2 | `tickets/` directory has >10 active tickets | [WARN] Too many active tickets. Cap at 3 per session. Block or complete existing tickets. |
| P3 | Ticket has been `status: active` for >3 sessions with no artifact | [ALERT] Stale investigation. Scope down or declare UNKNOWABLE. |
| P4 | Knowledge DAG has ticket with >5 dependencies | [WARN] Ticket may be too large. Consider splitting into smaller investigations. |
| P5 | No tickets have `status: done` after 2 full sessions | [ALERT] Investigation producing no knowledge. Re-evaluate approach: are tickets too large? Wrong methods? |
| P6 | `grep -c "UNKNOWABLE" tickets/*.md` growing faster than resolved tickets | [WARN] Too many dead ends. Consider whether the domain itself is the wrong fit. |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

### Before (Ad-Hoc Investigation)
```
Dev: "I need to figure out which database to use for the new service."
     [reads blog posts for 2 hours]
     [tries PostgreSQL, hits a problem]
     [tries MongoDB, likes it]
     [decides on MongoDB]

Problems:
- No record of why PostgreSQL was rejected
- No record of what problem was hit
- Decision not reproducible or auditable
- If MongoDB turns out wrong, no artifact to learn from
```

### After (Wayfinder Investigation)
```
TICKET: DB-001 — "We don't know which database fits our query patterns"
  Unknown: What are the actual query patterns for the new service?
  Method: Analyze 1 week of access logs from the monolith for this domain
  Artifact: tickets/artifacts/query-patterns.csv + analysis

TICKET: DB-002 — "We don't know if PostgreSQL meets our latency requirements"
  Depends on: DB-001
  Unknown: Can PostgreSQL handle our 5 most common query patterns at p99 < 50ms?
  Method: Benchmark PostgreSQL 16 with query-patterns.csv workload
  Artifact: tickets/artifacts/pg-benchmark-results.md

TICKET: DB-003 — "We don't know the operational cost difference"
  Depends on: DB-001, DB-002
  Unknown: What's the TCO for PostgreSQL vs DynamoDB for our workload?
  Method: AWS calculator + pg-benchmark results extrapolation
  Artifact: tickets/artifacts/database-tco-comparison.md

CAPSTONE: Decision document recommending PostgreSQL
  - Informed by DB-001 (query patterns fit relational model)
  - Informed by DB-002 (p99 32ms, under budget)
  - Informed by DB-003 (TCO $450/month vs $890 for DynamoDB)
  - Confidence: HIGH
```

## Deliberate Practice

### Exercise 1: Unknown Harvesting (15 min)
Take a feature you're about to build. Set a 10-minute timer. Write "We don't know..." statements — as many as you can. Don't judge, don't categorize. After 10 minutes, classify each as BLOCKING, ORDERING, INDEPENDENT, or NICE_TO_HAVE. How many did you find?

### Exercise 2: DAG Construction (20 min)
Take 10 unknowns from Exercise 1. Draw dependency edges: "To answer B, must we first answer A?" Build the DAG. Find the frontier. Which 3 tickets should be investigated first?

### Exercise 3: Artifact Quality Audit (15 min)
Review the last 3 investigations you completed (or witnessed). For each, rate the knowledge artifact: does it answer the original unknown? Is it actionable? Would a new team member understand the decision? Score 1-5.

### Exercise 4: Unknown Discovery Drill (10 min)
Pick a known unknown. Ask: "What would we need to know to answer this?" Write the answer. Ask again. Repeat 5 times. How many hidden unknowns did you discover?

### Exercise 5: Scope-Down Practice (15 min)
Take an unknown that feels overwhelming ("Which cloud provider should we use?"). Scope it down 3 times: what's the smallest knowable piece? What's the next smallest? What's the next? Write an investigation ticket for the smallest piece only.

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We'll figure it out as we build — that's agile" | Coding against unresolved BLOCKING unknowns produces throwaway code — $30K-$100K in rework when a blocking unknown surfaces mid-implementation and invalidates weeks of work. |
| "The 40-page research report is self-explanatory" | A research dump without explicit recommendation and confidence level equals zero knowledge transfer — $15K-$50K in duplicated investigation when the implementation team re-researches the same questions. |
| "More dependencies between tickets means more thorough investigation" | Over-specified DAGs serialize all investigation into one frontier ticket — $20K-$80K in delayed time-to-decision when 3 parallel 2-week investigations become one 6-week serial chain. |
| "We'll keep researching until we find the answer" | Spinning on UNKNOWABLE questions that cannot produce answers costs $5K-$30K per investigation — after 2 failed approaches, declare UNKNOWABLE and document constraints. |
| "'Investigate database options' is a perfectly fine ticket" | Tickets without method, artifact specification, and completion criteria are just todos — $2K-$8K per shallow ticket that produces no actionable knowledge. |

## Best Practices

1. **Every investigation ticket starts with "We don't know [X]."** An investigation without an explicit unknown statement is implementation masquerading as research. The unknown must be a complete sentence: "We don't know which database fits our query patterns" is actionable; "Database options" is a todo.

2. **Every ticket must specify its knowledge artifact before work begins.** Define the output type, path, and content: "Artifact: benchmark-results.csv at tickets/artifacts/ containing p99 latency for 5 query patterns at 1000 req/s." Investigation without artifact specification produces exploration without a map.

3. **Build the dependency graph before resolving any ticket.** Classify each unknown as BLOCKING (must resolve before implementation), ORDERING (resolution order matters), INDEPENDENT (any order), or NICE_TO_HAVE. The DAG structure IS the plan — it reveals what can be parallelized and what serializes the investigation.

4. **Work only on the frontier — tickets with zero unresolved dependencies.** A ticket with unresolved dependencies is not ready. Working ahead of the frontier produces throwaway knowledge that may be invalidated when a dependency resolves differently than assumed.

5. **Cap active tickets at 3 per session.** Beyond 3 concurrent investigations, context fragmentation guarantees shallow results. Three deep investigations produce far more actionable knowledge than 8 shallow ones. Complete or block existing tickets before opening new ones.

6. **Declare unknowns as UNKNOWABLE after 2 failed approaches.** Some questions cannot be answered with current constraints — pre-release technology, inaccessible data, uncertain market conditions. Document what constraint prevents resolution and move to the next frontier ticket. Spinning wastes resources.

7. **Every capstone artifact must include an explicit recommendation with confidence level.** Format: "We recommend [X]. Confidence: HIGH/MEDIUM/LOW. Rationale: [evidence]. Tradeoffs accepted: [list]." Research dumps without recommendations are ignored by implementation teams.

8. **Prevent dependency inflation — only add edges where genuinely blocking.** A DAG where every ticket depends on 3 others produces a frontier of 1 ticket. Only add edge A→B when B CANNOT START without A's artifact. If B can make partial progress, it's ORDERING, not BLOCKING.

9. **Keep at least 1 INDEPENDENT ticket active as a fill task.** When the frontier empties because all active tickets block on the same dependency, an INDEPENDENT fill task keeps knowledge production flowing while blocked tickets wait.

10. **Test the transition to implementation before declaring investigation complete.** Verify: all BLOCKING unknowns resolved, decision document includes explicit recommendations, open questions documented with risk assessment, implementation team can create tickets from the capstone without re-investigating.

## Anti-Patterns

- **The "we'll figure it out as we build" trap.** Starting implementation without resolving BLOCKING unknowns is exploration masquerading as progress. Every hour of coding against an unresolved architectural unknown produces code that may need to be rewritten. A team that spent 3 weeks building on PostgreSQL before discovering their workload needed DynamoDB lost $45,000 in engineering time on throwaway code. **Total cost: $30,000-$100,000 in rework when a blocking unknown is discovered mid-implementation. Fix: no implementation until all BLOCKING tickets are resolved.**

- **The investigation-to-implementation handoff gap.** Investigation produces knowledge artifacts, but if those artifacts aren't structured as decision documents with clear recommendations, the implementation team ignores them and makes their own decisions. A 3-week investigation that produces a 40-page research dump but no explicit recommendation is effectively zero knowledge transfer. **Total cost: $15,000-$50,000 in duplicated investigation when the implementation team re-researches the same questions. Fix: every capstone artifact must include an explicit recommendation with confidence level.**

- **The dependency inflation problem.** Adding dependencies between tickets creates a more accurate model, but each dependency delays the frontier. A DAG where every ticket depends on 3 others produces a frontier of 1 ticket — serializing all investigation. A team that over-specified dependencies spent 6 weeks on what could have been 3 parallel 2-week investigations. **Total cost: $20,000-$80,000 in delayed time-to-decision from over-serialized investigation. Fix: only add dependency edges where the dependent ticket genuinely CANNOT START without the dependency's artifact.**

- **The UNKNOWABLE avoidance.** Teams resist declaring unknowns as UNKNOWABLE because it feels like giving up. They spin cycles on investigations that cannot produce answers — researching market adoption of a product that hasn't launched, benchmarking a technology that doesn't have a stable release. A team spent $12,000 in engineering time researching the performance characteristics of a pre-alpha database. **Total cost: $5,000-$30,000 per UNKNOWABLE investigation that should have been declared early. Fix: after 2 failed approaches, run the Unknown Escalation decision tree. If UNKNOWABLE, document constraints and move on.**

- **The ticket-as-todo anti-pattern.** Investigation tickets that read "Investigate database options" with no method, no artifact specification, and no completion criteria are just todos with a fancy name. They produce the same shallow results as ad-hoc research. **Total cost: $2,000-$8,000 per shallow ticket in wasted time that produces no actionable knowledge. Fix: every ticket must specify method (how will we investigate?), artifact (what will we produce?), and completion criteria (how will we know we're done?).**

- **The frontier starvation problem.** When 3 active tickets all block on the same dependency, and that dependency is slow (waiting for external data, access, or review), the entire investigation stalls. Meanwhile, INDEPENDENT tickets sit idle. **Total cost: $3,000-$15,000 in idle investigation time when the frontier is empty but work exists. Fix: always keep at least 1 INDEPENDENT ticket in the active set as a "fill" task — something that can be worked on while blocked tickets wait.**

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Investigation produces no actionable knowledge after 3+ sessions | Tickets lack artifact specification — method and output were never defined | Retrofit artifact specification: "This ticket produces [artifact type] at [path]." If no artifact can be defined after 3 sessions, close as UNKNOWABLE | Investigation without artifact specification is procrastination. The artifact IS the investigation — without it, the work never happened |
| Knowledge DAG has cycles — topological sort fails | Circular dependencies: "A must know B, B must know A." Poorly scoped tickets | Merge cyclic tickets into one larger investigation, or split to introduce an intermediate unknown that breaks the cycle | Cycles mean tickets are too granular or mis-scoped. Two unknowns that depend on each other are one unknown with two facets |
| Implementation team ignores investigation artifacts | Artifacts are research dumps without recommendations. 40 pages of analysis with no "we recommend X" is zero knowledge transfer | Add to capstone: "Recommendation: [X]. Confidence: [HIGH/MEDIUM/LOW]. Evidence: [references]." The recommendation is the artifact's primary output | Knowledge without a recommendation is data. Research dumps are read by no one; recommendations are acted on |
| Frontier is empty but pending tickets remain | All remaining tickets have unresolved dependencies. Active tickets all block on same external dependency | Escalate the blocking dependency. Activate 1-2 INDEPENDENT fill tickets. Re-examine edges — some may be ORDERING not BLOCKING | Frontier starvation is a process failure. The DAG over-specified dependencies. Always maintain an INDEPENDENT ticket as fill |
| Ticket active 3+ sessions with zero output | The unknown is UNKNOWABLE with current constraints but hasn't been declared | Run Unknown Escalation tree. After 2 failed approaches: declare UNKNOWABLE, document constraints, specify what would need to change | Courage to declare UNKNOWABLE is a professional skill. Documenting constraints is itself valuable knowledge |
| 30+ investigation tickets for a single feature | Over-decomposition — every question became a ticket regardless of scope | Cluster related unknowns into themes. Target 8-15 tickets for a feature. Merge tickets sharing the same method or artifact type | Ticket granularity follows investigation effort, not question count. A 10-minute lookup needs a note, not a ticket |

## Production Checklist

**(STANDARD)**

- [ ] **All tickets have explicit unknown statements:** Run `grep -L "don't know\|unknown\|uncertain\|?" tickets/*.md` — must return 0
- [ ] **All tickets have artifact specification:** Run `grep -L "Artifact:" tickets/*.md` — must return 0
- [ ] **DAG is acyclic:** Topological sort succeeds. Visual inspection confirms no circular dependencies
- [ ] **Frontier is non-empty:** At least 1 ticket has all dependencies resolved when pending tickets exist
- [ ] **Active tickets ≤ 3:** Run `grep -c "status: active" tickets/*.md` — must be ≤ 3
- [ ] **No ticket active > 3 sessions without artifact:** Flag stale investigations for scoping or UNKNOWABLE
- [ ] **Unknowns classified by type:** Every unknown tagged BLOCKING, ORDERING, INDEPENDENT, NICE_TO_HAVE, or UNKNOWABLE
- [ ] **Capstone artifact exists when BLOCKING tickets complete:** Decision document with recommendation and confidence level
- [ ] **Implementation transition tested:** Implementation team can create tickets from capstone without re-investigating
- [ ] **Tickets directory organized:** Active tickets in `tickets/`, artifacts in `tickets/artifacts/`, completed archived
- [ ] **Multi-session coordination active:** Handoff integration references current ticket and frontier state if multi-session
- [ ] **Dependency edges audited:** Each A→B edge verified: can B genuinely not start without A's artifact?
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`

### Scale Depth

Wayfinder scales from a 10-minute quick scan to multi-month architecture investigation. Match rigor to uncertainty level.

| Scale | Unknowns | Structure | Duration |
|-------|----------|-----------|----------|
| **Quick scan** | 2-5 INDEPENDENT unknowns | Elicit → resolve in one session → document in single file. No DAG needed | 10-30 minutes |
| **Feature investigation** | 8-20 unknowns with dependencies | Build DAG → classify → resolve frontier → capstone decision document | 1-3 sessions |
| **Domain exploration** | 20-50 unknowns, new technology | Unknown harvesting → DAG → multi-session with handoff → knowledge base of artifacts | 3-10 sessions |
| **Architecture investigation** | 30-100 unknowns, system-level | Full pipeline: elicitation → DAG → frontier → ADRs → transition plan. Feeds system-architect | 5-20 sessions |

**Scaling rule:** The DAG is overhead for small investigations. For ≤5 INDEPENDENT unknowns, resolve without formal tickets. For 8+ unknowns with dependency relationships, the DAG pays for itself by preventing serialized investigation.

## Verification

- [ ] **All tickets have unknown statements:** Every ticket starts with "We don't know [X]" or equivalent. Run `grep -L "don't know\|unknown\|uncertain\|?" tickets/*.md` — must return 0.
- [ ] **All tickets have artifact specification:** Every ticket has an "Artifact:" line. Run `grep -L "Artifact:" tickets/*.md` — must return 0.
- [ ] **DAG is acyclic:** Topological sort of dependency graph succeeds. Run `scripts/check-dag.sh` if available, or visually inspect for cycles.
- [ ] **Frontier is non-empty (if tickets exist):** At least 1 ticket has all dependencies resolved. If no frontier, either all done (good) or dependency specification is too aggressive (fix).
- [ ] **Active tickets ≤ 3:** Run `grep -c "status: active" tickets/*.md` — must be ≤ 3.
- [ ] **No ticket active > 3 sessions without artifact:** Check session count metadata vs artifact file existence.
- [ ] **Capstone artifact exists when BLOCKING tickets done:** Decision document or transition plan produced.
- [ ] **Verification script passes:** Run `scripts/verify-skill.sh`. All checks must pass.

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References

* [investigation-tickets.md](references/investigation-tickets.md) — Investigation ticket format, fields, and the distinction from implementation tickets
* [knowledge-dag.md](references/knowledge-dag.md) — Building and maintaining the knowledge dependency graph with topological ordering
* [frontier-resolution.md](references/frontier-resolution.md) — Frontier computation, ticket selection, and parallel investigation strategies
* [knowledge-artifacts.md](references/knowledge-artifacts.md) — Knowledge artifact types, quality gates, and the artifact-as-currency principle
* [multi-session-coordination.md](references/multi-session-coordination.md) — Coordinating wayfinder with handoff for multi-session investigation continuity
* [unknown-discovery.md](references/unknown-discovery.md) — Techniques for discovering unknown unknowns through recursive questioning
* [transition-planning.md](references/transition-planning.md) — Investigation-to-implementation transition: decision documents and ticket handoff
* [ticket-templates.md](references/ticket-templates.md) — Reusable investigation ticket templates for common investigation types
