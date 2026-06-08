"""Market subclient regression tests — focuses on interval routing for OHLCV."""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest

from tooja.brokers.kis import market as market_mod
from tooja.brokers.kis.broker import KisBroker
from tooja.brokers.kis.market import KisMarketClient


def _broker(env="real"):
    return KisBroker(
        app_key="K", app_secret="S", cano="12345678", hts_id="H", env=env,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("interval,expected_etc", [
    ("1m", ""),
    ("5m", "5"),
    ("15m", "15"),
    ("30m", "30"),
    ("1h", "60"),
])
async def test_intraday_interval_sets_etc_cls_code(monkeypatch, interval, expected_etc):
    """Regression: each intraday interval must produce a distinct
    FID_ETC_CLS_CODE. Previously this was hardcoded to "" so 5m/15m/30m/1h
    all silently returned 1m bars."""
    captured: dict = {}

    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        captured["request"] = request
        return SimpleNamespace(output2=[])

    monkeypatch.setattr(market_mod, "call", fake_call)

    broker = _broker(env="real")
    await broker.open()
    try:
        client = KisMarketClient(broker)
        await client.get_ohlcv("005930", interval=interval, limit=5)
    finally:
        await broker.close()

    assert captured["request"].FID_ETC_CLS_CODE == expected_etc


@pytest.mark.asyncio
async def test_get_price_limits_maps_upper_lower(monkeypatch):
    from tooja.core.money import Money
    from tooja.core.enums import Currency

    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        assert request.FID_INPUT_ISCD == "005930"
        return SimpleNamespace(
            output=SimpleNamespace(
                stck_mxpr="91000",
                stck_llam="49000",
                model_dump=lambda: {"stck_mxpr": "91000", "stck_llam": "49000"},
            ),
        )

    monkeypatch.setattr(market_mod, "call", fake_call)
    broker = _broker(env="real")
    await broker.open()
    try:
        pl = await KisMarketClient(broker).get_price_limits("005930")
    finally:
        await broker.close()

    assert pl.upper_limit == Money(amount=Decimal("91000"), currency=Currency.KRW)
    assert pl.lower_limit == Money(amount=Decimal("49000"), currency=Currency.KRW)


@pytest.mark.asyncio
async def test_get_price_limits_rejects_overseas(monkeypatch):
    from tooja.core.errors import UnsupportedOperation

    broker = _broker(env="real")
    await broker.open()
    try:
        with pytest.raises(UnsupportedOperation):
            await KisMarketClient(broker).get_price_limits("NASD:AAPL")
    finally:
        await broker.close()
