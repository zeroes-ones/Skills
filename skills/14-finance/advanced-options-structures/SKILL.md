---
name: advanced-options-structures
description: >
  Use when the user needs advanced options strategies beyond the standard 17 covered by
  options-strategist — zebra spreads (zero extrinsic back ratios), double diagonals,
  flyagonals (butterfly-diagonal hybrids), double calendars, iron albatross, Christmas
  tree spreads, seagulls, box spreads, ratio diagonals, conversions/reversals, split-strike
  synthetics, and custom multi-leg strategy construction. Use when the user asks "how do I
  build [advanced structure]," "what strategy gives me [specific Greek profile]," or "I
  need zero-cost hedging with defined risk." Handles precise Greek targeting, margin
  optimization across Reg T and Portfolio Margin regimes, capital efficiency calculations,
  and risk assessment for each structure. Do NOT use for standard strategies covered by
  options-strategist (verticals, iron condors, basic butterflies, covered calls, CSPs,
  calendars, basic diagonals), trade execution (route to algorithmic-trader or
  options-automation-engineer), or options pricing (route to quantitative-analyst).
license: MIT
tags:
  - advanced-options
  - options-strategies
  - zebra-spread
  - double-diagonal
  - flyagonal
  - christmas-tree
  - seagull-spread
  - box-spread
  - synthetics
  - ratio-diagonal
  - custom-structures
  - margin-efficiency
  - capital-efficiency
author: Sandeep Kumar Penchala
type: finance
status: stable
version: 1.0.0
updated: 2026-07-31
token_budget: 4000
chain:
  type: symmetric
  consumes_from:
    - options-strategist
    - quantitative-analyst
    - options-risk-engineer
    - volatility-arbitrage-engineer
  feeds_into:
    - algorithmic-trader
    - portfolio-signal-manager
    - options-automation-engineer
  alternatives:
    - options-strategist
---
# Advanced Options Structures

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).
> No vendor-specific frontmatter fields.

---

<!-- QUICK: 30s -->

## Route the Request

> **This skill is for ADVANCED structures not covered by options-strategist.**

| User says | Route to | Section |
|-----------|----------|---------|
| "zebra spread," "zero extrinsic," "stock replacement with options" | **Zebra** | §2.1 |
| "double diagonal," "flyagonal," "diagonal butterfly hybrid" | **Double Diagonals & Flyagonals** | §2.2 |
| "Christmas tree," "seagull," "zero-cost hedge" | **Christmas Trees & Seagulls** | §2.3 |
| "box spread," "conversion," "synthetic loan," "gut spread" | **Box Spreads & Synthetics** | §2.4 |
| "custom structure," "ratio diagonal," "build my own strategy" | **Custom Structure Design** | §2.5 |
| "how much margin for [advanced structure]" | **Margin & Capital Efficiency** | §5 |
| "should I use [advanced structure] or [standard structure]" | **Strategy Selection** | §3 |
| "what can go wrong with [structure]" | **Error Decoder** | §7 |

> **Gate:** If the user's strategy is already covered by options-strategist (verticals, iron condors,
> basic butterflies, covered calls, CSPs, calendars, basic diagonals, straddles, strangles), route
> there. This skill is for structures that require Greek decomposition, custom construction, or
> margin regime optimization beyond the scope of standard strategies.

---

<!-- STANDARD: 3min -->

## Ground Rules

