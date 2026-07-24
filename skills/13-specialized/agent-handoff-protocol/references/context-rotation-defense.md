# Context Rotation Defense — 12 Patterns to Prevent Context Rot

Context rot: the progressive degradation of decision quality as context is
passed through multiple agent handoffs. Each handoff loses ~5-15% fidelity.
After 5+ handoffs, downstream agents operate on corrupted or incomplete context.

## The 12 Defense Patterns

### Pattern 1: Immutable Decision Anchors
Freeze decisions after N handoffs. Once frozen, they become constraints.
**Rule:** After 3 handoffs, a decision graduates from "decision" to "constraint."

### Pattern 2: Checksum Chain
Every handoff includes a SHA-256 checksum of the previous handoff state.
**Detection:** Checksum mismatch → handoff chain tampered → abort pipeline.

### Pattern 3: Periodic Re-Origin
Every 3 handoffs, re-derive context from original source (PRD, ADR, spec)
instead of chaining from previous handoff. Breaks error accumulation.

### Pattern 4: Confidence Decay
Each handoff reduces confidence of inherited decisions by one level.
`high → medium → low → treat_as_question`. Forces re-validation.

### Pattern 5: Constraint Inheritance Audit
Before accepting a handoff, verify all `non_negotiable: true` constraints
from ALL prior handoffs are still present. Missing constraint → reject.

### Pattern 6: Decision Contradiction Detection
Compare new decisions against ledger. If new decision contradicts
prior (even implicitly), surface conflict before proceeding.

### Pattern 7: Token Budget Watermark
Every handoff records token_budget_before and token_budget_after.
If budget > 12,000 after pruning, reject until pruner runs again.

### Pattern 8: Artifact Freshness Check
Artifacts older than 2 pipeline stages without re-validation are
marked `stale`. Stale artifacts blocked from being used as input.

### Pattern 9: Double-Blind Verification
For critical decisions (confidence=low, cost_of_reversal=prohibitive),
require a second agent (debate topology) to independently verify.

### Pattern 10: Rollback Points
Mark every 3rd handoff as a rollback point. If context rot detected,
pipeline rolls back to last rollback point and re-derives.

### Pattern 11: Progressive Disclosure Anchoring
Each agent receives only Tier 1 (critical). If it needs more, it
requests Tier 2 (relevant). Never auto-load Tier 3 (noise).

### Pattern 12: Termination Condition
If 3 or more `open_questions` accumulate without resolution, pause
pipeline. Escalate to human or supervisor agent. Don't compound uncertainty.

## Rot Severity Levels

| Level | Handoffs | Symptom | Response |
|-------|----------|---------|----------|
| Green | 0-2 | No detectable drift | Normal operation |
| Yellow | 3-4 | Minor inconsistencies in rationale | Run Pattern 3 (Re-Origin) |
| Orange | 5-6 | Contradictory decisions appearing | Run Pattern 9 (Double-Blind) |
| Red | 7+ | Constraints missing, decisions orphaned | Abort pipeline, restart from source |
