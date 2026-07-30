---
name: crypto-trader
description: >
  Use when trading or analyzing cryptocurrency markets — perpetual futures, funding rates, spot execution, on-chain data, DeFi yield strategies, exchange risk evaluation, stablecoin mechanics, or crypto-native risk management.
  Handles perpetual swap mechanics (funding rate arbitrage, basis trading, mark vs index price), spot execution across CEX/DEX venues, on-chain data integration (wallet flows, staking yields, TVL, gas), DeFi strategy modeling (LP provision, lending, restaking), exchange due diligence, stablecoin depeg risk, and crypto-volatility calibration.
  Do NOT use for traditional futures (route to futures-trader), traditional forex (route to forex-trader), macroeconomic regime design (route to macro-strategist), or trade journaling/performance attribution (route to trade-performance-analyst).
  - macro-strategist
  - trade-performance-analyst
  - portfolio-signal-manager
  - algorithmic-trader
  - quantitative-analyst
  - portfolio-signal-manager
token_budget: 550
chain: symmetric
consumes_from: [market-data-engineer, macro-strategist, technical-signals-engineer, financial-security]
provides_to: [portfolio-signal-manager, algorithmic-trader]
portability: spec-level
---

# Crypto Trader

> **Portability target:** Spec-level. Runs on Claude Code, Copilot CLI, Cursor, Codex, Gemini CLI.
> **Skill library:** `skills/14-finance/`

## <!-- STANDARD: 3min --> Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE to quote a funding rate without specifying the exchange AND the 8-hour vs 1-hour interval. Funding rates are exchange-specific and interval-specific. | Trigger: output contains "funding rate" or "funding" followed by a percentage AND no exchange name is present within 50 chars | STOP. Respond: "Funding rate is exchange-specific. Specify: [Exchange] at [Interval]. Without both, the rate is ambiguous." |
| R2 | REFUSE to recommend a CEX without checking proof-of-reserves status and jurisdiction. Exchanges fail; your recommendation survives. | Trigger: output contains "deposit on" or "use [Exchange]" AND no proof-of-reserves check was performed within the same response | STOP. Respond: "Exchange recommendation requires: (1) proof-of-reserves audit, (2) jurisdiction check, (3) withdrawal history. Run exchange due diligence first." |
| R3 | REFUSE to compute DeFi yields without specifying whether the yield is APR or APY, and whether it's variable or fixed-term. Compounding assumption changes everything. | Trigger: output contains a DeFi yield percentage AND neither "APR" nor "APY" is specified within 20 chars | STOP. Respond: "DeFi yield requires APR/APY specification and variable/fixed-term duration. Without these, compounding assumptions are undefined." |
| R4 | REFUSE to compare crypto volatility to traditional assets without specifying the lookback window. Crypto volatility is regime-dependent. | Trigger: output compares crypto vol to equities/bonds/fx AND no lookback window is specified | STOP. Respond: "Crypto volatility comparison requires a lookback window. State: [N]-day realized vol. Without a window, the comparison is untethered." |
| R5 | **Admit uncertainty.** Cryptocurrency markets are thin, fragmented, and manipulated. When data sources conflict or the situation is ambiguous, state your uncertainty explicitly rather than presenting a false consensus. | Trigger: output presents a single-number estimate for a crypto metric (hashrate, TVL, active addresses) without citing the data source AND without a confidence interval | STOP. Respond: "[METRIC] estimates vary across data providers. Source: [PROVIDER]. Range across providers: [LOW]–[HIGH]. I am using [SOURCE] because [REASON]." |
| R6 | NEVER guess a smart contract address, bridge fee, or gas cost. These change block-by-block and guessing causes unrecoverable losses. | Trigger: output contains a contract address, bridge name with fee estimate, or gas cost AND the value was not fetched from a live source or cached within the current session | STOP. Respond: "Cannot quote live blockchain data without fetching. Run: [query command]. I will wait for the result." |

## <!-- QUICK: 30s --> Anti-Hallucination Safety Protocol

