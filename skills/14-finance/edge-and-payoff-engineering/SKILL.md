---
name: edge-and-payoff-engineering
description: >
  Use when the question is whether a trading book makes money and what to change if not — "how do
  I make money", "why do I keep losing", "my win rate is high but I'm down", "is my edge real",
  "what payoff do I need", "which setups should I stop trading", "how many trades before I know",
  "what should my risk per trade be". Handles expectancy engineering: the p/b/E algebra in R units,
  break-even payoff b*=(1-p)/p, cohort attribution with a kill list, the multiple-testing guard,
  required sample n_req=4*(sd_R/|E|)^2, the payoff-engineering panel, cost drag in R, and risk per
  trade derived from streak survival. Ships a deterministic stdlib engine. Do NOT use for
  metric definitions (trade-performance-analyst); timeframe bucketing
  (timeframe-performance-statistics); sizing bands (trade-sizing-recovery,
  portfolio-signal-manager, algorithmic-trader); the position router
  (options-position-lifecycle, equity-position-lifecycle); strategy selection
  (options-strategist); data provenance (trading-decision-data-catalogue).
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: active
version: "1.0.0"
updated: 2026-10-14
tags:
  - expectancy
  - payoff-ratio
  - break-even-payoff
  - win-rate
  - r-multiples
  - cohort-attribution
  - kill-list
  - multiple-testing
  - bonferroni
  - required-sample-size
  - kelly-fraction
  - losing-streak
  - risk-per-trade
  - cost-drag
  - disposition-effect
  - trade-journal
  - deterministic-calculator
token_budget: 4500
chain:
  examples:
  - skills/14-finance/edge-and-payoff-engineering/examples/logs
  consumes_from: [timeframe-performance-statistics, trade-performance-analyst]
  feeds_into: [options-trading-playbook, equity-trading-playbook]
---

# Edge and Payoff Engineering

> **Portability target:** spec-level. The algebra is arithmetic and the engine is stdlib-only Python 3 with no network, no vendor, no broker and no market-data dependency of any kind. Every threshold is a named, printed constant.

<!-- QUICK: 30s -->
The whole skill is two equations and one decision:

```
E   = p*b - (1-p)          expectancy per trade, in R units
b*  = (1-p)/p              the payoff you must beat, given your win rate
```

Then: `E_net = E - c_R`, where `c_R = cost_per_trade / R_dollars`. If `b < b*` you are **structurally unprofitable** — you are winning trades and losing money, and no amount of trimming, rolling or hedging changes it. That is the disposition effect expressed as arithmetic.

No amount of position management creates edge. Those manage risk. Expectancy comes from four levers only: **raise `p`, raise `b`, cut cost, trade enough times to know which of the first three you actually have.**

<!-- STANDARD: 3min -->
This skill owns **expectancy engineering**: the p/b/E algebra, the break-even payoff, cohort attribution and the kill list, the required-sample calculation, the payoff rule as the primary control, cost drag in R, and risk per trade derived from streak survival. It owns **nothing** about what Sharpe, Sortino or Calmar mean (`trade-performance-analyst`), nothing about timeframe bucketing (`timeframe-performance-statistics`, which it consumes), nothing about sizing bands (`trade-sizing-recovery`), and nothing about what to do next with an open position (`options-position-lifecycle`, `equity-position-lifecycle`).

Read `references/expectancy-algebra.md` first, then `references/break-even-payoff.md`. Everything else in this skill is a consequence of those two.

---

## Route the Request

<!-- QUICK: 30s -->
| The owner says | This skill answers with |
|---|---|
| "how do I make money" | The four levers, ranked by measured effect on `E_net`, on their own ledger (panel 5) |
| "why do I keep losing" | `b` versus `b*`, and the kill list of cohorts with `n ≥ 30` and `E_net ≤ 0` |
| "my win rate is high but I'm down" | `b < (1-p)/p`. The disposition effect, as arithmetic (panel 4) |
| "is my edge real" | `n_req = 4·(sd_R/|E|)²` versus `n`. Verdict: `POSITIVE EDGE`, `NEGATIVE EDGE`, or `INSUFFICIENT SAMPLE` |
| "what payoff do I need" | `b_needed = (E_target + 1 − p)/p` for `E_target` of +0.2R, +0.3R, +0.5R (panel 4a) |
| "which setups should I stop trading" | The KILL LIST, then the multiple-testing guard on it (panels 2 and 3) |
| "how many trades before I know" | `n_req`, and `years_at_current_pace = n_req / trades_per_year` |
| "what should my risk per trade be" | `R_max = D_tolerance / (L × safety)`, derived, never asserted (panel 1) |

### Auto-Route (no user input needed)

* **A ledger is attached or named** → run the engine, present panel 1 and panel 2 verbatim, then the kill list. Do not summarise the numbers away.
* **No ledger exists** → build the CSV schema first. Say plainly that until there is a `trade_id,open_date,close_date,pnl,risk,cost,setup` file there is no measurable answer, only arithmetic on imagined trades. Offer the hand-check fixture so they can see the shape.
* **The ledger has no `risk` column** → the engine drops to CURRENCY MODE and says so. Tell the user that position size now contaminates the payoff ratio and that the single most valuable thing they can add is the planned risk at entry.
* **The ledger has no `cost` column** → the engine prints the zero-cost warning in capitals. Repeat it. Every figure is gross until cost is supplied.

### Ask or fetch, never assume

Ask for: the account equity (for the dollar translation of `R_max`), the currency the account can lose before the method is abandoned (`D_tolerance`), and whether `pnl` is gross or net of cost. Never assume the account size; `--capital` defaults to 100,000 for arithmetic convenience only and the engine prints the value it used so the assumption is never hidden. `[VERIFIED]` — the engine echoes both `capital` and `D_tolerance` in its `SETTINGS` block on every run, so a run can never be quoted without them.

---

## Anti-Rationalization

<!-- STANDARD: 3min -->
Every one of these sentences is a reason not to do the arithmetic. Each has a mechanical reply.

| You will think | The arithmetic reply |
|---|---|
| "My win rate is good, so I'm fine." | `p` alone decides nothing. Print `b*`. If `b < b*` you lose money winning 7 of 10. |
| "It's a small sample, but the direction is right." | Then the verdict is `INSUFFICIENT SAMPLE`, not `POSITIVE EDGE`. Print `n_req`. |
| "I'll size up on the next run of winners." | The edge is unchanged; only the variance grew. `E` does not contain `n`, and it does not contain your size. |
| "I cut my losers quickly, so my risk is smaller than planned." | Then `risk` on the CSV is fiction and every R in the report is fiction with it. |
| "Commissions are noise." | `c_R = cost_per_trade / R_dollars`. On the shipped illustrative book `c_R = 0.029875R` against a gross `E` of `+0.000941R`. The "noise" is 32 times the signal. |
| "This setup made money last month." | A month is a cohort. Read its `n`, then read the Bonferroni bar. |
| "The strategy stopped working." | Or you had a routine losing streak of length `L`. The engine prints `L` so the two can be told apart. |
| "Half-Kelly is for cowards." | Half-Kelly is the acknowledgement that `p` and `b` are estimated, not known. Full Kelly on an estimated edge is a leverage decision disguised as a sizing formula. |
| "I only need to fix the worst month." | Months are not decisions you can change. Setups are. Kill on `setup` first. |

---

## Ground Rules

<!-- QUICK: 30s -->
These are the rules of the skill. Each has a mechanical trigger — a condition a machine can evaluate — so that the rule is not a matter of mood.

