"""Live KIS demo order round-trip test (opt-in, gated by the ``kis_live`` marker).

Migrated from the former ``scripts/orders_smoke.py``. This is the ONLY coverage
of the live mutating order round-trip against KIS demo (모의투자) — the broader
``tests/test_kis_live.py`` sweep DRY_RUNs every dangerous POST and the unit/wire
tests use mocks, so this exercises the real ``order-cash`` + ``order-rvsecncl``
path end to end:

    orders.create -> orders.get -> orders.cancel -> orders.get (verify cancelled)

It places a LimitOrder BUY 1 share of 005930 (Samsung Electronics) at roughly
0.75 x prev_close rounded DOWN to the nearest 1,000 KRW tick — far enough below
market that it rests unfilled but still inside the KRX daily limit. The order is
always cancelled in a ``finally`` block so a resting demo order is never left
behind, even if an assertion fails mid-way.

SAFETY: hard-guarded to KIS demo. The test skips unless demo is selected
(``KIS_ENV=demo`` or the ``KIS_DEMO_*`` creds are present) AND credentials
resolve — mirroring ``orders_smoke.py``'s ``KIS_ENV != "demo"`` refusal so it can
NEVER fire against a real account.

Run manually:
    uv run pytest -m kis_live tests/test_kis_orders_live.py -s
"""

from __future__ import annotations

import os
from decimal import Decimal
from pathlib import Path

import pytest

from tooja.brokers.kis.broker import KisBroker
from tooja.core.enums import Currency, OrderSide, OrderStatus, TimeInForce
from tooja.core.models import LimitOrder, Money, Symbol

ROOT = Path(__file__).resolve().parent.parent
_DEMO_PREFIX = "KIS_DEMO_"


def _load_dotenv(path: Path = ROOT / ".env") -> None:
    """Best-effort load of repo-root .env into the environment (no overwrite)."""
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


def _pick(suffix: str) -> str | None:
    """Resolve a KIS cred from env, preferring KIS_<suffix> then KIS_DEMO_<suffix>."""
    return os.environ.get(f"KIS_{suffix}") or os.environ.get(f"{_DEMO_PREFIX}{suffix}")


@pytest.mark.kis_live
@pytest.mark.asyncio
async def test_kis_demo_order_create_get_cancel_roundtrip():
    _load_dotenv()

    # Hard guard: refuse anything but demo so this can never hit a real account.
    env = os.environ.get("KIS_ENV", "demo")
    have_demo_creds = bool(_pick("APP_KEY") and _pick("APP_SECRET") and _pick("CANO"))
    if env != "demo":
        pytest.skip(f"KIS_ENV={env!r} is not 'demo'; refusing live order round-trip")
    if not have_demo_creds:
        pytest.skip("KIS demo credentials not set (KIS_APP_KEY/KIS_DEMO_APP_KEY etc.)")

    app_key = _pick("APP_KEY")
    app_secret = _pick("APP_SECRET")
    cano = _pick("CANO")
    hts_id = _pick("HTS_ID")
    acnt_prdt_cd = _pick("ACNT_PRDT_CD") or "01"
    assert app_key and app_secret and cano and hts_id, "missing required KIS demo creds"

    broker = KisBroker(
        app_key=app_key,
        app_secret=app_secret,
        cano=cano,
        hts_id=hts_id,
        acnt_prdt_cd=acnt_prdt_cd,
        env="demo",
    )

    sym = "005930"  # Samsung Electronics

    async with broker:
        quote = await broker.market.get_quote(sym)
        current = quote.price.amount
        # Unfillable limit: 0.75 x prev_close (fallback current), rounded DOWN to
        # the nearest 1,000 KRW — a valid tick at this price range and inside the
        # KRX -30% daily limit, so it rests and never fills.
        ref = quote.prev_close.amount if quote.prev_close is not None else current
        bid_price = ((ref * Decimal("0.75")) // Decimal("1000")) * Decimal("1000")
        assert bid_price > 0

        req = LimitOrder(
            symbol=Symbol.parse(sym),
            side=OrderSide.BUY,
            qty=Decimal(1),
            price=Money(amount=bid_price, currency=Currency.KRW),
            time_in_force=TimeInForce.DAY,
        )

        order = None
        try:
            order = await broker.orders.create(req)
            assert order is not None
            assert order.order_id, "create() must return an Order with a non-empty order_id"

            fetched = await broker.orders.get(order.order_id)
            assert fetched is not None
            assert fetched.order_id == order.order_id

            cancelled = await broker.orders.cancel(order.order_id)
            assert cancelled is not None

            final = await broker.orders.get(order.order_id)
            assert final is not None
            assert final.status in (OrderStatus.CANCELLED, OrderStatus.REJECTED), (
                f"expected cancelled/closed status, got {final.status!r}"
            )
        finally:
            # Never leave a resting demo order: if create() succeeded but a later
            # step raised, best-effort cancel here.
            if order is not None and order.order_id:
                try:
                    await broker.orders.cancel(order.order_id)
                except Exception:
                    pass
