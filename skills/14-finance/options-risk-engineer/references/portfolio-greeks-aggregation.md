# Portfolio Greeks Aggregation

## Core Aggregation Formulas

### Delta Aggregation
```
Delta_total = Σ(position_delta × position_size × 100)
```
Each option contract controls 100 shares. A position with delta 0.30 on 10 contracts = 300 shares of delta exposure [COMPUTED]. For short positions, negate: short 5 contracts of a 0.40 delta call = -200 delta shares.

### Gamma Aggregation
```
Gamma_total = Σ(position_gamma × position_size × 100)
```
Gamma is the rate of delta change per $1 move in underlying. Gamma_total of 50 means delta changes by 50 shares per $1 move in SPY. A $3 SPY move shifts delta by 150 shares — on a 1000-share portfolio, that is a 15% delta swing from price movement alone [COMPUTED].

### Theta Aggregation
```
Theta_total = Σ(position_theta × position_size × 100)
```
Theta is daily time decay in dollars. Theta of +$85 means the portfolio earns $85/day from time decay (theta-positive), all else equal. Theta of -$45 means you are paying $45/day — verify this is intentional [COMPUTED].

### Vega Aggregation
```
Vega_total = Σ(position_vega × position_size × 100)
```
Vega is dollar change per 1% change in implied volatility (IV). Vega of +$200 means portfolio gains $200 if IV rises 1%. Vega of -$350 means you lose $350 per 1% IV rise.

## Gamma Exposure (GEX)

GEX measures total dealer gamma across all strikes and expirations:
```
GEX = Σ(gamma × open_interest × 100 × spot_price²)
```
[COMPUTED]

- **GEX > 0**: Dealers are net long gamma → market stabilizing. Dealers buy dips and sell rips as they delta-hedge, dampening volatility.
- **GEX < 0**: Dealers are net short gamma → market amplifying. Dealers sell into dips and buy into rips, accelerating moves.
- **GEX flip**: When GEX crosses from positive to negative, markets transition from mean-reverting to trending. S&P 500 realized volatility approximately doubles in negative-GEX regimes vs positive-GEX regimes [INFERRED from GEX research].

Example: SPY at $500 with 50,000 OI at the 500 strike, gamma = 0.02:
```
raw GEX     = 0.02 × 50,000 × 100 × 500²  = $25,000,000,000  = $25 billion
per 1% move = raw GEX × 0.01              = $250,000,000     = $250 million
```
[COMPUTED]

**State which of the two you are quoting, every time — they differ by exactly 100×, and both are
published under the name "GEX".** The raw `Σ(Γ × OI × 100 × S²)` figure is a dollar-gamma per unit
move; the per-1%-move figure is that value × 0.01 and is the convention most dealer-positioning
vendors publish. A "$25B GEX" headline and a "$250M GEX" headline describe exactly the same book.

## Vanna: Delta-Vol Interaction

Vanna = change in delta per 1% change in IV. Critical for larger positions [COMPUTED]:

- **Positive vanna**: Delta increases as IV rises. A call position that is 0.30 delta at 20% IV becomes 0.35 delta at 25% IV — you have 5 more deltas per contract without price moving.
- **Negative vanna**: Delta decreases as IV rises. Your hedge weakens precisely when you need it most.
- **Dollar impact**: On a 500-contract position, vanna of 0.02 means a 5% IV spike adds (0.02 × 5 × 500 × 100) = $5,000 of additional delta exposure you did not plan for [COMPUTED].

## Charm: Delta Decay

Charm = change in delta per day passing [COMPUTED]:

- **ITM options**: Delta increases toward 1.00 (-1.00 for puts) as expiration approaches. Your 0.90-delta ITM call becomes 0.94 delta tomorrow without price moving.
- **OTM options**: Delta decreases toward 0 as expiration approaches. Your 0.20-delta OTM put becomes 0.16 delta tomorrow — your tail hedge is decaying.
- **ATM options**: Charm is near zero at-the-money. Delta stays roughly stable day-to-day for ATM.

