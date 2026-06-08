"""KIS account promoted methods: buying power + sellable quantity."""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest

from tooja.brokers.kis import account as account_mod
from tooja.brokers.kis.account import KisAccountClient
from tooja.brokers.kis.broker import KisBroker
from tooja.core.enums import Currency
from tooja.core.money import Money


def _broker():
    return KisBroker(app_key="K", app_secret="S", cano="12345678", hts_id="H", env="real")


@pytest.mark.asyncio
async def test_get_buying_power_maps_nrcvb_buy_amt(monkeypatch):
    captured = {}

    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        captured["req"] = request
        return SimpleNamespace(output=SimpleNamespace(nrcvb_buy_amt="1500000"))

    monkeypatch.setattr(account_mod, "call", fake_call)
    broker = _broker()
    await broker.open()
    try:
        bp = await KisAccountClient(broker).get_buying_power()
    finally:
        await broker.close()

    assert bp == Money(amount=Decimal("1500000"), currency=Currency.KRW)
    assert captured["req"].CANO == "12345678"
    assert captured["req"].ACNT_PRDT_CD == "01"


@pytest.mark.asyncio
async def test_get_buying_power_non_krw_unsupported(monkeypatch):
    from tooja.core.errors import UnsupportedOperation

    broker = _broker()
    await broker.open()
    try:
        with pytest.raises(UnsupportedOperation):
            await KisAccountClient(broker).get_buying_power(currency=Currency.USD)
    finally:
        await broker.close()


@pytest.mark.asyncio
async def test_get_sellable_quantity_single_object_output1(monkeypatch):
    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        assert request.PDNO == "005930"
        return SimpleNamespace(output1=SimpleNamespace(ord_psbl_qty="42"))

    monkeypatch.setattr(account_mod, "call", fake_call)
    broker = _broker()
    await broker.open()
    try:
        qty = await KisAccountClient(broker).get_sellable_quantity("005930")
    finally:
        await broker.close()
    assert qty == Decimal("42")


@pytest.mark.asyncio
async def test_get_sellable_quantity_list_output1(monkeypatch):
    async def fake_call(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        return SimpleNamespace(output1=[SimpleNamespace(ord_psbl_qty="7")])

    monkeypatch.setattr(account_mod, "call", fake_call)
    broker = _broker()
    await broker.open()
    try:
        qty = await KisAccountClient(broker).get_sellable_quantity("000660")
    finally:
        await broker.close()
    assert qty == Decimal("7")