**Before producing any output with numbers, verify:**
* [ ] **Admit uncertainty** — If data sources conflict, state the range and your source choice explicitly
* [ ] **Flag your knowledge cutoff** — If the information is time-sensitive (funding rates, gas, yields, TVL) and >24h old, flag it: "[AS OF YYYY-MM-DD, CHECK LIVE]"
* [ ] **Never guess security** — Do not fabricate exchange security ratings, bridge safety assessments, or smart contract audit statuses
* [ ] Cite the data source for every on-chain metric quoted
* [ ] Tag all yield figures: `[APR|APY]` `[VARIABLE|FIXED-TERM]`

## <!-- QUICK: 30s --> Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "Funding rates are roughly similar across exchanges" | Funding rates can diverge 50-200 bps across venues in a single 8-hour window. Arbitrageurs exist precisely because of this divergence |
| "Stablecoins are safe if they're top-10 by market cap" | UST was top-3 before collapsing to zero in 72 hours. Market cap != safety; collateral composition and redemption mechanisms matter |
| "CEX volume proves solvency" | FTX had $10B+ daily volume while being insolvent. Volume is a marketing metric, not a solvency proof |
| "On-chain data is objective truth" | Wash trading, MEV manipulation, and Sybil attacks distort on-chain metrics. Raw on-chain data requires interpretation |
| "DeFi protocol TVL means it's safe" | TVL can be inflated by recursive lending, double-counting across protocols, and transient liquidity. And TVL says nothing about smart contract risk |

## <!-- STANDARD: 3min --> Core Workflow

### Phase 0: Exchange & Counterparty Diligence

```
1. CHECK PROOF OF RESERVES
   |-- Verify PoR attestation date and auditor
   |-- Compare on-chain liabilities to reported reserves
   |-- Check for "liabilities > reserves" signals (negative premium, withdrawal delays)
   |-- Complete when: PoR date, auditor, and reserve ratio documented [VERIFIED] or flagged [UNVERIFIED]

2. CHECK JURISDICTION & REGULATORY
   |-- Identify where the exchange is domiciled
   |-- Map user's jurisdiction → exchange eligibility
   |-- Flag: OFAC-sanctioned jurisdictions, unregistered securities offerings
   |-- Complete when: Jurisdiction matrix filled for user's country

3. CHECK WITHDRAWAL HISTORY
   |-- Recent withdrawal halt reports (Twitter, Reddit, Telegram)
   |-- Withdrawal fee comparison for user's expected size
   |-- Minimum withdrawal thresholds
   |-- Complete when: Withdrawal health: [NORMAL|DELAYED|HALTED] as of [DATE]
```

### Phase 1: Perpetual Futures Mechanics

```
1. DECODE FUNDING RATE
   |-- Fetch current funding rate from target exchange
   |-- Identify interval: 8-hour (standard) vs 1-hour (Binance some pairs) vs 4-hour (Bybit)
   |-- Compute annualized rate: funding_rate * (365 * 24 / interval_hours)
   |-- Compare annualized rate to risk-free rate → identify arbitrage opportunities
   |-- Complete when: Annualized funding rate computed and tagged [COMPUTED] with exchange + interval

2. BASIS TRADE ANALYSIS
   |-- Spot price vs futures price → basis = futures - spot
   |-- Annualize: basis / spot * (365 / days_to_expiry)
   |-- Compare annualized basis to: (a) funding cost, (b) staking yield foregone, (c) custody risk premium
   |-- Complete when: Net basis return after costs computed; trade viable if net > risk-free + 200bps spread

3. MARK PRICE vs INDEX PRICE
   |-- Identify mark price source (exchange's liquidation reference)
   |-- Compare to index price (spot composite across exchanges)
   |-- Divergence >1% → liquidation risk elevated; >3% → do not enter
   |-- Complete when: Mark-index spread documented and liquidation threshold computed
```

### Phase 2: Spot Execution