These are **negative constraints** — they tell you what NOT to do. Violating any of these will lose money.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to leg into multi-leg structures. Always enter as a single spread order. Legging creates catastrophic risk if the market moves mid-execution | Trigger: `grep "leg" trade_plan` → `leg_count > 2` AND `order_type ≠ "spread"` | STOP. "Legging risk detected. Enter all legs simultaneously as one spread order. Single-leg fill during vol spike = catastrophic unhedged position." |
| R2 | REFUSE to sell American-style box spreads in non-PM accounts. Early assignment on one leg breaks the risk-free nature | Trigger: `grep "box_spread" trade_plan` → `style = "american"` AND `account ≠ "portfolio_margin"` | STOP. "American-style box spreads are assignment-risky in non-PM accounts. Use European-style (SPX) or upgrade to Portfolio Margin." |
| R3 | REFUSE to leave naked shorts beyond 1:1 ratio. Any structure with ratio > 1:1 short:long has uncovered risk beyond the spread | Trigger: `short_count > long_count` in position_size calculation | STOP. "Uncovered shorts detected. Add far-OTM protective wing or reject the structure. Ratio > 1:1 means catastrophic loss on gap move." |
| R4 | REFUSE to trade any leg with OI < 500 or volume < 50. Multi-leg exits are impossible on illiquid strikes | Trigger: `min(OI) < 500 OR min(volume) < 50` on any option leg | STOP. "Liquidity fails: OI < 500 or volume < 50. Multi-leg exit on illiquid strikes loses 10-30% on spread alone. Pick different strikes." |
| R5 | REFUSE structures where margin > 3× max loss. If margin exceeds 3x the maximum possible loss, the structure is capital-inefficient | Trigger: `margin_required > 3 × max_loss` in capital_efficiency calculation | STOP. "Capital-inefficient: margin > 3× max loss. A simpler structure achieves the same payoff with less buying power. Route to simpler structure." |
| R6 | REFUSE to model P&L at mid-price. Mid-price modeling is optimistic — fills happen at the spread | Trigger: `grep "mid" pnl_calculation` → `model_price = "mid"` | STOP. "Mid-price modeling is optimistic. Recompute P&L using bid for sell legs + ask for buy legs. The spread gap is 5-15% of expected profit." |
| R7 | ALWAYS check dividend calendar for all short call legs. ITM short calls get assigned the day before ex-div | Trigger: `short_call = true AND DTE > ex_div_date` → no assignment warning in plan | STOP. "Ex-dividend assignment risk unaddressed. ITM short calls will be assigned pre-ex-div. Cost: lost remaining time premium + dividend amount. Close or roll before ex-date." |
| R8 | REFUSE to exceed 25% of buying power on one advanced structure. These structures have non-linear risk that can gap beyond models | Trigger: `position_BPR > 0.25 × total_BP` in portfolio_allocation | STOP. "Position exceeds 25% buying power. Advanced structures gap beyond models during vol events. Single-position failure = portfolio-level damage." |
| R9 | REFUSE structures you can't explain in one sentence. Complexity without clarity is a liability, not an edge | Trigger: `leg_count > 4 AND user_cant_explain_pnl_diagram` → no simplification offered | STOP. "Complexity without clarity. If the P&L diagram can't be explained in one sentence, route to a simpler structure. The edge is in understanding, not complexity." |
| R10 | REFUSE to roll positions more than 2 times. Rolling losers repeatedly compounds losses — if thesis breaks, close it | Trigger: `roll_count ≥ 2 AND position_P&L < 0` in roll_tracker | STOP. "Max 2 rolls exceeded on losing position. Death by a thousand rolls: P&L = -40% on positions rolled 3+ times. Close the position." |

---

<!-- STANDARD: 3min -->

## Strategy Selection Decision Tree

```
User has a market view that options-strategist can't fully address
│
├─ "I want stock-like returns with less capital"
│   ├─ 30-60 day horizon → Zebra (§2.1)
│   ├─ 90+ day horizon → LEAPS strategist
│   └─ Permanent → Just buy the stock
│
├─ "I want to harvest theta while staying delta-neutral"
│   ├─ Sideways market, low IV → Double Diagonal (§2.2)
│   ├─ Sideways market, specific target → Flyagonal (§2.2)
│   └─ Sideways market, wider range → Iron Albatross (wider IC)
│
├─ "I'm directional but want embedded risk management"
│   ├─ Bullish, want profit zone + cushion → Christmas Tree Call (§2.3)
│   ├─ Bearish, want profit zone + cushion → Christmas Tree Put (§2.3)
│   └─ Own stock, want free downside protection → Seagull (§2.3)
│
├─ "I need synthetic borrowing/lending/arbitrage"
│   ├─ Borrow at below margin rates → Short Box Spread (SPX, PM only) (§2.4)
│   ├─ Lend at above T-bill rates → Long Box Spread (§2.4)
│   ├─ Fix an underwater position → Conversion/Reversal (§2.4)
│   └─ Near-delta-1 with defined risk → Gut Spread (§2.4)
│
├─ "I have specific Greek targets — build me something"
│   ├─ Specific Δ, Γ, Θ, V targets → Custom Structure (§2.5)
│   ├─ Want leverage + theta → Ratio Diagonal (§2.5)
│   └─ Complex multi-factor view → Strategy Composition (§2.5)
│
└─ "Is this even viable in my account?"
    ├─ Cash account (< $2K) → Long calls/puts only (route to options-strategist)
    ├─ Cash account ($2K-$10K) → Debit zebra, call-based seagulls (§5)
    ├─ Reg T margin → Most debit spreads, some credit (§5)
    └─ Portfolio margin → Full advanced structures unlocked (§5)
```

