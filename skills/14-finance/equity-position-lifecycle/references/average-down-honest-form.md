# Average Down: The Honest Form

Averaging down is the most reflexive action in equity investing and one of the most expensive. It feels like discipline ("I am buying what I already believe in, cheaper") and behaves like leverage (I am adding risk to a position that has just been marked wrong by the market).

This file is not an argument against averaging down. It is the gate that separates the two cases, and the arithmetic that shows what the action actually buys.

**Portability target:** spec-level. The gate is a decision procedure; every number in it is supplied by another skill.

## Why equities are different from options here

The options lifecycle has an escape hatch: a defined-risk restructure. You can convert an unstructured position into a bounded one, and the bounded form is a legal way to spend more money on a thesis because the worst case is now known.

**Equities have no such structure.** A larger equity position has a larger worst case, full stop. There is no conversion that bounds it, no spread that caps it, no wing that absorbs it. The only thing that can make an average-down safe is a gate, and the gate has to be applied before the order rather than after the regret.

That single asymmetry is why the gate below has five clauses and no discretionary bypass.

## The five-clause gate

All five. A failure on any clause is an answer: **CUT**, not a delay, not a smaller add.

### Clause 1 — The thesis is re-underwritten to the *lower* price

The test is not "do I still like it". It is: does the written thesis still hold **at the price the market is now offering**, and does the re-underwrite produce a *new*, lower invalidation level?

- "It's cheaper now" fails this clause by construction. Cheapness relative to your own entry price is not information about the company; it is information about your basis.
- "Nothing has changed" fails it too, because something has changed: the market has repriced the name, and the re-underwrite must account for why.
- **Evidence of a pass:** a dated, written paragraph that names what the market now believes, why that is wrong, and the lowest price at which the thesis would still be true.

### Clause 2 — Blended basis and blended break-even, recomputed and written down

Both numbers, before the order.

- Blended basis: the total cost of all shares divided by the total shares.
- Blended break-even: the price at which the position is flat, including the exit costs you would actually pay.

The point of writing them down is that they move less than people assume. See the arithmetic below.

### Clause 3 — The total position after the add is still inside the per-idea band

This is where most real average-down proposals die. The band is 10% of the book per position, 25% per sector [VERIFIED — the caps published in `portfolio-signal-manager`].

- **What it means operationally:** averaging down is only possible on a position that was *undersized to begin with*. If the position was already at its band, the arithmetic forbids the add regardless of how good the thesis is.
- **Why the rule is not arbitrary:** a position at its band that gets larger is a concentration decision taken as a side effect of a valuation decision. Those are different decisions and they deserve to be made separately.

### Clause 4 — A written invalidation level for the enlarged position

The original level was written for the original size. A bigger position needs its own level, decided in advance, because the cost of being wrong is now larger.

### Clause 5 — A stated maximum number of adds

State one, in advance, in the record. **One.** The gate's own logic requires it: each add must re-pass clause 1, and a thesis that has been re-underwritten twice at successively lower prices has usually stopped being a thesis and started being a narrative. A maximum of one add is the honest default; a maximum of two is defensible for a position deliberately built in thirds; anything beyond that is averaging *into* a loss rather than averaging *down* a price.

## What the arithmetic actually buys

An original position of 500 shares at $80.00, now trading at $64.00.

| Item | Value | Formula |
|---|---|---|
| Original cost | **$40,000** | 500 × 80.00 = 40,000 [COMPUTED] |
| Add: 250 shares at $64.00 | **$16,000** | 250 × 64.00 = 16,000 [COMPUTED] |
| Shares after | 750 | 500 + 250 = 750 |
| Blended basis | **$74.67** | (40,000 + 16,000) ÷ 750 = 74.67 [COMPUTED] |
| Break-even from $64.00, before the add | **+25.0%** | (80.00 ÷ 64.00) − 1 = 25.0% [COMPUTED] |
| Break-even from $64.00, after the add | **+16.7%** | (74.67 ÷ 64.00) − 1 = 16.7% [COMPUTED] |
| Recovery requirement bought | **8.3 points** | 25.0 − 16.7 = 8.3 [COMPUTED] |
| Shares added | **+50%** | 250 ÷ 500 = 50% [COMPUTED] |
| Capital added | **+40%** | 16,000 ÷ 40,000 = 40% [COMPUTED] |

