# Margin Regimes and Forced Liquidation

Margin is not a rate the holder chooses; it is a **claim on the position** that a third party can
enforce on a date. This file states the regimes, the numbers, the clocks, and the arithmetic that
tells a holder where the call actually is.

## §1 — The Regimes

| Regime | Applies to | Initial requirement | Maintenance | Call clock |
|---|---|---|---|---|
| **Cash** | Cash accounts | 100% of cost | 100% (no lending) | Settlement date; good-faith violations freeze payment privilege for 90 calendar days |
| **Reg T** (standard margin) | Most margin accounts | **50%** of market value long; **150%** of market value short | FINRA Rule 4210(c) — see §2 | Reg T deficiency: **3 business days** |
| **Portfolio Margin (PM)** | Eligible accounts, broker-approved | Theoretical stress-test based | Stress-based, per-strategy | Deficiency must be cured in **3 business days** or the member liquidates |
| **SPAN / exchange-derived** | Futures and futures options | Exchange-determined performance bond | Exchange-determined | Exchange/broker rules |

**Sources:** Reg T initial margin — 12 CFR 220.12(a) and (c)(1). Reg T payment period — 12 CFR 220.2,
220.4(c)(3)(i). Maintenance — FINRA Rule 4210(c). Portfolio-margin cure — FINRA Rule 4210(g)(10)(A).

## §2 — Maintenance Margin, Exactly as the Rule States It

| Position | Maintenance requirement (FINRA Rule 4210(c)) |
|---|---|
| Long, margin-eligible equity | **25%** of current market value |
| Long, **non-margin-eligible** equity | **100%** of current market value |
| Short, price **< $5.00** | greater of **$2.50 per share** or **100%** of current market value |
| Short, price **≥ $5.00** | greater of **$5.00 per share** or **30%** of current market value |

**Source:** FINRA Rule 4210(c). These are the numbers; everything else in this file is arithmetic on
them.

Two of those rows are worth staring at. A long position in a non-margin-eligible security carries a
100% maintenance requirement — it is, for margin purposes, a cash-only asset, so it contributes
nothing to the account's cushion. And a short below $5.00 carries a requirement equal to the **full
market value** of the short, which is what makes low-priced short positions behave like
unlimited-risk instruments.

## §3 — Where the Call Actually Is [COMPUTED]

The requirement is a **percentage of market value**, and market value falls with the price. So the
requirement shrinks while equity falls faster.

**Long-only, maximum Reg T leverage.** With market value `MV` and debit `D`, `equity = MV − D` and
`requirement = 0.25 × MV`. A call occurs when:

```
MV − D < 0.25 × MV
0.75 × MV < D
MV < D / 0.75 = 1.3333 × D
```

At maximum Reg T leverage `MV = 2 × D`, so the call lands at `MV = 1.3333 × D` — a decline of
`(2 − 1.3333) / 2 = 33.33%` from the purchase price. At that point equity is
`1.3333D − D = 0.3333D`, which is `0.3333D / 1.3333D = 25%` of market value — the maintenance
requirement itself, as it must be at the moment of a maintenance call, and not 16.67% of it (the
denominator is market value, not the debit). Read that as a number: **a maximally
leveraged Reg T long account is on a maintenance call after a one-third decline** — not after the
account is wiped out, and not after the 50% initial margin is exhausted:

```
BUY            $20,000 of stock with $10,000 cash + $10,000 debit
MAINTENANCE    0.25 × $20,000 = $5,000      equity $10,000 → cushion $5,000
CALL AT        MV = $10,000 / 0.75 = $13,333.33
               decline from $20,000 = 33.33%
               equity at call = $13,333.33 − $10,000 = $3,333.33 = 25% of MV
```

**Short-side arithmetic.** Short 500 shares at $40.00:

```
SHORT MARKET VALUE        500 × $40.00 = $20,000
REG T INITIAL             150% × $20,000 = $30,000      [VERIFIED — 12 CFR 220.12(c)(1)]
PROCEEDS HELD             $20,000 (the short sale proceeds stay in the account)
ADDITIONAL DEPOSIT        $30,000 − $20,000 = $10,000
FINRA 4210(c) MAINTENANCE greater of $5.00/share × 500 = $2,500  vs  30% × $20,000 = $6,000
                          → $6,000 binds
```

