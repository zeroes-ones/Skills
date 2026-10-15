---
name: options-trading-playbook
description: >
  Use when the owner asks how do I make money with options, why do I keep losing
  on credit spreads, is selling premium worth it, what win rate do I need, should
  I buy or sell options, which options strategy is profitable, or my options book
  is flat. Handles the payoff-corner map, why the popular rules break even
  (50%-of-credit/2x-credit needs 80%), stop/target arithmetic, regime matching,
  cost drag per leg and rung, small-account choice, streak survival, and the
  iteration protocol. Ships a deterministic stdlib-only payoff checker printing b,
  p* and n_req. Do NOT use for structure selection once the profile is set
  (options-strategist, advanced-options-structures), open-position exits (options-position-lifecycle), leg surgery
  (options-leg-management), size bands (trade-sizing-recovery), book Greeks or
  margin (options-risk-engineer), or expectancy measurement
  (edge-and-payoff-engineering).
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: active
version: "1.0.0"
updated: 2026-10-14
tags:
  - options-strategy
  - payoff-corner
  - expectancy
  - break-even-win-rate
  - premium-selling
  - credit-spreads
  - long-premium
  - stop-and-target
  - regime-matching
  - cost-drag
  - per-leg-cost
  - multi-rung-scaling
  - streak-survival
  - iteration-protocol
  - overfitting
  - determinism
  - strategy-cards
  - small-account
  - kelly
token_budget: 4500
chain:
  examples:
  - skills/14-finance/options-trading-playbook/examples/checks
  consumes_from: [options-strategist, trade-sizing-recovery, edge-and-payoff-engineering]
  feeds_into: [options-position-lifecycle]
---

# Options Trading Playbook

> **Portability target:** Spec-level. The payoff arithmetic is closed-form algebra and the checker is stdlib-only Python 3 with no network, no vendor, no broker and no third-party dependency. Every threshold is a named, printed constant, and every output carries its own formula.

<!-- QUICK: 30s -->
The whole skill is one question: **which payoff corner should this book be trading, and does the arithmetic say it pays?**

Run `scripts/payoff_check.py` on the card before capital is risked. Read `b`, `E_net`, `p*` and the verdict. If the verdict is not `POSITIVE`, do not trade the card — no amount of conviction changes `p* = 1/(1+b)`.

This skill owns **the strategy layer**: which payoff profile to trade, in which regime, with which rules, and how to iterate toward positive expectancy without curve-fitting. It owns nothing about *structure mechanics* once the profile is chosen — that is `options-strategist` — and nothing about *what to do with an open position* — that is `options-position-lifecycle`.

<!-- STANDARD: 3min -->
The honest headline, and it is uncomfortable: **the most popular credit-spread management card in retail options requires an 80% win rate just to break even.** Take profit at 50% of the credit, stop at 2× the credit, and `b = 0.5C/2C = 0.25`, so `p* = 1/1.25 = 80.00%`. At exactly `p = 0.80`, `E = 0.80 × 0.25 − 0.20 = 0.0000R`. **Identically break-even, not approximately.** That single line explains why premium-selling books so often come out flat, and it is derived — not asserted — in `references/break-even-payoff-for-credit-structures.md`.

Everything below is arithmetic on that identity. The skill does **not** claim any strategy is profitable, and no output of it should ever be read as such. See `references/what-this-cannot-promise.md` before acting on any number here.

---

## Route the Request

### Auto-Route (no user input needed)

| The request sounds like | Where it goes |
|---|---|
| "How do I make money with options?" | `references/payoff-corners-for-options.md`, then Core Workflow Phase 1 |
| "Why do I keep losing on credit spreads?" | The `b = 0.25` → `p* = 0.80` derivation, then Phase 2 |
| "Is selling premium worth it?" | Both sides of `p` and `b`; run the checker on the card as written |
| "What win rate do I need?" | `p* = 1/(1+b)` — read `b` off the card's exits first |
| "Should I buy or sell options?" | Corner selection: it is not a preference, it is which corner your measured `p` clears |
| "Which options strategy is profitable?" | Refuse the framing: a *corner* has a price; a strategy is profitable only at a `p` you have measured |
| "My options book is flat" | Expectancy decomposition by cohort — `--from-log`, then Phase 3 |
| "How many contracts?" | `R_max` from `references/streak-survival-by-corner.md`, then defer the band to `trade-sizing-recovery` |
| "Is this card any good?" | `payoff_check.py` on the card; the verdict is the answer |
| "How do I know if my edge is real?" | `n_req`, then the iteration protocol — and `references/overfitting-by-iteration.md` first |
| "Which structure for a 2.5R target?" | `options-strategist` — this skill hands it the payoff profile, not the structure |

<!-- DEEP: 10+min -->
### Ask or fetch, never assume

1. **What are the exits, in money or in R?** `b` comes from the two exit prices and nothing else. If the answer is "discretionary", there is no `b` and no `p*`, and no computation can proceed.
2. **Is `R` the stop distance or the structural max loss?** For premium selling these differ. The one term where it matters is `c_R = cost_per_trade / R_dollars`, and a larger `R` makes the fee look smaller. The checker prints an `R BASIS` line; read it.
3. **What is the measured win rate, and over how many decided trades?** A `p` from memory is not an input. `p` with its sample size is.
4. **What is `c_R` per trade, per contract, per leg, round trip?** Not the headline commission — commission plus fees plus half-spread, with two tickets per leg.
5. **What are the account's drawdown tolerance and its trade pace?** `R_max` needs `D_tol`; `years_at_pace` needs trades per year. Both are the owner's numbers, not defaults.
6. **What is the regime, named by the sibling that classifies it?** `technical-signals-engineer` for trend/range, `macro-strategist` for cross-asset and liquidity, the options siblings for vol rank and term structure.
7. **How many cycles has this cohort already had?** Without the cycle count, the Bonferroni bar stays at the single-hypothesis level. See `references/the-iteration-protocol.md` step 5.

**Route out, not in**, when the question is: a structure to build (`options-strategist`), an open position's next move (`options-position-lifecycle`), one leg's repair (`options-leg-management`), contract counts and loss bands (`trade-sizing-recovery`), the book's Greeks or margin (`options-risk-engineer`), a realised ledger's metrics (`edge-and-payoff-engineering`), or order routing (`options-automation-engineer`).

---

## Anti-Rationalization

| The rationalization | The arithmetic answer |
|---|---|
| "I win 8 out of 10, so the credit spread works." | 80% is *exactly* break-even on the 50%/2× card `[COMPUTED]`. Winning often is the corner's shape, not evidence of an edge. |
| "The stop rarely gets hit, so a wide stop is fine." | The stop's width *is* `b`'s denominator. Widening it lowers `b` and raises `p*` — from 66.67% at 1× to 80.00% at 2× `[COMPUTED]`. |
| "I'll size up while I'm hot." | The streak table says a `p = 0.35` corner expects a 13-loss run in 250 trades `[COMPUTED]`. The streak is the worst moment to raise size; `R_max` is the cap. |
| "Costs are small, they don't matter." | A `$5.20 cost` round trip on a `$15 loss` structure is `c_R = 0.3467R` — larger than a `+0.2250R` edge `[COMPUTED]`. Cost is the whole result there. |
| "A 55% win rate is better than 50%, so it's positive." | Compare to `p*`, never to 50%. On a `b = 0.25` card, 55% is twenty-five points below break-even. |
| "Backtests and live trading differ, so the numbers don't apply." | `b`, `p*`, `n_req` and `L` are closed-form. They apply to every tradeable payoff in every market. Only `p` is estimated. |
| "I've tested twenty variations and one works." | Twenty cycles at nominal 5% is a **64.15%** chance of at least one false positive, and the best-of-twenty overstates its edge by **1.87 × se_E** `[COMPUTED]`. |
| "My book is flat, so I need a better strategy." | A flat pooled figure containing one negative cohort and one unproven cohort is three findings, not a strategy problem. Separate the cohorts first. |
| "Long premium is worse than selling premium." | They are different corners. `b = 2.5` needs `p = 28.57%`; `b = 0.25` needs `p = 80.00%` `[COMPUTED]`. Which is easier is a question about *your* measured `p`. |
| "The Greeks said it was safe." | Greeks describe a position's sensitivities at an instant. They say nothing about `p`, `b`, `n_req` or whether the card pays. |
| "I only changed the stop, so it's the same strategy." | Changing the stop changes how often you lose. It is a new card needing a new cohort tag and a new measurement. |
| "Paper says it works, so it works." | Paper is a prediction. `n_req` is how long until the prediction is graded, and it is usually measured in years. |

