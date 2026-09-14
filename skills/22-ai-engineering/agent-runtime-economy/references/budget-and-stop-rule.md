# Budget and Stop Rule

A budget without a stop rule spends to the cap regardless of progress.

## The three dimensions

| Budget | Bounds | Fails to catch |
|---|---|---|
| Tokens | Total context and generated spend | A slow single call |
| Turns | Number of model round-trips | Expensive turns |
| Wall-clock | Elapsed time | Idle waiting vs work |

All three are needed; each catches what the others miss.

## Setting the number

A budget is a decision about worth, not an arbitrary limit. Derive it: what is this task worth, and what spend is proportionate? A number with no rationale gets raised the first time it binds — which discards the only signal it produced.

## Defining convergence

The stop rule ends a session that has stopped improving. It must be measurable:

| Signal | Convergence condition |
|---|---|
| Outcome metric | No improvement over the last N turns |
| Repetition | The current attempt duplicates a prior one |
| Context | The agent is re-reading its own earlier turns |
| Definition | It can no longer state what "done" means |

## Failure modes

- **Cap only.** Spends to the cap on a task that converged ten turns earlier.
- **Budget raised reflexively.** The cap's signal is discarded when it first binds.
- **Only one dimension.** A token cap misses a spinning loop that generates little text.
- **Stop rule written mid-crisis.** Defined under pressure, it will be wrong.
- **Convergence assumed.** No measurable signal means "still working" is unfalsifiable.
- **Every session hitting the cap.** The cap is wrong, or the task is mis-sized.