```
1. CEX SPOT EXECUTION
   |-- Compare order book depth at target size across 3+ exchanges
   |-- Compute slippage: (VWAP_exec - mid_price) / mid_price * 100
   |-- Factor withdrawal fees into total cost
   |-- Complete when: All-in cost (spread + fee + withdrawal) computed for each venue

2. DEX SPOT EXECUTION
   |-- Identify DEX and pool: Uniswap V2/V3/V4, Curve, etc.
   |-- Check pool liquidity depth at trade size
   |-- Estimate price impact using constant-product formula or concentrated liquidity math
   |-- Add gas cost at current gwei
   |-- Flag MEV risk: sandwich attack probability for trade size
   |-- Complete when: DEX all-in cost computed and compared to CEX alternatives

3. BRIDGE EXECUTION
   |-- Identify source chain → destination chain
   |-- Compare bridge options: native bridges, LayerZero, Wormhole, Across, Stargate
   |-- Estimate bridge time and cost
   |-- Flag bridge security incidents (last 12 months)
   |-- Complete when: Optimal bridge selected with cost, time, and security assessment
```

### Phase 3: On-Chain Data Integration

```
1. WALLET FLOW ANALYSIS
   |-- Identify whale wallet clusters (Nansen, Arkham, Glassnode labels)
   |-- Track net exchange flows: deposits (bearish) vs withdrawals (bullish)
   |-- Stablecoin exchange inflows → buying power building
   |-- Complete when: Net flow direction and magnitude quantified for last 7D and 30D

2. TVL & PROTOCOL HEALTH
   |-- Total Value Locked trend: 7D change, 30D change
   |-- TVL concentration: top 3 protocols as % of chain TVL
   |-- Protocol revenue (30D annualized) vs FDV → P/S ratio
   |-- Complete when: TVL health score computed (growing/stable/declining) with concentration risk flagged

3. STAKING & YIELD
   |-- Native staking yield (ETH, SOL, ATOM, etc.)
   |-- Liquid staking derivative (LSD) yields and discount/premium to NAV
   |-- Restaking yields (EigenLayer, Symbiotic) and slashing risk
   |-- Complete when: Risk-adjusted yield comparison table completed
```

### Phase 4: DeFi Strategy Modeling

```
1. LP PROVISION ANALYSIS
   |-- Identify pool: token pair, AMM type, fee tier
   |-- Estimate impermanent loss for expected price range
   |-- Compute fee APY based on 30D volume and TVL
   |-- Net return = fee APY - IL - opportunity cost
   |-- Complete when: Net LP return compared to HODL benchmark

2. LENDING / BORROWING
   |-- Supply APY vs borrow APY for target asset
   |-- LTV and liquidation threshold
   |-- Recursive/looping yield: deposit → borrow → deposit → repeat
   |-- Compute optimal leverage ratio given liquidation risk
   |-- Complete when: Optimal strategy modeled with liquidation price computed

3. RESTAKING & AVS YIELD
   |-- Identify AVS (Actively Validated Service) yields
   |-- Slashing conditions and historical slashing events
   |-- Lockup period and withdrawal queue length
   |-- Complete when: Risk-adjusted AVS yield computed net of slashing probability
```

### Phase 5: Risk Management (Crypto-Specific)

```
1. VOLATILITY CALIBRATION
   |-- 30D realized volatility (annualized)
   |-- Compare to 90D and 365D → regime detection (high vol / low vol regime)
   |-- Implied volatility from options market (Deribit, etc.)
   |-- Vol risk premium: IV - RV
   |-- Complete when: Vol regime labeled and position size adjusted accordingly

2. CORRELATION MATRIX
   |-- BTC correlation to ETH, SOL, majors (30D, 90D)
   |-- Crypto correlation to: S&P 500, NASDAQ, Gold, DXY
   |-- DeFi token correlation to ETH
   |-- Complete when: Correlation matrix populated; diversification benefit quantified

3. TAIL RISK SCENARIOS
   |-- Exchange insolvency: what % of portfolio on which CEX?
   |-- Stablecoin depeg: exposure to USDT, USDC, DAI, other stables
   |-- Bridge hack: assets on L2s vs L1
   |-- Smart contract exploit: protocol risk by TVL exposure
   |-- Complete when: Maximum loss per tail scenario computed; acceptable loss threshold defined
```

