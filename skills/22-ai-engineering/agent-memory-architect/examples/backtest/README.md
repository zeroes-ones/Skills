# Backtest Example — agent-memory-architect

> **Hypothetical demonstration scenario** for skill-runner validation.
> No production data is claimed. Every figure is **[COMPUTED]** from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario: a recurring research-and-report agent runs 40 times a month.
- Baseline behaviour: each run re-derives prior findings from scratch.
- Rates and volumes are illustrative inputs, not measured from an organisation.

| Parameter | Value | Tag |
|---|---|---|
| Runs per month | 40 | [ESTIMATED] |
| Re-derivation cost per run (no memory) | 18,000 tokens | [ESTIMATED] |
| Injected memory per run | 900 tokens | [ESTIMATED] |
| Blended token price | $12 per 1M tokens | [ESTIMATED] |
| Repeat-failure rate without memory | 15% | [ESTIMATED] |
| Cost of one repeat failure (rework) | $600 | [ESTIMATED] |
| Consolidation job cost per month | $40 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

**Without memory** — every run re-derives:

- Re-derivation: 40 × 18,000 = 720,000 tokens = **$8.64**/month
- Repeat failures: 40 × 15% = 6 events × $600 = **$3,600**/month
- Total: **$3,608.64**/month

**With memory (write-manage-read)** — recall replaces re-derivation, but memory is *paid for on every run*:

- Re-derivation drops to 4,000 tokens/run (recall covers the rest): 40 × 4,000 = 160,000 = **$1.92**
- Injected memory: 40 × 900 = 36,000 tokens = **$0.43**
- Repeat failures drop to 3% (prior outcomes are retrieved): 40 × 3% ≈ 1 × $600 = **$600**
- Consolidation job: **$40**
- Total: **$642.35**/month

**Delta:** **$2,966/month** avoided, ≈82% of the unmanaged cost.

Note the memory injection is **$0.43** — trivial. The saving comes from avoided re-derivation and avoided repeat failures, which is why memory must be justified on *behaviour*, not on storage cost.

## Best case

The store is retrieval-first: queries were designed before the schema, so recall lands on the first attempt. Consolidation counts outcomes rather than re-summarising, so the store stays truthful as it ages and the failure rate keeps falling across quarters.

## Worst case

The store is write-only. Entries accumulate, nothing is read, and the agent re-derives everything while paying storage for a log. Worse: if recall is later wired *without* a context-only wrapper, a prior run's conclusion re-enters as an instruction and the repeat-failure rate rises above baseline — the system becomes an error amplifier.

## Learnings / key takeaways

1. Memory pays on avoided re-derivation and avoided repeat failure, not on storage efficiency.
2. Injection cost is small; the risk is trust, not tokens.
3. A write-only store is pure cost, and it is the most common outcome of building memory without a read query.
4. Consolidation by counting keeps the store's history true; re-summarising gradually makes it fiction.
5. The poisoning path is the one you build: unlabelled recall turns a prior run's output into a current instruction.

## What this does not show

- No real agent, token counts, or failure rates underlie these figures; they are stated assumptions for arithmetic.
- The 82% figure depends entirely on how expensive re-derivation was; a task with cheap re-derivation would show a much smaller delta.
- Storage technology and embedding choice are out of scope — see `llm-engineer`.
