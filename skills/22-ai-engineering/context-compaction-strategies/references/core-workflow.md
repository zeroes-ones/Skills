## Core Workflow

### Step 1: Progressive Disclosure Architecture

Design the three-tier loading system for every skill:

```
┌──────────────────────────────────────────────────────────────┐
│                 PROGRESSIVE DISCLOSURE TIERS                   │
│                                                               │
│  TIER 1 (150 tokens) — ALWAYS LOADED                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Route table + headlines: "This skill handles X. Use     │ │
│  │ when Y. Trigger keywords: [a, b, c]. DO NOT use for Z." │ │
│  │ Intent matching only — enough to decide if skill applies │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ↓ trigger match                       │
│  TIER 2 (800 tokens) — LOADED ON INTENT MATCH                 │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Core workflow steps + decision trees + ground rules.    │ │
│  │ Enough for ~80% of invocations. Covers standard path.    │ │
│  │ Decision tree branches are entry points to Tier 3 refs.  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                    ↓ edge case / uncertainty                   │
│  TIER 3 (4000 tokens) — LAZY-LOADED ON BRANCH TRAVERSAL       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Full gotchas, detailed examples, reference summaries,    │ │
│  │ verification checklists, deliberate practice exercises.  │ │
│  │ Only loaded when decision tree explicitly branches here. │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

**Tier boundary enforcement:**
- Tier 1 → 2 transition: keyword match in agent's intent (case-insensitive grep on route table)
- Tier 2 → 3 transition: decision tree branch that explicitly references a Tier 3 section
- Tier 3 → 2 eviction: 70% context window saturation → drop to Tier 2 representation
- Tier 3 → 1 eviction: 85% context window saturation → drop to Tier 1 headlines only
- Full eviction: 95% saturation → remove skill entirely; log what was evicted

### Step 2: Token Budget Management

Allocate and monitor token budgets per skill in the pipeline:

```python
# token_budget_manager.py
SKILL_BUDGET = {
    "tier1_headline": 150,      # Route + headline (always loaded)
    "tier2_workflow": 800,      # Core workflow + decision trees
    "tier3_full": 4000,         # Complete skill with gotchas + references
}

CONTEXT_SATURATION_THRESHOLDS = {
    "warning": 0.70,   # Yellow: prepare eviction candidates
    "critical": 0.85,  # Orange: evict Tier 3 content
    "overflow": 0.95,  # Red: emergency Tier 3 eviction + Tier 2 compression
}

def check_saturation(current_tokens: int, window_size: int) -> str:
    ratio = current_tokens / window_size
    if ratio >= 0.95: return "overflow"
    if ratio >= 0.85: return "critical"
    if ratio >= 0.70: return "warning"
    return "healthy"

def eviction_policy(saturation: str, active_skills: list) -> list:
    if saturation == "overflow":
        return [s for s in active_skills if s["tier"] == "tier1"]
    if saturation == "critical":
        return [s for s in active_skills if s["tier"] in ("tier1", "tier2")]
    if saturation == "warning":
        return sorted(active_skills, key=lambda s: s["priority"])[:-1]
    return active_skills
```

### Step 3: Context Pruning Algorithms

Three pruning strategies, selected by content type:

**A. Summarization-Based (LLM compression to 20% original tokens)**
```
Input: conversation history (turns 1-15, 8,000 tokens)
Prompt: "Summarize this conversation preserving: (1) all decisions made,
         (2) all facts discovered with file:line references, (3) all state
         changes, (4) unresolved blockers. Target: 1,600 tokens (20%)."
