"""Live KIS smoke test — exercises the read paths against real KIS.

NEVER calls order POST. Run with:
    uv run python scripts/live_smoke.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from datetime import date, timedelta

from tooja.brokers.kis.broker import KisBroker
from tooja.core.enums import RankingType


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


def _env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        print(f"missing env: {name}", file=sys.stderr)
        sys.exit(2)
    return v


async def main() -> int:
    _load_dotenv()
    env = os.environ.get("KIS_ENV", "demo")
    prefix = "KIS_REAL_" if env == "real" else "KIS_DEMO_"

    def pick(suffix: str) -> str:
        # Prefer KIS_<SUFFIX>; fall back to env-specific KIS_REAL_/KIS_DEMO_.
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
        env=env,  # type: ignore[arg-type]
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
        # Token / approval_key (lazy).
        await step("auth.get_access_token", broker.get_access_token())
        await step("auth.get_approval_key", broker.get_approval_key())

        # market.*
        q = await step("market.get_quote 005930", broker.market.get_quote("005930"))
        if q is not None:
            print(f"     -> price={q.price} change={q.change}")

        ob = await step("market.get_orderbook 005930", broker.market.get_orderbook("005930", depth=5))
        if ob is not None:
            print(f"     -> bids={len(ob.bids)} asks={len(ob.asks)}")

        bars = await step(
            "market.get_ohlcv 1d limit=5",
            broker.market.get_ohlcv("005930", interval="1d", limit=5),
        )
        if bars is not None:
            print(f"     -> {len(bars)} bars")

        # account.*
        bal = await step("account.get_balance", broker.account.get_balance())
        if bal is not None:
            print(f"     -> total={bal.total_asset}  positions={len(bal.positions)}")

        await step("account.get_positions", broker.account.get_positions())

        # orders.* (read-only)
        await step(
            "orders.list_orders today",
            broker.orders.list_orders(status="all", since=date.today()),
        )

        # info.*
        info = await step("info.get_stock 005930", broker.info.get_stock("005930"))
        if info is not None:
            print(f"     -> name={info.name}")

        # analytics.* — date window: last 30d (server returns daily series).
        until = date.today()
        since = until - timedelta(days=30)
        await step(
            "analytics.investor_flows 30d",
            broker.analytics.investor_flows("005930", since=since, until=until),
        )

        # rankings.*
        rk = await step(
            "rankings.get VOLUME",
            broker.rankings.get(RankingType.VOLUME, limit=5),
        )
        if rk is not None:
            print(f"     -> {len(rk)} entries; top={rk[0].symbol if rk else 'none'}")

    print()
    if failures:
        print(f"FAILURES ({len(failures)}): {failures}")
        return 1
    print("ALL OK")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
