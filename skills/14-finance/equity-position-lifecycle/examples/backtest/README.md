# Review Record and Grading Format

This directory holds the **evidence format** for this skill: what a holder records on every review of an open equity position, and how each recorded action is graded later. It describes a structure, not results.

**No performance results are claimed here.** Nothing in this directory is a measured outcome, a backtest, an equity curve or a track record. The illustrative rows below are labelled `[COMPUTED]` arithmetic on invented inputs chosen to demonstrate the format — they are not observations from any account. Where a figure depends on live data (marks, spreads, premiums, dividend dates, margin schedules), the format leaves a blank for the operator to fill from a source they can name. Nothing is invented to fill a column.

## Why a record format belongs with a decision skill

An equity position never expires, so nothing external forces a decision about it. What forces a decision is a written date and a written level. A record is how those two things survive contact with a bad week: a date in a notebook can be renegotiated, a date in a record with a grading field cannot be quietly moved.

The record has three jobs:

1. **Make the decision visible while it is a decision.** A review that produces no written outcome is indistinguishable from no review.
2. **Make the deadline enforceable.** The improve-by date and the invalidation level are fields, not memories.
3. **Make the rules improvable.** The precedence table in this skill — which clock beats which — can only be tuned from graded conflicts. Without the grading record it drifts back to folklore.

## Part 1 — The review record

One record per position per review. The fields are fixed so that two reviews can be compared, and so that a missing field is visible rather than inferred.

```text
record_id:            <position-id>-<yyyy-mm-dd>-<n>
position:             <ticker> <shares> sh, basis <price>, lots <n>, opened <date>
reviewed_at:          <timestamp with timezone>
mark_source:          <where the mark came from>          source: <broker|vendor|manual read>

step1_forced:         margin:<clear|call> borrow:<clear|recalled> pdt:<clear|flagged>  PASS|FAIL
step2_thesis:         level:<price>  version:<date>  close:<price>  reading:<...>  PASS|FAIL
step3_identity:       shares:<n>  lots:<n>  basis:<price>  overlay:<none|detail>  corp_action:<none|detail>  PASS|FAIL
step4_events:         earnings:<date|none>  exdiv:<date|none>  reconstitution:<date|none>  macro:<date|none>
step5_tax:            days_to_anniversary:<n>  wash_sale_window:<open until D|closed>  qual_div_window:<state>
step6_plan:           rung:<hit|not hit>  band_state:<inside|breach>  position_pct:<n>%  band_cap:<n>%
step7_liquidity:      spread:<abs>/<pct>  depth_at_size:<yes|no>  class:<tradeable|marginal|writeoff>
step8_records:        level:<price>  target:<price|condition>  improve_by:<date>  events_listed:<yes|no>

disposition:          HOLD|ADD|AVERAGE DOWN|TRIM|CUT|ROTATE|HEDGE|CLOSE
priority_rung:        <1-8>
why:                  <one sentence naming the trigger>
queued:               <actions that qualified but lost, with the clock they represented>
numbers:
  blended_basis:      <$>    [COMPUTED] from <lots and prices>
  post_action_pct:    <n>%   [COMPUTED] from <position value / book value>
  tax_at_stake:       <$>    [COMPUTED] from <gain or loss × rate difference>
  friction:           <$>    [ESTIMATED] from <round-trip band × position value>
  numbers_owner:      equity-tax-lot-and-exit-management | equity-risk-and-capital-engineer | portfolio-signal-manager
clock_that_won:       forced | level | event | tax | plan_rung
mechanism:            first 30 min RTH | at the level | before the event boundary | on the anniversary
escalation_rung:      WATCH|PREPARE|ACT|FORCE
expectation:          <one sentence, falsifiable>
grade_on:             <date>
re_arm_at:            <level that pulls the review forward>
```

### Field notes

- **`step1_forced` is checked first, every time.** A margin call above a $1,000 deficiency must be satisfied by liquidation unless funded, and no advance notice is required [VERIFIED — 12 CFR 220.4(d)]. If this field is anything other than `clear`, the review stops and the disposition is reduce-only.
- **`step2_thesis` carries a version date.** A level with no version is a level that will move. Versioning is what makes "the level quietly moved" a visible defect rather than a feeling.
- **`step3_identity` is a gate for a reason.** Equity positions mutate without anyone trading: a reinvestment, a spin-off, a tender, an overlay someone forgot. A review of a position that is not the position described is a review of nothing.
- **`step5_tax` flags, it does not decide.** The tax clock has no disposition of its own; it appears in `clock_that_won` only when a higher clock did not fire, and then only as a *timing* change to a discretionary action.
- **`clock_that_won`** is the field that makes the precedence table testable. Recording it turns "which clock won" from an argument into data.
- **`numbers_owner`** records who supplied the arithmetic. This skill routes decisions and owns no numbers. A record with `numbers_owner: unknown` is incomplete.
- **`expectation`** must be falsifiable. "The position improves" is not; "the level holds and the position reaches rung 2 at 68.00 by 2026-12-11" is.
- **`re_arm_at`** is a level, not a date. The date is the floor on attention; the level is the trigger.

