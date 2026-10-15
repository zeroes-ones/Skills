---
name: timeframe-performance-statistics
description: >
  Use when the question is WHICH REVIEW TIMEFRAME a book's PnL should be judged by — "which
  timeframe should I review", "daily or monthly stats", "is my edge real or noise", "how many
  trades before I can trust this", "show me my PnL by week/month/quarter", "am I beating
  losses", "my win rate". Handles the bucketing itself (day, week, 2-week, month, quarter,
  half, year), which bucket's statistics are actually trustworthy, the nesting and
  autocorrelation caveat, and the cadence rule tying review timeframe to average holding
  period. Ships a deterministic stdlib-only calculator that prints a VERDICT with its caveat.
  Do NOT use for metric DEFINITIONS — Sharpe, Sortino, Calmar, drawdown, profit factor
  (trade-performance-analyst); per-trade sizing (trade-sizing-recovery, portfolio-signal-manager,
  algorithmic-trader); the review SCHEDULE of an open position (options-position-lifecycle,
  equity-position-lifecycle); or which market data to buy (trading-decision-data-catalogue).
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: active
version: "1.0.0"
updated: 2026-10-14
tags:
  - performance-measurement
  - review-cadence
  - timeframe
  - bucketing
  - small-sample-statistics
  - t-statistic
  - autocorrelation
  - effective-sample-size
  - drawdown-by-period
  - win-rate
  - break-even-win-rate
  - profit-factor
  - trade-journal
  - deterministic-calculator
  - holding-period
  - marginal-edge
token_budget: 4500
chain:
  examples:
  - skills/14-finance/timeframe-performance-statistics/examples/logs
  consumes_from: [trade-performance-analyst]
  feeds_into: [edge-and-payoff-engineering]
---

# Timeframe Performance Statistics

> **Portability target:** spec-level. The bucketing is pure calendar arithmetic and the engine is stdlib-only Python 3 with no network, no vendor and no broker dependency. Every threshold is a named, printed constant.

<!-- QUICK: 30s -->
The whole skill is one question: **at which review timeframe do my statistics become trustworthy?** Run the engine, read the VERDICT, read the caveat that comes with it — the caveat is always printed, because the buckets are nested and a bucket t-statistic is a stability indicator, not a significance test.

This skill owns **the bucketing** and **the significance of each bucket**. It owns nothing about what the metrics *mean* — that is `trade-performance-analyst` — and nothing about the review *schedule* of an open position — that is the two lifecycle skills.

<!-- STANDARD: 3min -->
The honest answer is usually uncomfortable: **more periods is not more information, and no bucket choice can turn 120 trades into evidence.** On the shipped synthetic demonstration the only bucket clearing both gates has a t-statistic of 0.948, and the only bucket clearing |t| ≥ 2 has two periods. Both facts are in the same table, and reading them together is the skill.

---

## Route the Request

### Auto-Route (no user input needed)

| The request sounds like | Where it goes |
|---|---|
| "Which timeframe should I review — daily, weekly, monthly?" | Core Workflow step 2, then the engine |
| "Show me my PnL by week / month / quarter" | Run the engine; the `--csv` block is the series |
| "Is my edge real, or is it noise?" | The VERDICT and the beat-losses test together |
| "How many trades before I can trust this?" | `(references/significance-and-sample-size.md)` |
| "Am I beating losses?" | The beat-losses test — `win_rate` vs `break_even_win_rate` |
| "My win rate is 55%" | Compare it to *this book's* break-even rate, never to 50% |
| "Which bucket gave the best Sharpe?" | Refuse the framing: buckets are nested, and this skill does not annualise |
| "What was my worst drawdown?" | `max_drawdown` **at the finest bucket with defensible trades-per-period**, not the convenient one |

<!-- DEEP: 10+min -->
### Ask or fetch, never assume

1. **What is in `pnl`?** Net or gross of commission, fees, financing and spread. Every number below it is gross or net according to this one answer, and the engine cannot tell.
2. **What is the `close_date`, and which population is this?** The closing *fill's* trade date is the right key; a settlement date, expiry date or order date shifts every bucket. One account and one instrument class per run.
3. **What is the average holding period, and the capital base?** The cadence rule needs the first; only the return-based rows need the second, and inventing one is worse than omitting it.

---

## Anti-Rationalization

| The rationalization | The reality |
|---|---|
| "The weekly view shows a better edge than the monthly view" | Impossible. Every trade is in every bucket, so `win_rate`, `payoff_ratio`, `break_even_win_rate` and `edge` are identical in all seven columns. Only `t_stat`, `n_eff` and `max_drawdown` move |
| "120 daily periods is a bigger sample than 13 monthly ones" | The same 120 trades, re-arranged. No new information. And a one-trade period has no payoff ratio at all |
| "The monthly t-stat is 0.948, so I need more months" | More months adds periods at a constant trades-per-period, which does help. Reviewing the *same* book weekly instead of monthly does not: it buys periods and pays with trades per period |
| "The yearly bucket shows |t| = 2.079, so the yearly view is significant" | Two periods. One degree of freedom in the denominator. The engine excludes it on `n_periods` |
| "I review all seven buckets and take the strongest" | A selection across seven candidates, with roughly a 30% chance that at least one clears a 5% threshold by luck — before the dependence adjustment, which makes it worse |
| "The yearly drawdown is 0.00, so the book is low risk" | The daily bucket measured −$2,007.03 on the same trades. A bucket that cannot see risk is not measuring it |
| "My win rate is 55%, that's above break-even" | The break-even rate for this book is 48.88%, and 6.12 points of edge is inside 2 × 4.54 points of standard error. The engine says FAIL |
| "Sharpe 0.26 monthly means Sharpe 0.91 annualised" | This engine refuses to annualise Sharpe: lookback, frequency and risk-free rate are required and none are guessed. `trade-performance-analyst` owns that gate |
| "The half-yearly view is smoother, so it's more stable" | It reports `lag1_autocorrelation = n/a` because three periods cannot estimate a correlation, and its drawdown is 46% below the daily figure |
| "Fees are a rounding detail" | Fees are per trade and hit every bucket equally, so seven buckets will agree on a gross edge that may be negative net |

---

## Ground Rules

**These are gates, not advice. Each has a mechanical trigger and a fixed response.**

| Rule | Mechanical Trigger | Violation Response |
|---|---|---|
| R1 | A bucket statistic is quoted without naming the bucket, the trade count and `n_eff` | STOP. Restate all three in the same sentence, or strike the statistic |
| R2 | Two buckets presented as corroborating each other (weekly *and* monthly, quarterly *and* yearly) | STOP. Say the buckets are nested and the same trades are re-aggregated; call it one stability check |
| R3 | Any claim using the words "proven", "confirmed" or "significant" about an edge | STOP. Quote `edge_test` (`PASS`/`FAIL`) and the required trade count from `(references/significance-and-sample-size.md)` |
| R4 | `max_drawdown` quoted from a bucket that is not the finest with defensible `trades_per_period` | STOP. Report the fine-bucket figure, or apply the owning skill's 1.3–1.5× band and label it `[ESTIMATED]` |
| R5 | Any annualised figure produced from a bucket, including annualised Sharpe | STOP. This engine does not annualise. `--capital` adds three simple returns with a printed warning and nothing more |
| R6 | A `t_stat` quoted without its `n_eff` on the same line | STOP. The engine prints them together; carry the line |
| R7 | An engine output quoted without the provenance of the data behind it | STOP. The engine echoes the log's `# PROVENANCE:` lines for exactly this reason; paste them |
| R8 | A synthetic or illustrative log presented as a result, a backtest or a market finding | STOP. It is a demonstration of the engine, not evidence about any instrument |
| R9 | The bucket chosen after seeing which bucket produced the best number | STOP. Re-derive the bucket from the cadence rule, or disclose the search across seven buckets |
| R10 | A `win_rate` compared to 50%, to a benchmark, or to another book's win rate | STOP. Compare it to *this* book's `break_even_win_rate`, which the engine prints |
| R11 | A metric definition (Sharpe, Sortino, Calmar, profit factor, drawdown) restated as if owned here | STOP. Hand the definition back to `trade-performance-analyst` and cite it |
| R12 | A review cadence stated from habit ("monthly because reports are monthly") | STOP. Compute the mean holding period from `close_date − open_date` and apply the quarter-to-half rule |