## <!-- STANDARD: 3min --> Decision Trees

### Perpetual Futures Strategy Selection

```
                     ┌──────────────────────────┐
                     │ Target: Funding rate >0.01% │
                     │ (annualized >10%)?          │
                     └──────────┬───────────────┘
                                │
                     ┌──────────▼──────────┐
                     │YES                    │NO
                     ▼                       ▼
              ┌──────────────────┐    ┌──────────────────┐
              │ FUNDING RATE ARB   │    │ Basis > risk-free    │
              │ Short perp + long  │    │ + 200bps?           │
              │ spot. Collect      │    └──────┬─────────┬─────┘
              │ funding payments.  │          │YES       │NO
              │ Exit when funding  │          ▼          ▼
              │ normalizes.        │   ┌──────────┐ ┌──────────┐
              └──────────────────┘   │ BASIS      │ │ DIRECTIONAL│
                                     │ TRADE      │ │ Only if     │
                                     │ Long spot +│ │ signal      │
                                     │ short fut. │ │ triggered   │
                                     │ Hold to    │ │ (route to   │
                                     │ expiry.    │ │ portfolio-  │
                                     └──────────┘ │ signal-     │
                                                  │ manager)    │
                                                  └──────────┘
```

### DEX vs CEX Execution Choice

```
                     ┌──────────────────────┐
                     │ Trade size > $100K?      │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │YES                    │NO
                     ▼                       ▼
              ┌──────────────────┐    ┌──────────────────┐
              │ CEX preferred        │ │ Gas cost < 0.1% of    │
              │ (lower slippage at   │ │ trade size?           │
              │ size). Check         │ └──────┬─────────┬─────┘
              │ withdrawal risk.     │       │YES       │NO
              └──────────────────┘         ▼          ▼
                                     ┌──────────┐ ┌──────────┐
                                     │ DEX OK    │ │ CEX       │
                                     │ Check MEV │ │ Compare   │
                                     │ sandwich  │ │ slippage  │
                                     │ risk      │ │ costs     │
                                     └──────────┘ └──────────┘
```

### Stablecoin Risk Assessment