### Which actions require a record

Every action above HOLD. HOLD itself is recorded on the third consecutive hold on the same position, which is the attention-budget check.

| Action | Record required | Additional evidence |
|--------|-----------------|---------------------|
| HOLD | On the 3rd consecutive hold | A forced re-underwrite paragraph, dated |
| ADD | Yes | All five preconditions marked PASS/FAIL; blended basis `[COMPUTED]` |
| AVERAGE DOWN | Yes | All five gate clauses marked PASS/FAIL; post-add band percentage `[COMPUTED]` |
| TRIM | Yes | Shares before and after; the lot instruction issued; the remainder's rule |
| CUT | Yes | The mechanism, the fill, and the gap versus the mark |
| ROTATE | Yes | The friction `[COMPUTED]`, the replacement's size, and the wash-sale check on both names |
| HEDGE | Yes | Shares protected and residual; cost as a percentage of position; the tax flag and its answer |
| CLOSE | Yes | The reason class, the lot instruction, and whether a wash-sale window opened |

## Part 2 — The grading record

Written at `grade_on`, or at resolution, whichever comes first. It answers one question: **did the action do what it was expected to do, and was the clock that produced it the right one for that case?**

```text
record_id:            <the review record this grades>
graded_at:            <timestamp>
resolution:           at_plan | worse_than_plan | better_than_plan | unresolved_at_deadline
resolved_by:          target | level | improve_by_date | forced_action | event | corporate_action
fill_vs_mark:         <$>   (execution cost, recorded separately from the gain or loss)
clock_that_won:       <forced | level | event | tax | plan_rung>
clock_should_have_won: <only if, in hindsight, a different clock would have been better>
lot_outcome:          <what the lots actually did — the field that ties this record to the tax owner>
lesson:               <one line, specific enough to change a rule>
rule_change:          <none | the rule text change, with a date>
```

### The resolution vocabulary

| Value | Meaning |
|-------|---------|
| `at_plan` | The written expectation was met within the written window |
| `worse_than_plan` | The window passed, or the level broke, without the expectation being met |
| `better_than_plan` | The expectation was met materially early or materially beyond the target |
| `unresolved_at_deadline` | The improve-by date arrived with no disposition applied — always a process defect, never a market outcome |

`unresolved_at_deadline` is the most important category in the whole record. It is the signature of the failure this skill exists to prevent: a position that was never forced by any clock, and therefore never decided.

### Grading discipline

1. **Grade against the written expectation, not against the P&L.** A cut that was correct at the level and profitable by accident grades `at_plan` on process, with a note that the outcome was luck. Confusing process quality with outcome quality is how a bad process survives a good quarter.
2. **Grade the execution separately.** `fill_vs_mark` is an execution measurement; it never justifies changing a level or a band.
3. **Only `clock_that_won` differences produce rule changes.** If the same conflict keeps resolving the same way and keeps being wrong, that is a rule to rewrite — and the record is what proves it.
4. **Grade the tax fields honestly.** `lot_outcome` is where a decision to sell "the shares" rather than "these lots" shows up as a surprise. Recording it is how the lot instruction improves.
5. **One line for the lesson.** A lesson that runs three sentences will not be read, and a lesson that is not read cannot change a rule.

## Part 3 — Illustrative rows (format demonstration only)

**The inputs are invented and the arithmetic is `[COMPUTED]` from those invented inputs.** These are not observations from any account and not a performance claim. The point is the shape of the record and how a grading decision is made.

