# Verification Recipes — runnable checks for this skill

> The checks in SKILL.md's Verification section, written as runnable procedures rather than
aspirations.

---

## Verification recipes

The six checks in SKILL.md's Verification section, made runnable.

### The hiding test (boundary, R2)

```
verdict_a = run(verifier, claim + evidence + producer_reasoning)
verdict_b = run(verifier, claim + evidence)
assert verdict_a == verdict_b        # a moving verdict means the boundary is not enforced
```

### The independence assertion (R6)

```
for each producer->verifier pair:
    assert pair.verifier != pair.producer                     # role
    assert pair.verifier.context_seed is None                 # context: not the producer's session
    assert "reasoning" not in pair.verifier.inputs            # information
    assert pair.verifier.model_family != pair.producer.model_family   # model (for judgment checks)
```

Every assertion must be enforceble in the graph, not in a prompt — a prompt-level restriction is a
request, and R2 asks for a boundary.

### The calibration gate (R5)

```
assert len(known_bad_set) >= 10
assert rejection_rate_on_known_bad == 1.0        # all known-bad rejected
assert false_reject_rate < agreed_threshold      # still usable; measure it, do not assume
```

### The metric-pair gate (R4)

```
for each gated target:
    assert target.intent is written_down          # not just a formula
    assert target.harm_metric is not None         # or an accepted risk with an owner
assert gate reads (target, harm_metric)           # the pair, never the target alone
```

### The self-verification scan (R1)

```
for each node with an outputs artifact:
    assert no gate/exit_when reads node.verdict where node also produced the artifact
```

### Re-calibration trigger (CR12)

```
assert calibration_record.model == current_validator_model   # a stale model invalidates the record
```

---
