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
