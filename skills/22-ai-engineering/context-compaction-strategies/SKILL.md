---
name: context-compaction-strategies
description: Manage token budgets, progressive disclosure, context window optimization, summarization strategies, dual-representation compilation (human-readable vs agent-optimized), structured context pruning, attention budget allocation, context retention policies across multi-turn conversations, state ledger design, and working memory vs long-term context separation. Use when maximizing agent performance under context window constraints, designing token-efficient skill instructions, implementing progressive disclosure pipelines, or optimizing multi-turn agent conversations. Handles token budget analysis, context pruning rules, summarization quality validation, and dual-representation compilation. Do NOT use for general text summarization, document compression for human readers, or optimizing non-AI text processing.
author: Sandeep Kumar Penchala
license: MIT
portability: spec_level
type: specialized
status: stable
version: 1.0.0
updated: 2025-07-24
tags: [context-window, token-budget, progressive-disclosure, dual-representation, summarization, context-pruning, attention-allocation, state-ledger]
token_budget: 4500
chain:
  consumes_from: [agent-handoff-protocol, multi-agent-orchestration]
  feeds_into: [all skills — optimization target]
compatible_with: [agent-handoff-protocol, multi-agent-orchestration, agent-eval-pipeline]
allowed-tools: [view, edit, create, bash, glob, grep, sql]
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

## Route the Request

```
Request received
  │
  ├─ "optimize context window" → This skill
  ├─ "reduce token usage" → This skill
  ├─ "progressive disclosure" → This skill
  ├─ "context pruning strategy" → This skill
  ├─ "dual-representation compile" → This skill
  ├─ "summarize document for humans" → Route to technical-writer
  └─ "compress general text" → Not this skill — use summarization tools
```

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|--------------------|
| 1 | NEVER prune context that contains active decisions — irreversible information loss | Pruning operation detected on state with `status: in_progress` fields | HALT — archive decisions to state ledger before pruning |
| 2 | NEVER summarize code blocks without preserving exact syntax — paraphrased code is useless | Code block detected in to-be-summarized context | PRESERVE verbatim or replace with file reference + hash |
| 3 | NEVER exceed 80% of model's effective context window — leave headroom for generation | Current estimated tokens > 0.8 × context_window_size | PRUNE lowest-priority 20% of tokens immediately |
| 4 | NEVER use lossy summarization on security-critical sections — vulnerabilities hide in details | Security, authentication, or data validation context flagged | PRESERVE verbatim, lossless compression only |
| 5 | NEVER compact without recording what was removed — no accountability for missing information | Compaction executed without metadata log | LOG: what was removed, why, recovery path before proceeding |
| 6 | NEVER assume all tokens have equal information density — prioritize by semantic importance | Uniform pruning without token importance scoring | SCORE tokens: decisions > constraints > code > examples > prose |
| 7 | NEVER compact during active generation — context change invalidates in-progress output | Agent mid-response when compaction triggered | WAIT for turn boundary before compacting |

## The Expert's Mindset

You manage agent context the way an operating system manages RAM — with paging, swapping, and priority-based eviction. You understand that token limits are a hard physical constraint, not a suggestion. Every token in context either earns its place by improving output quality or it's waste.

You think in terms of: **information density** (decisions per token), **semantic layering** (critical vs contextual vs background), **recoverability** (can this information be reconstructed if pruned?), and **attention dilution** (does too much context degrade focus on what matters?).

Your mental model is NOT "fit everything into context" — it's "maximize decision quality per token by ruthlessly eliminating noise."

## Operating at Different Levels

**Strategic (budget allocation):** Allocate token budgets across skill sections — Ground Rules (15%), Decision Trees (25%), Gotchas (10%), Core Workflow (15%), Reference Summaries (10%), Examples (15%), Frontmatter/Overhead (10%). Track actual usage vs budget.

**Tactical (progressive disclosure):** Design information hierarchies — Level 1 (always in context: ground rules, critical gotchas), Level 2 (loaded on-demand: full decision trees, detailed examples), Level 3 (referenced: complete reference files, appendices).

**Operational (compaction execution):** Implement compaction rules: (1) archive completed decisions to state ledger, (2) replace verbose code with file references, (3) summarize conversation history to key decisions, (4) prune resolved branches from decision trees.

## When to Use