---

## Ground Rules

| # | Mechanical Trigger | Violation Response |
|---|---|---|
| GR1 | Any recommendation about which strategy to trade is produced without having run `scripts/payoff_check.py` on the card | Stop. Run the checker. Do not restate the card until a verdict is in hand. |
| GR2 | A win rate is quoted without its sample size | Stop. Report `p` and `n` together, plus `se_p = sqrt(p(1-p)/n)`. A `p` without `n` is a memory. |
| GR3 | `R` is used in more than one sense in the same output | Stop. Pick one definition (`1R` = the money lost when the stop fires), write it on the card, and recompute. Check the `R BASIS` line. |
| GR4 | A cost figure is quoted per leg or per contract when the decision is per trade | Stop. Convert to `cost_per_trade = fee_per_contract × legs × 2` and then to `c_R`. |
| GR5 | A dollar or percentage figure appears with no provenance tag | Stop. Tag it `[COMPUTED]` with its formula, `[ESTIMATED]` with its derivation, `[VERIFIED]` with its source, or `[ILLUSTRATIVE]`. Untagged numbers are removed. |
| GR6 | A cycle is measured before `n_req` trades | Stop. State the trades taken, the trades required, and mark the reading as a peek. A peek is not evidence. |
| GR7 | A proposed change moves more than one of `p`, `b`, `c_R` | Stop. Split into separate cycles. Two changes and the result is unattributable. |
| GR8 | A holdout is re-fitted, or used more than once | Stop. The holdout is spent. Start a new cycle; do not re-check against the old holdout. |
| GR9 | A cycle count is not incremented, or a strategy is tuned past 5 failed cycles | Stop. Apply `alpha_adjusted = 0.05/m`. At `m = 6` the rule is `rotate`, not `tune`. |
| GR10 | The words "profitable", "works", "guaranteed" or "safe" are applied to a strategy rather than to a payoff configuration | Stop. Restate as: this *payoff* pays `E_net` per trade *if* `p` and `b` hold. Then point at `references/what-this-cannot-promise.md`. |
| GR11 | A synthetic-fixture number (`examples/logs/synthetic-options-log.csv`) is quoted as a finding | Stop. The fixture is SYNTHETIC / ILLUSTRATIVE. Relabel it or remove it. |
| GR12 | Structure selection, leg surgery, position exit ordering or contract counts are answered from this skill | Stop. Defer to `options-strategist`, `options-leg-management`, `options-position-lifecycle`, or `trade-sizing-recovery` respectively. |

**Complete when** every recommendation in the output traces to a `payoff_check.py` run or a `[COMPUTED]` derivation shown inline.

---

## The Expert's Mindset

<!-- QUICK: 30s -->
An options trader who lasts does not think in strategies. They think in **corners** — a `(b, p)` pair with a published price — and they know that the structure is downstream of the corner, not upstream of it.

- **The exits define the corner.** `TP` and `SL` are one decision with two numbers in it. The structure is chosen afterwards, to express the payoff at the right cost.
- **A win rate is a measurement with an error bar, not a personality trait.** The bar is often wider than the edge.
- **Cost is a constant in the card, not a month-end surprise.** It is the only lever whose effect is known before the outcome is.
- **A streak is a scheduled event.** A `p = 0.35` corner with 250 trades a year expects a 13-loss run. Sizing that survives the streak is the whole job.
- **The sample is the hypothesis.** If a card needs 4,896 trades to grade, the card is the problem, not the patience.
- **The failure mode to fear is not a losing trade. It is a winning sample.**

<!-- STANDARD: 3min -->
The three sentences that separate a professional from a hopeful:

1. **"What is my `p*`?"** Not my win rate — my *required* win rate. It is `1/(1+b)` and it is fixed the moment the exits are fixed.
2. **"How long until I can grade it?"** `n_req = 4(sd/|E|)²`. If the answer is longer than the horizon, the answer is a different card.
3. **"Which lever am I pulling, and can I pull it today?"** `c_R` is free. `b` is a rules change. `p` is a research project. Pull them in that order.

An expert also holds a specific discomfort: **a book can be flat for years and be behaving exactly as its arithmetic predicted.** The absence of profit is not automatically evidence of a mistake — it can be evidence that `n_req` has not been reached. The mistake would be to change something before the sample could speak.

---

## Deliberate Practice

<!-- DEEP: 10+min -->
| Drill | What it trains | How to run it |
|---|---|---|
| **Corner naming** (10 min) | Reading `(b, p*)` straight off a management rule | Take ten retail options articles. For each, extract the target and the stop, compute `b = TP/SL` and `p* = 1/(1+b)`, and write the required win rate. Compare it to the win rate the article claims. |
| **Backwards sizing** (15 min) | Deriving `b` from a measured `p` | Pick a `p` you believe you have. Compute `b_required = (1 + c_R − p)/p`. Ask whether any structure you trade reaches it. |
| **Ticket counting** (10 min) | Making cost automatic | For twelve structures from 1 to 4 legs, compute `cost_per_trade = fee × legs × 2` and `c_R` at three structure sizes. Time yourself; this should become instant. |
| **Streak rehearsal** (20 min) | Sitting through a scheduled streak | Take your own `p`. Compute `L = ceil(ln(N)/ln(1/(1−p)))`. Write out a `L`-loss sequence with its drawdown at your current size. If the number is unacceptable, change the size now, on paper. |
| **The 50%/2× audit** (10 min) | Applying the identity to your own book | Take every open credit position. Write its `b` from the *actual* exit orders. Compute `p*`. Compare to your measured `p`. This is usually the moment the skill becomes real. |
| **One-change discipline** (30 min) | Resisting compound edits | Write the last five changes you made to a live card. Count how many cycles moved one lever. |
| **Bonferroni arithmetic** (15 min) | Feeling the cost of fishing | Take `m = 5`. Compute `alpha_adjusted = 0.05/5 = 0.01`, `FWER = 1 − 0.95⁵ = 0.2262`, and the required `\|E_net\|` at your own `se_E`. `[COMPUTED]` |
| **Peek detection** (15 min) | Catching yourself measuring early | Keep a log of every time you looked at a cohort's performance. Count the looks. That count is your true `m`. |

---

## Operating at Different Levels

| Level | What the trader has | What this skill asks of them |
|---|---|---|
| **L1 — Learner** | One card, no measured `p`, a broker app | Compute `p*` for the card. That single number is the entire lesson. Do not run a cycle yet. |
| **L2 — Operator** | One card, a rough `p`, some exit discipline | Run `payoff_check.py` on the card. Fix `b` first — it is free. Then start cycle 1 with a `setup` tag and an `n_req`. |
| **L3 — Practitioner** | Two or three corners, a cohort-tagged log, a real `p` per cohort | Run the iteration protocol properly: 70/30 holdout, one lever per cycle, Bonferroni from cycle 2. Retire the negative corner rather than repairing it. |
| **L4 — Professional** | A book of cohorts, a kill list, measured `se_E` per cohort | Manage the correlation question with `options-risk-engineer`. Size from `R_max` per corner, not per trade. Treat `n_req` as a budget line. |
| **L5 — Desk** | Multiple books, delegated execution, a research pipeline | The arithmetic here becomes a *constraint on the research agenda*: only corners whose `n_req` fits the horizon get researched at all. `p` improvement is a capital-allocation decision, priced against the sample it needs. |