| # | Rule | Mechanical Trigger | Violation Response |
|---|---|---|---|
| GR1 | Every statistic is computed in **R units**, never raw currency | The ledger's `risk` column is absent or has a blank/non-positive value on any row | Engine drops to CURRENCY MODE, prints the reason and the offending line number, and states that position size now contaminates `b` |
| GR2 | Cost is an **input**, never a default of zero | `cost` column absent, or every row's `cost` is 0 | Engine prints `*** COST IS ZERO IN THIS RUN ***` and labels every figure GROSS |
| GR3 | No positive-expectancy claim on fewer trades than `n_req` | `n < n_req = 4·(sd_R/|E|)²` | Verdict forced to `INSUFFICIENT SAMPLE (< n_req trades)` regardless of how good `E` looks |
| GR4 | No cohort is killed or kept on fewer than 30 trades | Cohort `n < 30` | Verdict forced to `INSUFFICIENT (n<30)`, whatever the sign of `E_net` |
| GR5 | Cohort mining carries a multiple-testing correction | Cohort count `m` | Bonferroni bar `z` such that the two-sided tail is `0.05/m`; count clearing the adjusted bar printed next to the count clearing a naive 1.96 |
| GR6 | The payoff ratio is reported with the sample it came from | Always | `b` is printed with `n`, `wins` and `losses` beside it. A `b` driven by one outlier win is visible as `wins = 1` or as an `avg_win` far above the rest |
| GR7 | Risk per trade is **derived**, never asserted | Any request for "what should my risk be" | Answer with `R_max = D_tolerance / (L × safety)`, printing `D_tolerance`, `L` and `safety`. There is no house number |
| GR8 | A losing streak of length `L` is not evidence of a broken edge | Observed streak `<= L × safety` | State that the streak is routine; escalate only past `L × safety` |
| GR9 | The engine's own output is quoted, not paraphrased | Any number in a report | Paste the engine line. If a number appears in prose, it appears in `examples/run-output.txt` too |
| GR10 | Synthetic data is labelled everywhere it appears | Filename, file header, README, or output block | Any figure from a synthetic log carries `SYNTHETIC` / `ILLUSTRATIVE` or is withdrawn |

---

## The Expert's Mindset

<!-- DEEP: 10+min -->
An expert on this subject holds four positions that a beginner finds uncomfortable.

**1. The payoff is a control, not a prediction.** A beginner asks "will this go up?". An expert sets a stop and a target such that `p·b − (1−p) > c_R` **before the trade is opened**, and then lets `p` be whatever it is. This is why `references/payoff-rule-engineering.md` exists: the payoff rule is a mechanical setting applied at entry, whereas `p` is a selection problem with no mechanical answer. On a high-win-rate, low-payoff book, `b` is the binding constraint and the payoff rule is the whole fix.

**2. Most losing traders are not unlucky. They are structurally unprofitable.** `SETUP-CREDIT` in the shipped synthetic ledger wins **61.8%** of its trades and returns `E = −0.0750R` `[VERIFIED]` — the engine's number, not a plausible-sounding one. Its payoff is `0.4956` against a break-even payoff of `0.6176`. The trade that gets closed early because the loss is uncomfortable, and the winner that gets banked early because the profit is pleasant, are the two halves of one arithmetic error. The psychology is the cause; the payoff ratio is the measurement.

**3. `n_req` is the most expensive number in the skill.** On the shipped illustrative ledger the pooled gross expectancy is `+0.000941R` with `sd_R = 1.072301`, so `n_req = 5,199,305.93` trades and `years_at_current_pace = 32,882.67` `[VERIFIED]`. That is what "prove a tiny edge" costs. The honest expert does not try to buy that evidence; they change `p`, `b` or cost until `|E|` is large enough that `n_req` fits inside the trading life they actually have.

**4. The book is not a strategy. It is a portfolio of strategies.** The shipped illustrative ledger pools to `NEGATIVE EDGE` at `E_net = −0.028935R` while containing a cohort at `E_net = +0.2447R` over 62 trades `[VERIFIED]`. A pooled mean over one good and three bad slices describes none of them. Cohort attribution is not an optimisation; it is the minimum bar for knowing what you own.

**5. What the expert refuses to do.** They refuse to annualise a two-month sample, refuse to quote a `Sharpe` (that is `trade-performance-analyst`), refuse to name a risk percentage that "feels right", and refuse to call a `+0.0009R` edge a finding. All three refusals are printed in the engine's own output, so the refusal travels with the number.

---

## Deliberate Practice

<!-- STANDARD: 3min -->
Five drills, each checkable against the shipped fixtures. Do them in order; each one uses the number the previous one produced.

1. **Hand-check the algebra.** Open `examples/logs/hand-check-synthetic.csv`. Its header carries every expected value. Recompute `p`, `b`, `E`, `p*`, `b*`, Kelly, `sd_R`, `n_req` and `L` on paper, then run the engine and compare. Every field of that fixture is checkable in your head because `risk = 100` on every row and the ten R-multiples are `+2 +2 +1 −1 +1 −1 +3 −1 −1 +1`. `[COMPUTED]` — the header's `n_req = 25.19` comes from `4·(1.505545/0.6)² = 25.185176`.

2. **Say why the hand-check verdict is `INSUFFICIENT SAMPLE`.** `E_net = +0.600000R` and the verdict is still insufficient, because `n = 10 < n_req = 25.19`. If that surprises you, the point of the skill has not landed yet.

3. **Pick the binding constraint on the disposition cohort.** `SETUP-CREDIT` in the illustrative ledger runs `p = 0.6182`, `b = 0.4956`. Compute `b* = (1−p)/p = 0.6176` by hand. Then compute what `b` must become for `E = +0.2R`: `(0.2 + 1 − 0.6182)/0.6182 = 0.9412`. `[COMPUTED]` — a paper answer in under a minute, and it is the actual instruction to give the trader.

4. **Rank the four levers on your own ledger.** Run panel 5. Before reading it, predict the order. On a high-`p`, low-`b` book the answer is `(b)` then `(a)`; on a low-`p`, high-`b` book it inverts. The prediction is the drill.

5. **Find a KILL that is really a duplicate.** On the illustrative ledger, `side=short` (`n = 105`, `E_net = −0.1054`) and `iv_rank IVR 25-50` (`n = 54`, `E_net = −0.3071`) are mostly the same losing trades wearing different labels. Practise identifying overlapping cohorts so that the kill list is not counted as independent evidence of five separate problems.

---

## Operating at Different Levels

<!-- STANDARD: 3min -->
| Level | What "edge and payoff engineering" means here | The artifact that proves it |
|---|---|---|
| **L1 — one account, one setup** | Compute `p`, `b`, `b*` on at least 30 closed trades. Stop trading if `b < b*` and you cannot move it | A 30-row ledger with a `risk` and `cost` column, and one printed `b*` |
| **L2 — a few setups** | Cohort attribution by `setup`. Take the kill list. One derived risk-per-trade number instead of a feeling | The engine's panel 2 plus a KILL LIST with the `n` printed beside each row |
| **L3 — a book of many setups** | Multiple-testing guard on every cohort screen. `n_req` and `years_at_current_pace` used to decide *which* setups are worth the evidence they cost | Panel 3 with the adjusted bar, and a written budget of trades per setup |
| **L4 — a desk or a fund** | Expectancy as a monitored production statistic: `E_net` per cohort, per regime, with the streak-survival `R_max` as the sizing input and a review cadence tied to holding period | A monthly expectancy report in which every number carries an `n`, its source, and the date it was measured |
| **L5 — a firm** | Expectancy engineering as a control: no strategy is funded without a `b > b*` demonstration at `n ≥ n_req`, cost is budgeted in R, and cohort screens are pre-registered before the data is cut | A funding gate that cites `b*`, `n_req` and `c_R`, and a pre-registration record |

