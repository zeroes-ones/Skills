# Graph Justification

<!-- STANDARD: 3min -- when an auditable graph is warranted, including for governance -->

## The rung with a dual nature

A bounded graph — typed nodes, edges, conditions, loops, gates, budgets — is simultaneously **more
machinery** and **more comprehensible** than the rungs below it. That dual nature is why its
justifications are specific and narrow.

| | |
|---|---|
| **Buys** | auditable, repeatable control flow with verification, escalation and enforcement |
| **Charges** | a manifest to maintain, an engine to run, and the discipline of every rung below it |
| **New failure mode** | configuration error — the graph itself is wrong |
| **Debuggability** | **high**, because the structure is explicit — once the manifest exists |

A graph is the only rung that *increases* debuggability as it adds machinery. That is its real
advantage, and it is only an advantage when the structure is actually needed.

## The five justifications, and only these

| Justification | The requirement it serves | Signal you need it |
|---|---|---|
| **Repeatability** | the same input must produce the same path, auditably | "we must be able to show how this result was reached" |
| **Governance** | a regulated flow needs a reviewable route, not just a correct outcome | an auditor, regulator or certification asks for the route |
| **Verification** | nodes must substantiate completion, with gates that can fail | a claim of completion must be *checked*, not asserted |
| **Escalation** | a bounded failure must route somewhere deliberate | "what happens when it gives up" has a required answer |
| **Scale of operation** | many workflows sharing a common execution contract | 10+ workflows needing the same budget, loop and gate semantics |

**"We wanted an agent, and a graph is the grown-up version" is not on the list.**

## The governance case, stated properly

The most commonly misapplied justification, and the clearest example of why the rung has its own
criteria. A regulated flow may need an explicit graph **even where a single call would produce the same
answer**, because the requirement is a reviewable path rather than an outcome.

```text
Requirement: a credit decision must be reproducible and reviewable —
             an auditor asks "how was this decided?" and the answer must be a path

Single call: correct answer, no reviewable path → fails the requirement
Graph:      the decision route is a manifest, each node has a recorded verdict
            and evidence, gates can fail → meets the requirement

The graph is justified by GOVERNANCE, not by capability. Stating which is
what makes the justification audit-able itself.
```

**The discipline this imposes:** if the justification is governance, then the graph's *structure* is
part of the requirement, and simplifying it away is a compliance change — not an optimisation.

## The verification case

The rung's other strong justification, and the one most often neglected.

```text
Without verification:  a node says "done" and the graph advances
With verification:     a node must substantiate its completion
                       (evidence present, declared criteria covered)
                       → an unsubstantiated claim does NOT advance the graph

That is the difference between a pipeline that reports completion and one that
CHECKED it — and it is not obtainable at the lower rungs, where "done" is
whatever the model said.
```

**The cost is real:** every node now needs an evidence contract, and every contract can fail. That is
the point — a gate that cannot fail is not a gate.

## The shape of an unjustified graph

The symptoms that the graph rung was entered for a lower rung's problem:

| Symptom | What it means |
|---|---|
| One node does all the work | the graph is decorative; a single call plus a wrapper would serve |
| No node has a `workflow:` contract | verification is not being used — then why the engine? |
| No budgets declared | enforcement is not being used |
| No gates or escalation paths | the escalation justification does not apply |
| Loops that never iterate more than once | the loop semantics are unused |
| Nodes that always run in strict sequence | a chain (Rung 2) is the same thing, cheaper |
| The manifest changes more often than the prompts | the graph is being used as configuration |

**The "one node does all the work" symptom is the most common and the most telling:** a graph with six
nodes where five are pass-throughs, and one contains the entire prompt, is a single call wearing a
manifest.

## The cost of an unjustified graph

| Cost | Detail |
|---|---|
| A manifest to maintain | updated alongside every prompt change |
| An engine to operate | version, behaviour, upgrades |
| Configuration failure modes | the graph can be wrong in ways the prompt cannot |
| Slower iteration | changing a prompt may mean changing a manifest |
| Cognitive load | new engineers learn the structure *and* the prompts |
| Enforcement machinery unused | budgets, gates and contracts that nothing exercises |

None of these is large individually. Together they are the reason an unjustified graph is worse than
the chain it replaced, despite being more explicit.

## The decision

```text
Does the requirement need a REVIEWABLE PATH rather than just a correct outcome?
├── Yes (repeatability, governance, verification, escalation) → the graph is justified
│   └── state which justification, explicitly
└── No ↓
    Are 10+ workflows sharing a common execution contract?
    ├── Yes → justified on the scale-of-operation ground
    └── No  → the graph is not justified. Use the rung below:
        ├── fixed sequence           → Rung 2 (chain)
        ├── enumerable variation     → Rung 3 (routing)
        ├── unpredictable variation  → Rung 5 (orchestrator, bounded)
        └── latency or reliability   → Rung 4 (parallelism)
Finally, ALWAYS:
  └── Every node must name the failure it addresses, and every rung must have an
      exit condition (R4) — a graph with no exit condition is permanent
```

## Recording a graph decision

```text
Rung:          6 (bounded graph)
Baseline:      Rung 3 routing — 84% pass, but no reviewable path and no
               verification of completion claims

Justification: VERIFICATION + GOVERNANCE
               - verification: node completion must be substantiated, with gates
                 that can fail (regulatory internal audit requirement)
               - governance: the decision route must be reviewable on demand

Nodes:         6, each with a `workflow:` completion contract
               each names the measured failure it addresses
Budgets:       max_steps 40; cost cap enforced
Gates:         a human gate on escalation, with a recorded reason
Trade:         a manifest to maintain; an engine to operate; slower prompt
               iteration; configuration failure modes
Exit:          if the audit requirement is lifted, this collapses to a chain
               (check with the compliance owner, 2027-06)
```

## Checklist

- [ ] One of the five justifications applies, and is stated explicitly
- [ ] If the justification is governance, the structure is acknowledged as part of the requirement
- [ ] Every node names the measured failure it addresses (R6)
- [ ] Every node has a completion contract, or the verification justification does not apply
- [ ] Budgets are declared and enforced, or the enforcement machinery is unused
- [ ] Gates and escalation paths exist, or that justification does not apply
- [ ] Loops actually iterate more than once, or a chain would serve
- [ ] No node is a pass-through whose work another node does
- [ ] An exit condition exists, owned by whoever owns the requirement
