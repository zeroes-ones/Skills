# Backtest — Evidence Format for `trading-decision-data-catalogue`

> **This file is a FORMAT, not a result.** No market outcome, no dataset performance and no market
> statistic is recorded or claimed here. What is defined is the **evidence record a run of this skill
> must produce** and the **grading rubric** applied to it, so that two runs can be compared without
> argument about what was measured.
>
> Every numeric value below appears inside a worked *grading* illustration whose inputs are stated on
> the spot. Those figures are `[COMPUTED]` arithmetic on those hypothetical inputs. They are not
> observations of any market, and no dataset is claimed to have produced them.

## §1 — What Is Recorded, Per Decision

One record per decision. A record missing any field below is incomplete and grades as a **failure of
evidence**, regardless of whether the decision turned out well.

| Field | Type | Meaning | Required provenance |
|---|---|---|---|
| `record_id` | string | Stable identifier for the decision | — |
| `decided_at` | ISO timestamp | When the decision was made, with the zone | — |
| `decision` | string | One sentence, with an action verb and a horizon | — |
| `horizon` | string | The holding or evaluation window, in the same units as the lags collected | — |
| `regime` | enum | `cash` / `reg-t` / `portfolio-margin` | `[BROKER-VERIFIED]` |
| `dataset_records` | array | The **nine-field catalogue record** for every dataset that entered the decision (see §2) | one kind label and one lag per row |
| `datasets_demoted` | array | Every candidate marked **"nice-to-know"**, with the reason | — |
| `constraints_resolved` | array | Each CONSTRAINT with `date`, `market_calendar`, `calendar_year_read` | `[VERIFIED — named rule]` or stated as unresolved |
| `observed_vs_inferred` | object | For every figure that could be either: which it is, and for inferred ones the assumption and its falsifier | `[COMMON-PRACTICE]` where inferred |
| `base_rate` | object | `values`, `defined_at`, and the position of this line relative to the results line in the document | must precede the results |
| `counterfactual` | object | The alternative action, over the same period and size, **in dollars** with the formula | `[COMPUTED]` |
| `holdout` | object | `period`, `chosen_by`, and whether the sample was point-in-time | `[COMPUTED]` / named source |
| `action` | string | What was decided, in one sentence, with the position ids | — |
| `falsifier` | string | What result would have changed the decision | — |
| `cost_ledger_delta` | object | Any subscription added, cancelled or reconsidered, with the price **read from the vendor's page** or marked unverified | `[VERIFIED — vendor pricing page]` or "price unverified" |
| `outcome` | object | What happened, recorded at the horizon in §3 | `[BROKER-VERIFIED]` where a fill is involved |
| `lesson` | string | One sentence, written only after the outcome is known | — |

**A record with an entry in `datasets_demoted` that is empty fails.** This is the single most common
defect the format exists to catch: a run that discarded nothing did not rank anything, and a
catalogue that ranks everything as useful is worthless.

## §2 — The Nine-Field Dataset Record, Embedded

Every element of `dataset_records` carries all nine fields. A row missing one fails.

| Field | Value shape | The specific thing being graded |
|---|---|---|
| `question` | one line, verb phrase | that the dataset is anchored to the decision, not collected |
| `kind` | `SIGNAL` / `STATE` / `CONSTRAINT` | exactly one; a blank or "both" fails |
| `source` | publisher + dataset name (+ endpoint or file) | that a second person can find it again |
| `cost` | `free`, or the tier and price | a price not read from the vendor says **"price unverified"** |
| `frequency` | what the publisher says | — |
| `lag` | when *you* can see it | **must be separate from `frequency`** |
| `how_it_lies` | the documented failure mode | the trap that will bite this specific dataset |
| `decision_changed` | the action that differs | if empty, the row must move to `datasets_demoted` |
| `rank` | integer, with `nice-to-know` allowed | that at least two rows per decision are demoted |

## §3 — The Outcome Horizon

The horizon is set at decision time and **is not moved afterwards**.

| Decision class | Horizon | Why |
|---|---|---|
| **short-entry** | the borrow's own stated recall terms, or 10 sessions | the entry either survives the constraint or does not |
| **event-hold** | the event's own resolution date | the event's clock ends when it ends |
| **flow-read** | 5 sessions | the flow claim has a short stated life |
| **thesis-underwrite** | the next scheduled review, or the quarter end | a thesis is a standing view |
| **signal-triage** | the validation's own stated holding period | the claim was about that period |
| **budget-prune** | the next quarterly re-audit | a subscription decision is graded at the re-audit |
| **backtest-audit** | the backtest's own period | the claim was about that period |

## §4 — Grading

Each record is graded on **five axes**, each scored 0–2. A record scoring **below 8 of 10 is a failed
evidence record**, even if the decision turned out well.

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| **Provenance** | a number with no tag | tags present but a `[VERIFIED]` lacks a named source, or a price is asserted without being read | every number tagged; every `[VERIFIED]` names a rule, statute, release or dataset page; every price read or marked unverified |
| **Freshness** | lag absent, or inferred | a frequency given and the lag implied | a frequency **and** a separate lag, read from the publisher, compared against the horizon |
| **Kind discipline** | kinds absent | kinds present but an inferred figure presented as observed | every row labelled; every inferred figure names its assumption and its falsifier |
| **Counterfactual** | adjectives ("the data was better") | a percentage with no dollars | dollars, same size and period, with the formula shown |
| **Discard** | nothing demoted | one demotion with a weak reason | at least two demotions per decision, each with a stated reason |