The level changes the sample sizes and the cadence. It never changes the algebra. `E = p·b − (1−p)` is the same equation for one account and for a five-hundred-person firm.

---

## When to Use

<!-- QUICK: 30s -->
* The owner asks **any** of: "how do I make money", "why do I keep losing", "my win rate is high but I'm down", "is my edge real", "what payoff do I need", "which setups should I stop trading", "how many trades before I know", "what should my risk per trade be".
* A closed-trade ledger exists (or can be exported) and the question is what it says about profitability.
* A trader has a high win rate and a flat or falling equity curve. This is the canonical entry point.
* A decision is about to be made to **size up**, **add a setup**, or **drop a setup**, and nobody has computed `b*` or `n_req`.
* A trade journal needs a payoff rule, a stop/target pair, or a defensible risk-per-trade figure.
* A period of losses needs to be diagnosed as either a routine streak of length `L` or a change in `p` or `b`.

## When NOT to Use

<!-- QUICK: 30s -->
| Not this skill | Go to |
|---|---|
| Defining Sharpe, Sortino, Calmar, maximum drawdown, profit factor | `trade-performance-analyst` |
| Bucketing performance by day/week/month/quarter and testing significance per bucket | `timeframe-performance-statistics` (this skill **consumes** its close-date convention) |
| Choosing a position-size band or a scale-in ladder | `trade-sizing-recovery`, `portfolio-signal-manager`, `algorithmic-trader` |
| Deciding whether to close, roll, or trim an **open** position | `options-position-lifecycle`, `equity-position-lifecycle` |
| Choosing which option strategy matches a market view | `options-strategist` |
| Deciding what market data to buy or how to store it | `trading-decision-data-catalogue` |
| Anything requiring live prices, live Greeks, or a forward-looking return estimate | Nothing here. This engine reads realised P&L only and has no market-data dependency |

---

## Decision Trees

<!-- DEEP: 10+min -->
### DT1 — Is this book structurally profitable?

```
Is b >= b* = (1-p)/p ?
├─ NO  → structurally unprofitable at the current p.
│        Is p > 0.55?
│        ├─ YES → DISPOSITION EFFECT. The binding constraint is b. Raise the
│        │        profit target; do not add filters. Recompute b_needed →
│        │        (E_target + 1 - p)/p                                       panel 4a
│        └─ NO  → the win rate is the constraint too. Kill the worst cohort
│                 first, then re-measure.                                    panel 2
└─ YES → gross E > 0. Is E > c_R ?
         ├─ NO  → COST IS THE BINDING CONSTRAINT. The book pays more to trade
         │        than it earns. Cut contracts, widen strikes, trade less.   panel 5 (c)
         └─ YES → a real gross-and-net edge exists. Is n >= n_req ?
                  ├─ NO  → INSUFFICIENT SAMPLE. Keep trading, keep measuring.
                  │        Do not size up.
                  └─ YES → POSITIVE EDGE. Size from R_max, not from how the
                           last month felt.                                  panel 1
```

### DT2 — Which lever should be pulled first?

```
What does c_R compare to |E| ?
├─ c_R > |E|            → COST first. It is fully under your control,
│                          it is mechanical, and it needs no market
│                          view.                                   → panel 5 (c)
├─ b < b*               → PAYOFF first. Change the target/stop rule,
│                          not the entry filter.                     → panel 4a
├─ p* - p > 0.05        → WIN RATE. This is an entry-filtering problem
│                          and it is the hardest of the three; expect
│                          to spend trades finding it.
└─ all three clear but n < n_req
                        → MORE TRADES (or fewer setups). Cutting the
                           number of setups raises n per setup faster
                           than trading more raises n overall.
```

### DT3 — Kill, keep, or wait?

```
What is the cohort's n ?
├─ n < 30       → INSUFFICIENT. Do not kill, do not keep, do not add.
│                  Either get to 30 or stop measuring it.
└─ n >= 30      → Is E_net <= 0 ?
                  ├─ YES → KILL. Then ask: is this cohort the SAME
                  │         trades as another KILL, seen through a
                  │         different column (side, symbol, iv_rank)?
                  │         ├─ YES → one problem, one fix.
                  │         └─ NO  → a separate problem; kill both.
                  └─ NO  → KEEP, and record n and E_net so next
                           month's number has a baseline.
```

### DT4 — Losing streak: routine or broken?

```
How long is the current losing streak?
├─ <= L x safety        → ROUTINE. L is the EXPECTED longest streak;
│                          a streak of L happens most samples. Keep
│                          sizing at R_max and keep measuring.
└─ >  L x safety        → Suspect a change. Recompute p and b on the
                           last 30 closed trades ONLY.
                           ├─ b still > b* and p within 2 se of the
                           │  prior p   → likely still routine. The
                           │  prior p's standard error is the answer.
                           └─ b <= b* or p below 2 se → the edge has
                              moved. Cut size to R_max, kill the
                              worst cohort, re-derive.      → panel 2
```

---

## Core Workflow

<!-- STANDARD: 3min -->
### Phase 1 — Get the ledger right, before any statistic

1. Export one row per **closed** trade: `trade_id,open_date,close_date,pnl,risk,cost,setup`.
2. `risk` = the **planned** risk at entry, in the same currency as `pnl`. For a defined-risk structure that is the max loss at entry; for a stock with a stop it is `(entry − stop) × shares`. If there is no honest answer for an undefined-risk position, leave it blank — the engine will say it dropped to currency mode rather than averaging two units together.
3. `cost` = commission + exchange/regulatory fees + **half the spread**. A zero cost column is the single most flattering mistake available.
4. `setup` = your own tag, decided **at entry**. This is what makes cohort attribution possible, and cohort attribution is where the money is.
5. Write a `# PROVENANCE:` line naming the source, the account, the window, and whether `pnl` is gross or net. The engine echoes it; an output without it should not be quoted.

### Phase 2 — Run the engine and read panel 1

```bash
py -3 scripts/edge_engine.py --capital 250000 --csv examples/logs/<your-log>.csv
```

Read, in this order: `E_net`, then `b` and `b*`, then `n_req` versus `n`, then `c_R`, then `R_max`. The verdict line is a summary of those five reads and nothing more.

### Phase 3 — Read panel 2 and take the kill list

Cohorts sorted by `E_net`. Kill on `setup` first: `setup` is a decision you can stop making, whereas `symbol` and `month` are labels you did not choose. Watch for overlapping cohorts — the same losing trades appear under several columns, so five KILL rows may be one problem.

### Phase 4 — Read panel 3 and discount the kill list

`m` cohorts were tested. The Bonferroni bar is `0.05/m` two-sided. Read the count that clears the **adjusted** bar, and read the `n` of every cohort that clears it. On the shipped illustrative ledger, the one cohort clearing the adjusted bar is a two-trade month with `t = −61.637` `[VERIFIED]` — a number that is arithmetically correct and evidentially worthless. Bonferroni bounds the number of tests; it does not repair a cohort with two observations.

### Phase 5 — Read panel 4, then change one rule

