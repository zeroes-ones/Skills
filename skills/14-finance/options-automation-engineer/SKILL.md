---
name: options-automation-engineer
description: >
  Use when the user wants to build automated options trading systems, design
  scanner-to-execution pipelines, implement auto-roll logic for decaying positions,
  construct multi-leg order routing with legging risk protection, or deploy circuit
  breakers for gamma risk, IV spikes, and early assignment. Use when the user asks
  "automate my options strategy," "build options trading bot," "auto-roll credit
  spreads," or "multi-leg execution." Handles full pipeline (scan→filter→strategy→
  size→execute→monitor→journal), broker API patterns (IBKR, tastytrade, Tradier),
  complex order routing, auto-roll logic, OCO/bracket orders, 4-level circuit breaker
  hierarchy, and safety ramp-up (paper→small→live). Do NOT use for strategy design or
  backtesting (route to options-strategist, swing-options-trader, or intraday-options-
  trader first), general-purpose algorithmic trading (route to algorithmic-trader),
  DevOps infrastructure (route to devops-engineer), or portfolio management (route to
  portfolio-signal-manager).
license: MIT
tags:
  - automation
  - options
  - multi-leg-execution
  - auto-roll
  - scanner
  - broker-api
  - circuit-breakers
  - algorithmic-trading
chain:
  consumes_from: [algorithmic-trader, options-strategist, options-risk-engineer, intraday-options-trader, swing-options-trader, advanced-options-structures]
  feeds_into: [trade-performance-analyst, portfolio-signal-manager, devops-engineer, algorithmic-trader]
version: 1.0.0
status: active
author: Skills Library
created: "2026-07-16"
category: "14-finance"
token_budget: 4000
---

# Options Automation Engineer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).
> No vendor-specific frontmatter fields.

<!-- STANDARD: 3min -->
## Route the Request

| User Intent | Route To | Decision Gate |
|-------------|----------|---------------|
| "Automate options trading" / "build options trading bot" | → Full Pipeline (§3-4, ref: scanner-to-execution-pipeline.md) | Start with strategy validated in paper trading |
| "Multi-leg order execution" / "spread order routing" | → Execution (§5, ref: multi-leg-execution.md) | MUST use native complex orders |
| "Auto-roll options" / "automate rolling spreads" | → Auto-Roll (§6, ref: auto-roll-and-adjustment-logic.md) | Max 2 rolls per position |
| "OCO for options" / "bracket orders options" | → Conditional Orders (§7, ref: conditional-orders-for-options.md) | Use underlying-based triggers for spreads |
| "Options broker API" / "connect broker for options" | → Broker APIs (§8, ref: broker-api-options-specs.md) | IBKR for advanced, tastytrade for UX, Tradier for simple |
| "Circuit breakers" / "safety for options bot" | → Safety (§9, ref: circuit-breakers-and-safety.md) | 4-level breaker hierarchy |

