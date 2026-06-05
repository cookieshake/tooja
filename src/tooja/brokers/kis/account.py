"""KIS Account subclient — balance / positions via inquire-balance."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import balance_from_inquire, position_from_balance_row
from tooja.brokers.kis.raw.domestic_stock_trading.inquire_balance import (
    InquireBalanceExecutor,
    InquireBalanceRequest,
)
from tooja.core.clients import AccountClient
from tooja.core.models import Balance, Position, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


class KisAccountClient(AccountClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def get_balance(self) -> Balance:
        rows, summaries = await self._iterate_balance()
        return balance_from_inquire(rows, summaries, raw={"page_count": len(rows)})

    async def get_positions(self) -> list[Position]:
        rows, _ = await self._iterate_balance()
        return [p for p in (position_from_balance_row(r) for r in rows) if p is not None]

    async def get_position(self, symbol: Symbol | str) -> Position | None:
        sym = _as_symbol(symbol)
        for p in await self.get_positions():
            if p.symbol.ticker == sym.ticker:
                return p
        return None

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
