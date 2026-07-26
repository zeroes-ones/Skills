---
name: agent-handoff-protocol
description: Use when building multi-agent pipelines, passing state between specialized
  agents, or designing cross-agent orchestration. Handles state serialization, context
  pruning, decision gate ledgers, handoff contracts, multi-agent topology selection,
  and context rot defense. Do NOT use for single-agent workflows, simple sequential
  scripts without state passing, or non-AI pipeline orchestration (use ci-cd-builder
  for CI/CD).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: framework
status: stable
version: 1.0.0
updated: 2026-07-24
tags:
- agent
- handoff
- state
- orchestration
- multi-agent
token_budget: 4000
chain:
  consumes_from:
  - agent-eval-pipeline
  - multi-agent-orchestration
  feeds_into:
  - backend-developer
  - system-architect
  - devops-engineer
  - security-engineer
---
# Agent Handoff Protocol

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Framework for serializing agent state, pruning context, recording decisions, and enforcing contracts between specialized agents in multi-agent pipelines. Designed for production use with LangGraph, CrewAI, and AutoGen patterns.

---

## Route the Request

Every request enters through the auto-router. Match the intent to the anchor below. If nothing matches, escalate to human.

### Auto-Route Table (A1–A8)

| ID | Intent Pattern | Route To |
|----|---------------|----------|
| A1 | "handoff state from X to Y" / "serialize context for next agent" | [Core Workflow → Phase 1: Serialize](#core-workflow) |
| A2 | "what should I prune?" / "context too large for next agent" | [Core Workflow → Phase 2: Prune](#core-workflow) |
| A3 | "record this decision" / "log the architecture choice" | [Core Workflow → Phase 3: Record Decision Gate](#core-workflow) |
| A4 | "create handoff contract" / "what does agent X owe agent Y?" | [Core Workflow → Phase 4: Sign Contract](#core-workflow) |
| A5 | "which topology should I use?" / "supervisor vs peer vs debate" | [Decision Tree 4: Multi-Agent Topology Selection](#decision-trees) |
| A6 | "agents disagree on X" / "resolve conflict between agents" | [Decision Tree 5: Conflict Resolution](#decision-trees) |
| A7 | "is this handoff ready?" / "verify state before passing" | [Verification Checklist](#verification) |
| A8 | "context is corrupt after N handoffs" / "decisions contradict" | [Context Rotation Defense Patterns](#references) |

### Intent Route Tree

```
Incoming request
├─ Contains "handoff" OR "pass to" OR "next agent"?
│  ├─ Yes → Is state already serialized?
│  │  ├─ Yes → A7 (verify) → then A2 (prune) → then A4 (contract) → deliver
│  │  └─ No  → A1 (serialize) → A3 (record decisions) → A2 (prune) → A4 (contract)
│  └─ No  → Continue
├─ Contains "topology" OR "supervisor" OR "peer" OR "debate" OR "swarm"?
│  └─ Yes → A5 (select topology)
├─ Contains "disagree" OR "conflict" OR "contradict"?
│  └─ Yes → A6 (resolve conflict)
├─ Contains "corrupt" OR "stale" OR "drift" OR "rot"?
│  └─ Yes → A8 (context rot defense)
└─ No match → Escalate to human with suggested route
```

---

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|--------------------|
| R1 | Must NOT pass handoff with `token_budget_after` > 12,000 | Token counter exceeds threshold during serialization | Re-run pruning with stricter rules; if still over, mark handoff `blocked` |
| R2 | Must NOT drop `non_negotiable: true` constraints | Constraint count in handoff < constraint count in previous handoff | Reject handoff; diff constraints; restore missing before proceeding |
| R3 | Must NOT hand off to self (`origin_skill` = `target_skill`) | Serializer detects self-loop | Abort serialization; escalate to pipeline supervisor |
| R4 | Must NOT accept handoff with checksum mismatch | SHA-256 of received state ≠ recorded checksum | Reject handoff; request re-transmission from upstream agent |
| R5 | Must NOT make irreversible decisions without ledger entry | Decision gate recorded with `reversible: false` but no ledger row | Block handoff; require ledger entry before proceeding |
| R6 | Must NOT hand off with >3 unresolved open questions | `open_questions.length > 3` at serialization time | Pause pipeline; escalate to human or supervisor agent |
| R7 | Must NOT hand off without verifying all downstream contracts accepted | Handoff contract in `PROPOSED` state (not `ACCEPTED`) | Block delivery; wait for downstream `ACCEPTED` or `REJECTED` |
| R8 | Must NOT override prior agent's decision without marking it SUPERSEDED | Ledger shows same gate with different choice, no SUPERSEDED marker | Reject override; require explicit SUPERSEDED entry with rationale |
| R9 | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| R10 | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

---


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

| Bias | Trap | Why It Hurts Handoffs | Correction |
|------|------|-----------------------|------------|
| **Completeness Bias** | "I'll pass everything — they can filter" | Bloats token budget, buries signal in noise | Progressive disclosure: Tier 1 always, Tier 2 on demand, Tier 3 never auto |
| **Recency Bias** | "My decisions are the important ones" | Downstream agents inherit confidence without context from upstream | Confidence decay: each handoff drops confidence one level |
| **Ownership Bias** | "The next agent will figure out the gaps" | Open questions accumulate, compound uncertainty, pipeline stalls | Max 3 open questions rule; beyond that, escalate |
| **Simplicity Bias** | "One handoff format fits all pipelines" | Wrong topology, wrong pruning rules, wrong contract shape | Topology-aware serialization: different pipelines need different formats |
| **Finality Bias** | "Once I decide, it's settled" | Irreversible decisions recorded too early block flexibility | Every decision must declare `reversible` and `cost_of_reversal` |
| **Trust Bias** | "Downstream agents will respect my constraints" | Non-negotiable constraints silently dropped | Checksum chain + constraint inheritance audit on every handoff |

---

## Operating at Different Levels

| Level | Name | When to Operate Here | Key Move | Token Budget | Example |
|-------|------|---------------------|----------|-------------|---------|
| L1 | **Single Handoff** | Quick pass between 2 agents, simple pipeline | Serialize state → prune → sign contract → deliver | ~500 | "System architect hands off ADRs to backend developer" |
| L2 | **Linear Pipeline** | Sequential chain of 3-5 agents, each building on previous | Supervisor topology, sequential handoffs, ledger continuity check | ~1,500 | "Business → Architecture → Development → DevOps → Security" |
| L3 | **Branching Pipeline** | One agent feeds multiple downstream agents in parallel | Hierarchical topology, parallel handoffs, artifact sharing via `~/.agents/artifacts/` | ~3,000 | "Architecture feeds Dev, DevOps, and Security simultaneously" |
| L4 | **Collaborative Mesh** | Agents need bidirectional feedback, peer review cycles | Peer-to-peer topology, bidirectional contracts, debate gates for conflicts | ~5,000 | "Frontend lead and backend lead negotiate API contract" |
| L5 | **Swarm Exploration** | Many agents explore in parallel, merge results downstream | Swarm topology, shared state with conflict resolution, merge agent | ~8,000 | "5 agents review 5 microservices, merge findings into audit report" |

---

## When to Use

| Trigger | Scenario | Which Level | Expected Output |
|---------|----------|-------------|-----------------|
| Multi-agent pipeline being designed | You need 3+ agents to collaborate on one deliverable | L2-L3 | Topology selection + handoff format + contract templates |
| Context too large for next agent | Token budget exceeds downstream agent's capacity | L1 | Pruned state with `token_budget_after` < 12,000 |
| Decision needs to survive 3+ handoffs | Architecture choice must be honored by all downstream agents | L2 | Decision gate ledger entry + constraint object |
| Agents producing contradictory outputs | Two agents make conflicting choices on same gate | L4 | Conflict resolution via debate topology or escalation |
| Pipeline audit required | Need to trace why agent Z made choice X | L2-L5 | Full decision gate ledger with chain of custody |
| Context degradation detected | After 5+ handoffs, agents make errors from stale context | L3-L5 | Context rot defense: re-origin, checksum verification, rollback |
| Cross-skill contract negotiation | Agent A needs Agent B to deliver specific artifacts | L1 | Signed handoff contract with acceptance criteria |

---

## Core Workflow

### Phase 1: Serialize State

Before any handoff, serialize the current agent's complete state into the standard JSON format.

```json
{
  "handoff_version": "1.0.0",
  "pipeline_id": "uuid",
  "origin_skill": "system-architect",
  "target_skill": "backend-developer",
  "created_at": "ISO8601",
  "decisions": [
    {
      "gate": "architecture-pattern",
      "choice": "event-driven-microservices",
      "rationale": "Team has Kafka expertise; system requires >10K events/sec; async boundaries align with domain seams",
      "rejected_alternatives": ["monolith", "modular-monolith"],
      "confidence": "high",
      "reversible": false,
      "timestamp": "ISO8601"
    }
  ],
  "artifacts": [
    {"type": "adr", "path": "decisions/001-use-kafka.md", "status": "approved", "checksum": "sha256..."},
    {"type": "spec", "path": "specs/order-service-openapi.yaml", "status": "draft", "checksum": "sha256..."}
  ],
  "constraints": [
    {"type": "technology", "value": "Must use PostgreSQL 15+", "source": "architect-decision", "non_negotiable": true},
    {"type": "compliance", "value": "GDPR data residency: EU-only", "source": "legal-review", "non_negotiable": true}
  ],
  "context_pruned": {
    "removed_sections": ["business-strategy-details", "ceo-communication-style"],
    "token_budget_before": 28000,
    "token_budget_after": 8500,
    "pruning_rules_applied": ["remove-strategy-layer", "keep-constraints-only"]
  },
  "open_questions": [
    {"question": "Should we use NestJS or Express?", "assigned_to": "backend-developer", "deadline": "2 days"}
  ]
}
```

**Checkpoint:** Is `handoff_version` compatible with target agent? Is `pipeline_id` consistent?
  Complete when: Handoff JSON is valid, handoff_version matches target agent compatibility matrix, and pipeline_id is consistent across the chain.

### Phase 2: Prune Context

Apply pruning rules from [Context Pruning Rules](references/context-pruning-rules.md) based on pipeline stage.

**Pruning algorithm:**
```
1. Identify target skill role from pipeline stage
2. Load stage-specific keep/remove rules
3. Filter decisions: keep only decisions relevant to target's domain
4. Filter artifacts: remove artifacts target doesn't need
5. Compress: collapse verbose rationale into one-line summaries
6. Measure: if token_budget_after > 12,000, re-run with stricter rules
7. Record: populate context_pruned object with what was removed
```

**Checkpoint:** Is `token_budget_after` ≤ 12,000? Are all `non_negotiable: true` constraints intact?
  Complete when: token_budget_after ≤ 12,000 and all non_negotiable constraints are preserved intact.

### Phase 3: Record Decision Gate

Every architectural or strategic choice goes into the decision gate ledger. See [Decision Gate Ledger](references/decision-gate-ledger.md).

**When to record a gate:**
- Architecture pattern selection
- Technology stack choice (database, message broker, framework)
- API contract decisions (REST vs GraphQL vs gRPC)
- Security boundary definition
- Data ownership assignment

**When NOT to record:**
- Implementation details (which library version within chosen stack)
- Formatting preferences
- Temporary workarounds with clear sunset dates
  Complete when: Every architecture pattern, technology choice, API contract, security boundary, and data ownership decision is recorded in the decision gate ledger.

### Phase 4: Sign Contract

Create a handoff contract using the [Handoff Contract Template](references/handoff-contract-template.md).

**Contract flow:**
```
Upstream agent creates contract → PROPOSED
Downstream agent reviews → ACCEPTED or REJECTED
If ACCEPTED → Upstream delivers → IN_PROGRESS
If REJECTED → Upstream revises or escalates
On delivery verified → FULFILLED
If deliverable fails acceptance → BREACHED
```

**Checkpoint:** All P0 requests acknowledged? All deliverable paths resolve?
  Complete when: All P0 requests acknowledged by the downstream agent, and every deliverable path resolves to ACCEPTED or escalated.

### Phase 5: Deliver and Verify

Write handoff state to `~/.agents/state/handoffs/{pipeline_id}/NNN-{origin}→{target}.json`.

Downstream agent:
1. Loads Tier 1 (pipeline identity, constraints)
2. Requests Tier 2 if needed (role-specific artifacts)
3. Verifies checksum of received state
4. Audits constraint inheritance (all `non_negotiable` from prior handoffs present?)
5. Accepts or rejects contract
6. Begins work
  Complete when: State file written to ~/.agents/state/handoffs/, downstream agent loads Tier 1-2, verifies checksums, audits constraint inheritance, and begins work.

---

## Decision Trees

### Decision Tree 1: Handoff Timing — When to Hand Off vs. Continue

```
Agent finishes a unit of work
│
├─ Are there >0 decisions made that affect downstream agents?
│  ├─ Yes → Is at least 1 decision irreversible?
│  │  ├─ Yes → HANDOFF NOW (downstream must know before proceeding)
│  │  └─ No  → Continue to next check
│  └─ No  → CONTINUE (nothing to communicate)
│
├─ Has current agent exhausted its scope?
│  ├─ Yes → HANDOFF (agent's role complete)
│  └─ No  → Continue to next check
│
├─ Would continuing add >500 tokens to handoff state?
│  ├─ Yes → HANDOFF NOW (avoid state bloat)
│  └─ No  → CONTINUE (more efficient to batch decisions)
│
└─ Are there >3 accumulated open questions?
   ├─ Yes → HANDOFF NOW (stop compounding uncertainty)
   └─ No  → CONTINUE (resolve more before handoff)
```

### Decision Tree 2: Context Pruning — What to Keep vs. Remove

```
For each context item in handoff state:
│
├─ Does the target agent's role need this to make decisions?
│  ├─ No  → REMOVE
│  └─ Yes → Continue
│
├─ Is this item >2 pipeline stages old?
│  ├─ Yes → Is it marked non_negotiable?
│  │  ├─ Yes → KEEP (constraint survives aging)
│  │  └─ No  → REMOVE (stale context)
│  └─ No  → Continue
│
├─ Is this a rejected alternative from a decision?
│  ├─ Yes → Is the decision reversible?
│  │  ├─ Yes → KEEP (may need to revisit alternatives)
│  │  └─ No  → REMOVE (irreversible — alternatives are historical noise)
│  └─ No  → Continue
│
├─ Is this an internal reasoning transcript?
│  ├─ Yes → COMPRESS (summarize to one-line rationale)
│  └─ No  → Continue
│
└─ KEEP (passes all filters)
```

### Decision Tree 3: State Serialization Format — JSON vs. YAML vs. SQLite vs. Memory

```
Select serialization format:
│
├─ Is this a cross-process handoff (different agent processes)?
│  ├─ Yes → Is the pipeline stateless (no need to query past state)?
│  │  ├─ Yes → JSON (universal, schema-validated, human-readable)
│  │  └─ No  → SQLite (queryable ledger, supports incremental updates)
│  └─ No  → Continue
│
├─ Is latency critical (<100ms per handoff)?
│  ├─ Yes → MEMORY (in-process shared state, no serialization overhead)
│  └─ No  → Continue
│
├─ Is human readability required for audit trail?
│  ├─ Yes → Does the team prefer YAML?
│  │  ├─ Yes → YAML (more readable for long prose rationale)
│  │  └─ No  → JSON (better tooling support, stricter validation)
│  └─ No  → SQLite (best for machine-to-machine, queryable, incremental)
│
└─ Default: JSON (best balance of portability, validation, and readability)
```

### Decision Tree 4: Multi-Agent Topology Selection — Supervisor vs. Hierarchical vs. Peer vs. Debate vs. Swarm

```
Select topology for pipeline:
│
├─ Is the pipeline strictly sequential (A → B → C)?
│  └─ Yes → SUPERVISOR (one orchestrator routes state)
│
├─ Does the pipeline have parallel branches?
│  ├─ Yes → Do branches need to coordinate with each other?
│  │  ├─ Yes → HIERARCHICAL (lead agents coordinate, sub-agents execute)
│  │  └─ No  → SUPERVISOR with parallel fan-out
│  └─ No  → Continue
│
├─ Do agents need bidirectional feedback loops?
│  └─ Yes → PEER-TO-PEER (agents negotiate directly)
│
├─ Is this a high-stakes decision with low confidence?
│  └─ Yes → DEBATE (two agents argue, arbiter decides)
│
├─ Is maximum parallelism needed with no ordering constraints?
│  └─ Yes → SWARM (all agents write to shared state, merge at end)
│
└─ Default: SUPERVISOR (simplest, best audit trail, works for 80% of cases)
```

### Decision Tree 5: Conflict Resolution — When Two Agents Disagree

```
Agent B detects contradiction with Agent A's ledger:
│
├─ Is the contradiction on the same decision gate?
│  ├─ Yes → Is Agent A's decision marked irreversible?
│  │  ├─ Yes → ABORT. Escalate to human. Do NOT override.
│  │  └─ No  → Continue
│  └─ No  → This is a NEW decision. Record normally.
│
├─ Does Agent B have materially better information?
│  ├─ Yes → OVERRIDE with SUPERSEDED marker and new rationale.
│  │        Must include: why better info, why original was wrong.
│  └─ No  → Continue
│
├─ Is the contradiction on cost_of_reversal = "prohibitive"?
│  ├─ Yes → ESCALATE to debate topology. Both agents present case.
│  └─ No  → Continue
│
├─ Can both choices coexist (non-overlapping scope)?
│  ├─ Yes → RECORD both with scope boundaries. Neither is wrong.
│  └─ No  → MARK conflict. Escalate if confidence < high on either side.
│
└─ Default: When in doubt, ESCALATE. Silent override is the worst outcome.
```

---


## Error Recovery

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

### Upstream (Consumes From)

This skill has no upstream dependencies — it is a foundational framework that sits at the start of the pipeline chain.

### Downstream (Feeds Into)

| Skill | What This Skill Provides | What That Skill Does With It | Handoff Format |
|-------|-------------------------|------------------------------|----------------|
| **system-architect** | Business constraints, NFRs, regulatory requirements | Translates into architecture decisions, ADRs | Tier 1 constraints → ADRs, topology diagrams |
| **backend-developer** | ADRs, API contracts, data models, tech constraints | Implements services, writes code, creates APIs | Full state with artifact paths, tech constraints |
| **devops-engineer** | Runtime dependencies, env schema, resource requirements, health checks | Builds Dockerfiles, k8s manifests, CI/CD pipelines | Pruned to infrastructure-relevant state |
| **security-engineer** | Auth flows, data classification, SBOM, network surface | Audits for vulnerabilities, validates compliance | Pruned to security surface area only |

### Cross-Topology Coordination

| Topology Combination | When to Use | Handoff Pattern |
|---------------------|-------------|-----------------|
| Supervisor → Supervisor | Nested pipelines (sub-pipelines within stages) | Supervisor passes state to sub-supervisor, waits for completion |
| Supervisor → Swarm | Parallel exploration within a stage | Supervisor fans out same state to N agents, merge agent consolidates |
| Peer → Supervisor | Collaborative design finalizes into sequential delivery | Peers negotiate contract, then supervisor orchestrates delivery |
| Debate → Supervisor | High-stakes decision gates | Arbiter records final decision, supervisor routes it to implementers |

---


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System context, integration points, architectural constraints | Before specialized implementation — understand the system it fits into |


## Proactive Triggers

| # | Trigger Condition | Why It Matters | If Ignored |
|---|-------------------|---------------|------------|
| 1 | Pipeline involves 3+ agents in sequence | Context rot accelerates after 3 handoffs. Each handoff loses ~10% fidelity. | By agent 5, decisions are based on corrupted context. Rework cost: 2-4x original estimate. |
| 2 | Token budget before pruning > 15,000 | Bloated state slows downstream agents, wastes tokens, buries critical constraints in noise. | Downstream agent misses a `non_negotiable` constraint and makes an invalid decision. Cost: full pipeline restart. |
| 3 | Two agents record decisions on overlapping gates | Silent contradiction breaks the decision chain. Audit trail becomes unreliable. | Production incident traced to contradictory architecture decisions. Mean time to resolve: 3-5 days. |
| 4 | Handoff contract sits in PROPOSED >24 hours | Pipeline stalls. Downstream agent may be blocked waiting for upstream. | Deadline miss cascades through pipeline. Each day of stall compounds by 1.5x downstream. |
| 5 | >3 open questions accumulate without resolution | Uncertainty compounds. Each new question increases probability of wrong decision by 15%. | Pipeline proceeds on assumptions. 40% chance of major rework at integration stage. |
| 6 | Checksum verification fails on received handoff | State was corrupted or tampered with during transit. | Downstream agent operates on wrong data. Debugging cost: 2-5x normal because root cause is hidden in transmission layer. |

---

## What Good Looks Like

| Dimension | Excellent (10/10) | Mediocre (5/10) | Unacceptable (0/10) |
|-----------|-------------------|-----------------|---------------------|
| **State Completeness** | Every decision gate recorded with rationale, alternatives, confidence, reversibility. Non-negotiable constraints preserved across all handoffs. | Most decisions recorded but rationale is vague ("best option"). Some constraints dropped silently. | Decisions missing from ledger. Constraints lost after 2 handoffs. State is a raw dump with no pruning. |
| **Context Pruning** | Token budget_after < 8,000 for all handoffs. Tier 1/2/3 loading respected. No noise reaches downstream agents. | Budget_after ~15,000. Some business context leaks through. Agent wastes tokens on irrelevant details. | Budget_after > 25,000. Full raw context dumped to every agent. 60%+ of tokens are noise. |
| **Contract Discipline** | Every handoff has signed contract with acceptance criteria. Breach conditions clear. Downstream agent verifies before proceeding. | Contracts exist but acceptance criteria are vague. Verification is informal ("looks good to me"). | No contracts. Agents hand off blindly. Deliverables assumed complete without verification. |
| **Conflict Resolution** | Contradictions detected by checksum chain. Conflicts escalated through debate topology. All overrides marked SUPERSEDED with rationale. | Conflicts detected but resolved by last-writer-wins. SUPERSEDED markers sometimes missing. | Contradictions go undetected for 3+ stages. Silent overrides corrupt decision chain. Impossible to audit. |
| **Rot Defense** | Checksum chain verifies every handoff. Re-origin at handoff #3. Confidence decay enforced. Max 3 open questions rule active. | Some rot defense active but re-origin skipped due to time pressure. Confidence stays frozen at original level. | No rot defense. After 5 handoffs, agents operate on garbled context. Decisions contradict each other. Pipeline must be restarted from scratch. |

---

## Deliberate Practice

| Exercise | Skill Level | Time | What You'll Learn |
|----------|-------------|------|-------------------|
| **Serialize a real decision** | L1 | 10 min | Take the last architecture decision you made. Serialize it into a full decision gate ledger entry with rationale, alternatives, confidence, reversibility, and cost of reversal. |
| **Prune a bloated handoff** | L1 | 15 min | Take a real PRD or architecture doc (~5,000 words). Prune it for a backend developer downstream. Keep only what they need. Measure token_budget_before and after. |
| **Build a 3-agent pipeline** | L2 | 30 min | Create a supervisor topology pipeline: system-architect → backend-developer → devops-engineer. Write handoff state for each transition. Audit constraint inheritance. |
| **Resolve a simulated conflict** | L3 | 20 min | Create two contradictory decision gate entries for the same gate. Run the conflict resolution tree. Document the resolution with SUPERSEDED markers. |
| **Design a debate topology** | L4 | 30 min | Pick a real unresolved architecture decision. Assign two agents to debate it. Write the arbiter's decision with full rationale and rejected arguments. |
| **Audit a corrupt pipeline** | L5 | 45 min | Take a pipeline with 5 handoffs. Inject 3 intentional corruptions (missing constraint, silent override, stale artifact). Detect and fix each one using the rot defense patterns. |
| **Select topology for a real project** | L2-L5 | 20 min | Take your current project's agent pipeline. Run the topology decision tree. Justify why your choice beats each alternative. |

---

## Gotchas

| # | Gotcha | Cost if Ignored | Prevention |
|---|--------|----------------|------------|
| 1 | **Context drift across >3 handoffs** — After the 3rd handoff, state fidelity drops below 70%. By the 5th handoff, agents operate on ~50% accurate context. Decisions made at this depth are unreliable. | **$8,000-$15,000** in rework when pipeline output fails integration tests because foundational assumptions were corrupted mid-pipeline. | Enforce re-origin at handoff #3. Run checksum chain verification before every handoff. Flag any pipeline deeper than 5 stages for human review. |
| 2 | **Token budget exhaustion from bloated state** — Passing full 28,000-token state to every downstream agent in a 5-agent pipeline wastes ~100,000+ tokens on noise. | **$2,000-$5,000** in unnecessary API costs per pipeline run, plus 3-4x slower agent response times causing deadline misses. | Progressive disclosure: Tier 1 always, Tier 2 on demand, Tier 3 never auto. Hard cap at 12,000 tokens per handoff. |
| 3 | **Decision gate contradictions between agents** — Agent B overrides Agent A's database choice without marking it SUPERSEDED. Agent C implements based on Agent B's choice. Agent D references Agent A's original. Chaos. | **$15,000-$30,000** when contradictory architecture decisions cause production outage. Debugging takes 3-5 days because no one knows which decision is authoritative. | Decision gate ledger with checksum chain. Conflict detection on every handoff receipt. Irreversible decisions require debate topology to override. |
| 4 | **Missing handoff artifacts causing rework** — Upstream agent references `specs/order-service-openapi.yaml` in handoff but the file doesn't exist at that path. Downstream agent spends 4 hours reverse-engineering the API from code. | **$3,000-$8,000** per missing artifact in rework time. Compound if multiple artifacts are missing — downstream agent may give up and restart from scratch. | Artifact checksum in handoff state. Downstream agent verifies all artifact paths resolve before accepting contract. Artifact freshness check (Pattern 8). |
| 5 | **Over-pruning removing critical constraints** — Pruner removes "GDPR: EU data residency" constraint because it looks like "business strategy." Security engineer deploys to US region. | **$50,000-$500,000+** in regulatory fines, legal exposure, and emergency remediation. GDPR fines alone can reach €20M or 4% of global revenue. | Non-negotiable constraints are NEVER pruned. Constraint inheritance audit on every handoff. Compliance constraints get special `type: compliance` tag that bypasses all pruning. |
| 6 | **Silent handoff failures (no acknowledgment)** — Upstream agent writes handoff and assumes delivery. Downstream agent never receives it. Pipeline proceeds with stale or missing state. | **$5,000-$12,000** in wasted work when two agents operate on divergent state and produce incompatible outputs that must be reconciled or discarded. | Contract lifecycle enforcement: PROPOSED → ACCEPTED before upstream considers handoff complete. Timeout: if not accepted within SLA, escalate. |
| 7 | **Confidence inflation across handoffs** — Agent A records `confidence: medium`. Agent B references the decision as `"as established by architecture…"` implying certainty. By Agent C, it's treated as gospel. | **$10,000-$20,000** when a medium-confidence decision made early in the pipeline becomes an unquestioned constraint by the end. If wrong, entire pipeline output is invalid. | Confidence decay pattern: each handoff drops confidence by one level. Medium → Low → Treat as Question. Forces re-validation before commitment. |

---

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|-----------------|---------|
| "I'll just pass everything — the next agent can filter what they need." | You're dumping 28,000 tokens of noise on an agent with a 4,000-token budget. They'll miss the critical constraint in the flood. Progressive disclosure exists for a reason. |
| "It's just a prototype — we don't need formal handoff contracts." | Prototypes become production. The missing contract becomes the missing audit trail when something breaks. 80% of "temporary" pipelines are still running 6 months later. |
| "I know we disagree on the database choice, but I'll just pick one and move on." | Silent override is the #1 cause of pipeline corruption. The other agent will discover the contradiction 3 stages later. Mark it SUPERSEDED or escalate to debate. |
| "The checksum verification is overkill for a 3-agent pipeline." | State corruption doesn't care about pipeline size. One flipped bit in a constraint value and your entire pipeline output is wrong. Checksums take microseconds. |
| "We're under deadline — skip the pruning, we'll optimize later." | The pruning you skip today becomes the rework you do tomorrow. Bloated handoffs slow EVERY downstream agent. 10 minutes of pruning saves hours of confusion. |

---

## Verification

### Pre-Handoff Checklist (Upstream Agent)

- [ ] All decisions recorded in ledger with `gate`, `choice`, `rationale`, `confidence`, `reversible`
- [ ] All `non_negotiable: true` constraints present and accounted for
- [ ] `token_budget_after` ≤ 12,000
- [ ] `context_pruned` object populated with what was removed and why
- [ ] All artifact paths resolve and checksums match
- [ ] `open_questions.length` ≤ 3
- [ ] `handoff_version` compatible with target agent
- [ ] `pipeline_id` matches current pipeline
- [ ] No self-handoff (`origin_skill` ≠ `target_skill`)
- [ ] Contract created and in `PROPOSED` state

### Pre-Acceptance Checklist (Downstream Agent)

- [ ] Checksum of received state matches recorded checksum
- [ ] All `non_negotiable` constraints from ALL prior handoffs present (constraint inheritance audit)
- [ ] No contradictory decisions detected (scan ledger for same gate, different choice)
- [ ] All artifact paths resolve to actual files
- [ ] Tier 1 loaded and understood
- [ ] Tier 2 requested if needed
- [ ] Contract reviewed: deliverables clear, deadlines feasible
- [ ] Contract state: `ACCEPTED` (or `REJECTED` with rationale)

### Pipeline Health Check (Any Agent)

- [ ] Current handoff number ≤ 5 (if >5, flag for human review)
- [ ] No confidence=low decisions older than 2 handoffs without re-validation
- [ ] No open questions older than 3 handoffs without resolution or escalation
- [ ] Rollback point available if handoff number is multiple of 3
- [ ] Context rot severity at Green or Yellow (if Orange/Red, abort and re-origin)

---

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References

This skill is supported by detailed reference specifications. Load these when deeper guidance is needed on a specific topic.

| # | Reference | Description | When to Load |
|---|-----------|-------------|--------------|
| 1 | [State Schema Specification](references/state-schema-spec.md) | Complete JSON schema with field types, validation rules, and examples | When implementing serialization or debugging schema errors |
| 2 | [Context Pruning Rules](references/context-pruning-rules.md) | Stage-specific keep/remove rules for every pipeline transition | When pruning context for a handoff |
| 3 | [Handoff Contract Template](references/handoff-contract-template.md) | Bilateral contract format with lifecycle states and breach conditions | When creating or reviewing a handoff contract |
| 4 | [Multi-Agent Topologies](references/multi-agent-topologies.md) | 5 topology patterns (Supervisor, Hierarchical, Peer, Debate, Swarm) with decision matrix | When designing a new multi-agent pipeline |
| 5 | [Decision Gate Ledger](references/decision-gate-ledger.md) | How to record, reconcile, and audit decisions across agents | When recording decisions or detecting contradictions |
| 6 | [Cross-Agent Directory Conventions](references/cross-agent-directory-conventions.md) | `~/.agents/` directory structure, environment variables, naming conventions | When setting up a new agent workspace |
| 7 | [Context Rotation Defense](references/context-rotation-defense.md) | 12 patterns to detect and prevent context degradation across handoffs | When pipeline exceeds 3 handoffs or corruption suspected |
| 8 | [Progressive Disclosure Pipeline](references/progressive-disclosure-pipeline.md) | Tier 1/2/3 loading strategy with role-based filters | When optimizing token usage in multi-agent pipelines |

### External References

- **LangGraph Documentation:** [langchain.com/langgraph](https://langchain.com/langgraph) — Reference implementation of supervisor and hierarchical topologies
- **CrewAI Multi-Agent Patterns:** [docs.crewai.com](https://docs.crewai.com) — Peer-to-peer and sequential agent orchestration
- **AutoGen Handoff Patterns:** [microsoft.github.io/autogen](https://microsoft.github.io/autogen) — Debate topology and swarm coordination patterns
- **OpenAI Swarm:** [github.com/openai/swarm](https://github.com/openai/swarm) — Lightweight multi-agent orchestration with handoff primitives

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Handoff payload includes entire conversation history (50K tokens) → Agent B receives truncated context because token limit exceeded mid-payload. The last 40% of the handoff — including the actual task and constraints — is silently dropped | No context pruning before handoff. The handoff protocol serializes the full conversation without distinguishing "needed context" from "historical discussion." Agent B gets the first 30K tokens (problem exploration) but misses the last 20K (actual requirements and decisions) | Implement structured handoff: separate "decision ledger" (must survive) from "conversation history" (summarize). Handoff payload = decision ledger + 500-token summary of relevant history. Validate payload size before sending — if >10K tokens, require pruning or escalation. Agent B should reject handoffs over token budget with a specific error, not silently truncate | Handoff payload size is a correctness problem, not just a cost problem. Truncated context means Agent B is working with partial information but doesn't know what it's missing. The handoff must be designed to fit in the receiving agent's context budget with room to work |
| State serialized as JSON: `{ "lastUpdated": "2024-01-15T00:00:00" }`. Agent B parses the date string as local time (UTC-8), interprets it as `2024-01-14T16:00:00Z`. Decision logs show events happening 8 hours before they actually occurred, breaking SLA compliance reporting | JSON has no native date type. Agent A serialized a Date object as ISO 8601 string. Agent B parsed it with `new Date(str)` which uses local timezone. No timezone normalization in the handoff contract. The handoff spec says "pass a Date" but doesn't specify the serialization format or timezone | Serialize all timestamps as ISO 8601 with explicit UTC offset: `2024-01-15T00:00:00Z`. Parse timestamps with a timezone-aware library. Add a validation rule: any timestamp without an explicit timezone offset (Z or ±HH:MM) is rejected. Include `timezone` field in handoff metadata: `"timezone": "UTC"`. Never rely on implicit timezone handling | Dates are the silent corruptor of all serialization protocols. ISO 8601 without 'Z' is ambiguous — it means local time, but "local" depends on which machine is parsing it. Every timestamp in a handoff must carry its timezone explicitly. Implicit timezone handling is a data corruption bug, not a formatting preference |
| Decision ledger not updated for 15 consecutive handoffs → Agent G makes a decision that directly contradicts Agent A's decision from handoff #2. The pipeline produces two conflicting architectural choices, neither aware of the other. Final output is internally inconsistent | Decision ledger update was "best effort" — agents logged decisions when they remembered. No enforcement: the handoff protocol didn't check whether the ledger was updated before passing state. Busy agents skipped logging to save time, creating an incomplete historical record | Enforce mandatory ledger updates: the handoff protocol rejects state unless the ledger contains an entry for the current agent's completed work. Add a ledger hash to the handoff payload — the receiving agent can verify ledger integrity. Require "no unlogged decisions" assertion before allowing handoff. If the assertion fails, the agent must log before handing off | Decision ledgers that are optional become empty ledgers. Every agent in a chain will optimize for speed and skip logging. The protocol must enforce logging as a precondition of handoff — no log entry, no state transfer. A ledger with gaps is worse than no ledger: it creates false confidence in incomplete information |
| Context pruning removes "irrelevant" message from conversation history → that message contained the API key for the next pipeline step. Agent B can't authenticate to the downstream service. Pipeline fails with "401 Unauthorized" and the error doesn't indicate what's missing | Pruning heuristic based on message length and position — short messages at the end of long threads were classified as low-signal. The API key was in a brief message: "here's the key: sk-abc123." No content-aware pruning — the heuristic treated all short messages as noise | Implement content-aware pruning: messages containing credentials, API keys, URLs, or code blocks are preserved regardless of length. Use regex patterns to identify high-signal short messages. Never prune the last 5 messages — working memory gets priority. Add a "pruned content summary" to the handoff: "removed X messages, Y tokens. Preserved all messages matching high-signal patterns." | "Irrelevant" is a dangerous pruning heuristic when the system doesn't understand content semantics. The shortest message in a conversation is often the most consequential — "use this key" is 13 characters that are worth more than the preceding 2,000 characters of discussion. Content-aware preservation rules are essential |
| Handoff contract specifies: "Agent B handles authentication." Agent B expects a pre-authenticated session token in the state. Agent A interprets "Agent B handles authentication" as "Agent B will do its own authentication" — passes no token. Agent B can't access protected resources | Ambiguous contract language. "Handles" doesn't specify: does Agent B perform authentication (login flow), or does Agent B receive authentication credentials (token)? Both agents interpreted the same contract differently. No contract validation that checks whether required state fields are populated before handoff | Define handoff contracts with explicit input/output schemas: "Agent B INPUT: auth_token (string, required). Agent B OUTPUT: authenticated_session (object)." Validate required inputs are populated before handoff — fail with clear error if `auth_token` is null. Use formal contract schemas (JSON Schema, Protocol Buffers) instead of natural language descriptions | Natural language contracts are ambiguous by design. "Handles authentication" means different things to different agents depending on their training. Formal input/output schemas eliminate interpretation — the agent either has the required input or it doesn't. Schema validation at handoff boundaries is the only way to catch contract violations before they propagate |
| Max-depth counter set to 10 → legitimate 11-step multi-agent pipeline gets killed at step 10 with "max delegation depth exceeded." Pipeline produces partial output. Half-configured infrastructure is left running, costing $200/hr in cloud resources with no work being done | Depth limit was arbitrary — "10 seems like plenty." The actual pipeline is a linear chain: analyze → design → implement → test → review → refactor → document → package → deploy → verify → monitor. Each step is a legitimate delegation. No distinction between linear chains (legitimate depth) and cycles (illegitimate depth) | Distinguish depth from cycles: linear chain depth is fine, cycles are not. Use cycle detection (agent ID already in chain) as the hard limit, not an arbitrary max depth. Set a soft depth warning at 10+: log a warning but continue. Only kill on cycle detection or explicit timeout. Implement rollback: if pipeline is killed, the orchestrator cleans up partial state — never leave half-done infrastructure running | Max-depth counters are a blunt instrument for a specific problem (cycles). They catch one deep-architecture pattern (11-step linear pipeline) but let through a 3-step cycle. Cycle detection replaces arbitrary depth limits with a precise problem detector. Cleanup on kill is mandatory — a killed pipeline must not leave resources running |

## State Log

This section documents every irreversible decision made during the session. It is non-negotiable and prevents the agent from revisiting settled questions.

| # | Decision | Rationale | Alternatives Considered | Timestamp |
|---|----------|-----------|------------------------|-----------|
| 1 | *[no decisions logged yet]* | — | — | — |

**Rules:**
- Append a new row for each irreversible or hard-to-reverse decision
- Never modify past rows — only append
- If revisiting a decision, add a NEW row (do not edit the old one)