## 10 Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to automate multi-leg options without native complex/spread orders. Legging into spreads programmatically guarantees execution risk — a single-leg fill without its hedge during a vol spike = catastrophic unhedged position | Trigger: `grep "leg" order_routing_code` → `order_type ≠ "spread"` AND `leg_count ≥ 2` | STOP. "Multi-leg automation without native spread orders. Hard-code: all multi-leg entries MUST use broker-native complex orders (e.g., IBKR `what-if` combo). Never leg in programmatically." |
| R2 | REFUSE to auto-roll credit spreads more than 2 times per position. Positions rolled 3+ times underperform by -40% cumulative P&L vs closing cleanly | Trigger: `roll_count ≥ 3 OR (roll_count ≥ 2 AND last_roll_credit < 0.05)` in roll_tracker | STOP. "Auto-roll limit exceeded: max 2 rolls per position. Positions rolled 3+ times lose 40% cumulative P&L vs clean exit. Roll credit < $0.05 = DO NOT ROLL. Close position." |
| R3 | REFUSE to go live without 4-level circuit breaker hierarchy. Position → Strategy → Account → Market. Any missing layer = time bomb | Trigger: `grep -c "circuit_breaker_level" system_config` < 4 | STOP. "Missing circuit breaker layer. Implement all 4 levels before going live: position-level (max loss/contract), strategy-level (daily P&L cap), account-level (% drawdown), market-level (VIX/regime)." |
| R4 | REFUSE to allow CRITICAL circuit breaker override. The moment you override a circuit breaker, automation converts from safety tool to risk amplifier | Trigger: `grep "override.*critical.*breaker" system_code` → any match | STOP. "CRITICAL circuit breaker override attempted. No override, no exception. If a CRITICAL breaker fires, the system enters EMERGENCY_STOP until manual review. This is the safety failsafe." |
| R5 | REFUSE to ignore position correlation in automated entry sizing. Automated systems compound correlation risk faster than manual trading due to higher trade frequency | Trigger: `new_position_correlation > 0 AND position_size = “full”` in automated trade signal | STOP. "Correlation-unadjusted position size. Reduce new position size by (1 − avg_correlation). Automation amplifies correlation risk — 50 trades/day vs 5 magnifies the compounding effect." |
| R6 | REFUSE to ignore VIX-level position scaling. Vol spikes are the most common killer of options automation systems | Trigger: `VIX > 30 AND position_sizes ≠ "halved" OR VIX > 40 AND short_vol_positions > 0 OR VIX > 50 AND total_positions > 0` | STOP. "VIX-level position scaling violated. Enforce: VIX > 30 → halve all sizes. VIX > 40 → close all short-vol. VIX > 50 → close everything. Hard-code — this is a non-optional circuit breaker." |
| R7 | REFUSE PMCC automation without hard-coded short-strike-above-LEAPS check. Violating this guarantees loss if assigned — never rely on human review | Trigger: `grep "PMCC" strategy_code` → `short_strike ≤ LEAPS_strike` | STOP. "PMCC short strike ≤ LEAPS strike. Hard-code: `assert(short_strike > LEAPS_strike, 'PMCC_SHORT_BELOW_LONG_ERROR')`. This is a compile-time check, not runtime." |
| R8 | REFUSE directional entries within 5 days of earnings. Binary event risk cannot be managed by position sizing — hard-code earnings blackout | Trigger: `abs(entry_date - earnings_date) ≤ 5 AND position_type = “directional”` in trade signal | STOP. "Earnings within 5 days on directional position. Hard-code blackout: `if (next_earnings - today) < 6: skip_directional_entries()`. Binary event risk is unmanageable at any size." |
| R9 | REFUSE to scan technical patterns before liquidity filter. Never scan 1000 tickers on technicals when 800 fail the liquidity check | Trigger: `scanner_pipeline[0] ≠ “liquidity_filter”` in scanner_config | STOP. "Scanner pipeline not liquidity-first. Order: (1) liquidity (OI/volume/spread), (2) earnings blackout, (3) technical patterns. Liquidity is the cheapest check — filter early, save compute." |
| R10 | REFUSE to deploy real-money automation without paper → small-size ramp-up. Production bugs cost real money — the ramp-up catches edge cases paper trading misses | Trigger: `deploy_mode = “live” AND (paper_trading_days < 10 OR small_size_days < 10)` | STOP. "Deployment ramp-up incomplete. Require: 2 weeks paper trading (catches logic bugs), then 2 weeks at 25% size (catches slippage/partial fills/API failures). Then full scale." |

## Decision Tree