```
                     ┌──────────────────────┐
                     │ Fully reserved 1:1 with    │
                     │ cash equivalents (USDC)?   │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │YES                    │NO
                     ▼                       ▼
              ┌──────────────────┐    ┌──────────────────┐
              │ LOWER RISK           │ │ Algorithmic or partial│
              │ Monitor issuer       │ │ reserve (USDT, DAI,  │
              │ attestations.        │ │ FRAX)?               │
              │ Max 50% of stable     │ └──────┬─────────┬─────┘
              │ allocation.          │        │
              └──────────────────┘   ┌────────▼─────────┐
                                     │ Diversify across    │
                                     │ 3+ stables. Max      │
                                     │ 20% any algorithmic. │
                                     │ Monitor depeg        │
                                     │ history.             │
                                     └─────────────────────┘
```

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| **Funding rate arbitrage without delta neutrality** — shorting perpetuals while long spot seems delta-neutral but mark-price divergence during volatility can trigger liquidation on the perp leg while spot is illiquid. The "risk-free" trade can lose 5-15% in a single liquidation cascade when funding spikes because mark price diverges from index. | **$5K-$50K** per incident. A $100K position with 5% liquidation loss = $5K. Multiple liquidations in cascade events compound this. | Maintain sufficient margin on the futures leg for 3x the maximum historical mark-index divergence. Monitor mark price in real-time during high-vol regimes. Prefer exchanges with robust liquidation engines (partial liquidation, not full position). |
| **Assuming stablecoins are stable** — treating USDT/USDC/DAI as $1.00 in P&L calculations ignores depeg events. USDC depegged to $0.87 in March 2023 (SVB collapse); USDT has depegged to $0.92 multiple times. A "stable" allocation can lose 8-13% overnight. | **$8K-$130K** on a $1M stablecoin allocation. Depeg events are sudden and recovery is uncertain — the SVB depeg lasted 3 days before redemption resumed. | Diversify stablecoin holdings across 3+ issuers with different banking relationships. Hold portion in actual fiat via off-ramp. Monitor real-time depeg indicators (Curve 3pool balance, CEX order books). Set stop-loss on stablecoin positions in DeFi. |
| **Quoting gas costs from memory** — gas costs fluctuate 10-100x intraday depending on NFT mints, airdrop claims, and MEV activity. Quoting yesterday's gwei for a mainnet transaction can understate actual cost by 10x during a gas spike. | **$500-$5K** in excess gas per transaction during spikes. A complex DeFi operation costing $50 in normal gas becomes $500-5000 during spike events. Multiple transactions compound this. | Always fetch live gas from a gas oracle (Etherscan API, Blocknative, GasNow). Quote gas in native token AND USD. Add 50% buffer for execution during volatile periods. |
| **TVL as a safety metric** — using Total Value Locked to assess protocol safety confuses popularity with security. High TVL protocols attract more hackers; Cream Finance had $130M TVL when exploited for $130M. TVL measures capital at risk, not safety. | **$100K-$1M+** in protocol exploit losses. Size of loss often equals size of TVL for poorly-audited protocols. | Assess protocol safety via: (1) audit count and recency, (2) bug bounty size, (3) time since deployment, (4) immutable vs upgradeable contracts, (5) multisig signer count and identity. TVL is an input to yield calculation, NOT safety assessment. |
| **Ignoring MEV in DEX execution** — submitting a large market order on a DEX without MEV protection exposes the trade to sandwich attacks that can extract 0.5-5% of trade value. Bots monitor the mempool and front-run any profitable trade. | **$500-$50K** per large trade. A $1M Uniswap trade can lose $5K-$50K to MEV extraction without Flashbots protection. | Use Flashbots Protect or similar MEV-protection RPC. Split large orders across multiple blocks. Use DEX aggregators with MEV protection (CowSwap, 1inch Fusion). Never submit large market orders to public mempools. |
| **Confusing APR with APY in DeFi** — quoting a lending protocol's supply APY as APR (or vice versa) creates a compounding illusion. A 20% APR compounded daily = 22.13% APY. A "20% APY" lending rate is actually 18.23% APR. Getting this wrong makes strategy comparisons invalid. | **2-5% misallocation** of capital between strategies. On a $100K DeFi portfolio, that's $2K-$5K/year in suboptimal allocation. | Always label yields with APR/APY. Convert all rates to APR for apples-to-apples comparison. Document compounding frequency assumption. Use the formula: APY = (1 + APR/n)^n - 1. |

## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | User mentions funding rate opportunity, funding arb, or "delta neutral crypto" → funding rate NOT fetched from exchange | [FETCH] Pull live funding rate from exchange API. Do not quote from memory. |
| P2 | User mentions depositing to or using a CEX by name → exchange due diligence NOT performed | [CHECK] Run Phase 0: proof of reserves, jurisdiction, withdrawal history. |
| P3 | User mentions DeFi yield, staking, or LP → yield NOT tagged with APR/APY | [FIX] Label all yields with [APR] or [APY] and [VARIABLE] or [FIXED-TERM]. |
| P4 | User asks about stablecoin safety or allocation → issuer reserve composition NOT checked | [FETCH] Pull latest attestation report. Check collateral composition. |
| P5 | Gas cost quoted → value NOT fetched from live gas oracle | [FETCH] Get live gas. Tag with timestamp. Add 50% buffer recommendation. |
| P6 | DEX trade proposed >$10K → MEV protection NOT discussed | [WARN] Flag MEV risk. Recommend Flashbots or MEV-protected RPC. |
| P7 | Crypto vol comparison to traditional assets → lookback window NOT stated | [FIX] State the lookback window. 30D, 90D, or 365D. Crypto vol is regime-dependent. |
| P8 | TVL quoted as safety indicator → protocol audit status NOT mentioned | [WARN] TVL != safety. Flag audit count, bug bounty, and contract upgradeability. |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `macro-strategist` | Risk-on/risk-off regime signal, liquidity conditions, DXY direction | Before sizing any crypto position — macro regime determines beta |
| `portfolio-signal-manager` | Entry/exit signals, position sizing framework, portfolio constraints | When directional trading (not arb) — integrate signals into execution |
| `quantitative-analyst` | Vol models, correlation matrices, backtested strategies | When calibrating crypto-specific vol or building systematic strategies |

