# Anti-Patterns

<!-- STANDARD: 3min -- the complexity anti-pattern catalogue with detection heuristics -->

## 1. Complexity by default

**Symptom:** a design starts at a graph or multi-agent for a task with one input and one output.
**Cause:** architecture treated as a signal of seriousness rather than a purchase (R1).
**Detection:** is there a measured single-call baseline?

```bash
# is there any record of a baseline measurement?
find . -iname "*baseline*" -o -iname "*single-call*" 2>/dev/null | head || echo "  NONE"
```

**Fix:** build and measure the bottom rung first; climb only on a measured failure.

## 2. Agency for knowable steps

**Symptom:** an agent loop, planner or orchestrator over a sequence that was known in advance.
**Cause:** task difficulty confused with unpredictability (R2).
**Detection:** can you write the steps before seeing the input? If yes, it is a workflow.

**Fix:** a deterministic chain, with the model inside each step.

## 3. Two rungs at once

**Symptom:** a change adding a chain *and* a router, or a router *and* an orchestrator.
**Cause:** climbing without measuring each rung (R3).
**Detection:** does the diff add more than one rung's mechanism?

**Fix:** revert to one rung, measure, then decide about the next.

## 4. Permanent complexity

**Symptom:** a node nobody can justify removing, and nobody knows why it exists.
**Cause:** no exit condition recorded at climb time (R4).
**Detection:** does every rung have a written, falsifiable exit condition with a date?

**Fix:** audit by removal; record the failing case or remove the node.

## 5. Speculative capability

**Symptom:** "more robust", "more capable", "better quality" as the rationale.
**Cause:** no measured failure named (R6).
**Detection:** does each rung point at a *failing case*?

**Fix:** name the failure with its case, or remove the rung.

## 6. Building for imagined scale

**Symptom:** complexity justified by anticipated volume.
**Cause:** unmeasured scale assumption (R5).
**Detection:** is there a measured or derived volume figure?

**Fix:** derive the volume; show where the simpler design breaks; remove the rest.

## 7. The decorative graph

**Symptom:** six nodes where one contains the whole prompt and five are pass-throughs.
**Cause:** the graph was entered for a lower rung's problem.
**Detection:** which node does the work? Is it more than one?

**Fix:** collapse to a single call plus a wrapper, or make the other nodes meaningful.

## 8. Untested new failure modes

**Symptom:** a chain that mislinks, a router that misroutes, a fan-out that partially fails.
**Cause:** each rung's own failure mode was never identified.
**Detection:** does each rung have a test for the failure *it* introduces?

**Fix:** identify and test the rung's failure mode before shipping.

## 9. Open action space

**Symptom:** an agent with access to a shell, arbitrary code execution, or an unbounded tool set.
**Cause:** agency granted over what may be done, not just which option (Anti-Hallucination).
**Detection:** can you write the complete list of permitted actions?

**Fix:** bound the action space to an allow-list, or escalate to `appsec-engineer`.

## 10. The unmeasured router

**Symptom:** a router whose classification accuracy was never measured.
**Cause:** routing added on the assumption that classes are separable.
**Detection:** is there a measured routing accuracy figure?

**Fix:** measure it; merge unreliable paths; apply the clustering test.

## 11. Parallelism for quality

**Symptom:** a fan-out or voting block added to improve accuracy.
**Cause:** parallelism confused with quality improvement.
**Detection:** is the stated problem latency (sectioning) or reliability (voting)?

**Fix:** for a quality shortfall, use a better prompt, model or retrieval — not parallelism.

## 12. Voting on correlated failures

**Symptom:** voting that multiplies cost without improving accuracy.
**Cause:** the failures are correlated, so they repeat.
**Detection:** were failure correlations measured?

**Fix:** fix the shared cause; voting does not help correlated errors.

## 13. The unbounded orchestrator

**Symptom:** cost and latency distributions with a very long tail.
**Cause:** no `max_subtasks` or `max_replans`.
**Detection:** is the subtask count bounded?

**Fix:** bound the plan size and the replan count; enforce a cost cap.

## 14. The graph as configuration

**Symptom:** the manifest changes more often than the prompts.
**Cause:** the graph is being used where configuration would do.
**Detection:** compare manifest and prompt change frequency.

**Fix:** move the varying values into config; the graph should change for structural reasons.

## 15. No recorded rationale per rung

**Symptom:** a new engineer cannot tell why a node exists.
**Cause:** the rationale lives in someone's memory.
**Detection:** does each node name its failure in a durable place?

**Fix:** record the rung, its failure and its exit condition.

## Detection sweep

```bash
SRC="${1:-workflow/manifests}"

echo "== node count per manifest (a proxy for over-build) =="
for f in $SRC/*.yaml; do
  n=$(grep -cE '^\s+- id:' "$f" 2>/dev/null)
  echo "  $n nodes  $(basename "$f")"
done

echo "== nodes declaring a completion contract (verification in use?) =="
grep -rl "workflow:" skills/*/*/SKILL.md 2>/dev/null | wc -l | xargs echo "  skills with contracts:"

echo "== manifests declaring budgets (enforcement in use?) =="
grep -rl "budget:" $SRC/*.yaml 2>/dev/null | wc -l | xargs echo "  manifests with budgets:"

echo "== manifests declaring gates or escalation (escalation in use?) =="
grep -rlE "escalate_to|gates:" $SRC/*.yaml 2>/dev/null | wc -l | xargs echo "  manifests with escalation:"

echo "== loops present, and do they cap iterations? =="
grep -rn "max_iterations" $SRC/*.yaml 2>/dev/null | head -3 || echo "  none"

echo "== is there a recorded complexity decision / baseline? =="
find . -iname "*complexity*decision*" -o -iname "*rung*baseline*" 2>/dev/null | head || echo "  NONE"
```

Interpretation: **a graph with no contracts, no budgets and no gates** is using none of the machinery
that justifies the rung — it is a chain paying a graph's costs. **A high node count with few declared
failures** suggests nodes without a failure to address. **No recorded complexity decision** means the
rungs were chosen by preference.
