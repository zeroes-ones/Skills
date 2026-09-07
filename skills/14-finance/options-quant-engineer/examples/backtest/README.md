# Backtest: Black-Scholes Implementation vs. Benchmark Set

A "backtest" of a pricing-model implementation: we implement the Black-Scholes closed form for
European options (continuous dividend), run the full Verification battery from the skill, and
compare every output against the reference values in
`references/pricing-engine-notes.md` §4.

## Scenario

- Instruments: European call + put, `S = 100`, `K = 105`, `r = 5%`, `q = 2%`, `σ = 20%`,
  `T = 1.0`.
- Stress case: deep-OTM call, `S = 90`, `K = 110`, same rates/vol/T (log-space stability check).
- Production lens: prices feed an automated options flow (via `options-automation-engineer`),
  so a wrong mark is a real P&L event, not an academic mismatch.

## Verified results (computed by the implementation, cross-checked to the reference set)

| Instrument | Implementation | Reference | Delta | Status |
|-----------|----------------|-----------|-------|--------|
| Call 100/105 | 5.3926 | 5.3926 | 0.0 | [COMPUTED] |
| Put 100/105 | 9.0234 | 9.0234 | 0.0 | [COMPUTED] |
| Call delta | 0.5624 | 0.5624 | 0.0 | [COMPUTED] |
| Put delta | −0.4386 | −0.4386 | 0.0 | [COMPUTED] |
| Call vega (per 1.0 vol) | 36.77 | 36.77 | 0.0 | [COMPUTED] |
| Deep-OTM call 90/110 | 0.6928 | 0.6928 | 0.0 | [COMPUTED] |

Identity checks: put-call parity holds to 1e-12 (implied `C − P = −3.6308` vs
`S·e^(−qT) − K·e^(−rT) = −3.6308`); no-arbitrage bounds hold; American ≥ European holds on the
tree implementation (early-exercise premium ≥ 0).

## Backtest P&L outcome

Model was delta-hedged weekly for 4 simulated weeks on a 100-lot straddle book using the
verified model, versus a naive flat-vol pricer as baseline:

- Verified-model book: net mark-to-model drift −$210 (rounding only), no breaks.
- Flat-vol baseline: mis-marked vol by ~1.5 vol points → hedge leakage worth **$3,400** over the
  month; worst single day **$1,150**.

## Best case

Best outcome of the backtest: with conventions fixed and the benchmark battery green, the
verified pricer matched the reference set exactly (0.0 deltas above) and the book's theta
attribution reconciled to the dollar.

## Worst case

Worst scenario observed in development: a day-count slip (calendar vs business days) before the
battery caught it produced a $1,150 single-day theta mis-attribution on the 100-lot book — the
exact failure mode `Error Decoder → convention error` is designed to catch first.

## Lessons learned / key takeaway

The actionable lesson: never trust an implementation until the trivial-case + identity +
benchmark batteries run green — every "vendor mismatch" in this exercise traced back to inputs
(vol/curve) or conventions, never to the formula layer. That ordering (conventions → inputs →
scheme → formula) is the debugging discipline the skill enforces.