Read the last two rows together with the row above them. **Eight points of recovery were bought with four-tenths more money, on a thesis that has not yet been re-underwritten.** If the re-underwrite in clause 1 fails, the eight points were bought at the price of a permanently larger loss.

Scale it to see the shape of the risk: if the position goes to $56.00 after the add, the loss is larger by exactly the added capital times the further decline, and there is no structural floor underneath it.

## What the band usually says

The same proposal, on a $250,000 account:

- Original position $40,000 = **16%** of the book [COMPUTED]: 40,000 ÷ 250,000 = 16.0%.
- Band = 10% = **$25,000** [VERIFIED — `portfolio-signal-manager` cap].
- The position is already **$15,000 over** the band [COMPUTED]: 40,000 − 25,000 = 15,000.
- The proposed add of $16,000 would take it to **$56,000 = 22.4%** [COMPUTED]: 56,000 ÷ 250,000 = 22.4%.

**Clause 3 fails before the thesis is even discussed.** That ordering is intentional: a position that is already oversized has a problem that predates the add proposal, and the correct next action is a trim back inside the band — not a larger bet on the same name.

## The audit trail

Every average-down proposal produces a record, pass or fail:

```text
proposal:          average down, 250 sh at 64.00 on a 500 sh position (basis 80.00)
clause_1_thesis:   FAIL — "it's cheaper now" is not a re-underwrite; no new level produced
clause_2_blended:  74.67 [COMPUTED] (40,000 + 16,000) ÷ 750 — computed, but moot given clause 1
clause_3_band:     FAIL — 22.4% post-add against a 10% band [COMPUTED]
clause_4_level:    not reached
clause_5_max_adds: not reached
disposition:       CUT. The gate failed at two clauses; a failure is an answer, not a delay.
queued:            trim back toward the band on the next rung, or CLOSE on a broken thesis
```

A refusal recorded this way is evidence. A refusal remembered as "we decided not to" is not.

## Rejection examples, and what they teach

| Proposal | Clause that fails | Lesson |
|---|---|---|
| "It's down 20%, so it's on sale" | 1 | The entry price is not a valuation input |
| "I'll bring my basis down so I can get out flat sooner" | 1 | The blended basis does not change the company |
| "Just a small add, nothing structural" | 3 or 5 | Small adds still fail the band and still consume the maximum |
| "The thesis is fine — I checked" | 1 | Clause 1 requires a written, dated artifact, not a checkmark |
| "I'll add here and add again if it goes lower" | 5 | A maximum stated in advance is the whole point of clause 5 |
| "It's a long-term hold, so the level doesn't matter" | 4 | Long duration is not the absence of a level |

## Failure modes

1. **The reflexive add.** The add is triggered by the price, not by the gate. Countermeasure: the five clauses are recorded before the order, with the clause numbers in the record.
2. **The averaged-down position that becomes the largest risk in the book.** Countermeasure: clause 3 is computed post-add and shown in dollars.
3. **The maximum that grows.** "One add" becomes two, then three, each with a story. Countermeasure: the add count and the maximum are both fields in the record.
4. **The re-underwrite replaced by a restatement.** The same sentences are copied forward with a new date. Countermeasure: clause 1 must produce a new, lower invalidation level.
5. **The level written for the original size only.** Countermeasure: clause 4 requires a level for the enlarged position.
6. **The tax consequence of the new lot ignored.** The added shares are a new lot with a new acquisition date, which changes which shares a later sale touches and can interact with wash-sale timing. Countermeasure: flag the lot interaction to `equity-tax-lot-and-exit-management`.
7. **Averaging down a name inside a wash-sale window.** A purchase in the name can void a recently harvested loss [VERIFIED — IRC §1091]. Countermeasure: the wash-sale flag from the health check blocks the add outright.
8. **The add funded by selling a winner.** That is a rotation, and a rotation has its own friction arithmetic. Countermeasure: route it to rung 3.

## What the honest form looks like when it passes

An average-down that passes all five clauses is a legitimate action, and it is recognisable:

- The position was small relative to the band, so clause 3 passes with room to spare.
- The written re-underwrite names what the market believes and why it is wrong.
- The blended basis and break-even are on the page.
- The enlarged position has its own level, lower than the original and justified by the re-underwrite.
- The maximum add count is one, stated before the order, and it is now spent.

That set of conditions is rare, which is the point. The gate exists so that when it passes, the action is genuinely different from the reflex — not so that it can be argued past.