```
Build options automation system
│
├─ Strategy Design (UPSTREAM — route to strategy skills first)
│  ├─ Do strategies exist and are they profitable in manual/paper trading?
│  │  ├─ NO → Route to options-strategist/swing-options-trader/intraday-options-trader
│  │  └─ YES → Proceed to automation design
│  │
├─ Architecture Design
│  ├─ What broker? → IBKR (advanced), tastytrade (UX), Tradier (simple) (§8)
│  ├─ What order types? → Native complex orders for spreads. (§5)
│  ├─ What runtime? → Event-driven (WebSocket) vs scheduled (cron) vs hybrid. (§4.2)
│  ├─ What database? → PostgreSQL for trades, Redis for market data cache. (§4.3)
│  └─ Where hosted? → Cloud VM (24/7) vs home server vs broker's cloud. (§4.4)
│
├─ Pipeline Construction (§4-5)
│  ├─ Scanner → Filter Chain → Strategy Selector → Sizing Engine → Order Builder → Execution → Monitor → Journal
│  ├─ Each layer independently testable
│  └─ Each layer has its own error handling and logging
│
├─ Safety Systems (MANDATORY — before going live) (§9)
│  ├─ Level 1: Position breakers (max loss, max holding days, gamma zone)
│  ├─ Level 2: Strategy breakers (consecutive losses, daily cap, max open positions)
│  ├─ Level 3: Account breakers (daily/weekly/monthly loss caps, drawdown cascade: -10%/-20%/-30%)
│  └─ Level 4: Market breakers (VIX levels, SPY vs 200SMA, market-wide halts)
│
├─ Testing & Deployment (§10)
│  ├─ Paper trade: 2 weeks minimum
│  ├─ Small size live: 2 weeks at 25% target size
│  ├─ Ramp to full size: Increase 25% per week if no breakers triggered
│  └─ Monitoring: Execution quality, breaker events, P&L drift
│
└─ Operations (§10.5)
   ├─ Daily health check: System alive? Orders routing? Data fresh?
   ├─ Weekly review: Breaker events, execution quality, P&L attribution
   └─ Monthly audit: Strategy profitability, correlation drift, system upgrades
```

## Core Workflow

### Phase 1: Strategy Validation (1-4 weeks)

Before writing a single line of automation code, the strategy must be:
1. Profitable in manual testing (30+ trades minimum)
2. Documented with precise entry/exit rules
3. Understood for failure modes (when does it lose? how badly?)

### Phase 2: Paper Trading Architecture (2 weeks)

1. Broker sandbox/paper account connected
2. Scanner pipeline running (no execution)
3. Signals logged for review
4. No real money. No paper money simulated by the broker's real market — use their sandbox.

### Phase 3: Safety Layer Implementation (before any execution)

1. All 4 levels of circuit breakers implemented
2. Breaker events logged to separate audit log
3. Manual override mechanism (with multi-step confirmation)
4. Tested with simulated breaker scenarios

### Phase 4: Graduated Live Deployment (4-6 weeks)

**Week 1-2:** Paper trading. Review every signal. Fix bugs.
**Week 3-4:** 25% of target position size. Live money. Monitor continuously.
**Week 5-6:** 50% size if no breakers triggered in weeks 3-4.
**Week 7-8:** 75% size if no breakers triggered in weeks 5-6.
**Week 9+:** Full target size. Ongoing monitoring.

### Phase 5: Ongoing Operations

1. Daily automated health check report
2. Weekly execution quality review
3. Monthly strategy profitability audit
4. Quarterly system architecture review

## Architecture Deep Dives

### 1. Scanner-to-Execution Pipeline

> **Reference:** scanner-to-execution-pipeline.md

8-layer architecture: Scanner → Filter Chain → Strategy Selector → Sizing Engine → Order Builder → Execution → Monitor → Journal. Each layer independently testable. Computational efficiency through filter ordering (liquidity first, technicals last).

### 2. Multi-Leg Execution

> **Reference:** multi-leg-execution.md

Complex Order Book (COB) routing. Legging risk quantification. Broker-specific routing decisions. Fill quality metrics. Execution timing by time of day and market conditions.

### 3. Auto-Roll & Adjustment Logic

> **Reference:** auto-roll-and-adjustment-logic.md

Credit spread roll matrix by DTE/OTM/ITM state. PMCC roll logic with non-negotiable strike constraint. State machine for the full trade lifecycle. Automated roll rules with credit thresholds.

### 4. Conditional Orders

> **Reference:** conditional-orders-for-options.md

