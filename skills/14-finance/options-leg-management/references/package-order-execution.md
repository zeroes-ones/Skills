# Package Order Execution

Ground Rule R2 says a same-structure change goes as ONE multi-leg order at a single net price.
This file explains why that is an economic rule rather than a stylistic preference, what to do
when a venue rejects the package, and how to sequence a split without ever creating naked risk.

## Why the package usually fills better

A multi-leg structure's legs are not equally liquid. A body near the money is liquid; a far wing
several strikes out may trade rarely. Single-leg execution prices each leg in **its own** market,
so the illiquid leg is the one that sets the worst price.

| Leg type | Typical liquidity | What a lone fill costs |
|---|---|---|
| Near-the-money body | Deep book, tight spread | Little — this is the leg that looks fine when legged |
| Adjacent strike (one or two away) | Reasonable | Modest |
| Far wing (3+ strikes out, low OI) | Thin, wide, sometimes one-sided | Can consume the structure's entire remaining edge |
| Very short-dated short leg (a few cents) | Nominal quotes, often no real size | A market order here can fill at the worst tick in the book |

The illusion is that the **liquid** leg looks better when legged. It usually is slightly better in
isolation. The judgement must be made on the structure's **net**: `package fill` versus
`sum of the individual fills`. `[COMMON-PRACTICE]` The desk's observation, from its own fill
records, is that packages win the comparison on far-wing structures far more often than
single-leg execution does; the exact rate is book- and product-specific and should be measured
on your own fills, not assumed.

## The package-first order of operations

```text
   1. Draft the change as ONE complex order at a net price.
   2. Price it relative to the natural: the natural is the midpoint of the package's
      combined bid/ask. A first draft at or slightly inside the natural is normal.
   3. Submit. If it fills, log the fill and the slippage versus the natural in the
      structure's own units.
   4. If it is rejected:
        ├── widen ONCE, by roughly 10% of the structure's remaining edge
        │       └── fills ──▶ log
        └── rejected again ──▶ SPLIT, using the coverage-derived sequencing rule
   5. Record the rejection: venue message text + timestamp, in the ledger row.
```

Two widenings is the limit. Beyond that, the price you are accepting is evidence that the
operation is no longer the one you designed, and the right answer is to not trade that leg today.

## The sequencing rule — derive it, never remember it

When a package must be split, the only safe order is the one whose **intermediate states are all
defined-risk**. That order is structure-specific and is derived from the coverage map:

| Structure | Protecting leg | Safe split order | The order that is FORBIDDEN |
|---|---|---|---|
| Spread (long + short) | the long | buy back the short FIRST | sell the long first → naked short |
| Fly `+1K1 / −2K2 / +1K3` → vertical | K1 (and K3, both wings) | buy back K2 FIRST | sell K3 first → 2 naked shorts |
| Fly → long-only | both wings | buy back both K2 bodies FIRST | sell K3 alone → 1 naked short + 1 short body |
| Iron condor, one side | each side's long wing | close the side's short FIRST, then its long | close the long first → naked short |
| Calendar | the long BACK leg | close the short FRONT leg first | close the back leg first → naked short front |
| Collar / covered call | the stock position (or a higher long call) | close the short call first, then the shares | closing the shares first → naked short call |

The last two rows are the ones people get wrong by memorizing. **For any structure, the rule is:
close the SHORT that would be uncovered before you close its cover.** Write the coverage map down
for the specific structure in front of you, then read the sequence off the map.

```text
   coverage map, worked for a calendar:
       -1 x <front>C      covered by  ->  +1 x <back>C
       +1 x <back>C       covers      ->  -1 x <front>C

   split order: close -1 x <front>C first  -> state: +1 x <back>C  (long only) PASS
                 then close +1 x <back>C   -> state: flat                     PASS

   the reverse order gives -1 x <front>C alone -> NAKED SHORT CALL           FAIL
```

## Order types and their hazards on this desk

