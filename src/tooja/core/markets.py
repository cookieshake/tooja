"""Market metadata shared across adapters.

The settlement currency of an exchange. Cash is pooled by currency (every
researched broker reports per-currency deposits with exchange as per-position
metadata), so this map is the single source of truth for which currency a
symbol's exchange settles in.
"""

from __future__ import annotations

from tooja.core.enums import Currency, Exchange

_EXCHANGE_CURRENCY: dict[Exchange, Currency] = {
    Exchange.KRX: Currency.KRW,
    Exchange.NXT: Currency.KRW,
    Exchange.NASD: Currency.USD,
    Exchange.NYSE: Currency.USD,
    Exchange.AMEX: Currency.USD,
    Exchange.SEHK: Currency.HKD,
    Exchange.SHAA: Currency.CNY,
    Exchange.SZAA: Currency.CNY,
    Exchange.TKSE: Currency.JPY,
    Exchange.HASE: Currency.VND,
    Exchange.VNSE: Currency.VND,
}


def currency_of(exchange: Exchange) -> Currency:
    """Settlement currency for an exchange.

    Raises KeyError for an unmapped exchange — a missing mapping is a
    programmer error (a new Exchange enum member), never silently defaulted.
    """
    try:
        return _EXCHANGE_CURRENCY[exchange]
    except KeyError as e:
        raise KeyError(f"no currency mapping for exchange {exchange!r}") from e
