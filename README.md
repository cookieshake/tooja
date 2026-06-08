# tooja

[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**한국 증권사를 위한 통합 Python 클라이언트.** 브로커에 종속되지 않는 공통 추상화(thick API)와, 필요할 때 증권사 원본 API를 그대로 호출하는 raw 탈출구(escape hatch)를 함께 제공합니다. ccxt가 거래소에 해준 일을 한국 증권사에 하는 것이 목표입니다.

현재 지원 어댑터: **한국투자증권(KIS)**, **토스증권(Toss)**.

> ⚠️ **상태: 0.1.0 (초기).** KIS 단일 어댑터. 시세·계좌·주문·스트림은 모의투자(demo)에서 전 구간 검증됨. 실전(real) 주문은 코드 경로가 KIS 서버까지 정상 도달함을 확인했으나 실제 체결까지의 종단 검증은 아직입니다. **실전 사용 시 반드시 소액으로 직접 확인하세요.**

---

## 특징

- **공통 모델 + raw 탈출구** — 정규화된 `Quote`/`Order`/`Balance` 등으로 작업하다가, 미지원 엔드포인트는 `broker.raw.*`로 원본 호출
- **async-first** — 모든 I/O가 `async`/`await`, `asyncio` 기반
- **실전/모의 전환** — `env="real"` 또는 `env="demo"` 한 줄로 전환 (ccxt/Alpaca 관례)
- **엄격한 금액 타입** — `Money`는 `Decimal` 전용, 통화 불일치 연산 차단
- **자동 rate limit** — 토큰 버킷 + 서버측 `EGW00201` 지수 백오프 재시도
- **토큰 캐시** — 디스크 영속화, 멀티 계정 안전(app_key 해시 스코프)
- **WebSocket 스트림** — 시세/체결/호가/내 주문, 자동 재연결 + PINGPONG

---

## 설치

```bash
# uv (권장)
uv add tooja

# pip
pip install tooja
```

요구사항: Python 3.13+

> PyPI 배포 전이라면 소스에서 설치:
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
        cano="50000000",       # 계좌번호 앞 8자리
        hts_id="your_hts_id",
        env="demo",            # "real" 또는 "demo"
    ) as broker:
        quote = await broker.market.get_quote("005930")  # 삼성전자
        print(quote.price)     # Money(amount=Decimal('70000'), currency=KRW)


asyncio.run(main())
```

브로커는 async context manager입니다. `async with` 블록을 벗어나면 HTTP 세션이 정리됩니다. 직접 제어하려면 `await broker.open()` / `await broker.close()`.

토큰과 approval_key는 **지연 발급**됩니다 — 첫 인증 호출 시 자동 발급되어 디스크에 캐시됩니다.

---

## 토스증권 (Toss) Quick Start

```python
import asyncio
from tooja.brokers.toss import TossBroker


async def main():
    async with TossBroker(
        client_id="...",
        client_secret="...",
        account_seq=12345678,   # 선택 — 계좌/주문 호출에만 필요
    ) as broker:
        quote = await broker.market.get_quote("005930")  # 삼성전자
        print(quote.price)     # Money(amount=Decimal('...'), currency=KRW)


