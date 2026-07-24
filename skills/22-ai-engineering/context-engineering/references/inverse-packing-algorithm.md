# Inverse Context Packing Algorithm

## Overview

Inverse Context Packing flips the traditional "additive" assembly: start with every candidate file, rank by relevance, then remove from the bottom until the budget is met. This guarantees the highest-priority files always make it in.

## Why Not Additive Packing?

Additive packing ("start empty, add files until full") has three failure modes:
1. **Ordering bias:** Files encountered first get included regardless of priority
2. **Budget fragmentation:** Small files fill the budget before a large critical file is considered
3. **Threshold oscillation:** Hard to set a single relevance threshold that works across all file sizes

## Algorithm — Full Specification

```
FUNCTION inverse_context_packing(
    candidates: List[FileMetadata],
    token_budget: int,
    relevance_threshold: float = 0.4,
    dedup_similarity: float = 0.85
) -> List[FileMetadata]:

    // Phase 1: Sort by relevance (descending)
    sorted_candidates = SORT candidates BY relevance_score DESC

    // Phase 2: Greedy inclusion until budget exhausted
    context = []
    tokens_used = 0

    FOR EACH file IN sorted_candidates:
        cost = estimate_tokens(file.content)

        IF tokens_used + cost > token_budget:
            CONTINUE  // Budget exhausted for this file

        IF file.relevance_score < relevance_threshold:
            CONTINUE  // Below quality bar

        // Optional: chunk large files
        IF cost > token_budget * 0.25:
            file.content = extract_signatures(file.content)
            cost = estimate_tokens(file.content)

        context.append(file)
        tokens_used += cost

    // Phase 3: Deduplication
    context = deduplicate(context, similarity_threshold=dedup_similarity)

    // Phase 4: Compression
    context = compress(context)

    RETURN context
```

## Relevance Scoring Inputs

Each candidate file receives a score 0.0-1.0 based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Edit recency | 0.35 | How recently was this file modified in git? |
| Import distance | 0.30 | How many hops in the dependency graph from files the agent is editing? |
| Semantic similarity | 0.25 | Cosine similarity between file summary embedding and task description |
| File size penalty | 0.10 | Penalty for very large files (> 500 LOC → penalty increases) |

## Deduplication Strategy

Not just identical files — catch near-duplicates:
- Hash every paragraph (split on `\n\n`)
- Compute Jaccard similarity between all file pairs
- If Jaccard > 0.85, keep the file with higher relevance score, drop the other
- Special case: test files and source files are NOT duplicates even if structurally similar

## Compression Techniques

1. **Strip comments** — unless task involves documentation
2. **Collapse whitespace** — multiple blank lines → single blank line
3. **Truncate literals** — strings > 500 chars → `"...[truncated N chars]"`
4. **Signature-only mode** — for large library files: keep imports + function signatures, drop bodies
5. **Tree-sitter aware** — use AST to identify and preserve critical code paths

## Edge Cases

- **Single file exceeds budget:** Always include (Ground Rule override). Truncate to signature-only.
- **Zero files above threshold:** Lower threshold to 0.2. Flag for manual review.
- **All files fit in budget:** Skip Phase 3-4. Log as "suboptimal budget allocation."
- **Cyclic dependencies:** Treat the entire cycle as one unit. Use the max relevance score in the cycle.
