# Broker Integration — Futures

> Broker API specifics for futures: IBKR futures orders, Schwab futures, order types, SPAN pulls.

## Supported Brokers for Futures

| Broker | Futures Support | API Access | SPAN Margin | Spread Orders | Notes |
|--------|----------------|------------|-------------|---------------|-------|
| Interactive Brokers | Full | TWS API, Client Portal API, ib_insync | Yes (reqMktData genTick 238) | Yes (Combo orders) | Best futures broker for API trading |
| Schwab (thinkorswim) | Full | Schwab Developer Portal (limited) | Yes (Analyze tab) | Yes (Spread Book) | API futures support evolving |
| Alpaca | None | N/A | N/A | N/A | Futures not on roadmap per 2026-07 |
| Robinhood | None | N/A | N/A | N/A | No futures offering |

## Interactive Brokers (IBKR) — Futures API

### Connection

```
ib_insync: from ib_insync import IB, Future, FuturesOption
TWS API Port: 7497 (TWS) or 4002 (IB Gateway)
```

### Contract Definition

```python
from ib_insync import Future

# E-mini S&P 500
es = Future(symbol='ES', lastTradeDateOrContractMonth='202609', exchange='CME', currency='USD')

# Crude Oil
cl = Future(symbol='CL', lastTradeDateOrContractMonth='202608', exchange='NYMEX', currency='USD')

# Gold
gc = Future(symbol='GC', lastTradeDateOrContractMonth='202608', exchange='COMEX', currency='USD')

# 10-Year T-Note
zn = Future(symbol='ZN', lastTradeDateOrContractMonth='202609', exchange='CBOT', currency='USD')
```

### Market Data

```python
# Quote
ib.reqMktData(contract, '', False, False)

# SPAN Margin (generic tick type 238)
ib.reqMktData(contract, '238', False, False)
# Returns: initial margin, maintenance margin per contract
```

### Order Types

```python
from ib_insync import LimitOrder, MarketOrder, StopOrder

# Limit order (preferred for most futures)
order = LimitOrder(action='BUY', totalQuantity=1, lmtPrice=5525.50)

# Market order (use sparingly — only during DAY session)
order = MarketOrder(action='SELL', totalQuantity=1)

# Stop order (risk management only)
order = StopOrder(action='SELL', totalQuantity=1, stopPrice=5517.50)

# Calendar spread order (preferred for rolls)
spread = Future(symbol='ES', lastTradeDateOrContractMonth='202609', exchange='CME')
spread_next = Future(symbol='ES', lastTradeDateOrContractMonth='202612', exchange='CME')
combo = ib.bracketOrder(limitOrder, spread, spread_next, action='SELL')
```

### Important IBKR Futures Notes

- IBKR auto-liquidates physical delivery long futures 2-3 days before FND
- Futures are traded in the "US" account segment by default
- SPAN margin updates every Friday evening (CME publishes new risk arrays)
- IBKR charges ~$0.85/contract for futures (tiered pricing available)
- Micro contracts (MES, MNQ, M2K) trade at 1/10th the tick value and margin

## Schwab (thinkorswim) — Futures API

### API Access
- Schwab Developer Portal: developer.schwab.com
- Futures order placement available via Trading API
- Market data: Level 1 and Level 2 quotes
- SPAN margin: available through Account API (margin requirements)

### Limitations
- Futures API documentation is limited compared to IBKR
- Some order types may require thinkorswim platform
- Test thoroughly in paper trading before live

## SPAN Margin Retrieval

### Method 1: Broker API (Preferred)

```
IBKR: reqMktData(contract, '238', False, False)
Schwab: Account → marginRequirements (includes SPAN detail)
```

### Method 2: CME SPAN Direct

```
CME Clearing FTP: ftp.cmegroup.com/pub/span
Files updated weekly (Fridays)
Format: Binary PC-SPAN files (requires parsing)
Advanced: Use for independent margin verification
```

### Method 3: Exchange Websites

```
CME: cmegroup.com/clearing → Margins → Product search
CBOT: Same as CME (CME Group)
ICE: theice.com/clear-us → Margins
```

## Order Types by Session

| Session | Market | Limit | Stop | Spread | Notes |
|---------|--------|-------|------|--------|-------|
| PRE-OPEN (8:00-8:30 AM CT) | NO | YES | NO | NO | Wide spreads, thin book |
| OPEN (8:30-9:00 AM CT) | CAUTION | YES | YES | YES | High vol, limit preferred |
| DAY (9:00 AM-3:00 PM CT) | YES | YES | YES | YES | Best execution |
| CLOSE (3:00-3:15 PM CT) | CAUTION | YES | YES | YES | Settlement risk |
| POST-CLOSE (3:15-4:00 PM CT) | NO | CAUTION | NO | NO | Avoid |
| OVERNIGHT (5:00 PM-8:00 AM CT) | NO | YES | NO | YES | Limit only |
| WEEKEND | NO | CAUTION | NO | NO | Gap risk on Sunday open |

## Futures-Specific Order Qualifiers

| Qualifier | Description | When to Use |
|-----------|------------|------------|
| GTC (Good Till Canceled) | Order works until filled or canceled | Overnight limit orders |
| GTD (Good Till Date) | Order works until specified date | Specific roll windows |
| IOC (Immediate or Cancel) | Fill what you can, cancel rest | Illiquid contracts, partial fills |
| FOK (Fill or Kill) | Fill entire order or cancel | Calendar spreads |
| MIT (Market if Touched) | Becomes market order when price is touched | Trend entry (use carefully) |