**Always:**
- **Admit uncertainty** — if the fee treatment, the `close_date` convention or the capital base is unknown, say so before printing a number.
- Name the bucket in every sentence that contains a statistic. A statistic without its bucket is not a statistic.
- Print `n_eff` next to `n_periods`. Always. The engine does; the report must.
- Keep the synthetic label attached to synthetic data. It is cheap and it is the whole defence.

---

## The Expert's Mindset

<!-- QUICK: 30s -->
An expert reads a timeframe table and looks **first at the coverage rows, not the statistics**: how many periods, how many trades per period. The statistics cannot rescue a bucket whose periods are one trade each, and no amount of arithmetic fixes a book with too few trades. The second thing an expert looks for is **the bucket that looks best** — because that is usually where the trap is.

Three habits distinguish the expert from the enthusiast:

1. **They treat `n_eff` as part of the number.** A 13-period t-statistic with an effective sample of 10.8 is a weaker claim than the integer suggests, and the expert says so unprompted.
2. **They separate description from inference.** "The win rate was 55% against a 48.88% break-even" is a fact about a sample. "The edge is real" is an inference the sample does not support. The expert never lets the first sentence drift into the second.
3. **They quote the refusals.** Every `n/a` in the engine's output is a deliberate guard with a reason attached — one period has no spread, three periods cannot estimate autocorrelation, a bucket with no loser has no break-even rate. The expert reports the guard, not a workaround.

And the habit underneath all three: **an expert is more interested in the bucket that failed than the one that passed.** On the shipped log, the finding is not "monthly is the answer" — it is "`2W` missed the gate at 4.44 trades per period — 27 periods would need 135 trades to reach 5.00, so this book sits 15 trades short of a genuinely finer review timeframe". That sentence is worth more than the verdict.

---

## Deliberate Practice

<!-- STANDARD: 3min -->
| Level | Drill | Time | Success criterion |
|---|---|---|---|
| Novice | Run the engine on `examples/logs/hand-check-synthetic.csv` and hand-verify every field of the monthly bucket against the expected block in the file's header | 30 min | Every value matches on paper, including `t_stat = 5.000000` and `payoff_ratio = 1.666667` |
| Intermediate | Run the illustrative log with `--bucket M` and `--bucket M --capital 250000`. Explain why every *trade totals* row is identical and only the return rows differ | 20 min | Can state the bucketing-invariance of pooled trade statistics without looking it up |
| Advanced | Re-generate the illustrative log with the seed changed, then re-run. Predict which buckets change verdict and why | 40 min | Predicts the gate that will move, and checks it |
| Advanced | Take your own ledger and run all seven buckets. Write one paragraph per bucket saying why it does or does not qualify, quoting the failing constraint | 60 min | Every paragraph cites a gate field, not an impression |
| Expert | Compute the trade count your edge would need for 80% power, run the engine monthly for six months, and chart `t_stat` and `n_eff` against `n_trades` | 6 months | Can say whether the claim is strengthening because the sample is growing, or because composition shifted |
| Expert | Deliberately construct a book whose yearly bucket reports a large |t| with two periods, and write the memo explaining why that is not a finding | 30 min | The memo names the degrees of freedom, not just the period count |

**The one drill that changes behaviour:** re-run the engine with the largest single win and the largest single loss removed from the log. If the verdict or the `edge_test` flips, you have learned how much of your headline rests on two trades. Do it once per quarter on the real ledger.

**The drill that fixes the habit for good.** Take any timeframe claim you have made in the last year. Re-run the engine over the full log it rested on, then answer four questions in writing: (1) how many trades were in the sample, and how many *effective* periods did the claim really rest on; (2) was the bucket chosen from the holding period, or from the number it produced; (3) did the claim survive removing the largest win and the largest loss; (4) was the drawdown measured at a resolution that could see it. If any answer is uncomfortable, restate the claim in the next review with both figures and the dates. The engine's archive makes that a two-minute job; not having one is why the claim gets re-made instead of corrected.

---

## Operating at Different Levels

| Level | Scope | Autonomy | Craft expectation |
|---|---|---|---|
| L1 Apprentice | Run the engine on one log with the default buckets; read the VERDICT line | None — the bucket choice is given | Can find `n_periods`, `trades_per_period` and `t_stat` and say which gate failed |
| L2 Practitioner | Choose the bucket from the cadence rule before looking at P&L; report the gate failures per bucket | Sets the bucket, not the thresholds | Can explain in one sentence why a bucket failed and what would change it |
| L3 Senior | Own the monthly review: archive output, track `t_stat`, `n_eff`, `edge` and `edge_test` month over month | Owns the review record | Distinguishes a claim strengthening from a sample composition change, and says which is happening |
| L4 Lead | Own the timeframe system for several books of different holding periods; set per-book cadences and gates; split mixed logs by population | Owns the review design | Can show, from the archive, which bucket was named when and whether the naming was stable |
| L5 Transformative | Own the governance: who runs the engine, who reconciles the log, who independently checks the verdict. Make the caveat non-optional in the tooling | Owns the evidence chain | Can produce, on demand, the six-month trail showing a claim's strength and the refusals that bound it |

**The shift that matters:** at L1–L2 the practitioner is looking for an answer. At L3+ they are maintaining a record that can be audited, and the record's most valuable entries are the `FAIL` and `n/a` lines.

---

## When to Use

- **Choosing a review timeframe** for a book's realised P&L: daily, weekly, biweekly, monthly, quarterly, half-yearly or yearly.
- **Asking whether an edge is real or noise** at the granularity the trade count supports — and getting an explicit `INSUFFICIENT DATA` when it does not.
- **Deciding how many trades are needed** before a claim can be made, with the arithmetic shown.
- **Testing whether the win rate beats its own break-even rate**, and by how much.
- **Producing a per-period P&L series** — week, month, quarter — with cumulative P&L and per-period drawdown.
- **Measuring drawdown at a defensible resolution** and seeing how much a coarser bucket hides.
- **Reconciling a bucket series** to the ledger total (`sum(net_pnl)` must equal total trade P&L for every bucket).
- **Setting a cadence from a holding period**, and checking that it agrees with the two lifecycle skills' cadence tables.
- **Auditing someone else's timeframe claim** — nested buckets presented as corroboration, a yearly t-statistic on two periods, an annualised Sharpe from a 13-month sample.

