# Design Gates: Hard Gates Between Phases

## Gate Architecture

### G1: Problem Validation Gate
**Entry criteria:** Problem statement written. Evidence of problem existence (data, interviews, support tickets).
**Exit criteria:** Problem validated by at least one source of evidence not originating from the stakeholder.
**Failure response:** Return to Phase 1 — Problem Framing.

### G2: Exploration Completeness Gate
**Entry criteria:** 3+ approaches considered. Trade-off matrix complete. Constraint inventory documented.
**Exit criteria:** Team can articulate why rejected approaches were rejected with specific rationale.
**Failure response:** Return to Phase 2 — Solution Space Exploration.

### G3: Spec Review Gate (HARD GATE)
**Entry criteria:** All 9 checklist items complete. Design brief produced.
**Exit criteria:** Explicit approval decision. "Yes, we are confident this is the right thing to build."
**Failure response:** Return to the incomplete checklist item. NO EXCEPTIONS.

## Gate Automation
Each gate should have a checklist that can be verified programmatically. Gates are binary: open or closed. No "partially open."