Panel 4a gives `b_needed = (E_target + 1 − p)/p` for `E` targets of +0.2R, +0.3R and +0.5R. Panel 4b walks `b` up a ladder. Convert the chosen row into **one mechanical rule change**: a target price, a stop distance, a contract count, or an entry filter. One rule, then re-measure.

### Phase 6 — Read panel 5 and rank the levers

`(a)` +5pp on `p` is worth `0.05·(b+1)`; `(b)` +0.25 on `b` is worth `0.25·p`; `(c)` −25% on cost is worth `0.25·c_R`; `(d)` +50% on `n` is worth **exactly zero per trade**. Pull the largest one first. Pulling the smallest one first is how a year gets spent.

### Phase 7 — Derive risk per trade, then act

```
R_max = D_tolerance / (L × safety)          safety default 1.5
R_max_frac = (D_tolerance / capital) / (L × safety)
```

Use the printed `L` (the seeded simulation), not a remembered figure. If your average loss is `kR` rather than `1R`, divide `R_max` by `k`. Then act: change the rule from phase 5, keep size at `R_max`, and re-run the engine at the next review point with the same `--capital` so the numbers stay comparable.

### Completion criteria

* **Complete when** the ledger is in R MODE and the engine's `UNITS MODE` block says so, with `risk` positive on every row.
* **Complete when** `cost` is filled on every row and the capitalised zero-cost warning is absent from the output.
* **Complete when** the engine has printed the pooled panel, the cohort table and the multiple-testing panel from the same run.
* **Complete when** `b` and `b*` are reported together and the disposition-effect banner is either absent or explicitly answered.
* **Complete when** `n` is compared against `n_req`, and the verdict is quoted as printed rather than upgraded by judgement.
* **Complete when** the KILL LIST is written down as decisions, each with its `n`, and the overlapping cohorts have been merged into distinct problems.
* **Complete when** the count of cohorts clearing the **adjusted** Bonferroni bar is reported with the `n` of every clearer.
* **Complete when** `R_max` is derived from `D_tolerance`, `L` and `safety`, and the current position size has been compared against it.
* **Complete when** exactly one mechanical rule has been changed and named, rather than several changed at once.
* **Complete when** a state-log entry exists with `mode`, `capital`, `D_tolerance`, `safety`, `c_R`, `n_req` and the ledger's provenance label.

### The twelve traps — each with its countermeasure

1. **Trap — optimising `p` when `b` is the binding constraint.** On a book with `p > 0.55`, `b` is almost always the binding constraint and it is cheap to change. *Countermeasure:* compute `b*` before touching any entry filter. If `b < b*`, the fix is a target, not a filter.
2. **Trap — measuring `p`, `b`, `E` on fewer trades than `n_req` and calling it proof.** *Countermeasure:* print `n_req` beside `n` on the same line. The verdict is forced to `INSUFFICIENT SAMPLE` when `n < n_req`.
3. **Trap — cohort mining without the multiple-testing correction.** Testing 35 cohorts at a naive 1.96 finds something with probability about 83.4% whether or not an edge exists. *Countermeasure:* panel 3 prints the Bonferroni bar, the count that clears it, and the `n` of every clearer.
4. **Trap — a payoff ratio driven by one outlier win.** *Countermeasure:* `b` is always printed with `wins`, `losses` and `avg_win`. If `wins` is small or `avg_win` is far above the rest of the distribution, the payoff is one trade wearing a statistic.
5. **Trap — averaging over setups so a good cohort hides a fatal one.** The shipped illustrative ledger pools to `E_net = −0.028935R` while holding a cohort at `+0.2447R` `[VERIFIED]`. *Countermeasure:* never report a pooled `E_net` without the cohort table beside it.
6. **Trap — computing `E` on gross P&L while costs eat it.** `c_R = 0.029875R` against a gross `E` of `+0.000941R` on the same ledger `[VERIFIED]`: the cost is 32 times the signal. *Countermeasure:* the engine's zero-cost warning, in capitals, whenever cost is missing or zero.
7. **Trap — Kelly on an unmeasured edge.** `f* = (p·b − (1−p))/b` has `p` and `b` in it, and both are estimates. *Countermeasure:* half-Kelly is printed beside Kelly, and neither is printed without `n` on the same panel.
8. **Trap — sizing from a percentage that feels nice instead of from the streak derivation.** *Countermeasure:* `R_max = D_tolerance / (L × safety)`, with `D_tolerance`, `L` and `safety` all printed. There is no house number, and the engine asserts none.
9. **Trap — scaling up after a winning streak.** The edge is unchanged; only the variance grew. *Countermeasure:* lever `(d)` prints `delta E_net = 0.0000` and the reason, by construction, on every run.
10. **Trap — treating a high win rate as skill when the payoff is below `b*`.** *Countermeasure:* panel 4 prints `b`, `b*` and the disposition-effect banner whenever `b < b*`.
11. **Trap — measuring in currency so position size contaminates the statistic.** In currency, a bigger position makes a trade look better and `b` measures size. *Countermeasure:* R MODE is forced whenever `risk` is present and positive on every row, and the engine says which mode it is in at the top of its output.
12. **Trap — confusing "the strategy stopped working" with "I had a normal losing streak of length `L`".** *Countermeasure:* `L` is printed twice — the closed-form estimate and a seeded simulation — so a streak of that length is pre-labelled routine.

### Regime Table

| Regime | What it does to the four levers | What to do |
|---|---|---|
| **Bull market / uptrend** | `p` rises and `b` usually *falls*, because winners are banked early and targets are hit before they should be. `E` can fall while the equity curve rises | Recompute `b*` at the new `p`. A rising `p` with a collapsing `b` is the disposition trap hiding inside a good month |
| **Correction / pullback** | `p` falls, `b` usually rises (stops are hit at their full width; targets are reached less often). `L` grows with `(1−p)` | Expect the streak. Re-derive `R_max` at the new `p` rather than keeping the old size |
| **Bear market / downturn / drawdown** | `p` falls hard and tail losses widen, so `avg_loss` grows above `1R` and every R in the report shrinks in real terms | Re-measure `avg_loss` in R. If it is above 1R, divide `R_max` by it. Cohort attribution almost always shows one setup carrying all the damage |
| **Crash / tail event / black swan (2008 financial crisis, March 2020, market collapse)** | The sample's `sd_R` is set by events outside the sample. `n_req` computed on the calm period understates the required sample permanently | State that the `n_req` figure excludes this regime. Prefer a cohort-level `b*` check over a pooled one; pooled means are dominated by whichever regime is longest |

Regime coverage is a **sampling** problem, not a modelling one. The engine cannot detect a regime change — it says so in panel 6 — and the only defence is to keep the review cadence short enough that a change is visible in a cohort before it is visible in the account.

### Failure Modes

