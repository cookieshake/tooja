"""Spot-checks on the generated Toss raw layer: executor metadata + model parsing
against the OpenAPI examples. Guards generator correctness."""

from __future__ import annotations

import importlib
import pkgutil
from decimal import Decimal

import tooja.brokers.toss.raw as raw_pkg


def test_all_generated_modules_import():
    mods = [m.name for m in pkgutil.walk_packages(raw_pkg.__path__, raw_pkg.__name__ + ".")]
    for name in mods:
        importlib.import_module(name)
    assert any(".market_data." in m for m in mods)
    assert any(".order." in m for m in mods)


def test_get_prices_executor_metadata():
    from tooja.brokers.toss.raw.market_data.get_prices import GetPricesExecutor

    assert GetPricesExecutor.PATH == "/api/v1/prices"
    assert GetPricesExecutor.METHOD == "GET"
    assert "symbols" in GetPricesExecutor.QUERY_PARAMS
    assert GetPricesExecutor.ENVELOPED is True


def test_create_order_executor_metadata():
    from tooja.brokers.toss.raw.order.create_order import CreateOrderExecutor

    assert CreateOrderExecutor.PATH == "/api/v1/orders"
    assert CreateOrderExecutor.METHOD == "POST"
    assert CreateOrderExecutor.BODY_CONTENT == "json"
    assert "X-Tossinvest-Account" in CreateOrderExecutor.HEADER_PARAMS


def test_get_order_executor_has_path_param():
    from tooja.brokers.toss.raw.order_history.get_order import GetOrderExecutor

    assert GetOrderExecutor.PATH == "/api/v1/orders/{orderId}"
    assert "orderId" in GetOrderExecutor.PATH_PARAMS


def test_token_executor_not_enveloped_and_form_body():
    from tooja.brokers.toss.raw.auth.issue_o_auth2_token import IssueOAuth2TokenExecutor as T

    assert T.PATH == "/oauth2/token"
    assert T.METHOD == "POST"
    assert T.ENVELOPED is False
    assert T.BODY_CONTENT == "form"


def test_price_response_model_parses_decimal_and_nullable():
    from tooja.brokers.toss.raw.models import PriceResponse

    p = PriceResponse(symbol="005930", lastPrice="72000", currency="KRW", timestamp=None)
    assert p.symbol == "005930"
    assert p.last_price == Decimal("72000")
    assert p.timestamp is None


def test_stock_info_nested_and_enum_forward_compat():
    from tooja.brokers.toss.raw.models import StockInfo

    s = StockInfo(
        symbol="005930", name="삼성전자", englishName="SamsungElec",
        isinCode="KR7005930003", market="KOSPI", securityType="STOCK",
        isCommonShare=True, status="ACTIVE", currency="KRW",
        sharesOutstanding="5919637922", listDate=None, delistDate=None,
        leverageFactor=None, koreanMarketDetail=None,
    )
    assert s.market == "KOSPI"
    assert s.shares_outstanding == Decimal("5919637922")
    # unknown enum value must not hard-fail (forward-compat: enums are str)
    s2 = StockInfo(
        symbol="X", name="n", englishName="e", isinCode="i",
        market="SOME_FUTURE_MARKET", securityType="STOCK", isCommonShare=True,
        status="ACTIVE", currency="KRW", sharesOutstanding="1",
    )
    assert s2.market == "SOME_FUTURE_MARKET"
