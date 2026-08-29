# Compression Validation — Retention-Test Protocol

> Compression is lossy by design. This protocol makes the loss **measured and bounded** instead of silent. Ground Rule R5: no lossy compression ships without a retention test ≥ 90%.

## When Compression Is Allowed

1. Lossless reductions first (zero quality risk): dedup, whitespace collapse, comment stripping, truncation of noise (lockfiles, minified bundles).
2. Lossy compression only when content **cannot be stabilized for caching** (unique per-request content, long conversation tails).
3. Never for decision-critical content without an explicit owner sign-off (legal, compliance, safety, financial).

## The Retention Test (90% Gate)

1. Take a representative payload (e.g., a 20-turn conversation or a 50K-token source bundle).
2. Write the compressed form (summary / pruned context) — target ≤ 500 tokens of summary or the planned post-compression size.
3. Build a held-out question set of 20-30 questions that a *correct* agent must be able to answer from the original (decisions made, facts stated, unresolved questions, state changes, exact error codes, file paths).
4. A fresh agent answers the questions **using only the compressed form**.
5. Compute accuracy = correct answers / total. **Pass = ≥ 90%.**
6. Commit the question set and the result; any future regression case is added to the suite.

## What Retention Must Preserve (by Context Role)

| Context role | Must preserve | Typical loss |
|--------------|---------------|--------------|
| Decisions & rationale | The decision, who made it, why, and the alternatives rejected | Keep 100% — never compress away |
| Facts & state | Values, config, environment, current status | Keep 100% |
| Unresolved questions | Open items + their owners | Keep 100% |
| Error/stack traces | Exact error code, file, line, stack | Keep verbatim (L4 rule from context-engineering) |
| Verbatim exchange | Exact wording of a quote or instruction | Compressible — but keep the instruction's meaning |
| Code & data | Semantics, not formatting | Compressible with care; never break semantics |

## Common Failure: The Dropped Decision Point

Symptom: an agent acts on a summary and violates a rule that existed only in the original ("never deploy on Fridays" was in turn 12; the summary says "deploy when ready").

Why it happens: summaries preserve *topics* (what was discussed) far better than *constraints* (what was decided). Decision points are usually one line in the middle of a long turn — the first thing summarization drops.

Prevention: the retention question set must include **constraint probes** — questions whose answer is a single decision line, not a topic. If constraint probes score < 90%, the summary is inadequate regardless of topic coverage.

## Validation Loop

```
compress → retention test → fail? → targeted fix (add decision block / keep verbatim list)
   ↑                                    ↓
   └────────────── pass ≥ 90% ── ship + commit test suite
```

## When NOT to Compress

- Content cached or cacheable (stabilize instead — cheaper and lossless).
- Content under audit/compliance obligation (retention requirement is legal, not economic).
- Content the *user* wrote and expects verbatim fidelity on (summarizing user requirements back to them loses trust).
- Content where the correctness cost of a miss exceeds the token savings by 100× or more (one wrong deploy >> $400/month of saved tokens).