1. **Failure mode — the `risk` column is aspirational.** Stops were not enforced at entry, so the real loss on some trades exceeded the planned risk. Every R in the report is then understated as a loss and the payoff ratio is optimistic. *Exit condition:* compare `avg_loss` in the report against `1R`; if it is above 1.15R, the stops were not at the stated width.
2. **Failure mode — cost is omitted, and the omission flips the verdict.** `c_R` is added only when a `cost` column exists. On the illustrative ledger the difference between `E = +0.000941R` and `E_net = −0.028935R` `[VERIFIED]` is the entire sign of the book. *Exit condition:* the capitalised zero-cost warning in the engine's output.
3. **Failure mode — a cohort is killed on noise.** A 12-trade month with `E_net = −0.2R` looks decisive and is not. *Exit condition:* the `n >= 30` rule, enforced by the engine, not by discipline.
4. **Failure mode — the kill list is counted as independent evidence.** `side=short`, `iv_rank IVR 25-50` and two `setup` cohorts on the illustrative ledger overlap heavily: the same losing trades under four labels. Killing "five problems" when there is one is a wasted quarter. *Exit condition:* check whether the killed cohorts are disjoint before treating them as separate findings.
5. **Failure mode — a payoff ratio manufactured by one trade.** One `+8R` winner among 40 trades can carry `b` above `b*` by itself. *Exit condition:* re-run with that trade removed and see whether `b` still clears `b*`.
6. **Failure mode — Kelly applied to an estimated edge.** `f*` on a 45-trade sample is a leverage decision with a formula attached. *Exit condition:* half-Kelly printed beside Kelly, and `n` on the same panel.
7. **Failure mode — the required sample is never computed, so a good-looking `E` is traded up.** *Exit condition:* `years_at_current_pace` printed; if it exceeds the trader's horizon, the honest answer is "change `p`, `b` or cost", not "trade more".
8. **Failure mode — sizing set by preference rather than by the streak.** *Exit condition:* `R_max` must be printed with `D_tolerance`, `L` and `safety` and the arithmetic shown.
9. **Failure mode — a losing streak triggers an unplanned strategy change.** *Exit condition:* compare the observed streak against `L × safety` before changing anything; a streak under that bar is routine.
10. **Failure mode — the ledger mixes populations.** Positions, hedges, and an unrelated instrument in one file make every pooled statistic a blend of different processes. *Exit condition:* cohort by `symbol` and check that the `setup` cohorts are populated consistently across symbols.
11. **Failure mode — the trade that was never booked.** A rolled position, an assignment, or a partial exit that is still open is invisible here, and the ledger silently under-counts the losses. *Exit condition:* the closed-trade count versus the broker's own closed-position count for the same window.

---

## Best Practices

<!-- STANDARD: 3min -->
1. **Always convert to R before anything else.** A currency ledger makes `b` a measurement of position size. This is not a stylistic preference; it is the difference between a statistic and an artefact.
2. **Fill `cost` on every row, and fill it honestly.** Half the spread is the part people forget, and it is usually the larger part on a short-dated option.
3. **Tag `setup` at entry, never after the outcome.** A tag applied after the fact is a label for how the trade went, and cohort attribution on it measures nothing. `[COMMON-PRACTICE]`
4. **Report `b` and `b*` on the same line, always.** `b` alone invites the reader to compare it to 1.0, which is the wrong comparison unless `p = 0.5`.
5. **Never report a pooled `E_net` without the cohort table.** A pooled mean over one good slice and three bad ones describes none of them.
6. **Print `n` next to every statistic, including `t`.** On the illustrative ledger the only cohort clearing the Bonferroni bar has `n = 2`. `n` is the first thing to read and the last thing people read.
7. **Kill on `setup` first.** It is the only cohort dimension that corresponds to a decision you are free to stop making.
8. **Change one rule at a time, then re-measure for at least 30 trades.** Two simultaneous changes cannot be attributed, and fewer than 30 trades cannot be decided.
9. **Use half-Kelly, or less, until `n >= n_req`.** Full Kelly on an estimated `p` and `b` is a bet on the estimates, not on the edge.
10. **Derive risk per trade from `L` and `D_tolerance`; never accept a percentage because it sounds modest.** `R_max` on the shipped trimmed book is `0.023493` of capital, or `$2,349.30` on a `$100,000` account `[VERIFIED]` — derived, not asserted.
11. **State the mode, the capital, `D_tolerance` and `safety` in every report.** The engine prints them in a `SETTINGS` block precisely so that a quoted number cannot be separated from the assumptions behind it.
12. **Keep a pre-registration of the cohorts you will screen, and the rule for killing them, before you look.** A screen designed after seeing the data is a screen fitted to the data.
13. **Watch `avg_loss` in R.** If it drifts above `1R`, the stops have moved and every R figure in the report needs rescaling before it is used for sizing.
14. **Write the exit condition for every rule change before you make it.** A target change, a kill, or a new filter needs a stated exit condition — the observation that would make you reverse it — or it becomes permanent by default.

---

## Error Decoder

<!-- STANDARD: 3min -->
| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| `CURRENCY MODE` in the output | No `risk` column, or a blank/non-positive value on some row | Add the planned risk at entry to every row and re-run | Mixing two units inside one mean is worse than either unit alone, so the engine refuses rather than guessing |
| `*** COST IS ZERO IN THIS RUN ***` | No `cost` column, or every row's cost is 0 | Add commission + fees + half-spread per trade | A gross expectancy is a flattering expectancy; the sign of the verdict can rest on this one column |
| `payoff ratio b … inf` | No losing trades in the sample | Read `E` and `sd_R` and nothing else; `b` is undefined, not excellent | An infinite payoff ratio is a statement about the sample, not about the strategy |
| `n_req (2-sigma) … 5199305.93` | `E` is very close to zero relative to `sd_R` | Stop trying to prove the edge. Change `p`, `b` or cost and re-measure | A near-zero expectancy cannot be separated from zero inside a human trading life |
| Verdict `NEGATIVE EDGE` with `p = 0.62` | `b < b*` — the disposition trap | Raise the profit target until `b` clears `b*`; do not add entry filters | A good win rate with a bad payoff is a maths error, not luck |
| Every cohort `INSUFFICIENT (n<30)` | The cohort dimension has too many values, or the ledger is too small | Reduce to 3-5 `setup` tags, or keep accumulating | Twelve setups on 80 trades are 6-trade cohorts and 6-trade cohorts are noise |
| `cohorts clearing ADJUSTED bar : 1 of 35` with a tiny `n` | Bonferroni bounds the number of tests, not the size of a cohort | Read the `n` printed beside every clearer | A two-trade cohort with `t = −61.637` is arithmetically correct and evidentially worthless |
| `R_max … n/a` | `L` is 0 (no losing trades possible) or `capital` is not positive | Supply `--capital`; on an all-wins sample wait for losses before sizing | Survival risk needs a streak to survive; with `p = 1` there is nothing to derive from |
| `years_at_current_pace 32882.67` | `n_req` is enormous because `|E|` is tiny | Treat as a rejection of the strategy, not a plan | The number is the answer, not an inconvenience |
| `ERROR: line N: cannot parse amount` | A currency string the parser does not accept | Use `1234.5`, `1,234.50`, `$1,234.50`, or `(1,234.50)` | The engine fails loudly with a line number instead of silently skipping a row |

## Error Recovery

<!-- STANDARD: 3min -->
| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| The engine refuses the file | Header lacks `close_date` or `pnl` | Fix the header; both are required | A refusal with a line number is cheaper than a wrong answer |
| Verdict flips between runs | The input changed, or a different `--capital`/`--dd-tolerance` was used | Re-run with the settings recorded in the `SETTINGS` block | The run is deterministic given (ledger, capital, tolerance, safety). A flip means one of those moved |
| `E` and `E (closed form x avg_loss)` disagree | `avg_loss` is not `1R` | Read the reconciliation row; the difference is the average loss | The two forms are the same number; the gap measures how far the book is from losing what it planned |
| The kill list kills everything | `cost` is large relative to `E`, or the whole book is negative | Fix cost or `b` at the book level first; cohort-level kills cannot rescue a negative book | Killing slices cannot create edge; it can only stop the bleeding from a slice that has none |
| No cohort clears the adjusted bar, but one KEEP cohort looks good | `n < n_req` for that cohort | Do not act on it. Accumulate, or reduce the number of setups | "Not yet distinguishable" is the correct reading of a positive `E_net` on a small `n` |
| `streak note` says `p = 1` or `p = 0` | A degenerate sample | Nothing to derive; collect more trades | The engine reports degenerate cases instead of inventing a number for them |