`[COMMON-PRACTICE]` Most retail books sit at L1–L2 and skip the `p*` computation entirely, which is why the same cards are abandoned and re-adopted repeatedly without ever being graded.

---

## When to Use

<!-- QUICK: 30s -->
If the question is *which* payoff to trade or *whether* a card pays, it is this skill. If the question is *how to build* it or *what to do with it open*, it is not.

- The owner asks **which options strategy to trade** and has no measured payoff profile.
- The owner asks **why a card they already trade is not paying**, and no one has computed its `p*`.
- The owner asks **what win rate they need** — this skill answers it exactly and immediately.
- The owner asks **whether to buy or sell premium**, and the answer should be a corner comparison rather than a preference.
- The owner's book is **flat or drifting** and needs expectancy decomposition by cohort.
- A **new card** is being written and needs its `p`, `b`, `n_req` and `R_max` stated before it is traded.
- A **cost problem** is suspected: leg count, rung count, or structure size.
- A **strategy is being chosen for a named regime** and needs the corner that regime pays.
- An existing strategy has run **5 cycles with `E_net ≤ 0`** and needs the rotation decision.

**Complete when** the owner can state, for the card in question: `b`, `p*`, the measured or hypothesised `p`, `E_net`, `n_req`, and the verdict.

---

## When NOT to Use

- **Structure mechanics once the profile is chosen** — how to pick strikes, deltas, expirations and skew for a given payoff → `options-strategist`, `advanced-options-structures`.
- **An open position's next move** — hold / add / restructure / trim / cut / roll / convert / close, and their order → `options-position-lifecycle`.
- **One leg's repair** — scale-outs, fly-to-vertical downgrades, pin guard, legging rules → `options-leg-management`.
- **Contract counts, loss bands, size ladders, re-entry after a loss** → `trade-sizing-recovery`.
- **Portfolio Greeks, margin, buying power, the DTE calendar, gap stress tests** → `options-risk-engineer`.
- **Expectancy measurement on a realised ledger, and the cohort kill list** → `edge-and-payoff-engineering`.
- **Timeframe bucketing and significance-by-bucket** → `timeframe-performance-statistics`.
- **Order routing, automation, circuit breakers** → `options-automation-engineer`.
- **Which market data to buy and how to source it** → `trading-decision-data-catalogue`.

**Complete when** the response names the sibling that owns the out-of-scope part, rather than answering it here.

---

## Decision Trees

### DT1 — Which payoff corner should this book be trading?

```
What do you actually have?
│
├─ A measured win rate with its sample size, and a card with written exits
│   ├─ Compute b = TP/SL, then p* = 1/(1+b)
│   │   ├─ p > p* by more than se_E     →  POSITIVE. Trade it. Size from R_max.
│   │   ├─ |p - p*| inside se_E         →  MARGINAL. Not gradable at this n.
│   │   │                                   →  lengthen the cycle to n_req, OR
│   │   │                                   →  raise b (free) to lower p*
│   │   └─ p < p* by more than se_E     →  NEGATIVE. Do NOT tune it.
│   │                                        └─ rotate to a different CORNER
│   └─ ▼ If b could be raised by a rules change, do that FIRST — it needs no forecast
│
├─ A card but no measured win rate
│   ├─ Compute p* anyway. That number IS the requirement.
│   ├─ Run the checker at a plausible p. Read the sensitivity panel.
│   └─ ▼ The entry condition must plausibly supply the p. If nothing does, the card is a wish.
│
└─ No card and no profile
    ├─ Name the regime first (see DT2: the regime picks the corner)
    └─ ▼ Then read the corner off references/payoff-corners-for-options.md
```

### DT2 — Which corner does this regime pay?

```
What is the regime, named by the sibling that classifies it?
│
├─ Trending (ADX > 25, signed slope) — technical-signals-engineer
│   ├─ Long premium, directional: b = 2.5 → p* = 28.57%
│   ├─ Short premium here is hurt: realised b falls as stops gap
│   └─ ▼ Exit rule: 1R stop, 2.5R target, trail after 1.5R
│
├─ Range-bound (ADX < 20, flat slope, ATR/close < 2%)
│   ├─ Short premium, defined risk: b = 0.5 → p* = 66.67%
│   └─ ▼ Stop must be ≤ 1x the credit. A 2x stop raises p* to 80.00%
│
├─ High IV with realised below implied
│   ├─ Short premium, defined risk. This is the variance risk premium.
│   └─ ▼ Gate on IV rank AND on realised trailing implied
│
├─ Low IV with realised above implied
│   ├─ Long premium — directional or non-directional
│   └─ ▼ The IV-rank gate IS the edge source, not a refinement
│
├─ Event-driven (earnings, FOMC, FDA)
│   ├─ Long premium through the event, or short premium after the IV crush
│   └─ ▼ sd is high and bimodal: n_req rises, and R_max falls
│
└─ Volatile range (ADX < 20 AND ATR/close > 3%)
    └─ ▼ NO CORNER CLEARS ITS COST. Stay flat.
```

### DT3 — Is the card positive, marginal, or dead?

```
Run: payoff_check.py on the card
│
├─ verdict == POSITIVE
│   ├─ E_net ≥ se_E at the planned n
│   ├─ Check n_req against the trading horizon (years_at_pace)
│   │   ├─ fits     →  trade it; size from R_max; log with a setup tag
│   │   └─ doesn't  →  ▼ the card is real but ungradable: raise b or change size
│   └─ ▼ Advance to the next cycle only after n_req trades, never before
│
├─ verdict == MARGINAL
│   ├─ |E_net| < se_E: indistinguishable from no edge at this n
│   ├─ Compute n_req. If it exceeds a decade of trading, the card is dead in practice
│   └─ ▼ Prefer raising b (free) over lengthening the sample (years)
│
└─ verdict == NEGATIVE
    ├─ Do not tune parameters. Tuning a card with no edge IS the failure mode.
    ├─ Raise b first if the exits permit it (stop tighter relative to target)
    ├─ Then reduce c_R (fewer legs, fewer rungs, larger R)
    └─ ▼ After 5 cycles with E_net ≤ 0: ROTATE to a different corner. Full stop.
```

### DT4 — Where is the cost coming from?

```
c_R is larger than expected. Which term?
│
├─ Leg count
│   ├─ cost_per_trade = fee_per_contract × legs × 2
│   ├─ 4 legs @ $0.65 round trip = $5.20 per structure
│   └─ ▼ On a $100 R that is 0.0520R; on a $500 R it is 0.0104R
│
├─ Rung count
│   ├─ fee_per_rung = legs × fee_per_contract
│   ├─ fee_negative iff position_value < rung_split × legs × fee_per_contract
│   └─ ▼ 4 legs, 3 rungs, $0.65 → threshold $7.80 per spread
│
├─ Structure size
│   ├─ c_R = cost_per_trade / R_dollars rises as R falls
│   └─ ▼ Below R ≈ $25 a 4-leg structure consumes 92% or more of a 0.225R edge
│
└─ Half-spread omitted
    ├─ Usually the largest component, and it scales with legs
    └─ ▼ Recompute c_R with it included before concluding anything
```

**Complete when** a corner, a `p*`, and a cost term have all been named with their arithmetic.

---

## Core Workflow

### Phase 1 — Establish the corner, before anything else

