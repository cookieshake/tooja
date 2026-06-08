"""Live KIS demo orders smoke test.

Exercises orders.create / orders.get / orders.cancel against KIS demo (모의투자).
Places a LimitOrder BUY 1 share of 005930 at price = current * 0.5 (won't fill),
then cancels it.

Run:
    uv run python scripts/orders_smoke.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from decimal import Decimal

from tooja.brokers.kis.broker import KisBroker
from tooja.core.enums import Currency, OrderSide, TimeInForce
from tooja.core.models import LimitOrder, Money, Symbol


def _load_dotenv(path: str = ".env") -> None:
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except FileNotFoundError:
        pass


async def main() -> int:
    _load_dotenv()
    env = os.environ.get("KIS_ENV", "demo")
    if env != "demo":
        print(f"REFUSING to run orders smoke in env={env!r}. Set KIS_ENV=demo.", file=sys.stderr)
        return 2

    prefix = "KIS_DEMO_"

    def pick(suffix: str) -> str:
        v = os.environ.get(f"KIS_{suffix}") or os.environ.get(f"{prefix}{suffix}")
        if not v:
            print(f"missing env: KIS_{suffix}", file=sys.stderr)
            sys.exit(2)
        return v

    broker = KisBroker(
        app_key=pick("APP_KEY"),
        app_secret=pick("APP_SECRET"),
        cano=pick("CANO"),
        hts_id=pick("HTS_ID"),
        acnt_prdt_cd=os.environ.get("KIS_ACNT_PRDT_CD")
        or os.environ.get(f"{prefix}ACNT_PRDT_CD", "01"),
        env="demo",
    )

    failures: list[str] = []

    async def step(name: str, coro):
        try:
            r = await coro
            print(f"OK   {name}")
            return r
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            failures.append(name)
            return None

    async with broker:
        sym = "005930"  # Samsung Electronics

        quote = await step(f"market.get_quote {sym}", broker.market.get_quote(sym))
        if quote is None:
            return 1

        current = quote.price.amount
        # Place a limit far below market so it sits unfilled, but inside the
        # KRX daily limit (-30% of prev_close). Use 0.75 * prev_close for a
        # comfortable margin, then round down to 1,000 KRW (valid tick at this
        # price range).
        ref = quote.prev_close.amount if quote.prev_close is not None else current
        bid_price = ((ref * Decimal("0.75")) // Decimal("1000")) * Decimal("1000")
        print(f"     current={current} ref={ref} -> bid={bid_price}")

        req = LimitOrder(
            symbol=Symbol.parse(sym),
            side=OrderSide.BUY,
            qty=Decimal(1),
            price=Money(amount=bid_price, currency=Currency.KRW),
            time_in_force=TimeInForce.DAY,
        )

        order = await step("orders.create LIMIT BUY 1@half-price", broker.orders.create(req))
        if order is None:
            return 1
        print(f"     order_id={order.order_id} status={order.status}")

        # Roundtrip lookup.
        fetched = await step(f"orders.get {order.order_id}", broker.orders.get(order.order_id))
        if fetched is not None:
            print(f"     fetched status={fetched.status}")

        # Cancel.
        cancelled = await step(
            f"orders.cancel {order.order_id}",
            broker.orders.cancel(order.order_id),
        )
        if cancelled is not None:
            print(f"     cancelled status={cancelled.status}")

        # Verify cancellation.
        final = await step(f"orders.get (post-cancel) {order.order_id}", broker.orders.get(order.order_id))
        if final is not None:
            print(f"     final status={final.status}")

    print()
    if failures:
        print(f"FAILED: {len(failures)} — {failures}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
