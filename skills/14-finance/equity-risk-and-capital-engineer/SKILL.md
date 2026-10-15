---
name: equity-risk-and-capital-engineer
description: >
  Use when the question is what forces action on an equity position — its clocks, not its
  direction: "margin call — how long before they liquidate?", "my short got recalled", "how much
  cash must I keep in reserve?" — plus index, lock-up and tender dates. Handles the equity time
  axis (T+1 settlement, the Reg T call, the holding period, the wash-sale and short-swing
  clocks), forced liquidation, the day-trading intraday-margin rule that replaced the
  pattern-day-trader minimum (FINRA 4210(d)(2)), short borrow mechanics, the reserve floor and
  its ladder, and corporate actions — merger, split, spinoff. Do NOT use for position decisions
  (equity-position-lifecycle), lots (equity-tax-lot-and-exit-management), sizing
  (portfolio-signal-manager, algorithmic-trader), selection (fundamental-analyst,
  macro-strategist), or futures and options positions — futures SPAN, option exercise
  (futures-options-trader, futures-trader), options margin and Greeks (options-risk-engineer),
  0DTE (intraday-options-trader).
license: MIT
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-10-14
tags:
  - equity-risk
  - margin
  - margin-call
  - forced-liquidation
  - settlement
  - t-plus-one
  - reg-t
  - portfolio-margin
  - intraday-margin
  - short-borrow
  - hard-to-borrow
  - buy-in
  - recall
  - reg-sho
  - threshold-securities
  - concentration
  - liquidity
  - exit-cost
  - capital-reserve
  - buying-power
  - wash-sale
  - short-swing
  - corporate-actions
token_budget: 4500
chain:
  examples:
  - skills/14-finance/equity-risk-and-capital-engineer/examples/backtest
  consumes_from: []
  feeds_into: [equity-position-lifecycle, equity-trading-playbook]
---

# Equity Risk and Capital Engineer

> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Gemini CLI, Codex, Cursor, Kimi Code CLI). No vendor-specific frontmatter fields; every broker example is illustrative and every rule is cited by document.

Equities have no days-to-expiration, and that absence is the trap. An options holder has a countdown printed on the contract. An equity holder believes they have time, and instead they have **clocks** — deadlines written in regulation, statute and contract that force a sale, a delivery, a close-out or a taxable event at a price nobody chose. This skill owns those clocks, the margin regime that enforces them, the borrow that can be taken away, the exit that costs more than the drawdown, and the reserve that keeps a good position from being sold at a bad price.

This is the equity analogue of `options-risk-engineer`. The options book owns DTE; this book owns the calendar that does the same job.

### The Four Clocks — This Replaces DTE

| Clock | Rule | Source | Forces |
|---|---|---|---|
| **Settlement** | **T+1** since 2024-05-28 | SEC Release 34-96930 | funding and delivery deadline |
| **Reg T payment / margin call** | settlement **+ 2 business days = 3 business days** | 12 CFR 220.2, 220.4(c)(3)(i) | fund the call |
| **Tax holding period** | long-term = **more than 1 year**; period runs from the day **after** the buy trade date to the **sale trade date** | IRC §1222; IRS Publication 550 | a **barrier**, not a deadline |
| **Wash sale** | **61-day window, ±30 days** | IRC §1091 | a **window to stay out of** |
| **Short-swing (insiders)** | **less than six months** | 15 U.S.C. §78p(b) | the insider's real DTE |
| **Reg SHO close-out** | close out by the **beginning of regular trading hours on the settlement day following the settlement date**; the **third consecutive settlement day** for a long-sale fail; **35 consecutive calendar days** for a Rule 144 / deemed-to-own fail | 17 CFR 242.204(a) | forced close-out |
| **Threshold securities** | fails of **at least 10,000 shares AND at least 0.5% of shares outstanding for 5 consecutive settlement days** places the security on the SRO list; close-out after **13 consecutive settlement days**; the security drops off after **5 consecutive settlement days** back below both legs | 17 CFR 242.203(b)(3), (c)(6) | a rolling clock that removes borrow, then removes the position |

**Source:** SEC Release 34-96930 (T+1 effective 2024-05-28); 12 CFR 220.2 and 220.4(c)(3)(i) (Reg T payment period); IRC §1222 and IRS Publication 550 (holding period); IRC §1091 (wash sales); 15 U.S.C. §78p(b) (short-swing); 17 CFR 242.204(a) (Reg SHO close-out); 17 CFR 242.203(b)(3), (c)(6) (threshold securities). Full treatment, including the insider filing clocks and the honest scope line for who they bind, is in [equity-time-axis-calendar.md](references/equity-time-axis-calendar.md).

**What this skill owns:** the equity time axis and its forced-action deadlines; margin regimes and forced-liquidation exposure; short-side borrow mechanics; concentrated-position, correlation and liquidity risk; exit-cost planning at entry; the cash / buying-power reserve floor and the deployment ladder; corporate-action interruptions.

