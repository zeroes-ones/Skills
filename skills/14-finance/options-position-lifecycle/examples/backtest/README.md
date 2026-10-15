# Review Record and Grading Format

This directory holds the **evidence format** for this skill: what a desk records on every position review, and how each recorded action is graded later. It describes a structure, not results.

**No performance results are claimed here.** Nothing in this directory is a measured outcome, a backtest, or an equity curve. The illustrative rows below are labelled `[COMPUTED]` arithmetic on invented inputs chosen to demonstrate the format — they are not observations from any account. Where a figure would depend on live data, it is marked `[ESTIMATED]` with its derivation, or left for the operator to fill in from a source they can name.

## Why a record format belongs with a decision skill

A position-management skill produces decisions. Decisions that are not recorded cannot be graded; decisions that are not graded cannot improve the rules that produced them. The precedence table in this skill, in particular, only becomes trustworthy if it can be checked against what actually happened when a rule won.

So the record has two halves:

1. **The review record** — written at the moment of the review, before the action is executed.
2. **The grading record** — written at the revisit date, or when the position is resolved, whichever comes first.

Both are plain text. No special tooling is required; a text file, a spreadsheet, or a notebook all work. What matters is that the fields are the same every time.

## Part 1 — The review record

One record per position per review. The fields are fixed so that two different reviews can be compared, and so that a missing field is visible rather than inferred.

```text
record_id:            <position-id>-<yyyy-mm-dd>-<n>
position:             <underlying, structure, expiry, contracts>
reviewed_at:          <timestamp with timezone>
mark_source:          <where the mark came from>          source: <vendor|broker|manual read>

step1_thesis:         level:<...>  measurement:<close|intraday>  reading:<...>  PASS|FAIL
step2_structure:      legs:<n>  widths:<...>  ratio:<...>  naked:<none|detail>  PASS|FAIL
step3_clock:          dte:<n>  zone:<0-2|3-7|8-21|22-45|46+|leaps>  forces:<one line>  PASS|FAIL
step4_band:           rung_hit:<yes|no>  band_state:<inside|breach>  mark_or_pnl:<...>
step5_liquidity:      width:<abs>/<pct_of_mark>  oi:<n>  class:<tradeable|marginal|writeoff>
step6_events:         earnings:<date|none>  macro:<date|none>  exdiv:<date|none>  other:<...>
step7_instruments:    tp:<live|absent|n/a>  sl:<level + action>  session:<rth|ext>  qty_match:<yes|no>

disposition:          HOLD|ADD|RESTRUCTURE|TRIM|CUT|ROLL|CONVERT|CLOSE
priority_rung:        <1-7>
why:                  <one sentence naming the trigger>
queued:               <actions that qualified but lost>
numbers:
  new_max_loss:       <$>        [COMPUTED] from <width, credit/debit, contracts>
  new_breakeven:      <price>    [COMPUTED]
  credit_or_debit:    <$>        [COMPUTED]
  numbers_owner:      trade-sizing-recovery | options-risk-engineer
mechanism:            into strength | first 30 min RTH | before 15:45 ET | at the event boundary
escalation_rung:      WATCH|PREPARE|ACT|FORCE
expectation:          <one sentence, falsifiable>
grade_on:             <date>
re_arm_at:            <level that pulls the review forward>
```

### Field notes

- **`priority_rung`** is the rung of the action router that fired. Recording it makes disagreements about priority visible: two people can argue about an action, and the record shows which rule each was applying.
- **`numbers_owner`** records who supplied the arithmetic. This skill routes decisions; it does not own band arithmetic or calendar windows. A record with `numbers_owner: unknown` is an incomplete record.
- **`expectation`** must be falsifiable. "The position improves" is not; "the level holds and the mark reaches $1.70 by 2026-11-14" is.
- **`re_arm_at`** is the level, not the date. The date is the floor on attention; the level is the trigger.
- **`mark_source`** matters because marks disagree between venues and between the mid and the last. A review built on a mark nobody can reproduce is not evidence.