---

<!-- STANDARD: 3min -->

## Core Workflow

### Phase 1: Strategy Selection (5 min)

```
1. Identify the gap: What does the user's view require that standard strategies don't provide?
   - Capital efficiency? → Zebra
   - Free hedging? → Seagull
   - Specific Greek profile? → Custom structure
   - Arb/synthetic? → Box/Conversion

2. Verify the view is solid before building complexity:
   ├─ Directional conviction: ≥ 6/10
   ├─ Time horizon specified: ___ DTE
   ├─ IV environment known: IV rank ___%, IV percentile ___%
   └─ Account type known: Cash / Reg T / PM

3. Pre-filter strategies by account viability (§5)
```

### Phase 2: Construction & Greek Validation (10 min)

```
For the selected structure:
1. Select strikes using the construction rules in the relevant reference doc
2. Calculate net Greeks at entry (Δ, Γ, Θ, V)
3. Model P&L at expiration and at 50% of DTE
4. Calculate breakeven points
5. Verify all legs meet liquidity requirements (R4)
6. Calculate margin requirement (R5)
```

### Phase 3: Risk Assessment (5 min)

```
1. Identify the primary failure mode for this structure
2. Calculate max loss (including gap risk beyond model)
3. Check R2 (American box short), R7 (dividend), R8 (BP concentration)
4. Size position: max_loss ≤ 2% of account equity
5. Set exit triggers:
   - Profit target: ___% of max profit
   - Stop loss: ___% of max loss
   - Time stop: exit at ___ DTE regardless
   - Greeks-based stop: exit if |Δ| exceeds ___ or Θ flips sign
```

### Phase 4: Execution (ongoing)

```
1. Place as single spread order (never leg in — R1)
2. Set GTC profit-taking order immediately after fill
3. Monitor daily:
   - Greeks drift (especially gamma near expiration)
   - Short leg ITM status (assignment risk)
   - Dividend dates for short calls
4. Roll or close per adjustment rules in reference docs
5. Log trade with strategy type, Greeks at entry, and exit reason
```

---

<!-- DEEP: 10+min -->

## Strategy Deep Dives

### §2.1 Zebra (Zero Extrinsic Back Ratio)

**What:** 2 DITM calls (0.75+ delta) + 1 short ATM call. Net delta ~0.90. Near-zero theta.
**Why:** Stock replacement with 2-3x capital efficiency. No time decay on the dominant long legs.
**Edge:** Leveraged directional with theta working FOR you (short ATM call decays).

> **Construction details, P&L math, adjustment rules, and comparison vs. stock/LEAPS:**
> → `references/zebra-and-zero-extrinsic.md`

**Quick construction:**
```
Long:  2 calls at 0.75+ delta (verify extrinsic < 2% of premium)
Short: 1 call at 0.50 delta (ATM)
Net:   ~0.90 delta, θ ≈ 0, ν ≈ 0
Cost:  (2 × L_premium - S_premium) × 100
```

**Best for:** High-conviction directional, 30-60 DTE, accounts where stock is too capital-intensive.

### §2.2 Double Diagonals & Flyagonals

**What:** Time-spread hybrids combining calendars/diagonals with verticals/butterflies.
**Why:** Exploit vol surface mispricing — differential decay rates + term structure roll-down.
**Edge:** 20-30% more theta than equivalent butterflies; wider profit zones than standard diagonals.

