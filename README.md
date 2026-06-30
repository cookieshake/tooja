# tooja

[![PyPI](https://img.shields.io/pypi/v/tooja)](https://pypi.org/project/tooja/)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**A unified Python client for Korean securities brokers.** One broker-agnostic API
(`Quote` / `Order` / `Balance` / streams) across multiple brokers, plus a raw escape
hatch to each broker's native API when you need it. The goal: do for Korean brokers
what ccxt did for crypto exchanges.

Adapters: **Korea Investment & Securities (KIS)** · **Toss Securities (Toss)**.

---

## Features

- **One API, many brokers** — normalized `Quote`/`Order`/`Balance`; switch adapters without touching strategy code
- **Raw escape hatch** — reach any native endpoint directly via `broker.raw.*`
- **async-first** — every call is `async`/`await`, built on `asyncio`
- **Strict `Money`** — `Decimal`-only, rejects math across mismatched currencies
- **Built-in rate limiting** — token bucket + exponential backoff on the server-side `EGW00201`
- **Persistent token cache** — on disk, multi-account safe (scoped by app_key hash)
- **WebSocket streams** — quotes/trades/orderbook/my-orders, with auto-reconnect + PINGPONG

---

## Installation

```bash
uv add tooja      # or: pip install tooja
```

Requires Python 3.13+. To work from source:

```bash
git clone https://github.com/cookieshake/tooja && cd tooja && uv sync
```

---

## Quick start

The constructor differs per broker; **everything after it is identical.**

```python
import asyncio
from tooja.brokers.kis import KisBroker
from tooja.brokers.toss import TossBroker


async def main():
    # Korea Investment & Securities
    broker = KisBroker(
        app_key="...", app_secret="...",
        cano="50000000",          # first 8 digits of the account number
        hts_id="your_hts_id",
        env="demo",               # "real" or "demo"
    )

    # ...or Toss Securities — same API from here on
    # broker = TossBroker(client_id="...", client_secret="...", account_seq=12345678)

    async with broker:
        quote = await broker.market.get_quote("005930")   # Samsung Electronics
        print(quote.price)        # Money(amount=Decimal('70000'), currency=KRW)


asyncio.run(main())
```

A broker is an async context manager; leaving the `async with` block closes the HTTP
session (use `await broker.open()` / `await broker.close()` for manual control).
Tokens are issued **lazily** — on the first authenticated call — and cached to disk.

---

## Brokers

Both adapters speak the same API; they differ in how much of it they implement.

| Domain        | KIS                                                  | Toss                                                       |
|---------------|------------------------------------------------------|------------------------------------------------------------|
| **market**    | full — quote, orderbook, OHLCV, price limits         | quote, orderbook, price limits; OHLCV `1m`/`1d` only       |
| **account**   | full                                                 | full                                                       |
| **orders**    | full, incl. fills; overseas exchanges (US/HK/JP/CN/VN, limit-only) | no stop orders, no fills                     |
| **info**      | full — incl. dividends, financials, halts            | `get_stock`, `get_warnings`, `is_holiday` only             |
| **analytics** | ✅ investor flows, program trading, short selling, …  | —                                                          |
| **rankings**  | ✅                                                    | —                                                          |
| **stream**    | ✅ quotes, trades, orderbook, my-orders               | —                                                          |

Anything not covered above raises `UnsupportedOperation` — and is still reachable via
the [raw escape hatch](#raw-escape-hatch).

### KIS

```python
KisBroker(app_key="...", app_secret="...", cano="50000000", hts_id="...", env="demo")
```

| Argument             | Description                                                              |
|----------------------|-------------------------------------------------------------------------|
| `app_key`,`app_secret` | KIS app key/secret                                                    |
| `cano`               | first 8 digits of the account number                                    |
| `hts_id`             | HTS user ID (required for the WS my-order stream)                        |
| `acnt_prdt_cd`       | account product code, defaults to `"01"`                                |
| `env`                | `"real"` (live, 20 RPS) / `"demo"` (paper, 2 RPS)                        |
| `rate_limit`         | a `RateLimitConfig`, optional                                           |

`env` is the entire safety boundary — there is no dry-run mode, so with `env="real"`
orders are actually sent. Note that KIS **demo does not provide some TRs** (e.g.
`inquire-daily-ccld`, `search-stock-info`).

### Toss

```python
TossBroker(client_id="...", client_secret="...", account_seq=12345678)
```

| Argument                | Description                                                           |
|-------------------------|----------------------------------------------------------------------|
| `client_id`,`client_secret` | Toss Open API OAuth2 client credentials                          |
| `account_seq`           | account sequence number (int); required only for account/order calls |
| `token_cache`           | `"disk"` (default) / `"memory"`                                      |
| `rate_limit`            | a `RateLimitConfig`, optional                                        |

Authentication is **OAuth2 client_credentials**; the access token is issued on the
first call and cached.

---

## Usage

These calls are the same on any adapter — the examples use `broker` from the quick start.

### Market

```python
await broker.market.get_quote("005930")                          # -> Quote
await broker.market.get_quotes(["005930", "000660"])             # -> list[Quote] (concurrent)
await broker.market.get_orderbook("005930", depth=10)            # -> Orderbook
await broker.market.get_ohlcv("005930", interval="1d", limit=30) # -> list[OHLCV]
# KIS intervals: "1m" "5m" "15m" "30m" "1h" "1d" "1w" "1M"  ·  Toss: "1m" "1d"
```

### Account

```python
balance = await broker.account.get_balance()      # -> Balance (total_asset, cash, orderable_cash, positions)
positions = await broker.account.get_positions()  # -> list[Position]
pos = await broker.account.get_position("005930") # -> Position | None
```

### Orders

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

await broker.orders.get(order.order_id)                            # -> Order (current state)
await broker.orders.replace(order.order_id, price=Decimal(69000)) # amend
await broker.orders.cancel(order.order_id)                        # cancel

# market sell
await broker.orders.create(MarketOrder(
    symbol=Symbol.parse("000660"), side=OrderSide.SELL, qty=Decimal(5),
))

# overseas (KIS): routed by the exchange prefix — limit orders only
await broker.orders.create(LimitOrder(
    symbol=Symbol.parse("NASD:AAPL"), side=OrderSide.BUY, qty=Decimal(1),
    price=Money(amount=Decimal("145.00"), currency=Currency.USD),
))

# query
await broker.orders.list_orders(status="open")   # "all" | "open" | "closed"
await broker.orders.list_fills()                 # KIS only -> list[Fill]
```

### Info / analytics / rankings

```python
from datetime import date
from tooja.core import RankingType

await broker.info.get_stock("005930")            # -> StockInfo
await broker.info.is_holiday(date(2026, 1, 1))   # -> bool

# KIS only:
await broker.info.get_dividends("005930")
await broker.info.list_halts()                   # halted symbols
await broker.analytics.investor_flows("005930")  # trading flows by investor type
await broker.rankings.get(RankingType.VOLUME, limit=30)  # -> list[RankingEntry]
```

### Streams (WebSocket, KIS only)

```python
async with broker.stream.quotes(["005930", "000660"]) as stream:
    async for quote in stream:
        print(quote.symbol, quote.price)

# trades / orderbook follow the same pattern; orders() streams my-order fills
```

Streams are entered with `async with` and consumed with `async for`. They auto-reconnect
by default; adjust subscriptions at runtime with `await stream.subscribe(sym)` /
`await stream.unsubscribe(sym)`.

### Rebalancing

```python
from decimal import Decimal
from tooja.core import Symbol
from tooja.core.enums import RebalanceDirection
from tooja.portfolio.rebalance import Rebalancer, TargetWeight

rb = Rebalancer(
    broker,
    targets=[
        TargetWeight(symbol=Symbol.parse("005930"), weight=Decimal("0.6")),
        TargetWeight(symbol=Symbol.parse("000660"), weight=Decimal("0.4")),
    ],
    cash_buffer_rate=Decimal("0.02"),   # hold 2% of total assets as cash
    min_order_value=Decimal("10000"),   # ignore gaps below 10,000 KRW
    drift_band=Decimal("0.05"),         # only trade symbols >5% off target
    step_rate=Decimal("0.5"),           # close half the gap each run
    direction=RebalanceDirection.BOTH,  # or BUY_ONLY / SELL_ONLY
    cash_sink=Symbol.parse("133690"),   # park surplus cash in this symbol
)

plan = await rb.compute_plan()   # dry run — inspect before trading
await rb.execute(plan)           # convert trades to orders and place them
```

`compute_plan()` returns a full `RebalancePlan` you can inspect first: the
broker-neutral `trades` (`PlannedTrade`: symbol, side, qty), plus the
`expected_holdings`, `expected_cash`, and `expected_drift` they should produce
once filled. The plan states *what* to trade; `execute()` decides *how* at
submit time — domestic (KRX) trades become market orders, while overseas
trades become marketable limit orders at the live quote ± `limit_offset`
(KIS overseas regular-session trading is limit-only). The strategy knobs:

- **`drift_band`** — no-trade band; leave a symbol untouched until it drifts past
  this fraction of its target value (cuts churn from tiny gaps).
- **`step_rate`** — fraction of each gap to close per run. `< 1.0` rebalances
  gradually, using unbiased stochastic rounding on fractional shares so it still
  converges over many runs. Applies to off-target liquidations too: a dropped
  symbol is wound down by the same fraction each run rather than dumped at once
  (full mode, `1.0`, still exits it entirely in one go).
- **`direction`** — restrict to buys only, sells only, or both.
- **`cash_sink`** — invest cash above the buffer into one symbol instead of
  leaving it idle. Suppressed when `direction=SELL_ONLY` (the sink only ever
  adds buy exposure).
- **`limit_offset`** — aggressiveness of the marketable-limit price used for
  overseas trades at execute time (default `0.01` = 1%): buys are priced at
  quote × (1 + offset), sells at quote × (1 − offset). A trade whose quote
  cannot be fetched is skipped for that run. Domestic trades are unaffected.

`Rebalancer` depends only on the `Broker` ABC, so it works with any adapter.

---

## MCP server

`tooja` ships an [MCP](https://modelcontextprotocol.io/) server so AI assistants
(Claude Desktop, Claude Code, and any MCP-capable host) can query market data, inspect
account state, and place trades on your behalf — with strong safety defaults.

### Install

```bash
pip install tooja[mcp]
# or, with uv:
uv add "tooja[mcp]"
```

### Run

```bash
python -m tooja.mcp        # stdio transport (the standard MCP mode)
```

### Configuration

Configuration is loaded from environment variables by default, or from a TOML file when
`TOOJA_MCP_CONFIG` is set.

#### Single-account (KIS example)

| Variable | Description |
|---|---|
| `TOOJA_MCP_BROKER` | `kis` |
| `TOOJA_MCP_ENV` | `real` or `demo` |
| `TOOJA_MCP_APP_KEY` | KIS app key |
| `TOOJA_MCP_APP_SECRET` | KIS app secret |
| `TOOJA_MCP_CANO` | First 8 digits of the account number |
| `TOOJA_MCP_HTS_ID` | HTS user ID |
| `TOOJA_MCP_ACNT_PRDT_CD` | Account product code (default `01`) |
| `TOOJA_MCP_TRADING` | `true` / `false` — enable write tools (default `false`) |

For **Toss**, replace `APP_KEY/APP_SECRET/CANO/HTS_ID/ACNT_PRDT_CD` with
`TOOJA_MCP_CLIENT_ID`, `TOOJA_MCP_CLIENT_SECRET`, and `TOOJA_MCP_ACCOUNT_SEQ`.

#### Multi-account

Set `TOOJA_MCP_ACCOUNTS=main,pension` and prefix each field with the account name in
upper-case:

```bash
TOOJA_MCP_ACCOUNTS=main,pension
TOOJA_MCP_MAIN_BROKER=kis
TOOJA_MCP_MAIN_APP_KEY=...
TOOJA_MCP_MAIN_APP_SECRET=...
TOOJA_MCP_MAIN_CANO=...
TOOJA_MCP_MAIN_HTS_ID=...
TOOJA_MCP_MAIN_TRADING=true

TOOJA_MCP_PENSION_BROKER=kis
TOOJA_MCP_PENSION_APP_KEY=...
TOOJA_MCP_PENSION_APP_SECRET=...
TOOJA_MCP_PENSION_CANO=...
TOOJA_MCP_PENSION_HTS_ID=...
TOOJA_MCP_PENSION_TRADING=false
```

When more than one account is configured, tool calls require an `account` argument
(`"main"` / `"pension"` etc.). With a single account it is optional and defaults to the
only account.

#### Optional TOML config

Point `TOOJA_MCP_CONFIG=/path/to/config.toml` at a TOML file for structured config.
`${ENV_VAR}` references inside the TOML are expanded from the process environment.

### Claude Desktop / Claude Code integration

Add a block like this to your MCP host's config (e.g. `~/.claude/claude_desktop_config.json`
or `~/.claude.json`):

```json
{
  "mcpServers": {
    "tooja-real": {
      "command": "python",
      "args": ["-m", "tooja.mcp"],
      "env": {
        "TOOJA_MCP_BROKER": "kis",
        "TOOJA_MCP_ENV": "real",
        "TOOJA_MCP_APP_KEY": "<your-app-key>",
        "TOOJA_MCP_APP_SECRET": "<your-app-secret>",
        "TOOJA_MCP_CANO": "<your-cano>",
        "TOOJA_MCP_HTS_ID": "<your-hts-id>",
        "TOOJA_MCP_TRADING": "true"
      }
    },
    "tooja-demo": {
      "command": "python",
      "args": ["-m", "tooja.mcp"],
      "env": {
        "TOOJA_MCP_BROKER": "kis",
        "TOOJA_MCP_ENV": "demo",
        "TOOJA_MCP_APP_KEY": "<your-demo-app-key>",
        "TOOJA_MCP_APP_SECRET": "<your-demo-app-secret>",
        "TOOJA_MCP_CANO": "<your-demo-cano>",
        "TOOJA_MCP_HTS_ID": "<your-hts-id>",
        "TOOJA_MCP_TRADING": "true"
      }
    }
  }
}
```

Each entry is an isolated server process — real and demo accounts never share state.
If `python` is not in the system PATH, use the full path to the interpreter in your
virtual environment.

### Safety model

| Layer | Mechanism |
|---|---|
| **Read-only by default** | Order and rebalance *write* tools are only registered when `TOOJA_MCP_TRADING=true` for that account. With `trading` off the server exposes market data, balance, and order history but cannot place or modify orders. |
| **Two-phase confirm** | Every write tool requires two calls. The first call returns a preview of the intended action plus a `confirm_token`. Calling again with that exact `confirm_token` executes the action. Changing any parameter (symbol, qty, price, …) invalidates the token and forces a new preview. |

> **Note:** Real-time streaming (WebSocket quotes, trades, orderbook) is intentionally
> not exposed in this version of the MCP server.

---

## Raw escape hatch

For endpoints the common API doesn't cover, call each broker's native API directly via
`broker.raw`. Categories are lazily imported on first access.

```python
# KIS — auto-generated executor classes (338 endpoints)
ExecCls = broker.raw.domestic_stock_quotations.InquirePriceExecutor

# Toss — categories: account, asset, auth, market_data, market_info,
#        order, order_history, order_info, stock_info
client = broker.raw.market_data
```

> The raw layer currently exposes executor/category access; normalized call helpers are
> future work. For most tasks the common API above is enough.

---

## Rate limits & errors

```python
from tooja.core import RateLimitConfig

broker = KisBroker(..., rate_limit=RateLimitConfig(per_sec=10, max_retries=5, base_backoff=0.1))
```

Defaults: 20 RPS on KIS real, 2 RPS on KIS demo. The server-side `EGW00201`
(transactions-per-second exceeded) is retried automatically with exponential backoff.

All exceptions inherit from `BrokerError`:

`AuthError` · `PermissionDenied` · `RateLimitError` · `UnsupportedOperation` ·
`MarketClosed` · `SymbolNotFound` · `OrderRejected` · `InsufficientFunds` ·
`OrderNotFound` · `NetworkError` · `TimeoutError` · `SubscriptionLimitExceeded` ·
`ConfigError` · `BrokerAPIError`

```python
from tooja.core import OrderRejected

try:
    await broker.orders.create(...)
except OrderRejected as e:
    print(e.raw_code, e.raw_message)   # preserves the original broker code/message
```

---

## Disclaimer

`tooja` is an **unofficial, independent** project. It is **not affiliated with,
endorsed by, or supported by** Korea Investment & Securities, Toss Securities, or
any other broker. All product names, logos, and trademarks belong to their
respective owners.

The software is provided "as is", without warranty of any kind. You are solely
responsible for any trading activity conducted through this library, including any
financial loss. Use it at your own risk.

---

## License

[MIT](LICENSE) © Youngchan Kim
