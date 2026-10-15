# Reg SHO, Fails to Deliver and the Threshold List

This is the equity market's own settlement-risk clock. It does not care about the holder's view, and
it does not offer a negotiation. Once a position is failing to deliver or once a security is on the
threshold list, a **forced close-out** is scheduled — and it executes at whatever price the market
offers on that day.

## §1 — The Close-Out Requirement: 17 CFR 242.204(a)

| Case | Close-out deadline |
|---|---|
| General fail to deliver | By the **beginning of regular trading hours on the settlement day following the settlement date** |
| Fail resulting from a **long sale** | By the **third consecutive settlement day** after the fail arose |
| Fail on a **Rule 144** / **deemed-to-own** position | Within **35 consecutive calendar days** |

**Source:** 17 CFR 242.204(a) (Rule 204, "Close-out requirement").

Three different clocks, three different lengths, one shared property: **all of them are counts, not
announcements.** Nobody calls the holder to say the count has started.

## §2 — Threshold Securities: 17 CFR 242.203(b)(3) and (c)(6)

A security lands on the SRO threshold list when:

```
fail-to-deliver positions ≥ 10,000 shares
        AND
fail-to-deliver positions ≥ 0.5% of the security's shares outstanding
for 5 consecutive settlement days
```

and a member holding a threshold position must **close out after 13 consecutive settlement days** of
fails. The security **drops off the list** when the fails return below **both** thresholds for
**5 consecutive settlement days**.

**Source:** 17 CFR 242.203(b)(3), 242.203(c)(6).

### §2.1 — Where each threshold binds [COMPUTED]

```
0.5% × shares outstanding = 10,000 shares
        → shares outstanding = 2,000,000
```

| Shares outstanding | Which leg binds | Threshold in shares |
|---|---|---|
| 1,000,000 | **10,000 shares** (0.5% would be 5,000) | 10,000 |
| 2,000,000 | both, exactly | 10,000 |
| 20,000,000 | **0.5%** (0.5% = 100,000) | 100,000 |

So for a company with fewer than two million shares outstanding the flat 10,000-share leg is the
binding threshold, and for anything larger the percentage leg is. A small-cap name can be placed on
the threshold list by a fail that would be invisible in a large cap.

### §2.2 — The two counters, and the one honest ambiguity

Both counters are counts of **consecutive settlement days**. Settlement days are business days on
which the market settles (see `settlement-and-payment-period.md` §1). A plain arithmetic read of the
retrieved rule text gives:

```
SETTLEMENT DAY   1        2        3        4        5        ...   13
                 │        │        │        │        │              │
list threshold   └────────┴────────┴────────┴────────┘
                 (5 consecutive settlement days of fails ≥ both legs → on the SRO list)
close-out        └────────┴────────┴────────┴────────┴── ... ──────┘
                 (13 consecutive settlement days of fails → mandatory close-out)
```

**The honest limit of the research:** the rule text retrieved does not settle whether the 13-day
counter begins on the first settlement day of the fail, or only once the 5-day list period has been
completed. Plan against the **earlier** of the two readings, and confirm the actual date against the
broker's own fail report — a firm that is holding a threshold position has that date in its systems,
and it is the firm that will execute the close-out.

## §3 — A Worked Timeline [COMPUTED]

Fails begin on **Monday 2026-03-02** in a security with 20,000,000 shares outstanding (so the 0.5%
leg binds at 100,000 shares) and 150,000 shares failing:

```
SETTLEMENT DAY  DATE            FAIL SHARES    ON LIST?   COUNTER
      1         Mon 2026-03-02    150,000        no          1
      2         Tue 2026-03-03    150,000        no          2
      3         Wed 2026-03-04    150,000        no          3
      4         Thu 2026-03-05    150,000        no          4
      5         Fri 2026-03-06    150,000       YES ←        5
      6         Mon 2026-03-09    150,000       yes          6
      7         Tue 2026-03-10    150,000       yes          7
      8         Wed 2026-03-11    150,000       yes          8
      9         Thu 2026-03-12    150,000       yes          9
     10         Fri 2026-03-13    150,000       yes         10
     11         Mon 2026-03-16    150,000       yes         11
     12         Tue 2026-03-17    150,000       yes         12
     13         Wed 2026-03-18    150,000       yes         13  ← close-out required
```

150,000 shares is ≥ 10,000 and ≥ 0.5% × 20,000,000 = 100,000, so both legs are satisfied throughout
[COMPUTED]. The dates are business-day arithmetic on the March 2026 calendar; the *convention* for
starting the 13-day counter is the ambiguity named in §2.2, and the conservative reading puts the
deadline at the earlier date shown.

**What this looks like to the holder.** The borrow disappears first — a security on the threshold
list is unattractive to lend, so the locate dries up and the desk prices what remains accordingly.
Then the close-out arrives. A short position in a threshold name is on a countdown from the day the
fails start, whether or not the fails are the holder's own.

## §4 — What the Holder Actually Controls

Almost nothing, which is the point of writing it down:

| Thing | Controllable? | What to do |
|---|---|---|
| Whether fails occur | Partly — a fail is a delivery failure, and a short seller who locates and delivers does not create one | Deliver. Do not let a locate expire unfilled |
| Whether the security goes on the list | No — it depends on the market's aggregate fails | Monitor the list; treat membership as a change in the position's risk, not as news |
| The 13-day close-out | No | Plan the exit *before* the counter could reach 13, not after |
| The price at close-out | No | Reduce size while the book is still two-sided |

## §5 — Reading the List

- **Threshold lists are published per SRO** and are the authoritative artifact. Any list reproduced
  from memory is worthless; the list changes daily.
- **Membership is a rolling condition**, not a status. A name can enter and leave repeatedly, and
  each entry restarts a count.
- **A name on the list is not automatically hard to borrow by rule** — but a lending desk's response
  to it is a commercial decision (see `short-borrow-and-buy-in-mechanics.md` §1). This is why the
  borrow status is tagged [BROKER-VERIFIED] and the list membership is tagged [VERIFIED — the SRO's published threshold list, with the read date].

## §6 — Failure Modes

1. **Treating the close-out as a deadline the firm will remind you about.** It will not.
2. **Sizing a short in a name whose shares outstanding are small.** The 10,000-share leg can be
   crossed by a single market participant's fail.
3. **Assuming the 35-calendar-day Rule 144 clock is generous.** 35 calendar days can be 23 or 24
   settlement days; it is longer than the general rule but it is not long.
4. **Confusing the failure clock with the recall clock.** Recall has no rule-fixed period; the
   fail has three different ones.
5. **Holding a threshold position while waiting for a thesis to work.** The clock is not interested
   in the thesis.
6. **Working from a memorised threshold list.** The list is daily.
7. **Assuming a long-sale fail has the same deadline as a short-sale fail.** Long-sale fails get the
   third-consecutive-settlement-day rule.
8. **Believing the exit at close-out will be orderly.** The firm closes it out; it does not work the
   order for two weeks first.

## §7 — Verification

- [ ] Every short position reports a fail age where a fail exists.
- [ ] Threshold-list membership has been read from the SRO's current list, with the read date.
- [ ] Where the 13-day deadline is quoted, the start-convention ambiguity in §2.2 is stated.
- [ ] No threshold list has been reproduced from memory.
- [ ] The exit plan for any threshold position pre-dates the 13-day counter's first possible expiry.