| record_id | disposition | rung | numbers | expectation | resolution | lesson |
|-----------|-------------|------|---------|-------------|------------|--------|
| EX-01 | CUT | 2 (level breached) | exit at the mark, 500 sh at 62.00, realised 2,000 loss `[COMPUTED]`: 500 × (66.00 − 62.00) = 2,000 | "exit in the first 30 minutes of regular hours; level does not recover" | `at_plan` — resolved by level, fill 2 cents worse than the mark | A cut that fills near the mark is a process success, whatever the P&L says |
| EX-02 | HOLD-WITH-DEADLINE | 8 (nothing triggered) | level 54.20 v1; target 68.00; improve-by 2026-12-11 | "level holds and the position reaches 68.00 by the date" | `unresolved_at_deadline` — the date arrived, no review ran in the final three weeks | The date existed but the cadence did not re-arm at the level; a contract needs both triggers |
| EX-03 | AVERAGE DOWN (refused) | 7 (gate failed) | post-add 22.4% of a 250,000 book against a 10% band `[COMPUTED]`: 56,000 ÷ 250,000 = 22.4% | "no add; the position is already over band, so trim or hold" | `at_plan` — the refusal held and the position was trimmed at the next rung | A refusal is a saved loss only if the alternative is executed; the refusal needs a mechanism |
| EX-04 | HOLD (tax-timed) | 5 (plan rung) | tax at stake 510 `[COMPUTED]`: 3,000 × (0.408 − 0.238) = 510, against 2,789 of 20-session one-sigma risk | "decide the economics first; sell on the anniversary if the level still holds" | `at_plan` — resolved by the improve-by date, sale executed one session after the anniversary | The tax clock changes timing, not the decision; the level was the gate either way |
| EX-05 | TRIM | 5 (rung hit) | 300 of 900 sh at 48.00; proceeds 14,400 `[COMPUTED]`: 300 × 48.00 = 14,400 | "the remainder reaches rung 2 at 54.00, or the trail from 58.00 fires" | `at_plan` — rung 2 filled; lots chosen by the tax owner per the issued instruction | Writing the remainder rule before rung 1 is what made the runner manageable |
| EX-06 | ROTATE | 3 (capital needed) | friction 1,072 `[COMPUTED]`: 952 tax + 120 estimated round trip = 1,072, or 2.69% of 39,900 | "the replacement beats the held position by more than the friction in year one" | `better_than_plan` — resolved by the improve-by date | Computing the friction first turned an intuition into a comparison with a number in it |

### Best case, worst case, and what the record is for

Read the rows as three separate kinds of evidence:

- **Best case.** EX-06 is what the format buys: the rotation was compared against a computed bar rather than a feeling, and the replacement was sized against freed capital rather than assumed capital. The best outcome here is not a large number; it is a comparison that could be argued with.
- **Worst case.** EX-02 is the failure this format exists to surface: a contract existed, the expectation was written, and the position still reached its deadline undecided because the cadence did not re-arm at the level. The record makes that a named, countable defect instead of a story about a bad month.
- **Learnings.** Every row produces exactly one actionable lesson. Only two of the six produce a rule change. That ratio is the point: most decisions are fine, and the ones that are not leave a trace specific enough to rewrite a rule.

## Part 4 — Aggregate views worth keeping

Simple counts. None of them requires statistics to be useful.

| View | How to compute | Why it matters |
|------|---------------|----------------|
| Deadline slippage | Improve-by dates passed without a review, ÷ all improve-by dates | The direct measure of the defect this skill exists to prevent |
| Level version churn | Mean number of versions per invalidation level | A level that moves more than once or twice is not a level |
| Clock audit | For each `clock_that_won`, the share graded `at_plan` | Tunes the precedence table from outcomes instead of opinion |
| Tax-timing outcome | Graded rows where `clock_that_won: tax` | If tax keeps winning and keeps grading badly, the precedence order is wrong or the arithmetic is not being done |
| Gate refusal ledger | Average-down proposals refused, and what happened next | Tests whether the gate is protecting the account or just frustrating it |
| Execution cost | Mean `fill_vs_mark` | Separates execution problems from decision problems, which are fixed in different places |
| Rotation throughput | Rotations executed per year, and their graded outcome | A book with zero rotations is not patient; it is unexamined |

## Part 5 — Where the numbers come from

- Every dollar figure in the illustrative rows is `[COMPUTED]` from the invented inputs stated in the same row, and is reproducible by hand. Nothing here is a measured account result.
- Where a figure depends on live data — marks, spreads, option premiums, dividend dates — the record cites its source inline and the operator fills it in. This document deliberately leaves those blank rather than inventing them.
- Threshold conventions referenced by the format — the per-idea band, the round-trip friction band, the cadence boundaries — are operating conventions of this skill and its upstream sizing skill. They are marked `[ESTIMATED]` or attributed to the skill that publishes them, and they are approximate by construction.
- Statutory and regulatory attributions in this skill name their sources next to the tag (`[VERIFIED]` against the Internal Revenue Code, the Code of Federal Regulations, FINRA rules, exchange rules and the SEC release that shortened the settlement cycle to T+1). No external URL, vendor page or research paper is cited anywhere, and none should be inferred.
- Broker-set numbers — house maintenance percentages, recall notice periods, liquidation timing — are marked `[BROKER-VERIFIED]` and must be read from the schedule the broker actually applies. They are not constants and are not guessed here.
- **Past performance is not a guarantee of future results.** A record of well-graded decisions is evidence about a process; it is not a forecast, and it does not make the next position safe.