---

## Cross-Skill Coordination

<!-- QUICK: 30s -->
### Upstream (what this skill needs)

| Upstream Skill | What it supplies | Interface |
|---|---|---|
| `timeframe-performance-statistics` | The **close-date bucketing convention** — a trade belongs to the bucket containing its close date — and the significance-by-bucket apparatus | This skill consumes the convention and does not re-derive it; bucket-level significance stays there. The engine repeats the convention in its own docstring and output so the two can never silently diverge |
| `trade-performance-analyst` | The **definitions** of Sharpe, Sortino, Calmar, maximum drawdown and profit factor | This skill does not define or compute any of them. It computes `E`, `b`, `b*`, `n_req`, `L` and `c_R`, and nothing else. There is no annualised return anywhere in its output |

### Downstream (what this skill produces)

**Downstream consumers** — declared as `feeds_into: [options-trading-playbook, equity-trading-playbook]` in the front-matter: this skill's output is a *measurement and a verdict*, and those two playbooks consume it when validating a proposed rule set. The other natural readers are:

| Downstream Skill | What it takes from here | Note |
|---|---|---|
| `trade-sizing-recovery` | The derived `R_max` as the **ceiling** for any sizing band or ladder it prescribes | This skill derives one number; that skill owns the bands, the ladders and the recovery schedule |
| `portfolio-signal-manager` | Per-cohort `E_net` and the kill list, as a weighting input | This skill says which slices are negative; that skill decides what the portfolio does about it |
| `algorithmic-trader` | `b*`, `b_needed` and `n_req` as testable acceptance criteria for a strategy before it is automated | An automated strategy with `b < b*` automates a loss at higher speed |
| `options-position-lifecycle`, `equity-position-lifecycle` | The kill list and `b*` as context for decide-what-to-do-next on an open position | Those skills own the router; this one owns only what the closed ledger says |
| `options-strategist` | The payoff structure a book actually needs, expressed as a required `b` | Strategy selection stays there; the *required payoff* comes from here |
| `trading-decision-data-catalogue` | The exact CSV schema this engine consumes | That skill owns provenance and storage; this one owns the schema it needs |

---

## Proactive Triggers

<!-- STANDARD: 3min -->
Surface this skill, unprompted, when any of these is observed:

* The equity curve is **flat or falling** while the reported win rate is **above 55%**. That combination has one arithmetic cause and it is `b < b*`.
* A trader says **"I just need to be more selective"** while `b` is below `b*`. Selectivity raises `p`; the binding constraint is `b`.
* A trader wants to **increase size** without a printed `n_req`. Size cannot fix a sample problem, and it amplifies a negative edge.
* A **new setup is added** to a book that already has more than five `setup` tags. Cohort sizes fall and every verdict becomes `INSUFFICIENT`.
* **Cost is described as negligible** for any strategy whose gross `E` is under about `0.05R`. On the shipped ledger `c_R = 0.029875R` was 32 times the gross expectancy.
* A **losing streak** is being used as evidence that a strategy broke. Check it against `L × safety` first.
* A **"best setup"** is being promoted on fewer than 30 trades.
* **Profit factor, Sharpe or Calmar** is quoted as the sole evidence of edge. Those are `trade-performance-analyst` metrics; they do not contain `b*` and cannot decide structural profitability.

---

## Anti-Patterns

<!-- STANDARD: 3min -->
* ❌ **"My win rate is 65%, so I'm profitable."** `p` without `b*` decides nothing. `SETUP-CREDIT` wins 61.8% and loses `0.0750R` per trade `[VERIFIED]`. → ✅ Print `b` beside `b*` on every report.
* ❌ **"The sample is small but the direction is clear."** Direction is not a statistic, and `n_req` is the sample the dispersion demands. On the hand-check fixture a `+0.60R` expectancy on 10 trades is still `INSUFFICIENT SAMPLE` because `n_req = 25.19`. → ✅ Print `n_req` beside `n`.
* ❌ **"I'll size up on this run of winners."** The edge is unchanged; only the variance grew. Lever `(d)` prints `delta E_net = 0.0000` for exactly this reason. → ✅ Size from `R_max` and the streak derivation, never from recent results.
* ❌ **"Commissions don't matter at my size."** The illustrative ledger's `c_R` is `0.029875R` against a gross `E` of `+0.000941R`: the cost is 32 times the signal. → ✅ Fill `cost` on every row, half-spread included.
* ❌ **"This setup is my best; it made 4R last month."** A month is a cohort with an `n` of a dozen. → ✅ Read the cohort's `n`, then read the Bonferroni bar.
* ❌ **"The strategy stopped working."** The engine prints `L` twice, precisely so that a streak of that length is pre-labelled routine. → ✅ Compare the streak against `L × safety` before changing anything.
* ❌ **"Full Kelly is optimal."** Full Kelly is optimal for *known* `p` and `b`. Both are estimates on any real ledger. → ✅ Report half-Kelly beside Kelly, and neither without `n`.
* ❌ **"Risk 2% because that's standard."** A percentage that feels modest is not derived from anything about this book. → ✅ `R_max = D_tolerance / (L × safety)`.

---

## State Log

<!-- STANDARD: 3min -->
Keep this block in the ledger's own directory, one row per engine run. It is the only thing that makes this month's `E_net` comparable to last month's.

```
date            : 2026-10-14
ledger          : examples/logs/illustrative-cohorts-synthetic.csv   SYNTHETIC
rows            : 200     mode: R     c_R: 0.029875
capital         : 100,000.00     D_tolerance: 20,000.00     safety: 1.50
p / b / b*      : 0.510000 / 0.962557 / 0.960784
E / E_net       : 0.000941 / -0.028935
n_req / pace    : 5,199,305.93 trades  /  32,882.67 years_at_current_pace
L               : formula 7.427 / simulated 6.810
R_max           : 0.019580 of capital = $1,958.03
verdict         : NEGATIVE EDGE
cohorts / bar   : 35 tested, adjusted z 3.1888, 1 clearing (n=2), KILL LIST 10
rule changed    : (none this run)
next review     : after 30 further closed trades
```

Fields that must never be omitted: `mode`, `capital`, `D_tolerance`, `safety`, `c_R`, `n_req`, and the ledger's provenance label. A state log without `mode` cannot be compared across runs, and a state log without the provenance label can be a synthetic fixture wearing a real account's name.

---

## Production Checklist

