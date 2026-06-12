from tooja.core.enums import Currency, Exchange
from tooja.core.markets import currency_of


def test_currency_of_known_exchanges():
    assert currency_of(Exchange.KRX) == Currency.KRW
    assert currency_of(Exchange.NXT) == Currency.KRW
    assert currency_of(Exchange.NASD) == Currency.USD
    assert currency_of(Exchange.NYSE) == Currency.USD
    assert currency_of(Exchange.AMEX) == Currency.USD
    assert currency_of(Exchange.SEHK) == Currency.HKD
    assert currency_of(Exchange.SHAA) == Currency.CNY
    assert currency_of(Exchange.SZAA) == Currency.CNY
    assert currency_of(Exchange.TKSE) == Currency.JPY
    assert currency_of(Exchange.HASE) == Currency.VND
    assert currency_of(Exchange.VNSE) == Currency.VND


def test_currency_of_is_total_over_exchange_enum():
    # Guards against an Exchange being added without a currency mapping.
    for ex in Exchange:
        assert isinstance(currency_of(ex), Currency)
