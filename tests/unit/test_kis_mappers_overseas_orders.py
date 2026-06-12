"""order/fill mappers for overseas inquire-ccnl rows."""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest

from tooja.brokers.kis._mappers import (
    fill_from_ovrs_ccnl_row,
    order_from_ovrs_ccnl_row,
)
from tooja.core.enums import Currency, Exchange, OrderSide, OrderStatus


def _row(**over):
    base = dict(
        ord_dt="20260611", odno="0030089601", orgn_odno=None,
        sll_buy_dvsn_cd="02", rvse_cncl_dvsn=None,
        pdno="AAPL", ft_ord_qty="5", ft_ord_unpr3="145.00",
        ft_ccld_qty="0", ft_ccld_unpr3="0", nccs_qty="5",
        prcs_stat_name="완료", rjct_rson="", ord_tmd="221500",
        ovrs_excg_cd="NASD", tr_crcy_cd="USD",
        dmst_ord_dt="20260612", thco_ord_tmd="071500",
    )
    base.update(over)
    return SimpleNamespace(**base)


def test_open_buy_order_maps():
    o = order_from_ovrs_ccnl_row(_row(), {"k": "v"})
    assert o.order_id == "0030089601"
    assert o.symbol.exchange is Exchange.NASD
    assert o.symbol.ticker == "AAPL"
    assert o.side is OrderSide.BUY
    assert o.qty == Decimal(5)
    assert o.filled_qty == Decimal(0)
    assert o.status is OrderStatus.OPEN
    assert o.price.currency is Currency.USD
    assert o.price.amount == Decimal("145.00")
    assert o.raw == {"k": "v"}


def test_partial_fill_status():
    o = order_from_ovrs_ccnl_row(
        _row(ft_ccld_qty="2", ft_ccld_unpr3="144.90", nccs_qty="3"), {},
    )
    assert o.status is OrderStatus.PARTIALLY_FILLED
    assert o.filled_qty == Decimal(2)
    assert o.avg_fill_price.amount == Decimal("144.90")


def test_filled_and_cancelled_and_rejected_status():
    filled = order_from_ovrs_ccnl_row(
        _row(ft_ccld_qty="5", ft_ccld_unpr3="144.90", nccs_qty="0"), {},
    )
    assert filled.status is OrderStatus.FILLED
    cancelled = order_from_ovrs_ccnl_row(_row(rvse_cncl_dvsn="02"), {})
    assert cancelled.status is OrderStatus.CANCELLED
    rejected = order_from_ovrs_ccnl_row(_row(prcs_stat_name="거부"), {})
    assert rejected.status is OrderStatus.REJECTED


def test_sell_side_maps():
    o = order_from_ovrs_ccnl_row(_row(sll_buy_dvsn_cd="01"), {})
    assert o.side is OrderSide.SELL


def test_unmapped_exchange_raises():
    with pytest.raises(ValueError, match="exchange"):
        order_from_ovrs_ccnl_row(_row(ovrs_excg_cd="XXXX"), {})


def test_unmapped_currency_raises():
    with pytest.raises(ValueError, match="currency"):
        order_from_ovrs_ccnl_row(_row(tr_crcy_cd="XYZ"), {})


def test_missing_key_fields_return_none():
    assert order_from_ovrs_ccnl_row(_row(odno=None), {}) is None
    assert order_from_ovrs_ccnl_row(_row(pdno=""), {}) is None


def test_fill_mapper_requires_filled_qty():
    assert fill_from_ovrs_ccnl_row(_row(), {}) is None   # ft_ccld_qty == 0
    f = fill_from_ovrs_ccnl_row(
        _row(ft_ccld_qty="2", ft_ccld_unpr3="144.90"), {"r": 1},
    )
    assert f.order_id == "0030089601"
    assert f.qty == Decimal(2)
    assert f.price.amount == Decimal("144.90")
    assert f.price.currency is Currency.USD
    assert f.side is OrderSide.BUY
    assert f.raw == {"r": 1}