> **Construction details, P&L zones, Greek evolution over time, and adjustment cadence:**
> → `references/double-diagonals-and-flyagonals.md`

**Quick differentiation:**
| Feature | Double Diagonal | Flyagonal |
|---------|----------------|-----------|
| Legs | 4 (2 calls + 2 puts) | 4 (all calls or all puts) |
| Primary edge | Dual theta + vega-positive | Pin-seeking + diagonal theta |
| Best market | Sideways, low-moderate IV | Stock trending toward a target |
| Max profit at | Short strikes at near exp. | Body strike at near exp. |

### §2.3 Christmas Trees & Seagulls

**What:** Directional structures with embedded risk management.
**Why:** Christmas trees embed a butterfly within a vertical for cushion. Seagulls provide zero-cost downside protection.
**Edge:** Asymmetric payoff without the full cost of separate hedges.

> **Construction, P&L zones, strike selection formula, ratio variants:**
> → `references/christmas-trees-and-seagulls.md`

**Quick construction:**
| Structure | Components | Best For |
|-----------|-----------|----------|
| Christmas Tree (call) | 1L-2S-1S-1L calls at ascending K | Bullish with a target ceiling |
| Seagull (bullish) | +Stock/Call -OTM Call +OTM Put | Zero-cost downside floor |
| Seagull (ratio) | +Call -2×OTM Call +Put | Bullish, limited capital, accept upside cap |

### §2.4 Box Spreads, Conversions & Synthetics

**What:** Put-call parity structures — risk-free (or near-risk-free) positions.
**Why:** Synthetic borrowing at below-margin rates, arbitrage detection, position repair.
**Edge:** Risk-free by construction (European-style). The market occasionally misprices these.

> **Put-call parity math, American vs. European risks, synthetic equivalents table:**
> → `references/box-spreads-and-synthetics.md`

**Critical warning:** [VERIFIED] The 2019 Robinhood box spread incident — a trader sold an American-style box spread and saw -$60,000 when one leg was early-exercised. Never sell short boxes on American-style options in non-PM accounts. Use SPX (European, cash-settled) for box spreads.

### §2.5 Ratio Diagonals & Custom Structures

**What:** Strategy composition framework — build structures with specific Greek targets.
**Why:** When no off-the-shelf strategy matches your precise Greek requirements.
**Edge:** Exact delta/theta/vega targeting. Capitalize on specific vol surface dislocations.

> **Composition rules, Greek targeting algorithm, primitive catalog, constraint enforcement:**
> → `references/ratio-diagonals-and-custom-structures.md`

**When to build custom vs. use standard:**
```
Custom justified when:               Standard when:
- Specific Δ/Θ/V targets needed     - Approximate profile is fine
- Different IV views per strike      - Uniform IV environment view
- PM account (margin nets correctly)  - Reg T (margin punishes complexity)
- You can model Greeks over time      - Set-and-forget monitoring
```

---

## Research Prerequisites

Before recommending any advanced structure, gather:

| # | Data Point | Source | Mandatory |
|---|-----------|--------|-----------|
| RP1 | Current IV rank and IV percentile | quantitative-analyst | ✅ |
| RP2 | IV term structure (contango/backwardation) | quantitative-analyst | ✅ |
| RP3 | IV skew (put skew vs. call skew) | quantitative-analyst | ✅ (for ratio structures) |
| RP4 | Option chain liquidity (volume, OI, spread) per strike | market-data-engineer | ✅ |
| RP5 | Earnings date (within DTE range?) | fundamental-analyst | ✅ |
| RP6 | Ex-dividend dates for all short call legs | fundamental-analyst | ✅ |
| RP7 | Account type and available buying power | Account verification | ✅ |
| RP8 | Correlation to existing positions | options-risk-engineer | ⚠️ (multi-position portfolios) |

> **Iterative research loop:** If any RP fails (e.g., OI < 500 on a key leg), iterate — find a different strike or a different structure. Do NOT proceed with insufficient data.

---

<!-- DEEP: 10+min -->

## Margin & Capital Efficiency

> **Full margin treatment for each structure, Reg T vs. PM comparison, position sizing rules:**
> → `references/margin-and-capital-efficiency.md`

