from tooja.core.enums import (
    AssetClass,
    Currency,
    Exchange,
    FinancialPeriod,
    OrderSide,
    OrderStatus,
    RankingType,
    TimeInForce,
)


def test_exchange_members():
    assert Exchange.KRX.value == "KRX"
    assert Exchange.NASD.value == "NASD"
    assert Exchange.SEHK.value == "SEHK"
    # All 11 exchanges present.
    assert {e.value for e in Exchange} == {
        "KRX", "NXT", "NASD", "NYSE", "AMEX",
        "SEHK", "SHAA", "SZAA", "TKSE", "HASE", "VNSE",
    }


def test_asset_class_members():
    assert {a.value for a in AssetClass} == {"stock", "futop", "bond", "elw"}


def test_order_side_status_tif():
    assert OrderSide.BUY.value == "buy"
    assert OrderStatus.PARTIALLY_FILLED.value == "partial"
    assert TimeInForce.IOC.value == "IOC"
    assert TimeInForce.GTC.value == "GTC"  # Defined even though KIS does not support it.


def test_currency_members():
    assert {c.value for c in Currency} == {"KRW", "USD", "HKD", "CNY", "JPY", "VND"}


def test_financial_period_members():
    assert FinancialPeriod.QUARTERLY.value == "Q"
    assert FinancialPeriod.ANNUAL.value == "Y"


def test_ranking_type_count():
    # spec §4: 16 variants
    assert len(RankingType) == 16
    assert RankingType.MARKET_CAP.value == "market_cap"
    assert RankingType.FOREIGN_NET_BUY.value == "foreign_buy"