| Order type | Where it helps | Where it bites |
|---|---|---|
| Complex / package at a net price | Every same-structure change | Venue support is not universal for 4+ legs; verify |
| Limit on a single leg | Only after a package rejection | The far wing may never trade at your limit; a partial fill is a state you must test |
| Market on a single leg | Nowhere in this skill | On a thin leg it fills at the worst available price; on a cheap short it can fill at several multiples of the mid |
| Stop on a single leg | Nowhere in a multi-leg structure | A stop on a far wing with no bid fills at whatever exists; the trigger and the fill can be far apart |
| Complex order with a time-in-force beyond the session | Rarely needed | The structure's other legs move while your order rests |

`[VERIFIED]` US options exchanges provide complex/package order types that execute at a single net
price; the specific types, supported leg counts and matching rules are venue-specific and are set
out in the exchange rulebooks (for example the CBOE rulebook's provisions on complex orders).
Verify against the exchange you route to — do not assume a type name or leg limit.

## Session eligibility

A leg operation can be blocked by the session, not by the market.

| Session | What to check |
|---|---|
| Regular session (US equity options) | The default; the widest book for most names |
| Pre-market / after-hours | Equity options generally do not trade the underlying's extended session. Do not draft an options leg order for a session in which the options market is closed |
| Expiry-day late session | Liquidity thins before the close; the pin guard's 15:45 ET working deadline exists precisely because the close is the point after which the toolkit narrows |
| Index options | Last-trading-day and settlement conventions can differ from the underlying's; verify per product |

`[BROKER-VERIFIED]` Session availability, order-type support and leg-count limits are
broker-specific. Verify against your broker's documentation rather than assuming; and note that
session and product conventions change over time, so a remembered rule may be stale.

## What to log for every execution

| Field | Why it matters |
|---|---|
| Package as drafted (legs, sides, net price) | Reproduces the intent, not just the outcome |
| Natural at drafting time | The benchmark for slippage |
| Fill (legs, sides, net price, timestamp) | The only truth; the basis is derived from this |
| Slippage vs. the natural, in structure units | Feeds the counterfactual study |
| Rejection message and timestamp, if any | Proves the split was a fallback, not a choice |
| Sequencing used, if split | Proves the intermediate states were defined-risk |
| Post-fill leg list with the R1 result | The safety artifact |

## Anti-patterns

| ❌ | Why | ✅ |
|---|---|---|
| ❌ Legging "to get a better price on the liquid leg" | Judging the operation by one leg instead of the net | ✅ Compare package fill against the sum of individual fills, on the structure's net |
| ❌ Splitting a fly package by selling the wing first | Passes through a two-naked-short state | ✅ Buy back the body first |
| ❌ Splitting a calendar by closing the long back leg first | Leaves a naked short front leg | ✅ Front leg first; derive from the coverage map |
| ❌ Market orders on thin legs to "just get it done" | The fill can exceed the structure's remaining edge | ✅ Limit orders; widen once; then stop for the day |
| ❌ Assuming your venue supports a 4-leg package with your order type | Support and leg limits are venue-specific | ✅ Verify, and have the sequencing fallback written before you need it |
| ❌ Widening repeatedly without limit | You are no longer trading the operation you designed | ✅ Two attempts, then stop for the session |

## Sources, provenance and limits

- `[VERIFIED]` US options exchanges provide complex/package order types that execute at a single
  net price: CBOE and other US options exchange rulebooks. Exact type names, supported leg counts
  and matching algorithms vary by venue and by product.
- `[VERIFIED]` A listed option is separately exercisable; an uncovered short carries unbounded
  (call) or strike-to-zero (put) risk: OCC standard options disclosure document.
- `[BROKER-VERIFIED]` Order-type availability, session eligibility and leg-count limits are
  broker-specific and change over time. Verify; do not assume.
- `[COMMON-PRACTICE]` The two-widening limit, the "10% of remaining edge" widening step, and the
  desk's fill-quality observations are conventions backed by this desk's own records, not by a
  vendor-independent study. Treat the fill-quality claim as a hypothesis to test on your own
  fills, not as a measured result.
- Nothing here is financial advice or a **guarantee** of execution quality. Past performance of a
  routing approach does not predict the next fill, and the figures the desk records are
  approximate once a quote has gone stale.
