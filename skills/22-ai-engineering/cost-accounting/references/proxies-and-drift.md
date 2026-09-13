# Proxies and Drift

<!-- STANDARD: 3min -- when a proxy is acceptable, how it drifts, and when to replace it -->

## What a proxy is, and when it is legitimate

A proxy is a quantity that correlates with cost but is not cost: steps, calls, tokens, wall-clock,
node count.

**A proxy is legitimate when it is (a) labelled as a proxy, (b) accompanied by its drift condition,
and (c) replaced the moment the real quantity is measurable.** It is illegitimate when presented as
cost.

| Proxy | Correlates while | Drifts when |
|---|---|---|
| `steps_used` | every node costs about the same | one node uses a dearer model, or a node's context grows |
| API call count | every call has similar size | caching changes the effective cost of a call |
| tokens (unpriced) | the model mix is stable and prices are flat | a model swap, a price change, a cache discount |
| node executions | per-node cost is uniform | per-node model routing is introduced |
| wall-clock | spend is proportional to time | a slow cheap call vs a fast dear one |

**The drift is always silent.** That is what makes proxies dangerous: a proxy does not fail, it
becomes wrong. The correlation that held when it was chosen stops holding, and nothing reports it.

## The specific drift that bit this repository

```text
Before: budget.steps_used was the only cost proxy (skill-sli-report called it
        "cost proxy" in its own docstring), and export-traces carried
        "cost": 0.0 placeholders.

Problem: steps measure activity. A 40-step run of cheap classification calls and a
         40-step run of premium reasoning calls have the same step count and up to
         100× different bills.

Fix:    the executor reports usage; the runner accumulates real cost per node and
        per run; the proxy is retired for the measured quantity.
```

The lesson is general: **a proxy is technical debt with an interest rate**, and the rate is invisible
until something changes the correlation.

## Detecting proxy drift

You cannot detect it by watching the proxy — it keeps behaving. You detect it by reconciling against
something real.

```text
Drift check (do this whenever a proxy is in use):
  1. Record proxy value and TRUE cost (invoice or measured usage) for a period.
  2. Compute the ratio: true_cost / proxy_value.
  3. Is the ratio stable across periods and across workflows?
     ├── Stable  → the proxy is still valid; keep the ratio to convert, and re-check
     │             whenever the model mix, cache policy or prices change
     └── Moving  → the proxy has drifted. Replace it, or re-fit the ratio and
                   record the new basis and its date.
```

**The trigger conditions** — re-check after any of these, because each breaks a correlation:

- a model swap or a new model in the mix
- a price change
- a cache policy change or a hit-rate move
- per-node model routing introduced
- a change to loop bounds or escalation policy
- a change to the context payload's size

## The conversion discipline

Where a proxy must be used, convert it honestly:

```text
NOT:  "the run cost $0.02"                    (a proxy presented as cost)
BUT:  "40 steps; at the measured $0.00048/step basis (as of <date>) ≈ $0.0192 [COMPUTED]"
```

The second statement is usable *and* auditable: the basis is stated, the date is stated, and a reader
can challenge the assumption. The first is a proxy wearing a cost figure's clothes.

## Deciding whether to replace a proxy

```text
Is the real quantity measurable?
├── No  → the proxy is the honest best option. Label it, state its drift condition,
│         and record that measurement is unavailable so it is revisited.
└── Yes → replace it. Is the replacement work justified?
    ├── The proxy is used for a DECISION (a gate, a budget) → replace it. A decision
    │   on a drifting number is a decision on luck.
    └── The proxy is used for a TREND only → a labelled proxy may be acceptable, but
        state that it cannot support an absolute claim.
```

**The line:** proxies may inform a trend; they must not gate a decision. Anything with a threshold
attached needs the real quantity.

## Why "unmeasured" beats "proxied" in some cases

```text
Option A: report steps as cost        → a number, plausibly wrong, presented as knowledge
Option B: report "cost unmeasured"    → no number, honestly stated

B is better whenever a decision rests on it, because B prompts the fix while A
suppresses it. A proxy's worst property is that it looks like an answer.
```

This is the same principle as `measurement-status.md`, applied to proxies: the system must be able to
say "I do not know" rather than produce a confident wrong number.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| A proxy presented as cost | a drifting number used as knowledge |
| An unlabelled proxy | the reader cannot know the correlation is conditional |
| A proxy gating a decision | the threshold is met or missed on luck |
| A proxy with no drift condition stated | nobody knows when to re-check |
| Re-fitting the ratio silently | the change of basis is invisible in the trend |
| Keeping a proxy after measurement becomes possible | technical debt with an invisible interest rate |
| A proxy across a model-mix change | the correlation is broken exactly when it matters |

## Checklist

- [ ] Any proxy is labelled as a proxy wherever it appears (R2)
- [ ] The proxy's drift condition is stated, so the re-check trigger is known
- [ ] Proxies inform trends, never gate decisions
- [ ] A proxy in use is reconciled against a real quantity (invoice or measured usage) periodically
- [ ] Conversion to a cost estimate states the basis and its date, and is tagged `[COMPUTED]`
- [ ] The proxy is replaced as soon as the real quantity is measurable
- [ ] Re-checks are triggered by model, price, cache, routing, loop and payload changes
- [ ] Where measurement is genuinely unavailable, that fact is recorded so the gap is revisited
