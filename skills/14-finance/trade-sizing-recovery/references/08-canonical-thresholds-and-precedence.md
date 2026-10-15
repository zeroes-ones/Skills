# Canonical Thresholds, Precedence & the Two Ladders — Derivations

Companion to `SKILL.md` (Canonical Threshold Table, Drawdown-Linked Size Ladder, Winner-Add Sizing).

This file holds the *derivations* behind the numbers in `SKILL.md`. The numbers themselves live in
`SKILL.md` so an agent can act on them without loading this file. Nothing here is a new threshold:
every level below is either taken from an existing skill in this library or computed from one.

---

## 0. Ownership map — who owns which artifact

| Artifact | Owner | What it means here |
|---|---|---|
| The **numbers** (TP rungs, loss cuts, DTE forces) | `trade-sizing-recovery` (this skill) | The Canonical Threshold Table in `SKILL.md` is the tie-breaker |
| The **order** of exit events on a live position | `options-position-lifecycle` | It sequences; it does not re-price |
| Calendar / expiry forces, pin and assignment windows, aggregate Greeks | `options-risk-engineer` | Overrides every number in the table |
| The **reserve floor** (margin headroom + book open-risk budget) | `options-risk-engineer` | Never restated, shrunk or re-derived here |
| Structure choice at entry | `options-strategist` | Supplies the family; the table supplies the exits |
| Execution of the exit | `swing-options-trader` / the broker | Executes the size and the level it is given |

A number without an owner is a number that gets negotiated in the moment. Every row of the table has
exactly one owner: this skill.

---

## 1. The five conventions, side by side

The library currently states five exit conventions. None of them is wrong; none of them
was written as the arbiter — and only four of the five are numeric at all.

| # | Source | What it says | Unit it is stated in |
|---|---|---|---|
| 1 | `trade-sizing-recovery` (this skill) | TP rungs ≥1.8× and 2.5–3×; sell in thirds; LEAP 1.5–2×; triage bands −30/−40/−50/−70/−90% | multiple of debit paid |
| 2 | `options-strategist` (`references/profit-taking-and-trimming.md`, `references/adjustment-and-exit-rules.md`) | credit spread 50% of max credit; iron condor 25% of max credit; debit spread 50%/75% of max profit; calendar 25–50%; butterly 30–50%; CSP/CC 50–80%; stop 2× credit (spreads), 3× credit or 200-SMA (naked put), 100% of debit (debit spread); 21-DTE and 7-day rules | % of max credit, % of max profit, × credit |
| 3 | `swing-options-trader` | credit spreads close at 50% of max profit; iron condors at 25% of wing width; debit spreads cut at 50% loss; long calls/puts take profit at 100%+ and cut at 40% loss | % of max profit, % of wing width, % of premium |
| 4 | `leaps-strategist` | Δ ≥ 0.95 → take profit or roll up; DTE < 90 → roll-or-close; extrinsic above threshold → close; 2+ PMCC debit rolls → close; DTE < 180 with no thesis → time exit | delta, DTE, extrinsic |
| 5 | `options-position-lifecycle` (`references/tp-sl-precedence-and-arbitration.md`) | **A precedence order only**: desk breaker → calendar/expiry force → plan rung declared at entry → structure-family threshold → discretionary override. It restates **no rung numbers** — by design, so that it cannot drift against source 1 | rank order (not a price) |