1. Get the exits. `TP` and `SL`, in R or in money, and the order type that implements each.
2. Compute `b = TP / SL` `[COMPUTED]`.
3. Compute `p* = 1/(1+b)` `[COMPUTED]`. **This is the requirement.** Write it down.
4. Compute `b* = (1−p)/p` at the hypothesised `p` `[COMPUTED]` — the break-even payoff at that win rate.
5. Compare `p*` to the win rate actually measured, and to `se_p`. If `|p − p*|` is inside the error bar, the card cannot be graded yet.

### Phase 2 — Establish the cost, which is free to fix

6. `cost_per_trade = fee_per_contract × legs × 2` — two tickets per leg `[COMPUTED]`.
7. `c_R = cost_per_trade / R_dollars` `[COMPUTED]`.
8. Compute `p*_net = (1 + c_R)/(1 + b)` — the *net* required win rate `[COMPUTED]`.
9. If the card scales out in rungs, compute the threshold `rung_split × legs × fee_per_contract` and check it against the structure's value.

### Phase 3 — Measure the record, by cohort

10. Run `payoff_check.py --from-log <log>` with `setup` and `cost` columns present.
11. Read `p`, `b`, `E`, `c_R`, `E_net` **per cohort**. Never act on the pooled row.
12. Compare each cohort's realised values against its card's prediction.
13. Retire negative cohorts. Do not repair them.

### Phase 4 — Fix the payoff

14. `c_R` first: remove the rungs, reduce the legs, or increase `R` — all free.
15. `b` second: tighten the stop relative to the target. This is a rules change, and it makes the card a **new** card.
16. Re-run the checker. The `b` change alters `p` too — the tighter stop fires more often — so the new `p` must be measured, not assumed.
17. `p` last, and only as a research project with a named signal.

### Phase 5 — Iterate, with the protocol

18. Pre-register which lever changed and the direction predicted.
19. Run exactly `n_req` trades. Hold out the last 30%. Never re-fit the holdout.
20. Increment `m`. Apply `alpha_adjusted = 0.05/m` and publish the threshold.
21. At 5 cycles with `E_net ≤ 0`, rotate the corner.

### Failure Modes

1. **Failure mode — the popular credit card is traded with no `p*` computation.** The card needs `p* = 80.00%` `[COMPUTED]`. A trader who does not know that number cannot know whether they are meeting it.
2. **Failure mode — the wide stop.** A 2×-credit stop with a 50%-of-credit target gives `b = 0.25` and `p* = 80.00%`; the same card at a 1× stop gives `b = 0.50` and `p* = 66.67%` `[COMPUTED]`. The wide stop costs thirteen percentage points of required skill.
3. **Failure mode — the win rate is compared to 50% instead of to `p*`.** On a `b = 0.25` card, 55% is twenty-five points below break-even.
4. **Failure mode — the cost is omitted, or only the commission is counted.** A `$5.20 cost` on a `$15 loss` structure is `c_R = 0.3467R` against a `+0.2250R` edge: `E_net = −0.1217R` `[COMPUTED]`, and the half-spread was not even included. On a `$400 risk` structure the same fee is `0.0130R` and the card survives `[COMPUTED]`.
5. **Failure mode — cost is amortised annually instead of charged per trade.** `E_net = E − c_R` is per trade. Averaging the fee across winners hides it from the losers, where it also applies.
6. **Failure mode — the card is measured before `n_req`.** A hot week is not evidence. The `p = 0.68, b = 0.5` card needs `n_req = 4,896` trades `[COMPUTED]`; measuring it at 40 is a peek.
7. **Failure mode — two levers moved in one cycle.** A tighter stop *and* a better entry filter produce a rise in `E` that cannot be attributed to either.
8. **Failure mode — the holdout is re-fitted.** Once the holdout informs a parameter choice it is part of the fit, and the 70/30 split has become 100/0.
9. **Failure mode — the cycle count is not incremented.** Without `m`, the Bonferroni bar stays at 1.96 and a searched card passes a single-hypothesis test. At `m = 20`, `FWER = 64.15%` `[COMPUTED]`.
10. **Failure mode — a negative corner is tuned instead of rotated.** Past five failed cycles a real edge must clear `0.1141R` at `se_E = 0.0443R` `[COMPUTED]` — 5.7 times the edge the card actually has. Tuning is the failure mode this skill exists to prevent.
11. **Failure mode — the pooled book is acted on.** A flat pooled figure containing one negative cohort and one unproven cohort is three findings. Acting on the pool hides the losing cohort behind the winning one.
12. **Failure mode — `R` is defined as the structural max loss while the stop is far inside it.** Every number below gets flattered, most importantly `c_R = cost_per_trade / R_dollars`.
13. **Failure mode — a `p` without a sample size.** `p = 0.80` measured over 40 trades carries `se_p = 0.0632` `[COMPUTED]`, spanning 0.68 to 0.92 — the whole decision.
14. **Failure mode — the streak is not planned for.** A `p = 0.35` corner expects a 13-loss run in 250 trades `[COMPUTED]`. Sizing at the `p = 0.80` allowance loses the account on a streak that was scheduled in advance.
15. **Failure mode — a multi-rung scale-out pays a second opening fee.** Three rungs on a 4-leg structure costs `3 × $2.60 = $7.80` versus a single close at `$2.60`; the `$5.20` difference is exactly the round-trip fee of opening the structure `[COMPUTED]`.
16. **Failure mode — a synthetic-fixture number is quoted as a market finding.** `examples/logs/synthetic-options-log.csv` is SYNTHETIC / ILLUSTRATIVE. It is not market data and not a backtest.
17. **Failure mode — a bull market is treated as making premium selling safe.** A bull market raises short-put win rates and raises the gap when it ends. Both sides of the card move together.
18. **Failure mode — a stop change is assumed to leave `p` unchanged.** The stop's whole job is to set how often the trade loses. A new stop is a new card.

### Regime Table

| Regime | What the sibling names it | Corner that pays | `p*` at that corner's `b` | What kills it |
|---|---|---|---|---|
| **Trending** | strong uptrend / volatile uptrend, ADX > 25 | long premium, directional | 28.57% at `b = 2.5` | a false break; a quiet range that bleeds theta |
| **Trending against the seller** | volatile downtrend, weak uptrend failing | long premium, bearish | 28.57% at `b = 2.5` | short-premium books here: stops gap, realised `b` collapses |
| **Range-bound** | ranging, ADX < 20, ATR/close < 2% | short premium, defined risk | 66.67% at `b = 0.5` | a breakout; the loss arrives in one gap, not as a stop |
| **High IV, realised below implied** | high IV rank with realised trailing | short premium, defined risk | 66.67% at `b = 0.5` | realised vol rising through implied; the term structure inverting |
| **Low IV, realised above implied** | low IV rank | long premium | 28.57% at `b = 2.5` | implied re-rating upward after entry; a quiet follow-through |
| **Event-driven** | earnings, FOMC, FDA, index rebalance | long premium pre-event; short premium post-crush | 28.57% / 66.67% | a move smaller than the implied move; the crush after entry |
| **Volatile range** | ADX < 20 with ATR/close > 3% | **nothing** | — | no corner clears its own cost; `[COMMON-PRACTICE]` this is the regime `technical-signals-engineer` calls "no edge in chaotic ranges" |
| **Correction** | a 5–10% pullback | long premium, bearish | 28.57% at `b = 2.5` | a V-shaped reversal; theta on a slow decline |
| **Bear market** | a 10–20% downturn | long premium, bearish | 28.57% at `b = 2.5` | short-premium books here take the largest drawdowns in the corner's history |
| **Crash / tail event** | a 20%+ decline, a black swan, a market collapse | long premium with positive convexity | 20.00% at `b = 4.0` | short-premium books are destroyed together — the correlation-collapse question belongs to `options-risk-engineer` |

