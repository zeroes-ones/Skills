# Backtest — Evidence Format for `equity-risk-and-capital-engineer`

> **This file is a FORMAT, not a result.** No market outcome, no historical performance and no
> strategy return is recorded or claimed here. What is defined here is the **evidence record a run of
> this skill must produce** and the **grading rubric** applied to it, so that two runs can be compared
> without argument about what was measured.
>
> Every numeric value below appears inside a worked *grading* illustration whose inputs are stated on
> the spot. Those figures are `[COMPUTED]` arithmetic on those hypothetical inputs. They are not
> observations of any market.

## §1 — What Is Recorded, Per Decision

One record per decision. A record without every field below is incomplete and grades as a failure of
evidence, regardless of whether the decision turned out well.

| Field | Type | Meaning | Required provenance |
|---|---|---|---|
| `record_id` | string | Stable identifier for the decision | — |
| `decided_at` | ISO timestamp | When the decision was made, with the zone | — |
| `decision_class` | enum | `margin` / `borrow` / `liquidity` / `concentration` / `reserve` / `event` | — |
| `regime` | enum | `cash` / `reg-t` / `portfolio-margin`, and the account's equity | `[BROKER-VERIFIED]` |
| `clock_type` | enum | Which clock the decision was taken against: `settlement`, `reg-t-payment`, `holding-period`, `wash-sale`, `short-swing`, `reg-sho`, `threshold`, `offer`, `index`, `lock-up`, `none` | `[VERIFIED — named rule]` or `[COMMON-PRACTICE]` |
| `deadline_date` | ISO date | The clock resolved to a **date** in the market's business-day calendar. A duration alone does not satisfy this field | `[COMPUTED]` |
| `calendar_source` | string | The market calendar used to resolve the date, with its read date | `[BROKER-VERIFIED]` or named source |
| `broker_figures` | object | Buying power, requirement, maintenance excess, borrow status — each with the read timestamp | `[BROKER-VERIFIED]` |
| `computed_figures` | object | The skill's own arithmetic, each with its formula | `[COMPUTED]` |
| `modelled_figures` | object | Impact cost, spread widening, `WCSD`, buy-in risk premium — each with its derivation and error bound | `[ESTIMATED ±X%]` |
| `binding_term` | enum | For a reserve decision: `R_dd` / `R_tail` / `R_exit` | `[COMPUTED]` |
| `action` | string | What was decided, in one sentence, with the position ids affected | — |
| `exit_routes_referenced` | [ref] | The exit records the decision relied on (`exit_route`, `exit_cost_pct`, `exit_cost_cap`, `size_vs_adv`, `days_to_liquidate`) | `[COMPUTED]` per record |
| `counterfactual` | object | What the alternative action would have cost, in dollars, under the same inputs | `[COMPUTED]` |
| `outcome` | object | What actually happened, recorded at the horizon in §3 | `[BROKER-VERIFIED]` where a fill or a fee is involved |
| `lesson` | string | One sentence, written only after the outcome is known | — |

**A record with an empty `deadline_date` on a clock-driven decision fails, even if the deadline was
described in words.** That is the single most common defect this format exists to catch: a deadline
held as a duration is a deadline that gets missed on a long week.

## §2 — Per Decision Class, the Minimum Evidence

| Decision class | Fields that must be non-empty beyond §1 | The specific thing being graded |
|---|---|---|
| `margin` | `regime`, `broker_figures.maintenance_requirement`, `computed_figures.call_distance_dollars`, `computed_figures.call_distance_pct`, `clock_type = reg-t-payment`, `deadline_date` | That the call distance was computed at **maintenance**, that the deadline is a **date**, and that any 15-business-day figure was labelled a ceiling on the member |
| `borrow` | `broker_figures.borrow_status`, `broker_figures.borrow_fee_annual_pct`, `recall_terms`, `fail_age_settlement_days`, `exit_routes_referenced[].buy_in_exposure` | That the recall period was **not** asserted as a rule, and that the borrow and buy-in exposure were priced into the exit cost |
| `liquidity` | `exit_routes_referenced[].exit_route` (not broker liquidation), `exit_cost_pct`, `exit_cost_cap`, `size_vs_adv`, `days_to_liquidate` | That the exit was sized as a fraction of average daily volume, and costed as spread plus impact |
| `concentration` | The four measures (weight in NAV, fraction of ADV, fraction of shares outstanding, exit-weighted contribution) and each cluster's weight at correlation → 1.0 | That the exit-weighted measure was reported, and that clusters close whole |
| `reserve` | `computed_figures.reserve_floor` with all three terms, `binding_term`, `uncommitted_BP_after_fill`, `headroom_after` | That the floor was tested **before** the ticket and that the binding term was named. A floor tested after the fill fails outright |
| `event` | The event's own deadline with its source, and — for a tender, exchange, redemption or expiry — the **offer's instruction cutoff time** | That the deadline came from the offer document and not from an assumed number of days |

## §3 — The Outcome Horizon

An outcome is recorded at a fixed horizon so that two runs can be compared. The horizon is set at
decision time and is not moved afterwards:

| Decision class | Horizon | Why that horizon |
|---|---|---|
| `margin` | The clock's own `deadline_date`, plus the following settlement date | The question was whether the call was cured in time; nothing later changes the answer |
| `borrow` | 30 calendar days, or the position's closure if earlier | Recall and fee conditions move on a scale of days to weeks |
| `liquidity` | The realised `exit_cost_pct` at the moment the exit completes | The model's claim was a cost, and only a fill can grade it |
| `concentration` | The next scheduled review, or the first index effective date, whichever is sooner | Concentration is a standing condition, not a trade |
| `reserve` | The `deadline_date` of the next ticket decision | The claim was about a gate, and the gate is either held or breached |
| `event` | The event's own resolution date | The event's clock ends when it ends |

