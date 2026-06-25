"""Wire-level regression tests for KIS adapter.

These tests bypass the usual `monkeypatch(orders_mod, "call", ...)` shortcut and
instead inject an `httpx.MockTransport` into the broker so the entire raw layer
(`raw/base.py:execute → _parse_response → _raise_for_status_error`) plus the
adapter mapping are exercised end-to-end. Each fixture under `tests/fixtures/`
captures a specific KIS wire quirk we hit on live demo (single dict output,
EGW00201 promotion, OFL_YN requirement).

Token issuance is stubbed out by pre-attaching a fake `TokenManager` so we
don't have to fixture-route the OAuth call too.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from tooja.brokers.kis.broker import KisBroker
from tooja.brokers.kis.orders import KisOrdersClient
from tooja.core.enums import Currency, OrderSide, OrderStatus
from tooja.core.errors import RateLimitError
from tooja.core.models import LimitOrder, Order, Symbol
from tooja.core.money import Money

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def _load(name: str) -> tuple[int, dict]:
    data = json.loads((FIXTURES / name).read_text())
    return data["_status"], data["_body"]


async def _fake_get_token() -> str:
    return "FAKE_TOKEN"


def _inject(broker: KisBroker, handler) -> None:
    """Attach a MockTransport-backed httpx client + fake token manager,
    then mark the broker as open."""
    transport = httpx.MockTransport(handler)
    broker._http = httpx.AsyncClient(
        base_url=broker.base_url, transport=transport,
    )
    broker._tokens = SimpleNamespace(
        get_token=_fake_get_token,
        invalidate=lambda: None,
        get_approval_key=_fake_get_token,
    )
    broker._open = True


def _broker(env="real") -> KisBroker:
    return KisBroker(
        app_key="K", app_secret="S", cano="12345678", hts_id="H", env=env,
    )


# ────────────────────────────────────────────────────────────────────────────
# Regression 1: order-cash `output` arriving as single dict (not list).
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_order_cash_single_dict_output_is_normalized_to_list():
    status, body = _load("order_cash_single_dict_ok.json")

    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["payload"] = json.loads(request.content.decode())
        return httpx.Response(status, json=body)

    broker = _broker(env="demo")
    _inject(broker, handler)
    try:
        req = LimitOrder(
            symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY,
            qty=Decimal("1"),
            price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        )
        order = await broker.orders.create(req)
    finally:
        await broker.close()

    assert order.order_id == "TEST0001"
    assert "order-cash" in captured["url"]


# ────────────────────────────────────────────────────────────────────────────
# Regression 1b: order-rvsecncl (cancel/replace) has the SAME single-dict quirk
# as order-cash. _rvsecncl is called directly with a pre-built Order so the wire
# only sees the cancel call (get() would otherwise need its own fixture).
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_order_rvsecncl_single_dict_output_is_normalized_to_list():
    from datetime import datetime, timezone

    status, body = _load("order_rvsecncl_single_dict_ok.json")

    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(status, json=body)

    broker = _broker(env="demo")
    _inject(broker, handler)
    existing = Order(
        order_id="TEST0001",
        symbol=Symbol(ticker="005930"),
        side=OrderSide.BUY,
        qty=Decimal("1"),
        type="limit",
        price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        status=OrderStatus.OPEN,
        submitted_at=datetime.now(timezone.utc),
        raw={"krx_fwdg_ord_orgno": "06010"},
    )
    try:
        client = KisOrdersClient(broker)
        cancelled = await client._rvsecncl(
            existing, dvsn="02", new_qty=None, new_price=None,
        )
    finally:
        await broker.close()

    assert cancelled.order_id == "TEST0002"
    assert cancelled.status is OrderStatus.CANCELLED
    assert "order-rvsecncl" in captured["url"]


# ────────────────────────────────────────────────────────────────────────────
# Regression 2: EGW00201 arriving as HTTP 500 must be retried, not bubbled as
# NetworkError. We let the handler return 5 EGW00201 responses (exceeding the
# default `max_retries=5`) so the loop exhausts and raises RateLimitError —
# proving the promotion path is reached AND the retry classification works.
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_egw00201_http500_promotes_and_exhausts_to_rate_limit_error():
    status, body = _load("egw00201_http500_rate_limited.json")
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(status, json=body)

    broker = _broker(env="real")
    # Shrink backoff so the test doesn't sleep for seconds.
    broker.rate_limit = broker.rate_limit.__class__(
        per_sec=broker.rate_limit.per_sec,
        max_retries=2,
        base_backoff=0.0,
    )
    _inject(broker, handler)
    try:
        req = LimitOrder(
            symbol=Symbol(ticker="005930"),
            side=OrderSide.BUY,
            qty=Decimal("1"),
            price=Money(amount=Decimal("70000"), currency=Currency.KRW),
        )
        with pytest.raises(RateLimitError):
            await broker.orders.create(req)
    finally:
        await broker.close()

    # Original try + max_retries retries = 3 total attempts.
    assert calls["n"] == 3


# ────────────────────────────────────────────────────────────────────────────
# Regression 3: account.get_balance request payload MUST include OFL_YN.
# KIS rejects the request as 'INPUT_FIELD_NAME OFL_YN' when omitted, even
# though the apiportal spec lists it as Optional.
# ────────────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_inquire_balance_request_includes_ofl_yn():
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if "inquire-balance" in request.url.path:
            # Domestic inquire-balance — capture query params for assertion.
            captured["query"] = dict(request.url.params)
            return httpx.Response(200, json={
                "rt_cd": "0",
                "msg_cd": "MCA00000",
                "msg1": "OK",
                "ctx_area_fk100": "",
                "ctx_area_nk100": "",
                "output1": [],
                "output2": [{
                    "dnca_tot_amt": "100000000",
                    "tot_evlu_amt": "100000000",
                }],
            })
        if "inquire-psbl-order" in request.url.path:
            # Domestic orderable-cash enrichment — valid response so get_balance
            # doesn't degrade; not the subject of this regression.
            return httpx.Response(200, json={
                "rt_cd": "0",
                "msg_cd": "MCA00000",
                "msg1": "OK",
                "output": {"nrcvb_buy_amt": "100000000"},
            })
        # Overseas inquire-present-balance — return empty valid response.
        return httpx.Response(200, json={
            "rt_cd": "0",
            "msg_cd": "MCA00000",
            "msg1": "OK",
            "output1": [],
            "output2": [],
            "output3": None,
        })

    broker = _broker(env="demo")
    _inject(broker, handler)
    try:
        await broker.account.get_balance()
    finally:
        await broker.close()

    assert "OFL_YN" in captured["query"], (
        "Adapter must send OFL_YN even though spec lists it as Optional — "
        "KIS server rejects with 'INPUT_FIELD_NAME OFL_YN' otherwise."
    )


def test_overseas_inquire_ccnl_output_rows_are_typed():
    """Regression: generator emitted `output: list[str]` for container arrays
    marked A0002 in the KIS spec, so real dict rows failed validation."""
    from tooja.brokers.kis.raw.overseas_stock_trading.inquire_ccnl import (
        InquireCcnlResponse,
    )

    resp = InquireCcnlResponse.model_validate({
        "rt_cd": "0", "msg_cd": "MCA00000", "msg1": "ok",
        "ctx_area_fk200": "", "ctx_area_nk200": "",
        "output": [{
            "ord_dt": "20260612", "odno": "0030089601",
            "sll_buy_dvsn_cd": "02", "pdno": "AAPL",
            "ft_ord_qty": "2", "ft_ord_unpr3": "145.00",
            "ft_ccld_qty": "0", "nccs_qty": "2",
            "ovrs_excg_cd": "NASD", "tr_crcy_cd": "USD",
        }],
    })
    assert resp.output[0].pdno == "AAPL"


def test_overseas_inquire_nccs_output_rows_are_typed():
    from tooja.brokers.kis.raw.overseas_stock_trading.inquire_nccs import (
        InquireNccsResponse,
    )

    resp = InquireNccsResponse.model_validate({
        "rt_cd": "0", "msg_cd": "MCA00000", "msg1": "ok",
        "output": [{"odno": "1", "pdno": "AAPL"}],
    })
    assert resp.output[0].pdno == "AAPL"


def test_overseas_inquire_present_balance_frcr_amt_is_string():
    """Regression: generator emitted `thdt_buy_ccld_frcr_amt: dict` from the
    KIS spec's Object marking, but the real response returns a string like
    '0.000000', so env="real" get_balance() raised 20 ValidationErrors."""
    from tooja.brokers.kis.raw.overseas_stock_trading.inquire_present_balance import (
        InquirePresentBalanceResponse,
    )

    resp = InquirePresentBalanceResponse.model_validate({
        "rt_cd": "0", "msg_cd": "MCA00000", "msg1": "ok",
        "output1": [{
            "pdno": "AAPL", "prdt_name": "APPLE INC",
            "thdt_buy_ccld_frcr_amt": "0.000000",
            "thdt_sll_ccld_frcr_amt": "0.000000",
        }],
        "output2": [],
    })
    assert resp.output1[0].thdt_buy_ccld_frcr_amt == "0.000000"