**Favourable outcome does not upgrade a grade.** A decision that made money on an unsourced number is
an unsourced number, and the next one will not be so lucky. Equally, an unfavourable outcome does not
downgrade a record whose evidence was sound — the point of the format is to grade the *evidence*, not
the outcome.

## §5 — Worked Grading Illustration [COMPUTED]

Hypothetical inputs, stated once, used by both runs below. **No market data is implied, and no
dataset is asserted to behave as described.** The two runs differ only in the quality of their
evidence.

```
INPUTS (hypothetical, fixed for reproducibility)
  decision            "consider shorting NAME ahead of the print"
  horizon             10 trading days
  regime              reg-t margin, NAV $500,000
  candidate datasets  D1 broker borrow, D2 threshold list, D3 short interest,
                      D4 daily short-sale volume, D5 GEX heatmap,
                      D6 a social-sentiment feed
  annual data cost    0 (all candidates free or already held in this illustration)
```

```
Run 1 — graded 10/10

  dataset_records (abbreviated; all nine fields present per row)
    D1 kind=CONSTRAINT  source=broker platform, read 2026-10-14T09:31-05:00
       frequency=continuous   lag=none (no publication; read time recorded)
       how_it_lies=one broker's inventory, not the market's; changes intraday
       decision_changed=whether the short is sized against an inventory that exists
       rank=1
    D2 kind=CONSTRAINT  source=exchange threshold list, as-of recorded
       frequency=daily   lag=per the exchange's own publication
       how_it_lies=one exchange's list is not the universe; SEC says appearance is
                    not a negative statement about the issuer
       decision_changed=whether a close-out clock removes the trade entirely
       rank=2
    D3 kind=STATE       source=FINRA Rule 4560
       frequency=semi-monthly
       lag=settlement on the 15th or last settlement business day; publication on the
           7th business day after settlement; Revision Flag overwrites history
       how_it_lies=a rise may be a correction to a prior period
       decision_changed=whether the name is crowded
       rank=3
    D4 kind=STATE (flow)  source=FINRA daily short-sale volume
       frequency=daily  lag=daily
       how_it_lies=off-exchange only (TRF/ADF/ORF); FINRA states it does not equate
                   to bi-monthly short interest
       decision_changed=NONE -> DEMOTED
       rank=nice-to-know
    D5 kind=SIGNAL (inferred)  source=vendor GEX product
       frequency=intraday display   lag=n/a (not a publication; an inference)
       how_it_lies=inferred from open interest under the vendor's sign convention;
                   flipping the convention flips the conclusion
       decision_changed=NONE at this horizon without a stated assumption -> DEMOTED
       rank=nice-to-know
    D6 kind=SIGNAL  source=social-sentiment feed
       frequency=continuous   lag=continuous
       how_it_lies=tone over a self-selected sample; no base rate; horizon unstated
       decision_changed=NONE -> DEMOTED
       rank=nice-to-know

  datasets_demoted  3  (D4, D5, D6) — each with a stated reason
  constraints_resolved
    threshold close-out clock: 13 consecutive settlement days, resolved to a date on
    the exchange calendar for the year, calendar_year_read=2026
  base_rate.defined_at  2026-10-14T10:02-05:00  (BEFORE any signal was opened)
  counterfactual         the same short at the same size without the borrow check:
                         [COMPUTED] 4,000 shares × $0.42 of modelled extra slippage
                         if the borrow had to be replaced mid-hold = $1,680 cost
  holdout.period        the 12 most recent completed quarters, chosen by the analyst
  action                "sized the proposed short to the broker's stated borrow
                         inventory less a 40% buffer"
  falsifier             "if the borrow inventory is below 1.5× the proposed size at
                         the open, do not enter at all"
  cost_ledger_delta     $0 (no subscription added; all candidates free or held)
  lesson                written only after the outcome

  GRADING  provenance   2 (every figure tagged; the borrow is BROKER-VERIFIED with a read time)
           freshness    2 (frequency and lag separate on every row; D3's lag read from FINRA)
           kind         2 (D4 labelled a flow; D5 labelled inferred with its assumption)
           counterfactual 2 ($1,680 with the formula, same size and period)
           discard      2 (three demotions, each with a reason)
           TOTAL       10/10
```

```
Run 2 — the same decision, graded 3/10

  "Short interest is up and there's a lot of put buying, so shorts are piling in.
   The GEX chart says dealers are long gamma at the strike, so a squeeze is likely."

  datasets_demoted   none
  frequency for D3   "semi-monthly"; lag: ABSENT
  D4                 used as if it were short interest
  D5                 presented as an observation of dealer positioning
  base_rate          never defined; the results were read first
  counterfactual     none

  GRADING  provenance   0 (numbers with no tags, and no named source)
           freshness    1 (a frequency given for one dataset, no lags anywhere)
           kind         0 (an inferred figure presented as observed)
           counterfactual 0 (no comparison, no dollars)
           discard      2 (nothing was claimed to be important, but nothing was sourced)
           TOTAL        3/10  ->  FAILED EVIDENCE RECORD, and the short was sized against
                                 an assumption about dealer positioning
```

## §6 — Notes for the Grader

1. **Grade the record, not the outcome.** The outcome column is evidence *about* the record, not the
   record's grade.
2. **The position of the base-rate line is a fact about the document.** Check it by reading order,
   not by asking.
3. **"Unverified" is a passing answer; a guess is not.** A record that says a vendor price could not
   be read scores 2 on provenance. A record that states a price it did not read scores 0.
4. **A demotion list is not a sign of a weaker analysis.** It is the sign of a completed one.
5. **Where a field's provenance tag is `[COMMON-PRACTICE]`, say what convention it is.** That is a
   different, and acceptable, claim from a verified one.