**Two kinds of conflict, and only one of them is a number.** Sources 1–3 disagree about *numbers
and units* (source 3's "% of wing width" is the 5× trap worked in §3). Source 4 does not disagree
about a number at all: its exits are stated as delta / DTE / extrinsic triggers, so there is no
price rung for source 1 to overrule — calling it a fifth *number* would make the reconciliation
vacuous. Source 5 disagrees about **order**: it is a rank order over the same live position, and
left alone it would outrank source 1's row by default.

Five sources, three kinds of thing (a number, a trigger type, an order). The table in `SKILL.md`
converts the numbers into the unit each family trades in and fixes which of them binds; the
precedence rule beneath it fixes what happens when a rank order and a number disagree. Because
source 5 is order-only and holds no numbers, there is nothing in it for this skill to re-price —
which is exactly why the two can be reconciled instead of one being discarded.

---

## 2. Reconciliation — every sibling number mapped to a canonical row

| Sibling rule | Canonical row it feeds | Same, or changed? |
|---|---|---|
| credit spread "close at 50% of max credit" (2, 3) | Credit vertical, rung 1 = 50% of max credit | **Same.** The most-repeated number in the corpus; keep it |
| iron condor "25% of max credit" (2) | Iron condor, rung 1 = 25% of max credit | **Same** — and it beats (3)'s phrasing, see §3 |
| iron condor "25% of wing width" (3) | Iron condor, rung 1 | **Changed:** read as a dollar profit target it is 5× larger and usually unreachable (§3) |
| debit spread "50% then 75% of max profit" (2) | Debit vertical, rungs 1–2 | **Same** |
| debit spread "cut at 50% loss" (3) | Debit vertical, loss cut | **Changed:** the level rule binds first; the premium backstop is −40% of debit, uniformly with long premium |
| long option "cut at 40% loss" (3) | Long call/put, loss cut = −40% of debit | **Adopted as the family backstop** |
| debit spread "stop = 100% of debit paid" (2) | Debit vertical | **Reclassified:** that is the structural worst case, not an actionable stop. Restating it as a stop is how a −100% loss gets a plan attached to it |
| straddle/strangle "25% of debit paid" as a stop (2) | Long premium backstop | **Changed:** 25% is tighter than this file's −30% triage floor and would exit before the review band ever fires. Long premium uses −40%, reviewed at −30% |
| credit spread "2× credit" (2, 3) | Credit vertical, loss cut | **Same.** Both sources agree; it is the family's one hard stop |
| naked put "3× credit or below 200-SMA" (2) | CSP, loss cut | **Same** |
| covered call "50–80% of premium" (2) | CSP/CC, rungs 1–2 | **Same** |
| calendar "25–50% of max profit" (2) | Calendar/diagonal, rungs 1–2 | **Changed:** max profit is not well defined on a two-expiry structure. Re-expressed as +25%/+50% of debit |
| butterflies "30–50% of max profit" (2) | Iron butterfly, rung 1 = 30% of max credit | **Adopted** |
| LEAPS "Δ ≥ 0.95" and "DTE < 90" (4) | LEAPS/PMCC, rung 2 and time force | **Not a number to reconcile.** Delta and DTE are trigger *types*, not price rungs. Source 4 is the only source that states the LEAP exits in delta/DTE/extrinsic, so there is nothing numeric here for the table to overrule — the row adopts the triggers and states rung 1 in R-multiples |
| LEAPS "1.5–2×" (1) | LEAPS/PMCC, rung 1 = +50% of debit | **Same**, restated in R-multiples so it can be compared with rung 2 |
| "sell in thirds" (1) | All families | **Changed:** a 3-lot construction, not a universal rule (see `references/05-scale-out-ladders.md`, which already gives 1-lot and 2-lot variants) |
| 21-DTE close for all short premium (2, 3) | Time/DTE force, every short-premium family | **Same.** Universal across the corpus — the strongest consensus in the library |
| triage bands −30/−40/−50/−70/−90% (1) | Review triggers, not exits | **Same, role clarified:** a band forces a disposition; a table row decides which disposition |

---

## 3. Unit conversion — the step that makes the numeric conventions comparable

The corpus mixes three units that look alike and are not:

```
% of wing width      = (% of max credit) x (credit / width)
% of max credit      = (% of wing width)  x (width / credit)
R-multiple (debit)   = (exit - entry) / debit paid
% of max profit      = (mark - debit) / (max profit)
% of max profit      = R-multiple / (width/debit - 1)      # debit verticals only
```

**Worked: the 5× gap between two sibling rules.** A 10-lot condor with $10-wide wings collecting
$2.00 of credit per contract.

```
credit per lot      = $2.00 x 100                    = $200
total credit        = $200 x 10 lots                = $2,000      (= max profit)
wing width in $     = $10.00 x 100 x 10 lots        = $10,000     (= distance from credit to max loss)
options-strategist  : 25% of max credit             = 0.25 x $2,000 = $500 profit
swing-options-trader: 25% of wing width            = 0.25 x $10,000 = $2,500 profit
conversion          : 25% of max credit in wing-width terms
                      = 25% x ($2.00 / $10.00)      = 5% of wing width
```

The $2,500 target is 125% of the position's maximum profit and therefore **can never fire**. A rule
that cannot fire is not a rule; it is a reason to hold a condor into the last three weeks and eat the
gamma. Convert to % of max credit first, then compare — the arithmetic is the whole argument.

The same conversion trap sits in "sell in thirds": thirds presuppose a 3-lot position. On a 1-lot
position, rung 1 is a full exit; on a 2-lot position it is a half. Nothing about the rung *level*
changes.

---

## 4. Derivations

### 4.1 Why an add is capped at ⅓ R

```
R      = the ORIGINAL risk unit (max loss as sized at entry)
band top for the momentum-fly and debit-vertical rows   = 1.5% of trading capital
hard per-idea ceiling in references/01-sizing-bands.md   = 2.0% of trading capital
solve   R_max(1.5%) + R_max/n <= 2.0%   ->   1.5/n <= 0.5   ->   n >= 3
therefore the largest admissible add = 1/3 R
```

Check each candidate fraction against the ceiling:

| Add fraction | Combined risk after the add | Inside the 2.0% ceiling? |
|---|---|---|
| 1/2 R | 1.5% + 0.75% = 2.25% | NO |
| 1/3 R | 1.5% + 0.50% = 2.00% | YES — exactly at the ceiling |
| 1/4 R | 1.5% + 0.375% = 1.875% | YES, with slack |

**Corollary that matters:** a position already sized at the 2.0% long-dated-single ceiling has no
admissible add at any fraction — 2.0% + 2.0%/n > 2.0% for every n > 0. **No adds on a 2.0% LEAP.**
The only legal way to increase exposure there is a new, separately-sized idea.

### 4.2 Why the drawdown breakpoints sit at 5 / 10 / 15 / 25

Anchor: the streak arithmetic already in this skill's `references/02-expectancy-math.md`, computed
at the 1.5% per-trade band.

```
drawdown after k consecutive losses at 1.5% risk each = 1 - (1 - 0.015)^k
```

| Row | k (consecutive losses at 1.5%) | Probability of that streak at p(win) = 0.45 | Read |
|---|---|---|---|
| −5% | 3.4 | 0.55^3.4 ≈ 13% | One bad week at disciplined size. Trim, don't stop |
| −10% | 7.0 | 0.55^7 ≈ 1.5% | Past the 1-in-20 streak. The hand is statistically cold |
| −14.0% | 10 | 0.25% | The 1-in-400 streak the file already tabulates |
| −15% | 10.8 | 0.55^11 ≈ 1 in 700 | Beyond what bad luck explains at disciplined size |
| −25% | 19.0 | 0.55^19 ≈ 1 in 86,000 | **Not luck.** A broken rule, hidden correlation, or a gap |

A −25% book at disciplined 1.5% sizing has a 1-in-86,000 explanation. Treating it as "a bad run" is
the failure mode the ladder exists to prevent — at that depth the correct action is zero new risk
until the cause is named, not a bigger recovery trade. All figures `[COMPUTED]` from the formula
above; the probabilities match the binomial table already in `references/02-expectancy-math.md`.

### 4.3 Why 21 DTE and 15 DTE — and what the escalation factors actually are

**The escalation factors previously quoted here were wrong.** "2× gamma from 21→14 DTE, 5× from
14→7, 10× from 7→0" is not the Black–Scholes scaling. At the money with r ≈ 0 the ATM gamma of a
fixed strike scales as **Γ ∝ 1/√T** [COMPUTED]:

```
Γ_ATM = φ(d1) / (S · σ · √T)          d1 = σ√T / 2

21 → 14 DTE :  Γ ratio = √(21/14) = 1.22×      (not 2×)
14 →  7 DTE :  Γ ratio = √(14/7)  = 1.41×      (not 5×)
 7 →  0 DTE :  √(7/0) → diverges in the reduced form; in practice it is bounded
               by the strike/spread grid, but it is not a finite "10×"
45 →  7 DTE :  √(45/7)  = 2.54×
45 →  5 DTE :  √(45/5)  = 3.00×
```

So gamma **doubles when the remaining life is quartered**, not halved: 45 → 22.5 → 11.25 → 5.6 →
2.8 DTE is one doubling per step. The number that *does* double per halving of remaining life is
**gamma per dollar of premium still at stake**, and it is that ratio — not Γ/|Θ| — that the last
three weeks is about:

```
ATM option value  V_ATM ≈ S · σ · √(T/2π)
Γ_ATM / V_ATM = φ(0)·√(2π) / (S²σ²T) = 1 / (S²σ²T)   [COMPUTED, φ(0)·√(2π) = 1 exactly]

45 DTE: 1/(S²σ²·0.1233)      → 1.00×  (the entry)
22.5 DTE: 1/(S²σ²·0.0616)   → 2.00×
11.25 DTE: 1/(S²σ²·0.0308)  → 4.00×
 5.6 DTE: 1/(S²σ²·0.0154)   → 8.00×
 2.8 DTE: 1/(S²σ²·0.0077)   → 16.0×
```

**What this does and does not justify.** It justifies the *shape* of the 21-DTE rule: from a
45-DTE entry, the 2× / 4× / 8× / 16× rungs of gamma-per-premium land at ≈22 / ≈11 / ≈6 / ≈3 DTE, and
the zone labels the desk already uses (14–21 plan, 7–14 gamma acceleration, 3–7 active, 0–3 critical)
are a rounding of those rungs onto the weekly/monthly listing grid. It does **not** justify the exact
numbers 21, 14, 7 and 3 as constants, and it does not say "each halving of remaining life is one
risk-doubling" in any absolute sense — that statement is only true of the ratio above. Limitations,
stated plainly: the reduced form is exact only at the money with r = q = 0, it assumes a fixed strike
and a constant σ, it ignores the vega/vol-of-vol term that dominates once the option is far OTM, and
the "premium still at stake" denominator is the ATM value, not a specific position's mark. Recompute
Γ/V from the position's own Greeks — the *ladder shape* is robust; the level is not.

- **21 DTE on short premium** — the universal corpus consensus (`options-strategist`'s 21-day rule,
  `swing-options-trader`'s time stop), and the T₀/2 rung of the ladder above. Direction is not in
  dispute: the last three weeks is where a short-premium winner's remaining credit stops paying for
  its gamma.
- **15 DTE on long premium** — this skill's own existing triage band already cuts at "DTE < 15d"
  (theta wall). The table adopts the existing number rather than inventing a second one.
- **90 DTE on LEAPS** — from `leaps-strategist`; the roll-or-close decision there also requires
  IV rank < 40 and trend > 40, which is why the table calls it a *decision*, not a close.

### 4.4 Why 1.8× and 2.5× with a −40% backstop

```
break-even win rate at rung 1  = 0.40R / (0.80R + 0.40R) = 33.3%
break-even win rate at rung 2  = 0.40R / (1.50R + 0.40R) = 21.1%
break-even win rate, blended   = 0.40R / (1.03R + 0.40R) ≈ 28%   (equal thirds, average exit +103%)
```

All three sit comfortably below the 0.35–0.45 honest hit-rate band already tabulated in
`references/02-expectancy-math.md`. A 1.8× rung with a −40% backstop needs only a 33% win rate; a
rule that needs 45%+ to break even is a rule fitted to desire. `[COMPUTED]`.

---

## 5. Precedence, worked arbitrations

Order — one order, the highest-ranked rule that applies wins:

1. **Desk circuit breaker** (drawdown row, margin breach, reserve floor, closed event gate)
2. **Calendar / expiry force** (DTE ≤ 21 short premium, ≤ 15 long premium, ≤ 90 LEAPS, pin/assignment windows)
3. **Plan-level override declared at entry** (a rung written on the ticket before the fill)
4. **The Canonical Threshold Table's family row** (the default)

A single rank order is only useful if it is written once. This is the only statement of the order in
this skill; the list in `SKILL.md`, Decision Tree 4, and every case below use this order and no
other.

**Convention on units and rounding, stated once.** Every dollar figure in this file and in
`SKILL.md` is a **per-position** figure unless it is written as a per-contract number, and every
per-contract figure is `premium × 100 shares` unless the contract multiplier is named. Dollar
figures are rounded **down** to the whole dollar: the tables are caps, so a rounded-up cap would
itself be a breach. That is why `references/01-sizing-bands.md` prints $37 where 0.75% × $5,000 is
$37.50, and $187 where 0.75% × $25,000 is $187.50 — floor, never nearest.

**When the table and an entry-time override disagree, the override wins — inside two limits.**
(a) *Timing*: the override must have been declared before the fill; a number chosen after entry is
not an override, and the table's row governs. (b) *The loss cut*: the override may be tighter than
the row on every level and looser than the row on a TP rung or a time stop, but it may never be
looser than the row's **loss cut**. Tighter override → override binds. Looser override on a rung →
override binds. Looser override on the loss cut → the row's loss cut binds and the override is
amended on the ticket before the fill. Anything still disagreeing after (a) and (b) is a unit error:
convert both into the family's unit (§3) and re-read; if they still differ, the higher-ranked rule
binds. Never average, and never carry both numbers for one position. Cases C and D below are worked
instances of exactly this test.

**Case A — the two agree, so act.** A credit spread collected $1.50, now marks $0.75, on a
**10-lot position** (10 contracts × 100 shares). `options-strategist` says close at 50% of max
credit; `swing-options-trader` says close at 50% of max profit. Same number, same unit, same action:
**close, and book $750 profit** — that is `$0.75 × 100 shares × 10 lots = $750`, i.e. **$75 per
contract**, and it is a per-position figure. (Per-contract arithmetic is shown because the two
readings only coincide when the lot count is explicit: 50% of a $1.50 credit is $0.75 per share, and
without the ×100 × 10 the same sentence reads as $0.75 — a 1,000× error.) Do not look for a third
opinion.

**Case B — the two disagree, so the table arbitrates.** The condor in §3 marks at 25% of max credit.
The table's row fires at $500 profit and books it. The other reading ($2,500) never fires. The
trader who applies the wrong unit holds a condor into the 21-DTE force and gives the credit back.

**Case C — an override meets the clock.** A plan declared at entry says "hold this credit vertical
to 80% of max credit." At 18 DTE the position is at 60% and still working. The override is valid
(declared before the fill, and tighter-than-the-row is not even at issue here — it is looser than
the row's 50%-of-max-credit rung, which is allowed). It still does not survive the calendar:
**rank 2 (the expiry force) outranks rank 3 (the override)**, so the position **closes at 21 DTE**,
override notwithstanding. An override can change the *price* at which you exit; it cannot buy an
extension of the calendar.

**Case D — the override the table will not accept.** After a position moves against you, you
"declare" a looser stop that keeps it alive. That is not an override for two independent reasons:
rank 3 requires the declaration **before the fill**, and even a valid override may never be looser
than the table's loss cut. Two failures, one conclusion — the table's loss cut binds.

**Case E — a legitimate entry-time override that is looser on a rung and tighter on the cut.** A
debit vertical's row says 50% of max profit with a −40%-of-debit backstop. At entry the trader writes
"take 70% of max profit; cut at −30% of debit." Rank 3 applies: the override binds on both, because
it is *tighter* on the loss cut and the row sets no ceiling on rung tightness in the other direction.
This is the case the order exists to make mechanical instead of a debate.

---

## 6. Regime behaviour of both ladders

| Regime | What the options book looks like | Drawdown row typically engaged | What breaks if the ladder is ignored |
|---|---|---|---|
| **Bull market / sustained uptrend** | Long premium works; short premium is capped early by the 50% rungs; streak ladder usually the binding constraint | 0 to −5% (ladder idle) | Complacency: the streak ladder steps up while correlated longs pile into one theme |
| **Correction (−5% to −10% index)** | Short-premium wings tested; long premium round-trips; a 3–5 session pullback parks a 1.5%-sized book near −5% to −10% | −5% to −10% (0.75×, ≤4 concurrent) | A "buy the dip" recovery funded from an unfreed risk budget turns a trim into a full stop |
| **Bear market / sustained downtrend** | Premium-selling edge improves but wings get breached; long premium decays even when directionally right | −10% to −25% (0.50× then 0.25×) | Climbing back on a V-bounce: the restart condition is *sessions above the level*, not a green candle |
| **Crash / tail event (2008-style, March-2020-style gap, black swan)** | A single overnight gap puts every short-premium position at or through its max loss; the book can cross three rows in one session | worse than −25% → 0.00×, manage-only | Compounding one crash with one oversized recovery trade. This is the scenario the 0.00× row is written for |

---

## 7. Failure-mode register

| Failure mode | Trigger / how you detect it | Consequence | Counter |
|---|---|---|---|
| **Open-mark blindness** | Drawdown computed from closed trades only; an unclosed position sits at −20% of cost | The book is deeper in drawdown than the ladder thinks; size stays at base | Compute drawdown from closed P&L **plus open marks**; deposit-adjusted |
| **Restart by one lucky session** | A single gap-up restores the equity level and the operator calls the drawdown over | Size returns to base while the cause is unaddressed | Restart needs sessions above the level **and** N closed trades at the reduced size |
| **Per-account ladder drift** | Two accounts, one ladder each; the deeper account's multiplier is not applied to the fresh one | The book sizes off its best-performing fragment | One ladder per **book**, where the book is the sum of the accounts |
| **Deposit mistaken for recovery** | Peak equity not adjusted for cash flow | Drawdown silently resets to zero on a deposit | Adjust peak and current equity by the same amount |
| **Recovery funded from the reserve** *(worst case)* | The plan needs maintenance-margin headroom it does not have | Margin call converts a recovery plan into forced liquidation | The reserve floor is `options-risk-engineer`'s; while it binds, the answer is manage-only |
| **Add dressed as a scale-in** | An add after a loss, after a thesis break, or on short premium | Averaging down with extra steps | Legality is `options-position-lifecycle`'s call; size is ⅓R or nothing |
| **Rule shopping** *(edge case)* | The same position is quoted at four different TP levels across four skills, changed daily | Whichever rule is convenient that morning wins; rungs drift away from price | One table, one unit, written on the ticket at entry |

---

## 8. Known limitations — what would falsify this

- The threshold levels are **conventions anchored to stated arithmetic**, not measured constants of
  nature. §4 shows the break-even win rates and the streak arithmetic they are derived from; if your
  measured hit rates or loss distribution differ materially from the band in
  `references/02-expectancy-math.md`, the derived rungs move with them.
- The drawdown breakpoint *counts* come from consecutive-loss arithmetic. A book whose losses are
  **correlated** (three momentum longs that are one bet) reaches a −15% drawdown with far fewer than
  11 losses — which is why the counter for the deep rows is "name the cause", not "wait it out".
- The ⅓R add cap is derived from this library's own 1.5%/2.0% band arithmetic. If a trader's band
  differs, re-solve `R_max + R_max/n ≤ ceiling` rather than importing ⅓.
- Nothing here is a prediction. Past streak frequencies are not guarantees of future ones, and a
  positive expectancy does not make any single trade positive.
- This skill does not verify fills, quotes, or OI. Every input it consumes is either exchange-reported
  or supplied by the owning skill, and its timestamps matter more than its precision.

---

## 9. Sources

- **[VERIFIED]** The OCC's *Characteristics and Risks of Standardized Options* is the authoritative
  disclosure document for US-listed options, and a standard equity option contract carries a
  100-share multiplier — which is why every "per contract" figure here is premium × 100.
- **[VERIFIED]** Regulation T is the Federal Reserve's margin regulation setting initial margin for
  non-portfolio-margin retail accounts; the same statement is made in this repo's
  `options-risk-engineer/references/margin-requirements.md`.
- **[VERIFIED]** Open interest and bid/ask prices are exchange-reported per option series (CBOE and
  the other US options exchanges publish them); broker screens can lag the exchange. Liquidity
  claims in this file are therefore sourced to the exchange, not to a broker display.
- **[VERIFIED]** Exercise deadlines are set under OCC rules; brokers typically impose an earlier
  instruction cut-off than the exchange deadline. Confirm the broker's cut-off for any expiring leg.
- Repo-internal conventions reused rather than restated: the 21-DTE rule
  (`options-strategist/references/adjustment-and-exit-rules.md`), the ±1σ theta crossover for
  calendars (`options-strategist/references/calendars-and-diagonals.md`), the IV-rank crossover at
  IV rank 40–50 (`options-strategist/references/pattern-recognition-engine.md`), the LEAPS
  delta/DTE triggers (`leaps-strategist`), and the streak table
  (`references/02-expectancy-math.md` in this skill). The gamma-escalation multiples the strategist
  reference quotes are **not** reused: they are not the Black–Scholes scaling, and §4.3 replaces them
  with the 1/√T derivation plus its stated limitations.
- **[VERIFIED]** The Γ ∝ 1/√T scaling and the Γ/V = 1/(S²σ²T) identity in §4.3 are reduced directly
  from the Black–Scholes at-the-money formulas with r = q = 0 (φ(0)·√(2π) = 1), and were checked
  numerically against a full Black–Scholes evaluation at 45 / 21 / 7 / 3 DTE. Recompute them from
  the position's own Greeks before relying on the level — the file is a derivation, not a quote.
- The four-rank precedence order in §5 is stated once, here. It agrees with
  `options-position-lifecycle`'s rank order for ranks 1–3 and declines that file's rank 5 (a
  post-entry discretionary override) as an override at all; see §5 for why.