## When NOT to Use

| Not this skill | Use instead |
|---|---|
| Sharpe, Sortino, Calmar, alpha, information ratio, benchmark-relative returns | `trade-performance-analyst` — definitions and inputs are owned there |
| Whether a metric is meaningful at N < 200 trades, the Sharpe standard-error formula, minimum sample sizes per metric | `trade-performance-analyst` — its `references/small-sample-statistics.md` |
| Position size, contract counts, loss bands, TP/SL levels | `trade-sizing-recovery`; portfolio-level sizing and signal aggregation → `portfolio-signal-manager`; systematic execution and backtest engine → `algorithmic-trader` |
| Whether today is the day to trim, roll, cut or close an open position | `options-position-lifecycle`; for equities `equity-position-lifecycle` |
| Whether the review should happen *today* because an event or a level came into range | the two lifecycle skills' re-arm triggers — a monitoring cadence, not a performance cadence |
| Which datasets to buy, which are free, what a feed costs | `trading-decision-data-catalogue` |
| Whether the trades in the log were independent decisions | `verification-independence-engineer`; the log's own completeness is a reconciliation problem, not a statistics problem |
| Tax lots, wash sales, holding-period barriers | `equity-tax-lot-and-exit-management` |
| Whether a regime is bull, correction, bear or crash right now | `macro-strategist`; this skill buckets by calendar, not by regime |

---

## Decision Trees

### DT1 — Which review timeframe should this book use?

```
Is the average holding period computed from close_date - open_date?
  ├─ NO  → compute it first. Every path below depends on it.
  └─ YES → cadence window = average holding period x [0.25 .. 0.50]
            ├─ under 1 day   → session-level: the bucket tool is the wrong instrument
            ├─ 1 .. 6 days   → W   (weekly)
            ├─ 6 .. 15 days  → W or 2W
            ├─ 15 .. 45 days → 2W or M
            ├─ 45 .. 135 days→ M
            ├─ 135.. 270 days→ Q
            └─ over 270 days → Q or H, and accept that a year holds 2-4 periods
                                  ▼
                        NOW run the engine on ALL buckets and read the gates.
                        If the cadence bucket fails a gate:
                          ├─ trades_per_period < 5 → cadence finer than the trade count
                          │    supports: review at that cadence DESCRIPTIVELY and carry
                          │    the claim on the coarse bucket.
                          └─ n_periods < 12 → the sample is too short. The finding is
                               "not enough history", not "wrong bucket".
```

### DT2 — Is this bucket's statistic trustworthy?

```
Read the bucket's coverage rows first.
  │
  ├─ n_trades differs between buckets?
  │     └─ YES → a trade was dropped or double-counted. STOP. Fix the export.
  │
  ├─ trades_per_period < 5 ?
  │     ├─ YES → periods carry no within-period averaging. The t_stat is about
  │     │         ordered trade outcomes, not period performance. NOT a period statistic.
  │     └─ NO  → continue
  │
  ├─ n_periods < 12 ?
  │     ├─ YES → the t-statistic is estimable but unstable. Report it as a
  │     │         description of a short sample. It cannot carry a claim.
  │     └─ NO  → continue
  │
  ├─ t_stat = n/a ?
  │     ├─ single period → no across-period variance exists. Report as n/a.
  │     ├─ sd = 0        → zero spread. Report as n/a; investigate before trusting.
  │     └─ otherwise     → read the --json note field for the stated reason.
  │
  ├─ |t_stat| < 2 ?
  │     ├─ YES → NOT DISTINGUISHABLE FROM NOISE. Report the number AND the band.
  │     └─ NO  → continue, but still quote n_eff next to n_periods
  │
  ├─ n_eff well below n_periods (rho > 0) ?
  │     └─ YES → the t_stat is optimistic. State the effective sample, not the count.
  │
  └─ max_drawdown reported from this bucket?
        └─ only if this is the FINEST bucket with trades_per_period >= 5.
           Otherwise take drawdown from that finer bucket and say so.
```

### DT3 — Are you beating losses?

```
pooled across the WHOLE log (identical in every bucket):
  break_even_win_rate = 1 / (1 + payoff_ratio)
  │
  ├─ payoff_ratio = n/a (no loser in the sample)
  │     └─ the break-even rate is undefined. Say so. A book with no loss has no
  │        measurable edge either — it has an untested one.
  │
  ├─ edge <= 0 ?
  │     └─ YES → the booking wins too rarely for its own average sizes. The timeframe
  │              is not the problem. This is a sizing, selection or exit problem.
  │
  ├─ edge > 0 but edge <= 2 x se_win_rate ?
  │     ├─ YES → edge exists in the sample, unproven. Compute the trade count needed
  │     │         for 80% power. State both numbers.
  │     └─ NO  → continue
  │
  ├─ edge > 2 x se_win_rate ?
  │     └─ PASS on the win-rate test. Still not a proven strategy: no out-of-sample
  │        period, no regime coverage, no independent verification. Say which.
  │
  └─ regardless of the path: recompute with the largest win and the largest loss
        removed. If the sign of edge flips, one trade is carrying the headline.
```

### DT4 — Drawdown: which number do you quote?

```
Do you have daily-resolution trade data?
  ├─ YES → compute max_drawdown at the finest bucket with trades_per_period >= 5
  │         (often D or W). Quote that. Name the bucket in the sentence.
  └─ NO  → you are on a coarse bucket → apply the 1.3-1.5x band owned by
            trade-performance-analyst, tag it [ESTIMATED], and write "estimated".

Then, always:
  ├─ compare against the coarser buckets and report the uplift as a percentage
  ├─ name the peak period and the trough period (from --csv or --periods)
  └─ if a coarser bucket reports a DEEPER drawdown than a finer one → periods were
     sorted wrongly. STOP and check the input ordering.
```

---

## Core Workflow

### Phase 1 — Get the log right (before any statistic)

1. Export one row per closed trade: `trade_id,open_date,close_date,pnl,risk,symbol`.
2. Write the `# PROVENANCE:` block: source, window, account, fee treatment, partial-exit convention.
3. Confirm `close_date` is the closing **fill's** trade date, not a settlement or expiry date.
4. Confirm `pnl` is net or gross per your provenance line, and that the choice is deliberate.
5. Split by population: one account and one instrument class per run.
6. Compute the mean holding period from `close_date − open_date`. This sets the cadence.

### Phase 2 — Fix the cadence before looking at P&L

7. Apply the quarter-to-half rule. Write the bucket down. Do not change it after seeing the numbers.
8. Cross-check the chosen cadence against `options-position-lifecycle`'s DTE-zone table or `equity-position-lifecycle`'s time-axis table. They govern *monitoring*; this governs *performance review*. Both can be true at once.

### Phase 3 — Run the engine

9. `py -3 scripts/timeframe_stats.py --csv <log> > reviews/YYYY-MM-timeframe-stats.txt`
10. Read the coverage rows first: `n_trades` must match in all seven columns.

**Complete when** `n_trades` is identical across every bucket and `cumulative_pnl` equals total trade P&L.

11. Read the gate failures per bucket.
12. Read `t_stat` and `n_eff` on the same line, then the noise band.
13. Read `max_drawdown` from the finest bucket with `trades_per_period >= 5`.
14. Read the beat-losses sentence and the `edge_test`.