OCO construction with underlying-based triggers. Bracket orders (OTO → OCO). Trailing stops with gamma adjustment. Volatility-based conditions. Broker support matrix.

### 5. Broker API Specifications

> **Reference:** broker-api-options-specs.md

IBKR (ib_insync), tastytrade, Tradier, TDA/Schwab, Alpaca comparison. Code examples for complex orders, auto-roll, and conditional orders on each platform. Execution quality monitoring.

### 6. Circuit Breakers & Safety

> **Reference:** circuit-breakers-and-safety.md

4-level breaker hierarchy with implementation code. Account drawdown cascade: -10% review → -20% reduce → -30% liquidate. Market-level: VIX thresholds + SPY trend. Audit trail requirements. Recovery protocol.

## Research Prerequisites

**RP1 (STRATEGY VALIDATION):** Has the strategy been profitable in manual trading? Minimum 30 trades with documented results.

**RP2 (BROKER SELECTION):** Which broker supports the needed complex order types? Verify API documentation for native complex orders.

**RP3 (DATA REQUIREMENTS):** Real-time quotes? Historical options data? Greeks? Identify data sources and costs.

**RP4 (PAPER TRADING ENVIRONMENT):** Set up broker sandbox. Verify all order types work in sandbox before live.

**RP5 (HOSTING):** Where will the automation run? Cloud VM (AWS, GCP, Azure)? Home server? Broker's cloud?

**RP6 (MONITORING):** How will you monitor the system? Alerts for breaker events? Daily P&L reports? System health checks?

**RP7 (FAILURE MODES):** What happens when (not if) the system fails? API disconnect? Stale data? Partial fill? Exchange halt?

**RP8 (RECOVERY PROCEDURES):** Documented procedures for every failure mode. How to safely restart after a breaker event?

## Error Decoder

| # | Symptom | Root Cause | Exact Fix | Lesson |
|---|---------|-----------|-----------|--------|
| E1 | "Spread order rejected: complex order not supported" | Broker doesn't support native complex orders for this spread type | Switch to broker that supports it. Do NOT simulate by legging single orders sequentially | If the broker can't handle your order type natively, switch brokers — don't hack around it |
| E2 | "Auto-roll executed at a loss — rolled ITM credit spread hoping for recovery" | Roll logic didn't have the ITM gate. Hoping, not trading | Add GR-R3: IF ITM credit spread AND roll credit < $0.05 → DO NOT ROLL. Close or take assignment | Rolling ITM spreads is loss-avoidance behavior, not a strategy. Code must enforce this |
| E3 | "System kept trading through 8 consecutive losses — account down 45%" | Circuit breakers not implemented. Consecutive loss check missing | Add Level 2 strategy breaker: 5 consecutive losses → pause 24 hours. Add Level 3 account breaker: -20% drawdown → close 50% | Circuit breakers are not optional. Ship with them or don't ship at all |
| E4 | "Position closed at 3× expected loss because stop limit was gapped through" | Stop limit on spread during VIX spike. Gap exceeded the limit price | Use stop market for liquid underlyings. Wider limit buffer (10%+) during VIX > 25. Or underlying-based stops for spreads | Option-price-based stops fail when you most need them — during vol events |
| E5 | "Scanner found 50 setups but only 3 had liquid options — wasted 47 API calls" | Liquidity filter applied last in the filter chain | Apply liquidity filter FIRST. Eliminate before technical analysis. Save API costs and compute | Filter chain ordering matters for cost and speed. Cheapest checks first |
| E6 | "Bot placed 20 trades in 30 seconds because the scanner ran on stale data" | Scanner ran before market data update completed. Stale signals triggered multiple entries | Add data freshness check before scanner runs. Add rate limiter: max 1 entry per minute. Add duplicate detection | Stale data is the most common silent killer of trading bots |
| E7 | "Broker API disconnected at 2:30 PM. System didn't detect it. Positions were unmanaged through close" | No heartbeat monitoring. No fallback detection | Add WebSocket heartbeat (every 5s). If no heartbeat for 30s → alert. If 60s → attempt reconnect. If 120s → emergency shutdown procedure | API disconnections happen. Your system must detect them and respond. Silence ≠ safety |

