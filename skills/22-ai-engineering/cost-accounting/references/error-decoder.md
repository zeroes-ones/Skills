# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. The dashboard says near-zero; the invoice says otherwise

**Symptom:** internal accounting reports trivial spend; the provider invoice for the same period is
orders of magnitude larger.
**Mechanism:** the executor never reported usage, so the cost field defaulted to `0.0`. Nothing failed,
because a zero is a valid number — the accounting cannot distinguish "spent nothing" from "was not
told" (R1).
**Diagnosis:** does the reporting carry a `measured` flag? Is any cost field defaulted without one?

**Fix:** make the executor return `usage`; add the flag; reconcile against the invoice per model.
**Recurrence guard:** reconciliation on a cadence with an accepted band (CR17).

## 2. Runs are cheaper and retries doubled

**Symptom:** per-call cost fell sharply, and the quarterly bill did not.
**Mechanism:** the optimisation reduced what one call costs while increasing how many calls the run
makes. Cost per call absorbs neither the retry nor the escalation (R3).
**Diagnosis:** is a success rate and a retry rate reported alongside the cost?

**Fix:** report cost per successful outcome; include the escalation cost in the comparison.
**Recurrence guard:** the gate asserts cost/success **and** success rate, retries and escalations.

## 3. The bill jumped with no code change

**Symptom:** spend rose materially in a period where the workflow did not change.
**Mechanism:** a provider price change, a model swap, or a cache policy change re-priced the same
usage. The tokens were identical; the rate was not (R2).
**Diagnosis:** compare the tokens delta and the price delta separately.

**Fix:** re-price the baseline, record the price date, and re-baseline deliberately.
**Recurrence guard:** every comparison reports the price split, so drift cannot be attributed to code.

## 4. One workflow consumes the budget

**Symptom:** a single workflow accounts for most of a fleet's spend.
**Mechanism:** usually an iteration loop with a generous cap, or an expensive model on a high-volume
node. The loop multiplies; a single call does not (R5).
**Diagnosis:** attribute by phase — if the retry/iteration phase dominates, it is the loop.

**Fix:** fix the upstream cause of the failed first attempt, or trade iterations against escalations
with both measured. Route the high-volume node's model.
**Recurrence guard:** per-node and per-phase attribution on every cost investigation.

## 5. Cost tracking exists and nobody acts on it

**Symptom:** a dashboard with numbers, reviewed occasionally, influencing no decisions.
**Mechanism:** the metric is not paired with an outcome and has no gate, so it is reporting rather
than governance (R4).
**Diagnosis:** what fails when the number gets worse? If nothing, there is no gate.

**Fix:** gate on cost-per-success delta against a baseline with a stated threshold.
**Recurrence guard:** the gate is a build step, not a dashboard (CR11).

## 6. Spend is untraceable across teams

**Symptom:** one budget line, many consumers, and arguments about attribution.
**Mechanism:** runs carry no payer tag, so no attribution is possible and the conversation becomes
political (R4-adjacent).
**Diagnosis:** is there a team/product tag on runs?

**Fix:** tag runs; report showback per team; move to chargeback only once the numbers are trusted.
**Recurrence guard:** tagging is a property of the run, and the untagged remainder is reported.

## 7. The forecast was wrong by an order of magnitude

**Symptom:** actual spend far exceeds the projection.
**Mechanism:** a total from a demo or a single run was extrapolated, rather than a measured unit
multiplied by a derived volume (R6).
**Diagnosis:** does the forecast rest on a measured per-unit cost, with the volume derived from
stated assumptions?

**Fix:** measure the unit; derive the volume; report base, worst and stress scenarios.
**Recurrence guard:** the forecast states each input's confidence (CR15).

## 8. A budget was raised with no record

**Symptom:** the cap always equals the spend; it has never failed.
**Mechanism:** with no increase path, the cap was edited to fit the invoice. A budget that cannot fail
is not a budget (R4).
**Diagnosis:** is there a recorded reason and a review date on increases?

**Fix:** require who, why, from/to, and a review date on every raise.
**Recurrence guard:** the increase path is a checklist item (CR12).

## 9. Two similar runs differ three-fold in cost

**Symptom:** the same task, wildly different spend, no explanation.
**Mechanism:** one run retried, or used a different model, or loaded a much larger context. A per-run
total cannot distinguish these (R5).
**Diagnosis:** compare phase splits and model routing between the two runs.

**Fix:** attribute per node and per phase; normalise the comparison; investigate the model and the
payload.
**Recurrence guard:** per-node cost recorded on every run, so variance is diagnosable after the fact.

## 10. Per-request metrics look excellent, the quarter does not

**Symptom:** the per-request cost is well optimised; the periodic bill keeps rising.
**Mechanism:** retries, cache misses, escalations and multi-node structure all live outside the
per-request metric (R3).
**Diagnosis:** does any metric measure to the end of the run?

**Fix:** cost per successful outcome, end to end, alongside the per-request metric.
**Recurrence guard:** the SLI reports cost per success, not per call.

## 11. The cost gate fails on a price change

**Symptom:** a gate failure with no corresponding code change.
**Mechanism:** an absolute cap rather than a delta. The price moved and the gate read it as a
regression (R4).
**Diagnosis:** does the gate compare a delta against a baseline, and report the price split?

**Fix:** delta gating with a re-priced baseline; classify the failure as a price change, not a defect.
**Recurrence guard:** the price delta is reported separately in every comparison.

## 12. A cache that saves nothing

**Symptom:** caching infrastructure added, bill unchanged.
**Mechanism:** the hit rate was assumed rather than measured; the cache rarely hits.
**Diagnosis:** what is the measured hit rate, and what does the forecast assume?

**Fix:** measure the hit rate; forecast from the measured value; remove the cache if it does not pay.
**Recurrence guard:** the hit rate is a required input to any caching forecast.

## 13. A run cap that cannot trip

**Symptom:** a `max_cost_usd` set on a workflow whose cap has never engaged.
**Mechanism:** the workflow is unmeasured (`measured: false`), so cost is 0.0 and the cap cannot be
crossed. A cap on an unmeasured workflow implies a control that is not operating (R4).
**Diagnosis:** is `measured` true for the workflow the cap protects?

**Fix:** get usage reported first; until then, note that the cap protects nothing.
**Recurrence guard:** the SLI reports unreported runs per workflow.

## 14. A cheaper model on the gating node

**Symptom:** a model route intended to save money increased total spend.
**Mechanism:** the node's verdict gates the rest of the run, so a slightly worse verdict caused more
retries — which cost more than the rate saved (R3).
**Diagnosis:** compare cost per success, not cost per call, before and after the routing.

**Fix:** route the high-volume, low-stakes node; keep the gating node on the reliable model.
**Recurrence guard:** model routing is justified by measured cost per successful outcome.

## 15. Reported cost rises slightly every month with flat usage

**Symptom:** a slow, steady increase with nothing visibly changed.
**Mechanism:** a gradual drift — context growing, a node's payload expanding, a cache hit rate
slipping — none of which shows in a per-run total.
**Diagnosis:** trend node-level and phase-level cost over months, not the run total.

**Fix:** find the growing term; it is usually context size or a deteriorating cache hit rate.
**Recurrence guard:** the SLI trend is reviewed, and node-level attribution is available.

## The triage rule

Three findings — **no `measured` flag**, **cost reported as a proxy**, and **no cost-per-success
metric** — are detectable with the sweep in `anti-patterns.md` and account for most cost-accounting
failures. Check those three first: the first means the numbers may be silently false, the second means
they may be drifting, and the third means the metric being optimised is the wrong one.
