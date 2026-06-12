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


def _make_kis_account(monkeypatch, domestic, overseas):
    client = KisAccountClient.__new__(KisAccountClient)
    client._broker = object()

    async def fake_iterate(self):
        return domestic  # (output1, output2) tuple

    async def fake_overseas(self):
        return overseas  # a Balance

    monkeypatch.setattr(KisAccountClient, "_iterate_balance", fake_iterate)
    monkeypatch.setattr(KisAccountClient, "_overseas_balance", fake_overseas)
    return client


@pytest.mark.asyncio
async def test_get_balance_merges_domestic_and_overseas(monkeypatch):
    from tooja.core.models import Balance

    class _Out2:
        dnca_tot_amt = "500000"
        tot_evlu_amt = "1000000"

    overseas = Balance(
        total_asset=Money(amount=Decimal("5000000"), currency=Currency.KRW),
        cash=[Money(amount=Decimal("2000"), currency=Currency.USD)],
        positions=[],
    )
    client = _make_kis_account(monkeypatch, domestic=([], [_Out2()]), overseas=overseas)

    bal = await client.get_balance()
    by_ccy = {m.currency: m.amount for m in bal.cash}
    assert by_ccy[Currency.KRW] == Decimal("500000")
    assert by_ccy[Currency.USD] == Decimal("2000")
    assert bal.total_asset.amount == Decimal("6000000")  # 1,000,000 + 5,000,000


@pytest.mark.asyncio
async def test_get_balance_propagates_overseas_failure(monkeypatch):
    async def fake_iterate(self):
        return ([], [])

    async def boom(self):
        raise RuntimeError("overseas down")

    monkeypatch.setattr(KisAccountClient, "_iterate_balance", fake_iterate)
    monkeypatch.setattr(KisAccountClient, "_overseas_balance", boom)

    client = KisAccountClient.__new__(KisAccountClient)
    client._broker = object()
    with pytest.raises(RuntimeError, match="overseas down"):
        await client.get_balance()


@pytest.mark.asyncio
async def test_overseas_balance_degrades_when_not_enrolled(monkeypatch):
    """A not-enrolled overseas service (PermissionDenied) degrades, not fails."""
    from tooja.core.errors import PermissionDenied
    from tooja.core.models import Balance

    async def denied(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        raise PermissionDenied("overseas service not enrolled", broker="kis")

    monkeypatch.setattr(account_mod, "call", denied)
    broker = _broker()
    await broker.open()
    try:
        bal = await KisAccountClient(broker)._overseas_balance()
    finally:
        await broker.close()

    assert isinstance(bal, Balance)
    assert bal.cash == []
    assert bal.positions == []
    assert bal.raw == {"overseas_skipped": "permission_denied"}


@pytest.mark.asyncio
async def test_get_balance_degrades_to_domestic_when_overseas_not_enrolled(monkeypatch):
    """End-to-end: PermissionDenied overseas yields a domestic-only balance."""
    async def fake_iterate(self):
        class _Out2:
            dnca_tot_amt = "500000"
            tot_evlu_amt = "1000000"
        return ([], [_Out2()])

    async def denied(broker, executor_cls, request, *, tr_id=None, extra_headers=None):
        from tooja.core.errors import PermissionDenied
        raise PermissionDenied("overseas service not enrolled", broker="kis")

    monkeypatch.setattr(KisAccountClient, "_iterate_balance", fake_iterate)
    monkeypatch.setattr(account_mod, "call", denied)

    broker = _broker()
    await broker.open()
    try:
        bal = await KisAccountClient(broker).get_balance()
    finally:
        await broker.close()

    by_ccy = {m.currency: m.amount for m in bal.cash}
    assert by_ccy[Currency.KRW] == Decimal("500000")
    assert Currency.USD not in by_ccy  # overseas skipped
    assert bal.total_asset.amount == Decimal("1000000")  # domestic only


@pytest.mark.asyncio
async def test_get_positions_includes_overseas(monkeypatch):
    from tooja.core.enums import Exchange  # noqa: F401 — exchange asserted via Symbol
    from tooja.core.models import Balance, Position, Symbol

    krx_pos = Position(
        symbol=Symbol.parse("005930"), qty=Decimal(10),
        avg_price=Money(amount=Decimal(70000), currency=Currency.KRW),
    )
    us_pos = Position(
        symbol=Symbol.parse("NASD:AAPL"), qty=Decimal(2),
        avg_price=Money(amount=Decimal("145.00"), currency=Currency.USD),
    )

    async def fake_balance(self):
        return Balance(positions=[krx_pos, us_pos])

    monkeypatch.setattr(KisAccountClient, "get_balance", fake_balance)
    client = KisAccountClient(_broker())

    positions = await client.get_positions()
    assert positions == [krx_pos, us_pos]

    # Strict ticker+exchange matching.
    assert (await client.get_position("NASD:AAPL")) == us_pos
    assert (await client.get_position("005930")) == krx_pos
    assert (await client.get_position("AAPL")) is None  # bare → KRX, no match