**Use when:**
- Skill instructions exceed 3,000 tokens — needs dual-representation compilation
- Multi-turn agent conversation approaching context limit
- Skill chain spanning 3+ agents — handoff state needs pruning between agents
- Agent performance degrades in later turns (attention dilution)
- Token costs need 30%+ reduction without quality loss

**Do NOT use when:**
- Context is well under 50% of window — premature optimization
- Single-turn, single-skill agent invocation
- Human-facing content summarization (different optimization criteria)

## Core Workflow

```
1. AUDIT current context — token count, information density per section
2. CLASSIFY tokens by priority: Critical / Contextual / Background / Redundant
3. SET compaction target — token budget or % reduction
4. SELECT compaction strategy per content type:
   - Decisions: Archive to state ledger, keep summary
   - Code: Replace with file reference + content hash
   - Conversation: Summarize to key decisions + action items
   - Examples: Keep 1 representative, prune duplicates
   - Prose: Compress to structured format (XML/JSON-LD)
5. COMPACT — apply strategies in priority order (background first)
6. VALIDATE — verify no critical information lost
7. LOG compaction — what was removed, why, recovery path
8. MONITOR — track token usage, recompact if approaching limit
```

## Decision Trees

### Decision Tree 1: Compaction Trigger

```
Context state check
  │
  ├─ Token count > 80% of context window?
  │   └─ YES → COMPACT NOW (emergency — 20% headroom rule violated)
  │
  ├─ Token count > 60% and new information needed?
  │   └─ YES → COMPACT (proactive — make room before needed)
  │
  ├─ Multi-turn conversation, turn count > 10?
  │   └─ YES → COMPACT conversation history (summarize early turns)
  │
  ├─ Agent-to-agent handoff about to occur?
  │   └─ YES → COMPACT to handoff state (serialize decisions, prune context)
  │
  └─ Token count < 40% and single-turn?
      └─ NO → Do not compact (no benefit, risk of information loss)
```

### Decision Tree 2: Content-Type Compaction Strategy

```
Content type to compact
  │
  ├─ Architectural decisions / ADRs
  │   └─ STRATEGY: Archive to state ledger → Replace with decision ID + 1-line summary
  │       └─ Recoverable: YES — full text in ledger
  │
  ├─ Code blocks (implementations)
  │   └─ STRATEGY: Replace with `file:path:hash` reference
  │       └─ Recoverable: YES — git checkout by hash
  │
  ├─ Conversation history (turns 1-N)
  │   └─ STRATEGY: Progressive summarization — turns 1-5 → 3 sentences, turns 6-10 → bullet points
  │       └─ Recoverable: PARTIALLY — key decisions preserved, nuance lost
  │
  ├─ Reference documentation
  │   └─ STRATEGY: Replace with `references/file.md` link + 1-sentence purpose
  │       └─ Recoverable: YES — full file on disk
  │
  ├─ Examples and illustrations
  │   └─ STRATEGY: Keep 1 best example per concept, prune rest
  │       └─ Recoverable: NO — examples are illustrative, not authoritative
  │
  └─ Frontmatter and metadata
      └─ STRATEGY: Compress to minified format (YAML → JSON-LD)
          └─ Recoverable: YES — lossless round-trip possible
```

### Decision Tree 3: Progressive Disclosure Depth

```
Information importance assessment
  │
  ├─ CRITICAL — wrong decision without this
  │   └─ LEVEL 1: Always in context (Ground Rules, critical gotchas, safety constraints)
  │       └─ Examples: "NEVER skip input validation", reentrancy warning
  │
  ├─ IMPORTANT — better decisions with this
  │   └─ LEVEL 2: Load on first reference (decision trees, workflow steps)
  │       └─ Trigger: Agent encounters relevant domain keyword
  │
  ├─ USEFUL — edge cases and optimization
  │   └─ LEVEL 3: Available by reference (examples, benchmarks, alternatives)
  │       └─ Trigger: Agent explicitly requests or uncertainty detected
  │
  └─ BACKGROUND — completeness, not actionability
      └─ LEVEL 4: Archived (full reference files, historical context)
          └─ Trigger: Rare edge case or post-mortem analysis
```

### Decision Tree 4: Dual-Representation Compilation