### Quick Reference: Which Structures Work in Your Account?

| Account Type | Zebra | Double Diagonal | Christmas Tree | Seagull | Box Spread | Flyagonal |
|-------------|-------|----------------|---------------|---------|-----------|-----------|
| Cash (< $2K) | ❌ | ❌ | ❌ | ⚠️ call-based | ❌ | ❌ |
| Cash ($2K-$10K) | ✅ debit | ⚠️ | ❌ | ✅ call-based | ❌ | ⚠️ |
| Reg T | ✅ | ✅ | ⚠️ | ✅ | ⚠️ long only | ✅ |
| Portfolio Margin | ✅ | ✅ | ✅ | ✅ | ✅ SPX only | ✅ |

**Universal rule:** Position max loss ≤ 2% of account equity. Never > 25% of buying power on one structure.

---

## Error Decoder

| # | Symptom | Root Cause | Exact Fix | Prevention Lesson |
|---|---------|-----------|-----------|-------------------|
| E1 | "My box spread shows -$60,000 loss" | American-style short box — early assignment on one leg broke the arbitrage | Close all remaining legs immediately. Accept the loss. Next time: use SPX (European) boxes only | **Never sell short boxes on American-style options.** The risk-free math only works if all legs survive to expiration |
| E2 | "Zebra is losing money even though stock is flat" | Long legs aren't deep enough ITM — extrinsic decay is eating the position | Check extrinsic on long legs. If > 2% of premium, roll deeper ITM or close | **Verify extrinsic < 2% before entry (R1 for Zebra).** 0.75+ delta isn't enough — check the actual extrinsic |
| E3 | "Christmas tree margin requirement is 3x what I calculated" | Reg T margins each leg independently — doesn't recognize the 6-leg structure | Reduce position size, switch to Reg T-friendlier structure, or upgrade to PM | **Run margin estimate for your account type before entering.** Reg T is punitive on 4+ leg structures |
| E4 | "One leg of my 4-leg spread filled but the others didn't" | You legged in instead of using a spread order. The market moved mid-execution | Cancel unfilled legs immediately. Close the filled leg at market. Accept the loss | **R1: Never leg into multi-leg structures.** Always use exchange-native spread orders |
| E5 | "Short call got assigned the day before ex-dividend" | Did not check the dividend calendar. ITM short calls ALWAYS get assigned before ex-div | Accept the assignment. Sell the delivered shares or exercise a long call to cover | **R7: Check ex-div dates for ALL short call legs.** If ITM short call AND ex-div before expiration → close or roll before ex-div |
| E6 | "Flyagonal max profit is 40% less than modeled" | Model used mid-prices. Filled at bid (sell legs) and ask (buy legs) — spread was 5%+ | Accept the reduced profit. Next time: model with bid/ask, not mid | **R6: Model P&L using bid/ask prices.** If the trade only works at mid, it doesn't work |
| E7 | "Ratio diagonal blew through the uncovered short strikes" | Underestimated realized volatility. The "naked" extra shorts had no hedge | Close the entire position. The loss on the naked shorts dominates any remaining theta | **R3: Cap all naked shorts with far OTM wings.** The small debit is insurance against tail events |

---

## Anti-Hallucination

Always tag information sources so the user knows what's verified vs. calculated:

| Tag | Meaning | Example Usage |
|-----|---------|--------------|
| `[VERIFIED]` | Directly verifiable — published by CBOE, OCC, FINRA, academic finance, or textbook (Hull, Natenberg, Taleb) | `[VERIFIED] Box spread payoff = K2 - K1 at expiration` |
| `[COMPUTED]` | Derived from first principles using Black-Scholes, put-call parity, or arithmetic | `[COMPUTED] Zebra net rho ≈ 0.22 per contract at these inputs` |
| `[ESTIMATED]` | Practitioner heuristic, not mathematically derived; directionally correct but imprecise | `[ESTIMATED] Double diagonals are 20-30% more theta-positive` |
| `[COMMON-PRACTICE]` | Widely used in the industry, not formally codified | `[COMMON-PRACTICE] 90% of trades should use standard strategies` |
| `[BACKTEST-EVIDENCE]` | Supported by the Trading project's empirical backtest data | `[BACKTEST-EVIDENCE] Simpler strategies with proper exits outperform complex multi-leg structures for directional trades` |
| `[AS OF YYYY-MM]` | Time-sensitive information. Verify if significant time has passed | `[AS OF 2026-07]` |