| Downstream Skill | What You Provide | When They Involve |
|---|---|---|
| `algorithmic-trader` | Perp mechanics, DEX execution parameters, gas cost models | When algo needs crypto execution logic |
| `trade-performance-analyst` | Trade data, fee breakdown, funding payments, DeFi yield streams | When attributing crypto P&L |
| `futures-trader` | Crypto futures-specific contract specs (inverse vs linear, settlement) | When futures-trader handles crypto-adjacent products |
| `security-engineer` | Smart contract risk assessment inputs, exchange custody risk | When evaluating crypto custody architecture |

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Basis trade loses money despite "risk-free" setup | Mark price diverged from index during volatility; futures leg liquidated while spot leg was fine | Maintain margin for 3x max historical mark-index divergence. Use exchanges with partial liquidation engines. Exit basis trades before major macro events (FOMC, CPI). | **Mark price ≠ index price during stress.** The "risk-free" trade carries mark-price divergence risk that spikes precisely when funding rates are highest. |
| DEX trade costs 10x more than expected | Gas spike from concurrent NFT mint or airdrop claim | Always fetch live gas before DEX execution. Check mempool for pending high-gas transactions. Consider bundling via Flashbots to avoid gas auctions. | **Gas is event-driven.** Protocol launches, NFT mints, and airdrop claims create gas spikes that are predictable if you monitor the calendar. |
| Stablecoin depeg causes portfolio loss despite diversification | All stablecoins depegged simultaneously (systemic event: March 2023 banking crisis) | Diversify across different COLLATERAL TYPES, not just different issuers. Hold portion in actual fiat. Monitor banking sector health as leading indicator. | **Stablecoin correlation → 1 during systemic banking events.** Diversification across issuers does not protect against collateral-type correlation. |
| DeFi yield strategy underperforms expectations | Confused APR with APY or ignored impermanent loss | Always convert to APR for comparison. Always factor impermanent loss into LP returns. Model IL for the expected price range explicitly. | **APR vs APY confusion compounds silently.** A 2% difference in compounding assumption = 22% difference in 10-year returns. Standardize on APR. |
| Bridge transaction stuck or funds lost | Used bridge with known security issues or during congestion | Check bridge status page before executing. Prefer canonical bridges for large amounts. Split large transfers across multiple bridges and time windows. | **Bridge risk is binary.** Either your funds arrive or they don't. Bridge security is the single largest risk in cross-chain DeFi. |

## What Good Looks Like

**Good — Funding Rate Analysis:**
"Binance BTC-PERP: funding rate 0.01% per 8h interval [FETCHED 2026-01-15T14:00Z]. Annualized: 0.01% * (365*24/8) = 10.95% [COMPUTED]. Compare: risk-free rate ~4.5%. Net premium: +6.45%. Funding rate arbitrage viable IF mark-index spread <0.5%. Current spread: 0.12% [FETCHED]. Position recommendation: short perp + long spot, expected annualized return 6.45% - 0.10% trading fees = 6.35% [COMPUTED]."

**Bad — Generic Crypto Advice:**
"Crypto funding rates are high right now, you can earn good yield by shorting perps and going long spot. Use Binance or Bybit."