```
Compile skill for agent consumption
  │
  ├─ Source format: Markdown (human-readable)
  │   └─ Keep as canonical source — single source of truth
  │
  ├─ Target: minified agent-optimized format
  │   ├─ Prose → structured directives (XML tags: <constraint>, <when>, <unless>)
  │   ├─ Tables → JSON arrays for faster parsing
  │   ├─ Decision trees → nested <branch> elements
  │   ├─ Code blocks → verbatim preservation
  │   └─ Reference links → inline summaries for critical refs
  │
  ├─ Compilation rules:
  │   ├─ Remove: markdown formatting chars (**, __, >), blank lines, comments
  │   ├─ Compress: repetitive qualifiers, redundant examples
  │   ├─ Preserve: all negative constraints, decision tree logic, gotcha content
  │   └─ Estimate: target 40-60% token reduction vs source
  │
  └─ Validation:
      ├─ Round-trip: minified → expanded → semantic equivalence check
      └─ Behavioral: agent with minified = agent with full (eval suite)
```

### Decision Tree 5: State Ledger Design

```
What to record in state ledger
  │
  ├─ Decision made? (ADR, architecture choice, technology selection)
  │   └─ RECORD: decision ID, description, alternatives, rationale, constraints, timestamp
  │
  ├─ Constraint discovered? (performance limit, API restriction, security requirement)
  │   └─ RECORD: constraint type, source, scope, enforcement level (MUST/SHOULD/MAY)
  │
  ├─ Assumption made? (user behavior, data volume, latency expectation)
  │   └─ RECORD: assumption, validation status (unvalidated/tested/confirmed/invalidated)
  │
  ├─ Risk identified? (technical debt, timeline risk, dependency risk)
  │   └─ RECORD: risk description, probability, impact, mitigation, owner
  │
  └─ Artifact created? (file, config, API endpoint, database schema)
      └─ RECORD: path, type, purpose, content hash, dependencies
```

## Cross-Skill Coordination

### Consumes From
- **agent-handoff-protocol:** Receives state ledger design, handoff serialization patterns
- **multi-agent-orchestration:** Receives context distribution requirements across agent topologies

### Feeds Into
- **All skills:** Provides token optimization patterns applicable to any skill

### Coordination with
- **agent-eval-pipeline:** Validate that compaction doesn't degrade agent behavior
- **multi-agent-orchestration:** Context partitioning between agents in topology

## Proactive Triggers

1. **Skill exceeds 3,000 tokens** — Suggest dual-representation compilation
2. **Multi-agent chain exceeds 3 agents** — Propose intermediate context compaction
3. **Agent conversation exceeds 15 turns** — Alert: context likely diluted, suggest summarization
4. **Token cost spike** — Analyze context for compaction opportunities
5. **Agent output quality decline in later turns** — Attention dilution detected, suggest pruning

## What Good Looks Like

✅ **Good:** "Compacted context from 8,200 to 4,100 tokens (50% reduction). Preserved all 12 decisions in state ledger, replaced 3 code blocks with file references, summarized turns 1-8 to key decisions. Validation: agent with compacted context produced identical architecture decisions (verified by diff)."

✅ **Good:** "Dual-representation compiled: 128KB markdown → 52KB XML minified (59% reduction). Semantic equivalence validated via eval suite: 97% behavioral match across 50 test scenarios."

❌ **Bad:** "I just truncated to the first 4,000 tokens. Hope nothing important was at the end." [[Lossy truncation without analysis — critical decisions may be lost]]

❌ **Bad:** "Summarized the security requirements to save tokens." [[Lossy summarization of security context — vulnerabilities can be introduced]]

## Deliberate Practice

1. **Token audit:** Take a skill at 5,000 tokens. Classify every token by priority (Critical/Contextual/Background/Redundant). Target: 30% identified as Background or Redundant.
2. **Dual-representation compile:** Convert a 500-token Proactive Triggers section to minified XML. Verify semantic equivalence. Measure token reduction.
3. **Conversation summarization:** Take a 20-turn agent conversation. Summarize to 500 tokens while preserving all decisions and action items. Have another agent judge completeness.
4. **Budget simulation:** Given a 100K context window and a 3-agent pipeline, allocate token budgets per agent. Optimize. Justify each allocation.
5. **Loss detection:** Intentionally over-prune a context. Can you identify what critical information was lost? Design a validation to catch this automatically.

## Gotchas

