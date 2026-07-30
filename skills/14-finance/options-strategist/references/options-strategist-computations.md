# Options Strategist — Full Computation Reference

---

## Core Workflow
**(STANDARD)**

<!-- STANDARD: 5min overview — skim the phases, read your target phase in detail -->

<!-- DEEP: 10+min -->
### Phase 1: Assess Market Conditions (~5 min)
<!-- DEEP: Full assessment protocol — read before any strategy selection -->
**Goal:** Gather and validate all inputs needed for strategy selection.

**Steps:**
1. **IV Rank/Percentile Check:** Determine IV rank (current IV relative to 1-year range). Classify: Low (0-25), Normal (26-50), Elevated (51-80), Extreme (81-100). This is the PRIMARY strategy driver.
2. **IV Term Structure:** Compare front-month IV to back-month IV. Contango (back > front), backwardation (front > back), or flat. This determines calendar/diagonal viability.
3. **IV Skew Assessment:** Check 25-delta call IV vs 25-delta put IV. Normal skew (puts richer), reverse skew (calls richer). This determines which side offers better premium.
4. **Directional Conviction Level:** Assess from UOA signals, technical analysis, and fundamentals. Assign: STRONG, MODERATE, WEAK, or NEUTRAL.
5. **UOA Signal Validation:** If UOA is a primary input, validate: OI ratio (>2 = opening, <0.5 = closing), multi-leg detection (within 60s window), earnings proximity, sector alignment.
6. **Event Calendar Check:** Catalog earnings, FDA dates, Fed meetings, economic releases within the intended DTE window. Any binary event → strategy must be event-aware.
7. **Liquidity Check:** Verify underlying ADV > 500K shares, option OI > 1,000 contracts at target strikes, bid-ask spread < 5% of option price.
8. **Capital Assessment:** Determine available capital, buying power, margin requirements. Classify account tier: Small (<$10K), Medium ($10K-$100K), Large ($100K+).

**Output:** Market Conditions Card with IV rank, term structure, skew assessment, conviction level, UOA summary, event risks, and capital tier.

  Complete when: All 8 data points are populated AND any missing data is flagged with "UNKNOWN — strategy selection degraded without this input." No strategy is selected until Phase 1 is complete.
  Complete when: IV rank, term structure, and skew are assessed. Event calendar is checked against intended DTE. UOA signals (if present) are validated for OI ratio and multi-leg detection.

<!-- DEEP: 10+min -->
### Phase 2: Strategy Selection (~10 min)
<!-- DEEP: Full strategy selection protocol -->
**Goal:** Select the optimal strategy from 15+ candidates based on the Phase 1 conditions.

**Steps:**
1. **Consult Strategy Selection Matrix:** Cross-reference IV Rank (low/normal/high) with Directional Conviction (bullish/bearish/neutral) in the master matrix (see references/strategy-selection-matrix.md). This yields the primary strategy CLASS (debit spread, credit spread, iron condor, calendar, etc.).
2. **Apply UOA Overrides:** If UOA signals are present, check for overrides:
   - UOA bullish + IV high → switch to credit strategy (bull put spread) even if matrix says debit
   - UOA bearish + IV low → switch to debit strategy (bear put spread)
   - Multi-leg UOA detected → consider mirroring the exact structure
   - Dark pool block → extend DTE to 60-90 days
3. **Capital Constraint Filter:** Eliminate strategies that exceed account limits:
   - < $10K: undefined-risk strategies eliminated (naked options, short strangles)
   - $10K-$50K: ratio spreads, backspreads eliminated
   - All tiers: max loss per trade capped at 2-5% of account per R3
4. **Event Risk Filter:** If earnings within DTE, eliminate strategies that are destroyed by gap moves (debit spreads become 100% loss on gaps; credit spreads become max loss). Consider earnings-specific strategies (iron condor capturing IV crush, butterfly).
5. **Strategy Comparison (Top 2):** For the top 2 candidate strategies, compute:
   - Max profit / Max loss ratio
   - Probability of profit (approximate)
   - IV impact direction (long vega vs short vega — does it align with IV rank?)
   - Breakeven width (as % of stock price)
   - Commission impact (number of legs × contracts)
6. **Final Selection:** Select the strategy with the highest expected value given all constraints. Document WHY this strategy over the runner-up.

**Output:** Strategy Selection Card with selected strategy, runner-up, selection rationale, IV/strategy alignment check.

  Complete when: Strategy is selected with documented rationale, runner-up is identified, and rejection reasons for all other strategy classes are noted. Strategy passes R4 (IV/strategy alignment check).
  Complete when: Strategy comparison between top 2 candidates is documented with max profit/loss ratio, probability of profit, and IV impact direction for each. Final selection is justified with quantified expected value.

<!-- DEEP: 10+min -->
### Phase 3: Leg Construction (~15 min)
<!-- DEEP: Full leg construction protocol -->
**Goal:** Construct the specific option legs — strikes, expirations, quantities — for the selected strategy.

