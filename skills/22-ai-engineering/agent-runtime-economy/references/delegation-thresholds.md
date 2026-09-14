# Delegation Thresholds

Inline, subagent, or workflow — each has a setup cost and must beat the simpler option.

## The baseline

One call is the cheapest structure that can work. Anything else must be justified against it, measured — not asserted.

## Thresholds

| Structure | Use when | Setup cost |
|---|---|---|
| **Inline** | One well-scoped step fitting the current context | None |
| **Subagent** | Work fits one step but would pollute the main context | Context handoff |
| **Pipeline** | Multiple dependent steps in a fixed order | Sequencing |
| **Workflow** | Control flow must be explicit, retried, or gated | Manifest, state, executor |

## The isolation test

Delegation's real benefit is context isolation, not parallelism. Ask: would this work pollute the context that must stay clean for the final answer? If yes, isolate. If no, inlining is cheaper.

## Failure modes

- **Workflow where a call would do.** The most expensive way to look capable.
- **Parallelism without isolation benefit.** Fan-out costs money; if the steps are independent but the results are tiny, it bought nothing.
- **Delegating to look thorough.** Structure as signalling rather than engineering.
- **No baseline measured.** The structure's value is asserted, never compared.
- **Threshold absent.** The same task is structured differently by different people, with no rule.
- **Subagent for a one-line lookup.** Handoff cost exceeds the work.