asyncio.run(main())
```

### 인증

| 인자 | 설명 |
|---|---|
| `client_id`, `client_secret` | Toss Open API OAuth2 client credentials |
| `account_seq` | 계좌 일련번호(int). 계좌/주문 API에만 필요; 시세·정보 조회는 불필요 |
| `token_cache` | `"disk"` (기본, 재기동 간 영속) / `"memory"` (프로세스 내) |
| `rate_limit` | `RateLimitConfig` 직접 지정 (선택) |

인증 방식: **OAuth2 client_credentials**. 액세스 토큰은 첫 호출 시 자동 발급되어 캐시됩니다.

`broker.raw.<카테고리>` 로 모든 Toss 엔드포인트(환율·수수료·시장캘린더 등)에 직접 접근할 수 있습니다 (카테고리: `account`, `asset`, `auth`, `market_data`, `market_info`, `order`, `order_history`, `order_info`, `stock_info`).

### 지원 매트릭스

| 도메인 | 지원 메서드 | 비고 |
|---|---|---|
| **market** | `get_quote` · `get_quotes` · `get_orderbook` · `get_ohlcv` · `get_price_limits` | candle interval: `"1m"` · `"1d"` 만 지원 (나머지 → `UnsupportedOperation`) |
| **account** | `get_balance` · `get_positions` · `get_position` · `get_buying_power` · `get_sellable_quantity` | `account_seq` 필수 |
| **orders** | `create` · `get` · `cancel` · `replace` · `list_orders` · `iter_orders` | stop 주문 → `UnsupportedOperation`; `list_fills` → `UnsupportedOperation` |
| **info** | `get_stock` · `get_warnings` · `is_holiday` | `list_halts` · `search` · `get_financials` · `get_dividends` → `UnsupportedOperation` |
| **analytics** | — | 전체 `UnsupportedOperation` |
| **rankings** | — | 전체 `UnsupportedOperation` |
| **stream** | — | 전체 `UnsupportedOperation` |

---

## KIS 인증 / 환경

| 인자 | 설명 |
|---|---|
| `app_key`, `app_secret` | KIS 앱 키/시크릿 |
| `cano` | 계좌번호 앞 8자리 |
| `hts_id` | HTS 사용자 ID (WS 내 주문 스트림에 필요) |
| `acnt_prdt_cd` | 계좌상품코드, 기본 `"01"` |
| `env` | `"real"`(실전, openapi:9443, 20 RPS) / `"demo"`(모의, openapivts:29443, 2 RPS) |
| `rate_limit` | `RateLimitConfig` 직접 지정 (선택) |

`env`가 전체 안전 경계입니다. dry-run 모드는 없습니다 — `env="real"`이면 주문이 실제로 전송됩니다.

---

## 사용 패턴

### 시세 (market)

```python
await broker.market.get_quote("005930")                       # -> Quote
await broker.market.get_quotes(["005930", "000660"])          # -> list[Quote] (동시 조회)
await broker.market.get_orderbook("005930", depth=10)         # -> Orderbook
await broker.market.get_ohlcv("005930", interval="1d", limit=30)  # -> list[OHLCV]
# interval: "1m" "5m" "15m" "30m" "1h" "1d" "1w" "1M"
```

### 계좌 (account)

```python
balance = await broker.account.get_balance()      # -> Balance (total_asset, cash, positions)
positions = await broker.account.get_positions()  # -> list[Position]
pos = await broker.account.get_position("005930") # -> Position | None
```

### 주문 (orders)

```python
from decimal import Decimal
from tooja.core import Money, Symbol, LimitOrder, MarketOrder, OrderSide, Currency

# 지정가 매수
order = await broker.orders.create(LimitOrder(
    symbol=Symbol.parse("005930"),
    side=OrderSide.BUY,
    qty=Decimal(10),
    price=Money(amount=Decimal(70000), currency=Currency.KRW),
))

await broker.orders.get(order.order_id)                       # -> Order (현재 상태)
await broker.orders.replace(order.order_id, price=Decimal(69000))  # 정정
await broker.orders.cancel(order.order_id)                    # 취소

# 시장가 매도
await broker.orders.create(MarketOrder(
    symbol=Symbol.parse("000660"), side=OrderSide.SELL, qty=Decimal(5),
))

# 주문/체결 조회
await broker.orders.list_orders(status="open")   # "all" | "open" | "closed"
await broker.orders.list_fills()                 # -> list[Fill]
async for o in broker.orders.iter_orders():
    ...
```

### 정보 / 분석 / 랭킹 (info / analytics / rankings)

```python
from datetime import date
from tooja.core import RankingType

await broker.info.get_stock("005930")               # -> StockInfo
await broker.info.get_dividends("005930")
await broker.info.is_holiday(date(2026, 1, 1))      # -> bool
await broker.info.list_halts()                      # 거래정지 종목

