"""KIS Analytics subclient — investor flows.

program_trading / short_selling / margin_balance / securities_lending are not
mapped here: KIS exposes per-day single-symbol endpoints that don't share a
field schema with each other. They're reachable via `broker.raw.*` until
specific use cases materialize.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import investor_flow_from_row
from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_investor import (
    InquireInvestorExecutor,
    InquireInvestorRequest,
)
from tooja.core.clients import AnalyticsClient
from tooja.core.models import InvestorFlow, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


class KisAnalyticsClient(AnalyticsClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def investor_flows(
        self,
        symbol: Symbol | str,
        *,
        since: date,
        until: date,
    ) -> list[InvestorFlow]:
        sym = _as_symbol(symbol)
        req = InquireInvestorRequest(
            FID_COND_MRKT_DIV_CODE="J", FID_INPUT_ISCD=sym.ticker,
        )
        resp = await call(self._broker, InquireInvestorExecutor, req)
        out: list[InvestorFlow] = []
        for row in getattr(resp, "output", []) or []:
            f = investor_flow_from_row(sym, row, row.model_dump())
            if f is not None and since <= f.date <= until:
                out.append(f)
        out.sort(key=lambda x: x.date)
        return out
