# Run-Level Levers

<!-- DEEP: 5+min -- node count, iteration count, escalation timing, cross-run caching, per-node model routing -->

## Two families of lever, and why they are confused

| Family | What it changes | Owner | Typical effect |
|---|---|---|---|
| **Per-request** | the cost of one call — tokens, cache, prompt, output length | `token-efficiency` | a fraction of a call's cost |
| **Run-level** | how many calls the run makes | **this skill**, with `agentic-complexity-ladder` | a multiple of the run's cost |

**The confusion is the reason "we optimised the prompt" sometimes moves the bill by nothing.** A
prompt that saves 20% per call on a run that makes 40 calls saves 20% of the *per-call* term. A run
that makes 12 calls instead of 40 saves 70% of the total. The second is larger, and it is a graph
decision.

Attribute first (`attribution.md`) — the loop, then the node, then the price. Only the first two
have run-level levers.

## Lever 1 — node count

```text
cost_per_run ≈ Σ (node_cost × node_calls_per_run)

Removing or merging a node removes its cost entirely, plus the handoff overhead
around it (a payload serialised, a summary generated, a verdict evaluated).
```

| Technique | Note |
|---|---|
| Remove a node whose work is implied by another | the cheapest node is the one that does not exist |
| Merge two nodes that always run together | fewer handoffs, one context load instead of two |
| Replace a node with a deterministic check | a validator in code costs nothing per run |
| Replace a node with a cheaper model | not removal — see Lever 5 |

**The guard:** each removal must preserve the outcome. This is a `agentic-complexity-ladder`
judgement, made with this skill's measured cost attached.

## Lever 2 — iteration count (usually the largest)

```text
A loop of N iterations multiplies the loop's member cost by N.

Loop cost = N × Σ(member cost)
```

Four independent levers on `N`:

| Lever | Mechanism | Risk |
|---|---|---|
| **Loosen the exit condition** | accept pass-with-notes, or a lower threshold | quality falls; assert it |
| **Lower `max_iterations`** | cap the multiplier | the run escalates more often instead |
| **Fix the upstream cause** | make the first attempt more likely to pass | the real fix, and the largest win |
| **Escalate earlier** | trade iterations for an escalation | escalations are expensive; compare |

**The trade that must be computed, not assumed:**

```text
Option A: let the loop run to 6 iterations
  expected cost = (probability of converging by N) × N × member_cost
Option B: escalate after 2 iterations
  cost = 2 × member_cost + escalation_cost × P(escalate)

Compute both. Escalating "early" is a saving only when the escalation is
cheaper than the iterations it replaces — which is often NOT true, because
an escalation can involve a human gate.
```

**The upstream fix is the one that actually reduces cost.** A loop that iterates four times because
the first attempt is systematically wrong is a prompt or context problem, not a loop-policy problem;
tightening the loop just moves the failure.

## Lever 3 — escalation timing and cost

Escalations are the most expensive per-unit action in most graphs, because they involve a gate, a
reroute, or a human.

| Escalation | Typical cost | Lever |
|---|---|---|
| Agent gate with a reroute | one extra node, plus a fresh window | tighten the reroute's channel selection |
| Human gate | a human's time, in latency and attention | reduce escalations by fixing upstream, not by lowering the bar |
| Terminal escalation | the run produced nothing | the most expensive outcome; measure its rate |

**Measure the escalation rate as a cost metric.** `escalation_rate × escalation_cost` is often the
largest single term in a fleet's bill, and it is invisible in a per-run average because most runs do
not escalate.

## Lever 4 — cross-run caching

The only lever that makes cost sublinear in volume.

| Cache | Saves | Condition |
|---|---|---|
| Prompt-prefix cache | the repeated prefix of a shared system prompt | stable prefix across runs (see `token-efficiency`) |
| Result cache | an identical node's output, reused across runs | the inputs are genuinely identical |
| Retrieval cache | a repeated lookup's results | the corpus is stable within the TTL |
| Compiled skill/context cache | the loaded context for a recurring node | the node's inputs repeat |

**The measured hit rate is the only number that matters.** A cache designed for a hit rate that never
materialises saves nothing and adds complexity. Measure it, and forecast from the measured rate, not
the intended one.

**The safety constraint:** never cache across tenants or authorization scopes (Anti-Hallucination).
A cross-tenant cache hit is a data leak, not a saving.

## Lever 5 — per-node model routing

Not run-level in structure, but the largest *per-node* lever and often the best single change.

```text
A 4-node graph where node 3 is high-volume and low-difficulty:

  all nodes on the premium model:  $0.0096 × 4 = $0.0384
  node 3 routed to a cheaper model: $0.0096 × 3 + $0.0015 = $0.0303   (−21%)

  the same change on a 40-call run:  40 × 0.0096 = $0.384
                                     39 × 0.0096 + 1 × 0.0015 = $0.377  (−2%)

Routing pays where the node's volume is high. On a run dominated by a loop,
route the LOOP's node, not the pipeline's nodes.
```

**The measured pair:** cost *and* quality, per node. A cheaper model on a node whose verdict gates
the rest of the run can cost more in retries than it saves in rate — which the cost-per-success
metric will show and a per-call comparison will not.

## Choosing a lever

```text
Attribution says:
├── the LOOP dominates →
│   ├── is the first attempt systematically failing? → fix upstream (Lever 2, real fix)
│   ├── is the exit condition very strict?           → loosen it, assert quality
│   ├── is max_iterations high?                      → lower it, expect more escalations
│   └── is an escalation cheaper than iterations?    → escalate earlier (compute it)
├── ONE NODE dominates →
│   ├── is it high volume?                           → route its model (Lever 5)
│   └── is it one call?                              → per-request levers (`token-efficiency`)
├── the PIPELINE structure dominates →
│   └── node count (Lever 1), with `agentic-complexity-ladder` on the outcome
└── VOLUME dominates →
    └── caching (Lever 4), measured hit rate
```

## The measurement discipline

Every run-level change is a change to the graph, so it needs the comparison discipline from
`cost-per-success.md`:

1. Fix the cohort, the method and the price basis.
2. Measure cost **and** quality and success rate.
3. Report the delta on cost per successful outcome.
4. State which family the improvement came from (run-level or per-request).

Step 4 is what stops a run-level win being credited to a prompt change, and vice versa — the
confusion that makes teams repeat the wrong optimisation.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Optimising the prompt for a loop problem | moves a constant, not the multiplier |
| Lowering `max_iterations` without measuring escalations | trades iterations for a possibly dearer escalation |
| Tightening a loop whose first attempt is systematically wrong | moves the failure; does not fix it |
| Caching without measuring the hit rate | complexity with no saving, and a forecast built on an intention |
| Caching across tenants | a data leak, not a saving |
| Routing a node's model on rate alone | retries can exceed the saving; measure cost per success |
| Treating a per-call saving as a run saving | conflating the two families |
| Removing a node without asserting the outcome | a `agentic-complexity-ladder` decision made on cost alone |

## Checklist

- [ ] Attribution has identified which family the cost sits in before any lever is chosen
- [ ] A loop-dominated cost was checked for a systematically-failing first attempt (the real fix)
- [ ] Escalation cost per escalation is measured, not assumed, before trading iterations for it
- [ ] `max_iterations` changes are measured on cost **and** escalation rate
- [ ] Cache hit rate is measured, and no cache crosses a tenant or authorization boundary
- [ ] Model routing is justified by measured cost per successful outcome, not by rate
- [ ] Node removals carry a `agentic-complexity-ladder` outcome justification
- [ ] Every change reports its delta on cost per success, and names the lever family
