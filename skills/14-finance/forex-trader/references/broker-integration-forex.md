# Broker Integration — Forex

## Broker Comparison: Leverage & Margin

| Broker | Max Leverage (Major) | Max Leverage (Minor) | Max Leverage (Exotic) | Margin During News | Negative Balance Protection |
|--------|---------------------|---------------------|----------------------|-------------------|---------------------------|
| OANDA | 50:1 (US: 50:1) | 20:1 | 10:1 | May increase | Yes |
| IG | 30:1 (retail), 50:1 (pro) | 20:1 | 10:1 | Notified 24h prior | Yes (retail only) |
| FXCM | 50:1 (US: 50:1) | 20:1 | 10:1 | No advance notice | Yes |
| IBKR | 50:1 (US) / 30:1 (EU) | 20:1 | 10:1 | Risk-based, real-time | No — can go negative |
| Saxo | 30:1 (retail) | 20:1 | 10:1 | May increase | Yes (retail) |
| Pepperstone | 30:1 (retail), 500:1 (pro) | 20:1 / 100:1 | 10:1 / 50:1 | Notified 48h prior | Yes (retail) |

## Order Types by Broker

| Order Type | OANDA | IG | FXCM | IBKR | Saxo | Pepperstone |
|-----------|-------|----|------|------|------|-------------|
| Market | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Limit | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stop Entry | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stop Loss (standard) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Guaranteed Stop | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ |
| Trailing Stop | ✓ | ✓ | ✓ | ✓ (bracket) | ✓ | ✓ |
| OCO (One-Cancels-Other) | ✓ | ✓ | ✗ | ✓ (bracket) | ✓ | ✓ |
| If-Then | ✗ | ✓ | ✗ | ✓ (conditional) | ✓ | ✗ |

## API Access Details

### OANDA v20 REST API
- Endpoint: `https://api-fxtrade.oanda.com/v3/`
- Auth: Bearer token (personal access token)
- Rate limits: 120 requests/second for pricing, 60/second for orders
- Practice account: `https://api-fxpractice.oanda.com/v3/`
- Key endpoints:
  - `GET /accounts/{accountID}/pricing?instruments=EUR_USD,GBP_USD` — Real-time quotes
  - `POST /accounts/{accountID}/orders` — Place order
  - `GET /accounts/{accountID}/positions` — Open positions
  - `GET /accounts/{accountID}/transactions` — Trade history

### IBKR TWS API
- Protocol: TCP socket (port 7496 for TWS, 7497 for Gateway)
- Requires TWS or IB Gateway running
- Contract definition: `Contract.symbol("EUR"), Contract.secType("CASH"), Contract.currency("USD"), Contract.exchange("IDEALPRO")`
- Order types: LMT, MKT, STP, STPLMT, TRAIL, TRAILLIMIT
- Key: IDEALPRO is the FX exchange. IDEAL is for small amounts (settled differently)

### IG REST API
- Endpoint: `https://api.ig.com/gateway/deal/`
- Auth: API key + session token (2-step: login → CST + X-SECURITY-TOKEN)
- Headers: `CST: {token}`, `X-SECURITY-TOKEN: {token}`, `Version: 2`
- Rate limits: 60 requests/minute for order operations, 120/minute for pricing
- Demo endpoint: `https://demo-api.ig.com/gateway/deal/`

## Spread & Commission Structures

| Broker | EUR/USD Typical Spread | Commission Model | Hidden Costs |
|--------|----------------------|------------------|--------------|
| OANDA | 0.8-1.2 pips (standard), 0.1-0.3 (core + $35/mil) | Spread-only or spread + commission | Core pricing requires $10K+ or $35/mil round-turn commission |
| IG | 0.6-0.9 pips (standard), 0.1-0.3 (DMA + $40/mil) | Spread-only or DMA commission | DMA requires professional status or $500K+ |
| FXCM | 0.2-0.4 pips (active trader), 1.0-1.5 (standard) | Spread-only | Active trader requires $25K+ and minimum volume |
| IBKR | 0.1-0.2 pips + $20/mil commission | Commission (transparent) | Best pricing for size. Minimum $10K for margin account |
| Saxo | 0.4-0.6 pips (VIP), 0.8-1.2 (classic) | Spread-only | VIP requires $200K+. Classic accounts pay wider spreads |
| Pepperstone | 0.0-0.3 pips (razor + $35/mil), 1.0-1.5 (standard) | Razor: commission. Standard: spread-only | Razor has raw spreads with commission |

## Minimum Position Sizes

| Broker | Standard Account | Mini Account | Micro Account | Nano Lots? |
|--------|-----------------|--------------|---------------|------------|
| OANDA | 1 unit (0.00001 lots) | N/A | N/A | Effectively yes |
| IG | 0.01 lots (1K) | N/A | N/A | No |
| FXCM | 0.01 lots (1K) | N/A | N/A | No |
| IBKR | 25K minimum for most pairs | N/A | N/A | No (institutional) |
| Saxo | 0.01 lots (1K) | N/A | N/A | No |
| Pepperstone | 0.01 lots (1K) | N/A | N/A | No |

OANDA is unique: fractional units down to 1, allowing precise position sizing for small accounts.

