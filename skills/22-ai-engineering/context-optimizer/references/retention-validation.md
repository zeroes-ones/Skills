# Retention Validation — The >= 90% Protocol for Lossy Steps

## Why

Compression and summarization are lossy by design. Without a retention gate, the token you save on a dropped constraint costs 100x when the agent acts on the missing rule. Every lossy step ships with a retention score.

## The Protocol

1. Take the representative payload (e.g., a 20-turn conversation or a 50K source bundle).
2. Write the compressed form (summary / pruned context) — target the planned post-compression size.
3. Build a held-out question set of 20-30 questions a *correct* agent must answer from the original:
   - decisions made, rationale, alternatives rejected
   - facts/state/values/config
   - unresolved questions + owners
   - exact error codes, file paths, stack lines
   - **constraint probes**: single-line decisions the summary is most likely to drop
4. A fresh agent answers the questions **using only the compressed form**.
5. Accuracy = correct / total. **Pass = >= 90%.**
6. Commit the question set + result; any future regression case is added to the suite.

## Constraint Probes (the #1 gap)

Summaries preserve *topics* far better than *constraints*. A rule like "never deploy on Fridays" is one line in the middle of a long turn — the first thing summarization drops. The question set MUST include constraint probes; if they score < 90%, the summary is inadequate regardless of topic coverage.

## Content-Class Rules

| Content class | Policy |
|---------------|--------|
| Decisions & rationale | Keep verbatim — never compress away |
| Facts & state | Keep 100% |
| Unresolved questions | Keep 100% |
| Error/stack traces | Keep verbatim (L4 rule) |
| Verbatim exchange | Compressible — but keep instruction meaning |
| Code & data | Compressible with care; never break semantics |

## When NOT to Compress

- Content that is cacheable (stabilize instead — cheaper and lossless).
- Decision-critical content without owner sign-off (legal, compliance, safety).
- User-authored requirements (summarizing them back loses trust).
- Content where the correctness cost of a miss exceeds token savings by 100x or more.

## Regression Loop

```
compress → retention test → fail? → targeted fix (keep decision block / verbatim list)
   ↑                                    ↓
   └────────────── pass >= 90% ── ship + commit test suite
```
