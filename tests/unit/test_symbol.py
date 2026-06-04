import pytest
from pydantic import ValidationError

from tooja.core.enums import AssetClass, Exchange
from tooja.core.models import Symbol


def test_construct_with_defaults():
    s = Symbol(ticker="005930")
    assert s.ticker == "005930"
    assert s.exchange == Exchange.KRX
    assert s.asset == AssetClass.STOCK


def test_str_repr():
    assert str(Symbol(ticker="005930")) == "KRX:005930"
    assert str(Symbol(ticker="AAPL", exchange=Exchange.NASD)) == "NASD:AAPL"


def test_frozen():
    s = Symbol(ticker="005930")
    with pytest.raises(ValidationError):
        s.ticker = "035720"  # frozen — immutable


def test_hashable_dict_key():
    a = Symbol(ticker="005930")
    b = Symbol(ticker="005930")
    d = {a: 1}
    assert d[b] == 1  # Equal values hash equally.


def test_parse_bare_ticker():
    s = Symbol.parse("005930")
    assert s == Symbol(ticker="005930", exchange=Exchange.KRX, asset=AssetClass.STOCK)


def test_parse_exchange_ticker():
    s = Symbol.parse("KRX:005930")
    assert s == Symbol(ticker="005930", exchange=Exchange.KRX)

    s = Symbol.parse("NASD:AAPL")
    assert s == Symbol(ticker="AAPL", exchange=Exchange.NASD)


def test_parse_exchange_asset_ticker():
    s = Symbol.parse("KRX:FUTOP:101W12000")
    assert s == Symbol(
        ticker="101W12000",
        exchange=Exchange.KRX,
        asset=AssetClass.FUTURES_OPTIONS,
    )


def test_parse_invalid_exchange():
    with pytest.raises(ValueError, match="exchange"):
        Symbol.parse("WTF:005930")


def test_parse_invalid_asset():
    with pytest.raises(ValueError, match="asset"):
        Symbol.parse("KRX:NOTANASSET:005930")


def test_empty_ticker_rejected():
    with pytest.raises(ValidationError):
        Symbol(ticker="")


def test_parse_empty_string_rejected():
    with pytest.raises(ValidationError):
        Symbol.parse("")


def test_parse_trailing_colon_rejected():
    # "KRX:" splits into ["KRX", ""] -> empty ticker
    with pytest.raises(ValidationError):
        Symbol.parse("KRX:")


def test_parse_case_normalization():
    # exchange uppercased, asset lowercased
    assert Symbol.parse("krx:005930") == Symbol(ticker="005930", exchange=Exchange.KRX)
    assert Symbol.parse("nasd:aapl") == Symbol(ticker="aapl", exchange=Exchange.NASD)
    assert Symbol.parse("KRX:futop:101W12000") == Symbol.parse("KRX:FUTOP:101W12000")


def test_parse_strips_whitespace_around_parts():
    expected = Symbol(ticker="005930", exchange=Exchange.KRX)
    assert Symbol.parse(" KRX:005930 ") == expected
    assert Symbol.parse("KRX : 005930") == expected
    assert Symbol.parse(" 005930 ") == expected


def test_parse_strips_whitespace_in_three_part():
    assert Symbol.parse(" KRX : FUTOP : 101W12000 ") == Symbol(
        ticker="101W12000",
        exchange=Exchange.KRX,
        asset=AssetClass.FUTURES_OPTIONS,
    )
