# Anti-Patterns

<!-- STANDARD: 3min -- the launch anti-pattern catalogue with detection heuristics -->

## 1. The single launch number

**Symptom:** "our launch time is 1.2 s" — with no mode, no device and no separation of display from
interactivity.
**Cause:** the metric was never decomposed (R1, R2).
**Detection:** ask which mode, which device class, and whether that is first-frame or interactive. Any
hesitation is the finding.

**Fix:** report mode, device class, cache state, and both TTID and TTFD.

## 2. Optimising the wrong mode

**Symptom:** weeks of work; no measured improvement on the complaint.
**Cause:** the complaint is about cold launch and the work targeted hot start (R6).
**Detection:** write down the complaint's mode, then the mode the work targets. Different means stop.

**Fix:** re-scope to the failing mode before continuing.

## 3. The flagship-and-warm measurement

**Symptom:** "it's instant on my phone"; users on mid-tier devices disagree.
**Cause:** measured on the fastest device, with a warm process (R1).
**Detection:** is the device class named? Was the process killed between runs?

**Fix:** cold, median device class, ≥10 runs, median and p90.

## 4. Fast first frame, dead interaction

**Symptom:** the page or screen appears immediately and ignores input for seconds.
**Cause:** TTID improved while TTFD was never measured (R2).
**Detection:** compare the two metrics; a large gap is the whole story.

**Fix:** measure TTFD, then attribute Phase 3.

## 5. The splash screen as the fix

**Symptom:** the splash gets longer each release; the app still takes as long to become usable.
**Cause:** the wait is covered, not reduced (R4).
**Detection:** is there a splash, and has the underlying work been measured at all?

**Fix:** reduce the work, then size the splash to the residual.

## 6. Unattributed cause

**Symptom:** "it's the framework" / "it's our dependency count".
**Cause:** no per-phase measurement (R3).
**Detection:** can the claimant show a phase breakdown that sums to the total?

**Fix:** attribute by phase (trace or ablation), with the residual stated.

## 7. Measurement by ablation without a control

**Symptom:** every component you removed appeared to save time; the total did not fall.
**Cause:** the device warmed or the background load changed between runs.
**Detection:** was the control re-measured after each ablation?

**Fix:** one change at a time; re-measure the control each round.

## 8. Before/after across changed conditions

**Symptom:** a claimed improvement that vanishes in the next build.
**Cause:** a different device, cache state or instrument for the comparison (R5).
**Detection:** compare the recorded methods, not just the numbers.

**Fix:** re-measure both sides with one method; publish the noise floor.

## 9. Optimising the handler in a serverless function

**Symptom:** handler micro-optimisation with a seconds-long cold start unchanged.
**Cause:** the module graph is the cost, not the handler (Decision Tree 3).
**Detection:** measure the import graph (e.g. `-X importtime`) before touching the handler.

**Fix:** reduce module-scope work, defer imports, tree-shake the entry.

## 10. Reading cumulative import time as the ranking

**Symptom:** you optimised a module that aggregates others and moved nothing.
**Cause:** cumulative time includes children; self time is the work.
**Detection:** sort by **self** time, not cumulative.

**Fix:** target high-self-time modules.

## 11. Module-scope side effects

**Symptom:** start-up cost that appears whenever a module is imported, anywhere.
**Cause:** configuration reads, connections or registrations at import time.
**Detection:** grep for top-level calls in the entry's import graph.

**Fix:** move them behind functions; import lazily.

## 12. Third-party initialisers left unowned

**Symptom:** a large pre-main cost with nothing in the app's own code to explain it.
**Cause:** dependencies self-initialising (providers, `+load`, auto-configuration).
**Detection:** an inventory of what *self-initialises*, not of what you wrote.

**Fix:** consolidate, defer, or remove — and remove the replaced hooks.

## 13. The stale compilation profile

**Symptom:** a profile ships and the benefit fades over releases.
**Cause:** the profile was generated once and never refreshed against changing code.
**Detection:** does the profile's coverage match the current launch trace?

**Fix:** regenerate on a trigger; treat it as a build artefact with an owner.

## 14. The budget with no gate

**Symptom:** launch drifts upward by a small increment each release.
**Cause:** a target without a consequence (R4).
**Detection:** name the thing that fails when the budget is exceeded. If nothing does, there is no
budget.

**Fix:** CI benchmark plus a production alert; a defined failure response.

## 15. The disabled gate

**Symptom:** the launch gate is skipped "temporarily"; launch regresses and nobody notices.
**Cause:** gate flakiness treated as an obstacle rather than a defect.
**Detection:** is the gate currently enabled in CI?

**Fix:** fix the flakiness; a gate that is routinely disabled is worse than none, because it implies
monitoring that is not happening.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== static initializers / constructors (Phase 1 candidates) =="
grep -rnE '__attribute__\s*\(\s*\(\s*constructor|^\s*\+\s*\(void\)\s*load' "$SRC" 2>/dev/null | head || echo "  none"
grep -rnE '^\s*static\s*\{' "$SRC" 2>/dev/null | head || echo "  none (Java/Kotlin)"

echo "== module-scope side effects (Python/JS entry graph) =="
grep -rnE '^(import|from|require)' "$SRC" 2>/dev/null | wc -l | xargs echo "  import count:"

echo "== Android self-initialising providers (manifest merge is the hidden source) =="
find . -name AndroidManifest.xml -not -path '*/build/*' 2>/dev/null \
  | xargs grep -l 'provider' 2>/dev/null | head || echo "  none in app manifest (check merged manifest!)"

echo "== is a compilation profile shipped? =="
find . -iname '*baseline*profile*' -o -iname '*startup-profile*' 2>/dev/null | head || echo "  none found"

echo "== launch benchmark / gate in CI =="
grep -rnE 'macrobenchmark|startupTiming|launch|TTID|time.to.interactive|lighthouse' \
  .github/workflows/ 2>/dev/null | head || echo "  NONE — no launch gate in CI"

echo "== splash screen present (check it is not the fix) =="
grep -rniE 'splash' "$SRC" 2>/dev/null | head || echo "  none"

echo "== launch budget recorded? =="
find . -iname '*launch*budget*' -o -iname '*budget*.json' -o -iname '*budget*.md' 2>/dev/null | head || echo "  NONE"
```

Interpretation: **no launch gate in CI** and **no recorded budget** are standalone findings — they mean
launch is unmanaged and will drift. A **splash screen present with no budget** is the classic
cover-the-wait pattern. A **manifest provider** in a dependency (visible only in the *merged* manifest)
is the most common single cause of an unexplained pre-main cost.