**What it does not own:** whether to act on an open position (`equity-position-lifecycle`), which tax lot to sell or how to harvest a loss (`equity-tax-lot-and-exit-management`), position size (`portfolio-signal-manager`, `algorithmic-trader`), or security selection (`fundamental-analyst`, `technical-signals-engineer`, `macro-strategist`).

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "margin call\|maintenance margin\|buying power\|reg t\|portfolio margin")` AND `file_contains("*", "position\|holding\|account")` | This is your skill. Jump to **Core Workflow** — Phase 2 (Margin and Forced Liquidation). |
| A2 | `file_contains("*", "short\|borrow\|locate\|recall\|buy.?in\|fail to deliver")` | This is your skill. Jump to **Phase 3** (Borrow and Delivery). |
| A3 | `file_contains("*", "concentrat\|position size\|% of adv\|liquidity\|exit cost\|slippage")` AND NOT `file_contains("*", "option\|strike\|expiration\|premium")` | This is your skill. Jump to **Phase 4** (Liquidity and Exit Cost). |
| A4 | `file_contains("*", "option\|greek\|strike\|expiration\|implied vol")` AND `file_contains("*", "portfolio\|book\|margin")` | Invoke **options-risk-engineer** instead. Options-book risk is that skill's; the two share one reserve language by design. |
| A5 | `file_contains("*", "should I close\|hold or sell\|cut it\|take profit\|trim")` AND `file_contains("*", "position\|holding")` | Invoke **equity-position-lifecycle** instead. This skill supplies the clock and the deadline; that skill decides the action. |
| A6 | `file_contains("*", "which lot\|wash sale\|harvest\|cost basis\|specific identification")` | Invoke **equity-tax-lot-and-exit-management** instead. This skill supplies the 61-day window; that skill decides the lot. |
| A7 | `file_contains("*", "how many shares\|position size\|kelly\|risk parity")` AND NOT `file_contains("*", "margin\|liquidity\|exit")` | Invoke **portfolio-signal-manager** or **algorithmic-trader** instead. Sizing is not this skill's. |

### Intent Route

```
What equity risk question is this?
├── "How long do I have before they liquidate?"      → Phase 2 (margin clock) + DT2
├── "My short got recalled / borrow went hard"       → Phase 3 + DT3
├── "Can I get out of this size?"                    → Phase 4 + DT4
├── "Am I too concentrated?"                         → Phase 5 + DT5
├── "How much cash should I keep back?"              → Phase 6 (reserve floor) + DT6
├── "What closes first if I need capital?"           → Phase 6 + DT7
├── "When is the index / lock-up / tender event?"    → Phase 7 + DT8
├── "Which clock is running on this position?"       → Phase 1 (clock map) → then the owning phase
└── Full book risk audit (all phases)                → Run Phases 0-9 in order
```

### Research Prerequisite — Before Any Output

This is a hard gate. Before producing any recommendation, establish:

1. **The account type and regime** — cash, Reg T margin, or portfolio margin. Every number downstream depends on it, and none of them can be computed without it.
2. **The market's calendar for the current year** — holidays and half-days. A business-day deadline computed against a remembered calendar is a missed deadline.
3. **The broker's own figures** — buying power, margin requirement, maintenance excess, borrow status. Computed figures are `[COMPUTED]`; the broker's are authoritative `[BROKER-VERIFIED]`.
4. **The date every external artifact was read.** Index calendars, threshold lists, offer documents and borrow statuses all move. A figure without a read date is a figure of unknown age.

**If any of the four is missing, say so and stop.** Do not estimate around a missing input; a confident margin number built on a guessed regime is worse than no number.

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to report any margin, borrow or liquidity number without a provenance tag. Every output value carries `[COMPUTED]` (arithmetic shown), `[BROKER-VERIFIED]` (from the broker's own platform, with the read date), `[VERIFIED]` (with a named rule or statute next to it), `[COMMON-PRACTICE]` or `[ESTIMATED ±X%]`. | Trigger: any margin, call-date, borrow, ADV, spread or exit-cost figure in output without a tag | STOP. "Number '{value}' for '{metric}' has no provenance. Tag it — `[COMPUTED]` with the formula, `[BROKER-VERIFIED]` with the platform and read date, or `[VERIFIED]` with the rule named. An untagged risk number is how a forced liquidation gets discovered." |
| R2 | REFUSE to state a deadline as a duration when a date is owed. "You have 3 business days" is wrong five days out of five. Give the date, the market it is a business day in, and the holiday assumption behind it. | Trigger: output contains "days" as a deadline without a resolved calendar date | STOP. "Deadline expressed as a duration. Resolve it: trade 2026-03-06 → settlement 2026-03-09 → Reg T payment due 2026-03-11. A duration is not a deadline." |
| R3 | REFUSE to present the FINRA Rule 4210(f)(6) 15-business-day figure as the customer's grace period. It is an outer bound on the **member**, not an entitlement of the **customer**. | Trigger: "15 business days" or "how long do I have" answered with a figure above 3 business days without the member-versus-customer distinction | STOP. "That figure is a ceiling on the firm, not a window for you. The operative customer number is the Reg T payment period: settlement plus 2 business days. Do not plan against 15." |
| R4 | REFUSE to compute a call distance from initial margin. The call lands at **maintenance**, and for a maximally leveraged Reg T long account that is a 33.33% decline, not a 50% one. | Trigger: call distance computed from an initial-margin percentage rather than the FINRA Rule 4210(c) maintenance table | STOP. "Call distance must be computed at maintenance. Long: `MV − D < 0.25 × MV` → `MV < D / 0.75`. Recompute; the answer is earlier than you said." |
| R5 | REFUSE to state a short position's exit plan without a borrow status, a fee, and the lending agreement's recall terms. No SEC or FINRA rule fixes a recall notice period; commonly quoted practice is 1–2 business days and that is practice, not rule. | Trigger: short position analysed with no `borrow_status`, no `borrow_fee_annual_pct`, or no recorded recall terms | STOP. "Short position's exit has no owner. Record the borrow status, the fee, and the lending agreement's recall terms. There is no rule-fixed notice period to fall back on." |
| R6 | REFUSE to let any position reach entry without a named `exit_route`, an `exit_cost_pct`, and an `exit_cost_cap`. Route (f) — broker liquidation — **is not a route**. | Trigger: position opened or analysed with `exit_route` null, or equal to broker liquidation | STOP. "Position has no exit route. A position whose only exit is a broker liquidation is a future forced sale. Name the mechanism, the participation rate, the number of sessions, and the fallback." |
| R7 | REFUSE to place or approve a ticket that leaves uncommitted buying power below the reserve floor. The floor is checked **before** the ticket, never after the fill. | Trigger: new ticket AND (total_BP − committed_margin − new_ticket_margin) below `max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost)` | STOP. "Ticket blocked: after this fill uncommitted BP = ${after} [[COMPUTED]], below the ${floor} reserve floor, with {term} binding. Close something first — risk first, economics second, housekeeping third, balance sheet never." |
| R8 | REFUSE to present a stop-loss order as a bound on a position's maximum loss. A stop becomes a market order when it triggers; a gap skips the trigger price entirely. | Trigger: output stating or implying that a stop bounds the loss on a position held across a close, an event, or a halt | STOP. "A stop does not bound a gapping loss. The bound is position size and the reserve. State the gap scenario in dollars before restating the stop." |
| R9 | REFUSE to quote the $100,000 portfolio-margin minimum as a regulatory requirement. The rule text retrieved contains $5,000,000, and only for eligible participants trading unlisted derivatives; $100,000 is broker-set. | Trigger: portfolio-margin eligibility or minimum equity quoted as a rule with the $100,000 figure | STOP. "That figure is broker-set, not regulatory. The rule text retrieved contains $5,000,000 for unlisted derivatives only. Confirm $100,000 with the specific broker before using it, and label it `[BROKER-VERIFIED]`." |
| R10 | REFUSE to assert a rule number for a fact whose primary source was not retrieved — **and refuse to hedge a clock away where the primary source has been read.** Triple/quad witching is the known no-source case in this skill; the 180-calendar-day bid-price cure is **not**, because Nasdaq Rule 5810(c)(3)(A) states it. | Trigger: output asserts a rule source for triple witching, or states a day-trading-margin minimum from the superseded $25,000 / 4-in-5 regime that FINRA Regulatory Notice 26-10 replaced effective 2026-06-04 | STOP. "That number is not verified in this skill's research. Say so. Where no primary source was retrieved, the answer is 'convention, unverified', not a rule number. And where the rule did change — day-trading margin in 2026 — say so and send the reader to the broker." |
| R11 | REFUSE to pad a retail risk list with insider, affiliate or institutional clocks. Form 4, Schedule 13D/13G, Form 13F, Rule 144 and Rule 10b5-1 cooling-off bind insiders, affiliates and managers above $100M. If the user is an ordinary retail holder, they are not you. | Trigger: insider filing clocks or Rule 144 holding periods presented inside a retail holder's risk list without a scope statement | STOP. "State the scope first. Those clocks bind insiders, affiliates and managers above $100M. If the user is none of those, delete them from the list rather than decorating it." |
| R12 | REFUSE to hand a liquidation priority to a person under pressure without it being already written down. The order is risk first, economics second, housekeeping third, balance sheet never — and "worst liquidity first" is the **wrong** order. | Trigger: a capital raise or drawdown response that closes positions without reference to the standing forced-selling order | STOP. "That is improvisation under pressure. The standing order is: route-less positions, then the cluster that caused it, then worst economics, then concentration, then borrow-fragile, then housekeeping. Worst liquidity is the LAST criterion, not the first." |

## Anti-Hallucination

<!-- STANDARD: 3min — EXTRA CRITICAL for equity risk -->

A wrong margin number causes a forced sale. A wrong deadline causes a missed close-out. A wrong borrow assumption causes a buy-in the holder never agreed to. **Every number below must carry its provenance, and every rule must name its document.**

### Provenance Tags (Mandatory on All Numerical and Regulatory Output)

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `[COMPUTED]` | Calculated by this skill from stated inputs and published rules, with the formula shown | Call distance, reserve floor, exit cost, days-to-liquidate, buy-in arithmetic |
| `[VERIFIED]` | **A named, checkable source is cited next to it** — a statute section, a CFR section, a FINRA rule number, an exchange rule, or a methodology document with the publisher named. The tag is a claim about provenance, not about confidence | Maintenance percentages, settlement cycle, payment periods, buy-in timings, Reg SHO clocks, index effective dates |
| `[BROKER-VERIFIED]` | Taken from the broker's own platform or a written statement from the desk, with the read date | Buying power, margin requirement, borrow status, borrow fee, recall terms, easy-to-borrow classification, portfolio-margin eligibility and minimums |
| `[ESTIMATED ±X%]` | Modelled, with the derivation and the error bound shown | Impact cost, spread widening in stress, buy-in risk premium, `WCSD`, the reserve coefficients |
| `[COMMON-PRACTICE]` | A desk convention with no source retrieved; claims nothing beyond "this is what desks do" | Recall notice periods as commonly quoted, lock-up length as commonly quoted, triple/quad witching, tax-loss-selling seasonality |
| `[ILLUSTRATIVE]` | A severity band whose purpose is to rank failure modes, never to be summed, budgeted from, or quoted as a distribution | The `$X–$Y` cost bands in Anti-Rationalization, Error Recovery and Gotchas |

**Every `[VERIFIED]` must print its source inline.** A bare `[VERIFIED]` with no document, no section and no read date is a mis-tagged estimate. Where this skill cannot name the source — broker auto-liquidation behaviour, recall notice periods, triple-witching dates, day-trading margin minimums (the member's schedule under FINRA Rule 4210(d)(2), not a rule number) — the tag must be `[BROKER-VERIFIED]`, `[COMMON-PRACTICE]` or `[ESTIMATED ±X%]`, **never** `[VERIFIED]`.

### Safety Protocol Rules

| Rule | Description | Consequence of violation |
|------|-------------|--------------------------|
| **Admit uncertainty** | When the regime is unknown, when the broker's figures have not been read, when the borrow status is stale, when the market calendar has not been confirmed for the year — say so. "Cannot compute the call distance: account type is not established and the broker's maintenance requirement has not been read." | A forced liquidation discovered on the day it happens, on a position that the holder believed was safe |
| **Flag your knowledge cutoff** | The clocks in this skill carry dates because they move: T+1 arrived in 2024, the Rule 13D amendment deadlines changed effective 2024-02-05, the Rule 10b5-1 cooling-off rules changed effective 2023-02-27, the **day-trading margin requirements were replaced in their entirety effective 2026-06-04** (FINRA Regulatory Notice 26-10, with a phase-in to 2027-10-20), **Nasdaq Rule 5810 was amended with SEC approval 2024-10-07 and again in February 2025**, and the Russell reconstitution moves from annual to semi-annual from 2026. Any of these may have moved again. | A rule applied from a superseded version, with the holder's plan built on it |
| **Never guess security** | The borrow is the broker's, the margin requirement is the broker's, the recall terms are the lending agreement's, and the easy-to-borrow classification has no regulatory definition at all. One broker's rules are not another's. | A position that was "easy to borrow" at one desk and recalled the next morning at another |
| **Disclose methodology** | Every `[COMPUTED]` shows its formula and inputs. "Call distance" without `MV < D / 0.75` is not checkable. "Exit cost 3.2%" without the spread and the impact term is not checkable. | A decision made on a number nobody can reproduce, including the person who produced it |
| **Verify against the broker** | Before any action that changes margin by more than $5,000, read the broker's own buying power, maintenance excess and margin requirement. The computed figure is `[COMPUTED]`; the broker's is authoritative. | A forced sale caused by the gap between a correct calculation and the firm's actual requirement |

### Sources This Skill Cites, and What Each One Establishes

- **Source:** SEC Release 34-96930 — the T+1 settlement cycle, effective 2024-05-28.
- **Source:** 12 CFR 220 (Regulation T) — §220.2 and §220.4(c)(3)(i) the payment period; §220.4(d) the duty to liquidate, the $1,000 de-minimis and the absence of any advance-notice requirement; §220.8(c)(1) the 90-calendar-day payment-privilege freeze; §220.12(a) and (c)(1) initial margin of 50% long and 150% short.
- **Source:** FINRA Rule 4210 — (c) the maintenance table; (f)(6) the member's 15-business-day outer bound; **(f)(8) "Special Initial and Maintenance Margin Requirements"** — the current text, which is **not** the pattern-day-trader rule and contains no "pattern day" string at all; **(d)(2) the intraday-margin framework that replaced the day-trading margin requirements in their entirety effective 2026-06-04** `[VERIFIED — FINRA Regulatory Notice 26-10; FINRA Rule 4210(d)(2)]`; (g)(4)(C) and (g)(10)(A) portfolio margin and its 3-business-day cure.
- **Source:** FINRA Rule 11810 — the buy-in and close-out timings, and 11810(j), the liability notice for a security in a tender, exchange, redemption or expiry; plus FINRA Rule 5110(e)(1), the 180-day restriction on underwriting-compensation securities.
- **Source:** 17 CFR 242.204(a) and 242.203(b)(3), (c)(6) — the Reg SHO close-out requirement and the threshold-security two-leg test.
- **Source:** 17 CFR 240.14e-1 — the tender offer minimum open period and the 10-business-day extension; with 240.16a-3(g), 240.13d-1, 240.13d-2, 240.13f-1, 240.10b5-1(c)(1)(ii)(B) and 230.144 for the insider and institutional clocks.
- **Source:** IRC §1222 and §1091, with IRS Publication 550 — the long-term holding period and the 61-day wash-sale window; and 15 U.S.C. §78p(b), short-swing liability for insiders inside six months.
- **Source:** S&P U.S. Indices Methodology, published by S&P Dow Jones Indices — the index share/IWF effective close, the reference date, the announcement time and notice, and the September Total Market reconstitution.
- **Source:** FTSE Russell reconstitution documentation — the June cadence, the move to a semi-annual reconstitution from 2026, and **each event's own rank day**: the **last trading day of April for the June event**, the **last business day of October for the December event**, with the December event dates.
- **Source:** Nasdaq Rule 5810 **as amended** — SEC approval **2024-10-07**, and again in **February 2025**, so the **eff. 2023-10-02** version is **superseded**: the listing-deficiency compliance periods, **5810(c)(3)(A)**'s **automatic compliance period of 180 calendar days** for the $1.00 bid-price requirement, and the **360-calendar-day** bid-price **suspension trigger**.

**And what was not retrieved.** Two widely repeated figures have not yielded a primary source in this skill's research: the triple/quad-witching convention and the $100,000 portfolio-margin minimum. They are stated as `[COMMON-PRACTICE]` and `[BROKER-VERIFIED]` respectively — and re-read against the current rule text before they are used, because a source with an old read date is a source that may have moved. **The third figure formerly on this list has been retired from it:** the **180-calendar-day bid-price cure** does have a primary source and is now asserted — **Nasdaq Rule 5810(c)(3)(A)**, an automatic compliance period of 180 calendar days from the deficiency notice. **Source:** the rule texts above, as read at the time of writing; every one of them is re-read before a live decision depends on it.

### Number Provenance Decision Tree

```
How was this number obtained?
├── From the broker's platform or a written desk statement, with a read date → [BROKER-VERIFIED]
├── Computed from published rules and stated inputs, formula shown      → [COMPUTED]
├── Modelled with a stated derivation and an error bound                → [ESTIMATED ±X%]
├── A desk convention with no source retrieved                          → [COMMON-PRACTICE]
├── A named statute, rule, release or methodology document              → [VERIFIED — name it]
└── Cannot determine the source, or the input is stale/unavailable      → DO NOT REPORT
                                                                          Request it, or state
                                                                          what is missing