## Greek Limits with Real Thresholds

| Greek | Limit | Rationale |
|-------|-------|-----------|
| Net Delta | ≤ 30% NAV (directional), ≤ 5% NAV (market-neutral) | A 30% delta portfolio loses 3% NAV on a 10% move — manageable. A 5% delta market-neutral should survive any directional shock [COMMON-PRACTICE] |
| Gamma per 1% move | ≤ 2% NAV | Gamma × (0.01 × spot) × 100 tells you delta change from a 1% move. If that exceeds 2% NAV, you are riding a gamma bomb [COMPUTED] |
| Positive Theta | ≥ 0.1% NAV/day | You should earn at least 0.1% of portfolio value daily from time decay for the risk you carry. Below this threshold, returns don't justify risk [COMMON-PRACTICE] |
| Vega per 1% IV | ≤ 5% NAV | A 5% IV move (common during events) shouldn't move your portfolio more than 25% NAV. At 10% NAV vega, a moderate 5% IV spike = 50% NAV loss [COMPUTED] |

## Warning Signs

1. **Net gamma flips negative**: Your portfolio accelerates into losses. A 2% move becomes a 4% move becomes an 8% move as gamma amplifies. This is how option sellers blow up.
2. **Theta goes negative**: You are paying time decay. Unless this is a defined-risk directional bet with a clear catalyst timeline, you are bleeding money [COMMON-PRACTICE].
3. **Vega exceeds 10% NAV**: One vol event and you're done. VIX can spike 20+ points in a single session — on 16 March 2020 it closed 57.83 → **82.69, +24.86 points** [VERIFIED — CBOE VIX historical daily closes, 2020-03-16]. At 10% NAV vega, that single session is a 249% NAV hit.
4. **Charm accumulation near expiration**: If 30%+ of portfolio delta comes from options ≤ 7 DTE, charm will significantly shift your exposure each day. You wake up with a different portfolio than you went to bed with [COMPUTED].
5. **Vanna concentration in same direction**: If all positions have positive vanna, your delta exposure inflates during vol spikes precisely when you need stable exposures.

## Computation Checklist

1. Pull all option positions with Greeks from broker API [BROKER-VERIFIED]
2. Compute net Delta, Gamma, Theta, Vega using formulas above [COMPUTED]
3. Compute GEX for market context (available from SpotGamma, SqueezeMetrics, or self-computed from OPRA data) [VERIFIED]
4. Check each Greek against limits table
5. Flag any warning sign triggers
6. Compute vanna and charm if position lifetime > 7 days
7. Document total portfolio Greek exposure in daily risk report

## Second-Order Greek Dependencies

### Gamma-Theta Tradeoff
For ATM options, gamma and theta are **linked** by the Black-Scholes PDE — same magnitude, opposite
sign, so a position cannot carry one without the other [COMPUTED, not sourced — it is an identity, not
an empirical claim]:
```
theta ≈ -0.5 × gamma × spot² × σ²
```
Equivalently, at the money, `Γ / |Θ| = 2 / (S²σ²)` — **independent of time to expiration** (the √T
cancels). That matters: a ratio that does not contain T cannot generate a DTE ladder, and any figure
that says `Γ/|Θ| ∝ 1/T` is a different (wrong) formula. What *does* scale with time is gamma per dollar
of premium still at stake, `Γ/V = 1/(S²σ²T)`, which is where the expiry calendar's ladder comes from.

A high-theta position necessarily carries high gamma. You cannot collect $100/day in theta without accepting the gamma risk that comes with it. This is not a strategy choice — it is a mathematical identity [COMPUTED].

