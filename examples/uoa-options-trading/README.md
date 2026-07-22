# UOA Options Trading System — From Research to Execution

> **Example project using the 14-finance domain + existing skills**
> A solo quant trader building an unusual options activity (UOA) detection and execution system for mid-cap equities.
>
> **Skills activated:** 15 (3 new finance skills + 12 existing)

---

## The Trader's Story

I'm a retail trader who follows unusual options activity on mid-cap companies. My edge: when a single transaction moves $1M+ in premium on at-the-money or out-of-the-money options with 7+ days to expiration, it's often institutional smart money positioning ahead of a move. I want to detect these signals programmatically, backtest entry/exit/trim strategies, and execute with discipline — not emotion.

I'm not building a SaaS. This is a personal trading system. It needs to be reliable, fast, and private.

---

## Full Skill Chain

```
UNUSUAL OPTIONS ACTIVITY → TRADE EXECUTION PIPELINE
═══════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DATA PIPELINE                                              │
│                                                                     │
│  market-data-engineer ───> Options flow ingestion                   │
│  │  Unusual Whales API → Kafka → TimescaleDB                        │
│  │  Polygon.io → historical options chains → Parquet/S3             │
│  │                                                                  │
│  data-engineer ───> ETL orchestration (Airflow/Dagster)             │
│  database-reliability-engineer ───> TimescaleDB operations           │
│  security-engineer ───> API key vault, encrypted storage            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 2: QUANTITATIVE ANALYSIS                                      │
│                                                                     │
│  quantitative-analyst ───> UOA signal detection                     │
│  │  ┌─────────────────────────────────────────────────────────┐    │
│  │  │ Detection Pipeline:                                      │    │
│  │  │  1. Filter: premium ≥ $1M, mid-cap, ATM/OTM, 7-365 DTE  │    │
│  │  │  2. Classify: sweep/block/split, ask-side/bid-side       │    │
│  │  │  3. Compute: IV rank, Greeks, volume/OI ratio            │    │
│  │  │  4. Score: STRONG BUY / BUY / WEAK BUY / NEUTRAL         │    │
│  │  │  5. Output: structured signal JSON → algorithmic-trader   │    │
│  │  └─────────────────────────────────────────────────────────┘    │
│  │                                                                  │
│  data-scientist ───> Statistical validation of signal efficacy     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 3: TRADING ENGINE                                             │
│                                                                     │
│  algorithmic-trader ───> Strategy execution                         │
│  │  ┌─────────────────────────────────────────────────────────┐    │
│  │  │ Trade Pipeline:                                          │    │
│  │  │  1. Consume signal → apply conviction filter             │    │
│  │  │  2. Position size → Kelly × account risk cap             │    │
│  │  │  3. Entry → momentum OR pullback, 50/30/20 scaling       │    │
│  │  │  4. Monitor → trailing stop 2× ATR, time stop 5 days     │    │
│  │  │  5. Trim → 25% at +10%, 25% at +20%, 25% at +40%        │    │
│  │  │  6. Exit → trailing stop hit OR signal invalidated       │    │
│  │  └─────────────────────────────────────────────────────────┘    │
│  │                                                                  │
│  system-architect ───> System design, component boundaries         │
│  backend-developer ───> Trade execution service, broker API         │
│  finops-engineer ───> Brokerage cost optimization                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 4: MONITORING & DASHBOARD                                     │
│                                                                     │
│  frontend-developer ───> P&L dashboard, signal feed, position view  │
│  observability-engineer ───> Trade execution latency, error rates  │
│  analytics-engineer ───> Performance attribution, Sharpe, drawdown │
│  devops-engineer ───> Deployment, uptime (critical during market)  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 5: RISK & REFINEMENT                                          │
│                                                                     │
│  data-scientist ───> Backtest new strategies, regime analysis      │
│  qa-engineer ───> Validate trade execution correctness             │
│  performance-engineer ───> Optimize signal processing latency      │
│  incident-responder ───> "Market open, system down" runbook        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## The UOA Signal Detection Pipeline (Detail)

### Filtering Rules

| Criteria | Threshold | Reason |
|----------|-----------|--------|
| Premium | ≥ $1,000,000 | Filters noise. Institutional money leaves footprints this size. |
| Market cap | $2B - $10B (mid-cap) | Large caps have too much hedging noise. Small caps have no options liquidity. |
| Moneyness | ATM (±5% of spot) or OTM | Deep ITM is often hedging, not directional bets. |
| DTE | 7 - 365 days | < 7 days: gamblers. > 365 days: LEAPS hedging, too slow. |
| Side | Ask-side preferred | Buying = initiating position. Selling = could be closing. |
| Condition | Sweep, Block, Split | Single-leg calls/puts preferred over complex spreads for directional signals. |

### Signal Scoring Matrix

| Score | Premium | Moneyness | OI Impact | IV Context | Action |
|-------|---------|-----------|-----------|------------|--------|
| **STRONG BUY** | $5M+ | OTM (>5%) | Vol > 2× OI | IV rank > 70 | Full position, momentum entry |
| **BUY** | $1M-$5M | ATM/OTM | Vol > OI | IV rank > 50 | Standard position, pullback entry |
| **WEAK BUY** | $1M-$5M | ATM | Vol < OI | IV rank 30-50 | Half position, wait for confirmation |
| **NEUTRAL** | Any | Any | Any | Any | No trade |
| **FADE (SELL)** | $1M+ | Deep OTM (>20%) | Vol > 3× OI | IV rank > 90 | Fade the move — lottery ticket |

---

## Entry, Exit & Trim Strategies

### Entry Strategies

```
Signal Received → Which entry?
├── STRONG BUY + price above VWAP → Momentum Entry (same day)
├── STRONG BUY + price below VWAP → Pullback Entry (wait for VWAP reclaim)
├── BUY signal + earnings within 5 days → Skip (hedging noise)
├── BUY signal + sector confirming → Standard Entry (next day)
└── WEAK BUY → Half position, Pullback Entry only
```

**Momentum Entry:** Enter within 30 minutes of signal confirmation. Price must be trading above pre-signal high. Use limit orders, not market — mid-cap spreads can be wide.

**Pullback Entry:** Wait for price to pull back to 20-period EMA on 30-min chart. Enter on bounce confirmation (bullish engulfing candle). Better risk/reward. Might miss 30% of moves but improves win rate.

**Scaling Entry:** 50% on initial signal, 30% on first higher high after entry, 20% on break of resistance. Never average down on a losing position.

### Exit Strategies

| Exit Type | Trigger | Action |
|-----------|---------|--------|
| Profit Target 1 | +10% from entry | Sell 25% of position |
| Profit Target 2 | +20% from entry | Sell 25% of position |
| Profit Target 3 | +40% from entry | Sell 25% of position |
| Trailing Stop | 2× ATR(14) from highest high | Sell remaining 25% |
| Time Stop | 5 trading days, no movement | Sell 100% |
| Signal Invalidation | Thesis broken | Sell 100% immediately |
| Hard Stop | -8% from entry | Sell 100% — first loss is best loss |

### Trim Ladder

```
Entry at $50.00 (1,000 shares = $50,000 position)
│
├── $55.00 (+10%) → Sell 250 shares → Lock in $1,250
│   Remaining: 750 shares, cost basis effectively ~$48.33
│
├── $60.00 (+20%) → Sell 250 shares → Lock in $2,500
│   Remaining: 500 shares, cost basis effectively ~$45.00
│
├── $70.00 (+40%) → Sell 250 shares → Lock in $5,000
│   Remaining: 250 shares, 2×ATR trailing stop at $65.80
│
└── Trailing stop hit at $65.80 → Sell 250 shares → Lock in $3,950
    Total P&L: $12,700 on $50,000 risk = 25.4% return
