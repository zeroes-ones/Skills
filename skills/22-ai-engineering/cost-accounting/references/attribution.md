# Attribution

<!-- DEEP: 5+min -- attributing a run's cost across nodes and phases from spans and run-state -->

## Why a total is not attribution

A run's total answers "how much". It cannot answer "why", and "why" is the only question that leads
to a reduction. This is R5: one run gives you a total, not a cause.

```text
Total: $0.28 for a 6-node run.

Which node?  unknown from the total
Which phase? unknown from the total
Is it the loop? unknown from the total
```

The useful artefact is a **tree**: run → node → phase, with cost at each level.

## The attribution tree

```text
run                                    $0.2840
├── implement            (1 attempt)   $0.0096
├── review               (1 attempt)   $0.0096
├── micro-sdlc-loop      (4 iterations) $0.2304   ← 81% of the run
│   ├── iteration 1      implement+review  $0.0192
│   ├── iteration 2      implement+review  $0.0192
│   ├── iteration 3      implement+review  $0.0192
│   └── iteration 4      implement+review  $0.0192   (+ the gate)
├── ship-gate            (1 attempt)   $0.0096
└── residual             (unattributed) $0.0248
```

**The finding is visible in the shape, not in a number**: 81% of the run is the loop, and each
iteration is cheap. The reduction is therefore "fewer iterations", not "cheaper node" — and that
distinction is exactly what a total cannot show.

## Node-level attribution

From run-state, each node record can carry its own cost:

```json
"nodes": {
  "implement": {"status": "done", "verdict": "pass", "iterations": 1,
                "cost": {"tokens_in": 1200, "tokens_out": 400,
                         "cost_usd": 0.0096, "reported": true}}
}
```

From spans, the same data arrives as attributes on `workflow.<name>.node.<id>`, so any span backend
can produce the tree without custom accounting.

| Source | Gives | Limitation |
|---|---|---|
| run-state `nodes[*].cost` | per-node cost, per run | needs the runner to accumulate it |
| OTel spans | per-node cost plus timing, joinable across runs | needs an exporter and a backend |
| Provider billing API | real spend, authoritative | coarse: per-key, per-day, not per-node |
| Ablation | cost per node *by difference* | expensive, and the control must be re-measured |

**Order of preference:** run-state or spans first (cheap and per-node), billing for ground truth,
ablation only when the others are unavailable.

## Phase-level attribution

The phase split is where the money usually is, and it is invisible at node level.

| Phase | What it is | Why it matters |
|---|---|---|
| **First attempt** | the node's baseline work | the irreducible cost of the work |
| **Retry / iteration** | repeated attempts after a failure verdict | the loop's cost — usually the largest term |
| **Escalation** | gates, reroutes, human handoffs | the cost of handling failure |

```text
Same node, two runs:
  run A: review, 1 attempt      $0.0096
  run B: review, 5 attempts     $0.0480

Node-level attribution sees "review costs $0.0096–$0.0480" and stops.
Phase-level attribution sees "the retry phase is 80% of this node's cost" and
names the lever: the exit condition is too hard to satisfy.
```

**The rule:** attribute to the phase before proposing a fix. "The model is expensive" and "the loop
runs five times" describe the same spend and imply opposite remedies.

## The three attribution questions

Ask them in this order; the first that produces an answer usually identifies the levers.

```text
1. IS IT THE LOOP?
   iteration count × per-iteration cost. If loops dominate, the lever is the
   exit condition, the max_iterations, or the escalation timing — not the prompt.

2. IS IT ONE NODE?
   rank nodes by cost. If one node dominates and iterations are low, the lever is
   that node's model, its prompt, or its context payload.

3. IS IT A PRICE?
   compare cost per token across periods. If tokens are flat and cost rose, the
   lever is routing or the contract, not the code.
```

Each answer points at a different skill (`agentic-complexity-ladder` for shape, `token-efficiency`
for per-call, `finops-engineer` for contract), which is why the question order matters.

## Ablation, when you must

Where per-node data does not exist:

```text
1. Baseline: run the workflow, record the total (median of ≥5 runs).
2. Change ONE node's model or prompt.
3. Re-run with everything else identical.
4. Difference = that node's contribution to the total.
5. Restore, and re-measure the baseline (guards against drift).
```

**Two rules that make it valid:** one change at a time, and the baseline re-measured. Without the
second, a workload that got cheaper for unrelated reasons is credited to the node you changed.

## Reporting shape

```text
Cost attribution — <workflow> — <date>

Method: 12 runs, median, executor-reported usage ([VERIFIED])
Total:  $0.2840 median

| Node / phase            | Cost     | Share |
|-------------------------|----------|-------|
| micro-sdlc-loop         | $0.2304  | 81.1% |
|   ↳ iterations 1–4      | $0.0768  |       |
|   ↳ escalation/gate     | $0.1536  |       |   ← the real finding
| implement (1 attempt)   | $0.0096  |  3.4% |
| review (1 attempt)      | $0.0096  |  3.4% |
| ship-gate               | $0.0096  |  3.4% |
| residual                | $0.0248  |  8.7% |
                          ---------
                          $0.2840

Reading: the loop is 81%, and within it the ESCALATION path is twice the
iterations themselves. The lever is escalation timing, not iteration cost.
```

The narrative line is the deliverable. A table without it leaves the reader to infer, and they will
infer "the expensive thing is the thing with the biggest number", which is usually the node and not
the phase.

## Checklist

- [ ] Attribution exists at node level, not only as a run total (R5)
- [ ] The phase split is computed where a loop exists (first attempt / retry / escalation)
- [ ] The attribution sums to the total, with the residual stated rather than distributed
- [ ] The largest term is reported as a candidate, and the narrative names the lever
- [ ] The three questions are asked in order: loop, then node, then price
- [ ] Ablation is used only when per-node data is unavailable, one change at a time, with the
      baseline re-measured
- [ ] The method, the run count and the measurement status accompany the attribution
