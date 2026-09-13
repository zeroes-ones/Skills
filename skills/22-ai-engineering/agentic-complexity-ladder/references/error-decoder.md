# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. A six-node graph that a single call matches

**Symptom:** the graph works, and so does the one-call version built for comparison.
**Mechanism:** complexity was added without a measured baseline, so no rung has a failure it addresses
(R1). Nothing failed, so nothing prompted an investigation — an over-built system works.
**Diagnosis:** build the bottom rung on the real task set and compare quality, cost and latency.

**Fix:** measure both; remove the nodes that a single call renders unnecessary.
**Recurrence guard:** the bottom-rung baseline exists before any climb (CR2).

## 2. Quality is worse than the version with fewer rungs

**Symptom:** a more sophisticated design performs worse.
**Mechanism:** each rung adds its own failure mode — a chain mislinks, a router misroutes, a fan-out
partially fails — and none of them was tested.
**Diagnosis:** does each rung have a test for the failure it introduces?

**Fix:** identify each rung's own failure mode and test it; fix the mislinking or misrouting.
**Recurrence guard:** the new-failure test per rung (CR8).

## 3. Cost doubled and nobody can say which change caused it

**Symptom:** a regression that cannot be attributed.
**Mechanism:** two rungs changed in one step, so the improvement or regression could come from either
(R3).
**Diagnosis:** does the diff add more than one rung's mechanism?

**Fix:** revert to the lower rung, re-measure, then re-apply one change at a time.
**Recurrence guard:** one rung per change, measured separately (CR7).

## 4. An agent loops without converging

**Symptom:** an agentic loop that retries until its budget is exhausted.
**Mechanism:** agency was applied where the steps were knowable in advance (R2). The failure is not in
the loop policy; it is that the loop should not exist.
**Diagnosis:** can you write the steps down before seeing the input?

**Fix:** replace with a deterministic chain; measure the difference.
**Recurrence guard:** the predictability check before granting agency (CR6).

## 5. Nobody can simplify the system

**Symptom:** every node is defended as "probably needed"; no one can name why.
**Mechanism:** no exit criteria and no recorded rationale — the complexity became permanent by default
(R4).
**Diagnosis:** does every rung have a written, falsifiable exit condition with a date?

**Fix:** audit by removal — take each node out, run the eval, decide.
**Recurrence guard:** exit conditions written at climb time (CR9).

## 6. A router misroutes and the wrong path handles the input

**Symptom:** intermittent incorrect handling that correlates with input type.
**Mechanism:** the classification is unreliable and was never measured; the classes may not be
genuinely separable.
**Diagnosis:** measure the routing accuracy on a real task set.

**Fix:** measure it; merge unreliable paths; apply the clustering test to the failures.
**Recurrence guard:** routing accuracy measured before trust (see `routing-decisions.md`).

## 7. Latency tripled with no quality gain

**Symptom:** a chain or fan-out added, and the outcomes unchanged.
**Mechanism:** the rung was added for a quality problem it cannot solve — a chain trades latency for
per-step accuracy, and if one call was already accurate, the trade buys nothing.
**Diagnosis:** compare against the single-call baseline.

**Fix:** remove the rung; it addressed no measured failure.
**Recurrence guard:** the failure is classified before the rung is chosen (CR4).

## 8. An unbounded agent took an unauthorised action

**Symptom:** the system did something outside the intended scope.
**Mechanism:** agency was granted over the action space, not merely over the routing
(Anti-Hallucination). That is a security decision made by accident.
**Diagnosis:** can you write the complete list of permitted actions?

**Fix:** bound the action space to an allow-list; escalate to `appsec-engineer`.
**Recurrence guard:** the action-space bound (CR11).

## 9. The design was built for a volume that never arrived

**Symptom:** sophisticated machinery handling a fraction of the anticipated load.
**Mechanism:** complexity justified by anticipated rather than measured volume (R5).
**Diagnosis:** is there a measured or derived volume figure behind the complexity?

**Fix:** derive the volume; show where the simpler design fails; remove the rest.
**Recurrence guard:** no complexity rests on anticipation alone (CR10).

## 10. A new team cannot modify the system

**Symptom:** changes take far longer than the code's size suggests.
**Mechanism:** nothing records which rung exists for which reason, so every change requires
reconstructing the design intent.
**Diagnosis:** can a reviewer see why each node exists, from the repository?

**Fix:** record each rung, its failure and its exit condition.
**Recurrence guard:** the rationale is durable (CR14).

## 11. A budget that cannot trip

**Symptom:** a declared cost or step budget that has never engaged.
**Mechanism:** either the budget is far above any observed value, or the run is unmeasured so the
budget cannot be evaluated. In both cases it implies a control that is not operating.
**Diagnosis:** has the budget ever failed, and is the underlying quantity measured?

**Fix:** set the budget from the measured distribution; confirm the quantity is measured.
**Recurrence guard:** budgets derive from measurements, and unmeasured runs are visible.

## 12. A gate that cannot fail

**Symptom:** a verification gate that has never rejected anything.
**Mechanism:** the gate's criteria are trivially satisfied, or the node's contract is not enforced.
**Diagnosis:** construct a deliberately unsubstantiated completion — does the gate reject it?

**Fix:** make the criteria substantive; verify the gate rejects a test case.
**Recurrence guard:** each gate is tested with a deliberate failure.

## 13. The manifest changes more often than the prompts

**Symptom:** version control shows structural churn unrelated to structural changes.
**Mechanism:** the graph is being used where configuration would do — values that should be data are
encoded as nodes and edges.
**Diagnosis:** compare manifest-change frequency with prompt-change frequency.

**Fix:** move the varying values into configuration; the graph should change structurally.
**Recurrence guard:** the graph-justification criteria, which exclude configuration as a reason.

## 14. Voting that costs N× and improves nothing

**Symptom:** accuracy unchanged despite tripled spend.
**Mechanism:** the model's failures are correlated — the same prompt gap breaks the same cases every
run — so repetition repeats the error.
**Diagnosis:** were failure correlations measured?

**Fix:** fix the shared cause; voting does not help correlated failures.
**Recurrence guard:** correlation measured before voting is adopted.

## 15. An orchestrator over an enumerable decomposition

**Symptom:** an orchestrator whose plans look structurally similar across inputs.
**Mechanism:** the decomposition *was* knowable; the 20-input test was never run (R6).
**Diagnosis:** decompose 20 real inputs by hand — do they repeat?

**Fix:** replace with a chain or routing; measure the difference.
**Recurrence guard:** the 20-input test before the orchestrator rung is entered.

## The triage rule

Three findings — **no measured baseline**, **agency over knowable steps**, and **no exit conditions** —
are detectable in an afternoon and account for most complexity mistakes. Check those three first: the
first means the climb was unjustified, the second means the wrong rung was chosen, and the third means
the complexity is permanent regardless of whether it was ever needed.
