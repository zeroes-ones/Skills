# Specific Identification Mechanics — choosing the lot on the ticket

> **Read this first.** The rule this file describes — selling a chosen lot rather than the
> broker's default — is governed by regulation. This skill names the governing regulation but
> **did not confirm its current text during research**, so nothing here about the *requirement*
> is tagged `[VERIFIED]`. Everything in this file that describes *broker behaviour* is
> `[BROKER-VERIFIED]` and is true of some brokers and not others. **Verify before relying on
> it**, and treat an unconfirmed assumption here as a risk, not a rule.

## The governing question

When a sale consumes shares, whose choice decides *which* shares? There is only one of two
answers, and the holder must know which one is in force before the order is sent.

1. A **default** applies — the broker's standing method. First-in-first-out, average cost, or
   another specified default.
2. A **specific identification** applies — the holder names the lots, and the broker records
   the naming.

If the holder does not know which of these is in force, the tax bill is being set by an
unexamined setting. That is the defect R1 exists to prevent.

## What the regulation is, and what is not claimed

`Treas. Reg. §1.1012-1(c)` is the regulation identified as governing the identification of
the shares or securities sold. This skill states that identification it identifies that
regulation, names it so a reader can read the current text, and **stops there**.

- It is **not** claimed here that the regulation requires any particular procedure.
- It is **not** claimed here that any broker's procedure satisfies it.
- It is **not** tagged `[VERIFIED]`, because the research pass did not confirm the current
  text. An unverified tax citation is exactly the defect this library was built to avoid.

The practical instruction that follows from this is short: **read the regulation and your
broker's published procedure before you rely on a specific identification to change your
tax.** Anything else is an assumption with a price attached.

## What a broker's procedure typically involves `[BROKER-VERIFIED]`

The shapes below are the common ones. None of them is universal, and the details — cut-off
times, channels, confirmation format — differ by firm, account type and sometimes security
type.

| Shape | How it works | Where it usually breaks |
|---|---|---|
| Per-trade instruction on the order ticket | A lot-relief or share-selection field on the sell ticket names the lots | Field missed; the ticket defaults silently |
| Standing election on the account | A one-time election sets a method for all future sales | The election may only be changeable under conditions, and may apply per account not per holder |
| Written instruction before the sale | A message to the desk describing the lots, timestamps and content preserved | Timing: an instruction sent after the fill may be too late |
| Post-trade confirmation request | Some firms permit a same-day correction under a published procedure | Not universal; may carry a fee or a restriction |
| No mechanism at all | The broker applies its default and offers no per-trade choice | The only remaining lever is to change the default itself, if it can be changed |

**The single most important sentence in this file:** the requirement and the deadline must be
verified with the broker, in writing, before the sale. A confirmation obtained afterwards is
a hope, not a record.

## A ticket-writing template

Whatever the mechanism, the instruction has enough content to be unambiguous. A usable
instruction names:

1. **Security and account**, unambiguously.
2. **Quantity to sell**, and whether the sale is all of the named lots or part of each.
3. **Each lot by its acquisition date and per-share basis** — not by "the oldest" or "the
   long-term ones".
4. **The quantity consumed from each lot**, so a partial-lot consumption is recorded.
5. **The action requested**, in the broker's own vocabulary for its lot-relief field.
6. **A timestamp and a copy**, kept with the trade record.

An instruction that says "sell my oldest 100 shares" has delegated the identification back
to the broker. It is a default in disguise.

## Average cost, and why it can be a one-way door

`[BROKER-VERIFIED]` Where an average-cost method applies to a holding — commonly, but not
only, for certain fund holdings — the consequences differ from the lot view:

- Every share of that holding carries the same basis per share.
- Lot selection may not be available for that holding at all.
- Certain elections may apply to all holdings of the same security, and may be difficult or
  impossible to reverse for shares already held.
- Some security types do not permit average cost at all.

The operational consequence for this skill is severe and simple: **if an average-cost method
is in force for a holding, the lot-selection ladder does not apply to it.** The correct
output is a one-line statement of that fact, not a four-row candidate table.

## The five questions to ask the broker, in writing

1. What is this account's default lot-relief method today?
2. Can it be changed? By what process, and does the change apply prospectively only?
3. Can I name specific lots on a single order? Through which channel, and by what cut-off
   time relative to the fill?
4. What confirmation will I receive that the naming was applied, and in what form?
5. If the wrong lots are consumed, is there a same-day correction procedure, and what does it
   cost?

The answers belong in the state log field `default_relief_method`, with the date they were
obtained. An answer more than a year old is a hypothesis.

## Documentation duty

The holder is the one who has to defend the position later, so the holder keeps:

- The instruction as sent, with a timestamp.
- The broker's acknowledgement, if one exists.
- The trade confirmation and the resulting lot quantities.
- The refreshed lot table after the sale.
- The reason the sale was made, in the ledger row, with the non-tax reason written first.

Five items. They take two minutes and they are the difference between a decision and an
accident.

## Failure modes

1. **What goes wrong — the ticket with no lot field.** The sale fills, the default applies, and the lowest-basis lot is gone. Nothing errors; the cost is simply never measured.
2. **What goes wrong — the late instruction.** The lot naming was sent after the fill or after the broker's cut-off. Whether it can still be applied depends on a procedure that was never read.
3. **What goes wrong — the ambiguous instruction.** "The oldest shares" is a default; "the 2024-01-31 lot of 100 shares at $50.00" is an identification. Only one of them is a decision.
4. **Worst case — the average-cost assumption.** A plan is built on choosing lots in a holding where lot choice does not exist; the plan cannot be executed and the exit is re-planned under time pressure.
5. **What goes wrong — the stale answer.** The procedure was confirmed two years and one broker merger ago. The default changed. Nobody re-asked.
6. **Known limitation — this file cannot tell you your broker's rule.** It can only tell you which questions to ask and what to write down.
7. **Edge case — correction after the fact.** A same-day correction may exist at one firm and not at another, and may be unavailable once the trade has settled.

## Checklist

- [ ] The default lot-relief method is recorded, with the date it was confirmed and its source.
- [ ] The process for a per-trade instruction is recorded, in the broker's own vocabulary.
- [ ] The cut-off time for the instruction is recorded, in the account's time zone.
- [ ] The confirmation format is known, and a sample has been seen.
- [ ] The correction procedure, if any, is recorded with its cost.
- [ ] Whether an average-cost method applies to this holding is recorded.
- [ ] Every sale's instruction is written before the order and kept with the trade record.
- [ ] The lot table is refreshed from the broker's export after every sale.