await broker.analytics.investor_flows("005930")     # 투자자별 매매동향
await broker.analytics.program_trading("005930")
await broker.analytics.short_selling("005930")

await broker.rankings.get(RankingType.VOLUME, limit=30)  # -> list[RankingEntry]
# RankingType: VOLUME, TURNOVER, MARKET_CAP, PRICE_CHANGE_UP, ... 등
```

### 실시간 스트림 (stream, WebSocket)

```python
async with broker.stream.quotes(["005930", "000660"]) as stream:
    async for quote in stream:
        print(quote.symbol, quote.price)

# trades / orderbook 도 동일 패턴
# 내 주문 체결 통보 (계좌 단위)
async with broker.stream.orders() as stream:
    async for update in stream:
        print(update.order_id, update.status)
```

스트림은 `async with`로 진입하고 `async for`로 소비합니다. 기본적으로 자동 재연결되며, 런타임에 `await stream.subscribe(sym)` / `await stream.unsubscribe(sym)`로 구독을 조정할 수 있습니다.

### 리밸런싱 (portfolio)

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
    cash_buffer_rate=Decimal("0.02"),   # 2%는 현금으로 보유
    min_order_value=Decimal("10000"),   # 1만원 미만 주문은 생략
)

plan = await rb.compute_plan()          # -> RebalancePlan (orders, expected_drift)
orders = await rb.execute(plan)         # 계획대로 주문 실행
```

`Rebalancer`는 `Broker` ABC에만 의존하므로 어떤 어댑터와도 동작합니다.

---

## Raw 탈출구

공통 모델이 다루지 않는 엔드포인트는 KIS 원본 API에 직접 접근할 수 있습니다. `broker.raw.<카테고리>.<Executor>`로 자동 생성된 raw executor 클래스(338개 엔드포인트)에 닿습니다.

```python
# raw executor 클래스 접근 (카테고리는 첫 접근 시 지연 import)
ExecCls = broker.raw.domestic_stock_quotations.InquirePriceExecutor
```

> 참고: 현재 raw 레이어는 **executor 클래스 접근**을 제공하며, 실행은 저수준입니다. 정규화된 호출 헬퍼는 향후 버전에서 다듬을 예정입니다. 대부분의 작업은 위의 thick API로 충분합니다.

---

## Rate limit & 에러

```python
from tooja.core import RateLimitConfig

broker = KisBroker(..., rate_limit=RateLimitConfig(per_sec=10, max_retries=5, base_backoff=0.1))
```

기본값은 실전 20 RPS / 모의 2 RPS. 서버측 `EGW00201`(초당 거래건수 초과)은 자동으로 지수 백오프 재시도됩니다.

예외는 모두 `BrokerError`를 상속합니다:

`AuthError` · `PermissionDenied` · `RateLimitError` · `UnsupportedOperation` · `MarketClosed` · `SymbolNotFound` · `OrderRejected` · `InsufficientFunds` · `OrderNotFound` · `NetworkError` · `TimeoutError` · `SubscriptionLimitExceeded` · `ConfigError` · `BrokerAPIError`

```python
from tooja.core import OrderRejected

try:
    await broker.orders.create(...)
except OrderRejected as e:
    print(e.raw_code, e.raw_message)   # KIS 원본 코드/메시지 보존
```

---

## 한계 & 로드맵

**현재 한계**
- KIS·Toss 어댑터 제공; Kiwoom / DB 등 미지원
- KIS 실전 주문 종단 검증 미완 (코드 경로는 검증됨)
- KIS 모의투자(demo)는 일부 TR 미제공 — 예: `inquire-daily-ccld`, `search-stock-info`
- Toss: stream/analytics/rankings 미지원
- Toss: OHLCV interval `"1m"`·`"1d"` 만 지원 (5m·15m 등 없음)
- raw 탈출구는 클래스 접근까지만 (실행 헬퍼는 향후)

**로드맵**
- 실전 주문 종단 검증
- raw 호출 헬퍼 정규화
- 추가 증권사 어댑터

---

## 라이선스

[MIT](LICENSE) © Youngchan Kim