### Which actions require a record

Every action above HOLD. HOLD itself is recorded only when it is the third consecutive HOLD on the same position, which is the attention-budget check.

| Action | Record required | Additional evidence |
|--------|-----------------|---------------------|
| HOLD | On the 3rd consecutive hold | A forced re-underwrite paragraph |
| ADD | Yes | The five preconditions, each marked PASS/FAIL, with blended cost `[COMPUTED]` |
| RESTRUCTURE | Yes | The completed five-clause gate worksheet |
| TRIM | Yes | Unit count before and after; the runner's trailing rule |
| CUT | Yes | The mechanism, the fill, and the gap versus the mark |
| ROLL | Yes | Roll count (1 or 2), net credit/debit, old and new break-even |
| CONVERT | Yes | The conversion worksheet with before/after criteria |
| CLOSE | Yes | The resolution type (closed / expired / assigned) |

## Part 2 — The grading record

Written at `grade_on`, or at resolution. The grading record answers one question: **did the action do what it was expected to do, and was the rule that produced it the right rule for that case?**

```text
record_id:            <the review record this grades>
graded_at:            <timestamp>
resolution:           at_plan | worse_than_plan | better_than_plan | unresolved_at_expiry
resolved_by:          target | level | calendar | grading_date | assignment | expiry
fill_vs_mark:         <$>  (execution cost, recorded separately from the loss or gain)
rule_that_won:        <the rank-1..rank-5 rule that bound, if a conflict was arbitrated>
rule_should_have_won: <only if, in hindsight, a different rule would have been better>
lesson:               <one line, specific enough to change a rule>
rule_change:          <none | the rule text change, with a date>
```

### The resolution vocabulary

| Value | Meaning |
|-------|---------|
| `at_plan` | The stated expectation was met within the stated window |
| `worse_than_plan` | The window passed, or the level broke, without the expectation being met |
| `better_than_plan` | The expectation was met materially early or materially beyond the target |
| `unresolved_at_expiry` | The position reached expiry without a disposition having been applied — always a process defect, never a market outcome |

`unresolved_at_expiry` is the most important category in the whole record. It is the signature of the failure this skill exists to prevent: a position that arrived at the end of its life without anyone having decided what to do with it.

### Grading discipline

1. **Grade against the written expectation, not against the P&L.** A cut that was correct at the level and profitable by accident grades as `at_plan` on the process, with a note that the market outcome was lucky. Confusing process quality with outcome quality is how a bad process survives a good quarter.
2. **Grade the execution separately.** `fill_vs_mark` is an execution measurement; it never justifies changing a band or a level.
3. **Only `rule_that_won` differences produce rule changes.** If the same arbitration keeps resolving the same way and keeps being wrong, that is a rule to rewrite — and the record is what proves it.
4. **One line for the lesson.** A lesson that runs three sentences will not be read, and a lesson that is not read cannot change a rule.

## Part 3 — Illustrative rows (format demonstration only)

The rows below show what the format looks like when filled in. **The inputs are invented and the arithmetic is `[COMPUTED]` from those invented inputs.** They are not observations from any account, and they are not a performance claim. The point is the shape of the record and the way a grading decision is made.

