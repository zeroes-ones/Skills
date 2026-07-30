# Portfolio Engine — Full Computation Reference

Extracted from Core Workflow Phases 0-5 for progressive disclosure. Loaded on demand when the model needs implementation-level detail.

## Phase 0: MCP Broker Connection State Machine

### States
DISCONNECTED → AUTHENTICATING → CONNECTED → SYNCING → READY → EXECUTING → RECONCILING → DISCONNECTED

| State | Actions |
|-------|---------|
| AUTHENTICATING | OAuth token exchange or API key validation. Token expiry tracking: refresh 5 min before expiry. Failure: retry 3x with exponential backoff (1s, 5s, 25s), then alert |
| CONNECTED | WebSocket for real-time order/position updates. Heartbeat: ping every 30s, reconnect if no pong in 60s. Rate limit tracking: remaining requests per minute |
| SYNCING | Download positions (ticker, quantity, avg_cost, market_value, unrealized_pnl). Download orders (pending, filled today, rejected). Download account (buying_power, margin_used, margin_limit, portfolio_value). Reconcile: compare broker vs local, flag discrepancies >$100 |
| READY | Portfolio state current (sync <60s old). Buying power known. Idempotency key generator active. Circuit breaker configured (max 5 rejected orders in 60s → halt) |
| EXECUTING | Submit order with idempotency key. Await fill (timeout 30s market, 300s limit). On fill: update local position. On reject: log reason, do NOT retry without investigation. On timeout: query status, do NOT resubmit (idempotency protects) |
| RECONCILING | Post-execution: compare expected vs actual fill price. Post-settlement: verify T+2 completed. Daily: full position reconciliation |

### MCP Interface Contract
- `get_account()` → Account(buying_power, margin, portfolio_value, day_trades_left)
- `get_positions()` → [Position(ticker, qty, avg_cost, mkt_value, unrealized_pnl)]
- `get_orders(status)` → [Order(id, ticker, side, qty, filled_qty, status)]
- `place_order(ticker, side, qty, type, limit_price, idempotency_key)` → Order
- `cancel_order(order_id)` → bool
- `get_order_status(order_id)` → Order
- Resources: `broker://{broker_id}/account`, `broker://{broker_id}/positions`, `broker://{broker_id}/orders`

## Phase 1: Signal Ingestion & Conflict Resolution

### Technical Signal JSON Contract
```json
{
  "source": "technical-signals-engineer",
  "signal_id": "tech-{date}-{seq}",
  "ticker": "AAPL", "timestamp": "ISO8601", "direction": "BUY|SELL|HOLD",
  "confidence": 78,
  "confidence_breakdown": {"indicator_alignment": 85, "volume_confirmation": 72, "regime_support": 65, "timeframe_alignment": 80},
  "indicators": {"primary": [...], "confirming": [...], "cautioning": [...]},
  "regime": "trending|ranging|volatile",
  "parameters_used": {"rsi_period": 14, "bb_std": 2.0, "macd_fast": 12, "macd_slow": 26},
  "caveats": [...], "raw_confidence_after_caveats": 78
}
```

### Fundamental Signal JSON Contract
```json
{
  "source": "fundamental-analyst",
  "signal_id": "fund-{date}-{seq}",
  "ticker": "AAPL", "timestamp": "ISO8601", "direction": "BUY|SELL|HOLD",
  "confidence": 62,
  "confidence_breakdown": {"valuation_margin": 45, "quality_triangulation": 78, "earnings_quality": 70, "comparable_alignment": 55},
  "valuation": {"dcf_range": {"bear": 165, "base": 195, "bull": 230}, "current_price": 198, "margin_of_safety": -0.015, "comparables_median_pe": 31.5, "company_pe": 34.2},
  "quality_scores": {"piotroski_f_score": 7, "altman_z_score": 6.8, "beneish_m_score": -2.4},
  "red_flags": [], "caveats": [...]
}
```

### Conflict Detection Logic
- Both AGREE (both BUY, both SELL, both HOLD) → skip conflict resolution, proceed to sizing
- One HOLD, other ACTION (BUY/SELL) → treat HOLD as "don't add" not "oppose"
- DIRECT CONFLICT (one BUY, other SELL) → enter Weighted Decision Matrix