Short 5,000 shares at $3.20 (below $5.00):

```
SHORT MARKET VALUE        5,000 × $3.20 = $16,000
FINRA 4210(c) MAINTENANCE greater of $2.50/share × 5,000 = $12,500  vs  100% × $16,000 = $16,000
                          → $16,000 binds — the requirement IS the market value
```

All three blocks are [COMPUTED] from the §2 maintenance table and the 150% initial short
requirement. They are the reason a short book's real constraint is the *price at which the cushion
disappears*, not the size of the position.

## §4 — The Call Timeline, and the Ceiling That Is Not an Entitlement

| Event | Clock | Source |
|---|---|---|
| Reg T deficiency | **3 business days** from the trade (settlement + 2) | 12 CFR 220.2, 220.4(c)(3)(i) |
| Firm's outer bound for margin / mark-to-market calls | "as promptly as possible and in any event **within 15 business days**" | FINRA Rule 4210(f)(6) |
| Portfolio-margin deficiency | cure in **3 business days** or the member must liquidate | FINRA Rule 4210(g)(10)(A) |
| Intraday-margin (day-trading) deficiency — see §5 | set by the member's intraday-margin schedule under **FINRA Rule 4210(d)(2)**; the old PDT special-call clock is **superseded** | FINRA Regulatory Notice 26-10; FINRA Rule 4210(d)(2) |
| Liquidation trigger | if the call is not met, the firm **must** liquidate; **no action is required if the deficiency is ≤ $1,000**; **no advance notice is required** | 12 CFR 220.4(d) |

**State this plainly every time the 15-day figure appears: it is a ceiling on the member firm, not a
grace period for the customer.** A holder who reads "15 business days" as their own window has
misread the rule in the direction that costs money. There is no rule requiring the firm to warn
before it liquidates, and the rule that governs liquidation says the firm *must*, not *may*.

The `$1,000` de-minimis figure is a floor on the firm's obligation to act, not on the holder's
obligation to cure. A $1,000 deficiency that is left standing becomes a larger one on the next down
day, and the de-minimis exemption does not survive it.

## §5 — Day-Trading Margin, After the 2026 Change — and the Cash-Account Freeze

**The rule changed in 2026, and this is the part of the file most likely to be read against a stale
broker page.**

- **Current framework — FINRA Rule 4210(d)(2)**, the intraday-margin requirements for day trading, as
  adopted by **FINRA Regulatory Notice 26-10**. That notice **replaced the day-trading margin
  requirements in their entirety** — including the day-trade count used to designate a "pattern day
  trader" and the **$25,000** minimum equity. SEC approval **2026-04-14/15**; **effective
  2026-06-04**, with phase-in through **2027-10-20**. **Source:** FINRA Regulatory Notice 26-10;
  FINRA Rule 4210(d)(2).
- **The old regime is superseded, not merely amended.** In the current FINRA Rule 4210, **(f)(8) is
  "Special Initial and Maintenance Margin Requirements"** — it is not PDT — and the current rule text
  contains no "pattern day" string at all. Anything still framed as *4 or more day trades in 5
  business days → $25,000 minimum equity → a 5-business-day special maintenance call → a 90-day
  cash-available restriction* is describing the **pre-2026-06-04** rule.
- **Historical line, kept deliberately:** a broker page or a summary that still describes the
  4-in-5 count and the $25,000 minimum is **not wrong about what the rule used to be; it is wrong
  about what the rule is.** Read the date on the page before acting on it.
- **Verify with your broker — this changed in 2026.** The operative intraday-margin schedule is now
  the member's, and the phase-in runs to 2027-10-20, so the number that binds your account is the
  member's current schedule. Ask for it in writing and record the read date `[BROKER-VERIFIED]`.

**Cash-account good faith (12 CFR 220.8(c)(1)):**
- Buying with unsettled proceeds is a free-riding / good-faith violation.
- Consequence: payment privilege frozen for **90 calendar days**.

Two different 90s lived in the old world — the PDT restriction and the cash-account freeze — with two
triggers and one shared outcome. One of them is gone: the PDT restriction was superseded in 2026. The
cash-account freeze under 12 CFR 220.8(c)(1) remains, and it is the one the holder can still trip
without noticing. It is invisible to a P&L view.

