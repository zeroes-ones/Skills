# The Ladder

<!-- DEEP: 5+min -- the six rungs, what each buys, costs and breaks -->

## The governing idea

Complexity is a **purchase**. Each rung buys a specific capability and charges for it in cost,
latency, failure modes and debuggability. The discipline is to know which capability you needed and
what you paid — because a rung bought without knowing either is how a six-node graph ends up losing
to a single well-written call.

**The default is the bottom rung.** The burden of proof sits with the complexity, not with the
simplicity. That inversion is the whole method.

## Rung 1 — Single call

| | |
|---|---|
| **Buys** | nothing extra; it is the baseline |
| **Costs** | one call; the lowest latency available |
| **Fails when** | the task needs more than one pass, external information, or a decision about its own steps |
| **New failure mode** | none beyond the model's own |
| **Debuggability** | highest — one prompt, one response |

**Always build this first.** It is the reference the climb is measured against, and it occasionally
wins outright. A team that skips it has no way to know whether the next rung helped.

## Rung 2 — Prompt chain

A sequence of calls where each processes the previous one's output, with optional programmatic checks
between the links.

| | |
|---|---|
| **Buys** | decomposition — each step is a simpler task than the whole |
| **Costs** | N calls instead of 1; latency multiplies; the chain's length is fixed |
| **Fails when** | the input type varies enough that one chain is wrong for some inputs |
| **New failure mode** | a link fails, or an earlier step's error propagates |
| **Debuggability** | good — you can see which link failed |

```
input → [step 1] → check → [step 2] → check → [step 3] → output
```

**The trade:** latency for accuracy. Each step is an easier task than the whole, which raises the
per-step success rate — at the cost of multiplying latency and adding N−1 failure points.

## Rung 3 — Routing

A classification step dispatches the input to a specialised path.

| | |
|---|---|
| **Buys** | separation of concerns — each path is optimised for its input class |
| **Costs** | a classification call, plus N paths to build, maintain and evaluate |
| **Fails when** | the classification is unreliable, or the classes are not genuinely separable |
| **New failure mode** | misrouting — the wrong specialist handles the input |
| **Debuggability** | good if routing is logged; poor if it is implicit |

```
input → [classify] → ┬→ path A (for class A)
                     ├→ path B (for class B)
                     └→ path C (for class C)
```

**The maintenance cost is the point.** Each path needs its own prompt, its own eval, and its own
on-call knowledge. Routing is justified when the classes are *genuinely* different — not when one
chain with a conditional sentence would do.

## Rung 4 — Parallelisation

Two distinct forms with different purposes:

| Form | What it does | Buys | Fails when |
|---|---|---|---|
| **Sectioning** | independent subtasks run concurrently | **latency** — the total is the slowest branch | sub-results depend on each other |
| **Voting** | the same task runs N times, results aggregated | **reliability** — through redundancy | the failures are correlated |

| | |
|---|---|
| **Costs** | N× the calls; aggregation logic; partial-failure handling |
| **New failure mode** | partial failure — some branches succeed, some do not |
| **Debuggability** | moderate — the aggregate hides which branch failed |

**The aggregation is the hidden cost.** Combining N results requires a policy: all-must-succeed,
majority, first-success, or weighted. That policy is code to write, test and maintain, and it is
where partial failures become visible.

## Rung 5 — Orchestrator–workers

A central step decomposes the task dynamically, delegates to workers, and synthesises.

| | |
|---|---|
| **Buys** | handling tasks whose sub-steps genuinely cannot be fixed in advance |
| **Costs** | planning tokens, unpredictable cost and latency, the hardest debugging |
| **Fails when** | the action space is open, or the decomposition was knowable all along |
| **New failure mode** | a bad plan — the orchestrator decides a decomposition that cannot work |
| **Debuggability** | lowest of the workflow family — the plan is data, not code |

**The diagnostic question:** if you can write the decomposition down after seeing 20 inputs, it was
knowable — and you needed a chain, not an orchestrator. The orchestrator's justification is precisely
that the decomposition *varies* in ways you cannot enumerate.