**If you don't know:** Say "I cannot compute this from available data" rather than inventing a number.
**If the user's scenario doesn't fit:** Route back to options-strategist rather than forcing an advanced structure where a standard one works better.

---

## Cross-Skill Coordination

### Upstream (Skills That Feed Into This One)

| Skill | What It Provides | Decision Gate |
|-------|-----------------|---------------|
| `options-strategist` | Strategy baseline, standard structure selection | IF strategy in options-strategist scope → route there. IF strategy needs Greek customization or isn't covered → use this skill |
| `quantitative-analyst` | Greeks, IV surface, vol term structure, put-call parity | IF IV rank unknown → fetch before recommending any structure |
| `options-risk-engineer` | Portfolio Greeks, margin type identification, correlation matrix | IF account type unknown → determine before sizing any position |

### Downstream (Skills That Consume This Skill's Output)

| Skill | What It Needs | Handoff Format |
|-------|--------------|----------------|
| `algorithmic-trader` | Strategy specification with exact strikes, ratios, DTE, entry conditions | Structured strategy dict: `{type, legs[{option, strike, dte, side, quantity}], entry_triggers, exit_rules}` |
| `portfolio-signal-manager` | Signal: "advanced structure recommended for [ticker]" with sizing and confidence | Signal format: `{ticker, structure_type, net_greeks, max_loss, confidence_score, reasoning}` |
| `options-automation-engineer` | Strategy definition for automated execution and monitoring | Machine-readable strategy spec with all legs, roll criteria, and exit conditions |

### Alternatives

| Skill | When to Use Instead |
|-------|-------------------|
| `options-strategist` | Standard strategies (verticals, ICs, butterflies, covered calls, etc.) — less complexity, better fills, lower margin |
| `leaps-strategist` | Long-dated options, stock replacement for 6+ months, PMCC optimization |

---

## What Good Looks Like

A successful advanced options structure recommendation:

1. **Strategy is correctly selected** — the user's view genuinely requires an advanced structure (not forcing complexity where a vertical spread would work better)
2. **All 10 Ground Rules are enforced** — no American short boxes, no legging, liquidity verified, margin checked, dividends checked
3. **Greeks are computed and presented** — the user knows Δ, Γ, Θ, V at entry and how they evolve
4. **P&L diagram is explained** — max profit, max loss, breakeven points in dollar terms, not just percentages
5. **Margins are calculated for the account type** — the user knows exactly how much buying power this consumes
6. **Exit rules are specified** — profit target, stop loss, time stop, and Greeks-based triggers
7. **Worst-case scenario is explicit** — "if X happens, you lose $Y, which is Z% of your account"
8. **The user can explain the trade** — if they can't, the structure is too complex (R9)
9. **Alternatives are presented** — "here's the simpler version if you want less complexity"
10. **Documentation is tagged** — all claims are `[VERIFIED]`, `[COMPUTED]`, `[ESTIMATED]`, or `[COMMON-PRACTICE]`

---

## Operating at Different Levels

| Level | Capability | Scope | What Changes |
|-------|-----------|-------|-------------|
| **L1: Apprentice** | Can identify when a standard strategy won't work and an advanced structure is needed | Single structure at a time | Follows construction recipes exactly. Uses standard strikes, ratios from reference docs |
| **L2: Practitioner** | Builds any advanced structure from the catalog with correct Greeks and margin calculation | Multi-leg portfolio | Adjusts strikes and ratios based on IV environment. Models Greeks over time and price |
| **L3: Specialist** | Designs custom structures to target specific Greek profiles. Understands vol surface arbitrage | Cross-structure optimization | Composes primitives into novel structures. Trades vol surface dislocations across term structure and skew |
| **L4: Expert** | Market-makes complex structures. Understands exchange margin algorithms and cross-margining | Institutional portfolio | Runs real-time Greek risk. Provides liquidity in multi-leg markets. Understands PIN risk and early exercise game theory |
| **L5: Transformative** | Creates new options structures. Publishes strategy research. Influences exchange rules | Industry-wide | Invents structures that become standard. Advises exchanges on complex order types. Teaches at OIC/CBOE level |

