# Measurement Tooling

How to obtain each number the budget needs, and the traps in each.

## Ambient floor

Capture the prompt as the runtime actually sends it, before task content. Count with a real BPE tokenizer.

- **Trap:** word counts understate tokens by 1.5–2.3× on prose with identifiers.
- **Trap:** `chars/4` overstates.
- **Trap:** tool schemas load per turn and are often omitted from the count.

## Routing precision

Build a held-out set of (task description → correct skill). Measure rank-1 and must-not violations.

- **Trap:** measuring top-N instead of rank-1 hides the miss rate.
- **Trap:** a growing corpus silently makes every decision harder; re-measure after additions.

## Per-phase spend

Attribute cost to phases: ambient, routing, task, retry, structure overhead.

- **Trap:** unattributed cost gets absorbed into "the task" and stops being investigable.
- **Trap:** attribution without instrumentation is a guess.

## Outcome

Success metric for the same run, always recorded alongside cost.

- **Trap:** a metric chosen after the fact to look favourable.
- **Trap:** no success metric at all, which is the most common.

## Failure modes

- **Estimating instead of measuring.** An estimate off by 2× misdirects everything downstream.
- **Instrumenting cost but not outcome.** Half the ledger is missing.
- **Measuring once.** Every structural change moves the numbers.
- **Aggregating too early.** Averages hide the runs that dominate cost.
- **Trusting a proxy.** Word counts, file sizes, and elapsed time are all proxies; label them as such.