### Weighted Decision Matrix
**Step 1 — Calibrate:** Technical confidence × 0.85 (tends to overstate by ~15%). Fundamental confidence × 0.90 (tends to overstate by ~10%).

**Step 2 — Regime weights:**
| Regime | Technical Weight | Fundamental Weight |
|--------|:---:|:---:|
| Trending (ADX > 25) | 0.65 | 0.35 |
| Ranging (ADX < 20) | 0.35 | 0.65 |
| Volatile (VIX > 30) | 0.50 | 0.50 |
| Earnings week (±5 days) | 0.25 | 0.75 |

**Step 3 — Score:** Decision_Score = (Cal_tech × Tech_W × Tech_Dir) + (Cal_fund × Fund_W × Fund_Dir), where BUY=+1, HOLD=0, SELL=-1

**Step 4 — Thresholds:** >+15=BUY, +5 to +15=BUY_WITH_CAUTION, -5 to +5=HOLD, -5 to -15=SELL_WITH_CAUTION, <-15=SELL

**Step 5 — Caution gates:** Size capped at 50% of normal, stop-loss at 1.5× ATR (vs 2×), review after 5 trading days.

### Conflict Resolution Documentation
```json
{"ticker": "AAPL", "conflict": "BUY vs HOLD", "decision": "BUY_WITH_CAUTION", "decision_score": 11.2,
 "breakdown": {"tech_calibrated": 66.3, "fund_calibrated": 55.8, "regime": "trending", "tech_weight_applied": 0.65, "fund_weight_applied": 0.35},
 "rationale": "...", "risk_constraints": {"max_position_pct": 0.05, "stop_loss_atr_multiple": 1.5, "review_date": "2026-08-06"}}
```

## Phase 2: Position Sizing

### Capital Pool
- Buying_Power = min(Account.cash × 2, Account.margin_limit)
- Reserved_Capital = max(Portfolio_Value × 0.05, $5,000)
- Available_Capital = Buying_Power − Current_Exposure − Reserved_Capital

### Signal Triage (when signals > capital)
Signal_Priority_Score = (Calibrated_Confidence × 0.5) + (Quality_Triangulation/100 × 0.3) + (Regime_Compatibility × 0.2). Sort descending. Allocate top-down.

### Method A — Volatility-Adjusted 1/N (default)
Vol_Weight = 1 / (Asset_30d_Vol / Median_Vol_Across_All). Adjusted_Position = Base_Position × Vol_Weight. Caps: 10% portfolio ($25K max) per position, 5% for leveraged ETFs.

### Method B — Kelly Criterion (requires >50 trades, win_rate >0.45)
f* = (bp − q) / b where b = avg_win/avg_loss, p = win_rate, q = 1−p. Half-Kelly: f = f*/2. Position = Portfolio_Value × f.

### Method C — Risk-Parity (portfolio-level rebalancing)
Risk_Budget = Available_Capital × (1/N). Position = Risk_Budget / Asset_30d_Vol. Rebalance when drift >20%.

### Sizing Overrides
| Condition | Action |
|-----------|--------|
| ETF holdings overlap >90% with existing | Size=0, "Duplicate Exposure" |
| ±5 days of earnings | 50% reduction |
| BUY/SELL_WITH_CAUTION | 50% reduction |
| Sector would exceed 25% | Reduce to fit or skip |
| Position < $1,000 after sizing | Skip |
| VIX > 35 | 40% reduction all new |
| Drawdown >15% from peak | HALT, only defensive exits |

### Output: Sized Signal Queue
```json
[{"rank": 1, "ticker": "AAPL", "direction": "BUY", "decision": "AGREE",
  "position_size": "$8,200", "pct_portfolio": 0.82, "method": "vol-adjusted-1/N",
  "stop_loss": "$185.40", "take_profit": "$215.00", "limit_price": "$198.50"}, ...]
```

## Phase 3: Portfolio Risk Monitoring