---

## Anti-Patterns

| ❌ Common Mistake | ✅ Correct Approach |
|-------------------|---------------------|
| "I'll leg into the spread to get better fills" | **R1: Single spread order only.** The "better fill" on one leg will be offset 10x by the loss when the market moves before the other legs fill |
| "Box spreads are free money — I'll just sell these every month" | **Box spreads are LOANS, not profits.** A short box must be repaid. American-style short boxes carry catastrophic early-assignment risk |
| "I'll add more legs to make the position profitable again" | **Adding legs to a losing position compounds complexity, not edge.** Close the position. Enter a new, clean structure if the view remains valid |
| "My model shows this is profitable at mid-prices" | **R6: Model with bid/ask.** Mid-price models are fantasy. If the trade doesn't work at real fill prices, it doesn't work |
| "Portfolio Margin lets me use 90% of my buying power" | **Never exceed 50% PM buying power.** PM recalculates continuously. A VIX spike widens stress scenarios → margin call → forced liquidation |
| "This 6-leg structure is sophisticated — it must be better" | **Complexity is not edge.** More legs = more slippage, more commissions, more things to break. If a 2-leg spread captures 80% of the view, use it |
| "I don't need to check dividends — the yield is tiny" | **R7: ITM short calls get assigned 100% of the time before ex-div, regardless of dividend size.** The dividend doesn't need to be large — any dividend triggers assignment |

---

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| American-style short box spread in a Reg T account — early assignment on one leg while the other 3 legs still have days to expiration. The "risk-free" arbitrage now has a $60K realized loss and 3 open legs with unknown risk | $50K-$150K per incident — American-style boxes carry binary early-assignment risk that European-style (SPX) boxes don't have | Never sell short boxes on American-style options outside Portfolio Margin accounts. Use SPX (European, cash-settled, Section 1256) for box spreads. The risk-free math only works if all legs survive to expiration |
| Zebra spread modeled with mid prices shows +2.5% profit. Filled at bid/ask — the actual cost has 4-6% spread because one leg is deep ITM (wide market) and the short leg is OTM. Real P&L at entry: already -2% before any move | $1K-$3K per zebra trade — mid-price modeling on multi-leg structures is systematically optimistic | Model P&L using bid (sell legs) + ask (buy legs). If the trade only works at mid-price, it doesn't work (R6). The spread on 3+ leg structures is the #1 hidden cost that mid-price models conceal |
| "I'll leg into the Christmas tree spread — better fills on each leg individually." First 2 legs fill, market moves 1.5%, remaining 4 legs are now $3.00 worse than modeled. Now holding a naked position while waiting | $5K-$20K per legged-in trade — legging risk is unbounded adverse selection | R1: Never leg into multi-leg structures. Always use exchange-native spread orders. The "better fill" on one leg is offset 10× by the loss when the market moves mid-execution |
| Flyagonal constructed with strikes that each have OI 50-200. Market drops, need to exit — the 4-leg spread has ZERO bids on 2 of the legs. Trapped in position for 5 days while theta decays | $2K-$5K in forced hold costs — illiquid multi-leg positions become unexitable prison trades | Verify OI > 500 and volume > 50 on every leg before entry. Multi-leg exits require all legs to have a market. One illiquid strike makes the entire structure unexitable (R4) |
| Margin calculation used SPAN/PM assumptions but the account is Reg T — Christmas tree (6 legs) margin requirement is 3× the modeled max loss. Position ties up 40% of account instead of expected 12% | $10K-$30K in opportunity cost + forced position reduction — wrong margin assumptions convert a "good" trade into a capital-destroying one | Run margin estimate for YOUR account type before entering. Reg T is punitive on 4+ leg structures — each leg is margined independently. Portfolio Margin reduces multi-leg margin by 50-80% (R5) |
| Ratio diagonal: entered with ratio 1:2 (1 long back month, 2 short front month). Stock rips through the naked short strikes on high realized vol. Loss on 2 naked shorts = $4,000. Theta collected on 1 long leg = $400 | $3K-$6K per ratio diagonal blow-up — the net short exposure dominates P&L when vol expands | R3: Cap all ratio structures with far-OTM protective wings. The small debit for the wing ($0.15-0.30) is tail insurance. An uncovered ratio > 1:1 short:long has catastrophic gap risk |
| Structure has 5 legs and "targets specific Greek profile." Trader can't explain the P&L diagram in one sentence when asked. Position held through an earnings event because "the Greeks showed it was neutral." Lost 15% because the correlation assumption was wrong | $3K-$10K per trade — complexity without clarity is a liability masquerading as sophistication | R9: If you can't explain the P&L diagram in one sentence, don't trade it. The edge is in understanding the trade, not in the number of legs. Simpler structures with proper exits outperform complex structures for 90% of directional trades |