## Anti-Hallucination

**[VERIFIED]** — Exchange rules (CBOE, ISE), broker API documentation, SEC/FINRA regulations.
**[COMPUTED]** — Sizing calculations, Kelly formulas, execution cost estimates with stated assumptions.
**[ESTIMATED]** — Practitioner guidelines for slippage, fill times, partial fill rates. Varies by broker and market conditions.
**[COMMON-PRACTICE]** — Industry-standard automation patterns. Not codified in documentation.
**[BACKTEST-EVIDENCE]** — Trading project empirical data for scoring, drawdown, and roll performance.

**Broker API specifications change.** Always verify against the latest broker API documentation before implementing. The code examples in this skill are patterns, not production-ready code — adapt to your broker's current API.

## Cross-Skill Coordination

### Upstream

| Skill | What to Request | Decision Gate |
|-------|----------------|---------------|
| `options-strategist` | Strategy definitions, Greeks requirements, structure specifications | Is the strategy well-defined enough to automate? |
| `swing-options-trader` | Swing-specific entry/exit rules, time stop logic, earnings calendar integration | Does the swing strategy have precise, automatable rules? |
| `intraday-options-trader` | Intraday entry/exit windows, gamma scalping parameters, execution timing | Are intraday rules fast enough for automation? |
| `options-risk-engineer` | Position sizing formulas, correlation matrices, drawdown limits | Is the risk framework comprehensive? |
| `algorithmic-trader` | General algo trading patterns, backtesting framework, execution infrastructure | Can we reuse existing algo infrastructure? |

### Downstream

| Skill | When to Hand Off | Handoff Format |
|-------|-----------------|----------------|
| `trade-performance-analyst` | Automation running, trades accumulating | "Automation performance: [strategy], [period], [trades], [win_rate], [avg_pnl], [sharpe], [max_dd], [breakers_triggered]" |
| `portfolio-signal-manager` | Automated signals need portfolio-level coordination | "Automated signal: [timestamp], [ticker], [strategy], [direction], [size], [confidence]" |
| `devops-engineer` | System needs deployment, monitoring, alerting | "DevOps requirements: [runtime], [uptime_SLA], [monitoring], [alert_channels], [disaster_recovery]" |

## What Good Looks Like

**Fully Automated Credit Spread System (GOOD):** Pipeline: nightly scanner → morning liquidity check → pre-market correlation check → 9:35 AM execution window. Native complex orders on IBKR. Auto-close at 50% profit or 2× stop. Hard breaker at -15% account drawdown. Daily health report to email. Weekly P&L summary. Result: 3 months live, 120 trades, 62% win rate, Sharpe 1.4, 0 breaker triggers, max drawdown -8%.

**Basic Automation (MINIMUM VIABLE):** Scanner runs on schedule. Signals sent to human for review. Human clicks approve. System executes native spread order. Human manages exits. Result: Reduced execution errors. Still human-dependent but execution is automated and safe.

**Over-Engineered Disaster (BAD):** Scanner → filter → strategy → sizing → execution → monitoring all automated. No circuit breakers. Single broker, single API key. No heartbeat. No audit log. Result: System ran for 2 weeks, then API disconnected during FOMC. Positions were not managed. Losses unknown for 4 hours. Account down 35%.

## Operating at Different Levels