**Complete when** the verdict, the caveat and the beat-losses result are all copied into the review record.

### The twelve traps — each with its countermeasure

1. **Trap: more periods is treated as more information.** The same trades re-aggregated create periods, not evidence. *Countermeasure:* quote `n_trades` alongside `n_periods` in every sentence; if `n_trades` did not change, nothing was learned.
2. **Trap: overlapping and nested buckets are treated as independent tests.** H contains Q contains M; Y contains all. *Countermeasure:* the engine prints the dependence caveat unconditionally — carry it, and never write "the weekly and monthly views agree".
3. **Trap: annualising a short sample.** Monthly mean × 12, or `period_sharpe × sqrt(12)`. *Countermeasure:* the engine refuses to annualise Sharpe and warns on the one simple return figure it does print; report only the observed window.
4. **Trap: Sharpe compared across buckets of different sample size.** `SE ≈ 1/sqrt(N)` means a 53-period Sharpe and a 13-period Sharpe are not comparable. *Countermeasure:* never compare period Sharpes across buckets; if a Sharpe comparison is required, take it to `trade-performance-analyst` with lookback, frequency and risk-free rate declared.
5. **Trap: autocorrelated period returns inflate the t-stat and shrink the effective sample.** *Countermeasure:* read `n_eff` next to `n_periods`; both are printed. On the illustrative log `D` loses 35% of its apparent sample and `M` loses 17%.
6. **Trap: survivorship and timing inside the log itself.** Trades not logged, ideas abandoned before entry, partial exits collapsed into one row. *Countermeasure:* reconcile `n_trades` against the broker's blotter every quarter; declare the partial-exit convention in the provenance block.
7. **Trap: the break-even rate is driven by one outlier trade.** With a 6.12-point edge, one −2.4R tail can flip the sign. *Countermeasure:* recompute with the largest win and largest loss removed and report both figures.
8. **Trap: drawdown from a coarse bucket hides the intra-month trough.** Monthly understated the daily figure by 21.17% on the illustrative log; the yearly bucket reported 0.00 against a real −$2,007.03. *Countermeasure:* quote drawdown from the finest defensible bucket, or apply `trade-performance-analyst`'s 1.3–1.5× band and tag it `[ESTIMATED]`.
9. **Trap: zero-P&L trades silently deflating the win rate.** *Countermeasure:* the engine reports `breakeven_trades` and excludes them from the denominator; state which denominator you used.
10. **Trap: fees absent from `pnl`, so every timeframe flatters the strategy equally.** *Countermeasure:* declare the fee treatment in the provenance block, then subtract a plausible round-trip cost and re-run; if the edge flips sign, the timeframe was never the problem.
11. **Trap: mixing instrument classes or accounts in one bucket series.** The pooled `payoff_ratio` then describes a population that does not exist. *Countermeasure:* one population per run; compare the verdicts, not the period counts.
12. **Trap: bucket boundary assignment.** A trade closing on the last day of a period belongs to that period. *Countermeasure:* the close-date convention is printed on every run; a one-day shift in `close_date` moves trades and is visible only by checking the printed span.
13. **Trap: a strategy with fewer than 12 periods declared "proven".** *Countermeasure:* the verdict returns `INSUFFICIENT DATA` and names the failed constraint — quote that, not a bucket.

### Regime Table

Buckets are calendar artefacts; **a bucket does not know what regime it contains**, and the engine has no regime label to work with. What changes is how a timeframe claim should be read.

| Regime | What the buckets look like | What changes here |
|---|---|---|
| **Bull market / uptrend** | Fine buckets produce long runs of small positive periods; `lag1_autocorrelation` is positive; `max_drawdown` is shallow and short-lived | The danger is over-confidence. A positive `t_stat` in an uptrend is often measuring the regime, not the strategy. A short-premium book's win rate rises. Quote the sample window explicitly and state which regime it covers |
| **Correction / pullback** | A cluster of negative periods inside a longer positive run; `n_eff` falls; the same trades now look noisier | Corrections are where a bucket boundary decides the story: a correction spanning a month-end appears in two monthly periods and looks milder than it was. Prefer the finer bucket for drawdown; state the peak and trough periods by name |
| **Bear market / downturn / drawdown** | Long negative runs; `sd_period_pnl` rises sharply; `t_stat` collapses or inverts; drawdown becomes the dominant field | A long-premium or trend book may look best here and worst in the bull market. **Do not compare a bear-market bucket statistic with a bull-market one as if they were the same test** — different regimes, different populations, and the coarse buckets may contain both |
| **Crash / tail event / black swan (for example March 2020)** | A single period that dwarfs the rest; `mean_period_pnl` moves more than `sd`; `payoff_ratio` moves entirely because of one trade | This is the regime that makes every bucket statistic unstable, and it is the reason a yearly bucket showing a large |t| on two periods is meaningless. **A sample containing one crash and no second one cannot estimate crash risk.** Say that, and treat the crash period as a named observation rather than as a data point in a series |

### Failure Modes

**Failure modes and known limitations — what goes wrong with timeframe analysis, and the countermeasure for each:**

1. **Failure mode: the bucket is chosen from the answer.** Seven buckets are tried and the best one is reported. Countermeasure: derive the bucket from the holding period before looking, or disclose the search.
2. **Failure mode: the yearly bucket reports a large |t| and is quoted.** Two periods, one degree of freedom. Countermeasure: the gate excludes it; quote the gate.
3. **Failure mode: nested buckets presented as corroboration.** Countermeasure: the engine's dependence caveat is printed unconditionally; carry it verbatim.
4. **Failure mode: `n_eff` dropped because `n_periods` looked better.** Countermeasure: the engine prints them on the same line; carry the line, never the number alone.
5. **Failure mode: drawdown quoted from the coarsest bucket.** On the illustrative log that is 0.00 against a real −$2,007.03. Countermeasure: finest defensible bucket, or the owning skill's 1.3–1.5× band tagged `[ESTIMATED]`.
6. **Failure mode: a marginal edge announced as proven.** A 6.12-point edge against a 9.08-point threshold. Countermeasure: quote `edge_test` and the trade count needed for 80% power.
7. **Failure mode: a one-trade period treated as a period.** The daily bucket's `win_rate` is 100% or 0% by construction. Countermeasure: the `trades_per_period >= 5` gate, and read the gate failure as the finding.
8. **Failure mode: a `pnl` column that omits fees.** Every bucket agrees on a gross edge. Countermeasure: declare the fee treatment and re-run with a cost subtracted.
9. **Failure mode: the log's own selection bias.** The window starts after a good month. Countermeasure: state the window and why it starts there; a shorter honest window beats a longer flattering one.
10. **Failure mode: two populations pooled to reach the trade gate.** Countermeasure: one population per run.
11. **Failure mode: an exit condition is not written down, so the review never fires.** A position sits unexamined because no date and no level were set. Countermeasure: the review date and the level trigger belong to the two lifecycle skills; if either is missing, the position is unmanaged regardless of what the statistics say.
12. **Failure mode: `n/a` treated as a defect and worked around.** Countermeasure: every `n/a` carries a reason in `--json` (`t_stat_note`, `autocorr_note`, `n_eff_note`); quote the reason.
13. **Failure mode: the statistics review displaces the position review.** A trader optimises the bucket instead of writing an exit level. Countermeasure: the cadence rule fixes the bucket once; attention goes to the positions.
14. **Failure mode: the review record is not kept, so a claim cannot be audited.** Countermeasure: archive the full stdout and the `--json` monthly; a claim without an archive is folklore.