The March 2020 selloff is the reference case for the last row: short-premium structures failed simultaneously rather than independently, which is why a book of five of them is one position, not five.

---

## Best Practices

1. **Compute `p*` before you compute anything else.** It is `1/(1+b)`, it is free, and it is the single number that decides whether the card is worth discussing.
2. **Fix `b` before you work on `p`.** `b` is a rules change available today; `p` needs a signal. `dE/dp = b+1` and `dE/db = p`, so the derivative favours win rate — but availability does not.
3. **Set the stop tighter relative to the credit than the target is.** For premium selling that means cutting at ≤ 1× the credit with a 50%-of-credit target, giving `b ≥ 0.5` and `p* ≤ 66.67%` `[COMPUTED]`.
4. **Count tickets, not trades.** `cost_per_trade = fee_per_contract × legs × 2`. A four-leg structure pays eight tickets, not four.
5. **Convert every cost to `c_R` before comparing structures.** A `$5.20` cost is `0.0104R` on a `$500` structure and `0.3467R` on a `$15` structure `[COMPUTED]`.
6. **Never scale out of a small structure without checking the threshold.** It is `rung_split × legs × fee_per_contract` per spread — a `$7.80 cost` floor for a 4-leg, 3-rung split at `$0.65` `[COMPUTED]` — and below it every rung banks less than it pays.
7. **Tag every trade with a `setup` cohort.** The tag is the key that makes expectancy decomposable and a kill list possible.
8. **Report `p` with its sample size and `se_p`.** A win rate without an error bar is a memory.
9. **Compute `n_req` before committing to a cycle.** If it exceeds the horizon, the card is the problem.
10. **Read `R_max` per corner, not per trade.** Streak length is a property of the win rate, so the permissible risk differs by more than 3× between the two central corners.
11. **Change one lever per cycle and pre-register which one.** Two changes and the result is unattributable.
12. **Hold out the last 30% by time, and never re-fit it.** Time holds out better than a random split because the regime changes.
13. **Increment the cycle count and publish the Bonferroni threshold.** Fishing has a price and the price is paid in required evidence.
14. **Retire negative corners; do not repair them.** Past five failed cycles, rotate.
15. **Treat a cost reduction as the only lever whose effect is known in advance.** It does not depend on `p` or `b` at all.
16. **Read the `R BASIS` line before believing any output.** Most wrong results are a wrong `R`.

**Complete when** the card has a stated `b`, `p*`, `c_R`, `E_net`, `n_req` and verdict, and each one traces to a printed formula.

---

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| `b` prints as `n/a` | `--sl 0`: a zero stop means the loss is unbounded, so there is no loss for the denominator | Supply a non-zero stop, or acknowledge there is no `b` and therefore no `p*` | Without a loss there is no payoff ratio. "No stop" is not a card. |
| Verdict is MARGINAL and the sign is positive | `\|E_net\| < se_E` at the planned `n` | Compute `n_req`. Raise `b` (free) or lengthen the cycle | A thin edge is not a weak edge; it is an unmeasured one. |
| `n_req` prints as `n/a` with "E ≤ 0" | `E_net` is zero or negative, so `4(sd/\|E\|)²` is undefined | This is a *result*, not an error. Do not supply an `E` to make it compute | You cannot see an edge that is not there. |
| `years_at_pace` prints as `n/a` | `n_req` is undefined, or `--trades-per-year` is not positive | Fix the card first, then the pace | The horizon is a property of the card, not of the patience. |
| `R_max` prints as `n/a` | `L = 0`, which happens only when `p = 1` | A win rate of 1 is a modelling error, not a sizing input | Check `p` before reading `R_max`. |
| Repaired stop made `E` worse | The target was cut at the same time as the stop | Change one lever. Re-run the checker after each single change | "50%/1×" is better than "50%/2×"; "25%/1×" is worse than both. |
| `E_net` far below `E` | `c_R` is large: too many legs, too many rungs, or too small an `R` | Halve the leg count, drop the rungs, or increase `R` | Cost is set by the structure; `R` is set by the market. |
| Fee looks 100× too large in credit mode | Per-share credit was divided into a per-spread fee | Use `--multiplier` (default 100); the tool derives `R` as `(W − C) × multiplier` | Exchange rules: the standard US equity-option multiplier is 100. |
| Cohort row and pooled row disagree | The pool contains cohorts with different `b` | Act on the cohort row. The pool is an average of strategies, not a strategy | Read the `setup` row, always. |
| A card passes at `m = 1` and fails at `m = 5` | The Bonferroni threshold tightened | This is the correction working. Publish the threshold | Searched results must clear a searched bar. |
| Tool output differs between runs | It cannot. The engine is deterministic | Your inputs differ. Diff the command lines | Determinism is verified by `scripts/verify-skill.sh`. |
| `b*` prints as `n/a` | `p = 0`: no payoff breaks even at a zero win rate | Check `p` | Every field has a domain; the engine states it rather than substituting a number. |

---

## Error Recovery

| Situation | Recovery |
|---|---|
| The checker's output looks wrong | Read the `R BASIS` line first, then `p`, then `c_R`. Those three explain almost every surprising output. |
| A cycle produced a negative result after `n_req` trades | Log it with its `setup` tag and increment `m`. A negative result is a finding; it needs no repair. |
| Five cycles, all `E_net ≤ 0` | Rotate the corner. Do not tune. Restate the new corner's `p*` and start `m` at 1. |
| A card was traded without a `p` measurement | Treat the trades as a cohort with an unknown `p`. Run `--from-log` to get the realised `p` with its `se_p`. Do not size from an unmeasured `p`. |
| Cost turned out to be much larger than expected | Convert to `c_R`. Reduce legs, drop the rungs, or increase `R`. This is the only lever whose effect is known before the outcome. |
| The stop was changed mid-cohort | The cohort is now two cards. Split the log by date of change and tag them separately. Pooling measures neither. |
| The holdout was used twice | The holdout is spent. Start a new cycle with a new holdout. Do not re-check against the old one. |
| A `p` estimate was revised downward | `p*` is unchanged — it depends only on `b`. Re-run the checker at the new `p` and accept the verdict. |
| Two levers were changed at once | The cycle's result is unattributable. Log it as such, revert one lever, and run the next cycle with one change. |
| The owner wants a strategy recommendation and there is no card | Do not recommend a structure. Give `p*` for the corners that fit the named regime, and ask for the exits. |
| A number cannot be verified | Say which part is unverified. State the formula that would verify it and the input that is missing. Do not substitute a plausible figure. |

**Complete when** every recovery ends with a stated next action, a `setup` tag, and a cycle count.

---

## Cross-Skill Coordination

### Upstream (what this skill needs)

| Upstream Skill | What it supplies | How this skill consumes it |
|---|---|---|
| `options-strategist` | the structure family that expresses a given payoff profile, the leg construction once the profile is chosen, and the pattern-recognition engine it consults before selecting anything | receives the corner; returns the `TP`/`SL` and the required `p*`. This skill never selects strikes, and it does not re-derive the pattern-recognition thresholds — it consumes them by name. |
| `trade-sizing-recovery` | per-trade size bands, loss bands, the size ladder, exit-threshold precedence | receives `R_max` as an upper bound; returns nothing. `R_max` is a cap, not a band. |
| `edge-and-payoff-engineering` | expectancy measurement on a realised ledger, the cohort kill list, cost drag in R | shares the `p`/`b`/`E` algebra and the exact CSV log schema, so a cycle logged once can be graded by either. |
| `technical-signals-engineer` | the named trend/range regime (ADX, SMA slope, ATR/close) | the regime filter field of every strategy card. Regimes are consumed by name, never redefined. |
| `macro-strategist` | central-bank reaction function, liquidity impulse, risk-on/risk-off | the cross-asset context that decides which corner is legal in a given quarter. |
| `quantitative-analyst` | IV rank, term-structure shape, the volatility inputs | the entry gate on both premium-selling and long-premium cards. |
| `options-risk-engineer` | portfolio Greeks, margin, the DTE calendar, gap and correlation stress | makes `sd`, `n_req` and `R_max` *more* conservative: they assume independent trades. |
| `trading-decision-data-catalogue` | which market data to buy and from where | the provenance behind an IV rank or a realised-vol comparison, when one is used. |

