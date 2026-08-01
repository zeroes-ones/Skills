# Broker Comparison for Intraday Options

> **Portability target:** Spec-level. Broker lists evolve — verify current terms before committing capital. This reference describes architectural differences that persist across pricing changes.

## The Intraday Broker Decision Matrix

Your broker IS your execution. In intraday options, the broker determines:
- Whether you get filled at 1% off mid or 8% off mid (a $25K/year difference)
- Whether your order hits the exchange in 30ms or 300ms (billion-dollar HFT firms exploit this gap)
- Whether your stop order fires when you need it or gets skipped

## Architecture Matters More Than Commissions

| Architecture | Latency | Quality | Free brokers are NOT free |
|-------------|---------|---------|---------------------------|
| DMA (Direct Market Access) | < 50ms | Exchange-native | Commission: $0.15-0.65/contract. Value: $25K/year in fill quality |
| Smart Router | 50-200ms | Multi-exchange optimization | Commission: $0.50-0.65/contract. Best price/quality ratio |
| PFOF (Payment for Order Flow) | 100-500ms | Internalized, no price improvement | "Free" but costs $0.50-2.00/contract in worse fills |

## Broker Profiles

### Interactive Brokers (IBKR Pro)

**Architecture:** DMA + Smart Router hybrid
**Latency:** < 50ms DMA, 50-150ms Smart
**Options commissions:** $0.15-0.65/contract
**Best for:** Gamma scalping, momentum, ORB, professional intraday
**Platform:** TWS (steep learning curve), IBKR Mobile, Client Portal API
**Key strength:** Exchange-native routing — order goes directly to the exchange. No internalization.
**Key weakness:** TWS UI is archaic. Mobile app is functional but not intuitive.
**Minimum for intraday:** $2,000 minimum deposit, but $25,000+ recommended (PDT rule).
**API:** REST + WebSocket. Most mature options API in retail. Supports complex multi-leg orders.

### tastytrade (tastyworks)

**Architecture:** Smart Router
**Latency:** 100-200ms
**Options commissions:** $1.00/contract to open, $0 to close (capped at $10/leg)
**Best for:** Swing options, multi-leg spreads, theta strategies
**Platform:** Desktop + web + mobile. Clean UI, built for options traders.
**Key strength:** Designed for options. Multi-leg order entry is intuitive. Good for swing/multi-day.
**Key weakness:** Latency too high for gamma scalping. Not DMA. Fill quality varies.
**Minimum:** $2,000 to open, no minimum for margin (options trading on cash accounts).
**API:** No public API. Not suitable for automation.

### Charles Schwab (thinkorswim, formerly TDA)

**Architecture:** Smart Router (formerly TDA's router)
**Latency:** 100-250ms
**Options commissions:** $0.65/contract
**Best for:** Swing, position, multi-timeframe. Excellent for analysis and research.
**Platform:** thinkorswim desktop (powerful), web, mobile. Best charting in retail.
**Key strength:** thinkorswim platform. Best analysis tools, scripting (thinkScript), paper trading.
**Key weakness:** Post-merger integration friction. Latency too high for scalping. No public API easily accessible.
**Minimum:** $0 minimum.
**API:** TDA API is being deprecated/migrated. Uncertain future. Not recommended for new automation builds.

### Tradier

**Architecture:** API-first brokerage
**Latency:** 100-300ms
**Options commissions:** $0.35/contract (flat), $10/month subscription options
**Best for:** Automation-first traders, developers, algo options
**Platform:** API only (no first-party trading platform — use 3rd party or build)
**Key strength:** Clean REST + WebSocket API. Built for developers. Predictable pricing.
**Key weakness:** Smaller broker = less liquidity access. Fill quality varies. Not for high-frequency.
**Minimum:** $0 minimum.
**API:** REST + WebSocket. Best developer experience. Sandbox environment available.

## Commission Math — Don't Be Fooled

"Free" brokers save $0.65/contract in commissions but cost $1-5/contract in worse fills.

| Trade Type | Contracts/Month | Commission Cost @ $0.65 | Fill Cost @ 3% Slippage | Total PFOF Loss |
|-----------|----------------|----------------------|----------------------|----------------|
| Light (5/day) | 100 | $65 | $150-500 | $215-565/month |
| Moderate (10/day) | 200 | $130 | $300-1,000 | $430-1,130/month |
| Active (20/day) | 400 | $260 | $600-2,000 | $860-2,260/month |
| Heavy (50/day) | 1,000 | $650 | $1,500-5,000 | $2,150-5,650/month |

**Bottom line:** The cheapest broker costs the most money. Use DMA or smart routing. Free = expensive.

## Quick Decision Tree

```
What's your primary trading style?
├── Gamma scalping, ORB, momentum → IBKR Pro (DMA required)
├── Swing trading, spreads, theta → tastyworks or IBKR (Smart Router OK)
├── Automation, algo trading → Tradier (API-first) or IBKR (mature API)
├── Learning, paper trading → thinkorswim paper account (free, best tools)
└── Free/zero-commission (PFOF) → DO NOT USE for intraday options. The fills cost more than commissions save.
```
