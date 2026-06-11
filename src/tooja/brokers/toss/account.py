"""Toss Account subclient — balance / positions / buying_power / sellable_quantity."""

from __future__ import annotations

import asyncio
from decimal import Decimal
from typing import TYPE_CHECKING

from tooja.brokers.toss._call import call
from tooja.brokers.toss._mappers import balance_from_holdings, position_from_holding, to_currency
from tooja.brokers.toss.raw.asset.get_holdings import GetHoldingsExecutor
from tooja.brokers.toss.raw.order_info.get_buying_power import GetBuyingPowerExecutor
from tooja.brokers.toss.raw.order_info.get_sellable_quantity import GetSellableQuantityExecutor
from tooja.core.clients import AccountClient
from tooja.core.enums import Currency
from tooja.core.models import Balance, Position, Symbol
from tooja.core.money import Money

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker


def _as_symbol(symbol: Symbol | str) -> Symbol:
    return Symbol.parse(symbol) if isinstance(symbol, str) else symbol


def _ticker(symbol: Symbol | str) -> str:
    return _as_symbol(symbol).ticker


class TossAccountClient(AccountClient):
    _broker_name = "toss"

    def __init__(self, broker: "TossBroker") -> None:
        self._broker = broker

    # ------------------------------------------------------------------
    # get_balance
    # ------------------------------------------------------------------

    async def get_balance(self) -> Balance:
        resp = await call(self._broker, GetHoldingsExecutor)
        # Query every currency Toss supports, not just the ones with holdings:
        # USD cash held with no US position (just exchanged, or fully exited a
        # US sleeve) must still surface, otherwise a USD-sleeve rebalancer reads
        # zero cash and can never bootstrap. Union in any holdings currency so a
        # future third currency is picked up automatically.
        currencies = {Currency.KRW, Currency.USD}
        currencies.update(
            to_currency(i.currency) for i in resp.items if i.currency is not None
        )
        cash = await asyncio.gather(
            *(self.get_buying_power(currency=c) for c in currencies)
        )
        return balance_from_holdings(resp, cash=list(cash))

    # ------------------------------------------------------------------
    # get_positions
    # ------------------------------------------------------------------

    async def get_positions(self) -> list[Position]:
        resp = await call(self._broker, GetHoldingsExecutor)
        return [position_from_holding(i) for i in resp.items]

    # ------------------------------------------------------------------
    # get_position
    # ------------------------------------------------------------------

    async def get_position(self, symbol: Symbol | str) -> Position | None:
        ticker = _ticker(symbol)
        resp = await call(self._broker, GetHoldingsExecutor, query={"symbol": ticker})
        if not resp.items:
            return None
        return position_from_holding(resp.items[0])

    # ------------------------------------------------------------------
    # get_buying_power
    # ------------------------------------------------------------------

    async def get_buying_power(self, *, currency: Currency = Currency.KRW) -> Money:
        resp = await call(
            self._broker,
            GetBuyingPowerExecutor,
            query={"currency": currency.value},
        )
        amount = resp.cash_buying_power if resp.cash_buying_power is not None else Decimal(0)
        return Money(amount=amount, currency=currency)

    # ------------------------------------------------------------------
    # get_sellable_quantity
    # ------------------------------------------------------------------

    async def get_sellable_quantity(self, symbol: Symbol | str) -> Decimal:
        ticker = _ticker(symbol)
        resp = await call(
            self._broker,
            GetSellableQuantityExecutor,
            query={"symbol": ticker},
        )
        return resp.sellable_quantity if resp.sellable_quantity is not None else Decimal(0)