**Steps:**
1. **Strike Selection Method Choice:** Choose from the 4 methods (UOA-informed, delta-based, standard deviation, technical levels) per the Strike Selection Decision Tree. UOA-informed is ALWAYS preferred when available.
2. **Short Strike Placement:** For credit spreads: 25-30 delta (standard) or 30-35 delta (aggressive, high IV). For iron condors: 16-20 delta each side (standard). For covered calls: 25-30 delta (income) or 15-20 delta (keep stock).
3. **Long/Wing Strike Placement:** For defined-risk spreads: 10-15 delta protective wing, 10-15 points wider than short for iron condors. Wing width determines max loss — ensure it fits capital constraints.
4. **DTE Selection:**
   - Credit strategies: 30-45 DTE (theta sweet spot)
   - Debit strategies: 30-60 DTE (time for thesis to play out)
   - Iron condors: 30-45 DTE (theta + manageable gamma)
   - Calendars: front 30, back 60 (or front 14, back 45 for events)
   - Earnings plays: front-month covering earnings date
5. **Contract Quantity:** Calculate: `max_contracts = floor(0.05 × account_value / max_loss_per_contract)`. For undefined-risk strategies, size based on notional exposure, not margin requirement. Never exceed 5% max loss per R3.
6. **Risk Profile Calculation:** For EVERY leg construction, compute and output:
   - Max loss (total dollar amount)
   - Max profit (total dollar amount)
   - Breakeven(s) at expiration
   - Probability of profit (approximate, based on short strike delta for credit spreads)
   - IV impact direction (net vega — long or short? positive or negative on IV change?)
   - Commission estimate (legs × contracts × rate)
7. **Pin Risk Assessment:** For credit spreads and iron condors: verify that the plan includes closing before expiration. Document pin risk exposure if held through expiration.

**Output:** Complete trade plan with specific strikes, expirations, contract quantities, risk profile, and commission estimate.

  Complete when: Every leg has a specific strike and expiration. Risk profile is fully quantified. Contract quantity respects capital constraints and R3. Pin risk is assessed and mitigated.
  Complete when: Risk profile card is complete with all 7 line items (max loss, max profit, breakeven, probability of profit, IV impact, commission estimate, pin risk assessment). No "[TBD]" or "~" placeholders remain — every number is explicit.

<!-- DEEP: 10+min -->
### Phase 4: Risk Validation (~5 min)
<!-- DEEP: Full risk validation — the \"trust but verify\" phase -->
**Goal:** Validate that the constructed strategy does not violate any risk rules and is appropriate for the account and market conditions.

**Steps:**
1. **Ground Rules Compliance Check:** Run through R1-R8. Every rule must pass or have a documented override with justification.
2. **Correlation Check:** Does this position correlate with existing positions? If adding to an existing sector > 30% of portfolio, reduce size or skip.
3. **Event Re-check:** Re-verify no new events (earnings announcements, FDA dates, Fed speeches) appeared since Phase 1.
4. **Liquidity Re-check:** Confirm bid-ask spreads haven't widened beyond acceptable thresholds.
5. **Max Drawdown Scenario:** Model the worst realistic scenario and verify account can survive it: "If the underlying gaps 10% against us overnight, what's the max loss?" If the answer exceeds your 5% per-trade limit, the strategy is too large.
6. **Strategy Soundness Checklist:**
   - [ ] Strategy class matches IV environment (debit for low IV, credit for high IV)
   - [ ] Strike width is appropriate for account size
   - [ ] DTE selection matches thesis timeframe + theta optimization
   - [ ] Profit target is achievable (not > max profit, not so small fees eat it)
   - [ ] Stop-loss is at a level that avoids death-by-commission (if stop is $0.20 wide and commission is $0.65/contract, a round-trip costs $1.30 = 6.5 contracts just to break even on the stop)
   - [ ] Exit plan is defined with 3 triggers: profit, stop, time

**Output:** Risk Validation Report — pass/fail on all checks with remediation if needed.

  Complete when: All 6 validation steps pass. Any failure is documented with remediation. Strategy is confirmed ready for execution.

<!-- DEEP: 10+min -->
### Phase 5: Adjustment & Exit Rules (~5 min)
<!-- DEEP: Full exit management design -->
**Goal:** Design the complete exit management plan before the trade is entered.

**Steps:**
1. **Profit Target:** Set at 50% of max credit (credit spreads, iron condors) or 50% of max profit (debit spreads, calendars). Exception: covered calls and CSPs at 80-90% of max credit. Record the exact dollar amount and GTC order logic.
2. **Stop-Loss:** Set at 2× credit received (credit strategies) or 100% of debit paid (debit strategies). Record exact dollar amount. Set hard stop — not mental.
3. **Time Stop:** Set at 21 DTE for all strategies. If trade is not at profit target by 21 DTE, evaluate for early close. Rationale: gamma risk increases exponentially in final 3 weeks.
4. **Adjustment Triggers:** Define specific conditions for rolling vs. closing:
   - Stock within X% of short strike → evaluate roll
   - Thesis invalidated → close immediately
   - Max roll count: 2 rolls maximum, then accept assignment or take loss
5. **Post-Exit Protocol:** After any exit (profit, stop, time), record in trade journal: entry reason, strategy, exit reason, P&L, MAE, MFE, and lesson. This data is more valuable than the P&L — it drives strategy refinement.

**Output:** Exit Management Plan with exact trigger prices, GTC order logic where applicable, and post-exit journal template.

  Complete when: Profit target, stop-loss, and time stop are all defined with exact prices. Adjustment triggers are specific and measurable. Maximum 2 rolls permitted.

