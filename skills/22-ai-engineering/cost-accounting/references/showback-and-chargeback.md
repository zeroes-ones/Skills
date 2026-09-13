# Showback and Chargeback

<!-- DEEP: 5+min -- attribution per team, the showback-first sequence, and when chargeback is safe -->

## The two practices, and the order

| Practice | What it does | Consequence |
|---|---|---|
| **Showback** | reports spend to the team that caused it | visibility, no consequence |
| **Chargeback** | bills it to that team's budget | visibility *and* consequence |

**The sequence matters, and the order is showback first.** Chargeback on top of attribution nobody
trusts produces disputes, not accountability — teams argue about the numbers instead of the spend,
and the practice is abandoned before it does any good.

```text
Showback for one quarter  → teams recognise their numbers as correct
                          → only THEN chargeback
Skip the quarter           → the first chargeback conversation is about the
                             accounting, not about the cost
```

## What attribution needs

Chargeback requires that every dollar be traceable to a payer:

| Requirement | Why |
|---|---|
| A tag on every run (team, product, task class) | an untagged run cannot be attributed to anyone |
| A denominator that is agreed | runs, successful outcomes, tasks — the teams must accept the unit |
| A rate that is agreed | the price basis, and whether cache discounts are passed through |
| A time window that matches finance's | otherwise the numbers never reconcile and the practice is discredited |
| A stated treatment of shared cost | the model, the shared gateway, fixed tiers |

**The tag is the whole thing.** Without it there is no attribution, and no amount of reporting will
produce accountability from a shared pot.

## The shared-cost problem

Some cost is genuinely shared and cannot be attributed per team. Decide the treatment explicitly.

| Cost | Options | Notes |
|---|---|---|
| Shared gateway/infra | flat split, proportional to usage, or absorbed centrally | proportional is defensible; flat is simple |
| Fixed commitment tier | amortise across teams, or absorb centrally | if nobody pays for unused headroom, nobody manages it |
| Exploration/experiment budget | a central pot, with an authorisation | otherwise it lands on whichever team ran it |
| Platform team's own runs (evals, CI) | platform budget | do not push engineering cost onto a product team |

**The failure to avoid:** leaving the treatment undefined, then improvising it during the first
dispute. That is how chargeback loses credibility.

## The unit, chosen carefully

```text
Bad unit:  runs                    → rewards running fewer, longer runs; penalises exploration
Bad unit:  API calls               → rewards failing cheaply, as cost-per-call does
Good unit: successful outcomes      → matches what the team is buying
Better unit: successful outcomes at or above a quality bar
```

**The best unit is the one the team already uses to describe its work.** A team measured on
"resolved tickets" should be charged per resolved ticket, not per token — the number then means
something to them, which is what makes it a management tool rather than a report.

## Guarding against the metric becoming the goal

Every chargeback unit invites a distortion. Name the distortion before someone finds it.

| Unit | The distortion | Guard |
|---|---|---|
| per successful outcome | declares success loosely | pair with the quality score (`cost-per-success.md`) |
| per run | fewer, bigger runs; less exploration | add an exploration budget outside the unit |
| per token | starves quality for cheapness | assert the quality band in the gate |
| per resolved ticket | tickets split or merged for advantage | audit the ticket definition periodically |
| per feature | features bundled to hide cost | attribute per task class, not per feature |

**The general form:** any unit that can be improved by degrading something else needs that something
else asserted alongside. This is not a reason to avoid chargeback; it is the design work chargeback
requires.

## Reporting that survives scrutiny

```text
Agent cost showback — <period>

Unit: successful outcomes at or above the quality bar (≥3.0/5).
Rate basis: <provider> rates as of <date>; cache discounts passed through.

| Team      | Runs  | Successes | Cost/success | Spend    | vs budget |
|-----------|-------|-----------|--------------|----------|-----------|
| Payments  | 4,120 | 3,502     | $0.041       | $143.58  | 72%       |
| Search    | 9,880 | 8,204     | $0.028       | $229.71  | 115% ⚠    |
| Platform  | 1,240 | 1,180     | $0.019       | $22.42   | (central) |
| Untagged  |   310 | —         | —            | $14.90   | (to fix)  |
                                             ---------
total                                          $410.61

Reconciliation: invoice for the period $398.20, variance +3.1% (accepted band ±5%).
Note: 310 untagged runs are attributed centrally this period; tagging is the
      action item.
```

Four things make that report credible: the unit is stated, the rate basis is dated, the variance
against the invoice is shown, and the unattributed remainder is named rather than hidden.

## When NOT to chargeback

| Situation | Why chargeback is wrong |
|---|---|
| Attribution is new and unverified | the numbers will be disputed and the practice discredited |
| Spend is small relative to team budgets | the accounting cost exceeds the management value |
| The work is exploratory by nature | charging for discovery suppresses discovery |
| The organisation is very small | a single budget is simpler and loses nothing |
| Trust in the numbers is low | fix attribution first; chargeback on bad numbers is a political problem, not a financial one |

**The honest test:** does the team change its behaviour when shown the number? If showback already
changed it, chargeback adds administration and no value.

## Checklist

- [ ] Showback runs for a quarter before any chargeback (R4-adjacent)
- [ ] Every run carries a tag identifying its payer
- [ ] The unit is agreed with the teams, and matches how they describe their work
- [ ] The rate basis and its date are published
- [ ] Shared cost treatment is decided in advance, not during a dispute
- [ ] The variance against the invoice is reported, with an accepted band
- [ ] The unattributed remainder is named as an action item, not hidden in a total
- [ ] The distortion each unit invites is named, with a guard asserted alongside
- [ ] Chargeback is skipped where attribution is unverified, spend is small, or the work is exploratory