```

## Anti-Rationalization

<!-- DEEP: 10+min -->

| Rationalization | Reality |
|---|---|
| "I have 15 business days on a margin call — that is the rule." | It is **not** the rule for you. FINRA Rule 4210(f)(6) bounds the **member firm**: margin and mark-to-market calls "as promptly as possible and in any event within 15 business days". The customer's operative period for a Reg T deficiency is the payment period — settlement **+ 2 business days**, which is **3 business days from the trade** (12 CFR 220.2, 220.4(c)(3)(i)). And 12 CFR 220.4(d) says the firm **must** liquidate if the call is not met, with **no advance notice required**. Planning against 15 days is planning against a rule written to constrain your broker. **Cost: an illustrative severity band of $10,000–$150,000 in forced-sale slippage and realised loss [ILLUSTRATIVE — a ranking band, not a measured distribution].** |
| "It's a short at a $2,000 borrow fee — cheap. I'll hold it while the thesis plays out." | The fee is annualised on notional and it moves daily with supply. Short 2,000 shares at $25.00 is $50,000 of notional; 3%/yr is $4.11/day, 20%/yr is $27.40/day, and 100%/yr is $136.99/day [COMPUTED]. At the last of those the position must appreciate by the entire notional in a year just to break even, before commissions. And the borrow can be recalled — **no SEC or FINRA rule fixes a recall notice period**; the commonly quoted 1–2 business days is `[COMMON-PRACTICE]`, and the desk's terms are the lending agreement's, not a rule's. **Cost: an illustrative band of $5,000–$100,000 and, more importantly, a position closed on a date you did not choose.** |
| "My stop at $36 caps my loss at 10%." | A stop is a market order with a trigger. 2,500 shares at $40.00 is $100,000 and the stop plans a $10,000 loss at $36.00. An overnight gap to $31.00 fills at $30.80 and realises $23,000 — **$13,000 more than the plan, in one night** [COMPUTED]. Where trading is not continuous, the bound on the loss is **size**, not the stop. **Cost: an illustrative band of $10,000–$80,000, per event, in gap slippage past the stop [ILLUSTRATIVE].** |
| "I'm too concentrated, but the drawdown is what worries me — the price is only 12% off its high." | The drawdown is the number that appears on the screen every day, which is why it gets the attention. The number that decides the outcome is the **exit**. A $150,000 position that is 15.6% of its own ADV carries a round-trip cost of about 3.21%, or **$4,815 that is gone the moment it is closed and can never recover**, against a $30,000 paper loss that can [COMPUTED]. In a stressed tape the spread widens 1.3–2.0× and that $4,815 becomes **≈$5,183 at 1.3× and ≈$6,058 at 2.0×** [COMPUTED from the §3 cost model; the widening multipliers are `[ESTIMATED ±25%]`]. **A concentrated position's real risk is the exit, not the drawdown.** Say it with the user's own numbers. |
| "Portfolio margin will save me — my broker advertises it from $100,000." | The research for this skill could **not** find a $100,000 figure in the current FINRA Rule 4210 text it retrieved. What that text contains is **$5,000,000**, and only for eligible participants trading unlisted derivatives [VERIFIED — FINRA Rule 4210(g)(4)(C)]. The $100,000 is therefore **broker-set, not regulatory** `[BROKER-VERIFIED]`, and must be confirmed with the specific broker. And PM is a margin **calculation** difference, not a margin **grace** difference: a PM deficiency must be cured in **3 business days** or the member must liquidate [VERIFIED — FINRA Rule 4210(g)(10)(A)]. **Do not present $100,000 as a rule.** |

## The Expert's Mindset

<!-- STANDARD: 3min -->

Equity risk is not about being right. It is about remaining solvent, and able to act, on the day you turn out to be wrong. Four questions define the discipline, and none of them is a price question:

1. **Which clock is running on this position?** Settlement, the payment period, the holding period, the wash-sale window, the borrow, the fail, the offer, the index date. Name it. A position with an unnamed clock is a position whose deadline will be discovered by the counterparty.
2. **Where is the call, in dollars and in price?** Not "I have plenty of cushion" — the market value at which maintenance is breached, and the dollar deficiency that follows.
3. **What does it cost to leave, and how many sessions does it take?** Not "it's liquid" — a percentage and a session count, at a stated participation rate.
4. **How much can never be spent?** The reserve. Not an intention, not a cash-like label: uncommitted buying power, above `max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost)`, tested before the ticket.

**World-class equity risk management is the art of never being the forced seller.** The forced seller is always selling into the worst tape, in the name someone else picked, at a size nobody wanted. The reserve, the exit plan and the concentration cap are the three walls that prevent it — and like all walls, they only work if they are built before they are needed.

### The Four Regimes — What Changes in Each

| Regime | What the clocks do | What changes in the book | The one thing to do |
|---|---|---|---|
| **Bull market / uptrend** | Nothing. The clocks are the same; only the pain is absent | Correlations fall, ADV rises, spreads tighten, borrow looks easy, and every input to the exit model improves — so the model *invites* a larger position | Re-measure the exit cost and **notice** that it improved. Do not convert an improvement in the weather into a change in size |
| **Correction / pullback** (−5% to −20%) | A margin call becomes arithmetically reachable; a Reg SHO fail becomes plausible in a thin name | The exit cost drifts up, days-to-liquidate lengthen, clusters begin to converge, and the cushion shrinks faster than the requirement | Raise the re-measurement cadence; do not add; re-test `exit_cost_pct` against its cap |
| **Bear market / downturn** (−20% or more) | Every clock is now a live threat, including the holding-period barrier and the wash-sale window if a loss is being realised | Correlations approach 1; the book behaves as one position; the exit is a multi-session programme, not a trade | Execute the standing forced-selling order, risk first. It should already be written down |
| **Crash / tail event** (a market collapse, a March-2020-style event) | The clocks stop being advisory. A buy-in, a close-out and a call can all land in the same week | Bids become optional, halts interrupt trading, and the reserve is the only remaining buffer | Nothing. In the crash regime there are no decisions left, only consequences — which is the argument for everything above |

All four regimes belong in the plan. **A plan written in an uptrend and never read in the other three is not a plan; it is a description of the weather on the day it was written.**

**Regime classification and data-derived thresholds.** Naming which of the four regimes the book is in uses the **Pattern Recognition Engine** meta-layer at `skills/14-finance/options-strategist/references/pattern-recognition-engine.md` (a repo-relative path — nothing here depends on it being installed in a project). And the thresholds in this skill are of exactly two kinds, and each is labelled: **rule-derived** (`[VERIFIED]` with the rule named beside it) and **desk policy** (`[ESTIMATED ±X%]` with the derivation shown, e.g. the `0.15 × NAV` coefficient as `0.25 × 0.50 × 1.2`). None of them is a round number chosen for comfort, and a threshold that cannot be traced to one of the two kinds is not a threshold — it is an opinion wearing a number.

## Operating at Different Levels

<!-- STANDARD: 3min -->

| Level | Scope | Example |
|-------|-------|---------|
| **L1: Apprentice** | Read the margin requirement and the settlement date off the broker's screen | "The Reg T call is due 2026-03-11, and I need $4,200 of settled cash in the account before then." |
| **L2: Practitioner** | Map every clock per position; compute the call distance at maintenance; record an exit route and cost per position | "The call price on this levered long is $66,667, a 33.33% decline; `exit_cost_pct` is 3.21% against a 3% core cap, so it is a satellite position or it is smaller." |
| **L3: Senior** | Run the book: the reserve floor, the deployment ladder, concentration clusters, borrow status, the forced-selling order | "$190,000 uncommitted against a $120,000 floor with `R_tail` binding; a $90,000 ticket is blocked. Two names are 80% of the exit-weighted concentration; the standing order closes them third." |
| **L4: Staff** | Manage the interaction of the clocks across a multi-position book, including shorts, corporate actions and index events | "The 13-settlement-day close-out counter and the December reconstitution effective date fall in the same week in the same name. The short's exit is scheduled before the counter can reach 10." |
| **L5: Transformative** | Design the capital policy itself — coefficients, ladder rungs, escalation thresholds — and prove it in the crash regime | "The floor's tail coefficient was relaxed from 1.0 to 0.50 only after twelve months of the book's own margin-expansion data; the ladder's rungs are re-derived from that data each year rather than inherited." |

## When to Use

<!-- QUICK: 30s -->

- A margin call has arrived, or is being asked about, and the question is **how long** and **what happens next**
- A short position's borrow has been recalled, gone hard-to-borrow, or its fee has moved
- A position is failing to deliver, or a held security is on, or near, the threshold list
- A position has become large relative to NAV, relative to its ADV, or relative to the book's correlated exposure
- The question is how to get out of a size without moving the price, and at what cost
- Deciding the cash or buying-power amount that must stay uncommitted, and how the ceiling tightens after losses
- Planning what closes first if capital is genuinely needed
- A scheduled date is approaching: index reconstitution, lock-up expiry, tender or exchange offer deadline, redemption or expiry, a known delisting-deficiency announcement
- Building the calendar of forced-action dates for a book, including the holding-period barrier and the wash-sale window
- Working out whether a stop-loss actually bounds the loss on a position that gaps

## When NOT to Use

<!-- QUICK: 30s -->

- Deciding **what to do** with an open equity position — close, trim, add, hold, average down — use **equity-position-lifecycle**. This skill supplies the clock, the deadline and the cost; that skill decides the action
- Choosing **which tax lot** to sell, harvesting a loss, or applying specific identification — use **equity-tax-lot-and-exit-management**. This skill supplies the 61-day wash-sale window; that skill decides the lot
- **Sizing** a new position — how many shares, what fraction of NAV, Kelly, volatility targeting — use **portfolio-signal-manager**; for automated execution of the size, **algorithmic-trader**
- **Selecting** a security or forming a view — use **fundamental-analyst**, **technical-signals-engineer**, or **macro-strategist**
- Portfolio-level **options** Greeks, pin risk, expiration calendars, option margin add-ons — use **options-risk-engineer**
- Constructing an **options hedge** for an equity position — use **options-risk-engineer** for the hedge mechanics; this skill owns only the equity-side clock and the capital it consumes
- **Executing** orders, working VWAP or TWAP, or connecting to a broker API — use **algorithmic-trader**
- **Broker-statement reconciliation** or tax reporting — a bookkeeping task, not a risk task

## Decision Trees

<!-- STANDARD: 3min -->

### DT1: Which Clock Is Running on This Position?

```
What kind of position, and what has happened to it?
├── A purchase that has not settled → SETTLEMENT CLOCK: T+1. Do not spend the same cash twice
│    ├── cash account? → the sale funding it has its OWN T+1; a mismatch is a free-riding
│    │    violation and a 90-calendar-day payment-privilege freeze (12 CFR 220.8(c)(1))
│    └── margin account? → the broker may front buying power; confirm, do not assume
├── A margin deficiency → REG T CLOCK: settlement + 2 business days = 3 business days
│    ├── is the deficiency ≤ $1,000? → the firm need not act (12 CFR 220.4(d));
│    │    the holder still must, and the exemption does not survive the next down day
│    └── deficiency funded from a realised loss inside ±30 days? → WASH-SALE WINDOW
│         is now open on the same trade (IRC §1091). Two clocks, one decision
├── A short position → BORROW CLOCK and DELIVERY CLOCK, and they are different clocks
│    ├── has the borrow been recalled? → no rule fixes the notice period; go to DT3
│    └── is the position failing to deliver? → REG SHO CLOCK (17 CFR 242.204(a))
│         └── security on the threshold list? → 13 consecutive settlement days (242.203(c)(6))
├── A position near the one-year mark → HOLDING-PERIOD BARRIER: a barrier, not a deadline.
│    └── but a tender or redemption deadline may sit INSIDE it → two clocks, opposite directions
├── An insider or affiliate near a round trip → SIX-MONTH SHORT-SWING CLOCK (15 U.S.C. §78p(b))
│    └── if the holder is not an insider, this clock is NOT THEIRS. Delete it
└── A security with a pending corporate action → THE OFFER'S OWN CUTOFF TIME
     └── FINRA Rule 11810(j) anchors the deadline to the offer's instructions, not to days
```

### DT2: "How Long Do I Have Before They Liquidate?"

```
What kind of deficiency is it?
├── Reg T deficiency → 3 BUSINESS DAYS from the trade (settlement + 2). Resolve to a DATE
│    ├── can the deficiency be funded with SETTLED funds today? → fund it, then re-read BP
│    ├── can it be funded only by a sale that has not settled? → that sale's own T+1 applies.
│    │    Confirm with the broker whether that cures the call. Tag the answer [BROKER-VERIFIED]
│    └── cannot fund? → the firm MUST liquidate; no advance notice is required (220.4(d))
├── Portfolio-margin deficiency → 3 BUSINESS DAYS to cure, or the member liquidates
│    └── FINRA Rule 4210(g)(10)(A). PM is a calculation difference, not a grace difference
├── Day-trading / intraday-margin deficiency → the cure clock is the MEMBER'S intraday-margin
│    schedule under FINRA Rule 4210(d)(2) — NOT the old PDT 5-business-day special call. The
│    $25,000 minimum and the 4-day-trades-in-5 designation were SUPERSEDED effective 2026-06-04
│    (FINRA Regulatory Notice 26-10). VERIFY WITH YOUR BROKER — this changed in 2026
└── Someone quoted 15 business days → STOP. That is the member's ceiling under 4210(f)(6),
     not the customer's window. Say so, then answer with the real number
```

### DT3: The Short's Borrow Is Recalled — What Now?

```
How much time do I have, and what can I actually do?
├── Notice period → THERE IS NO RULE-FIXED PERIOD. It is the lending agreement's [BROKER-VERIFIED]
│    └── "usually 1-2 business days" is [COMMON-PRACTICE], not a rule. Do not present it as one
├── Can a new locate be obtained? → price it, and re-test the exit-cost cap with the new fee
│    ├── new fee still inside cap → decide whether the thesis pays for the new fee
│    └── new fee outside cap → the position is now a forced sale on a date you did not choose
├── Cannot locate? → BUY IT BACK. Into whatever the market offers, before a delivery failure
│    └── a delivery failure starts a DIFFERENT clock: 3 consecutive settlement days for a
│         long-sale fail, sooner in general (17 CFR 242.204(a))
└── Has a buy-in notice already arrived? → FINRA Rule 11810 timings are live
     ├── reject IN WRITING by 6:00 p.m. ET on the notice date, or it is DEEMED ACCEPTED
     ├── cure delivery by 3:00 p.m. ET on the effective date
     ├── securities in transit get a 7-CALENDAR-DAY extension
     └── the buy-in is executed for the account and liability of the PARTY IN DEFAULT
          └── short 2,000 at $30.00, bought in at $42.00 = (42 − 30) × 2,000 = $24,000, before fees
