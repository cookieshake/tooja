"""KIS Account subclient — balance / positions via inquire-balance."""

from __future__ import annotations

import asyncio
from decimal import Decimal
from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    _dec,
    balance_from_inquire,
    balance_from_present_balance,
    merge_balances,
    position_from_balance_row,
)
from tooja.brokers.kis.raw.domestic_stock_trading.inquire_balance import (
    InquireBalanceExecutor,
    InquireBalanceRequest,
)
from tooja.brokers.kis.raw.overseas_stock_trading.inquire_present_balance import (
    InquirePresentBalanceExecutor,
    InquirePresentBalanceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_trading.inquire_psbl_order import (
    InquirePsblOrderExecutor,
    InquirePsblOrderRequest,
)
from tooja.brokers.kis.raw.domestic_stock_trading.inquire_psbl_sell import (
    InquirePsblSellExecutor,
    InquirePsblSellRequest,
)
from tooja.core.clients import AccountClient
from tooja.core.enums import Currency
from tooja.core.errors import PermissionDenied, UnsupportedOperation
from tooja.core.models import Balance, Position, Symbol
from tooja.core.money import Money

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


class KisAccountClient(AccountClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def get_balance(self) -> Balance:
        # No return_exceptions=True on purpose: an overseas-call failure must
        # propagate, not silently degrade to a domestic-only balance (which would
        # make a foreign-currency sleeve read "no cash" and mis-trade).
        domestic, overseas = await asyncio.gather(
            self._domestic_balance(),
            self._overseas_balance(),
        )
        return merge_balances(domestic, overseas)

    async def _domestic_balance(self) -> Balance:
        rows, summaries = await self._iterate_balance()
        return balance_from_inquire(rows, summaries, raw={"page_count": len(rows)})

    async def _overseas_balance(self) -> Balance:
        """Single-call overseas snapshot (no pagination; NATN_CD=000 = all)."""
        creds = self._broker.credentials
        req = InquirePresentBalanceRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            WCRC_FRCR_DVSN_CD="02",  # 외화
            NATN_CD="000",           # 전체 국가
            TR_MKET_CD="00",         # 전체 시장
            INQR_DVSN_CD="00",       # 전체
        )
        try:
            resp = await call(self._broker, InquirePresentBalanceExecutor, req)
        except PermissionDenied:
            # The overseas-stock service is not enrolled on this account. That is
            # a permanent account-config state, not a transient outage, so we
            # degrade to a domestic-only balance instead of failing get_balance
            # outright (which would break pure-KRW callers). Every OTHER failure
            # still propagates — see the comment in get_balance.
            return Balance(raw={"overseas_skipped": "permission_denied"})
        return balance_from_present_balance(resp)

    async def get_positions(self) -> list[Position]:
        rows, _ = await self._iterate_balance()
        return [p for p in (position_from_balance_row(r) for r in rows) if p is not None]

    async def get_position(self, symbol: Symbol | str) -> Position | None:
        sym = _as_symbol(symbol)
        for p in await self.get_positions():
            if p.symbol.ticker == sym.ticker:
                return p
        return None

    async def get_buying_power(self, *, currency: Currency = Currency.KRW) -> Money:
        if currency != Currency.KRW:
            raise UnsupportedOperation(
                f"KIS account.get_buying_power supports KRW only (got {currency})",
                broker="kis",
            )
        creds = self._broker.credentials
        req = InquirePsblOrderRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            PDNO="",
            ORD_UNPR="",
            ORD_DVSN="01",
            CMA_EVLU_AMT_ICLD_YN="N",
            OVRS_ICLD_YN="N",
        )
        resp = await call(self._broker, InquirePsblOrderExecutor, req)
        out = getattr(resp, "output", None)
        amt = _dec(getattr(out, "nrcvb_buy_amt", None)) if out is not None else None
        if amt is None:
            raise UnsupportedOperation(
                "KIS inquire-psbl-order returned no buying power", broker="kis",
            )
        return Money(amount=amt, currency=Currency.KRW)

    async def get_sellable_quantity(self, symbol: Symbol | str) -> Decimal:
        sym = _as_symbol(symbol)
        creds = self._broker.credentials
        req = InquirePsblSellRequest(
            CANO=creds.cano, ACNT_PRDT_CD=creds.acnt_prdt_cd, PDNO=sym.ticker,
        )
        resp = await call(self._broker, InquirePsblSellExecutor, req)
        out1 = getattr(resp, "output1", None)
        if out1 is None:
            return Decimal(0)
        item = out1[0] if isinstance(out1, list) else out1
        if item is None:
            return Decimal(0)
        qty = _dec(getattr(item, "ord_psbl_qty", None))
        return qty if qty is not None else Decimal(0)

    async def _iterate_balance(self) -> tuple[list, list]:
        """Walk all CTX_AREA_NK100 pages and return concatenated output1/output2."""
        creds = self._broker.credentials
        req = InquireBalanceRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            AFHR_FLPR_YN="N",
            OFL_YN="",  # KIS rejects with INPUT_FIELD_NAME OFL_YN if omitted.
            INQR_DVSN="02",
            UNPR_DVSN="01",
            FUND_STTL_ICLD_YN="N",
            FNCG_AMT_AUTO_RDPT_YN="N",
            PRCS_DVSN="01",
            CTX_AREA_FK100="",
            CTX_AREA_NK100="",
        )

        output1: list = []
        output2: list = []
        tr_cont = ""
        guard = 0
        while True:
            extra = {"tr_cont": tr_cont} if tr_cont else None
            resp = await call(
                self._broker, InquireBalanceExecutor, req, extra_headers=extra,
            )
            output1.extend(getattr(resp, "output1", []) or [])
            output2.extend(getattr(resp, "output2", []) or [])

            hdr = getattr(resp, "headers", None)
            nxt = getattr(hdr, "tr_cont", None) if hdr else None
            if nxt not in ("F", "M"):
                break
            req = req.model_copy(update={
                "CTX_AREA_FK100": getattr(resp, "ctx_area_fk100", "") or "",
                "CTX_AREA_NK100": getattr(resp, "ctx_area_nk100", "") or "",
            })
            tr_cont = "N"
            guard += 1
            if guard > 50:
                break
        return output1, output2