```

---

## System Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Unusual      │    │ Polygon.io   │    │ CBOE OPRA    │
│ Whales API   │    │ Options API  │    │ (future)     │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Kafka /   │
                    │  Redpanda   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼──────┐ ┌───▼──────────┐
       │ Stream Proc │ │ Raw     │ │ Alert        │
       │ (Python/Go) │ │ Store   │ │ Engine       │
       └──────┬──────┘ │(S3/Parq)│ └───┬──────────┘
              │         └─────────┘     │
       ┌──────▼──────┐                  │
       │ TimescaleDB │                  │
       │ (analytics) │                  │
       └──────┬──────┘                  │
              │                         │
       ┌──────▼──────┐          ┌──────▼──────┐
       │ Quant       │          │ Pushover /  │
       │ Analysis    │──────────▶ Telegram    │
       │ Engine      │          │ Alerts      │
       └──────┬──────┘          └─────────────┘
              │
       ┌──────▼──────┐
       │ Trading     │
       │ Engine      │──────▶ Alpaca/IBKR API
       └──────┬──────┘
              │
       ┌──────▼──────┐
       │ P&L         │
       │ Dashboard   │
       │ (Next.js)   │
       └─────────────┘
```

---

## What This Example Demonstrates

1. **Domain-specific skills extending the library** — The 14-finance domain adds specialized knowledge that general skills (data-engineer, data-scientist) don't cover
2. **Signal-to-execution pipeline** — A complete workflow from raw market data to trade execution
3. **Entry/exit/trim discipline** — Rules-based position management removes emotion from trading
4. **Solo trader scaling** — One person can build and operate this system using our tiered activation model
5. **Real risk management** — Position sizing, correlation limits, drawdown stops — not academic theory

---

## Skills Used (with domain)

| Skill | Domain | Phase |
|-------|--------|-------|
| market-data-engineer | 14-finance | Data Pipeline |
| quantitative-analyst | 14-finance | Signal Detection |
| algorithmic-trader | 14-finance | Trade Execution |
| data-engineer | 09-data | ETL Pipeline |
| database-reliability-engineer | 09-data | TimescaleDB Ops |
| data-scientist | 09-data | Backtesting, Validation |
| analytics-engineer | 09-data | P&L Dashboards |
| system-architect | 04-architecture | System Design |
| backend-developer | 05-development | Execution Engine |
| frontend-developer | 05-development | Dashboard UI |
| security-engineer | 08-security | API Keys, Encryption |
| devops-engineer | 07-devops | Deployment |
| observability-engineer | 07-devops | Monitoring |
| finops-engineer | 07-devops | Brokerage Cost Mgmt |
| performance-engineer | 13-specialized | Latency Optimization |
| incident-responder | 08-security | Market Hours Runbook |
| qa-engineer | 06-quality | Trade Verification |