```

### DT4: Can I Actually Get Out of This Size?

```
Size the exit from the position, not from the portfolio view
├── position_shares / 20-day ADV
│    ├── under 5% → 0.5 sessions at 10% participation; the spread dominates; verify it is a
│    │    two-sided market, then exit on the plan
│    ├── 5-20% → 0.5 to 2 sessions at 10% participation. THIS IS THE PLANNING BAND
│    ├── 20-50% → 2 to 5 sessions at 10%. The plan must be a PROGRAMME, with a fallback
│    └── over 50% → the position IS the market. Re-size or accept a multi-week unwind
├── round_trip_cost_pct = spread_pct + 2 × impact_pct     (impact grows as sqrt(Q/ADV))
│    ├── inside the 3% core cap → core position
│    ├── 3-5% → satellite position, or smaller
│    └── above 5% → fails the gate. Size down until it fits, or do not hold it
├── does the exit route have a NAME and a FALLBACK?
│    ├── yes → schedule it, and put the date on the calendar
│    └── no, or "the broker will handle it" → that is route (f), which is not a route
└── is a stop being counted as the bound?
     └── if the position is held across any close, event or halt → the bound is SIZE, not the stop
```

### DT5: Am I Too Concentrated?

```
Which measure, and does it breach?
├── position_value / NAV
│    ├── over 10% → BREACH: the single-name size ceiling, owned by portfolio-signal-manager
│    │    (10% single-name / 25% sector). Size down, or make the sizing argument there — and
│    │    record the exit plan either way. 15% is NOT a licence: no second cap exists here
│    └── within 10% but the cluster is over 25% at correlation → the CLUSTER is the breach
├── position_shares / 20-day ADV
│    └── over 20% → the exit-cost model will not hold in stress; re-measure and re-decide
├── position_shares / shares_outstanding
│    ├── over 1% → monitor, especially on the short side
│    └── short at or above 10,000 shares AND 0.5% → the Reg SHO threshold clock is engaged
├── exit_weighted_concentration = Σ ( value/NAV × exit_cost_pct )
│    └── one position contributing over half the total → THAT POSITION IS THE BOOK'S EXIT RISK
└── correlated cluster weight, sized at correlation → 1.0
     ├── the cluster is the position, not the ticker. Five names, one factor = ONE position
     └── the cluster closes WHOLE or not at all. Closing one leg converts diversification
          into concentration under pressure
```

### DT6: The Reserve Floor — Is This Ticket Allowed?

```
Compute BEFORE the ticket, never after the fill
├── uncommitted_BP_after_fill = total_BP − (committed_margin + new_ticket_margin)
├── reserve_floor = max( 0.15 × NAV , 0.50 × WCSD , 1.5 × exit_cost(book) )
│    ├── R_dd   = 0.15 × NAV      the nominal drawdown allowance
│    ├── R_tail = 0.50 × WCSD     the correlated drawdown — USUALLY THE BINDING TERM in equities
│    └── R_exit = 1.5  × exit     spread + impact, plus borrow and buy-in risk on shorts
├── is uncommitted_BP_after_fill ≥ reserve_floor?
│    ├── yes → ALLOWED. Log the headroom that remains
│    └── no  → BLOCKED. Name the binding term. Do not re-test after the fill
└── is a reserve breach already open?
     ├── yes → BLOCK ALL NEW TICKETS until restored, with no discretionary exception
     └── and close in the standing order: risk first → economics second →
          housekeeping third → balance sheet NEVER
```

### DT7: I Need Capital — What Closes First?

```
Capital is needed. What closes?  (NOT "worst liquidity first")
├── Is uncommitted BP already below the reserve floor?
│    ├── YES → the failure is upstream: the floor was tested after a fill, not before
│    │    └── Log it, block ALL new tickets until restored, then close in the order below
│    └── NO → this is a planned reduction, not an emergency — close in the order below anyway
├── 1. Route-less and recall-flagged positions → CLOSE NOW (no exit_route, no locate, no stop)
├── 2. The position or correlated cluster that CAUSED the drawdown → CLOSE the risk, not the winners
├── 3. Largest dollar exit cost among positions that can exit inside their own cap → worst
│      ECONOMICS, not worst LIQUIDITY. Worst liquidity is the LAST criterion, not the first
├── 4. Most concentrated name, and the highest position-as-%-of-ADV → CLOSE
├── 5. Highest borrow fee, or shortest fail age, on the short side → CLOSE
├── 6. Housekeeping: odd lots, spin-off stubs, residuals → housekeeping, no market impact
├── 7. NEVER FIRST: deepest liquidity, tightest spread, closest to target
│    └── they fund the loss at the best price the book can get; selling them first
│         leaves only the unwanted assets
└── 8. NEVER: one leg of a correlated cluster while keeping the rest
     └── it converts a diversified cluster into a concentrated one, when capital is shortest
```

### DT8: A Scheduled Date Is Approaching — What Does It Force?

```
Which event, and whose clock is it?
├── Index share / IWF change or a reconstitution effective close
│    ├── S&P: after the close of the THIRD FRIDAY of Mar/Jun/Sep/Dec; reference date is the
│    │    Wednesday before the SECOND Friday; S&P 1500 changes announced 5:15 p.m. ET with at
│    │    least 3 business days' notice; S&P Total Market reconstitutes after the close of
│    │    the THIRD FRIDAY in September
│    └── Russell: SEMI-ANNUAL (June and December) FROM 2026, and EACH EVENT HAS ITS OWN RANK
│         DAY — the June event: the last trading day of April (2026-04-30); the December
│         event: the last business day of October (2026-10-30). The first December event is
│         effective after the close on 2026-12-11, with prelim lists 2026-11-13 and updates
│         11-20, 11-27, 12-04
│         └── THIS IS A RECENT CHANGE. A June-only model of Russell is now wrong — and so is
│              one April rank day applied to both events of a two-event year
├── Tender or exchange offer → 20 business days minimum from first publication; a change in the
│    percentage sought, the consideration, or the soliciting fee requires 10 MORE business days;
│    consideration paid "promptly" after termination or withdrawal (17 CFR 240.14e-1)
│    └── and for a short or a hedge: FINRA Rule 11810(j) may substitute a LIABILITY NOTICE for a
│         buy-in, sent no later than TWO HOURS before the cutoff time in the OFFER'S INSTRUCTIONS
├── Lock-up expiry → about 180 days is CONTRACTUAL [COMMON-PRACTICE]; the only rule-fixed 180 days
│    is FINRA Rule 5110(e)(1), for underwriting-compensation securities only
│    └── supply rises and liquidity thins: re-measure exit_cost_pct on the date, not after it
└── Delisting deficiency → Nasdaq Rule 5810 AS AMENDED (SEC approval 2024-10-07, and again
     February 2025; the eff. 2023-10-02 text is SUPERSEDED)
     ├── bid price below $1.00 → AUTOMATIC COMPLIANCE PERIOD OF 180 CALENDAR DAYS from the
     │    deficiency notice [VERIFIED — Nasdaq Rule 5810(c)(3)(A)]
     │    └── and the 360-CALENDAR-DAY figure is the SUSPENSION TRIGGER — suspended if
     │         non-compliant with the $1.00 bid-price requirement for more than 360 days —
     │         not an extension, and not merely Listing Council discretion
     └── compliance plan → generally 45 calendar days to submit, 60 for the (v) case, as read
          in the rule version at the time of writing; re-read the amended text before relying
          └── THE HOLDER'S CLOCK IS THE ANNOUNCEMENT, never the issuer's cure period