**Exit conditions / stopping rules for this skill's own work:**

- **Exit condition:** the verdict, its `n_eff`, the beat-losses result and the drawdown bucket are all written into the review record.
- **Exit condition:** `INSUFFICIENT DATA` is reached and reported as the finding rather than worked around.
- **Stop-loss on the analysis itself:** if a conclusion survives only by choosing a bucket after seeing the numbers, the analysis is abandoned and restarted from the cadence rule.
- **Cut-loss:** if the log cannot be reconciled to the broker's total, no statistic is reported until it can.
- **Exit plan:** archive the run, whether you liked it or not, under `reviews/YYYY-MM-timeframe-stats.txt`.

---

## Best Practices

<!-- QUICK: 30s -->
1. **Fix the review bucket from the holding period before you look at a single P&L figure.** The quarter-to-half rule is in `(references/cadence-versus-holding-period.md)`. A bucket chosen after seeing the statistic is a selection, not a method.
2. **Read coverage before statistics.** `n_periods`, `n_trades` and `trades_per_period` decide whether anything below them means anything.
3. **Quote `n_eff` next to `n_periods`, every time.** They are printed on the same line so that nobody has to remember.
4. **Quote `max_drawdown` from the finest bucket with `trades_per_period >= 5`, and name the bucket.** Coarse buckets do not have less drawdown; they have a different, smaller statistic.
5. **Treat every `n/a` as a result.** One period has no spread; three periods cannot estimate autocorrelation; a bucket with no loser has no break-even win rate. Say which guard fired.
6. **Separate description from inference in writing.** "The win rate was 55.00% against a 48.88% break-even" is a description. "The edge is real" is an inference the 120-trade sample does not support.
7. **Recompute with the largest win and largest loss removed before publishing an edge.** A six-point edge and a −2.4R tail are the same order of magnitude.
8. **Declare the fee treatment in the log's provenance block.** The engine cannot detect it and no bucket choice can compensate for it.
9. **Keep one population per run.** Split by account and instrument class; compare verdicts rather than pooled counts.
10. **Archive every run, including the ones you dislike.** The archive is the only thing that can show a claim strengthening over time; deleting a bad month converts a trail into a highlight reel.
11. **Reconcile `n_trades` to the broker's blotter quarterly.** Unlogged trades and collapsed partial exits are invisible to the engine and are the two most common causes of an edge that exists only in the spreadsheet.
12. **Never annualise.** The engine prints `periods_per_year` as a calendar fact. Multiplying by it changes units, not information.

---

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Verdict says `INSUFFICIENT DATA` and names two different constraints across buckets | The book sits between the two gates: fine buckets lack trades per period, coarse buckets lack periods | Report it. Compute the trade count and history length that would clear both, and say which is closer | A book can be arithmetically incapable of supporting a timeframe claim |
| Every bucket reports the same `win_rate`, `payoff_ratio` and `edge` | Pooling across "the bucket" pools every trade, whatever the bucket | Nothing to fix. It is a proof that the review timeframe cannot move the win-rate test | `edge_test` is a property of the trade set, not of the calendar |
| `cumulative_pnl` is not equal to your broker's realised P&L | Undeclared fee treatment, missing rows, or cashflows included in `pnl` | Reconcile row by row; remove deposits, withdrawals and interest | The reconciliation check precedes every statistic |
| `max_drawdown = 0.00` on a book you know fell | The bucket is too coarse to see the fall | Re-run at the finest bucket with `trades_per_period >= 5` | A bucket cannot measure a path it does not resolve |
| `lag1_autocorrelation = n/a` on a bucket with 2-4 periods | Fewer than 3 periods, zero variance in a lagged sub-series, or `|rho| >= 0.999` | Read `autocorr_note` in `--json` | A guard firing is a finding about sample size |
| `n_eff` larger than the number of trades | `rho < 0`, which inflates `(1−rho)/(1+rho)` past what exists | Read `n_eff_capped`; the raw number is not a sample size | A formula outside its domain produces an impossible answer |
| `t_stat` moves a lot month to month while `n_trades` barely moves | Sample composition changed — a large loss aged out of the window | Track `avg_loss` and the largest single loss alongside `t_stat` | A rising t-stat is not always a strengthening claim |
| `profit_factor = inf` | No losing trades in the bucket | Report `inf` and state that no loss exists to divide by | `inf` is an answer, not a placeholder |
| Engine exits 2 with a line number | A malformed date or amount in the CSV | Fix the row; the engine refuses rather than skipping | Silent row-skipping is how a log becomes fiction |
| `declared : NONE` in the output | The log has no `# PROVENANCE:` line | Tag the log, then re-run | An unlabelled output must not be quoted |
| Per-period `edge` is `n/a` for most periods, but the pooled edge is a number | One-trade periods have no payoff ratio | Read the pooled figures; the per-period count is in `periods_positive_edge` | Per-period and pooled edge answer different questions |

---

## Error Recovery

**If the verdict looks too good:** re-read the "did NOT qualify" list first. A verdict naming a bucket that just crosses the gate is a weak verdict, and the near-miss bucket below it is usually the more informative line. Then check whether the bucket you are looking at is the one the cadence rule asked for.

**If you cannot reconcile the log:** stop. Export again from the broker's blotter with one row per closing fill. An unreconciled log cannot produce a reportable statistic, and the arithmetic will look perfectly healthy while being wrong.

**If the edge flips when you remove one trade:** the headline was never the edge. Report both figures, state that the book's result rests on one observation, and stop quoting the edge until the sample grows.

**If a `PASS` appears on the beat-losses test:** do not upgrade the claim. `PASS` means the win rate is distinguishable from its own break-even *in this sample*. It says nothing about an out-of-sample period, about regimes the sample barely contains, or about whether the person checking the result is independent of the person producing it.

**If you have already published a claim that this engine contradicts:** say so in the next review, with both figures and the dates. The engine's output is archived; the contradiction is checkable. A correction in the record is worth more than a quietly dropped claim.

---

## Cross-Skill Coordination

### Upstream (what this skill needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|----------------|-----------------|------------------------|
| `trade-performance-analyst` | The **definitions** of Sharpe, Sortino, Calmar, maximum drawdown and profit factor; the small-sample guidance (`SE ≈ 1/sqrt(N)`, minimum sample sizes per metric); the monthly-drawdown 1.3–1.5× intra-period adjustment | Every metric definition this skill refuses to redefine, and the one adjustment it cites for coarse-bucket drawdown |
| `trading-decision-data-catalogue` | Which datasets are worth having, which are free, what each costs | Where the trade ledger and any price context should come from — this skill reads only the CSV it is given |
| `equity-tax-lot-and-exit-management` | Realised P&L per lot, and the cost basis behind each close | Reconciling `pnl` to the tax record when the ledger and the 1099 disagree |
| `verification-independence-engineer` | A producer/verifier separation for the review record | Ensuring the person who reports the verdict is not the only person who checks the log |