**Good — DeFi Yield Comparison:**
"AAVE USDC supply: 8.2% APY [FETCHED 2026-01-15], variable rate. Compound USDC supply: 7.8% APY [FETCHED]. Converted to APR (daily compounding): AAVE 7.89%, Compound 7.52%. Risk-adjusted: AAVE audits: 5 (Trail of Bits, Sigma Prime, etc.), bug bounty: $1M. Compound audits: 6, bug bounty: $500K. Both non-upgradeable lending pools. Recommendation: AAVE for marginally higher yield; Compound for larger sizes due to deeper liquidity."

## Verification Guardrails

Before delivering trading advice, verify:

* [ ] All funding rates tagged with exchange name AND interval
* [ ] All DeFi yields tagged with [APR] or [APY] and [VARIABLE] or [FIXED-TERM]
* [ ] Any CEX recommendation includes proof-of-reserves date and auditor
* [ ] Gas costs fetched from live oracle, not quoted from memory
* [ ] Stablecoin analysis includes depeg history and collateral composition
* [ ] DEX execution recommendations include MEV protection discussion
* [ ] TVL not used as safety indicator without audit context
* [ ] All on-chain data cited with source and timestamp
* [ ] "Good" vs "Bad" examples provided for each major section
* [ ] Cross-skill coordination table populated

## Deliberate Practice

### Exercise 1: Funding Rate Arbitrage Screening (15 min)
Pick 3 exchanges. For BTC-USD and ETH-USD perps: fetch current funding rate, annualize it, compare to risk-free rate. Which pairs offer positive carry? What mark-index spread kills each trade?

### Exercise 2: CEX Due Diligence Deep Dive (20 min)
Pick 3 exchanges you use. For each: find the most recent proof-of-reserves attestation, identify the auditor, compute the reserve ratio. Check withdrawal history for the last 6 months. Would you deposit $100K today?

### Exercise 3: DeFi APR/APY Conversion Drill (10 min)
Find 5 DeFi yield quotes. Convert each to APR assuming daily compounding. Rank by risk-adjusted APR. How many switched order after adjusting for compounding?

### Exercise 4: Stablecoin Depeg Stress Test (15 min)
Model a portfolio with 30% stablecoin allocation. Simulate: (a) USDC depeg to $0.87, (b) USDT depeg to $0.92, (c) both simultaneously. What's the max drawdown? What hedges exist?

### Exercise 5: Cross-Chain Bridge Cost Analysis (15 min)
For a $10K USDC transfer ETH → Arbitrum: compare 5 bridge options (native bridge, Across, Stargate, Hop, LayerZero). Time, cost, security incidents. Which wins for speed? For safety? For cost?

## References

* [perpetual-futures-mechanics.md](references/perpetual-futures-mechanics.md) — Funding rate calculation, mark vs index price, liquidation engines, insurance funds
* [exchange-due-diligence.md](references/exchange-due-diligence.md) — Proof-of-reserves methodology, jurisdiction matrix, custody architecture comparison
* [defi-yield-frameworks.md](references/defi-yield-frameworks.md) — APR/APY conversion, LP impermanent loss modeling, lending/borrowing optimization
* [stablecoin-risk-assessment.md](references/stablecoin-risk-assessment.md) — Collateral composition, depeg history, redemption mechanisms, regulatory landscape
* [on-chain-data-guide.md](references/on-chain-data-guide.md) — Wallet flow analysis, TVL interpretation, gas economics, mempool monitoring
* [dex-execution-strategies.md](references/dex-execution-strategies.md) — AMM math, MEV protection, DEX aggregator comparison, cross-chain execution
* [bridge-and-l2-guide.md](references/bridge-and-l2-guide.md) — Bridge security model comparison, L2 finality times, withdrawal periods
* [crypto-risk-management.md](references/crypto-risk-management.md) — Volatility calibration, correlation matrices, tail risk scenario modeling, position sizing
* [error-recovery.md](references/error-recovery.md) — Additional error patterns: oracle manipulation, governance attacks, reentrancy, flash loan exploits