## §6 — Portfolio Margin: What the Research Could and Could Not Verify

This is a place where the honest answer matters more than the tidy one.

- **What the rule text retrieved actually contains** is a **$5,000,000** minimum equity figure, and
  it applies **only to eligible participants trading unlisted derivatives**.
  **Source:** FINRA Rule 4210(g)(4)(C).
- **The widely quoted $100,000 portfolio-margin minimum was not found** in the current FINRA Rule
  4210 text retrieved during research on this skill. **It must therefore be treated as
  broker-set, not regulatory → [BROKER-VERIFIED], and confirmed with the specific broker before it
  is used in any eligibility or capital decision.**
- **Do not present $100,000 as a regulatory requirement.** A user who is told it is a rule will make
  a different decision than one who is told it is their broker's policy — and only the second
  statement is defensible.

What *is* verifiable about the PM regime and matters for risk: a PM deficiency must be cured in
**3 business days** or the member must liquidate [VERIFIED — FINRA Rule 4210(g)(10)(A)]. PM is a
margin *calculation* difference, not a margin *grace period* difference.

## §7 — The Forced-Liquidation Sequence

When a call is not met, the outcome is not negotiated:

1. The firm chooses **what** to sell. It is not obliged to sell the position the holder would have
   chosen, and it is not obliged to sell the worst position first.
2. The firm chooses **when**. There is **no advance notice** requirement in 12 CFR 220.4(d).
3. The firm chooses **how**. A market order in a thin book, or a block worked by the desk — either
   is permitted.
4. The resulting price is charged to the account. The loss is realised, and it is realised without
   the holder's participation.

The only defence against this sequence is the reserve floor in `capital-reserve-and-deployment.md`,
tested **before** every ticket. A reserve computed after a fill is a post-mortem.

## §8 — Failure Modes

1. **Reading 15 business days as the customer's window.** It is the member's ceiling.
2. **Computing the call distance from the initial margin.** The call is at maintenance, and for a
   maximally leveraged long account that is a 33.33% decline, not a 50% one.
3. **Treating the $1,000 de-minimis exemption as a tolerance.** It is a limit on the firm's duty to
   act, not on the holder's exposure.
4. **Assuming PM changes the clock.** It changes the calculation; the cure is still 3 business days.
5. **Quoting $100,000 as a portfolio-margin rule.** The figure retrieved from the rule text is
   $5,000,000 for unlisted derivatives; $100,000 is broker-set.
6. **Forgetting the non-margin-eligible long row.** A 100% maintenance requirement means the position
   contributes no cushion at all.
7. **Sizing a sub-$5 short on the $2.50/share number.** At 100%-of-market-value the requirement can
   be more than five times larger.
8. **Blaming the broker for selling the best asset first.** Brokers sell what is liquid because
   liquidity is what protects them; the defence is the reserve, not an argument.
9. **Ignoring the interaction of a margin call with a wash-sale window.** Curing a call at a loss
   inside ±30 days can disallow the very loss that was meant to fund the cure.
10. **Reading day-trading margin from a pre-2026 page.** The day-trading margin requirements were
    replaced in their entirety **effective 2026-06-04** (FINRA Regulatory Notice 26-10); the old
    4-day-trades-in-5 designation and the $25,000 minimum are superseded, and the intraday schedule
    is now the member's, phasing in to 2027-10-20. Read the current rule and the member's schedule,
    not a summary — **and verify with the broker, because this changed in 2026.**

## §9 — Verification

- [ ] The margin regime is named before any margin number is reported.
- [ ] Reg T and PM figures are both computed where the account is PM-eligible.
- [ ] Call distance is computed at **maintenance**, with the arithmetic shown, not at initial margin.
- [ ] The 15-business-day figure, where used, is labelled a ceiling on the member.
- [ ] The PM minimum-equity figure used is labelled broker-set, and the broker has been asked.
- [ ] Any day-trading margin statement names the **current** framework (FINRA Rule 4210(d)(2);
  FINRA Regulatory Notice 26-10, effective 2026-06-04), labels the $25,000 / 4-in-5 regime
  **superseded**, and carries the instruction to verify with the broker.
- [ ] Margin figures are verified against the broker's own platform before a decision depends on them.