## Production Checklist

Before executing ANY advanced options structure, verify:

- [ ] **S1: Standard strategy check** — Verified this structure is NOT covered by options-strategist
- [ ] **S2: Liquidity** — All legs: OI > 500, volume > 50, bid/ask spread < 5% (R4)
- [ ] **S3: Single order** — Will execute as exchange-native spread order, not legged (R1)
- [ ] **S4: American box safety** — If short box: must be European-style (SPX/NDX) in PM account (R2)
- [ ] **S5: Naked short cap** — Any ratio > 1:1 short:long must have far OTM wing protection (R3)
- [ ] **S6: Margin verified** — Calculated for user's specific account type. Requirement < 3× max loss (R5)
- [ ] **S7: Bid/ask model** — P&L modeled using bid (sell legs) + ask (buy legs). Trade still profitable (R6)
- [ ] **S8: Dividend check** — No ex-dividend dates for ITM short calls within DTE (R7)
- [ ] **S9: Position sizing** — Max loss ≤ 2% account equity. Position BP ≤ 25% total BP (R8)
- [ ] **S10: IV environment** — IV rank known. Structure matches IV environment (e.g., not selling vega at IV rank < 20%)
- [ ] **S11: Earnings blackout** — No earnings within DTE range unless specifically trading the event
- [ ] **S12: Exit triggers set** — Profit target, stop loss, time stop, Greeks-based triggers all specified
- [ ] **S13: Worst case quantified** — User knows exact dollar max loss and account % at risk
- [ ] **S14: Explainability** — User can explain the P&L diagram in one sentence (R9)
- [ ] **S15: Simpler alternative considered** — Presented the standard-strategy alternative and why it doesn't fit

---

## References

| Reference | Covers | Use When |
|-----------|--------|----------|
| `references/zebra-and-zero-extrinsic.md` | Zebra mechanics, breakeven math, stock vs. options comparison | Building or evaluating a zebra spread |
| `references/double-diagonals-and-flyagonals.md` | Time-spread hybrids, vol surface exploitation, Greek evolution | Constructing double diagonals or flyagonals |
| `references/christmas-trees-and-seagulls.md` | Structured directional hedges, zero-cost protection | Building directional strategies with embedded risk management |
| `references/box-spreads-and-synthetics.md` | Arbitrage, synthetic loans, conversions, reversals, gut spreads | Arbitrage, synthetic borrowing, position repair |
| `references/ratio-diagonals-and-custom-structures.md` | Custom strategy construction, Greek targeting, primitive composition | Building bespoke structures with specific Greek targets |
| `references/margin-and-capital-efficiency.md` | Reg T vs. PM treatment, capital efficiency, account-type viability | Determining if a structure works in the user's account |
| `references/execution-quality-and-slippage.md` | Multi-leg spread costs by leg count, bid/ask modeling, liquidity requirements, broker comparison | Before executing any 4+ leg structure |
| `references/strategy-failure-case-studies.md` | Real blow-up cases: box spread margin call, zebra extrinsic trap, diagonal liquidity, Christmas tree margin shock, ratio diagonal vol explosion | When evaluating a new structure — learn from failures, not just theory |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-31 | Initial release. 6 advanced structures + custom composition framework + margin guide. 10 ground rules, 7 error patterns, 15-point production checklist |
