# Context Rotation Defense — 12 Anti-Rot Patterns

Prevent context degradation from stale, redundant, or irrelevant content across turns.

## Pattern 1: Redundancy Detection
- **Method:** Cosine similarity on sentence embeddings; threshold 0.92
- **Action:** Remove duplicate; retain earliest canonical instance

## Pattern 2: Staleness Scoring
- **Method:** Track last-access timestamp per section; > 15 turns = stale
- **Action:** Summarize to 20% of original tokens; archive

## Pattern 3: Recency-Weighted Attention
- **Method:** Exponential decay, lambda=0.1 per turn
- **Action:** Content > 10 turns old drops below 37% attention weight

## Pattern 4: Unproductive-Loop Detection
- **Method:** Hash (action, outcome) pairs; > 3 identical = loop
- **Action:** Halt agent; inject escalation; require triage

## Pattern 5: Priority-Based Section Ranking
- **Method:** Score sections: ground_rules(10) > decision_trees(9) > gotchas(7) > workflows(6) > examples(3) > prose(1)
- **Action:** Evict lowest-priority sections first

## Pattern 6: Progressive Summarization
- **Method:** Summarize oldest 5-turn block after every 5 turns
- **Action:** Replace block with single-paragraph summary

## Pattern 7: Lazy Reference Loading
- **Method:** Load file stubs (path + 1-line description); expand on demand

## Pattern 8: Token Quota Hard Cap
- **Method:** Per-skill cap at declared token_budget; exceed = auto-compact

## Pattern 9: Context Freshness Window
- **Method:** Auto-remove content > 50 turns old; exception: state ledger entries

## Pattern 10: Cross-Skill Deduplication
- **Method:** Detect > 60% sentence overlap across skills; merge to canonical copy

## Pattern 11: Attention Slot Fragmentation Prevention
- **Method:** Track distinct topic count; > 5 = fragmentation; consolidate to top 3

## Pattern 12: State Ledger Checkpointing
- **Method:** Serialize decisions to immutable ledger; prune context; keep recovery ref