## §4 — Grading

Each record is graded on four axes, each scored 0–2. A record scoring below 6 of 8 is a **failed
evidence record** even if the market outcome was favourable.

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| **Provenance** | A number without a tag | Tags present but a `[VERIFIED]` lacks a named source, or a broker figure lacks a read date | Every number tagged; every `[VERIFIED]` names a rule or statute; every broker figure carries a read date |
| **Clock discipline** | The deadline is a duration, or missing | A date is given but the calendar source is unstated | The deadline is a date, in the market's own calendar, with the calendar's read date |
| **Quantification** | Adjectives ("plenty of room", "liquid enough") | A percentage without dollars | Dollars, with the formula shown, plus the counterfactual |
| **Scope honesty** | An unverified figure asserted as a rule, or insider clocks applied to a retail holder | A caveat exists but is buried or ambiguous | The unverified items and the scope line are stated where the claim is made |

**Favourable outcome does not upgrade a grade.** A decision that made money on an untagged number is
an untagged number, and the next one will not be so lucky.

## §5 — Worked Grading Illustration [COMPUTED]

Hypothetical inputs, stated once, used by both runs below. No market data is implied.

```
INPUTS (hypothetical, fixed for reproducibility)
  NAV                              $500,000
  total_BP                         $400,000
  committed_margin                 $210,000
  WCSD (correlation → 1.0)         $240,000
  exit_cost(book)                  $ 64,000
  proposed ticket margin           $ 90,000
  account regime                   reg-t
```

```
Run 1 — graded 8/8
  uncommitted_BP      = 400,000 − 210,000             = $190,000        [COMPUTED]
  R_dd                = 0.15 × 500,000                = $ 75,000        [COMPUTED]
  R_tail              = 0.50 × 240,000                = $120,000        [COMPUTED]
  R_exit              = 1.50 × 64,000                 = $ 96,000       [COMPUTED]
  reserve_floor       = max(75,000, 120,000, 96,000)  = $120,000  (R_tail binding)
  after_fill          = 400,000 − (210,000 + 90,000)  = $100,000       [COMPUTED]
  headroom_after      = 100,000 − 120,000             = −$20,000  →  ticket BLOCKED
  action              reduce the ticket to $65,000: after_fill $125,000 ≥ $120,000 → ALLOWED

  GRADING  provenance 2 (every figure tagged, formula shown)
           clock      2 (no clock on this decision; deadline field correctly 'none')
           quantification 2 (dollars plus the $20,000 counterfactual shortfall)
           scope      2 (no unverified claim asserted)
           TOTAL      8/8

Run 2 — the same decision, graded 3/8
  "There's plenty of buying power and the ticket looks fine."
  "Reserve is about 20% of the account, which leaves room."

  GRADING  provenance 0 (no tags at all)
           clock      1 (no clock stated, but none was owed)
           quantification 0 (no dollar figure, no counterfactual)
           scope      2 (nothing unverified asserted)
           TOTAL      3/8  → FAILED EVIDENCE RECORD, and the ticket breaches the floor
```

The two runs reach opposite actions on identical inputs, and the grader can say why in one line. That
is the whole purpose of the format.

## §6 — Best Case

The best case is **not** the run with the highest return. It is the run with a complete record, a
correct binding term, and a decision that was inside the policy before the outcome was known.
In the illustration above, Run 1 is the best case at **8/8**, and its "best" property is that it
blocked a $90,000 ticket whose after-fill uncommitted buying power would have been $100,000 against a
$120,000 floor [COMPUTED] — a $20,000 shortfall that no market outcome can retroactively justify.

A best-case record is characterised by: every number tagged, every `[VERIFIED]` named, every deadline
a date, every exit route named, every dollar figure shown with its formula, and nothing unverified
asserted as a rule.

## §7 — Worst Case

The worst case is the record that **passes on outcome and fails on evidence** — the one that teaches
the wrong lesson. Three shapes recur:

1. **The lucky breach.** The floor was breached, the position recovered, and the log records a
   success. Graded: provisionally failed, because the decision was outside the policy and the
   outcome was noise.
2. **The untagged number.** A margin figure with no provenance that turned out to be right by
   coincidence. Graded: failed on the provenance axis, and the next one will be wrong.
3. **The duration that was not a deadline.** "Three business days" recorded instead of a date, and
   the weekend is discovered by the calendar rather than by the reader. Graded: failed on the clock
   axis, and the consequence is a missed payment period — which is where a forced sale begins.

## §8 — Learnings

- **Lesson learned (the format's first job):** a record is graded on evidence, not on outcome.
  Recording the outcome first and the reasoning afterwards inverts the audit trail and makes the log
  useless for the decision it is meant to inform.
- **Lesson learned (the binding term):** for an equity book, `R_tail` binds more often than `R_dd`,
  because the correlated drawdown is the term a NAV-percentage rule cannot see. A log that never
  records `R_tail` as binding has probably been computing `WCSD` as a sum of values rather than a
  simultaneous drawdown.
- **Lesson learned (the date):** the highest-yield single fix in this format is refusing a duration.
  Every missed payment period in the reference material traces back to a clock stored as "a few days".
- **Actionable lesson:** re-grade the last twenty records against §4 before trusting any of them. The
  distribution of scores, not the average, is what tells you whether the process is sound.
- **What this format validated:** that the skill's core loop — establish the regime, resolve the
  clock to a date, compute at maintenance, price the exit, test the reserve before the ticket — can be
  audited by a third party from the record alone, without access to the run.