```

## Core Workflow

### Phase 0: Establish the Regime and the Calendar (3min)

1. **Establish the account type and margin regime** — cash, Reg T margin, portfolio margin. Nothing downstream can be computed without it. Ask, or read it off the statement; do not infer it.
2. **Load the market calendar for the current year** — holidays and half-days — before computing any business-day deadline.
3. **Read the broker's own figures** with a timestamp: buying power, margin requirement, maintenance excess, borrow status, borrow fee. Everything read becomes `[BROKER-VERIFIED]` with its read date.
4. Complete when: the regime is named, the calendar is loaded for the current year, and every broker-sourced input carries a read date. If any of the three is missing, stop and say so rather than estimating around it.
   - Full clock table and the scope line on who each clock binds → [equity-time-axis-calendar.md](references/equity-time-axis-calendar.md)

### Phase 1: Build the Clock Map (5min)

1. **Per position, record every clock that applies**: trade date, settlement date (T+1), Reg T payment date (settlement + 2 business days), the holding-period date, the wash-sale window where a loss is realised, the short-swing date where the holder is an insider, and — for shorts — the borrow status and any fail age in consecutive settlement days.
2. **Resolve every duration to a date.** "3 business days" is not a deadline; 2026-03-11 is.
3. **Name the owning skill for each clock's decision.** This skill owns the clock and the deadline; the action on the position belongs to `equity-position-lifecycle`, and the tax-lot consequence to `equity-tax-lot-and-exit-management`.
4. Complete when: every open position resolves to at least one named clock with a resolved date, and every date has a source and a read date. A position with no named clock is an audit gap.
   - The consolidated clock table and the interaction cases → [equity-time-axis-calendar.md](references/equity-time-axis-calendar.md)

### Phase 2: Margin and Forced-Liquidation Exposure (5min)

1. **Name the regime, then compute under it.** Reg T initial margin is 50% of market value long and 150% short [VERIFIED — 12 CFR 220.12(a), (c)(1)]. Maintenance follows FINRA Rule 4210(c): long 25%; long non-margin-eligible 100%; short below $5.00 the greater of $2.50 per share or 100%; short at or above $5.00 the greater of $5.00 per share or 30% [VERIFIED — FINRA Rule 4210(c)].
2. **Compute the call distance at maintenance**, not at initial margin: `equity = MV − D` and `requirement = 0.25 × MV`, so the call lands at `MV < D / 0.75` — a 33.33% decline at maximum Reg T leverage [COMPUTED].
3. **State the liquidation rule exactly** — if the call is not met the firm **must** liquidate; **no action is required if the deficiency is ≤ $1,000**; **no advance notice is required** [VERIFIED — 12 CFR 220.4(d)].
4. Complete when: the regime is named, both a Reg T and a PM figure are reported where the account is PM-eligible, the call distance is shown in dollars and in price, and the 15-business-day figure has been labelled a ceiling on the **member** if it appears at all.
   - Full maintenance table, the call arithmetic, the post-2026 day-trading margin regime that replaced PDT, PM, and the honest note on the $100,000 figure → [margin-regimes-and-forced-liquidation.md](references/margin-regimes-and-forced-liquidation.md)

### Phase 3: Borrow, Delivery and the Short-Side Clocks (3min)

1. **Record the borrow status, the fee and the recall terms.** Easy-to-borrow and hard-to-borrow have **no regulatory definition** — the classification is the desk's `[BROKER-VERIFIED]`. The fee is negotiable and moves daily with supply `[BROKER-VERIFIED]`. **No SEC or FINRA rule fixes a recall notice period** `[BROKER-VERIFIED]`; the commonly quoted 1–2 business days is `[COMMON-PRACTICE]`.
2. **Price the borrow into the exit.** Short 2,000 shares at $25.00 is $50,000 notional: 3%/yr is $4.11/day, 20%/yr is $27.40/day, 100%/yr is $136.99/day [COMPUTED]. Add borrow accrued to the planned exit and a buy-in risk premium to `exit_cost_pct`.
3. **If delivery has failed, the buy-in timings are live** [VERIFIED — FINRA Rule 11810]: close-out no sooner than the third business day after delivery was due; the buy-in notice must reach the seller not later than 12:00 noon ET two business days before the proposed execution; the seller must reject in writing by 6:00 p.m. ET on the notice date or it is **deemed accepted**; delivery cure by 3:00 p.m. ET on the effective date; in-transit securities get a 7-calendar-day extension; and the buy-in is executed **for the account and liability of the party in default**.
4. Complete when: every short has a timestamped borrow status, a fee, the lending agreement's recall terms, a fail age where a fail exists, and a priced buy-in exposure on the exit record.
   - Recall, buy-in sequence and the short-side ledger → [short-borrow-and-buy-in-mechanics.md](references/short-borrow-and-buy-in-mechanics.md)
   - Fails, the 35-calendar-day Rule 144 case and the threshold-security rolling clock → [reg-sho-and-threshold-list.md](references/reg-sho-and-threshold-list.md)

### Phase 4: Liquidity and the Exit Plan (5min)

1. **Size the exit at entry, not at the exit.** Record `exit_route` (a–e; broker liquidation does not count), `exit_cost_pct`, `exit_cost_cap` and `size_vs_adv` in the entry record.
2. **Compute the cost as `spread_pct + 2 × impact_pct`**, with `impact_pct = k × σ_daily × sqrt(Q/ADV)` [ESTIMATED ±50%]. Size by **% of average daily volume**: the ceiling is 20% of ADV, and the plan is 10%. A $150,000 position at 15.6% of ADV carries a round-trip cost of about 3.21%, or **$4,815** [COMPUTED].
3. **Say the honest sentence out loud, with the user's numbers: a concentrated position's real risk is the exit, not the drawdown.** $4,815 of exit cost never recovers; a $30,000 drawdown can.
4. Complete when: every position has a non-null exit route that is not (f), an `exit_cost_pct` inside its cap, a `size_vs_adv` inside 20%, and a `days_to_liquidate` figure at 10% participation.
   - Cost model, participation table, re-measurement cadence, worked example → [liquidity-and-exit-cost-planning.md](references/liquidity-and-exit-cost-planning.md)

### Phase 5: Concentration and Correlation (3min)

1. **Compute four measures per large position:** weight in NAV, fraction of ADV, fraction of shares outstanding, and the correlation-adjusted weight against the largest position.
2. **Compute the exit-weighted concentration:** `Σ (value/NAV × exit_cost_pct)` [COMPUTED]. A position contributing over half of it **is** the book's exit risk, whatever its NAV weight says.
3. **Cluster by economic driver and size the cluster at correlation → 1.0**, never at measured correlation. The cluster closes whole or not at all.
4. Complete when: the four measures are reported, the exit-weighted concentration names its top contributor, every cluster is listed with its aggregate weight, and the two clocks of a concentrated position — the exit clock and the margin clock — are reported as dates or sessions.
   - The four measures, the two clocks, and the four-regime behaviour table → [concentration-and-correlation-risk.md](references/concentration-and-correlation-risk.md)

### Phase 6: The Reserve Floor and the Deployment Ladder (3min)

1. **Compute the floor before anything else:** `reserve_floor = max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost(book))`. The test is `uncommitted_BP_after_fill ≥ reserve_floor`, run **before** the ticket.
2. **Size to the ladder, which only tightens:** the effective ceiling is `min(margin-regime colour band, state ceiling)`. State ceilings — **capital ceilings** on committed margin — are: ≤ 60% after one position taken to a full planned loss, ≤ 45% after two (and no new shorts), ≤ 30% at a ≥ 15% NAV drawdown, ≤ 15% with **no new tickets** at ≥ 25% or Red. **These are not position-size rules**, and they do not replace `portfolio-signal-manager`'s **10% single-name / 25% sector** sizing caps: a ticket must satisfy both, and the tighter one binds.
3. **The worked test is the reference case.** NAV $500,000; total_BP $400,000; committed margin $210,000 → uncommitted BP **$190,000**. Floor terms `$75,000 / $120,000 / $96,000` → **floor $120,000**, `R_tail` binding. Headroom **$70,000** → a **$90,000-margin ticket is BLOCKED** (after-fill uncommitted BP $100,000) and a **$65,000 ticket is ALLOWED** (after-fill $125,000) [COMPUTED].
4. Complete when: the floor is computed from live `total_BP` with all three terms shown and the binding term named; the deployable ceiling is reported alongside the margin-regime band; every position has an exit cost inside its cap; and the forced-selling order is recorded as a standing priority **before** it is needed.
   - Coefficients with derivations, the end-to-end worked example, the ladder, the forced-selling order → [capital-reserve-and-deployment.md](references/capital-reserve-and-deployment.md)

### Phase 7: Corporate Actions and the Structural Calendar (3min)

1. **Map every scheduled date touching a held name**: index effective closes, reconstitution dates, tender and exchange offer windows, redemption and expiry dates, lock-up expiries, delisting announcements.
2. **Apply the event's own clock.** A tender offer must remain open at least 20 business days from first publication, and a change in the percentage sought, the consideration, or the soliciting fee requires at least 10 more business days [VERIFIED — 17 CFR 240.14e-1]. Where the security is subject to a tender, exchange, redemption or expiry, **FINRA Rule 11810(j)** lets the receiving member serve a **Liability Notice instead of a buy-in**, sent no later than **two hours before the cutoff time in the offer's instructions** [VERIFIED — FINRA Rule 11810(j)]. That deadline is the offer document's.
3. **Resolve the delisting clocks from the current rule, and label convention as convention.** The **180-calendar-day bid-price cure is a rule**: an **automatic compliance period of 180 calendar days** from the deficiency notice under **Nasdaq Rule 5810(c)(3)(A)**, with the **360 calendar days** figuring as the **suspension trigger** for continued non-compliance. Cite the **current** text — Rule 5810 was amended with SEC approval 2024-10-07 and again in February 2025 — and note that the holder's clock is the **announcement**, not the issuer's cure period. Triple/quad witching has no source retrieved here and is `[COMMON-PRACTICE]`.
4. Complete when: every scheduled date is on the position's calendar as a date with a source; the offer's instruction cutoff has been read wherever a tender, exchange, redemption or expiry is pending; and no unverified figure has been asserted as a rule.
   - Tender offers, the liability notice, delisting and halts, splits and spin-offs → [corporate-action-and-halt-playbook.md](references/corporate-action-and-halt-playbook.md)
   - Index and structural calendar, including the Russell semi-annual change from 2026 → [index-and-event-calendar.md](references/index-and-event-calendar.md)

### Phase 8: Gap and Event Exposure (3min)

1. **State every position's maximum loss as size-based, not stop-based.** A stop becomes a market order; a gap skips the trigger. 2,500 shares at $40.00 with a stop at $36.00 plans a $10,000 loss; an overnight gap to $31.00 fills at $30.80 and realises **$23,000** [COMPUTED].
2. **List the scheduled gap dates** — earnings, macro releases, index effective dates, lock-up expiries, corporate action dates — and re-test the book at a correlated gap, which is what the `WCSD` term in Phase 6 is modelling.
3. **Read the plan in the current regime.** Bull market, correction, bear market, crash: name which one the book is in, and whether the plan has ever been read in it.
4. Complete when: every position's maximum loss is size-based in dollars; scheduled gap dates are on the calendar; and the four regimes have each been applied to the book with the current regime named.
   - Gap arithmetic, event classes, and the compound margin-call-during-a-gap case → [gap-and-event-risk.md](references/gap-and-event-risk.md)

### Phase 9: The Standing Liquidation Priority (2min)

1. **Write the order down, before it is needed:** risk first → economics second → housekeeping third → balance sheet never. Route-less and recall-flagged positions first; then the cluster that caused the drawdown; then the largest dollar exit cost among positions that can exit inside their own cap; then the most concentrated; then the borrow-fragile; then housekeeping. **Worst liquidity first is the wrong order** — say it in those words.
2. **Confirm the reserve makes step seven unreachable.** The deepest-liquidity, tightest-spread positions are the balance sheet. They fund a loss at the best available price, and selling them first leaves the book holding only what nobody wanted.
3. Complete when: the order is recorded as a standing instruction; the reserve floor has been recomputed from live `total_BP`; and the escalation thresholds in `## Cross-Skill Coordination` are wired to the clocks in Phase 1.
   - The ordered list, and the failure modes of the policy itself → [capital-reserve-and-deployment.md](references/capital-reserve-and-deployment.md)

## Best Practices

<!-- STANDARD: 3min -->

1. Resolve every deadline to a **date** in the market's own business-day calendar, and re-read the calendar when the year rolls. A duration is not a deadline.
2. Compute the call distance at **maintenance**, show the formula, and quote it in dollars and in price. `MV < D / 0.75` is a 33.33% decline at maximum Reg T leverage, and knowing that number before the position exists is the whole discipline.
3. Whenever the 15-business-day figure appears, label it a **ceiling on the member firm**, not an entitlement of the customer, and restate the operable number: 3 business days from the trade.
4. Verify every margin, buying-power and borrow figure against the broker's own platform before a decision depends on it, and record the timestamp of the read.
5. Record every short position's borrow status, borrow fee and the lending agreement's **recall terms** at entry, and re-price the fee on a schedule. There is no rule-fixed notice period to rely on.
6. Price the borrow and a buy-in risk premium into the short's `exit_cost_pct` **before** computing the reserve floor. A reserve that ignores short-side cash demand is understated.
7. Give every position a named `exit_route` that is not "the broker will handle it", a participation rate, a session count, and a fallback.
8. Size by **percentage of average daily volume** — the ceiling is 20% of ADV and the plan is 10% — and report `days_to_liquidate` at 10% participation for every position.
9. Re-measure spread and ADV weekly, and immediately on any of: a new 52-week low, a gap of more than 5%, a halt, a delisting announcement, a threshold-list appearance, an index effective date, or a lock-up expiry.
10. Test the reserve floor **before** every ticket, name the binding term, and block the ticket when it fails. A reserve tested after the fill is a post-mortem.
11. Let the deployment ladder only tighten: the effective ceiling is `min(colour band, state ceiling)`, so a state ceiling can restrict but never relieve.
12. Record the forced-selling order as a **standing** instruction — risk first, economics second, housekeeping third, balance sheet never — so it is not improvised at the worst moment.
13. State every maximum loss as size-based, not stop-based, for any position held across a close, an event or a halt.
14. Say which clocks bind the user and which do not. Form 4, Schedule 13D/13G, Form 13F, Rule 144 and Rule 10b5-1 cool-offs bind insiders, affiliates and managers above $100M — if the user is none of those, they are not you, and padding the risk list with them is a defect.

## Error Decoder

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| "The call came on day three — I thought I had fifteen business days." | The 15 business days is FINRA Rule 4210(f)(6)'s outer bound on the **member firm**, not a customer entitlement. The Reg T payment period is settlement + 2 business days: 3 business days from the trade (12 CFR 220.2, 220.4(c)(3)(i)). The plan was built on the wrong clock entirely | Re-plan on the payment period. Compute the date at trade time, not when the notice arrives. Where 15 days is quoted, label it a ceiling on the firm | **Read the rule's subject before you read its number.** A ceiling on your broker is not a floor under you, and the two read identically in a summary |
| "My short got recalled with about a day's warning." | There is **no SEC or FINRA rule that fixes a recall notice period**. The terms are the lending agreement's, and the fee and availability are the desk's, moving daily with supply. The 1–2 business days everyone quotes is `[COMMON-PRACTICE]` | Attach the lending agreement's recall terms to the position at entry; re-price the borrow on a schedule; never assume a notice period | **A rule you cannot cite is a rule that does not protect you.** Ask the desk for the terms in writing, and treat the answer as a term of the trade |
| "The broker bought my short in 40% above where it was trading." | A buy-in under FINRA Rule 11810 is executed **for the account and liability of the party in default**. The notice must reach the seller by 12:00 noon ET two business days before execution; failing to reject **in writing** by 6:00 p.m. ET on the notice date is **deemed acceptance**; delivery must be cured by 3:00 p.m. ET on the effective date | Answer every buy-in notice in writing the day it arrives. Keep a locate available before the cure deadline. Price the buy-in exposure into the exit cost so it is not a surprise | **Silence is acceptance.** A delivery notice is a document with a deadline, not a notification to read later |
| "The name was on the threshold list and the borrow vanished." | 17 CFR 242.203(b)(3) puts a security on the SRO list after fails of at least 10,000 shares **and** at least 0.5% of shares outstanding for 5 consecutive settlement days; 242.203(c)(6) requires close-out after 13 consecutive settlement days. Both are counts, and nobody announces the start | Monitor the SRO list; treat membership as a change in the position's risk rather than as news; schedule the exit before the counter can reach 13 | **Consecutive-settlement-day counters do not send reminders.** The only announcement is the close-out |
| "I sold at a loss in December and the loss was disallowed." | The wash-sale rule (IRC §1091) is a **61-day window**, ±30 days around the sale — not a calendar-year boundary. A repurchase in January inside that window disallows the loss and adjusts the replacement lot's basis | Put the 61-day window on the position's calendar whenever a loss is realised, and check it before any re-entry in the same security or a substantially identical one | **The tax year and the wash-sale window are different shapes.** One ends on 31 December; the other follows the trade |
| "I sized the exit at double the stock's average daily volume and the price collapsed." | Impact cost grows with the **square root** of the fraction of daily volume traded, and the position was twice the whole day's volume. There was no market to leave into that had not already been moved by the sale | Size by percentage of ADV — 20% is the ceiling, 10% is the plan — and compute `days_to_liquidate` before entry | **A position that is larger than its market has an exit, not a price.** Size is the exit plan |