### Downstream (what this skill produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|------------------|-------------|-------------------------|
| `trade-performance-analyst` | A per-period P&L series with its bucket, `n_eff` and a reconciled trade count — plus a stated fee treatment | Compute Sharpe/Sortino/Calmar on a series whose frequency and lookback are already declared, which is exactly what its R1 gate requires |
| `trade-sizing-recovery` | Pooled `avg_win`, `avg_loss`, `payoff_ratio`, `break_even_win_rate` and `edge`, with the count each rests on | Recalibrate loss bands and R-multiple targets against realised averages rather than intended ones |
| `portfolio-signal-manager` | Period series, per-period drawdown and the dependence disclosure | Size the book against a drawdown that was measured at a resolution that could see it |
| `options-position-lifecycle` / `equity-position-lifecycle` | The chosen review cadence, derived from the average holding period, checked against their cadence tables | Reconcile the performance cadence with the monitoring cadence; a level breach still re-arms the monitoring review immediately |
| `algorithmic-trader` | Which bucket the strategy's own evaluation should use, and the gate its trade count must clear | Set the evaluation window for a systematic strategy before its parameters are fitted to one |

**Coordination rule:** the **cadence** belongs here (derived from the holding period), the **monitoring schedule** belongs to the two lifecycle skills (driven by clocks and levels), the **metric definitions** belong to `trade-performance-analyst`, and the **data** belongs to `trading-decision-data-catalogue`. When a request crosses two of those, answer the part you own and name who owns the rest.

---

## Proactive Triggers

- **Every bucket fails a gate** → say so as the finding, name the nearer constraint, and give the trade count or history length that would clear it. 🔴
- **The chosen review bucket is finer than the gate allows** → flag the conflict between the cadence rule and the trade count before anyone asks, and propose the descriptive-plus-claim split. 🟠
- **`t_stat` or `edge` moves materially while `n_trades` barely moves** → announce that the sample's composition changed, not its size. If one trade carries a large share of `gross_profit` or `gross_loss`, surface it next to the averages. 🟡
- **The yearly or half-yearly bucket reports the largest |t_stat|** → flag the period count before the number is quoted. 🔴
- **`max_drawdown` differs by more than 20% between the finest and the chosen bucket** → report both and name the resolution gap. 🟠
- **`|rho| >= 0.999` or `n_eff` capped** → state that a guard fired and that the raw formula is outside its domain. 🟡
- **A log arrives with no `# PROVENANCE:` line** → refuse to quote any number from the run until it is tagged. 🔴
- **Two instrument classes appear in one log** → propose the split and explain why pooling destroys the pooled payoff ratio. 🟠
- **An `edge_test = PASS` is about to be quoted as proof** → state what it does not cover: out-of-sample, regime coverage, independence of the verifier. 🟠

---

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ "The weekly and monthly views both show the edge, so it's confirmed" | ✅ They are nested summaries of the same trades. Call it one stability check |
| ❌ Choosing the bucket that produces the strongest t-statistic | ✅ Derive the bucket from the holding period, write it down, then run |
| ❌ Quoting the yearly |t| = 2.079 because it clears the noise band | ✅ Quote the gate it failed on `n_periods` = 2 and read it as a lesson about degrees of freedom |
| ❌ Reporting `max_drawdown` from whichever bucket you already had open | ✅ Take it from the finest bucket with `trades_per_period >= 5` and name the bucket in the sentence |
| ❌ Annualising `period_sharpe` because the bucket gives you `periods_per_year` | ✅ Report the observed window and send Sharpe work to `trade-performance-analyst` with frequency and lookback declared |
| ❌ Comparing "my win rate is 55%" to 50% | ✅ Compare it to this book's `break_even_win_rate`, printed by the engine, and to `2 × se_win_rate` |
| ❌ Dropping `n_eff` because the t-statistic reads better without it | ✅ They travel together; the engine prints them on one line for this reason |
| ❌ Pooling accounts or instrument classes to lift `trades_per_period` above 5 | ✅ One population per run, and report the gate failure as the finding |
| ❌ Re-running with a different seed, window or bucket until the number looks publishable | ✅ Archive the run you got. The trail's value is that it contains the bad months |
| ❌ Presenting `examples/` output as a backtest result | ✅ Label everything synthetic. The logs carry `SYNTHETIC / ILLUSTRATIVE` in their own headers and the engine echoes it |
| ❌ Treating every `n/a` as something to be worked around | ✅ Read the reason (`t_stat_note`, `autocorr_note`, `n_eff_note`) and report it |

---

## State Log

| Step | State | Possible Transition | What Could Go Wrong | Record |
|------|-------|-------------------|---------------------|--------|
| 1 | Log exported and tagged | → 2 if reconciled; → STOP if not | Missing rows, undeclared fees, cashflows in `pnl` | Export date, row count, fee treatment, `# PROVENANCE:` block |
| 2 | Holding period computed | → 3 | A bimodal book yields a mean that describes neither mode | Mean, min and max holding period; whether the book should be split |
| 3 | Review bucket fixed from the cadence rule | → 4 | The bucket is quietly changed after seeing the numbers | The bucket, the rule applied, the date it was fixed |
| 4 | All seven buckets run | → 5 | Buckets run one at a time and only the flattering one kept | Full stdout archived |
| 5 | Gates read per bucket | → 6 if any bucket qualifies; → STOP-and-report if none | A failing bucket is worked around instead of reported | `n_periods`, `trades_per_period`, the failing constraint per bucket |
| 6 | Verdict, `n_eff` and noise band read together | → 7 | `n_eff` dropped from the write-up | Verdict line verbatim, including the dependence caveat |
| 7 | Drawdown taken from the finest defensible bucket | → 8 | The coarse figure quoted because it is smaller | Bucket named, both figures, the uplift percentage |
| 8 | Beat-losses test read | → 9 | `PASS` upgraded into "proven" | `win_rate`, `break_even_win_rate`, `edge`, `2 × se`, `edge_test` |
| 9 | Claim written as a description with its bounds, then archived (recording any contradiction with an earlier claim) | → next month | Inference smuggled into a descriptive sentence, or a bad run deleted | The sentence with bucket, count and `n_eff` in it, plus the archive path |

---

## Production Checklist

- [ ] **CR1: Log exported, one row per closed trade** — **Complete when** row count matches the blotter's closed-trade count and the close-date span matches expectation.
- [ ] **CR2: Provenance block written** — **Complete when** source, window, account, fee treatment and partial-exit convention are all named in `# PROVENANCE:` lines.
- [ ] **CR3: `close_date` convention confirmed** — **Complete when** it is the closing fill's trade date, stated explicitly rather than assumed.
- [ ] **CR4: One population per run** — **Complete when** the log contains one account and one instrument class, or the run is split.
- [ ] **CR5: Holding period computed from closed trades** — **Complete when** mean, min and max `close_date − open_date` are written down.
- [ ] **CR6: Review bucket fixed before the P&L is read** — **Complete when** the bucket and the rule that produced it are dated in the record.
- [ ] **CR7: Cadence cross-checked against the lifecycle skills** — **Complete when** the reconciliation with `options-position-lifecycle`'s DTE-zone table or `equity-position-lifecycle`'s time-axis table is written, including which cadence is which.
- [ ] **CR8: All seven buckets run** — **Complete when** the full stdout is archived, not just the named bucket.
- [ ] **CR9: `n_trades` identical across all buckets** — **Complete when** the coverage row has been read in every column.
- [ ] **CR10: `cumulative_pnl` reconciles to total trade P&L** — **Complete when** it agrees for every bucket and with the broker's realised total.
- [ ] **CR11: Verdict and `n_eff` recorded together** — **Complete when** the verdict line, including the dependence caveat, is in the record verbatim.
- [ ] **CR12: Noise-band status recorded per bucket** — **Complete when** every bucket's `NOT DISTINGUISHABLE FROM NOISE` status is captured, not only the winner's.
- [ ] **CR13: Drawdown taken from the finest defensible bucket** — **Complete when** the bucket is named, the coarse figure is shown alongside, and the uplift is a percentage.
- [ ] **CR14: Beat-losses result recorded with its threshold** — **Complete when** `edge`, `2 × se_win_rate` and `edge_test` are all written.
- [ ] **CR15: Outlier sensitivity checked** — **Complete when** the engine has been re-run with the largest win and largest loss removed and both figures are in the record.
- [ ] **CR16: Claim written as a description with declared bounds, then archived** — **Complete when** the sentence names the bucket, the trade count and `n_eff`, claims nothing out of sample, and `reviews/YYYY-MM-timeframe-stats.txt` plus its `--json` companion both exist.

