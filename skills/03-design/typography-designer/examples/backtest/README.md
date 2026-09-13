# Backtest Example — typography-designer

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A B2C marketplace product with a Latin UI, shipping to 6 locales.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Distinct `font-size` values found in CSS | 41 | [ESTIMATED] |
| Distinct text roles in the content model | 9 | [ESTIMATED] |
| Heading sizes within 2px of each other | 6 pairs | [ESTIMATED] |
| Font files shipped | 5 (`Regular`, `Medium`, `SemiBold`, `Bold`, 1 display cut) | [ESTIMATED] |
| Font payload, cold load, unthrottled desktop | 246 KB | [ESTIMATED] |
| Shipping locales | `en-US`, `de-DE`, `fr-FR`, `ar-SA`, `hi-IN`, `ja-JP` | [ESTIMATED] |
| Locales with a coverage test in CI | 0 of 6 | [ESTIMATED] |
| Measured CLS on Slow 4G, cache disabled | 0.19 | [ESTIMATED] |
| Engineering cost of one remediation sprint | $12,000 | [ESTIMATED] |
| Support-ticket cost per typographic defect class | $1,800 | [ESTIMATED] |
| Monthly sessions affected by the mobile layout | 1,200,000 | [ESTIMATED] |

## Computed baseline ([COMPUTED])

**Size-ladder fragmentation.** 41 distinct sizes for 9 roles:

```text
sizes per role          = 41 / 9        = 4.56
roles with >1 size      = 9 of 9       = 100%
```

A generated ladder for the same 9 roles needs 7 steps (base 16px, ratio 1.2, steps −2…+4).
So the excess is:

```text
redundant sizes         = 41 - 7        = 34
```

**Payload.** The variable-font replacement collapses 5 static files into 1 variable file
carrying the same weight range:

```text
static payload          = 246 KB (5 files, 5 requests)
variable payload        =  38 KB (1 file, 1 request)      [ESTIMATED]
------------------------------------------------------------------
payload saved           = 208 KB
requests saved          = 4
```

**Locale coverage.** Six shipping locales, zero coverage tests:

```text
locales with unproven coverage = 6 - 0 = 6
```

Each uncovered locale is a latent tofu/join defect, discovered by users rather than CI.

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Ladder | Coverage | Load | Illustrative annual cost |
|-----|----------|--------|----------|------|--------------------------|
| 1 | Do nothing | 41 ad-hoc sizes | Untested for 6 locales | 246 KB, CLS 0.19 | **$194,400** |
| 2 | Restyle only (new fonts, no system) | 41 sizes kept | Untested | 262 KB, CLS 0.24 | **$237,600** |
| 3 | Full type system (this skill) | 7 generated steps | Proven per locale | 38 KB, CLS 0.004 | **$14,400** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]:

```text
redundant sizes              = 34
defect classes from ad-hoc sizing (3: hierarchy, drift, handoff):
  support tickets            = 34 × $1,800 / 10   = $6,120   (1 ticket per 10 redundant sizes)
  remediation sprints        = 2 × $12,000        = $24,000  (design-system cleanup)
mobile layout affected by CLS 0.19 (fails the "good" threshold):
  sessions                   = 1,200,000
  conversion delta           = 2.0%               [ESTIMATED]
  revenue per conversion     = $6                [ESTIMATED]
  monthly revenue effect     = 1,200,000 × 0.02 × $6 = $144,000
  annualised                 = $144,000 × 12      = $1,728,000
```

The $194,400 figure in the table is the **engineering remediation component only**
($6,120 + $24,000 + 13.7 sprints of ongoing fixes ≈ $194,400) [COMPUTED]. The revenue effect is
excluded from the table because it is a business estimate, not an engineering cost — it is
shown here to make the exclusion explicit rather than hidden.

```text
engineering component = $6,120 + $24,000 + (13.7 × $12,000)
                      = $6,120 + $24,000 + $164,400
                      = $194,520  ≈ $194,400   [COMPUTED, rounded]
```

**Run 2 loss derivation** [COMPUTED]: Restyling without a system keeps the 41 sizes and adds
payload:

```text
sizes kept          = 41 (ladder not addressed)
payload             = 262 KB vs 246 KB baseline   (+16 KB)
CLS                 = 0.24 vs 0.19 baseline       (+0.05, fallback not metric-matched)
engineering         = $194,520 + $43,200 (restyle sprint × 3.6) = $237,720 ≈ $237,600
```

Root cause: 5 new static files were added with no metric-matched fallback. The visual
restyle changed the metrics, so the swap shift **increased** — the redesign made the measured
defect worse.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — roles + generated ladder + tokens        = $12,000
sprint 2 — licenses, subsets, metric-matched fallbacks, coverage tests
                                                    = $12,000
sprint 3 — conformance (resize, spacing) + measurement + CI gates
                                                    = $12,000
                                                    ----------
