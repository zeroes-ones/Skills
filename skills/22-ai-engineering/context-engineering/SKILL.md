---
name: context-engineering
description: Use when designing or debugging AI agent context strategies, optimizing token budgets, building context assembly pipelines, or diagnosing context-related failures (wrong answers from missing info, bloated context causing poor reasoning, conversation drift). Handles 5-level context hierarchy design, inverse context packing, token budget allocation, context window optimization, conversation summarization, and file-level inclusion/exclusion decisions. Do NOT use for prompt engineering (route to llm-engineer), agent architecture design (route to ai-engineer), or model selection (route to ai-engineer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Context Engineering

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|-------------------|---------------------|
| 1 | NEVER include a source file without scoring its relevance first | `grep -c "include" context_plan.json \| awk '{if ($1>5) exit 1}'` | HALTs context assembly; re-rank all candidates |
| 2 | NEVER pass raw conversation history beyond 10 turns | `jq '.history \| length' context.json \| awk '{if ($1>10) exit 1}'` | Forces summarization pass before submission |
| 3 | NEVER exceed 80% of model context window | `python -c "import sys; t=int(sys.stdin.read()); print('BLOCKED' if t > 0.8 * 200000 else 'OK')"` < token_count.txt | Truncates lowest-relevance items until under budget |
| 4 | NEVER include Level 4 (error output) without first checking token cost of Level 1-3 | `test -f errors.log && wc -c errors.log \| awk '{if ($1>4096) exit 1}'` | Strips error output to last 50 lines + stack trace |
| 5 | NEVER skip deduplication pass before final submission | `grep -c "DUPLICATE" context_audit.log \| awk '{if ($1>0) exit 1}'` | Reruns dedup with stricter hash threshold |
| 6 | NEVER include a file from Level 3 if a sibling file at same level supersedes it | `diff <(sort level3_manifest.txt) <(sort level3_approved.txt) \| grep "^>" \| wc -l \| awk '{if ($1>0) exit 1}'` | Removes all unapproved Level 3 files; re-validates |
| 7 | NEVER assemble context without a token budget declared upfront | `jq '.token_budget' context.json \| awk '{if ($1==null\|\|$1<=0) exit 1}'` | Aborts assembly; requires explicit budget declaration |
| 8 | NEVER let prompt caching miss rate exceed 40% | `jq '.cache_hits / (.cache_hits + .cache_misses)' stats.json \| awk '{if ($1<0.6) exit 1}'` | Restructures prefix to maximize cache reuse |

## The Expert's Mindset

Context engineering is not prompt engineering — it's information logistics. Masters understand three non-obvious truths:

**1. More context degrades output.** Every token beyond what the model needs dilutes signal-to-noise. Studies show GPT-4 accuracy on retrieval tasks drops 7-12% when context exceeds 70% of the window. The optimal band is 30-55% utilization.

**2. Order matters more than content.** The "lost-in-the-middle" phenomenon means information at positions 25-75% of context depth is 20-40% less likely to be attended to. Critical instructions go at the top; critical facts go at the bottom. Never bury a requirement in the middle.

**3. Context is a cache, not a database.** Treat the context window as an L1 cache with high miss penalty (~$0.01-0.05 per unnecessary token across a session). Every file included without purpose is a cache pollution event that cascades into degraded performance on subsequent turns.

**Cognitive biases to guard against:**
- *Completeness bias* — "I'll just include everything to be safe" (exactly wrong)
- *Recency anchoring* — over-weighting what was recently fixed vs. what's broken now
- *Familiarity heuristic* — including files you know well even when irrelevant

## Operating at Different Levels

### Quick Scan (~30s)
Check the token budget dashboard. Verify cache hit rate > 60%. Confirm no Level 3-5 leak without Level 1-2 grounding. Run: `python context_audit.py --quick`

### Standard Engagement (~5min)
Full context assembly pass: Level 1→2→3→4→5 with relevance scoring at each transition. Apply Inverse Context Packing. Validate against Ground Rules. Run: `python context_audit.py --standard`

### Deep Dive (~30min)
Architecture review of the entire context pipeline. Includes: context window simulation with real workload traces, cache hit rate optimization, comparative testing with 3 different assembly strategies, and a dollar-cost projection for the next 10K requests.

## When to Use

**Triggers:**
- Agent produces wrong answer despite correct information being available in the repo
- Agent "forgets" instructions mid-conversation (context window overflow)
- Token costs are 2x+ above benchmark for similar tasks
- Building a new agent and designing its context assembly pipeline
- Agent reasoning quality degrades noticeably after turn 15+
- Migrating between models with different context window sizes
- Implementing RAG or hybrid retrieval for an agent
- Diagnosing "lost in the middle" failures

**When NOT to use:**
- Prompt phrasing or instruction tuning → route to `llm-engineer`
- Agent architecture, tool selection, or orchestration → route to `ai-engineer`
- Model selection or provider comparison → route to `ai-engineer`
- Pure retrieval quality (embedding models, chunking) → route to `ai-engineer`

## Route the Request

```
                    ┌─────────────────────────────┐
                    │  What artifact is present?   │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   ┌──────────────┐      ┌──────────────┐        ┌──────────────┐
   │ token_budget │      │ context_plan │        │ failure_log  │
   │ .json/.yaml  │      │ .json/.yaml  │        │ .log/.jsonl  │
   └──────┬───────┘      └──────┬───────┘        └──────┬───────┘
          │                     │                       │
          ▼                     ▼                       ▼
   Budget Analysis       Assembly Design         Failure Diagnosis
   (→ Decision Tree 1)   (→ Decision Tree 2-3)   (→ Decision Tree 4-5)
```

**Intent-based routing (no artifacts):**
- "Why is my agent wrong?" → Start at "Context Failure Diagnosis" (Section: Core Workflow, Step 4)
- "How do I fit more in context?" → Start at "Inverse Context Packing" (Section: Core Workflow)
- "My costs are too high" → Start at "Token Budget Allocation" (Section: Decision Trees)
- "Agent forgets instructions" → Start at "Conversation Summarization" (Section: Decision Trees)
- "Designing from scratch" → Start at "Core Workflow" and proceed sequentially

## Core Workflow

### The 5-Level Context Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT WINDOW (200K tokens)              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ L1: RULES FILES (ALWAYS)          ~2-8K tokens   ████ │  │
│  │ .cursorrules, .claude.yaml, SKILL.md, CLAUDE.md       │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ L2: SPECS (WHEN RELEVANT)         ~5-20K tokens  █████│  │
│  │ PRDs, ADRs, API contracts, data models, architecture  │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ L3: SOURCE FILES (SELECTIVE)      ~30-80K tokens █████│  │
│  │ Relevance-scored, deduplicated, priority-ordered       │  │
│  │     ├── Priority A: files agent is actively editing    │  │
│  │     ├── Priority B: direct dependencies (imports)      │  │
│  │     └── Priority C: related files (same module)        │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ L4: ERROR OUTPUT (DEBUG ONLY)     ~1-10K tokens  ██   │  │
│  │ Last 50 lines of errors + stack traces + fix attempts  │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ L5: CONVERSATION HISTORY (SUMMARIZED) ~3-15K ███       │  │
│  │ Compressed turns: decisions made, facts learned, state │  │
│  └───────────────────────────────────────────────────────┘  │
│                         BUFFER: ~30% reserved                │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Declare Token Budget

```python
# token_budget.py
MODEL_WINDOWS = {
    "claude-3.5-sonnet": 200_000,
    "claude-3-opus": 200_000,
    "gpt-4o": 128_000,
    "gpt-4-turbo": 128_000,
    "gemini-1.5-pro": 1_000_000,
}

def allocate_budget(model: str, task_complexity: str) -> dict:
    window = MODEL_WINDOWS[model]
    # Safety margin: never exceed 80% of window
    usable = int(window * 0.80)
    
    budgets = {
        "simple":  {"L1": 0.04, "L2": 0.08, "L3": 0.30, "L4": 0.03, "L5": 0.05, "buffer": 0.30},
        "standard":{"L1": 0.03, "L2": 0.10, "L3": 0.35, "L4": 0.05, "L5": 0.07, "buffer": 0.20},
        "complex": {"L1": 0.02, "L2": 0.12, "L3": 0.40, "L4": 0.08, "L5": 0.08, "buffer": 0.10},
    }
    
    alloc = budgets[task_complexity]
    return {k: int(usable * v) for k, v in alloc.items()}
```

### Step 2: Inverse Context Packing

The counter-intuitive approach: start with everything, then surgically remove.

```
Algorithm: INVERSE_CONTEXT_PACKING
  Input:  candidate_files[], token_budget, relevance_threshold
  Output: final_context[]

  1.  candidates ← ALL files in repo (recursive glob)
  2.  candidates ← SORT candidates BY relevance_score DESC
  3.  context ← [] , tokens_used ← 0
  4.  FOR each file IN candidates:
  5.      cost ← estimate_tokens(file)
  6.      IF tokens_used + cost > token_budget:
  7.          BREAK  // budget exhausted; rest are excluded
  8.      IF relevance_score(file) < relevance_threshold:
  9.          CONTINUE  // below quality bar
  10.     context.append(file)
  11.     tokens_used += cost
  12. context ← DEDUPLICATE(context)  // hash-based, content-aware
  13. context ← COMPRESS(context)     // strip comments, minify where safe
  14. RETURN context
```

**Why inverse?** Traditional "additive" packing starts empty and adds — this biases toward files seen first. Inverse packing starts with the full ranked set and cuts from the bottom, ensuring priority files always make it in and lower-priority files never displace higher ones.

### Step 3: Priority Ordering Within Level 3

```python
def score_file_relevance(file_path: str, task_description: str, 
                          dependency_graph: dict, edit_history: list) -> float:
    """
    Returns 0.0-1.0 relevance score.
    Factors: edit recency (0.35), import distance (0.30), 
             semantic similarity (0.25), file size penalty (0.10)
    """
    recency = _recency_score(file_path, edit_history)        # 0.35 weight
    proximity = _import_distance(file_path, dependency_graph) # 0.30 weight
    semantic = _embedding_similarity(file_path, task_description) # 0.25 weight
    size_penalty = min(1.0, 500 / max(os.path.getsize(file_path), 1)) # 0.10 weight
    
    return (0.35 * recency + 0.30 * proximity + 
            0.25 * semantic + 0.10 * size_penalty)
```

### Step 4: Context Window Optimization

**Deduplication:** Hash every paragraph (not line). Merge paragraphs with Jaccard similarity > 0.85. This catches copy-pasted code blocks and duplicate error messages.

**Compression:** Strip comments from source files (unless the task is "add documentation"). Collapse whitespace in non-Python files. Truncate long string literals > 500 chars to `"...[truncated {N} chars]"`.

**Relevance scoring decay:** Files that were included in the last 3 turns but never referenced get a 0.5x multiplier on their score. Files referenced by the agent get a 1.3x boost.

### Step 5: Validation Pass

```bash
# Run before every context submission
python context_audit.py --check-ground-rules \
  --max-tokens $(jq '.token_budget.L3' budget.json) \
  --cache-hit-target 0.60 \
  --dedup-threshold 0.85
```

## Decision Trees

### 1. Token Budget Allocation

**Phase 1 — Gather:**
- [ ] Model name and context window size
- [ ] Task complexity (simple/standard/complex)
- [ ] Expected conversation length (turns)
- [ ] Provider pricing ($/1K tokens input/output)

**Phase 2 — Decide:**
```
model_window > 150K?
  ├── YES → Use standard allocation, reserve 20% buffer
  │         L1: 3% | L2: 10% | L3: 35% | L4: 5% | L5: 7% | Buffer: 20%
  └── NO  → Use tight allocation, reserve 15% buffer
            L1: 4% | L2: 8% | L3: 25% | L4: 3% | L5: 5% | Buffer: 15%

Task is debugging?
  ├── YES → Shift 10% from L3 to L4
  └── NO  → Keep standard allocation

Expected turns > 20?
  ├── YES → Reserve additional 10% for L5 growth
  └── NO  → Standard L5 allocation
```

### 2. Context Level Selection

**Phase 1 — Gather:**
- [ ] Task type (write code, debug, review, explain, refactor)
- [ ] Agent state (cold start vs. mid-conversation)
- [ ] Available artifacts (error logs, PRDs, ADRs)
- [ ] Repository size (files count, total LOC)

**Phase 2 — Decide:**
```
Task is "write code"?
  ├── YES → Levels: L1 + L2 + L3 (no L4 unless errors exist)
  └── NO  → Continue

Task is "debug"?
  ├── YES → Levels: L1 + L3 + L4 (L2 only if specs explain expected behavior)
  └── NO  → Continue

Task is "review"?
  ├── YES → Levels: L1 + L2 + L3 (prioritize files in diff)
  └── NO  → All levels, standard allocation

Conversation turn > 10?
  ├── YES → Compress L5 to summary form (decisions + facts only)
  └── NO  → Include raw L5
```

### 3. File Inclusion Strategy

**Phase 1 — Gather:**
- [ ] Dependency graph (import tree)
- [ ] Recent git diff (what files changed)
- [ ] Agent's edit history (what files it modified)
- [ ] Task description (what the agent is asked to do)

**Phase 2 — Decide:**
```
File in git diff AND in edit history?
  ├── YES → Priority A (always include, full content)
  └── NO  → Continue

File is direct dependency of Priority A file?
  ├── YES → Priority B (include, may truncate if > 3K tokens)
  └── NO  → Continue

File shares module/package with Priority A?
  ├── YES → Priority C (include only function signatures + docstrings)
  └── NO  → Exclude unless relevance score > 0.7

Repository has > 200 files?
  ├── YES → Hard cap: max 15 Priority B + C files combined
  └── NO  → Soft cap: max 25 combined
```

### 4. Conversation Summarization

**Phase 1 — Gather:**
- [ ] Full conversation history (all turns)
- [ ] Agent's action log (tool calls, file edits)
- [ ] Error occurrences and resolutions
- [ ] Current task state

**Phase 2 — Decide:**
```
Turns > 15?
  ├── YES → Aggressive summarization
  │         • Keep: decisions (what was chosen), facts (what was learned), state (what changed)
  │         • Drop: tool call details older than 5 turns, resolved errors, intermediate reasoning
  │         • Format: "Turn [N]: [Action] → [Outcome]"
  └── NO  → Continue

Turns 5-15?
  ├── YES → Light summarization
  │         • Keep all decisions + facts, compress tool outputs > 2K tokens
  └── NO  → Keep raw history

Conversation crossed task boundary (new task started)?
  ├── YES → Full reset: summarize prior task as "Previously completed: [summary]"
  └── NO  → Incremental summarization
```

**Summarization template:**
```
## Session Summary (Turns 1-N)
- **Goal:** [original task]
- **Key decisions:** [bullet list]
- **Facts discovered:** [bullet list with file:line references]
- **State changes:** [files modified, configurations changed]
- **Unresolved:** [open questions or blockers]
```

### 5. Context Reset Triggers

**Phase 1 — Gather:**
- [ ] Current context utilization (% of window)
- [ ] Cache hit rate (last 10 requests)
- [ ] Agent response quality trend (human eval or heuristic)
- [ ] Conversation turn count

**Phase 2 — Decide:**
```
Context utilization > 85%?
  ├── YES → IMMEDIATE RESET. Compress L5, evict lowest-score L3 files.
  └── NO  → Continue

Cache hit rate < 40% for 5+ consecutive turns?
  ├── YES → Restructure prefix. Move static content (rules, specs) to stable prefix.
  └── NO  → Continue

Agent made same mistake 3 times?
  ├── YES → Context pollution suspected. Purge L4, re-include L2 specs.
  └── NO  → Continue

Turn count > 30?
  ├── YES → Forced L5 compression regardless of utilization.
  └── NO  → No action
```

### 6. Cross-File Dependency Resolution

**Phase 1 — Gather:**
- [ ] Import graph from static analysis (`pycg`, `madge`, `depcruise`)
- [ ] Git blame for each candidate file (who/last modified)
- [ ] File sizes (token estimates)
- [ ] Test coverage data per file

**Phase 2 — Decide:**
```
File imported by > 5 Priority A files?
  ├── YES → Include as Priority B even if not in diff
  └── NO  → Continue

File is test file for a Priority A source file?
  ├── YES → Include if task is "debug" or "refactor", exclude otherwise
  └── NO  → Continue

File has 0% test coverage AND is Priority C?
  ├── YES → Drop from context (unreliable signal, risk of confusion)
  └── NO  → Keep at assigned priority

File size > 5K tokens?
  ├── YES → Include only: imports + function signatures + class definitions (no bodies)
  └── NO  → Include full content
```

## Cross-Skill Coordination

| Situation | Route To | What to Hand Off |
|-----------|----------|------------------|
| Agent keeps producing wrong answers despite correct context | `llm-engineer` | Context assembly log + failure examples |
| Need to redesign how agent tools consume context | `ai-engineer` | Token budget model + level allocation strategy |
| Context assembly involves DB schema files | `database-designer` | Relevance-scored file manifest |
| Context includes API contracts | `api-designer` | Token budget for L2 specs |
| Agent is a code reviewer with context issues | `code-reviewer` | File inclusion strategy for review diffs |
| Context pipeline is part of CI/CD | `ci-cd-builder` | Context assembly as a pipeline stage |
| Diagnosing why agent missed a security vuln due to missing context | `security-reviewer` | Context manifest showing which files were included/excluded |
| Context includes localization files | `localization-engineer` | File relevance scoring for locale files |

## Proactive Triggers

| Condition | Detection Mechanism | Automatic Action |
|-----------|-------------------|------------------|
| Token usage crosses 75% threshold | `python context_monitor.py --check-usage` | Triggers L5 compression + L3 eviction sweep |
| Agent response contains "I don't have enough context" | Regex: `/(don't|do not) have (enough|sufficient) context/i` | Re-runs relevance scoring with lower threshold; re-includes top 3 excluded files |
| Same file included in 5+ consecutive turns without being referenced | `jq '.file_refs \| group_by(.file) \| map({file: .[0].file, count: length})'` | Applies 0.5x decay multiplier to that file's relevance score |
| Cache miss on a request with > 1000 tokens | `jq 'select(.cache_miss and .input_tokens > 1000)' requests.jsonl` | Analyzes prefix stability; suggests static prefix restructuring |
| Conversation has > 3 context reset triggers in one session | Counter in context_audit.log | Escalates to full manual review; pauses automated context assembly |

## What Good Looks Like

**Before (poor context engineering):**
```
Turn 1: Agent receives 45K tokens → 18 source files, full conversation history
Turn 5: Agent receives 67K tokens → 24 source files, raw history (12 turns)
Turn 10: Agent receives 112K tokens → 31 source files, raw history (22 turns)
Turn 15: Agent receives 158K tokens → context overflow, instructions truncated
Result: Agent "forgets" to run tests. Cost: $0.47 for this session alone.
```

**After (good context engineering):**
```
Turn 1: Agent receives 28K tokens → 4 rules files + 3 specs + 8 Priority A/B files
Turn 5: Agent receives 32K tokens → 10 files (2 new, 2 evicted) + summarized history
Turn 10: Agent receives 35K tokens → 11 files + compressed history (decisions only)
Turn 15: Agent receives 38K tokens → 9 files (stale files evicted) + session summary
Result: Agent completes all tasks correctly. Cost: $0.18 for the session.
```

**Key metrics improvement:**
- Token utilization: 78% → 42% (healthier band)
- Cache hit rate: 23% → 71% (Anthropic prompt caching active)
- File relevance precision: 38% → 82% (fewer irrelevant files)
- Task completion rate: 67% → 94%

## Deliberate Practice

1. **Budget calibration drill:** Take a real agent trace. Manually score each file for relevance. Compare your judgment against the automated scorer. Calibrate until agreement > 85%.

2. **Summarization quality check:** Take a 20-turn conversation. Write a summary in exactly 500 tokens. Have another agent try to answer a question about turn 12 using only your summary. Iterate until accuracy > 90%.

3. **Cache structure optimization:** Take 100 agent requests. Identify the largest stable prefix that can be cached. Measure cost savings from prompt caching. Target: > 40% cost reduction.

4. **Context pollution audit:** Run an agent on a known task. After each turn, check if any included file was never referenced. Target: < 15% unreferenced files per turn.

5. **Cross-model portability test:** Take a context assembly tuned for Claude 200K. Adapt it for GPT-4o 128K without losing task completion quality. Document every compression decision.

## Gotchas

### 1. Context Pollution: The Silent Killer ($1,200/month)
A 10-developer team running 50 agent calls/day each at $0.03/call. If 60% of context tokens are irrelevant (pollution), that's $0.018 wasted per call × 50 calls × 22 days × 10 devs = **$1,188/month in wasted tokens**. Worse: polluted context causes 15-25% more turns per task due to degraded reasoning, doubling the real cost. Fix: mandatory relevance scoring before inclusion. Every file in context must earn its place.

### 2. Token Waste from Including Irrelevant Files ($850/month)
Common pattern: including entire `utils/` directory "just in case." A typical `utils/` folder is 15-30 files averaging 500 tokens each = 7,500-15,000 tokens. At Anthropic's $3/M input tokens, that's $0.02-0.05 per request. Across 15,000 requests/month (team of 8): **$375-$850/month burned on files the agent never reads.** Fix: dependency-graph-based inclusion. Only include files reachable from the files the agent is actively editing.

### 3. Missing Critical Context Causing Wrong Answers ($3,200/incident)
A production debugging session where the agent doesn't receive the error stack trace (Level 4 excluded) proposes a fix that creates a new bug. Engineer spends 4 hours implementing the wrong fix, then 2 hours reverting, then 2 hours re-debugging. At $200/hr fully loaded: **$1,600 in wasted engineering time.** If this happens twice a month: **$3,200/month.** Fix: Ground Rule #4 — never exclude Level 4 without explicit override.

### 4. Context Window Overflow Strategy Failure ($2,500/month)
Agent operating near context window limit (90%+ utilization) has instructions from Level 1 truncated. The agent "forgets" it must write tests for all new code. A feature ships without tests, discovered in QA. 3 engineers spend 2 days retrofitting tests: 3 × 16hrs × $150/hr = **$7,200 one-time cost.** If this pattern repeats quarterly: **$2,400/month amortized.** Fix: Ground Rule #3 — hard cap at 80% utilization. Never let the buffer drop below 20%.

### 5. Prompt Caching Failures ($1,500/month)
Anthropic prompt caching requires a stable prefix (exact byte match). If context assembly varies file ordering between requests, every request becomes a cache miss. At $7.50/M input tokens (uncached) vs $0.30/M (cached) for cached read tokens, a 50K token request costs $0.375 uncached vs $0.015 cached. For 500 requests/day: uncached = **$187.50/day, cached = $7.50/day.** Difference: **$180/day or $3,960/month.** Even a 50% cache hit rate saves $1,980/month. Fix: deterministic file ordering in context assembly. Always sort by priority tier first, then alphabetically within tier. Static content (L1, L2) MUST be the prefix.

## Verification

Run this checklist before any context-related change goes to production:

- [ ] Token budget declared and enforced (`jq '.token_budget' context.json` returns valid allocation)
- [ ] Context utilization < 80% of model window (`python context_audit.py --check-usage`)
- [ ] All Level 3 files have relevance scores > 0.4 (`python context_audit.py --check-scores`)
- [ ] Deduplication pass completed with < 5% duplicate rate (`grep -c "DUPLICATE" context_audit.log`)
- [ ] Conversation history (L5) is summarized, not raw, if turns > 10
- [ ] Level 1 content (rules) is identical to previous request (cache-friendly prefix)
- [ ] File ordering is deterministic: priority tier → alphabetical
- [ ] No file in context has been included without being referenced for 3+ turns
- [ ] Error output (L4) trimmed to last 50 lines + stack trace only
- [ ] Cache hit rate measured and > 60% over last 50 requests
- [ ] Ground Rules 1-8 all passing (`python context_audit.py --check-ground-rules`)
- [ ] Dollar-cost projection updated for current assembly strategy

## References

- [Context Hierarchy Design](../references/context-hierarchy-design.md) — Detailed 5-level specification with per-level examples
- [Token Budget Calculator](../references/token-budget-calculator.md) — Formulas and tools for computing optimal budgets by model
- [Inverse Packing Algorithm](../references/inverse-packing-algorithm.md) — Step-by-step implementation of inverse context packing
- [File Relevance Scoring](../references/file-relevance-scoring.md) — Scoring methodology for context inclusion decisions
- [Conversation Summarization](../references/conversation-summarization.md) — Strategies for compressing history without information loss
- [Context Pollution Patterns](../references/context-polution-patterns.md) — Common pollution vectors and prevention techniques
- [Prompt Caching Strategies](../references/prompt-caching-strategies.md) — Provider-specific caching optimization guides
- [Context Failure Postmortem](../references/context-failure-postmortem.md) — Template for diagnosing context-related failures