### Downstream (what this skill produces)

| Downstream Skill | What it receives | Why it needs it |
|---|---|---|
| `options-position-lifecycle` | the card: corner, `TP`, `SL`, `setup` tag, and the `b` that follows | the exit ORDER and CADENCE on an open position operate on the numbers this skill fixed at entry. |
| `edge-and-payoff-engineering` | cycle records with `setup`, `cost` and `risk` columns | the cohort kill list is built from tagged cycles; the schema is shared. |
| `options-risk-engineer` | the corner and its `b`, per open position | portfolio gamma and the correlation question need each position's payoff shape. |
| `trade-sizing-recovery` | `R_max` per corner, and the prediction `p`/`b` | size bands sit *below* `R_max`; the bands need the cap and the corner. |
| `options-leg-management` | the `b` the structure is supposed to deliver | a leg repair is justified only if it moves the realised `b` back toward the card's `b`. |
| `timeframe-performance-statistics` | cohorts with close dates and a `setup` tag | bucketing needs a close-date convention and a cohort key; both come from the log this skill standardises. |
| `options-automation-engineer` | the exact rule set: entry condition, `TP`, `SL`, size | automatable rules require numeric exits and a numeric size, which is what a card is. |
| `trading-decision-data-catalogue` | which inputs a card needs (IV rank, realised vol, term structure) | the data budget follows the cards actually being run, not a wish list. |

---

## Proactive Triggers

- **The owner names a strategy without naming an exit.** Ask for `TP` and `SL` before anything else. Without them there is no `b`.
- **The owner quotes a win rate with no sample size.** Compute `se_p = sqrt(p(1−p)/n)` and show the interval. Then compare it to `p*`.
- **The owner says "my book is flat."** Decompose by cohort before offering any change. A flat pool is usually a positive cohort financing a negative one.
- **The owner mentions a scale-out, a rung, or "taking some off."** Compute the rung threshold immediately: `rung_split × legs × fee_per_contract`.
- **The owner describes a 4-leg structure on a small account.** Compute `c_R` at that `R` before discussing anything else.
- **The owner has tested several variations of one card.** Ask how many. That number is `m`, and it sets the bar.
- **The owner is about to change two things.** Name the two levers and ask which one is being tested.
- **The owner says "the stop rarely gets hit."** That is a description of the corner, not a defence of the stop. Compute `p*` at both stop widths.
- **The owner reports a winning month.** Ask for `n_req` and the trades taken so far. A winning stretch inside `n_req` is not evidence.
- **The owner is about to abandon a card after a losing streak.** Compute `L`. If the streak is shorter than or equal to `L`, the card behaved exactly as predicted.

**Complete when** every trigger fires a computation rather than an opinion.

---

## Anti-Patterns

❌ **Choosing a strategy first and computing `p*` later.** ✅ Name the corner from the regime, then write the exits, then compute `p* = 1/(1+b)` — all before selecting a structure.

❌ **Treating "I win most of the time" as an edge.** ✅ Winning most of the time *is* the `b = 0.25` corner's shape, and that corner needs 80.00%. Compute the requirement.

❌ **Repairing a negative corner by tuning parameters.** ✅ Raise `b` (free) or reduce `c_R` (free); after five failed cycles, rotate the corner. Tuning a card with no edge is the failure mode, not the fix.

❌ **Pooling cohorts and acting on the pool.** ✅ Read the `setup` row. A pooled figure is an average of strategies, which is not a strategy.

❌ **Amortising cost annually or across winners.** ✅ `E_net = E − c_R` is per trade. Charge it to every trade, including the losers.

❌ **Sizing from a win rate with no error bar.** ✅ Report `p`, `n` and `se_p` together, then compute `R_max`. A `p` without `n` is a memory.

❌ **Measuring a cycle before `n_req` trades.** ✅ A hot week is not evidence. State the trades taken, the trades required, and mark the reading a peek.

❌ **Changing two levers in one cycle.** ✅ One lever per cycle, pre-registered, with the direction predicted.

❌ **Scaling out without checking the rung threshold.** ✅ `fee_negative iff position_value < rung_split × legs × fee_per_contract`. Below it, every rung banks less than it pays.

❌ **Calling a card "profitable" because the checker said POSITIVE.** ✅ The verdict is about the *inputs*. Restate as "this payoff pays `E_net` per trade if `p` and `b` hold", and point at `references/what-this-cannot-promise.md`.

❌ **Quoting a synthetic-fixture number as a finding.** ✅ The fixture is SYNTHETIC / ILLUSTRATIVE. Relabel it or remove it.

❌ **Skipping the cycle count.** ✅ `alpha_adjusted = 0.05/m`. Without `m`, a searched card passes a single-hypothesis test.

---

## State Log

```
[CARD:  <setup-tag>]
  corner         : <long premium | short premium | symmetric>  b = <tp/sl>  p* = <1/(1+b)>
  structure      : <named>            (selected by options-strategist, not here)
  regime filter  : <named state>      (classified by technical-signals-engineer / macro-strategist)
  entry condition: <numeric trigger>
  TP / SL        : <levels>           r-basis = <stop distance | structural max loss>
  size rule      : R_max = <d_tol/(L*safety)>;  band source = trade-sizing-recovery
  prediction     : p = <x>  b = <y>  E = <p*b-(1-p)>  c_R = <cost/R>  E_net = <E - c_R>
  n_req          : <4*(sd/|E|)^2>   L = <ceil(ln(n)/ln(1/(1-p)))>   years_at_pace = <n_req/tpy>
  verdict        : <POSITIVE | NEGATIVE | MARGINAL>

[CYCLE: <n> of <5>]
  lever changed  : <p | b | c_R>       one only
  hypothesis     : <direction predicted, written BEFORE the first trade>
  trades taken   : <n>                 n_req = <n_req>
  fit window     : first 70%; holdout: last 30%; holdout re-fits: <0>
  realised       : p = <x> b = <y> E = <z> c_R = <a> E_net = <b>
  se_p / se_E    : <sqrt(p(1-p)/n)> / <sd/sqrt(n)>
  m (cycles)     : <m>   alpha_adjusted = 0.05/m = <x>   threshold = <z(1-x/2) * se_E>
  holdout result : <agrees | disagrees | not yet reached>
  outcome        : <keep | revise one lever | ROTATE corner>

[KILL LIST: <setup-tag> — retired <date> — reason: E_net <= 0 after <m> cycles]
```

**Complete when** every open card and every cycle has a filled block, and every retired cohort is on the kill list with its cycle count.

---

## Production Checklist