Output: structured summary at 20% token density
Validation: another agent answers factual questions using only summary
```

**B. Embedding-Based Retrieval (cosine similarity > 0.85)**
```python
def embedding_based_prune(context_sections, query, budget):
    query_embedding = embed(query)
    scored = []
    for section in context_sections:
        score = cosine_similarity(query_embedding, section.embedding)
        if score > 0.85:
            scored.append((section, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    selected, tokens = [], 0
    for section, score in scored:
        if tokens + section.token_count <= budget:
            selected.append(section)
            tokens += section.token_count
    return selected
```

**C. Rule-Based Truncation (section priority tagged in frontmatter)**
```
Frontmatter priority tags:
  sections:
    - name: "ground-rules"
      priority: 1   # NEVER truncate
    - name: "gotchas"
      priority: 2   # Truncate only if > 95% saturation
    - name: "decision-trees"
      priority: 3   # Truncate to branch headlines at 85% saturation
    - name: "examples"
      priority: 4   # Truncate first at 70% saturation
    - name: "deliberate-practice"
      priority: 5   # Drop entirely at 70% saturation
```

### Step 4: The 12 Context Rotation Defense Patterns

**Pattern 1: Redundancy Detection**
- Method: Sentence embedding deduplication at 0.92 cosine threshold
- Trigger: Two sentences in context with similarity > 0.92
- Action: Keep higher-timestamp version; drop older duplicate
- Counter: Redundant ground rules across turns waste attention budget

**Pattern 2: Staleness Scoring**
- Method: Score each section by `1.0 / (1 + hours_since_last_access)`
- Trigger: Section not referenced for > 5 turns
- Action: Apply 0.5x multiplier to relevance score; candidate for eviction
- Counter: Stale context occupies attention slots needed by fresh information

**Pattern 3: Recency-Weighted Attention Allocation**
- Method: Apply exponential decay: `weight = e^(-λ * turns_since_reference)` where λ=0.1
- Trigger: Every turn boundary
- Action: Re-rank all context sections by recency-weighted score
- Counter: Without decay, turn-1 instructions receive same attention as turn-15 instructions

**Pattern 4: Unproductive-Loop Detection**
- Method: Hash agent action + outcome pairs; detect > 3 identical cycles
- Trigger: Same (action, outcome) hash appears 3+ times in consecutive turns
- Action: Halt agent; inject escalation context; require human triage
- Counter: Looping agents burn tokens without progress — each cycle costs $0.03-0.15

**Pattern 5: Attention Zone Enforcement**
- Method: Classify context into primacy (0-200 tokens), mid (25-75%), recency (last 100 tokens)
- Trigger: Guardrail found in mid-context zone
- Action: Relocate to primacy zone (first 200 tokens)
- Counter: "Lost in the middle" — information at 25-75% depth is 20-40% less attended

**Pattern 6: Output Format Anchoring**
- Method: Place output format specification in last 100 tokens (recency zone)
- Trigger: Every context assembly
- Action: Append format spec to recency zone regardless of other content
- Counter: Recency effect ensures the last thing the model reads shapes its output

**Pattern 7: Mid-Context Avoidance**
- Method: Detailed examples, long prose, reference material → never in positions 25-75%
- Trigger: Any content > 200 tokens being placed in mid-context
- Action: Move to Tier 3 (lazy-loaded) or append to recency zone
- Counter: Long content in mid-context is the most likely to be ignored

**Pattern 8: Skill Conflict Detection**
- Method: Compare domain keywords across active skills; flag overlap
- Trigger: 2+ skills share > 3 domain keywords
- Action: Downgrade lower-priority skill to Tier 1; route ambiguities to human
- Counter: Conflicting skills cause the agent to apply wrong domain rules

**Pattern 9: Attention Slot Allocation**
- Method: Max 3 concurrent full-skill (Tier 2+) loads; remaining skills at Tier 1
- Trigger: 4th skill loading Tier 2 content
- Action: Evict lowest-priority full skill to Tier 1
- Counter: Beyond 3 concurrent skills, attention fragmentation causes cross-skill errors

**Pattern 10: Lazy-Loading Reference Files**
- Method: Reference files loaded only when decision tree branch explicitly traverses
- Trigger: Agent reaches a decision tree leaf that references `references/file.md`
- Action: Load file content inline; keep for 3 turns then evict
- Counter: Pre-loading all references burns 2,000+ tokens on unused content

**Pattern 11: Context Fragmentation Prevention**
- Method: Track attention allocation across skill boundaries; detect fragmentation
- Trigger: > 30% of context tokens come from > 5 different skill sources
- Action: Consolidate to top 3 skills; downgrade others to Tier 1
- Counter: Fragmented context prevents any single skill from having sufficient attention depth

**Pattern 12: State Ledger Checkpointing**
- Method: After every major decision, checkpoint: decision + rationale + constraints
- Trigger: Agent completes a decision tree branch
- Action: Serialize decision to ledger; prune decision tree context; keep ledger reference
- Counter: Without checkpointing, pruned decisions are unrecoverable

### Step 5: Dual-Representation Compilation

Compile human-readable markdown skills into agent-optimized minified formats:

```
SOURCE (markdown, 4500 tokens)          TARGET (minified XML/JSON-LD, ~2500 tokens)
─────────────────────────────────────   ─────────────────────────────────────
# Ground Rules                          <ground_rules>
                                         <rule id="1">
| # | Constraint        | Trigger        <constraint>NEVER prune active
|---|-------------------|---------------  decisions</constraint>
| 1 | NEVER prune active | Pruning on     <trigger>status:in_progress</trigger>
    | decisions          | in_progress    <response>HALT; archive to ledger
                                         </response></rule>
                                         </ground_rules>
