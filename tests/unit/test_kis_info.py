"""KIS info.get_warnings — maps search-stock-info caution flags."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from tooja.brokers.kis import info as info_mod
from tooja.brokers.kis.broker import KisBroker
from tooja.brokers.kis.info import KisInfoClient


def _broker():
    return KisBroker(app_key="K", app_secret="S", cano="12345678", hts_id="H", env="real")


@pytest.mark.asyncio
async def test_get_warnings_maps_halt_and_admin_flags(monkeypatch):
    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        assert request.PDNO == "005930"
        return SimpleNamespace(
            output=SimpleNamespace(
                tr_stop_yn="Y",
                admn_item_yn="N",
                model_dump=lambda: {"tr_stop_yn": "Y", "admn_item_yn": "N"},
            ),
        )

    monkeypatch.setattr(info_mod, "call", fake_call)
    broker = _broker()
    await broker.open()
    try:
        w = await KisInfoClient(broker).get_warnings("005930")
    finally:
        await broker.close()

    assert w.is_trading_halt is True
    assert w.is_administrative is False
    # Flags KIS does not report stay None.
    assert w.is_overheated is None
    assert w.is_liquidation is None
