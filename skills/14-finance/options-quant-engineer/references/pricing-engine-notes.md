# Pricing-Engine Notes — Conventions, Identities, Benchmark Values

Companion to the options-quant-engineer skill. Everything here is the *verification* layer:
conventions to state, identities to assert, and reference values to match. Treat these as test
specifications, not theory summaries.

## 1. Conventions to state before any pricing

- **Exercise:** European (exercise at expiry only) vs American (any time) vs Bermudan (set dates).
- **Rates:** continuous risk-free rate `r`; if a curve is available, use a discount factor handle,
  not a scalar. State day-count (ACT/365 default) and compounding.
- **Dividends:** continuous yield `q` vs discrete dividends `{t_i, d_i}`. Continuous q is a model
  simplification; discrete dividends change American exercise decisions.
- **Time:** `T` in years from `t0` to expiry using the day-count basis chosen. State whether
  calendar or business days.
- **Underlying:** spot `S` at reference time `t0`; for FX, quote convention (domestic/foreign
  rates map to r/q).

## 2. Identity battery (must pass for every pricing run)

Let `C`, `P` be European call/put with strike `K`, time `T`, spot `S`, rate `r`, dividend `q`.

- **Put-call parity:** `C − P = S·e^(−qT) − K·e^(−rT)`.
- **No-arbitrage call bounds:** `C ≥ max(S·e^(−qT) − K·e^(−rT), 0)` and `C ≤ S·e^(−qT)`.
- **No-arbitrage put bounds:** `P ≥ max(K·e^(−rT) − S·e^(−qT), 0)` and `P ≤ K·e^(−rT)`.
- **American ≥ European:** for identical parameters, American price ≥ European twin
  (early-exercise premium ≥ 0).
- **Sensitivity identities (European, continuous q):** delta put − delta call = −e^(−qT);
  vega equal for call and put; theta relationship via the BS PDE
  `theta + r·S·delta + ½·σ²·S²·gamma = r·V` (verify to tolerance).

## 3. Trivial-case battery

| Case | Expectation |
|------|-------------|
| `T → 0` (deep ITM call) | `C ≈ S·e^(−qT) − K·e^(−rT)` → at `T=0`: `max(S−K, 0)` |
| `σ → 0` | forward-looking: if `S·e^(−qT) > K·e^(−rT)` call → intrinsic; otherwise 0 |
| `S = K`, `T = 0` | 0 |
| `S ≫ K` | call ≈ `S·e^(−qT) − K·e^(−rT)`; delta → e^(−qT) |
| `S ≪ K` | call → 0 (watch underflow; use log-space intermediates) |
| `q = r = 0`, `K = S` ATM | approximate BSM: call ≈ `0.4·S·σ·√T` (sanity magnitude only) |

## 4. Benchmark values (Black-Scholes European, continuous q)

Reference set used to validate implementations. Parameters:
`S = 100`, `K = 105`, `r = 5%`, `q = 2%`, `σ = 20%`, `T = 1.0`.

| Quantity | Value |
|----------|-------|
| d1 | `(ln(S/K) + (r − q + σ²/2)·T) / (σ·√T)` ≈ 0.15702 |
| d2 | d1 − σ·√T ≈ −0.04298 |
| Call price | ≈ 5.3926 |
| Put price | ≈ 9.0234 (via put-call parity: `C − S·e^(−qT) + K·e^(−rT)`) |
| Call delta | ≈ 0.5624 |
| Put delta | ≈ −0.4386 (= call delta − e^(−qT)) |
| Call/Put vega | ≈ 36.77 (per 1.0 vol unit; scale by 0.01 for per-percent) |

Second set — deep OTM call, `S = 90`, `K = 110`, same rates/vol/T: price ≈ 0.6928 (use to test
log-space stability).

## 5. Sensitivity cross-check spec

- **Bumped Greeks:** central difference `(f(x+h) − f(x−h)) / (2h)` on price, per parameter.
- **Bump policy:** `h_spot = S·1e-4`, `h_vol = 1e-4`, `h_T = 1e-6` years, `h_rate = 1e-5`.
  State the policy in every report; never use one arbitrary epsilon for everything.
- **Tolerance:** analytic vs bumped agreement within `1e-4` on delta/gamma/vega for smooth
  payoffs; within `1e-2` on gamma/theta near ATM where curvature is highest. Barrier and
  path-dependent payoffs: bumped is the reference, analytic is the cross-check.

## 6. Calibration report template

For any fitted surface (SABR/local vol), report all four, not just RMSE:

1. **Fit quality:** RMSE in vol points and price space, per strike bucket.
2. **Parameter stability:** sensitivity of fitted parameters to (a) removing the two most
   extreme strikes, (b) ±1 market day of data.
3. **Hedge test:** one-week out-of-sample hedging P&L (delta-hedged with the calibrated surface)
   vs a flat-vol baseline.
4. **Failure envelope:** input ranges where calibration diverged or returned boundary values.

## 7. Failure-mode decoder (quick map)

| Symptom | Most likely cause |
|---------|-------------------|
| Wrong at every point | conventions (rate/dividend/day-count/exercise) |
| Wrong only American | early-exercise handling / discrete dividends |
| Wrong only deep OTM | exp underflow → log-space intermediates |
| Greeks NaN near ATM | bump size / tiny vega division → adaptive central diff |
| Fits but hedges badly | overfit (too many params, too few points) |
| Constant vendor gap across strikes | input mismatch (vol/curve), not implementation |

## 8. MC variance-reduction checklist

- Antithetic variates and/or control variate on the underlying (delta) if computing Greeks.
- Report standard error, not a bare point estimate.
- Match seed policy: reproducibility for tests, different seeds for production bounds.
- Convergence check: price at N and 4N agree within 2× reported SE.