---

## What Good Looks Like

A well-run timeframe review sounds like a lab notebook, not a pitch. It names its bucket, its trade count and its effective sample in the same breath; it quotes the constraint that failed as readily as the verdict that passed; it reports the drawdown from the resolution that could see it; and it refuses to annualise. When the book cannot support a claim, the review says so in one line and moves on to the positions, because the positions are where the money is.

**Signs of Excellence:**

- The bucket was fixed from the holding period *before* the P&L was read, and the record proves it with a date.
- `n_periods` and `n_eff` appear together in every sentence that contains a `t_stat`.
- The `INSUFFICIENT DATA` and `n/a` lines are quoted rather than worked around, and each carries its reason.
- The same run is re-issued with the largest win and largest loss removed; two populations are never pooled, and the archive spans months the desk would rather forget.

**Signs of Dysfunction:**

- The first number mentioned is an annualised Sharpe.
- The bucket changed between two runs of the same log.
- "The weekly, monthly and quarterly views all agree" appears in a decision record.
- The yearly bucket is quoted because it cleared |t| = 2.
- The drawdown figure is smaller in the summary than in any raw export — and nobody asked why — or the runs that produced a `FAIL` are missing from the archive.

---

## Verification Guardrails

### Pre-Generation

- [ ] The log's provenance is declared, or the run is refused until it is.
- [ ] `close_date` is the closing fill's trade date, and the printed span confirms it.
- [ ] The fee treatment of `pnl` is stated, gross or net, explicitly.
- [ ] The review bucket is fixed from the holding period and dated in the record.
- [ ] The population is single: one account, one instrument class.

### Post-Generation

- [ ] `n_trades` is identical across all seven buckets and equals the log's row count.
- [ ] `sum(net_pnl)` equals total trade P&L for every bucket.
- [ ] The verdict's `n_eff` and `n_periods` are both in the write-up.
- [ ] The dependence caveat is present verbatim in the record.
- [ ] `max_drawdown` was taken from the finest bucket with `trades_per_period >= 5`, and the bucket is named.
- [ ] `edge_test` is quoted, and a `PASS` is not upgraded into a proven strategy.
- [ ] The largest win and largest loss have been removed in a sensitivity run, and both figures are recorded.
- [ ] Any synthetic or illustrative log is labelled as such wherever its output appears.
- [ ] The full stdout and the `--json` companion are archived under a dated path.

---

## References

| Reference | Covers | Use When |
|-----------|--------|----------|
| [bucket-definitions.md](references/bucket-definitions.md) | The close-date convention and its cost, all seven bucket definitions, ISO-week and 2W anchoring, key sorting, partial periods, worked assignments | Explaining or arguing with how a trade was assigned to a period |
| [significance-and-sample-size.md](references/significance-and-sample-size.md) | What `t_stat` is and is not, the 12/5 gate and the noise band, the trade count needed for 2σ, 3σ and 80% power, the multiple-comparison problem | Any question of the form "how many trades before I can trust this" |
| [dependence-and-autocorrelation.md](references/dependence-and-autocorrelation.md) | Structural nesting versus serial dependence, the `n_eff` formula and its guards, the illustrative log's `rho` and `n_eff` table, block bootstrap recipe | Reading `lag1_autocorrelation` and `n_eff`, and defending the "not independent tests" caveat |
| [pnl-and-drawdown-by-period.md](references/pnl-and-drawdown-by-period.md) | The two P&L series, the exact drawdown algorithm and its three decisions, drawdown by bucket on the illustrative log, the 1.3–1.5× adjustment attributed to its owner | Any drawdown figure, and any reconciliation of the period series |
| [win-rate-versus-break-even.md](references/win-rate-versus-break-even.md) | The formulas, the break-even table by payoff ratio, why the test is bucketing-invariant, break-even trades, outlier fragility, fees | "Am I beating losses?" and every win-rate claim |
| [cadence-versus-holding-period.md](references/cadence-versus-holding-period.md) | The quarter-to-half rule, the worked options and equity examples, the reconciliation with both lifecycle skills' cadence tables, the full trades-per-period vs periods-per-year trade-off | Choosing or defending the review timeframe |
| [per-instrument-interpretation.md](references/per-instrument-interpretation.md) | Short-premium options, long-premium options, equities, futures and intraday, crypto, and mixed books — expected usable bucket and what usually fails | A book whose instrument class changes what the buckets mean |
| [reading-the-engine-output.md](references/reading-the-engine-output.md) | Field-by-field walkthrough of every output block with live values, and a five-minute reading routine | First run on a new log, or auditing someone else's run |
| [common-misreadings.md](references/common-misreadings.md) | Twelve misread sentences with the correction for each, including the annualisation and yearly-t-stat traps | Reviewing a write-up, or catching your own draft |
| [what-the-engine-cannot-tell-you.md](references/what-the-engine-cannot-tell-you.md) | Sixteen hard limits: no benchmark, no annualisation, no attribution, no intervals, no bias detection, no regimes, no independence of decisions | Before quoting anything, and whenever a claim starts to sound like a performance report |

### Data, sources and thresholds

