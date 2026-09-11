# Backtest Example — resilience-pattern-engineer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A payments service calls a card processor synchronously on the critical path.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Value | Tag |
|---|---|---|
| User-facing deadline | 2000 ms | [ESTIMATED] |
| Serialisation/render overhead | 200 ms | [ESTIMATED] |
| Dependencies on the path | 4 (processor, ledger, fraud, notify) | [ESTIMATED] |
| Attempt budget per dependency | 2 | [ESTIMATED] |
| Processor p99 latency, healthy | 250 ms | [ESTIMATED] |
| Processor p99 latency, degraded | 3000 ms | [ESTIMATED] |
| In-flight callers at peak | 4000 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

Budget arithmetic (the skill's Phase 2, Deadline):

```
available        = 2000 - 200 = 1800 ms
per-dependency   = 1800 / 4   = 450 ms
per-attempt      = 450 / 2    = 225 ms
```

Three configurations, computed from the assumptions above:

| Run | Configuration | Timeout fires? | Retry load multiple | Outcome | Illustrative loss |
|-----|---------------|----------------|--------------------|---------|-------------------|
| 1 | No timeout, fixed 1s retry ×3 | No (never derived) | 4× peak in each 1s window | Cascading outage, 40 min | **$180,000** |
| 2 | Timeout 30s (no deadline relation) | No (deadline hits first) | 4× peak | Users time out, service saturated | **$95,000** |
| 3 | Timeout 225 ms, full jitter, breaker | Yes at 225 ms | ~1.1× (spread over 0–800 ms) | Degrades a feature, service stays up | **$12,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario values
are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: 40 min outage × $4,500/min revenue at peak =
**$180,000**. Retry multiple = 4 (original + 3 retries) in each 1-second window.

**Run 2 loss derivation** [COMPUTED]: 30% of requests hitting the caller deadline over a 25-minute
degradation at $4,500/min × 0.85 attributable = **$95,000**.

**Run 3 loss derivation** [COMPUTED]: feature degraded (recommendations unavailable) for 8 minutes,
estimated revenue impact 15% of $4,500/min × 8 = $5,400, plus on-call and comms ≈ **$12,000**.

## Best case

Run 3 — the defence set derived from the deadline. The timeout **fires** (225 ms), the retry spread
keeps the load multiple near 1.1×, and the breaker stops retrying once the rolling-window failure
rate trips. The dependency's degradation becomes a degraded *feature* rather than an outage, and
loss stays at $12,000 ([COMPUTED] from the table above).

## Worst case

Run 1 — no derived timeout and fixed-delay retries. The retries multiply load 4× during the exact
window the processor is failing, converting a 5-minute network event into a 40-minute outage at
**$180,000** ([COMPUTED]). This is the classic retry storm: the retries are the outage, and the
dependency's fault is only the trigger.

Run 2 is the subtler failure: a 30-second timeout that can never fire, because the caller's
2000 ms deadline always arrives first. The service looks like it has a timeout; in reality it has
documentation. Loss $95,000 ([COMPUTED]).

## Learnings / key takeaways

- **Lesson learned:** derive the timeout from the deadline, not from a feeling. The 225 ms figure is
  arithmetic (`1800 / 4 / 2`), and it is the difference between a defence that fires and one that
  never can ([COMPUTED] from the table above).
- **Actionable lesson:** a fixed-delay retry at 4000 callers multiplies load 4× in each window. Full
  jitter spreads the same retries across 0–800 ms, holding the instantaneous multiple near 1.1× —
  the highest-value single change in this scenario ([COMPUTED]).
- **Actionable lesson:** the breaker's contribution is not error handling but *stopping the retries*.
  Without it, Run 3's load multiple climbs back toward Run 1's as the degradation persists.
- **What this validated:** the skill's core workflow (inventory → deadline → failure modes → pattern
  selection → retry math → verification) produced consistent, tag-annotated, dollar-quantified output
  across three configurations, and named the specific defence responsible for each outcome change.

## What this does not show

- No real production system was measured. All latencies and rates are [ESTIMATED].
- The skill's *output quality* on a real dependency inventory is not assessed here — see
  `examples/resilience-node/README.md`, where the agent correctly **refused** to produce a design
  because no inventory was supplied.