| Level | Scope | Key Capability |
|-------|-------|----------------|
| **L1: Apprentice** | Automate one strategy on one ticker with manual monitoring. Basic spread execution | Knows: Native complex orders, single-strategy pipeline, 1 broker API |
| **L2: Practitioner** | Multi-strategy automation with auto-roll. Position-level circuit breakers. Execution quality monitoring | Adds: Scanner pipeline, auto-roll logic, position breakers, 2+ brokers |
| **L3: Specialist** | Full pipeline with all 4 breaker levels. Multi-broker failover. Real-time monitoring dashboard | Adds: Account/market breakers, broker failover, monitoring stack |
| **L4: Architect** | Cross-asset automation (equities + options + futures). Dynamic sizing based on portfolio state. ML-enhanced entry timing | Adds: Cross-asset, dynamic sizing, ML optimization, institutional infrastructure |
| **L5: Transformative** | Design options automation frameworks used by others. Publish research on execution optimization. Create open-source automation tools | Adds: Framework design, research, open-source contributions |

## Anti-Patterns

| ❌ Common Mistake | ✅ Correct Approach |
|-------------------|-------------------|
| "I'll build the trading logic first, add safety systems later" | Safety systems ship BEFORE the trading logic. You can't retrofit circuit breakers onto a system that's already blown up |
| "I'll simulate spread orders by legging into them sequentially — the broker handles it fine manually" | Native complex orders only. Legging risk with automation = unbounded adverse selection. If the broker doesn't support native spreads, switch brokers |
| "My strategy has a 65% win rate — I'll use full Kelly sizing" | [BACKTEST-EVIDENCE] Half-Kelly reduces drawdown ~50% vs full Kelly with modest return reduction. Maximum 5% per trade regardless of Kelly output |
| "The bot has been running perfectly for 2 months — I can reduce monitoring" | Automation failures are rare but catastrophic. Monitoring doesn't scale down because nothing has happened yet. The one day you stop watching is the day it fails |
| "I'll override this circuit breaker just this once — the setup is too good to miss" | Every blown-up account started with "just this once." Circuit breakers are non-negotiable. If you override one, remove it from the system — don't pretend it exists |
| "I tested in paper trading for a week — ready for full-size live" | Minimum 2 weeks paper + 2 weeks at 25% size. Paper trading doesn't replicate real slippage, partial fills, or psychological pressure of real losses |

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Auto-roll logic executes on an ITM credit spread without the ITM gate, converting a defined-risk strategy into indefinite loss-avoidance rolling | $2K-$10K per position — ITM spreads rolled 3+ times underperform clean exits by 40% cumulative P&L | Hard-code GR-R3: IF ITM credit spread AND roll credit < $0.05 → DO NOT ROLL. Close position. The automaton must never roll a loser hoping it turns around |
| Circuit breakers are built but not wired to halt execution — the system logs the breach but keeps trading because "the alert system is a separate module" | $10K-$50K in a single vol event — a system that detects a problem but doesn't stop is more dangerous than one that doesn't detect it at all | Wire every breaker directly to the execution engine at compile time. A CRITICAL breaker that fires must call `system.halt()` — not log, not alert, not wait for confirmation. Hard stop |
| Scanner pipeline filters technical patterns before liquidity, scanning 1,000 tickers on CPU-intensive indicators when 800 fail the minimum OI check | $500-$2K/month in wasted cloud compute for medium-scale deployments, plus 10-30s latency increase | Liquidity filter FIRST in the pipeline: OI > 100 AND spread < 5%. This eliminates 60-80% of the universe with a single cheap API call before any technical computation |
| Production deployment skips paper trading — "the logic is simple, it should work, and paper trading doesn't replicate real conditions anyway" | $5K-$50K in production bugs: partial fills at 2x expected cost, slippage 3-5x model assumptions, API edge cases that only surface in live markets | Minimum 2 weeks paper + 2 weeks at 25% size. Paper catches logic bugs. Small live size catches slippage, partial fills, API edge cases. The ramp-up is non-negotiable |
| Stale market data feeds into the scanner — a 90-second delay spike goes undetected, signals trigger on prices that are $2+ stale | $5K-$20K per incident — orders fill at actual market prices that are completely different from the signal price, producing random entries | Implement data freshness heartbeat: `if (data.timestamp - now()) > 30 seconds: SKIP scan cycle, log alert`. Never act on stale data |
| Relying on option-price-based stop orders for multi-leg positions — a VIX spike gaps the spread price 300% past the stop limit, order never fills | $8K-$30K per incident — the stop you trusted doesn't exist exactly when you need it most | Use underlying-based stops for spread positions. Or implement a wider limit buffer (10%+) that activates when VIX > 25. Option-price stops fail during vol events — it's when, not if |
| Single broker, single API key, single data feed — broker API disconnects at 2:00 PM, positions unmanaged through 3:30 PM gamma window | $10K-$50K per incident — positions left unmanaged during the most dangerous time of day with no detection and no fallback | Multi-broker failover or at minimum: WebSocket heartbeat every 5s, alert at 30s silence, emergency reconnect at 60s, emergency shutdown at 120s. Silence ≠ safety |