Example, with every unit labelled [COMPUTED]: a near-the-money SPY 30-DTE strangle (S = $500, σ = 20%) collects **≈$19/day of theta per contract** — $191/day on a 10-contract position. Its ATM gamma is `Γ = φ(d1)/(Sσ√T) ≈ 0.0139 per share`, i.e. **1.39 Δshares per $1 per contract**. The identity then checks itself: `1.39 ÷ 19.05 = 0.073 = 365 × 2/(S²σ²)`. On 10 contracts, a $3 SPY move shifts delta by `1.39 × 3 × 10 ≈ 42 shares`. The theta you collect pays for delta-hedging friction — not risk-free income.

### Speed: Gamma of Gamma
Speed = rate of gamma change per $1 move. Large speed means gamma accelerates as price moves [COMPUTED]:
```
Speed = ∂gamma / ∂spot
```
Near expiration, speed is extreme. A position with gamma of 0.02 at 7 DTE can have gamma of 0.08 after a $5 adverse move. This is how "small" gamma positions become large gamma positions intraday. Speed warns you how fast your risk profile changes under stress.

## Real-World Greek Calculation Example

Portfolio: 10 SPY 500 straddles (long), 5 AAPL 190 calls (short), 20 IWM 200 puts (long). NAV: $250,000 [COMPUTED]:

| Position | Contracts | Net Δ (shares) | Net Γ (Δshares per +$1) | Net Θ ($/day) | Net ν ($ per +1 vol pt) |
|----------|-----------|-------|-------|-------|------|
| SPY 500 straddle (long) | 10 | +15 | +0.045 | -$22 | +$85 |
| AAPL 190 call (short) | 5 | -175 | -0.018 | +$12 | -$28 |
| IWM 200 put (long) | 20 | -380 | +0.032 | -$8 | +$45 |

**Convention for this table — stated once, and each column header carries its unit.** Every cell is a
**POSITION TOTAL** in the unit printed in the header, never a per-contract figure:

```
Net Δ (shares)          = delta_share   × 100 × contracts
Net Γ (Δshares per +$1) = gamma_share   × 100 × contracts
Net Θ ($/day)           = theta_share_per_day × 100 × contracts
Net ν ($ per +1 vol pt) = vega_share    × 100 × contracts
```

So the aggregate row is the plain **column sum** — and no other arithmetic. (The earlier edition mixed
conventions: its Δ and Θ were position totals, its ν was per-contract, and its "Gamma = +39" matched no
convention at all. That is the defect this table now closes.)

Aggregates (column sums): Δ = 15 − 175 − 380 = **−540 shares**; Γ = 0.045 − 0.018 + 0.032 = **+0.059 Δshares per $1**; Θ = −22 + 12 − 8 = **−$18.00/day**; ν = 85 − 28 + 45 = **+$102 per vol point**.

Portfolio assessment: Δ is −540 shares **across three different underlyings** — convert per underlying
(`delta_share × that underlying's price`) before any NAV comparison, because a share of SPY and a share
of IWM are not the same risk (guardrail G3). Γ is +0.059 Δshares per $1 at the book level, small only
because the legs partly offset — read the per-position gammas, not the total. Θ is −$18.00/day: the book
is paying time decay to own the long premium; verify that is intentional. ν is **+$102 per vol point**:
a 5-point IV spike costs $510, i.e. 0.2% of the $250,000 NAV, well inside the 5%-of-NAV limit — and since
vega is linear in size, the limit test is a multiplication, so state vega *per vol point* rather than as
a dollar total [COMPUTED].

*The row values above are sample inputs, not a calibrated book. Re-derive every column from your own
positions with the four formulas in `SKILL.md` Phase 0 before acting on a table like this.*

## Greek Monitoring Dashboard

Daily risk report fields [BROKER-VERIFIED pull from API]:
- Net Delta / NAV%
- Net Gamma / NAV% per 1% move
- Net Theta / NAV% per day
- Net Vega / NAV% per 1% IV
- GEX regime (positive/negative/flipping)
- Vanna concentration warning
- Charm impact for positions ≤ 7 DTE
- Any Greek exceeding limit threshold