- **CR1** — `b` computed from the two exit prices, and both exits implemented as live orders (not descriptions).
- **CR2** — `p* = 1/(1+b)` computed and written on the card `[COMPUTED]`.
- **CR3** — `b* = (1−p)/p` computed at the hypothesised `p` and compared to `b`.
- **CR4** — `p` reported with `n` and `se_p`; the interval compared to `p*`.
- **CR5** — `cost_per_trade = fee_per_contract × legs × 2` computed with the half-spread included.
- **CR6** — `c_R = cost_per_trade / R_dollars` computed, and `R` defined exactly one way.
- **CR7** — `p*_net = (1 + c_R)/(1 + b)` computed; the card clears it on the measured `p`.
- **CR8** — `n_req = 4(sd/|E|)²` computed and compared to the trading horizon.
- **CR9** — `L = ceil(ln(N)/ln(1/(1−p)))` computed, and `R_max = D_tol/(L × safety)` used as the size cap.
- **CR10** — the multi-rung threshold checked if the exit scales out.
- **CR11** — the verdict is `POSITIVE`, or the card is not traded.
- **CR12** — every trade tagged with a `setup` cohort and a `cost`.
- **CR13** — the regime filter named by the sibling that classifies it, with its numeric threshold.
- **CR14** — the cycle count `m` recorded, and `alpha_adjusted = 0.05/m` published.
- **CR15** — the holdout is by time, 30%, and has not been re-fitted.
- **CR16** — the kill criterion is a count and a measure, not a feeling.
- **CR17** — out-of-scope parts deferred to the named sibling rather than answered here.
- **CR18** — every number tagged, and every claim about profitability restated as a conditional.

---

## What Good Looks Like

A correct output from this skill looks like a **one-page card plus a cycle record**, and it reads like an engineer's note rather than a market call.

```
Corner           long premium, b = 2.50, p* = 28.57%                    [COMPUTED]
Exits            1R stop (stop-limit), 2.5R target (limit)             [VERIFIED] both are live orders
Prediction       p = 0.35, E = 0.35*2.5-0.65 = +0.2250 R               [COMPUTED]
Cost             c_R = 0.02 R  ->  E_net = +0.2050 R                   [COMPUTED]
Sample           n_req = 220.20, years_at_pace = 0.88 at 250 trades/yr [COMPUTED]
Streak           L = 13  ->  R_max = 0.20/(13*1.5) = 1.03% of equity   [COMPUTED]
Verdict          POSITIVE (E_net 0.2050 >= se_E 0.1056 at n = 250)
Regime filter    trend per technical-signals-engineer (ADX > 25, signed slope) AND IV rank <= 30
Kill criterion   retire after 5 cycles with E_net <= 0
Not claimed      that this strategy is profitable. The verdict is arithmetic on the inputs.
```

The properties that make that good:

1. **Every number carries a formula or a tag.** A reader can substitute and check.
2. **The requirement (`p*`) is stated before the prediction (`p`).** The order matters: it prevents choosing `p` to fit a desired verdict.
3. **The sample is a budget line, not a footnote.** `n_req` and `years_at_pace` sit beside the edge.
4. **The size cap is derived from the streak, not from the edge.** `R_max` uses `L`, which is a property of `p`.
5. **The claim is bounded.** The output says what it establishes and stops there.
6. **Out-of-scope parts are named, not answered.** The structure was handed to `options-strategist`; the band to `trade-sizing-recovery`.

**Complete when** the card could be handed to a second person who could reproduce every number from the formulas printed on it.

---

## Verification Guardrails

### Pre-Generation

- **Never guess security.** Nothing in this skill selects, recommends or prices a security. It prices a *payoff*.
- **Flag your knowledge cutoff.** The option mechanics relied on here — two tickets per leg per round trip, the 100-share standard contract multiplier, assignment and exercise being fee-bearing events — are long-standing listed-option conventions. Product listings, fee schedules, margin requirements and exchange rules change over time and must be verified at the source.
- **Admit uncertainty** about any `p` you have not measured. A hypothesised `p` is an input, not a finding.

### Post-Generation

- **Every number is tagged.** `[COMPUTED]` with its formula, `[VERIFIED]` with its source, `[ESTIMATED]` with its derivation, `[ILLUSTRATIVE]` for invented values, `[COMMON-PRACTICE]` for accepted convention.
- **No claim of profitability.** Any sentence implying a strategy makes money is restated as a conditional on `p` and `b`.
- **`R` is defined exactly once** in each output, and the `R BASIS` line is read before the numbers.
- **Cost is present and non-zero** in any comparison, or its absence is stated as a caveat.
- **The sample requirement is stated** wherever an edge is stated.
- **The cycle count is stated** wherever a tested result is stated.
- **Synthetic data is labelled** wherever its output appears.
- **Out-of-scope questions are deferred by name**, not answered.

**Complete when** every one of the eight post-generation items is satisfied.

---

## References

| File | What it covers |
|---|---|
| [`references/payoff-corners-for-options.md`](references/payoff-corners-for-options.md) | the corner map with each row's arithmetic derived, and which lever to fix first |
| [`references/break-even-payoff-for-credit-structures.md`](references/break-even-payoff-for-credit-structures.md) | the credit-spread break-even table; the `p = 0.80` identity; the net required win rate |
| [`references/stop-and-target-arithmetic.md`](references/stop-and-target-arithmetic.md) | `p* = sl/(tp+sl)`; the stop as the free lever; building a card backwards |
| [`references/regime-to-strategy-map.md`](references/regime-to-strategy-map.md) | regime × corner × structure × entry × exit × sizing, with the two central claims derived |
| [`references/cost-drag-per-leg-and-per-rung.md`](references/cost-drag-per-leg-and-per-rung.md) | per-leg and per-rung cost; the fee-negative threshold; cost as a required win rate |
| [`references/small-account-instrument-choice.md`](references/small-account-instrument-choice.md) | the size crossover where the fee exceeds the edge; the instrument-choice rules |
| [`references/streak-survival-by-corner.md`](references/streak-survival-by-corner.md) | `L` and `R_max` per corner; why the two corners need different risk per trade |
| [`references/the-iteration-protocol.md`](references/the-iteration-protocol.md) | the seven-step protocol: pre-register, one change, `n_req`, holdout, Bonferroni, rotate, log |
| [`references/overfitting-by-iteration.md`](references/overfitting-by-iteration.md) | the FWER and selection-overstatement tables; the three ways iteration overfits |
| [`references/strategy-cards.md`](references/strategy-cards.md) | the card schema, and what makes a card testable rather than merely stated |
| [`references/from-negative-to-positive-walkthrough.md`](references/from-negative-to-positive-walkthrough.md) | a worked three-cycle sequence with the honest verdict after each step |
| [`references/what-this-cannot-promise.md`](references/what-this-cannot-promise.md) | the limits: `p` has sampling error, the protocol stops self-deception, nothing is market data |
| [`references/measured-evidence.md`](references/measured-evidence.md) | what the four studies under `examples/` actually measured — legs and tenor buy shape not edge, cost per leg and per tenor, the real-but-fragile variance risk premium, and why 0DTE is unbacktestable — each number with its source path and its `[MODELED]` / `[COMPUTED]` / `[ESTIMATED]` tag |

### Data, sources and thresholds

- **Option mechanics** — `[VERIFIED]` the round-trip ticket count is two per leg, and the standard US equity-option contract multiplier is 100. Both are listed-option conventions; confirm current exchange rules (CBOE and OCC publish their fee and contract specifications) before relying on either for a specific account.
- **Fees and half-spreads** — inputs, not findings. Source them from the broker's own schedule and the exchange's published fee table; no fee schedule is asserted to be current here.
- **All thresholds in the checker** are named constants in `scripts/payoff_check.py` and are printed in the output beside the value they produce.
- **`examples/logs/synthetic-options-log.csv`** is SYNTHETIC / ILLUSTRATIVE, generated at fixed seed `20261014`. It is not market data, not a backtest, and not a result. The label travels with the data: the generator writes it into the file header and the engine echoes it into every output.
- **No vendor data of any kind.** No price series, no quote, no implied vol, no realised vol, no benchmark, no risk-free rate. The engine has no network call and no third-party dependency.
- **Numbers used above are the checker's own output** on the documented commands in `examples/checks/`, or `[COMPUTED]` derivations whose formulas are shown inline. Where a figure could not be verified, it is labelled unverified rather than presented as fact.
- **Knowledge cutoff** — mechanics referenced as of the author's checkout; exchange rules and product listings must be re-verified at the source.
- **Sources consulted for the mechanics only:** CBOE contract specifications, OCC contract-adjustment and exercise/assignment rules, and broker commission schedules. Data from these sources is used for ticket counts and the multiplier only; no market statistic, benchmark or backtest is cited, because none was used.
- **Citations** — verified against the sibling skills for regime naming (`technical-signals-engineer`, `macro-strategist`), for log schema and the `p`/`b`/`E` algebra (`edge-and-payoff-engineering`), and for the close-date convention (`timeframe-performance-statistics`). No external statistic is quoted anywhere in this skill.