## Production Checklist

Before ANY automated options system goes live:

- [ ] 1. **Strategy validated manually:** 30+ trades with documented profitability.
- [ ] 2. **Paper trading completed:** Minimum 2 weeks. All signals reviewed.
- [ ] 3. **Native complex orders:** All multi-leg orders use exchange-native spread orders.
- [ ] 4. **Liquidity filters first:** Scanner eliminates illiquid options before any other check.
- [ ] 5. **Earnings blackout hard-coded:** No directional entries within 5 days of earnings.
- [ ] 6. **Level 1 breakers active:** Position max loss, max holding days, gamma zone.
- [ ] 7. **Level 2 breakers active:** Strategy consecutive losses, daily cap, max open positions.
- [ ] 8. **Level 3 breakers active:** Account daily/weekly/monthly loss caps, drawdown cascade (-10%/-20%/-30%).
- [ ] 9. **Level 4 breakers active:** VIX thresholds, SPY trend, market-wide halts.
- [ ] 10. **Heartbeat monitoring:** WebSocket/API health check every 5 seconds. Alert on 30s silence.
- [ ] 11. **Audit log:** Every order, breaker event, and system state change logged.
- [ ] 12. **Recovery procedures documented:** What to do for every breaker event and system failure.
- [ ] 13. **Graduated deployment:** 25% size → 50% → 75% → 100%, 2 weeks at each level.
- [ ] 14. **Daily health report automated:** System status, P&L, open positions, breaker history.
- [ ] 15. **Manual override exists but requires multi-step confirmation:** No single-click overrides.

## References

| Reference | Covers | When to Read |
|-----------|--------|-------------|
| `multi-leg-execution.md` | Complex Order Book, legging risk, broker routing, order types, fill quality, execution timing | Before implementing order execution |
| `auto-roll-and-adjustment-logic.md` | Roll decision matrix, state machine, adjustment patterns, PMCC roll logic, roll tracking | Before implementing roll automation |
| `conditional-orders-for-options.md` | OCO, bracket, trailing stops, underlying-based triggers, broker support matrix | Before implementing exit automation |
| `scanner-to-execution-pipeline.md` | 8-layer pipeline architecture, scanner types, filter chain, strategy selector, sizing engine | Before building the scanner |
| `broker-api-options-specs.md` | IBKR, tastytrade, Tradier, TDA, Alpaca comparison. Code examples. Execution quality | During broker selection and API integration |
| `circuit-breakers-and-safety.md` | 4-level breaker hierarchy, implementation code, action matrix, audit trail, recovery protocol | BEFORE any live trading. Read first, implement second |
| `state-machine-implementation.md` | Full trade lifecycle state machine, transition validation, roll limits, crash recovery, audit trail | When implementing the trade management engine |
| `monitoring-and-observability.md` | SLIs, dashboard design, alert rules, logging levels, healthcheck endpoint, overnight checklist | Before deploying to production — monitoring is non-negotiable |

**Cross-reference skills:** `algorithmic-trader` (general algo patterns), `options-strategist` (strategy design), `options-risk-engineer` (risk frameworks), `swing-options-trader` (swing strategy rules), `intraday-options-trader` (intraday execution timing).

---

*Skill complete. Route strategy design upstream. Route trade analysis downstream. Safety systems are non-negotiable — ship with them or don't ship at all.*
