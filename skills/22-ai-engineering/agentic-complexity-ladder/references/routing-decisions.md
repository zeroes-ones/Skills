# Routing Decisions

<!-- STANDARD: 3min -- when a classifier earns its maintenance cost -->

## What routing buys, and what it charges

```
input → [classify] → ┬→ path A
                     ├→ path B
                     └→ path C
```

| Buys | Charges |
|---|---|
| separation of concerns — each path optimised for its class | one classify call per run |
| higher per-path accuracy | N prompts to write, evaluate and maintain |
| the ability to use different models per class | N evals, N on-call knowledge areas |
| bounded scope for each path's prompt | a new failure mode: misrouting |

**The maintenance cost is the decisive one.** Each path is a small product: its own prompt, its own
eval, its own failure modes, its own reason to change. A router is justified only when the classes are
*genuinely* different — not when one chain with a conditional sentence would serve.

## The clustering test

The test that decides whether routing can help at all.

```text
1. Take the measured failures from the current rung (say, a chain).
2. Ask: do the failures CLUSTER by input type?
   ├── Yes, failures concentrate in identifiable classes
   │   → routing can help: the failure is about the input class
   └── No, failures are randomly distributed across inputs
       → routing CANNOT help: the failure is in the work, not the class
         (a longer prompt, a better model, or a different rung)
```

**Worked example:**

```text
Chain baseline: 71% pass on 20 cases, 6 failures.

Failure distribution A (clusters):
  cases 04, 11, 19  → all "invoice" inputs   ← 3 of 3 invoice inputs fail
  cases 07, 13      → "receipt" inputs        ← 2 of 8 receipts fail
  case 18           → "statement"              ← 1 of 9 statements fail

Failure distribution B (random):
  cases 03, 07, 11, 14, 18, 20  → mixed classes, no pattern
```

**A justifies routing.** The invoice path is 100% broken and needs a different approach; separating it
lets the other 17 cases use the chain that already works for them.

**B does not.** The failures are scattered, so a router would add a classify call, three paths and a
misroute mode, and fix nothing — because there is no class to separate.

## The separability requirement

Even with clustering, the classification must be *reliable*.

| Requirement | Why |
|---|---|
| The classes are distinguishable from the input | if a human cannot label it confidently, a classifier cannot |
| The classifier's accuracy is measured | 85% routing accuracy means 15% of inputs get the wrong path |
| The misroute cost is acceptable | a misroute on a rare class is cheap; on a critical one, expensive |
| Class boundaries are stable | if the classes shift monthly, the classification must be re-measured continually |

**Measure the routing accuracy before trusting the router.** A router nobody has measured is a
distribution mechanism, not a control.

## The traffic question

A path for 2% of traffic costs as much to maintain as one for 50%.

```text
path A: 80% of traffic   → clearly worth its maintenance
path B: 18% of traffic   → probably worth it
path C:  2% of traffic   → maintaining a prompt, an eval and on-call knowledge for 2%
```

**Options for a low-traffic path:**

| Option | When |
|---|---|
| Fold it back into the main path with a conditional | the difference is a prompt sentence, not an approach |
| Accept slightly lower quality on the rare class | the class is rare and its bar is lower |
| Route it to a human | the class is rare and its cost of error is high |
| Keep it, if its cost of error justifies the maintenance | a rare class can be critical — a legal or medical input, for example |

The last row is the exception worth stating: **rarity does not imply low stakes.**

## When routing is the wrong rung

| Situation | Better rung |
|---|---|
| One chain with a conditional sentence serves every class | Rung 2 |
| Failures do not cluster | a better prompt, a stronger model, or retrieval |
| The classes are not reliably distinguishable | do not route on an unreliable signal |
| The work can be done simultaneously across classes | Rung 4 |
| The decomposition varies *unpredictably* | Rung 5 (the orchestrator's case, not the router's) |

**Routing versus orchestrator, precisely:** a router selects among a *fixed, known* set of paths. An
orchestrator decides the decomposition *dynamically*. If you can enumerate the paths, it is a router;
if you cannot, it is an orchestrator.

## Recording a routing decision

```text
Rung:      3 (routing)
Baseline:  Rung 2 chain — 71% pass, 20 cases
Test:      clustering — invoice inputs fail 3/3, others 17/20 pass
Classes:   invoice (15%), receipt (40%), statement (45%)
Classifier accuracy (measured): 96% on the 20-case set
Misroute cost: invoice→statement path produces a wrong layout, caught by validation
Trade:     +1 call (~$0.004), +0.3 s latency, 3 paths to maintain
Exit:      if invoice traffic falls below 5% of total, merge the path back (check 2027-01)
Eval:      cases 04, 11, 19 (the invoice failures) — must pass on the invoice path
```

Every field matters, and the `Classifier accuracy` line is the one most often missing.

## Checklist

- [ ] The clustering test passed — failures concentrate in identifiable classes (R6)
- [ ] The classes are reliably separable from the input
- [ ] Classifier accuracy is measured, on a real task set
- [ ] The misroute cost is assessed, and is acceptable or mitigated by validation
- [ ] Per-class traffic counts are known, and low-traffic paths have a stated justification
- [ ] The router was compared against a single chain with conditional handling
- [ ] The failing cases became the router's acceptance eval
- [ ] The trade is recorded: the classify call, the latency, the paths to maintain
- [ ] An exit condition exists, tied to traffic share