<!-- DEEP: 10+min -->
* **CR1** — The ledger has one row per closed trade, with `close_date` and `pnl` on every row.
* **CR2** — `risk` is present and positive on **every** row, so the run is in R MODE. The engine's `UNITS MODE` block says `R MODE`.
* **CR3** — `cost` is filled on every row and is not all-zero. The zero-cost warning is **absent** from the output.
* **CR4** — `setup` is filled and has 3-5 distinct values, each with at least 30 rows.
* **CR5** — A `# PROVENANCE:` line names the source, the account, the window, and whether `pnl` is gross or net.
* **CR6** — `--capital` is the real account equity, and `--dd-tolerance` is the real currency loss the method is allowed to take before it is abandoned.
* **CR7** — `E_net` is printed and is the number quoted, not `E`. If they differ, `c_R` is shown beside them.
* **CR8** — `b*` is printed beside `b`, and the disposition-effect banner is either absent or explicitly addressed.
* **CR9** — `n` is printed beside `n_req`, and the verdict is read from the comparison, not from the sign of `E`.
* **CR10** — The cohort table is printed with the pooled panel. No pooled number is reported alone.
* **CR11** — The multiple-testing panel is present, with `m`, the adjusted bar `z`, and the count clearing it **with the `n` of each clearer**.
* **CR12** — The KILL LIST is written down as a list of decisions, with each cohort's `n` beside it, and each killed cohort is checked for overlap with the others.
* **CR13** — `R_max` is printed with `D_tolerance`, `L` and `safety`, and the current position size is compared against it. `[COMPUTED]` — on the hand-check fixture `R_max = 20,000/(2.17825 × 1.5) = 0.061211`, or `$6,121.12` on `$100,000`.
* **CR14** — `L` is recorded so that the next losing streak can be judged against it.
* **CR15** — The state log block is written, with `mode`, `capital`, `D_tolerance` and `safety`.
* **CR16** — Exactly one rule was changed since the previous run, and it is named in the state log.

---

## What Good Looks Like

<!-- STANDARD: 3min -->
A good expectancy report is short, and every line of it carries its own sample size and its own assumption.

```
MODE             R (risk positive on 200/200 rows)
COST             c_R = 0.029875R, cost filled on 200/200 rows
POOLED           n=200  p=0.510000  b=0.962557  b*=0.960784  E_net=-0.028935
SAMPLE           n_req=5,199,305.93  years_at_current_pace=32,882.67
STREAK           L=6.810 (simulated), 7.427 (closed form)
RISK             R_max=0.019580 of capital = $1,958.03 on $100,000
VERDICT          NEGATIVE EDGE
COHORTS          35 tested, adjusted bar z=3.1888, 1 clearing (n=2)
KILL             SETUP-FADE n=60 E_net=-0.2527 | SETUP-CREDIT n=55 E_net=-0.1048
KEEP             SETUP-TREND n=62 E_net=+0.2447
ONE RULE CHANGED raise the credit target from 0.5R to 1.0R; hold everything else
```

`[VERIFIED]` — every figure in that block is pasted from the engine's actual stdout on the shipped illustrative ledger, and appears verbatim in `examples/run-output.txt`.

What makes it good:

* **A verdict, not a vibe.** `NEGATIVE EDGE` is a verdict the reader can disagree with.
* **`b` and `b*` on the same line.** The reader can see structural profitability without doing arithmetic.
* **A sample the verdict can withstand.** `n_req` and `years_at_current_pace` are printed even though they make the book look worse.
* **A kill list with `n` beside every row.** Decisions, each with the evidence behind it.
* **One rule changed, named.** Nothing else is claimed to have changed.
* **The assumptions on the top three lines.** Mode, cost, and the settings block. A quoted number cannot be detached from them.

---

## Verification Guardrails

<!-- DEEP: 10+min -->
### Pre-Generation

* Before running the engine, confirm the ledger's provenance label. A synthetic fixture and a real account must never be mixed in one directory (`trading-decision-data-catalogue` owns storage; this is the operational check).
* Confirm `risk` is positive on every row. `[VERIFIED]` — the engine prints the first offending line number when it is not.
* Confirm `cost` is filled. If it is not, treat every number as gross and say so before quoting anything.
* Confirm the currency and the capital. `R_max` in dollars is meaningless without the account it belongs to.

### Post-Generation

* Every number in the report appears in the engine's stdout. If a number is not in the output, it does not go in the report.
* `E_net` is quoted, not `E`, whenever they differ.
* No Sharpe, Sortino, Calmar or annualised return appears anywhere (`trade-performance-analyst` owns those).
* No risk percentage appears without the `R_max` derivation beside it.
* No cohort verdict appears without its `n`.
* No positive-expectancy claim appears on a sample below `n_req`.
* The synthetic/illustrative label survives into the report if the ledger is synthetic.

### The four anti-hallucination guardrails

* **Admit uncertainty** — say plainly that `p` and `b` are estimates from a sample, that `n_req` is a 2-sigma approximation rather than a proof threshold, and that `L` is an expectation and not a forecast. The engine's own panel 6 does this; repeat it rather than softening it.
* **Flag your knowledge cutoff** — this skill's content is arithmetic and does not expire, but every market-structural claim it makes (margin rules, contract specifications, settlement conventions, fee schedules) is subject to change. Say when a structural fact was last checked and direct the reader to the current rule text rather than to a remembered number.
* **Never guess security** — this skill consumes no market data, no prices and no security identifiers. It never needs to identify an instrument, and it must never invent one. If a request needs live prices, Greeks, or a forward-looking return estimate, say that this engine cannot supply them and route to the skill that can.
* **`[VERIFIED]`** means the figure was pasted from the engine's actual stdout on the named ledger, or read from the named file in this skill — nothing else qualifies. A number recalled from a conversation, a plausible-looking round figure, or a value from another book is `[ESTIMATED]` or `[ILLUSTRATIVE]`, and the difference matters most exactly when the number is being used to change a position size.

### The honesty statement this skill will not soften

The shipped fixtures are **SYNTHETIC**. The illustrative ledger's pooled verdict is `NEGATIVE EDGE`, and that is not a claim about any strategy — it is a claim about four invented cohorts. No number in this skill demonstrates that anything is profitable. It is not a backtest, it carries no market information, and it must never be quoted as a finding about any instrument, market or period. The engine is real, its arithmetic is checkable by hand, and the data it was demonstrated on was invented on purpose so that the demonstration could never be mistaken for a result.

Any figure in this document that is not pasted from the engine's own stdout is **unverified** by this skill's own standard. Structural claims about margin rules, contract specifications, settlement conventions and fee schedules are pointers to look up, not facts to rely on: they were written on 2026-10-14 and were not checked against a live rulebook from this environment.

---

## References

* [expectancy-algebra.md](references/expectancy-algebra.md) — `E = p·b − (1−p)` from first principles, in R units, with the derivation of every other field in the pooled panel.
* [break-even-payoff.md](references/break-even-payoff.md) — `b* = (1−p)/p`, why it decides structural profitability, and why `b` is compared to `b*` rather than to 1.0.
* [cohort-attribution-and-the-kill-list.md](references/cohort-attribution-and-the-kill-list.md) — how to build cohorts that correspond to decisions, and the KEEP / KILL / INSUFFICIENT rules.
* [multiple-testing-in-cohort-mining.md](references/multiple-testing-in-cohort-mining.md) — why a single significant slice out of 20 is expected by chance, Bonferroni in one page, and what Bonferroni cannot fix.
* [how-many-trades-to-know.md](references/how-many-trades-to-know.md) — `n_req = 4·(sd_R/|E|)²`, `years_at_current_pace`, and the honest use of both.
* [payoff-rule-engineering.md](references/payoff-rule-engineering.md) — the payoff rule as the primary control: stops and targets, not predictions.
* [cost-drag-in-r-units.md](references/cost-drag-in-r-units.md) — `c_R = cost_per_trade / R_dollars`, what belongs in `cost`, and why the zero-cost default is flattering.
* [streak-survival-and-risk-per-trade.md](references/streak-survival-and-risk-per-trade.md) — `L` and `R_max = D_tolerance / (L × safety)`, derived rather than asserted.
* [disposition-effect-as-a-math-error.md](references/disposition-effect-as-a-math-error.md) — `b < (1−p)/p` as the arithmetic face of selling winners and holding losers.
* [from-negative-to-positive-walkthrough.md](references/from-negative-to-positive-walkthrough.md) — the five-step walkthrough that takes the shipped negative cohort to a positive book, with the engine's real numbers.
* [what-the-engine-cannot-tell-you.md](references/what-the-engine-cannot-tell-you.md) — the refusals, in full, and what to do instead.

