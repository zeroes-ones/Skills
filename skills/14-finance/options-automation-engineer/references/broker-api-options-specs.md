# Broker API Options Specifications

## Comparison Matrix

| Feature | IBKR | TDA/Schwab | Tradier | tastytrade | Alpaca |
|---------|------|-----------|---------|------------|--------|
| **Options API** | ✅ Full | ⚠️ Limited | ✅ Good | ✅ Best-in-class | ⚠️ Basic |
| **Complex Orders** | ✅ Native | ✅ thinkorswim only | ✅ Up to 4 legs | ✅ Native | ❌ Single-leg only |
| **Real-time options quotes** | ✅ Streaming | ✅ Streaming | ✅ REST | ✅ Streaming | ⚠️ REST only |
| **Options chains** | ✅ Full | ✅ Good | ✅ | ✅ | ⚠️ Basic |
| **Greeks (server-computed)** | ✅ | ✅ thinkorswim | ✅ | ✅ | ❌ |
| **Conditional orders** | ✅ Full | ✅ | ❌ | ✅ | ❌ |
| **Paper trading** | ✅ | ✅ thinkorswim | ✅ Sandbox | ✅ | ✅ |
| **Historical options data** | ⚠️ Limited | ✅ thinkorswim | ❌ | ⚠️ Limited | ❌ |
| **SDK/Python library** | `ib_insync` | `schwab-py` | `tradier-python` | `tastytrade-api` | `alpaca-py` |
| **WebSocket** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Rate limits (trades/min)** | 50 | 120 | 60 | 30 | 200 |
| **Rate limits (quotes/sec)** | 100 | Unlisted | 120 | 50 | Unlimited* |
| **Min account** | $0 (Lite) | $0 | $0 | $0 | $0 |
| **Options approval** | Level 1-4 | Level 1-3 | Level 1-4 | Level 1-4 | Level 1-2 |
| **Portfolio margin** | ✅ | ✅ | ❌ | ❌ | ❌ |

## Interactive Brokers (IBKR) — Recommended for Advanced Automation

### Setup

```python
from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # TWS must be running
# OR: ib.connect('127.0.0.1', 4002, clientId=1)  # IB Gateway
```

### Options Chain

```python
# Get option chain
contract = Stock('AAPL', 'SMART', 'USD')
ib.qualifyContracts(contract)

chains = ib.reqSecDefOptParams(
    contract.symbol, '', contract.secType, contract.conId)

# Filter by expiration and strike
for chain in chains:
    if chain.expiration == '20260731':
        call_strikes = chain.strikes
```

### Complex Order (Spread)

```python
# Bull put spread
contracts = [
    Option('SPY', '20260731', 445, 'P', 'SMART'),
    Option('SPY', '20260731', 440, 'P', 'SMART'),
]
ib.qualifyContracts(*contracts)

# Create combo (native spread order)
bag = Bag()
bag.add(contracts[0], 1, action='SELL')  # Sell short put
bag.add(contracts[1], 1, action='BUY')   # Buy long put
combo = ComboLeg()
combo.bag = bag

order = Order()
order.action = 'SELL'  # Sell the spread (credit)
order.totalQuantity = 10
order.orderType = 'LMT'
order.lmtPrice = 0.30
order.tif = 'DAY'
order.outsideRTH = True

trade = ib.placeOrder(combo, order)
```

### Conditional Orders

```python
# Bracket order
parent = LimitOrder('BUY', 1, 4.50)
parent.transmit = False

profit = LimitOrder('SELL', 1, 9.00)
profit.parentId = parent.orderId
profit.transmit = False

stop = StopOrder('SELL', 1, 2.25)
stop.parentId = parent.orderId
stop.transmit = True  # Last child transmits the whole bracket

ib.placeOrder(option_contract, parent)
```

### Auto-Roll Logic

```python
def auto_roll_credit_spread(ib, position, target_dte=42):
    """Roll a credit spread to a new expiration."""

    # 1. Close existing position
    close_order = build_close_order(position)
    close_trade = ib.placeOrder(position.combo, close_order)

    # Wait for fill
    while not close_trade.isDone():
        ib.sleep(0.1)

    if close_trade.orderStatus.status != 'Filled':
        logger.error(f"Close order not filled: {close_trade.orderStatus.status}")
        return None

    # 2. Open new position at target DTE
    new_combo = build_same_strike_combo(
        position.underlying, position.strikes,
        target_dte, position.quantity
    )

    roll_credit = calculate_roll_credit(position, close_trade)
    if roll_credit < 0.05:
        logger.info(f"Roll credit ${roll_credit:.2f} too small — not rolling")
        return None

    new_order = LimitOrder('SELL', position.quantity, roll_credit)
    new_trade = ib.placeOrder(new_combo, new_order)

    return new_trade
```

### Limitations for Automation