## Error Recovery

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| The reserve floor is already breached and a new ticket is pending | The floor was tested after a fill, or not at all. The breach is upstream of the ticket, not caused by it | Block all new tickets until the floor is restored, with no discretionary exception, then reduce in the standing order: risk first, economics second, housekeeping third, balance sheet never | **A reserve that can be spent "temporarily" is not a reserve.** The exception is the failure mode |
| A concentrated name's exit cost has drifted from 3.0% to 5.5% and nothing was decided | ADV and spread were measured once, at entry, and never re-measured. Nothing broke; the market simply changed shape | Re-measure immediately, re-test against the cap, and either size down or re-plan the exit as a multi-session programme | **Exit cost is data, not a constant.** An unmeasured position is an unplanned position |
| Two positions in "different sectors" fell together by the same amount | They were one economic cluster, sized at measured correlation. In stress, correlation moves toward 1.0 | Re-cluster by economic driver, size the cluster at correlation → 1.0, and close clusters whole rather than one leg at a time | **Five tickers is not five positions.** The cluster is the position |
| A stop was hit and the realised loss was more than double the planned loss | The position gapped through the trigger. A stop becomes a market order, and a gap skips the price | Re-state the maximum loss as size-based, size the position for the gap, and use the reserve floor rather than the stop as the bound | **Stops manage speed, not size.** Where trading is not continuous, only size bounds the loss |
| The short was closed out at 13 settlement days while the thesis was still intact | The Reg SHO close-out clock is not interested in the thesis. It counts consecutive settlement days from the fail, and it ends in a mandatory close-out | Exit before the counter reaches 10; monitor fail age daily; treat threshold-list membership as a change in the position's risk | **A rule-governed clock beats a well-researched opinion.** Where the clock and the thesis disagree, the clock acts |

## Cross-Skill Coordination

### Upstream (Data In)

| Upstream Skill | What You Receive | When to Involve |
|----------------|------------------|-----------------|
| `market-data-engineer` | Prices, volume and ADV, corporate action calendars, index membership, halt notices, data quality flags | Before any ADV, spread or event computation; on any corporate action or halt in a held name |
| `portfolio-signal-manager` | The position list, weights, NAV, sector and factor exposures, rebalance signals, drawdown state | At Phase 0 and Phase 5; on any drawdown alert or rebalance signal |
| `fundamental-analyst` | Company fundamentals and event calendar inputs (earnings dates, guidance) | When a scheduled gap date must be established for a held name |
| `macro-strategist` | The regime read and scheduled macro releases | At Phase 8, to name the current regime and to list correlated gap dates |
| `options-risk-engineer` | The options book's margin consumption, `WCML`, and its own reserve floor and forced-selling order | Whenever a book holds both equities and options. The two are **sibling policy sets, each correct for its own instrument class** — an options book uses the options file, an equity-only book uses this one — and they are **not numerically identical**: the `R_dd` coefficient differs (`0.15 × NAV` here, `0.20 × NAV` there), the `R_tail` middle term differs (`WCSD`, a simultaneous drawdown, here versus `WCML`, a simultaneous max loss, there), and the ladder rungs diverge. **Where the two ever disagree on the same account, this skill defers** — see `references/capital-reserve-and-deployment.md` |
| `equity-position-lifecycle` | The verdict on an open position — hold, trim, close, add — together with its own review clock | Whenever a clock in Phase 1 reaches its action window |

### Downstream (Risk Out)

| Downstream Skill | What You Send | Trigger |
|------------------|---------------|---------|
| `equity-position-lifecycle` | The clock map, the resolved deadlines, the call distance, the exit cost, the reserve-floor state | PUSH: any clock entering its action window, any breach, any call |
| `equity-tax-lot-and-exit-management` | The 61-day wash-sale window, the holding-period date, and the realised loss that sits inside either | PUSH: on any realised loss, and on any position within 30 days of the long-term barrier |
| `portfolio-signal-manager` | The reserve floor, deployable capital, the deployment ceiling, concentration and exit-weighted concentration | PUSH: limit breach, ceiling change, reserve breach |
| `algorithmic-trader` | The forced-selling order and the exit programme (route, participation rate, session count) once a decision is made | PUSH: liquidation required, exit programme scheduled |
| `options-risk-engineer` | The equity side's capital consumption, so that the combined reserve is not double-counted or under-counted | PUSH: on any ticket that consumes margin in a book holding both |

### Escalation

```
LOW (a clock inside its window, floor intact)      → log it, put the date on the calendar
MODERATE (exit cost over its cap, or a cluster     → notify the decision owner; re-measure the
         above its weight)                          inputs; block new risk in that name
HIGH (margin call live, borrow recalled, fail       → reduce immediately in the standing order;
     age ≥ 10 settlement days, reserve breached)     notify the decision owner; halt new tickets
CRITICAL (liquidation under way, buy-in noticed,   → liquidate per the standing priority; halt all
         close-out demanded, halt in a held name)   new risk; post-mortem required before resuming
```

### Communication Contract

Every inter-skill message: `{message_id, source_skill, target_skill, message_type, timestamp,
correlation_id, payload: {clock_type, deadline_date, position_id, risk_numbers: [{value, unit,
description, provenance}], binding_term, recommended_action, urgency}, expected_response_type,
timeout_seconds}`.

## Proactive Triggers

<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---|---|---|
| A Reg T payment date is one business day away and the deficiency is not funded | Fund it with settled funds today, or expect the firm to act; confirm with the broker that the cure counts | The firm **must** liquidate if the call is not met, and **no advance notice is required** (12 CFR 220.4(d)) |
| The 15-business-day figure appears in a plan | Re-label it as a ceiling on the member and restate the 3-business-day payment period | Planning against a rule written to constrain the broker is the most expensive misread in this skill |
| A short's borrow fee moves by more than 5 percentage points in a week | Re-price the exit cost, re-test it against the cap, and decide the position on the new fee | The fee is a running charge, and it moves daily with supply |
| A short's fail age reaches 10 consecutive settlement days | Exit before the counter reaches 13; do not wait for the close-out | 13 consecutive settlement days triggers a mandatory close-out (17 CFR 242.203(c)(6)) |
| A buy-in notice arrives | Answer in writing by 6:00 p.m. ET on the notice date; arrange delivery before 3:00 p.m. ET on the effective date | Silence is **deemed acceptance** (FINRA Rule 11810) |
| Any position's `position_shares / 20-day ADV` crosses 20% | Re-measure the exit cost and re-plan the exit as a programme with a fallback | Above 20% the holder is the market in their own position |
| Any position's `exit_cost_pct` breaches its cap | Size down or re-plan the exit; do not carry an unpriced exit | An exit cost outside its cap is a position that fails its own gate |
| NAV drawdown reaches 15% from high-water | Drop the deployment ceiling to 30%, forbid new concentrated and new short positions, and re-read the plan in the current regime | A 15% drawdown is a regime signal: the correlation and exit-cost assumptions were built in the old regime |
| Uncommitted buying power falls below the reserve floor | Block **all** new tickets until restored, then reduce in the standing order | The reserve exists so a good position never has to be liquidated at a bad price |
| A held name appears on the threshold list | Treat membership as a change in the position's risk: re-price the borrow, re-plan the exit, and check the fail age | The borrow disappears before the close-out does |
| A held name has an index effective close within five sessions and the position is over 10% NAV | Decide **in advance** whether the index flow is the exit window or the exit obstacle; schedule accordingly | The largest scheduled liquidity event of the quarter is also the worst price discovery |
| A held name has a lock-up expiry within ten sessions | Re-measure spread and ADV on the date, and re-test the exit cost | Supply rises and liquidity thins; the exit cost moves for a reason unrelated to the security |
| A tender, exchange, redemption or expiry is pending in a held name | Read the **offer's instructions** for the cutoff time and compute the Rule 11810(j) deadline from it | The liability-notice deadline is anchored to the offer document, not to a fixed number of days |
| A scheduled gap date (earnings, macro release, index event) is within five sessions and the position is levered | Reduce, or fund the cushion to the gapped case; compute the compound case | The margin call and the exit clock racing in the same name is how positions die |
| A loss is realised inside ±30 days of a purchase in the same or a substantially identical security | Flag the wash-sale window and route the lot decision to `equity-tax-lot-and-exit-management` | A disallowed loss is a real dollar cost with no market event behind it |

## Anti-Patterns

<!-- STANDARD: 3min -->

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| ❌ **Planning against the 15-business-day figure** | It is FINRA Rule 4210(f)(6)'s ceiling on the **member firm**. The customer's operative period is settlement + 2 business days, and the firm must liquidate if it is not met, with no advance notice | ✅ Plan against the Reg T payment period, resolved to a date. Quote the 15-day figure only with the word "member" attached |
| ❌ **Sizing the exit at the exit** | Position size, ADV and spread are all known at entry. Discovering them at the exit means discovering them in the worst tape, with the least time | ✅ Record `exit_route`, `exit_cost_pct`, `exit_cost_cap` and `size_vs_adv` before the fill, and re-measure on a cadence |
| ❌ **Treating a stop order as a maximum-loss guarantee** | A stop becomes a market order when it triggers. A gap skips the trigger price: $100,000 with a stop planning a $10,000 loss realised $23,000 in one night [COMPUTED] | ✅ State the maximum loss as size-based in dollars, and re-test the position at a correlated gap rather than at the average day |
| ❌ **Computing concentration from NAV weight alone** | A name at 30% of NAV can contribute 80% of the book's exit-weighted concentration while a name at 24% of NAV contributes 2% of it [COMPUTED] | ✅ Report all four measures: weight in NAV, fraction of ADV, fraction of shares outstanding, and exit-weighted concentration, and name the top contributor |
| ❌ **Selling the least-liquid positions first because "we should get rid of the hard-to-sell things while we can"** | It maximises impact, realises the worst price on the assets with the least market to absorb them, and leaves the book holding only what nobody wanted | ✅ Close **risk first, economics second, housekeeping third, balance sheet never**. Worst liquidity is the **last** criterion, not the first |

## State Log

<!-- STANDARD: 3min -->

| State Field | Type | Persists Across | Description |
|---|---|---|---|
| `regime` | Enum | Session | cash / reg-t / portfolio-margin, with the source and the read date |
| `calendar.market` | MarketCalendar | Session | The current year's holidays and half-days, with the read date; every business-day computation depends on it |
| `clocks` | [PositionClock] | Daily | Per position: trade date, settlement date (T+1), Reg T payment date, holding-period date, wash-sale window, and any insider clock |
| `margin.current` | MarginSnapshot | Session → Daily | Buying power, requirement, maintenance excess, and utilisation — `[BROKER-VERIFIED]` with a timestamp |
| `margin.call_distance` | CallDistance | Realtime | The market value and the percentage decline at which maintenance is breached, computed at maintenance, not initial margin |
| `short.borrow` | [BorrowState] | Daily | Per short: `borrow_status` (with timestamp), `borrow_fee_annual_pct`, `recall_terms`, `fail_age_settlement_days` |
| `short.buy_in_exposure` | Dollar | Session | The priced buy-in liability per short, and the notice deadlines if a notice is live |
| `liquidity.exit_routes` | [ExitRecord] | Session | Per position: `exit_route` (a–e; (f) does not count), `exit_cost_pct`, `exit_cost_cap`, `size_vs_adv`, `days_to_liquidate` |
| `liquidity.remeasure` | [RemeasureTask] | Weekly | The spread and ADV re-measurement schedule, with the immediate-trigger list wired |
| `concentration.measures` | [PositionExposure] | Session | The four measures per large position, plus each correlated cluster's aggregate weight at correlation → 1.0 |
| `concentration.exit_weighted` | float | Session | `Σ (value/NAV × exit_cost_pct)` for the book, with the top contributor named |
| `capital.reserve_floor` | ReserveFloor | Realtime | `max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost)`, recomputed from live `total_BP` every time it is tested, never cached |
| `capital.deployable` | DeployableCapital | Session | `total_BP − reserve_floor`, the state ceiling from the ladder, and the effective ceiling `min(colour band, state ceiling)` |
| `capital.binding_term` | Enum | Session | Which of `R_dd`, `R_tail`, `R_exit` is binding — the term that decides the ticket |
| `events.calendar` | [EventDate] | Session | Index effective dates, reconstitution dates, lock-up expiries, tender windows, redemption and expiry dates, delisting announcements, with sources |
| `events.gap_dates` | [GapDate] | Session | Scheduled earnings, macro releases and other known gap generators for held names |
| `standorder.liquidation` | [PositionRef] | Session | The standing forced-selling order, recorded before it is needed |
| `policy.coefficients` | PolicyConfig | Session → Archive | The reserve coefficients and ladder rungs in force, with the derivation and the date they were last re-derived |

