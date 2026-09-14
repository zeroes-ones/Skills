# Retrieval and Budget

Retrieval strategy and how much of the window memory may take.

## Strategies by question

| Question a future run asks | Strategy |
|---|---|
| "Have we done this before?" | Exact key — workflow plus task id |
| "What happened last time?" | Recent-N by key, newest first |
| "Anything relevant to this?" | Embedding search — needs an index and a budget |
| "What are the durable facts?" | Filter by trust class, not recency |

Design the question first; the strategy follows. See Decision Tree 3.

## The window budget

Memory competes with the task for the same window. An explicit cap forces the ranking decision once, deliberately, rather than letting overflow decide.

```
cap          : memory tokens as a share of the window
rank         : recency, then trust class, then read frequency
truncate     : drop lowest-ranked first; never truncate mid-entry
floor        : always inject verified facts regardless of cap
```

## Failure modes

- **No cap.** Memory grows until it crowds out the task; quality degrades as the store improves.
- **Truncating mid-entry.** A half-injected record is worse than none — it reads as complete.
- **Ranking by recency alone.** A verified fact from a year ago can outrank a stale guess from yesterday.
- **Injecting everything "just in case".** The cost is paid on every turn; the return is unbounded speculation.
- **Embedding search with no budget.** Recall volume is unbounded and unmeasured.
