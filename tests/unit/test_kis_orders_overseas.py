"""KIS overseas order routing: TR matrix, create/cancel/replace, queries."""

from __future__ import annotations

import pytest

from tooja.brokers.kis import orders as orders_mod
from tooja.core.enums import Exchange, OrderSide

US = (Exchange.NASD, Exchange.NYSE, Exchange.AMEX)


@pytest.mark.parametrize("exchange", US)
def test_us_order_tr_ids(exchange):
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, False) == "TTTT1002U"
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, False) == "TTTT1006U"
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, True) == "VTTT1002U"
    # KIS asymmetry: US demo sell is VTTT1001U, NOT VTTT1006U.
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, True) == "VTTT1001U"


@pytest.mark.parametrize(
    ("exchange", "buy_real", "sell_real"),
    [
        (Exchange.TKSE, "TTTS0308U", "TTTS0307U"),
        (Exchange.SHAA, "TTTS0202U", "TTTS1005U"),
        (Exchange.SEHK, "TTTS1002U", "TTTS1001U"),
        (Exchange.SZAA, "TTTS0305U", "TTTS0304U"),
        (Exchange.HASE, "TTTS0311U", "TTTS0310U"),
        (Exchange.VNSE, "TTTS0311U", "TTTS0310U"),
    ],
)
def test_asia_order_tr_ids(exchange, buy_real, sell_real):
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, False) == buy_real
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, False) == sell_real
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.BUY, True) == "V" + buy_real[1:]
    assert orders_mod._ovrs_order_tr_id(exchange, OrderSide.SELL, True) == "V" + sell_real[1:]


@pytest.mark.parametrize(
    ("exchange", "real"),
    [
        (Exchange.NASD, "TTTT1004U"), (Exchange.NYSE, "TTTT1004U"),
        (Exchange.AMEX, "TTTT1004U"), (Exchange.SEHK, "TTTS1003U"),
        (Exchange.TKSE, "TTTS0309U"), (Exchange.SHAA, "TTTS0302U"),
        (Exchange.SZAA, "TTTS0306U"), (Exchange.HASE, "TTTS0312U"),
        (Exchange.VNSE, "TTTS0312U"),
    ],
)
def test_rvsecncl_tr_ids(exchange, real):
    assert orders_mod._ovrs_rvsecncl_tr_id(exchange, False) == real
    assert orders_mod._ovrs_rvsecncl_tr_id(exchange, True) == "V" + real[1:]


def test_is_overseas_predicate():
    assert not orders_mod._is_overseas(Exchange.KRX)
    assert not orders_mod._is_overseas(Exchange.NXT)
    for ex in (Exchange.NASD, Exchange.NYSE, Exchange.AMEX, Exchange.SEHK,
               Exchange.SHAA, Exchange.SZAA, Exchange.TKSE, Exchange.HASE,
               Exchange.VNSE):
        assert orders_mod._is_overseas(ex)