## Production Checklist

<!-- STANDARD: 3min -->

Before this skill is relied on with live positions:

- [ ] **CR1: Account regime established and recorded.** Cash, Reg T margin or portfolio margin, from the statement or the broker, never inferred. Every downstream number depends on it.
- [ ] **CR2: The market calendar for the current year is loaded, with its read date.** Holidays and half-days. Every business-day deadline in this skill resolves through it.
- [ ] **CR3: Every open position has a resolved clock map with dates.** Settlement, Reg T payment, holding period, wash-sale window where applicable, and borrow/fail age for shorts. No clock left as a duration.
- [ ] **CR4: Margin is verified against the broker's own platform, with a timestamp.** The computed figure is `[COMPUTED]`; the broker's determines whether a call arrives.
- [ ] **CR5: Call distance is computed at maintenance and shown in dollars and in price.** `MV < D / 0.75` for the long case; the FINRA Rule 4210(c) table for the short case.
- [ ] **CR6: Every short has a borrow status, a fee, the lending agreement's recall terms, and a fail age.** No rule-fixed recall period exists to fall back on.
- [ ] **CR7: The buy-in notice deadlines are encoded, not remembered.** Notice by 12:00 noon ET two business days out; written rejection by 6:00 p.m. ET on the notice date; cure by 3:00 p.m. ET on the effective date.
- [ ] **CR8: Every position has an exit record from entry.** Named route that is not (f), `exit_cost_pct` inside its cap, `size_vs_adv` inside 20%, and a `days_to_liquidate` figure.
- [ ] **CR9: Concentration is reported on all four measures, with the exit-weighted figure naming its top contributor.**
- [ ] **CR10: Correlated clusters are sized at correlation → 1.0, and close whole or not at all.**
- [ ] **CR11: The reserve floor is enforced by the system, not by discipline.** The pre-trade test blocks a ticket that would breach `max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost)`, and names the binding term.
- [ ] **CR12: The deployment ladder only tightens.** The effective ceiling is `min(colour band, state ceiling)`, and every rung has been observed to bind in a test.
- [ ] **CR13: The forced-selling order is recorded as the standing priority.** Risk first → economics second → housekeeping third → balance sheet never; worst liquidity is the last criterion, not the first.
- [ ] **CR14: Scheduled event dates for held names are on the calendar with sources.** Index effective dates, lock-up expiries, tender windows, redemption and expiry dates.
- [ ] **CR15: Every maximum loss is stated as size-based, not stop-based,** and the compound case (a gap during a margin call) has been computed for the largest levered position.
- [ ] **CR16: Every figure is tagged for what it actually is.** Triple/quad witching is labelled `[COMMON-PRACTICE]` and the $100,000 portfolio-margin figure `[BROKER-VERIFIED]`; the **180-calendar-day bid-price cure is asserted from Nasdaq Rule 5810(c)(3)(A)** in its **current** (post-2024/2025 amendment) form, with the holder's clock named as the **announcement**; and no day-trading-margin figure comes from the **superseded** $25,000 / 4-in-5 regime.
- [ ] **CR17: The scope statement is applied.** Insider, affiliate and institutional clocks are quoted only where they bind, and are removed from a retail holder's risk list.

## What Good Looks Like

- **Every clock has a date, a source and a read date.** "Settlement 2026-03-09, Reg T payment 2026-03-11, holding period 2027-03-03" — never "about three days".
- **The call price is known before the position exists.** In dollars and in price, computed at maintenance, with the formula shown.
- **No short is held without knowing who can take it away, on what terms, and for how much.** Borrow status, fee, recall terms, fail age, and a priced buy-in exposure, all in the record.
- **Every position has an exit it can actually execute.** A named route, a participation rate, a session count, a fallback, and a cost inside its cap.
- **The concentration conversation is about the exit.** The four measures reported, the exit-weighted figure naming its top contributor, and the sentence "the exit, not the drawdown, is the real risk" said with the user's own numbers.
- **The reserve is intact and deliberate.** Uncommitted buying power above `max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost)` before every ticket, with the binding term named.
- **The forced-selling order is written down before it is needed,** and it is not "worst liquidity first".
- **Scheduled dates are on the calendar, not in memory.** Index effective dates, lock-up expiries, tender windows — each with a source and a read date.
- **The plan has been read in all four regimes,** and the current regime is named.
- **What is unverified is labelled unverified, and what is verified is not hedged away.** Triple/quad witching and the portfolio-margin minimum are stated as convention and as broker-set respectively; the **180-calendar-day bid-price cure** is stated as the rule it is — **Nasdaq Rule 5810(c)(3)(A)** — with the holder's own clock named as the **announcement**.

## Verification Guardrails

<!-- STANDARD: 3min -->

| Guard | Test | Failure Response |
|---|---|---|
| G1: PROVENANCE-REQUIRED | Every margin, borrow, liquidity or cost figure in output carries `[COMPUTED]`, `[BROKER-VERIFIED]`, `[VERIFIED]` with a named source, `[ESTIMATED ±X%]` or `[COMMON-PRACTICE]`. | "Output blocked: '{value}' for '{metric}' has no provenance. An untagged risk number is how a forced liquidation gets discovered. Tag it or remove it." |
| G2: DEADLINE-IS-A-DATE | No deadline is expressed as a duration where a date is owed. Every deadline names the market's business-day calendar used. | "Deadline expressed as '{n} days'. Resolve it to a date in the market's calendar and re-state it. A duration is not a deadline." |
| G3: MEMBER-NOT-CUSTOMER | Where the 15-business-day figure appears, it is labelled a ceiling on the member firm, and the Reg T 3-business-day payment period is stated alongside it. | "Blocked: '15 business days' presented as the customer's window. That is FINRA Rule 4210(f)(6) bounding the member. The customer's number is settlement + 2 business days." |
| G4: MAINTENANCE-NOT-INITIAL | Any call distance is computed from the FINRA Rule 4210(c) maintenance table, with the arithmetic shown. | "Blocked: call distance computed from initial margin. Recompute: `equity = MV − D`, `requirement = 0.25 × MV`, call at `MV < D / 0.75`." |
| G5: BORROW-STATE-COMPLETE | Every short reports borrow status with a timestamp, fee, recall terms and fail age. No recall period is asserted as a rule. | "Blocked: short '{id}' has no borrow state. There is no rule-fixed recall notice period; record the lending agreement's terms and the desk's current fee." |
| G6: EXIT-RECORD-COMPLETE | Every position has a non-null `exit_route` that is not broker liquidation, an `exit_cost_pct` inside its cap, and a `size_vs_adv` inside 20%. | "Blocked: position '{id}' fails its exit gate. A position whose only exit route is a broker liquidation is not a position." |
| G7: RESERVE-FLOOR-PRE-TRADE | `uncommitted_BP_after_fill` is computed before the ticket and compared against `max(0.15 × NAV, 0.50 × WCSD, 1.5 × exit_cost)`, with the binding term named. | "Ticket blocked: after this fill uncommitted BP = ${after} [COMPUTED], below the ${floor} floor, with {term} binding. Close something first — risk first, economics second, housekeeping third, balance sheet never." |
| G8: LADDER-ONLY-TIGHTENS | The effective ceiling is taken as `min(colour band, state ceiling)`. A state ceiling is never used as relief. | "Blocked: the state ceiling was used to relax the margin band. The ladder only tightens. Retake the `min`." |
| G9: TAG-MATCHES-PROVENANCE | The triple/quad-witching convention and the $100,000 portfolio-margin minimum are labelled `[COMMON-PRACTICE]` and `[BROKER-VERIFIED]`, and no rule number is asserted for either. The **180-calendar-day bid-price cure is asserted only against Nasdaq Rule 5810(c)(3)(A)**. No day-trading-margin figure is asserted from the superseded $25,000 / 4-in-5 regime. | "Blocked: '{claim}' is asserted with no source retrieved, or a real clock has been hedged as unverified. Tag it to what it actually is — convention, broker-set, or the rule that says it — and where the rule changed in 2026, verify with the broker." |
| G10: STOP-IS-NOT-A-BOUND | No output presents a stop-loss order as bounding the loss on a position held across a close, an event or a halt. | "Blocked: a stop cannot bound a gapping loss. State the maximum loss as size-based in dollars, and compute the gapped case." |

### Failure Modes of This Skill's Own Output, and Their Countermeasures

A risk analysis fails in its own way, and the failure is silent. These are the failure modes of the output itself — each one numbered, each with the countermeasure that prevents it.

1. **Failure mode — the duration that pretends to be a deadline.** The clock is reported as "3 business days" and the weekend is discovered by the calendar rather than by the reader. *Countermeasure:* G2 above; resolve every business-day clock to a date in the market's own calendar, and print the calendar's read date beside it.
2. **Failure mode — the call distance computed at initial margin.** The cushion looks twice as large as it is, and the breach arrives at a 33.33% decline rather than a 50% one. *Countermeasure:* G4; compute `equity = MV − D` against `requirement = 0.25 × MV` and show the price at which `MV = D / 0.75`.
3. **Failure mode — the member's ceiling read as the customer's window.** Fifteen business days is quoted as grace and the Reg T payment period passes unmentioned. *Countermeasure:* G3; restate the 3-business-day payment period every time the 15-day figure appears.
4. **Failure mode — the borrow assumed to persist.** A recall, a fee that has tripled, or a locate that no longer exists is discovered while the position is open. *Countermeasure:* G5; timestamped borrow status, fee, recall terms and fail age on every short, refreshed on a schedule.
5. **Failure mode — the exit route that is really route (f).** "The broker will handle it" is recorded as a plan and the position is liquidated at a broker-chosen price. *Countermeasure:* G6; a named mechanism, a participation rate, a session count and a fallback, or the position fails its own gate.
6. **Failure mode — the reserve tested after the fill.** The gate becomes a post-mortem and the next decision is already constrained. *Countermeasure:* G7; compute `uncommitted_BP_after_fill` before the ticket and name the binding term of `R_dd`, `R_tail`, `R_exit`.
7. **Failure mode — the ladder used as relief.** A damaged book argues its way back to the normal ceiling and takes risk in the regime that damaged it. *Countermeasure:* G8; the effective ceiling is always `min(colour band, state ceiling)`.
8. **Failure mode — concentration measured only as weight in NAV.** The name that is 30% of NAV and 80% of the exit risk is treated as equivalent to the name that is 24% of NAV and 2% of it. *Countermeasure:* report all four measures and the exit-weighted concentration, with its top contributor named.
9. **Failure mode — the stop presented as a maximum loss.** A gap through the trigger turns a planned $10,000 loss into a realised $23,000. *Countermeasure:* G10; state the maximum loss as size-based in dollars and compute the gapped case.
10. **Failure mode — an unverified figure asserted as a rule, or a verified one hedged away.** Either the triple-witching convention or the $100,000 portfolio-margin minimum is repeated with the authority of the rules beside it, or a real clock — the 180-calendar-day bid-price cure at Nasdaq Rule 5810(c)(3)(A) — is written off as unverifiable and quietly drops out of the reader's calendar. *Countermeasure:* G9; tag each figure to what it actually is, cite the rule where a rule exists and the **current version** of it, and never attach a rule number that was not retrieved.
11. **Failure mode — the insider clock applied to a retail holder.** A risk list padded with Form 4, Schedule 13D, Form 13F and Rule 144 obligations that do not bind the user, hiding the two clocks that do. *Countermeasure:* state the scope line — insiders, affiliates and managers above $100M — before quoting any row of that table.
12. **Failure mode — the exit cost measured once, at entry.** A position drifts from a 3.0% round trip to 5.5% while no decision was taken, and is then exited into the thinner book. *Countermeasure:* the weekly re-measurement cadence, plus the immediate triggers — a new 52-week low, a gap beyond 5%, a halt, a delisting announcement, a threshold-list appearance, an index effective date, a lock-up expiry.
13. **Failure mode — the forced-selling order improvised under pressure.** Positions are closed by liquidity rather than by risk, and the book is left holding only what nobody wanted. *Countermeasure:* record the standing order — risk first, economics second, housekeeping third, balance sheet never — and verify that the reserve makes the balance-sheet step unreachable.
14. **Failure mode — the plan never read outside an uptrend.** The correlation and exit-cost inputs come from a bull market and are applied in a downturn. *Countermeasure:* re-read the plan in the named regime, and treat a plan that has never been read in the crash regime as unvalidated.

