# House-Money Conversion — turning a fly into a free long-only runner

The conversion takes a fly `+1× K1 / −2× K2 / +1× K3` and leaves `+1× K1` alone. Done at the
right moment it is the cheapest defined-risk conversion in the catalog. Done at the wrong moment
it is a `$475` `[COMPUTED]` debit described as "free".

## The package

```text
  buy  2 x K2      (close both short bodies)
  sell 1 x K3      (close the far wing)
  keep 1 x K1      (the runner)
  → ONE package, one net price
```

Nothing else is legal. Selling the wing alone, or buying one body alone, leaves a shape that is
not the original position and not the intended one (see
`(references/no-naked-risk-guardrails.md)`).

## The subtrahend — the only number that matters

```text
  conversion net debit per unit  =  2 x K2_mid  -  1 x K3_mid      (in premium, per share)
  conversion net debit per unit  =  that x 100 x units            (in dollars)
```

If that number is not computed from live quotes, the conversion is not priced. Two regimes:

| Regime | Typical shape | Verdict |
|---|---|---|
| Bodies still rich (spot at or near the body, DTE > ~5) | `2 × K2` large, `K3` small → net debit large | Do not convert. Wait for decay, or scale out whole units instead |
| Bodies decayed (spot has left the body, DTE ≤ ~3) | `2 × K2` small, `K3` small → net debit small | Convert. This is where "house money" becomes a true description |

Worked contrast from `(references/leg-arithmetic-worked-examples.md)`:

```text
  Example C (bodies rich):  2 x 3.05 - 1.35 = $4.75 per unit = $475 per unit   [COMPUTED]
  Example D (after decay):  2 x 0.25 - 0.05 = $0.45 per unit = $45  per unit   [COMPUTED]
  retained runner value in Example D ≈ $155 per unit                          [ESTIMATED]
  cost as a share of the runner = 45 / 155 = 29%                              [COMPUTED]
```

Same operation, same structure, `10.6×` different cost `[COMPUTED]`. Timing is the entire edge.

## The free-runner test

"Free" is a claim about cumulative cash, not about the last ticket. Run it explicitly:

```text
  free-runner test:
      realized_proceeds  =  sum of cash from scale-outs of this structure
      total_entry_debit  =  units_at_entry x entry_debit_per_unit
      conversion_cost    =  units_remaining x conversion_debit_per_unit
      net = realized_proceeds - total_entry_debit - conversion_cost
      runner is FREE if net >= 0
```

Worked (Example E): `realized $925 − total debit $405 − conversion $45 = +$475` `[COMPUTED]` from
`[ESTIMATED]` fills → free. The counter-check after only **one** scale-out gives
`455 − 405 − 90 = −$40` `[COMPUTED]` → not free. Both figures come from the same arithmetic on
different inputs, which is why the test must be run rather than remembered.

## Order of operations

```text
   1. trigger fires (>= 2x, or a known event inside the remaining life)
        │
        ▼
   2. have you taken the scale-out rungs you planned?
        │   ├── NO  ──▶ take them first (whole units). Realized proceeds are
        │   │            the numerator of the free-runner test
        │   └── YES ──▶ continue
        ▼
   3. compute the subtrahend from LIVE quotes:  2 x K2_mid - 1 x K3_mid
        │   ├── the result is large ──▶ do not convert; re-check after decay
        │   └── the result is small ──▶ continue
        ▼
   4. run the free-runner test
        │   ├── net < 0  ──▶ the runner is NOT free. Say so out loud, then
        │   │                 decide whether you want to pay for it anyway
        │   └── net >= 0 ──▶ continue
        ▼
   5. submit ONE package; ledger row FIRST (tag HM); log fill; re-arm the
      runner's own take-profit rung
```

## Why event dates change the calculus

An event inside the remaining life does two things at once: it inflates the wing's value (good —
the sell side of the package gets richer) and it inflates the bodies' value (bad — the buy side
of the package gets more expensive). The net effect on `2 × K2 − 1 × K3` is usually adverse before
the event, because the body is closer to the money and carries more vega than the wing.

```text
  pre-event:  2 x K2 - 1 x K3 is at its WIDEST  → conversion is expensive
  post-event: 2 x K2 - 1 x K3 is at its NARROWEST → conversion is cheapest,
              but the wing may also have collapsed, so the runner may be worth
              little
```

That tension is why the desk treats "event ahead" as a reason to **monetize into the spike**
rather than to hold: the wing's IV value is the part that a known event pays for, and the wing's
directional value after the event is a separate, unmodeled bet. `[COMMON-PRACTICE]`

## The runner after the conversion

After `HM`, what remains is a single long call `+1× K1`. It needs its own plan, not the fly's:

| Item | What to set |
|---|---|
| Take-profit rung | An explicit price, not "when it looks good". A common desk convention is to monetize a runner whose value reaches about 3× its own cost basis, in whole units |
| Time stop | A DTE at which the runner's remaining theta no longer justifies the capital it ties up |
| Event rule | If an event lands inside the runner's life, the spike is the exit — do not hold a naked long through a known event expecting a second spike |
| Capital note | The runner's risk is the premium already paid; it must still be counted in the position ledger and in the capital plan |
| Ledger | The conversion row (tag `HM`) and, if the runner is later scaled, its own `SC` row |

## Anti-patterns specific to this conversion

| ❌ | Why it fails | ✅ |
|---|---|---|
| Converting because the fly is "up 2×" without pricing the bodies | The bodies may still be rich; the conversion is then a large debit mislabeled as free | Compute `2 × K2_mid − 1 × K3_mid` first |
| Converting one unit of a multi-unit fly and leaving the others whole | Legal, but it creates two structures with two plans — and if the unit count is not respected it fractionates legs | Convert whole units; give each remaining unit its own rung |
| Selling the far wing in a separate ticket after buying the bodies | The intermediate state is `+1 K1 / +1 K3` — a long strangle, not the plan | One package, always |
| Calling the runner "free" because the fly was profitable once | Free is a cumulative-cash statement; run the free-runner test | Run the test, state the number |
| Holding the runner through the event that motivated the conversion | You converted to remove event risk, then re-took it | Monetize into the spike; the runner's spike is the exit |

## Sources, provenance and limits

- `[VERIFIED]` A listed option is separately exercisable and a multi-leg position is not one
  instrument to the exchange: OCC standard options disclosure document, US options exchange rules.
- `[VERIFIED]` US options exchanges provide complex/package order types that execute at a single
  net price: CBOE and other US options exchange rulebooks.
- `[COMPUTED]` Every figure above is arithmetic on stated inputs; the full derivations are in
  `(references/leg-arithmetic-worked-examples.md)`, Examples C, D and E.
- `[ESTIMATED]` The illustrative quotes are approximate and chosen for readability. Real quotes
  on cheap legs are indicative and can be stale — a fill is not a guarantee of the model.
- `[COMMON-PRACTICE]` The event-versus-decay tension, the runner's 3× monetization convention and
  the "state the number out loud" rule are desk conventions, not exchange rules.
- Past performance of this conversion on one book does not predict its next result; the
  arithmetic is only as good as the quotes it is fed.