| # | Gotcha | Impact | Cost |
|---|--------|--------|------|
| 1 | **Over-pruning decisions:** Archived a "temporary" architecture decision that later became critical — agent makes conflicting choice | System inconsistency, rework of dependent components | $10K-$50K in rework |
| 2 | **Lossy code summarization:** Summarized "SQL injection fix: use parameterized queries" → "fixed SQL issue" — agent re-introduces vulnerability | Security regression in production | $100K-$1M+ in breach costs |
| 3 | **Compaction during generation:** Context changed while agent was writing code — output references pruned context inconsistently | Corrupted output, silent logical errors | $5K-$50K in debugging |
| 4 | **Missing state ledger:** No record of what was pruned — agent can't recover critical context when needed | Irreversible information loss, dead-end agent | $20K-$100K in lost context |
| 5 | **False equivalence in dual-representation:** Minified version lost a "NOT" in "Do NOT use for..." constraint — agent uses skill incorrectly | Agent applies skill to wrong domain, produces garbage | $10K-$100K in misapplied AI |
| 6 | **Attention dilution from over-caution:** Kept 15 "just in case" gotchas — agent's attention spread too thin, misses the 1 critical constraint | Critical constraint ignored, focused on edge cases | $50K-$500K in missed primary concern |
| 7 | **Uniform pruning without priority:** Removed 30% of tokens uniformly — lost 2 critical ground rules, kept 5 verbose examples | Agent violates pruned ground rules | $20K-$200K in compliance/security violations |

## Anti-Rationalization — No Excuses

| # | Rationalization | Reality |
|---|----------------|---------|
| 1 | "We'll just use a model with a bigger context window" | Larger context doesn't solve attention dilution. Models attend to ~70% of context effectively. More tokens ≠ better decisions. Compaction is about focus, not just fitting. |
| 2 | "Summarization is good enough — the agent will figure it out" | Lossy summarization of code, security constraints, or precise instructions introduces ambiguity. Ambiguity is where agents hallucinate. Precision matters more than brevity. |
| 3 | "We don't need a state ledger — we'll remember what we removed" | Human memory of what was pruned decays within minutes. Multi-turn conversations span hours. Without a ledger, pruned information is gone forever. |
| 4 | "Dual-representation is premature optimization — markdown works fine" | 40-60% token reduction translates directly to: 40-60% lower API costs, 40-60% more room for actual work context, and faster agent startup. This compounds across every invocation. |
| 5 | "All tokens are equally important — we can't prune anything" | Information density varies by 100x between a Ground Rule ("NEVER skip validation") and prose ("In this section, we will explore the various approaches to..."). Equal treatment of unequal tokens is waste. |

## Verification

| # | Check | Expected |
|---|-------|----------|
| 1 | Token audit completed | All sections classified by priority (Critical/Contextual/Background/Redundant) |
| 2 | Compaction ratio achieved | ≥ 30% token reduction without loss of decision-critical information |
| 3 | State ledger populated | All pruned decisions recorded with recovery path |
| 4 | No code summarization | All code blocks either preserved verbatim or replaced with file reference + hash |
| 5 | Security constraints preserved | All "NEVER", "MUST NOT", security constraints in context verbatim |
| 6 | Dual-representation validated | Semantic equivalence between human and agent-optimized formats |
| 7 | Compaction logged | Metadata: what was removed, why, when, recoverable? |
| 8 | Behavioral equivalence | Agent with compacted context produces same decisions as full context (eval verified) |
| 9 | Headroom maintained | Context usage ≤ 80% of window after compaction |
| 10 | Recovery tested | Simulated need for pruned information → successfully recovered from ledger or file reference |

## References

- [token-budget-allocation.md](references/token-budget-allocation.md)
- [progressive-disclosure-patterns.md](references/progressive-disclosure-patterns.md)
- [dual-representation-compiler.md](references/dual-representation-compiler.md)
- [state-ledger-design.md](references/state-ledger-design.md)
- [summarization-strategies.md](references/summarization-strategies.md)
- [attention-dilution-metrics.md](references/attention-dilution-metrics.md)
- [context-pruning-rules.md](references/context-pruning-rules.md)
- [conversation-history-compaction.md](references/conversation-history-compaction.md)
- [information-density-scoring.md](references/information-density-scoring.md)
- [compaction-validation.md](references/compaction-validation.md)