## Deliberate Practice

<!-- STANDARD: 3min -->

1. **Clock-map drill.** Take five positions — one recently purchased, one levered, one short, one with a realised loss, one in a name with a pending corporate action — and write every clock that applies with a resolved date and a source. Time yourself. If any clock is a duration, the drill is not finished.
2. **Call-price calibration.** For ten historical positions, compute the price at which maintenance would have been breached, then compare against the actual worst drawdown over the following year. Were any of them inside the range they experienced?
3. **Borrow-recall rehearsal.** Take a short position and write the three responses — new locate, buy it back, fail to deliver — with the cost of each and the date by which each must start. Then find the lending agreement's actual recall terms.
4. **Exit-cost measurement.** For your largest position, compute `spread_pct`, `impact_pct`, `exit_cost_pct` and `days_to_liquidate` at 10% participation. Then place a small order in that name's size class and compare the realised slippage against the model. The model is wrong until it has been wrong once and corrected.
5. **Buy-in arithmetic.** Write out a FINRA Rule 11810 sequence for a hypothetical fail: notice date, the 12:00 noon ET deadline, the 6:00 p.m. ET rejection deadline, the 3:00 p.m. ET cure, and the dollar cost of a buy-in 15% above the short sale price. Then check whether your position record would have caught the notice.
6. **Reserve-floor audit.** Compute `R_dd`, `R_tail` and `R_exit` for your own book, name the binding term, and check whether every ticket taken in the last quarter would have passed. If the term that binds is `R_dd`, ask whether `WCSD` is being computed honestly.
7. **Gap stress by regime.** Apply four gaps — 5%, 12%, 25% and 40% — to the book, correlated, and record the cushion, the call trigger and the realised exit cost in each. Re-read the plan in the crash regime specifically.
8. **Calendar reconstruction.** Without looking, write down the index effective dates, lock-up expiries and offer deadlines that touch your positions in the next two quarters. Then look them up and count the misses. The misses are the drill.

## References

<!-- STANDARD: 3min -->

The following reference files are loaded on demand when deeper context is needed:

| Reference | Path | Content |
|---|---|---|
| **The Equity Time Axis** | [equity-time-axis-calendar.md](references/equity-time-axis-calendar.md) | The consolidated clock table: settlement, the Reg T payment period, the holding period, the wash-sale window, the short-swing clock, the Reg SHO close-out and the threshold-security clock. What each one forces, what happens if nothing is done, the insider and institutional filing clocks with the honest scope line for who they bind, and how the clocks compose. |
| **Settlement and the Payment Period** | [settlement-and-payment-period.md](references/settlement-and-payment-period.md) | T+1 since 2024-05-28 and what changed. The Reg T payment period as settlement + 2 business days. Two worked timelines showing the same rule five calendar days apart. The cash-account good-faith violation and the 90-calendar-day freeze. Business-day counting with holidays and half-days. |
| **Margin Regimes and Forced Liquidation** | [margin-regimes-and-forced-liquidation.md](references/margin-regimes-and-forced-liquidation.md) | Reg T initial margin at 50% long and 150% short. The FINRA Rule 4210(c) maintenance table. Where the call actually is, computed for the long and the short case. The call timeline, the 15-business-day ceiling on the member, and the liquidation rule. The day-trading margin framework that **replaced PDT** effective 2026-06-04 (FINRA Rule 4210(d)(2); FINRA Regulatory Notice 26-10), and the cash-account freeze. The portfolio-margin minimum figure that could not be verified and what to do about it. |
| **Short Borrow and Buy-In Mechanics** | [short-borrow-and-buy-in-mechanics.md](references/short-borrow-and-buy-in-mechanics.md) | What has no regulatory definition (easy-to-borrow, the borrow fee, the recall period) and what does. The FINRA Rule 11810 buy-in sequence with every deadline. Borrow-cost arithmetic at 3%, 20% and 100% annualised. A priced buy-in. The short-side risk ledger and its five required fields. |
| **Reg SHO and the Threshold List** | [reg-sho-and-threshold-list.md](references/reg-sho-and-threshold-list.md) | The three close-out clocks of 17 CFR 242.204(a) and which case each covers. The threshold-security two-leg test, where each leg binds by shares outstanding, the 5-day entry and 13-day close-out counters, a worked settlement-day timeline, and the one ambiguity in the start convention stated honestly. |
| **Liquidity and Exit-Cost Planning** | [liquidity-and-exit-cost-planning.md](references/liquidity-and-exit-cost-planning.md) | The exit contract recorded at entry: route, cost, cap and size against ADV. The spread and square-root impact cost model. A concentrated-position worked example end to end. Why the exit, not the drawdown, is the real risk. The participation and days-to-liquidate table. The re-measurement cadence and its triggers. |
| **Concentration and Correlation** | [concentration-and-correlation-risk.md](references/concentration-and-correlation-risk.md) | The four concentration measures and what each one misses. Exit-weighted concentration worked on a book, showing one name contributing most of the exit risk at a third of the NAV weight. Clustering by economic driver, correlation → 1.0 sizing, and the rule that a cluster closes whole or not at all. The two clocks of a concentrated position. |
| **Capital Reserve and Deployment** | [capital-reserve-and-deployment.md](references/capital-reserve-and-deployment.md) | The three-term reserve floor with each coefficient derived, tagged and open to disagreement. A fully worked end-to-end floor test with the binding term identified. The deployment ladder by book state. The equity exit-cost term including the short-side rows. The forced-selling order and why worst liquidity is last. The failure modes of the policy itself. |
| **Corporate Action and Halt Playbook** | [corporate-action-and-halt-playbook.md](references/corporate-action-and-halt-playbook.md) | Tender and exchange offers under 17 CFR 240.14e-1, and the equity analogue of an expiry wall — FINRA Rule 11810(j) and the liability notice anchored to the offer's own instructions. Merger and cash-out mechanics. Nasdaq Rule 5810 deficiency clocks — the **180-calendar-day automatic bid-price cure** at 5810(c)(3)(A), the **360-day suspension trigger**, and the rule's 2024/2025 amendments, quoted from the current text. Splits, reverse splits and spin-offs. |
| **Index and Event Calendar** | [index-and-event-calendar.md](references/index-and-event-calendar.md) | S&P share/IWF effective closes, the reference date, the announcement time and notice, and the September Total Market reconstitution. The Russell reconstitution and the change to a semi-annual cadence from 2026, with **each event's own rank day** (April for the June event, the last business day of October for the December event) and the December event dates. Triple and quad witching, stated as convention with no source invented. Lock-up expiries and the narrow rule-fixed 180 days. Tax-loss-selling seasonality. |
| **Gap and Event Risk** | [gap-and-event-risk.md](references/gap-and-event-risk.md) | Why a gap is not a fast move, and why a stop does not bound it. Stop arithmetic showing a planned 10% loss realising 23%. Gap exposure by position type. The scheduled gap dates. The compound case — a gap during a margin call — computed in dollars. The four regimes and what changes in each. |

### Related Skills

| Skill | Relationship | When to invoke |
|---|---|---|
| `equity-position-lifecycle` | **Downstream — the decision owner.** This skill supplies the clock, the deadline, the cost and the capital constraint; that skill decides whether to hold, trim, add or close | Whenever a clock enters its action window, or the user asks what to do with an open position |
| `equity-tax-lot-and-exit-management` | **Lateral — the tax-lot owner.** This skill supplies the 61-day wash-sale window and the one-year holding-period date; that skill selects the lot and handles the harvest | On any realised loss, and on any position within 30 days of the long-term barrier |
| `options-risk-engineer` | **Sibling policy set — the options-book analogue.** Same shape and the same one sentence, but **not numerically identical**: different coefficients (`0.15 × NAV` here, `0.20 × NAV` there), a different middle term (`WCSD`, a simultaneous drawdown, here; `WCML`, a simultaneous max loss, there) and different ladder rungs. An options book uses the options file, an equity-only book uses this one, and on a mixed account **this skill defers where the two disagree** | Whenever the account holds both equities and options, or the question is options-book risk |
| `options-position-lifecycle` | **Peer upstream** for accounts holding options — supplies the options-side decision | When the question concerns an open options position rather than an equity one |
| `portfolio-signal-manager` | **Upstream — the portfolio state.** Provides weights, NAV, exposures, drawdown and rebalance signals | At Phase 0 and Phase 5, and on any drawdown or rebalance signal |
| `market-data-engineer` | **Upstream — market data.** Prices, ADV, corporate action calendars, index membership, halts, data quality | Before any liquidity or event computation |
| `fundamental-analyst` | **Upstream — company facts,** including earnings and guidance dates | When a scheduled gap date must be established for a held name |
| `macro-strategist` | **Upstream — the regime read** and macro release calendar | At Phase 8, to name the current regime |
| `algorithmic-trader` | **Downstream — execution.** Executes the exit programme or the standing liquidation priority once a decision exists | When a reduction or exit programme has been decided |
| `trade-sizing-recovery` | **Peer.** Owns contract counts and loss bands for the position; this skill owns the clocks, the margin regime and the reserve that the size must respect | When the question is how many contracts or shares |
| `incident-responder` | **Reference — incident process** for a margin-call event, a forced liquidation, or a buy-in | When a CRITICAL escalation has occurred and a post-mortem is required |
| `financial-security` | **Reference — security review** before automating any part of this workflow with real money | Before deploying automated margin monitoring or liquidation logic |

## Gotchas

<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| The deadline was missed by two days and the trade settled anyway | The deadline was held as "3 business days" and traded on a Thursday, so the weekend silently absorbed two of them | Convert every business-day deadline to a date in the market's own calendar at the moment the trade is made, with the holiday assumption written down | **Business days are not calendar days, and they are not your business days.** The market's calendar governs |
| A "liquidity buffer" turned out not to be available on the day it was needed | The buffer was a position, or a money-market holding with its own settlement, rather than uncommitted buying power | Measure the reserve as uncommitted buying power, recomputed from live `total_BP` every time it is tested | **A reserve you have to sell something to reach is not a reserve.** It is a position with a hopeful name |
| The account was restricted for 90 days and nothing looked broken | A cash-account purchase was funded by unsettled sale proceeds: a good-faith violation under 12 CFR 220.8(c)(1), with a 90-calendar-day payment-privilege freeze | Fund cash-account purchases with settled cash only, and sequence sale then wait then buy | **Some failures do not appear in P&L.** The ability to transact is an asset with its own depletion risk |
| A short was bought in at a price nobody agreed to | A delivery failed, the buy-in ran to FINRA Rule 11810, and the notice was never answered in writing — which is deemed acceptance at 6:00 p.m. ET on the notice date | Answer every buy-in notice in writing the day it arrives; keep a locate available before the 3:00 p.m. ET cure deadline | **Notice is not the same as opportunity.** A notice with a deadline is a decision you have already been given |
| The exit cost doubled between the decision and the execution | ADV and spread were measured in the uptrend and never re-measured; the exit happened after a gap and a halt, into a thinner book | Re-measure weekly and immediately on the trigger list in `liquidity-and-exit-cost-planning.md` §5 | **Liquidity is a measurement, not a property.** The same position is liquid and illiquid at different times without changing |
| The reserve floor held perfectly and the account still got liquidated | Buying power itself shrank with the position values, so a reserve expressed as an absolute dollar amount became a smaller fraction of a larger requirement — and the requirement was computed after a gap | Recompute the floor from live `total_BP` every time it is tested, never cache it, and test the gapped case rather than the average day | **A reserve denominated in a shrinking quantity is not a floor.** It is a number that was true once |
