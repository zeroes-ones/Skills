# Independence Properties — the four axes and how to enforce each

> Independence is a set of four properties, not a label. This file holds the detail and the
enforcement test for each.

---

## The four independence properties

Independence is not a single property, and systems usually claim it while holding only part of it.
The four below are independent of each other: a validator can have any subset. **Independence is
only worth what the weakest axis allows**, so state all four and verify all four (R6).

| Property | Question it answers | Cheapest way to get it | What it does NOT give you |
|----------|--------------------|------------------------|---------------------------|
| **Role** | Is the verifier a different node from the producer? | Any separate node with its own verdict | Anything at all, on its own — a separate node can still be a twin |
| **Context** | Has the verifier been led by the producer's framing? | A fresh context that never saw the producer's session | Protection from shared model blind spots |
| **Information** | Does the verifier see the reasoning, or only the claim and evidence? | Withhold the reasoning trace; pass the artifact + evidence (R2) | Protection from a producer who wrote bad *evidence* |
| **Model** | Do the verifier's blind spots differ from the producer's? | A different model family for judgment-shaped checks | Anything if the check is calibration-free (R5) |

### The enforcement test for each property

A property is only real when a test can fail because of it. Each row below is the test that
*disproves* independence on that axis — cheap, mechanical, and runnable against the graph or the
validator's configuration. The information axis has the hiding test (below); the other three have
an equivalent.

| Property | Enforcement test | What a failure looks like |
|----------|-----------------|--------------------------|
| **Role** | Walk every consequential artifact and assert its approving node id is not the node that produced it; assert no gate or `exit_when` reads the producing node's own verdict. | The same node (or session) appears on both sides — R1. |
| **Context** | Dump the verifier's context seed and assert it is null or empty; assert it does not contain the producer's session id, prior turns, or scratchpad. | The verifier's context was seeded from the producer's session — R3. |
| **Information** | The hiding test: run the validator with the reasoning attached, then without; assert the verdict is identical. | The verdict moves when the reasoning is hidden — R2. |
| **Model** | Read the declared model on both nodes and assert they differ for judgment-shaped checks; for mechanical properties, assert the check is deterministic instead. | Same model family on both sides of a judgment-shaped check — R3. |

Each test must be enforced at the graph edge or node configuration, not requested in a prompt — a
prompt-level restriction is a request, and R2 asks for a boundary.

### Why role alone is worthless

A "separate agent" that shares a model, a context, and the producer's transcript is the same
reasoner wearing a different name. It will agree, and the agreement will feel like confirmation —
which is worse than no check, because it manufactures evidence.

### Why information independence is the highest-leverage axis

Context and model diversity cost money. Withholding the reasoning is nearly free, and it removes
the **most common** failure mode: a validator that reasons along the producer's path, inherits the
same wrong assumption, and approves. The empirical shape is familiar from code review — a reviewer
who reads the author's explanation first reviews the explanation, not the code.

**The enforcement test is mechanical.** Hide the reasoning, re-run the validator, compare verdicts:

```
verdict_with_reasoning    = run(validator, claim + evidence + producer_reasoning)
verdict_without_reasoning = run(validator, claim + evidence)

if verdict_with_reasoning != verdict_without_reasoning:
    # The validator is reading the reasoning. The boundary is not enforced.
else:
    # Consistent — necessary, not sufficient. It may still share model blind spots.
```

The test is one-directional: a matching verdict does not prove independence, but a *moving* verdict
disproves it. That asymmetry is genuinely useful — it catches the failure cheaply.

### The model-diversity decision

```
Is the checked property judgment-shaped (taste, adequacy, intent-match)?
├── Yes → model diversity is worth its cost. Use a different family where feasible.
└── No, it is mechanical (field present, schema valid, test passes) → use a deterministic check.
        Determinism has no blind spots to share and costs less (see SKILL.md, When NOT to Use #5).
```

---