- TWS/Gateway must be running (no direct API access without the desktop app)
- Complex order routing can be slow (> 5 seconds) during high-volume periods
- API disconnects are common during market hours; retry logic is essential
- The `ib_insync` library is community-maintained, not official
- Rate limits apply differently to TWS API vs Client Portal API
- Memory usage of ib_insync grows over time; restart daily

## Tradier — Best for Simplicity

### Setup

```python
import requests

TRADIER_TOKEN = "your_token"
BASE_URL = "https://api.tradier.com/v1"
HEADERS = {"Authorization": f"Bearer {TRADIER_TOKEN}", "Accept": "application/json"}

# Sandbox for testing
BASE_URL = "https://sandbox.tradier.com/v1"
```

### Multi-Leg Order

```python
def place_spread_order(account_id, symbol, option_symbol_short,
                       option_symbol_long, quantity, price, side="sell"):
    """Place a multi-leg spread order."""

    payload = {
        "account_id": account_id,
        "class": "multileg",
        "symbol": symbol,
        "type": "limit",
        "duration": "day",
        "price": price,
        "quantity": quantity,
        "side": side,  # "sell" for credit spread
        "leg": [
            {"option_symbol": option_symbol_short, "side": "sell_to_open",
             "quantity": quantity},
            {"option_symbol": option_symbol_long, "side": "buy_to_open",
             "quantity": quantity},
        ]
    }

    r = requests.post(
        f"{BASE_URL}/accounts/{account_id}/orders",
        headers=HEADERS, json=payload
    )
    return r.json()
```

### Limitation

- Max 4 legs per complex order
- No native conditional orders (OCO must be simulated)
- Limited exchange routing options
- Options symbol format is strict (e.g., `SPY240719P00445000`)

## tastytrade — Best UX for Options Automation

### Setup

```python
from tastytrade import Session, Account

session = Session('username', 'password')
accounts = Account.get_accounts(session)
account = accounts[0]
```

### Complex Order

```python
from tastytrade.order import NewOrder, OrderLeg, OrderType, TimeInForce, OrderAction

leg1 = OrderLeg(
    symbol='SPY  240719P00445000',
    action=OrderAction.SELL_TO_OPEN,
    quantity=10
)
leg2 = OrderLeg(
    symbol='SPY  240719P00440000',
    action=OrderAction.BUY_TO_OPEN,
    quantity=10
)

order = NewOrder(
    time_in_force=TimeInForce.DAY,
    order_type=OrderType.LIMIT,
    legs=[leg1, leg2],
    price=0.30
)

placed = account.place_order(session, order, dry_run=False)
```

### Advantage for Options Automation

- Schema designed for options from the ground up
- Native support for complex strategies (named strategies like iron_condor, butterfly)
- Built-in risk calculations
- Dry-run mode for testing without real orders
- Better WebSocket for real-time quotes and fills

## Execution Quality Monitoring

```python
def monitor_execution_quality(orders_history):
    """Track execution quality over time."""

    metrics = {
        "total_orders": len(orders_history),
        "avg_fill_vs_mid": sum(o.fill_vs_mid for o in orders_history) / len(orders_history),
        "avg_fill_time": sum(o.fill_time for o in orders_history) / len(orders_history),
        "partial_fill_rate": sum(1 for o in orders_history if o.partial_fill) / len(orders_history),
        "rejection_rate": sum(1 for o in orders_history if o.rejected) / len(orders_history),
        "exchange_distribution": Counter(o.exchange for o in orders_history),
        "fill_vs_mid_by_exchange": {},
    }

    for exchange in metrics["exchange_distribution"]:
        exchange_orders = [o for o in orders_history if o.exchange == exchange]
        metrics["fill_vs_mid_by_exchange"][exchange] = (
            sum(o.fill_vs_mid for o in exchange_orders) / len(exchange_orders)
        )

    # Alert on degradation
    if metrics["avg_fill_vs_mid"] > 0.03:
        alert("Fill quality degraded. Avg fill vs mid: {:.1%}".format(
            metrics["avg_fill_vs_mid"]))

    return metrics
```

## Broker Selection Decision Tree

```
Need complex order support?
├─ YES → Need portfolio margin?
│        ├─ YES → IBKR (only option with PM + complex orders)
│        └─ NO → Need best API DX?
│                ├─ YES → tastytrade
│                └─ NO → Tradier (simpler, cheaper)
└─ NO → Alpaca (for simple single-leg options only)
```

## Summary

- **IBKR** for institutional-grade automation with portfolio margin
- **tastytrade** for best options-specific API experience
- **Tradier** for simplicity and low cost
- **TDA/Schwab** for manual trading; API lags behind for options
- **Alpaca** for equity-first automation that occasionally trades options
- **Always test in paper/sandbox** before going live with real capital
- **Monitor execution quality** continuously — it degrades during high vol