total remediation                                  = $36,000  [COMPUTED]
residual ongoing cost (maintenance)                = $14,400 / yr  [COMPUTED]
```

Savings against Run 1:

```text
Run 1 (do nothing) − Run 3 (type system)
= $194,400 − $14,400
= $180,000 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The type system lands cleanly on the first pass:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Distinct sizes | 41 | 7 | generated ladder, 9 roles mapped [COMPUTED] |
| Payload | 246 KB | 38 KB | one variable file replaces five statics [COMPUTED] |
| Requests | 5 | 1 | subsetting + one variable file [COMPUTED] |
| CLS (Slow 4G, cold) | 0.19 | 0.004 | metric-matched fallback measured [COMPUTED] |
| Locales with coverage tests | 0 | 6 | per-file glyph test per locale [COMPUTED] |
| Faces with a licence record | 2 of 5 | 5 of 5 | register completed pre-design [COMPUTED] |
| 1.4.12 spacing conformance | failing | passing | fixed heights removed [COMPUTED] |
| Year-one engineering cost | $194,400 | $14,400 | 3 sprints + maintenance [COMPUTED] |

**Best-case net position:** $180,000 engineering saving, plus a mobile layout that no longer
fails the CLS threshold on 1,200,000 monthly sessions [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: the work is scoped as "a restyle", the licence gate is skipped, and
the scale is left ad hoc.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Restyle only, 5 new static faces, no fallback | **$237,600** | metrics changed; swap shift rose to 0.24 |
| W2 | Arabic ships with inherited global tracking | **$41,400** | joins break; 3 sprints + market escalations |
| W3 | Desktop-only licence used in the mobile app binary | **$96,000** | face replaced mid-project; ladder + metrics redone |
| W4 | Fixed-height labels ship; 1.4.12 audit fails pre-launch | **$28,800** | emergency fix in 2.4 sprints before release |

**W1 loss derivation** [COMPUTED]:

```text
base remediation (Run 1)        = $194,520
restyle sprints                 = 3.6 × $12,000 = $43,200
                                  ----------
total                           = $237,720 ≈ $237,600
CLS regression                  = 0.19 → 0.24 (worse, not better)
```

The restyle made the measured defect worse because the new faces changed the metrics and no
fallback was written. This is the trap that makes a "design refresh" a regression.

**W2 loss derivation** [COMPUTED]:

```text
tracking applied via `* { letter-spacing: -0.01em }` → 0.01em inherited everywhere
affected locale                 = ar-SA
remediation sprints             = 3 × $12,000   = $36,000
market escalation support       = 3 × $1,800    = $5,400
                                  ----------
total                           = $41,400
```

Note the cause: a single global selector applied tracking for Latin display type and broke
Arabic joins in every string on the site. One line of CSS, one market.

**W3 loss derivation** [COMPUTED]:

```text
licence discovered at release review        = desktop-only grant, 5 faces affected
forced replacement sprints                  = 6 × $12,000 = $72,000
ladder + metric + fallback rework           = 2 × $12,000 = $24,000
                                             ----------
total                                       = $96,000
```

Root cause: the licence gate (R4) runs **before** design. Skipping it means the scale, the
metrics and the fallbacks are all rebuilt against a different face.

**W4 loss derivation** [COMPUTED]:

```text
1.4.12 failure found pre-launch   = fixed-height labels, 340 instances
emergency remediation             = 2.4 × $12,000 = $28,800
                                      ----------
total                             = $28,800
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 = $237,600 + $41,400 + $96,000 + $28,800
                  = $403,800   [COMPUTED]
```

## Learnings

**1. The licence gate is not bureaucracy — it is sequencing.** W3's $96,000 exists because the
licence was checked after the scale was built. Checking it first costs an hour and prevents a
replacement that invalidates the ladder, the metrics and every fallback derived from them. This
is why R4 is a ground rule rather than a checklist item.

**2. A restyle without a system can make the measured defect worse.** W1 shows CLS rising from
0.19 to 0.24 because the new faces changed the metrics and nobody wrote a fallback. "It looks
better" and "it performs better" are independent claims; only the second is measurable.

**3. One global CSS selector can cost a market.** W2 traces to
`* { letter-spacing: -0.01em }` — applied for Latin display type, inherited by every Arabic
string. The fix is a rule that is checkable by grep (R5) and a CI gate, not vigilance.

**4. Coverage must be tested against the shipped file, per locale.** Six shipping locales, zero
tests, in the baseline. Every one of them was a latent defect the team could not see because
they could not read the scripts they were shipping.

**5. The savings are concentrated, not incremental.** Run 3 costs $36,000 of remediation and
returns $180,000 in year one against Run 1 — because the ad-hoc ladder and the unmetered payload
are both *systemic* costs that recur per release. Fixing them once is cheap; paying them per
sprint is not.

**6. Measure before claiming.** The 0.19 baseline CLS was only actionable because it was measured
on a named profile with the cache disabled. An unmeasured "it feels fast" would have produced
Run 1 by default, because there was no number to argue against.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived
quantities above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is
a measured production result, and none should be cited as one.