| record_id | disposition | priority_rung | numbers | expectation | resolution | lesson |
|-----------|-------------|---------------|---------|-------------|------------|--------|
| EX-01 | CUT | 3 (thesis broken) | exit at the mark of $0.55 on a $1.20 credit `[COMPUTED]`, ≈ +$65 before the exit spread | "level broken, exit in the first RTH window" | `at_plan` — resolved by level, fill 3 cents worse than the mark | A profitable position with a broken thesis is still an exit; the profit paid for a clean fill |
| EX-02 | TRIM | 5 (rung hit) | 2 of 6 spreads at $3.55, booking $330 `[COMPUTED]` | "the remainder reaches the second rung or the trail fires" | `at_plan` — trail fired at $3.28, total booked $1,246 `[COMPUTED]` | Writing the trailing rule before the runner existed is what made the trail executable |
| EX-03 | REFUSE / HOLD | 4 (band breach) | proposed restructure max loss $760 `[COMPUTED]` against a $600 band | "no restructure; the level holds and the position decays" | `worse_than_plan` — the level broke 6 sessions later and the position was cut | A refused repair is a saved loss only if the alternative is executed; the refusal must come with a mechanism |
| EX-04 | HOLD-WITH-TP | 7 (nothing triggered) | target 2.0× the mark, improve-by date 18 sessions out | "level holds and the mark reaches 2.0× by the date" | `unresolved_at_expiry` — no review ran in the final two weeks | The date existed but the cadence did not re-arm; the contract needs the level trigger, not only the date |
| EX-05 | ROLL (refused) | 6 (structure degraded) | net credit $0.30 but the break-even moved from 98.40 down to 95.70 `[COMPUTED]` | "refused; the roll moved the break-even against the thesis" | `at_plan` — cut instead, in the first 30 minutes of RTH | Both proposals ticked "credit"; only one was a roll. The break-even comparison is the test |

### Best case, worst case, and what the record is for

Read the rows above as three separate kinds of evidence:

- **Best case.** EX-02 is what the record buys when the format is used properly: the rung, the trim, the runner rule and the trail all exist before the pressure arrives, and the grading confirms that the process — not the price — produced the outcome. The best outcome here is not a large number; it is a decision that was made calmly and graded honestly.
- **Worst case.** EX-04 is the failure this format is designed to surface: a contract existed, the expectation was written, and the position still reached expiry undecided, because the cadence did not re-arm at the level. The record makes that a named, countable defect instead of a story about a bad week.
- **Learnings.** Every row produces exactly one actionable lesson, and only two of the five rows produced a rule change. That ratio is the point: most actions are fine, and the ones that are not leave a trace specific enough to rewrite a rule. A record that produces a lesson per row but a rule change never is a record nobody is reading.

## Part 4 — Aggregate views worth keeping

These are simple counts from the records, and none of them requires statistics to be useful:

| View | How to compute | Why it matters |
|------|---------------|----------------|
| Action latency | Sessions between a level breach and the action taken | If it is consistently above one session, the cadence or the re-arm triggers are too slow |
| Forced-action share | Actions taken in the 0–2 DTE zone ÷ all actions | A healthy book resolves before expiry; a high number means the earlier zones are being wasted |
| Unresolved count | Records with `resolution: unresolved_at_expiry` | The direct measure of the defect this skill exists to prevent |
| Arbitration audit | For each `rule_that_won`, the share graded `at_plan` | Tunes the precedence table from outcomes instead of opinion |
| Execution cost | Mean `fill_vs_mark`, by family | Distinguishes execution problems from decision problems, which are fixed in different places |
| Refusal ledger | Restructure proposals refused, and what happened next | Tests whether the gate is protecting the account or just frustrating it |

## Part 5 — Where the numbers come from

- Every dollar figure in the illustrative rows above is `[COMPUTED]` from the invented inputs stated in the same row, and is reproducible by hand. Nothing here is a measured account result.
- Where a figure depends on live data — marks, spreads, implied moves — the record cites its source inline and the operator fills it in. This document deliberately leaves those blank rather than inventing them.
- Threshold conventions referenced by the format (rungs, bands, cadence boundaries) are the operating bands of this skill and its upstream sizing skill; they are `[ESTIMATED]` conventions derived from the shape of option payoffs, not measured constants.
- Exchange and regulator attributions in this skill name their sources (`[VERIFIED]` against clearing-house and exchange rules and published margin requirements, for example OCC expiration processing and Cboe margin material). No external URL or research paper is cited here, and none should be inferred.
- **Past performance is not a guarantee of future results.** A record of well-graded decisions is evidence about a process; it is not a forecast, and it does not make the next position safe.