## Rung 6 — Bounded graph

Typed nodes, edges, conditions, loops, gates and budgets — the control flow is code, the content is
agentic.

| | |
|---|---|
| **Buys** | auditable, repeatable control flow with verification, escalation and enforcement |
| **Costs** | a manifest to maintain, an engine, and the discipline of every rung below |
| **Fails when** | used for a task the lower rungs serve — the graph is then pure overhead |
| **New failure mode** | configuration error — the graph itself is wrong |
| **Debuggability** | high *because* it is explicit, once the manifest exists |

**The dual nature:** a graph is more machinery and more comprehensible at the same time. Its
justifications are therefore specific:

1. **Repeatability** — the same input must produce the same path, auditably.
2. **Governance** — a regulated flow needs a reviewable route, not just a correct outcome.
3. **Verification** — nodes must substantiate completion, with gates that can fail.
4. **Escalation** — a bounded failure must route somewhere deliberate.
5. **Scale of operation** — many workflows sharing a common execution contract.

**"We wanted an agent, and a graph is the grown-up version" is not on that list.**

## The full ladder, side by side

| Rung | Buys | Cost | New failure | Debug difficulty |
|---|---|---|---|---|
| 1 Single call | baseline | 1 call | — | lowest |
| 2 Chain | decomposition | N calls, N× latency | link failure, error propagation | low |
| 3 Routing | specialisation | classify + N paths | misrouting | low |
| 4 Parallel | latency or reliability | N× calls, aggregation | partial failure | moderate |
| 5 Orchestrator | dynamic decomposition | planning tokens, variable cost | bad plan | high |
| 6 Graph | auditability, governance | manifest + engine | configuration error | moderate (explicit) |

Note the shape: **cost and new failure modes both grow monotonically**, while debuggability does not
fall off a cliff only because rung 6 is explicit. That asymmetry is why the burden of proof belongs
on the climbs.

## Walking it

```text
Start at Rung 1. Measure. Does it pass?

  passes → STOP. Write the exit condition anyway (you may need it later).

  fails  → classify the failure:
             format/structure   → still Rung 1; fix the prompt
             needs information  → retrieval, not a higher rung
             one pass too much  → Rung 2
             input-class variance → Rung 3
             latency or reliability → Rung 4
             decomposition unknown  → Rung 5
             audit/governance/repeatability → Rung 6

  then   → climb ONE rung, measure, and decide again.
```

**Never skip a rung on the way up.** Rung 3 without Rung 2 is possible, but it means the routing path
was never compared against a plain chain for the same inputs — and that comparison is the evidence
that the router earns its maintenance cost.

## Why the ladder runs down

Every rung has an exit condition. A rung added for a reason that has since disappeared is pure cost:
more calls, more latency, more failure modes, more code to read. The exit condition is written at
climb time because that is when the reason is known — nobody remembers it later.

| Rung | Typical exit condition |
|---|---|
| 2 Chain | mean input length halves, or the model's usable context doubles |
| 3 Routing | the input classes stop being separable, or one path's traffic drops below a threshold |
| 4 Parallel | the aggregation cost exceeds the latency saved, or branches become dependent |
| 5 Orchestrator | the decomposition becomes enumerable from the observed inputs |
| 6 Graph | the governance requirement is lifted, or the workflows are retired |

Each is *falsifiable* — which is what makes it a condition rather than an aspiration.

## Checklist

- [ ] The bottom rung was built and measured before any climb (R1)
- [ ] Each rung names the measured failure of the rung below that it addresses (R6)
- [ ] Each rung's own new failure mode is identified and tested
- [ ] Each rung's cost and latency delta is measured or ESTIMATED with its assumption
- [ ] No rung was skipped on the way up without a recorded reason
- [ ] Each rung has a falsifiable exit condition, with a date
- [ ] The graph rung, where used, cites one of its five specific justifications