---

## Gotchas

1. **`b` is a ratio, so it is scale-free — and that hides a real problem.** `b = 0.25` whether you compute it in credit units or R. The R *basis* only shows up in `c_R`, which is why a card can look fine and still be fee-dead.
2. **`p* = sl/(tp+sl)` is the same formula.** If a `p*` surprises you, recompute it as the stop's share of the total range. It is usually obvious that way.
3. **The ceiling on `L` is deliberate.** `ln(N)/ln(1/(1−p))` is the expected maximum; rounding down would understate the streak. The raw value is printed beside it so the rounding is auditable.
4. **`p = 0.80, b = 0.25` lands at `E = 0` exactly — and floating point does not.** The engine snaps residues inside `1e-12` to zero, because otherwise an exact break-even card reports `n_req = 3.2e32`. Read the note beside the value.
5. **A negative Kelly is reported, not clipped.** `f* = −0.50` is the criterion saying *do not bet*. Clipping it to zero would destroy the information.
6. **`n_req` is refused when `E ≤ 0`,** with the reason printed. A trade count cannot reveal an edge that is not there.
7. **`se_E = sd/sqrt(n)` is the resolution of the *mean*, not of a trade.** Comparing `E` to `sd` rather than to `se_E` makes almost every card look insignificant.
8. **A `MARGINAL` verdict is worse than a `NEGATIVE` one.** `NEGATIVE` gets abandoned; `MARGINAL` gets traded for years on a rounding error.
9. **Multi-rung scaling worsens the fee ratio by `rung_split²`** — the fee multiplies by `N`, the banked cash divides by `N`.
10. **The three-rung extra fee equals the opening round-trip fee** for a 4-leg structure: a `$5.20 cost` from `(3−1) × 4 × 0.65`, identical to `4 × 2 × 0.65` `[COMPUTED]`. That is not a coincidence, it is arithmetic.
11. **The high-p corner permits *larger* risk per trade, not smaller.** `R_max` is `D_tol/(L × safety)`, and `L` falls as `p` rises: 3.33% at `p = 0.80` versus 1.03% at `p = 0.35` `[COMPUTED]`. This is counterintuitive and it is the whole reason the two corners cannot share a size.
12. **Bonferroni is conservative and that is the right way to be wrong.** Correlated cycles produce an FWER *below* the independence figure; over-correcting beats believing a searched result.
13. **`E[max_m]` at `m = 2` is `1/sqrt(pi) = 0.5642`** — a known closed form, and a check that the order-statistic integral is being evaluated correctly.
14. **Pooling cohorts inflates `sd` and deflates `E` simultaneously.** A pooled book can be unmeasurable while one of its components is genuinely positive.
15. **A tighter stop changes `p`.** The stop's job is to set how often the trade loses. A new stop is a new card needing a new cohort tag.
16. **`--credit/--width` and `--tp/--sl` can disagree on `R` and still agree on `b`.** `b` is scale-free; `R` is not. Only `c_R` notices.
17. **The engine emits LF on every platform,** including when stdout is redirected on Windows. A CRLF diff would otherwise make an identical run look different.
18. **`verify-skill.sh` fails on an orphaned reference file.** Every file in `references/` must be linked from SKILL.md; a new reference that is not linked breaks the gate.

**Complete when** every gotcha above has been checked against the engine's actual behaviour rather than taken on trust.

---

## Anti-Hallucination

**These four rules are blocking. A response that violates any of them is wrong regardless of its arithmetic.**

- **Admit uncertainty.** A hypothesised `p` is an input, not a measurement. Every `p` in this skill is an estimate with sampling error, and the error is frequently larger than the edge. Say which inputs are measured, which are estimated, and which are invented.
- **Flag your knowledge cutoff.** The option mechanics used here — two tickets per leg per round trip, the 100-share standard contract multiplier, assignment and exercise being fee-bearing events — are long-standing listed-option conventions, referenced as of the author's checkout. Product listings, fee schedules, margin requirements and exchange rules change; verify them at the source. Never present a remembered schedule as current.
- **Never guess security.** This skill prices a *payoff*, not a security. It selects no strike, no expiration and no instrument. If a question requires a security to be named, defer to `options-strategist` or `trading-decision-data-catalogue`.
- **Tag every number `[VERIFIED]`, `[COMPUTED]`, `[ESTIMATED]` or `[ILLUSTRATIVE]`.** `[VERIFIED]` means it came from a named source and that source was consulted. `[COMPUTED]` means the formula is shown inline. `[ESTIMATED]` means the derivation is shown. `[ILLUSTRATIVE]` means it was invented. An untagged number is removed, not softened.

**Never do any of the following:**

- Claim or imply that any strategy is profitable, guaranteed, safe, or likely to work. A `POSITIVE` verdict is arithmetic on inputs; state it as a conditional on `p` and `b`.
- Invent a statistic, a benchmark, a citation, a backtest result, a market return or a comparison to an index. This skill has no benchmark, no risk-free rate and no market data, and it prints none.
- Quote a number from `examples/logs/synthetic-options-log.csv` as a finding about any instrument, strategy, volatility regime or period. The fixture is SYNTHETIC / ILLUSTRATIVE and the label travels with it.
- Present a `p` from memory as a measurement. A win rate without `n` and `se_p` is neither.
- Present a cycle result at fewer than `n_req` trades as evidence. Mark it a peek.
- Attribute a cycle's result to a lever when two levers moved.
- Answer a structure-selection, leg-surgery, position-exit-ordering, contract-count, portfolio-Greek or execution question from this skill. Defer it by name.

**If a claim cannot be verified, say which part is unverified.** A statement built on an input that could not be confirmed has an unverified foundation even when every step of arithmetic above it is correct. **Complete when** every number in the response carries a tag and every claim about profitability is a conditional.

---

## Deliberate Practice — Advanced Drills

<!-- DEEP: 10+min -->
**Drill 1 — the reverse card (25 min).** Take a card you currently trade. Compute its `b` from the *actual exit orders*. Compute `p*`. Then compute the payoff you would need to reach your *measured* `p`: `b_required = (1 + c_R − p)/p`. Ask whether any structure you trade reaches it. If not, you have found the reason the book is flat.

**Drill 2 — the fee audit (30 min).** For every card in the book, compute `cost_per_trade = fee × legs × 2` and `c_R` at the real structure size. Rank the cards by `c_R`. The worst `c_R` is almost never the card you were worried about.

**Drill 3 — the streak rehearsal (20 min).** Compute `L` for your `p`. Write out a `L`-loss sequence as a table of cumulative drawdown at your current size. If the number is unacceptable, the size is wrong now, not at the moment the streak arrives.

**Drill 4 — the peek audit (15 min).** Count how many times you checked a cohort's performance in the last month. That count is your true `m`. Apply `alpha_adjusted = 0.05/m` retroactively and see what survives.

**Drill 5 — the rung test (15 min).** For every structure you scale out of, compute the threshold `rung_split × legs × fee_per_contract` and compare it to the structure's current value. Count how many of your rungs were fee-negative.

**Drill 6 — the one-lever log (30 min).** Write down your last ten changes to live cards. Count how many cycles moved exactly one lever. This number correlates more strongly with eventual profitability than any indicator you can compute.