- `source:` the desk's own closed-trade ledger, exported to the schema in `examples/README.md` — [COMPUTED] every statistic in the engine's output is arithmetic on that one file and nothing else.
- `data from:` `scripts/timeframe_stats.py`, run on `examples/logs/*-synthetic.csv` — [ILLUSTRATIVE] the shipped logs are synthetic, generated at fixed seed 20260414, and carry no market information.
- `verified against:` the broker's realised-P&L total for the same window — the one reconciliation that catches missing rows and undeclared fees [COMPUTED] when it agrees; the run is withheld when it does not.
- `source:` `trade-performance-analyst` — owner of the Sharpe, Sortino, Calmar, drawdown and profit-factor definitions, and of the small-sample guidance this skill defers to. [VERIFIED] as an internal-library citation: the file and its `references/performance-metrics-reference.md`, `references/small-sample-statistics.md` and `references/drawdown-analysis.md` are present in this repository.
- `source:` `options-position-lifecycle` — its cadence reference `references/review-cadence-by-dte-zone.md` is the DTE-zone table this skill's cadence rule is checked against rather than contradicted. [VERIFIED] as an internal-library citation.
- `source:` `equity-position-lifecycle` and its `references/equity-time-axes-cadence.md` — the time-axis cadence table, including the ordinary-state weekly floor. [VERIFIED] as an internal-library citation.
- `published by:` Cboe — its three free index CSVs (`VIX_History.csv`, `VVIX_History.csv`, `SKEW_History.csv`) are the volatility context this skill does **not** load; they are named only because `trading-decision-data-catalogue` cites them as the free index-volatility source. [VERIFIED — Cboe, via that skill's citation].
- `data from:` Yahoo Finance, Bloomberg, or your own broker's blotter for daily closes and marks — levels only, never an intraday fill. [COMMON-PRACTICE] this skill reads no price data at all; the note exists so the boundary is explicit.
- `verified against:` exchange rules for session calendars, because whether a nominal "Friday" was a real trading session decides which day a close date lands on. [VERIFIED] as the class of source; no specific exchange rule is restated here.
- `data from:` `trading-decision-data-catalogue` — the owner of which datasets are worth paying for, which are free, and what each costs.
- [ESTIMATED] The verdict thresholds (`n_periods >= 12`, `trades_per_period >= 5`) and the `|t_stat| < 2` noise band are named operating choices, printed by the engine on every run and stated here so they can be argued with. The 2σ threshold is the conventional two-sided 5% marker under an independence assumption this skill explicitly does not claim to hold; the other two are pragmatic gates derived from when a bucket's per-period statistics become estimable at all. Past performance is not a guarantee and none of these thresholds certify a strategy.
- [ESTIMATED] The monthly-drawdown 1.3–1.5× intra-period adjustment is **not** derived here; it is quoted from `trade-performance-analyst`, which owns it, and applied only when fine-resolution data is unavailable. Meta-layer: `skills/14-finance/options-strategist/references/pattern-recognition-engine.md` names the pattern a position is holding; this skill is consulted after a pattern is named and a book has accumulated closed trades, and it neither names patterns nor requires the meta-layer.

---

## Gotchas

- **A bucket t-statistic and a bucket Sharpe are the same number.** `t_stat = period_sharpe × sqrt(n_periods)`. On the illustrative log, `M` reports `period_sharpe = 0.2629` over 13 periods and `t_stat = 0.948`. Presenting both as two findings doubles the apparent weight of one number. [COMPUTED]
- **The only bucket that clears |t| ≥ 2 is the one with two periods.** Yearly reports 2.079 over `n_periods = 2` while monthly reports 0.948 over 13. The most impressive-looking number in the table is the least stable one, and the gate exists to catch exactly that. [COMPUTED]
- **The yearly bucket reports `max_drawdown = 0.00` while the daily bucket measured a $2,007 drawdown on the same trades.** A bucket that cannot see risk does not report low risk — and the monthly figure understated the daily one by 21.17%, the same defect in milder form. [COMPUTED]
- **`n_eff` can exceed the number of trades.** On the six-trade hand-check fixture the two-week bucket's raw `n_eff` is 545.952 from four periods, because `rho = −0.985453`. The engine caps it at 6.000 and prints why. Quoting the raw figure as an effective sample size is quoting a formula outside its domain. [COMPUTED]
- **Autocorrelation costs the daily bucket a third of its sample.** `D` has 120 periods and 77.894 effective ones — 35% of the apparent sample is clustering. This is not a defect in the data; it is what a risk-off window looks like. [COMPUTED]
- **The beat-losses test cannot be moved by the timeframe.** Every bucket reports `edge = 6.12%` and `edge_test = FAIL`, because the pooled trade set is the same in all seven. If a write-up says one timeframe shows a better edge than another, the write-up is wrong. [COMPUTED]
- **A 6.12-point edge is not proof of anything at 120 trades.** Two standard errors on this win rate are 9.08 points, and reaching a two-sigma result would need about 265 trades — about 519 for 80% power. The engine says `FAIL`; the honest write-up quotes the count, not the edge. [COMPUTED]
- **`profit_factor = inf` is an answer, not a formatting failure.** It means the sample contains no losing trade to divide by, which is a statement about the sample — usually a statement about how short it is. [COMPUTED]
- **Reconciling to a $1,708 net P&L total is the cheapest check in the workflow.** If `sum(net_pnl)` does not equal the broker's realised total, the log is wrong and everything downstream is confidently wrong with it. [COMPUTED]
- **Fees are per trade, so every bucket flatters the strategy by roughly the same amount.** Seven buckets agreeing on a gross edge is not corroboration of a net one. Subtract a plausible round-trip cost and re-run before believing the $14 profit per trade (14.236583 unsimplified), or the $6,143 loss it was earned against. [ESTIMATED]
- **A `PASS` on `edge_test` still covers one sample.** It says the win rate differs from its own break-even here. Out-of-sample persistence, regime coverage and the independence of whoever checks the result are three separate questions, and all three are outside this engine. [COMPUTED]
- **The illustrative log's final year bucket holds one month of trades.** Partial periods are treated as periods, so a year comparison can be a full year against three weeks. Compare period lengths before comparing period values. [ILLUSTRATIVE]

---

## Anti-Hallucination

**These rules bind every response this skill produces.**

- **Admit uncertainty.** If the fee treatment, the `close_date` convention, the capital base or the population boundary is unknown, say so before any number is printed. An engine output on an unknown log is arithmetic on an unknown log.
- **Flag your knowledge cutoff.** This skill's thresholds, examples and figures are frozen as of **2026-10-14** and every number in `SKILL.md` and `references/` is quoted from `examples/run-output.txt` or derived arithmetically from a figure that is. Change the generator's seed and every illustrative number changes; re-run before quoting. Nothing here is a live market statement.
- **Never guess security** identifiers, contract specifications, venue rules, fee schedules, tax treatment or another person's account configuration. If a request needs one of those, name the source that owns it and stop. **Never guess a statistic either** — if the engine has not been run on the log in question, the number does not exist yet.
- **Label provenance.** Every number is tagged: `[COMPUTED]` when it is arithmetic the engine or a stated derivation produced; `[ESTIMATED]` when it is an assumption, with the derivation shown; `[ILLUSTRATIVE]` when it comes from a synthetic log; `[VERIFIED]` when it is checked against a named source — the source is named in the same sentence, and an internal-library citation names the repository file it resolves to.
- **Never present an illustrative log as a result, a backtest or a market finding.** The two logs shipped here are invented, the symbols are invented, the currency is invented, and each file carries no market information whatsoever. The engine echoes their `# PROVENANCE: SYNTHETIC / ILLUSTRATIVE` lines into every output so the label cannot be detached. If a downstream document quotes one of their numbers without that label, the document is wrong regardless of the arithmetic.
- **Never invent a benchmark, a market return, a citation or a comparison.** This engine has no benchmark and no risk-free rate, and it prints neither. A claim about outperformance is outside its scope, and no sentence here or in its output should be read as one.
- **A guard firing is a result, not an error.** Every `n/a` in the engine's output has a stated reason in `--json` (`t_stat_note`, `autocorr_note`, `n_eff_note`) and a documented cause in the references. Report the reason; never substitute a number.
- **If you cannot verify a claim, say which part is unverified.** A statement built from an engine run whose log you cannot reconcile has an unverified foundation even when every step of arithmetic above it is correct, and that fact belongs in the same paragraph.