### Data, sources and thresholds

* **Source of every statistic in this skill:** the reader's own broker trade blotter, exported as the CSV in `examples/README.md`. This engine consumes no price series and pulls nothing from any market-data vendor — not Yahoo Finance, not Bloomberg, not an exchange feed, not a CBOE data product.
* **Source of contract and market structure facts:** exchange rules and the issuer's own contract specifications (the CBOE publishes per-product specifications; the OCC publishes clearing and exercise conventions). Where this skill mentions a structural convention, it is a pointer to look up the current text, not a remembered number. `[COMMON-PRACTICE]`
* **Source of margin and fee facts:** the broker's published commission and fee schedule, and the current text of the applicable margin rule. Margin rules are published by the self-regulatory organisations and by the Federal Reserve's Regulation T; a fee schedule is published by the broker.
* **Source of the thresholds:** the `safety = 1.5` streak multiple, the `n >= 30` cohort floor and the `0.05` family-wise alpha are **named constants in `scripts/edge_engine.py`**, printed in the engine's `SETTINGS` block on every run. They are disclosed rules, not hidden ones — a reader who disagrees should change them there and say so. `[COMMON-PRACTICE]`
* **Source of every figure quoted as `[VERIFIED]`:** the engine's actual stdout, captured in `examples/run-output.txt`. Reproduce with the commands shown in that file. `[VERIFIED]`

---

## Gotchas

* **A payoff ratio is meaningless without `p`.** `b = 1.5` is excellent at `p = 0.45` and irrelevant at `p = 0.75`. Always print the pair. `[COMPUTED]` — at `p = 0.45`, `b* = 1.2222`; at `p = 0.75`, `b* = 0.3333`.
* **`E` and `p·b − (1−p)` are the same number multiplied by the average loss.** The engine prints both plus the reconciliation row, so a mismatch is never mistaken for an error. When they differ, the difference *is* `avg_loss`.
* **The disposition trap looks like skill.** A high win rate with a poor payoff produces a smooth equity curve that grinds down. `SETUP-CREDIT` wins `61.8%` and returns `E = −0.0750R`. `[VERIFIED]`
* **Cost is the trap that flips the sign.** `E = +0.000941R` and `E_net = −0.028935R` on the same 200 trades. The gap is `c_R = 0.029875R`. `[VERIFIED]`
* **`n_req` can be absurd, and the absurdity is the finding.** `5,199,305.93` trades and `32,882.67` years for the illustrative book. `[VERIFIED]` The answer is "change `p`, `b` or cost", never "trade more".
* **A cohort that clears the Bonferroni bar can still be worthless.** A two-trade month on the shipped ledger produces `t = −61.637`. `[VERIFIED]` Read `n` before `t`.
* **Overlapping cohorts inflate the kill list.** The illustrative ledger's kill list has 10 rows; `side=short` alone contains 58% of `SETUP-FADE` and 73% of `SETUP-CREDIT` `[COMPUTED]`, so several rows are one problem under different labels. Count distinct problems, not rows.
* **`R_max` is a ceiling, not a target.** It is the largest risk a routine streak of length `L` can survive. Risking less is always permitted; risking more is a different strategy with a different `D_tolerance`.
* **`avg_loss` above `1R` rescales everything.** If the book's average loss is `1.15R`, every `R_max` in the report needs dividing by about `1.15` before it is used. `[ESTIMATED]` — the scaling is exact for the streak arithmetic; the 1.15 is the illustrative figure.
* **A currency ledger cannot be compared to an R ledger.** Different units, different `b`, different `n_req`. The engine prints the mode at the top of every run so a mixed comparison is visible.
* **`L` is an expectation, not a worst case.** It is the *expected longest* streak in `N` trades. Roughly half of all samples contain a longer one. `[ESTIMATED]` — the simulation on the shipped books lands at `6.810` against a closed form of `7.427` on `N = 200`, which is the right order of magnitude for the approximation.
* **A ledger of closed trades cannot see an open position.** A roll that has not closed, an assignment, or a partial exit still open is invisible, and the report will understate the damage.

---

## Anti-Hallucination

<!-- DEEP: 10+min -->
This skill is arithmetic, and arithmetic is exactly where a confident wrong number is most damaging — it arrives looking like a fact and it changes a position size.

**Admit uncertainty.** `p` and `b` are sample estimates. Every derived field — `b*`, `E`, `n_req`, `R_max`, Kelly — inherits their sampling error, and none of them is printed with a confidence interval because intervals on `b*` are the reader's job with the reader's sample. The engine prints `n` beside every one of them so the error is never hidden; it does not pretend to have bounded it.

**Flag your knowledge cutoff.** The mathematics here does not expire: `E = p·b − (1−p)` will be true indefinitely. The **market-structural** details around it do expire — margin rules, contract specifications, settlement conventions, fee schedules, tax treatment of a closed option position. Where this skill touches one, treat it as a pointer to look up, not as a fact to rely on. This document was written on 2026-10-14 and its structural claims were not checked against a live rulebook from this environment; they are labelled `[COMMON-PRACTICE]` where they appear and they should be re-checked before any of them is used to justify a trade.

**Never guess security.** This engine consumes no market data and never needs to identify an instrument. It must never invent a ticker, a price, a contract specification, a spread width, or a margin requirement in order to make an example work. If a request needs live prices, live Greeks, or a forward-looking return estimate, say plainly that this skill cannot supply them and route to the skill that can.

**What `[VERIFIED]` means here, and what it does not.**

* `[VERIFIED]` — pasted from `scripts/edge_engine.py`'s actual stdout on the named ledger, and reproducible by running the command shown in `examples/run-output.txt`. Nothing else qualifies.
* `[COMPUTED]` — arithmetic worked out in this document and shown, so the reader can redo it.
* `[ESTIMATED]` — a number with a stated derivation whose inputs are themselves estimates.
* `[ILLUSTRATIVE]` — a synthetic fixture, or a round number chosen to make an example legible. **Not a market observation.**
* `[COMMON-PRACTICE]` — a widely used convention stated as a convention, not as a measured fact.

**What this skill will not claim.**

* It will not claim that any strategy, setup, or cohort is profitable. The shipped fixtures are synthetic and the illustrative ledger's pooled verdict is `NEGATIVE EDGE`.
* It will not claim a benchmark return, a typical win rate, a typical payoff ratio, or a typical cost for any strategy. No such figures appear anywhere in this skill, because none of them was measured here.
* It will not claim that `n_req` is a proof threshold. It is a 2-sigma separation heuristic, stated as such, and a reader who wants a real power calculation should compute one.
* It will not claim a citation it cannot support. The only sources named here are the reader's own broker blotter, published exchange and clearing-house documents, published broker fee schedules and the applicable margin rule text — each named as a place to look, never as a number remembered from training data.
* It will not claim that the demo proves the method. The demo proves the engine runs and that its arithmetic is checkable on paper. That is all it proves.
