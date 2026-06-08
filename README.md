# tooja

[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**A unified Python client for Korean securities brokers.** It pairs a broker-agnostic common abstraction (thick API) with a raw escape hatch that calls each broker's native API directly when you need it. The goal is to do for Korean brokers what ccxt did for crypto exchanges.

Currently supported adapters: **Korea Investment & Securities (KIS)**, **Toss Securities (Toss)**.

> ⚠️ **Status: 0.1.0 (early).** Quotes, account, orders, and streaming are fully verified end-to-end on the demo (paper) environment. Real (live) orders have been confirmed to reach the KIS servers along the full code path, but end-to-end verification through actual fills is not done yet. **When using the real environment, always verify yourself with small amounts first.**

---

## Features

- **Common models + raw escape hatch** — work with normalized `Quote`/`Order`/`Balance`, and reach unsupported endpoints directly via `broker.raw.*`
- **async-first** — all I/O is `async`/`await`, built on `asyncio`
- **Real/demo switch** — flip with a single `env="real"` or `env="demo"` (ccxt/Alpaca convention)
- **Strict money type** — `Money` is `Decimal`-only and blocks operations across mismatched currencies
- **Automatic rate limiting** — token bucket + exponential backoff retry on the server-side `EGW00201`
- **Token cache** — persisted to disk, multi-account safe (scoped by app_key hash)
- **WebSocket streams** — quotes/trades/orderbook/my-orders, with auto-reconnect + PINGPONG

---

## Installation

```bash
# uv (recommended)
uv add tooja

# pip
pip install tooja
```

Requirements: Python 3.13+

> Before it is published to PyPI, install from source:
> ```bash
> git clone https://github.com/cookieshake/tooja && cd tooja && uv sync
> ```

---

## Quick Start

```python
import asyncio
from tooja.brokers.kis import KisBroker


async def main():
    async with KisBroker(
        app_key="...",
        app_secret="...",
        cano="50000000",       # first 8 digits of the account number
        hts_id="your_hts_id",
        env="demo",            # "real" or "demo"
    ) as broker:
        quote = await broker.market.get_quote("005930")  # Samsung Electronics
        print(quote.price)     # Money(amount=Decimal('70000'), currency=KRW)


asyncio.run(main())
```

A broker is an async context manager. Leaving the `async with` block tears down the HTTP session. For manual control, use `await broker.open()` / `await broker.close()`.

Tokens and approval keys are issued **lazily** — they are issued automatically on the first authenticated call and cached to disk.

---

## Toss Securities (Toss) Quick Start

```python
import asyncio
from tooja.brokers.toss import TossBroker


async def main():
    async with TossBroker(
        client_id="...",
        client_secret="...",
        account_seq=12345678,   # optional — only needed for account/order calls
    ) as broker:
        quote = await broker.market.get_quote("005930")  # Samsung Electronics
        print(quote.price)     # Money(amount=Decimal('...'), currency=KRW)


asyncio.run(main())
```

### Authentication

| Argument | Description |
|---|---|
| `client_id`, `client_secret` | Toss Open API OAuth2 client credentials |
| `account_seq` | Account sequence number (int). Only required for account/order APIs; not needed for quotes or info lookups |
| `token_cache` | `"disk"` (default, persists across restarts) / `"memory"` (in-process) |
| `rate_limit` | Provide a `RateLimitConfig` directly (optional) |

Authentication: **OAuth2 client_credentials**. The access token is issued automatically on the first call and cached.

You can reach every Toss endpoint (exchange rates, fees, market calendar, etc.) directly via `broker.raw.<category>` (categories: `account`, `asset`, `auth`, `market_data`, `market_info`, `order`, `order_history`, `order_info`, `stock_info`).

### Support matrix

| Domain | Supported methods | Notes |
|---|---|---|
| **market** | `get_quote` · `get_quotes` · `get_orderbook` · `get_ohlcv` · `get_price_limits` | candle interval: only `"1m"` · `"1d"` supported (others → `UnsupportedOperation`) |
| **account** | `get_balance` · `get_positions` · `get_position` · `get_buying_power` · `get_sellable_quantity` | requires `account_seq` |
| **orders** | `create` · `get` · `cancel` · `replace` · `list_orders` · `iter_orders` | stop orders → `UnsupportedOperation`; `list_fills` → `UnsupportedOperation` |
| **info** | `get_stock` · `get_warnings` · `is_holiday` | `list_halts` · `search` · `get_financials` · `get_dividends` → `UnsupportedOperation` |
| **analytics** | — | all `UnsupportedOperation` |
| **rankings** | — | all `UnsupportedOperation` |
| **stream** | — | all `UnsupportedOperation` |

---

## KIS authentication / environment

| Argument | Description |
|---|---|
| `app_key`, `app_secret` | KIS app key/secret |
| `cano` | first 8 digits of the account number |
| `hts_id` | HTS user ID (required for the WS my-order stream) |
| `acnt_prdt_cd` | account product code, defaults to `"01"` |
| `env` | `"real"` (live, openapi:9443, 20 RPS) / `"demo"` (paper, openapivts:29443, 2 RPS) |
| `rate_limit` | Provide a `RateLimitConfig` directly (optional) |

`env` is the entire safety boundary. There is no dry-run mode — with `env="real"`, orders are actually sent.

---

## Usage patterns

### Quotes (market)

```python
await broker.market.get_quote("005930")                       # -> Quote
await broker.market.get_quotes(["005930", "000660"])          # -> list[Quote] (concurrent)
await broker.market.get_orderbook("005930", depth=10)         # -> Orderbook
await broker.market.get_ohlcv("005930", interval="1d", limit=30)  # -> list[OHLCV]
# interval: "1m" "5m" "15m" "30m" "1h" "1d" "1w" "1M"
```

### Account (account)

```python
balance = await broker.account.get_balance()      # -> Balance (total_asset, cash, positions)
positions = await broker.account.get_positions()  # -> list[Position]
pos = await broker.account.get_position("005930") # -> Position | None
```

### Orders (orders)

```python
from decimal import Decimal
from tooja.core import Money, Symbol, LimitOrder, MarketOrder, OrderSide, Currency

# limit buy
order = await broker.orders.create(LimitOrder(
    symbol=Symbol.parse("005930"),
    side=OrderSide.BUY,
    qty=Decimal(10),
    price=Money(amount=Decimal(70000), currency=Currency.KRW),
))

await broker.orders.get(order.order_id)                       # -> Order (current state)
await broker.orders.replace(order.order_id, price=Decimal(69000))  # amend
await broker.orders.cancel(order.order_id)                    # cancel

# market sell
await broker.orders.create(MarketOrder(
    symbol=Symbol.parse("000660"), side=OrderSide.SELL, qty=Decimal(5),
))

# query orders/fills
await broker.orders.list_orders(status="open")   # "all" | "open" | "closed"
await broker.orders.list_fills()                 # -> list[Fill]
async for o in broker.orders.iter_orders():
    ...
```

### Info / analytics / rankings (info / analytics / rankings)

```python
from datetime import date
from tooja.core import RankingType

await broker.info.get_stock("005930")               # -> StockInfo
await broker.info.get_dividends("005930")
await broker.info.is_holiday(date(2026, 1, 1))      # -> bool
await broker.info.list_halts()                      # halted symbols

await broker.analytics.investor_flows("005930")     # trading flows by investor type
await broker.analytics.program_trading("005930")
await broker.analytics.short_selling("005930")

await broker.rankings.get(RankingType.VOLUME, limit=30)  # -> list[RankingEntry]
# RankingType: VOLUME, TURNOVER, MARKET_CAP, PRICE_CHANGE_UP, ...
```

### Real-time streams (stream, WebSocket)

```python
async with broker.stream.quotes(["005930", "000660"]) as stream:
    async for quote in stream:
        print(quote.symbol, quote.price)

# trades / orderbook follow the same pattern
# my-order fill notifications (per account)
async with broker.stream.orders() as stream:
    async for update in stream:
        print(update.order_id, update.status)
```

Streams are entered with `async with` and consumed with `async for`. They auto-reconnect by default, and you can adjust subscriptions at runtime with `await stream.subscribe(sym)` / `await stream.unsubscribe(sym)`.

### Rebalancing (portfolio)

```python
from decimal import Decimal
from tooja.core import Symbol
from tooja.portfolio.rebalance import Rebalancer, TargetWeight

rb = Rebalancer(
    broker,
    targets=[
        TargetWeight(symbol=Symbol.parse("005930"), weight=Decimal("0.6")),
        TargetWeight(symbol=Symbol.parse("000660"), weight=Decimal("0.4")),
    ],
    cash_buffer_rate=Decimal("0.02"),   # hold 2% as cash
    min_order_value=Decimal("10000"),   # skip orders below 10,000 KRW
)

plan = await rb.compute_plan()          # -> RebalancePlan (orders, expected_drift)
orders = await rb.execute(plan)         # execute the orders as planned
```

`Rebalancer` depends only on the `Broker` ABC, so it works with any adapter.

---

## Raw escape hatch

For endpoints the common models don't cover, you can reach the KIS native API directly. `broker.raw.<category>.<Executor>` gives you the auto-generated raw executor classes (338 endpoints).

```python
# access a raw executor class (categories are lazily imported on first access)
ExecCls = broker.raw.domestic_stock_quotations.InquirePriceExecutor
```

> Note: the raw layer currently exposes **executor class access**, and execution is low-level. Normalized call helpers will be refined in a future release. For most tasks, the thick API above is enough.

---

## Rate limit & errors

```python
from tooja.core import RateLimitConfig

broker = KisBroker(..., rate_limit=RateLimitConfig(per_sec=10, max_retries=5, base_backoff=0.1))
```

Defaults are 20 RPS on real / 2 RPS on demo. The server-side `EGW00201` (transactions-per-second exceeded) is retried automatically with exponential backoff.

All exceptions inherit from `BrokerError`:

`AuthError` · `PermissionDenied` · `RateLimitError` · `UnsupportedOperation` · `MarketClosed` · `SymbolNotFound` · `OrderRejected` · `InsufficientFunds` · `OrderNotFound` · `NetworkError` · `TimeoutError` · `SubscriptionLimitExceeded` · `ConfigError` · `BrokerAPIError`

```python
from tooja.core import OrderRejected

try:
    await broker.orders.create(...)
except OrderRejected as e:
    print(e.raw_code, e.raw_message)   # preserves the original KIS code/message
```

---

## Limitations & roadmap

**Current limitations**
- KIS and Toss adapters provided; Kiwoom / DB and others not supported
- KIS real-order end-to-end verification incomplete (the code path is verified)
- KIS demo (paper) does not provide some TRs — e.g. `inquire-daily-ccld`, `search-stock-info`
- Toss: stream/analytics/rankings not supported
- Toss: OHLCV interval supports only `"1m"` · `"1d"` (no 5m, 15m, etc.)
- The raw escape hatch goes only as far as class access (execution helpers are future work)

**Roadmap**
- Real-order end-to-end verification
- Normalized raw call helpers
- Additional broker adapters

---

## License

[MIT](LICENSE) © Youngchan Kim