### Real-Time Dashboard (every 60s)
| Metric | Formula | Alert Threshold |
|--------|---------|-----------------|
| Total Value | Σ(position.mkt_value) | — |
| Beta-Weighted Exposure | Σ(pos.mkt_value × pos.beta) | >1.5× portfolio |
| VaR(95%, 1-day) | Historical simulation, 252-day window | >3% of portfolio |
| CVaR(95%) | Expected shortfall beyond VaR | — |
| Max Drawdown from Peak | Current / Peak − 1 | 5-10%=Yellow, 10-15%=Orange, 15-20%=Red, >20%=EMERGENCY |
| Sharpe (trailing 90d) | (Return − Rf) / σ | <0 = "underperforms cash" |
| N_effective | (Σλᵢ)² / (Σλᵢ²) | <3 for 10+ positions = "diversification failure" |

### Automated Risk Responses
| Trigger | Response |
|---------|----------|
| VaR >4% of portfolio | Alert. Reduce all sizes 25%. |
| Two consecutive -2% days | Halt new positions. Review signals. |
| N_effective <3 | Reduce leverage 50%. Sell highest-correlated pair. |
| Single position P&L >-15% | Auto-close. Post-mortem required. |
| Margin used >80% | Reduce to <60%. Sell weakest. |
| Broker disconnect >2 min | Cancel all open orders. No new orders. |

### Stress Test Scenarios
2008-style (SPY -38%, corr→1.0, VIX→80), 2020-COVID (SPY -34%, VIX→82), 2022-rate-hike (SPY -19%, Growth -30%), Tech-crash (QQQ -33%), Liquidity-crisis (spreads 5×), Flash-crash (SPY -9% in 30 min). Any scenario >40% drawdown → REDUCE LEVERAGE IMMEDIATELY.

## Phase 4: Correlation-Aware Portfolio Construction

### Pre-Allocation Checks
- Pairwise correlation >0.80 → flag. >0.95 with same index/ETF → REJECT
- Sector exposure >25% after adding → reduce other sector positions or reject candidate

### Diversification: N_effective = (Σλᵢ)² / (Σλᵢ²) via PCA on returns covariance. <5 with 10+ positions = undiversified.

### ETF/Stock Mix
- Min 20% broad-market ETFs (SPY, VTI, BND), max 40% single stocks, max 10% leveraged ETFs, max 5% any single leveraged ETF

### Rebalance Triggers
- Calendar: quarterly (Jan/Apr/Jul/Oct 1st), Drift: >20% from target, Signal: new conflict with existing, Regime: VIX crosses 20→30
- Execution: calculate targets → sells first → buys after → limit orders at mid
- Tax-aware: prefer loss lots, prefer >1yr held, defer if >80% short-term gains

## Phase 5: Signal-to-Execution Pipeline

### Bidirectional Communication Protocol
**PUSH received:**
- technical-signals-engineer: regimeChanged → recalculate all weights, adjust ATR multiples
- fundamental-analyst: redFlagDetected → IMMEDIATE close, suppress all new signals
- market-data-engineer: corporateAction → adjust sizing, flag tax; dataQualityDegraded → HALT new orders
- algorithmic-trader: executionAlert → update slippage model

**PULL requests sent:**
- → technical-signals-engineer: reScoreRequest (when signal stale >20d, regime changed, parameter change)
- → fundamental-analyst: valuationUpdateRequest (when price moves >10% from base, earnings released)
- → market-data-engineer: dataRefreshRequest (when prices >60s stale)

### Circuit Breakers
| Failure | Threshold | Action |
|---------|-----------|--------|
| Rejected orders in 60s | >5 | HALT. Investigate. |
| Consecutive stop-loss triggers | >3 in session | HALT. Regime check. |
| P&L swing (unrealized) | >$5K in <5 min | PAUSE. Check news. |
| Broker margin call | Any | IMMEDIATE reduction. Sell weakest 50%. |
| API error rate | >10% | HALT. Connection check. |
| Price gap (>3 ATR) | Any | Close at market. |

### Completion Checklist
[VERIFIED] Broker READY, all conflicts resolved, no position >10%, no sector >25%, N_effective >3, stop-losses set, idempotency keys generated, circuit breakers armed, stress tests run.

