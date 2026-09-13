# Anti-Patterns

<!-- STANDARD: 3min -- the cost-accounting anti-pattern catalogue with detection heuristics -->

## 1. Silence-as-zero

**Symptom:** a dashboard reports trivial agent spend while the invoice grows.
**Cause:** usage was never reported, so the cost field defaulted to `0.0` (R1).
**Detection:** is there a `measured` flag, and does the reporting treat an unset field as unknown?

```bash
# does the accounting distinguish measured from unmeasured?
grep -rn "measured" scripts/*.py | head
# does any code default cost to 0.0 without a flag?
grep -rn '"cost": 0.0\|cost_usd.: 0' scripts/*.py | head
```

**Fix:** report `usage` from the executor; carry a `measured` flag; reconcile against the invoice.

## 2. Proxy presented as cost

**Symptom:** cost "measured" in steps, calls or tokens-without-pricing.
**Cause:** the proxy was cheaper to obtain than the real quantity (R2).
**Detection:** does the reported cost field trace to a provider rate, or to a count?

**Fix:** measure real usage; label any remaining proxy with its drift condition (see `proxies-and-drift.md`).

## 3. Cost per call

**Symptom:** "we cut cost per call 40%" with retries unchanged or worse.
**Cause:** the metric stops at the request boundary (R3).
**Detection:** is a success rate reported alongside the cost?

**Fix:** cost per successful outcome, with the success rate shown.

## 4. Outcome-blind saving

**Symptom:** a cheaper configuration that fails more often, reported as a win.
**Cause:** the comparison omitted the success rate (R3).
**Detection:** does the saving claim state the success rate on both sides?

**Fix:** report cost per success, plus quality, on both sides.

## 5. Unenforced budget

**Symptom:** a `max_cost_usd` in a manifest that has never failed anything.
**Cause:** nothing checks it (R4).
**Detection:** is the cap checked in the run loop, and does a breach halt the run?

**Fix:** check after each node and in loop passes; halt and record the breach.

## 6. Silent budget raise

**Symptom:** the cap always equals the spend; the budget never fails.
**Cause:** the cap is edited to fit, with no record (R4).
**Detection:** does an increase require a reason and a review date?

**Fix:** record who, why, from/to, and a review date on every raise.

## 7. Total-only accounting

**Symptom:** a per-run total and no way to say which node or phase consumed it.
**Cause:** per-node cost was never accumulated (R5).
**Detection:** does run-state carry `nodes[*].cost`?

**Fix:** accumulate per node; split by phase; state the residual.

## 8. The unexamined loop

**Symptom:** a workflow whose cost is dominated by iterations nobody priced.
**Cause:** the loop bound was set for reliability, never for cost (R5).
**Detection:** rank cost by phase — if the retry phase dominates, this is it.

**Fix:** attribute the loop, then trade iterations against escalations with both measured.

## 9. Escalation cost blindness

**Symptom:** a low per-run average and a large bill, because a small share of runs escalate expensively.
**Cause:** the escalation rate × escalation cost is not tracked as a cost term.
**Detection:** `escalation_rate × escalation_cost` — is it computed?

**Fix:** measure both, and treat the product as a first-class cost metric.

## 10. Demo-scaled forecast

**Symptom:** a projection an order of magnitude from reality.
**Cause:** a total extrapolated rather than a unit multiplied (R6).
**Detection:** does the forecast rest on a measured per-unit cost?

**Fix:** measured unit × derived volume, with assumptions and scenarios (see `forecasting.md`).

## 11. Median-only forecast

**Symptom:** the forecast holds until a bad month; the tail was never modelled.
**Cause:** p90 omitted.
**Detection:** is the tail reported with the median?

**Fix:** report p90 and a worst-case scenario.

## 12. Untraceable shared spend

**Symptom:** one budget, no attribution, arguments about who caused the cost.
**Cause:** runs carry no payer tag.
**Detection:** is there a team/product tag on runs?

**Fix:** tag runs; showback; chargeback only once attribution is trusted.

## 13. Chargeback before trust

**Symptom:** the first chargeback conversation is about the accounting, not the spend.
**Cause:** chargeback skipped the showback period.
**Detection:** have teams confirmed their numbers are correct before being billed?

**Fix:** showback for a quarter, then chargeback.

## 14. Never reconciling

**Symptom:** confidence in the numbers, and no evidence for it.
**Cause:** internal accounting never compared to the invoice.
**Detection:** is there a reconciliation log with dates and variances?

**Fix:** reconcile per model, on a cadence, with an accepted band and a log.

## 15. Price drift attributed to code

**Symptom:** a cost gate fails after a provider price change; the wrong team investigates.
**Cause:** tokens and price were not separated.
**Detection:** does the comparison report the tokens delta and the price delta separately?

**Fix:** split them; re-baseline deliberately on a price change.

## 16. Security traded for a saving

**Symptom:** a cheaper configuration that skipped a validation, cached across tenants, or disabled a guardrail.
**Cause:** cost was treated as the only objective (Anti-Hallucination).
**Detection:** does any saving reduce a validation, a scope boundary, or a guardrail?

**Fix:** refuse; escalate to `appsec-engineer`.

## Detection sweep

```bash
SRC="${1:-scripts}"

echo "== does the accounting carry a measured flag? =="
grep -rn "measured" "$SRC" 2>/dev/null | head -3 || echo "  NONE — an unset cost reads as zero"

echo "== any cost field defaulted to 0.0 without provenance? =="
grep -rnE '"cost(_usd)?": *0(\.0)?[^0-9]' "$SRC" 2>/dev/null | head -3 || echo "  none obvious"

echo "== is cost a proxy (steps/calls) in reporting? =="
grep -rniE "cost proxy|as cost|proxy" "$SRC" 2>/dev/null | head -3 || echo "  none"

echo "== manifests with a step budget but no cost cap =="
for f in workflow/manifests/*.yaml; do
  grep -q "max_steps" "$f" 2>/dev/null && ! grep -q "max_cost_usd" "$f" 2>/dev/null && echo "  $f"
done

echo "== is cost per success computed anywhere? =="
grep -rniE "cost_per_success|per_success|per successful" "$SRC" 2>/dev/null | head -3 || echo "  NONE — the decision metric is missing"

echo "== reconciliation log present? =="
find . -iname "*reconcil*" -not -path "*/node_modules/*" 2>/dev/null | head -3 || echo "  NONE"

echo "== does any saving touch a security control? =="
grep -rniE "skip.*(valid|verif)|disable.*(guardrail|check)|cache.*(cross|tenant)" "$SRC" 2>/dev/null | head -3 || echo "  none obvious"
```

Interpretation: **no `measured` flag** plus **a cost field defaulted to zero** is the silence-as-zero
defect, and it is the highest-severity finding here — it suppresses the alarm. **A step budget with no
cost cap** means spend is unbounded while activity is bounded. **No cost-per-success computation**
means the decision metric does not exist.
