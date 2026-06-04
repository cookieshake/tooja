"""KIS Orders subclient.

POLICY: order POST endpoints (create/cancel/replace) are ALWAYS dry-run.
The raw payload is built and validated, then returned as an Order with
status=PENDING and order_id="DRY-<uuid>"; no HTTP POST is sent to KIS.

Inquiries (get / list / fills) are real reads.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, AsyncIterator, Literal

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    fill_from_daily_ccld_row,
    kis_ord_dvsn,
    order_from_daily_ccld_row,
)
from tooja.brokers.kis.raw.domestic_stock_trading.inquire_daily_ccld import (
    InquireDailyCcldExecutor,
    InquireDailyCcldRequest,
)
from tooja.core.clients import OrdersClient
from tooja.core.enums import OrderSide, OrderStatus, TimeInForce
from tooja.core.errors import OrderNotFound
from tooja.core.models import Fill, Order, OrderRequest, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


_DRY_RUN_PREFIX = "DRY-"


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


def _yyyymmdd(d: date | datetime) -> str:
    if isinstance(d, datetime):
        d = d.date()
    return d.strftime("%Y%m%d")


class KisOrdersClient(OrdersClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def create(self, req: OrderRequest) -> Order:
        """Dry-run order creation — builds the KIS payload but does not POST it."""
        self._broker._require_open()
        sym = _as_symbol(req.symbol)
        creds = self._broker.credentials
        ord_dvsn = kis_ord_dvsn(req.type)
        price = getattr(req, "price", None)
        ord_unpr = str(price.amount) if price is not None else "0"
        payload = {
            "CANO": creds.cano,
            "ACNT_PRDT_CD": creds.acnt_prdt_cd,
            "PDNO": sym.ticker,
            "ORD_DVSN": ord_dvsn,
            "ORD_QTY": str(req.qty),
            "ORD_UNPR": ord_unpr,
        }
        order_id = f"{_DRY_RUN_PREFIX}{uuid.uuid4().hex[:12]}"
        return Order(
            order_id=order_id,
            symbol=sym,
            side=req.side,
            qty=req.qty,
            filled_qty=Decimal(0),
            avg_fill_price=None,
            type=req.type,
            price=price,
            stop_price=getattr(req, "stop_price", None),
            status=OrderStatus.PENDING,
            time_in_force=getattr(req, "time_in_force", TimeInForce.DAY),
            client_order_id=req.client_order_id,
            submitted_at=datetime.now(timezone.utc),
            raw={"dry_run": True, "payload": payload},
        )

    async def cancel(self, order_id: str) -> Order:
        """Dry-run cancel."""
        if not order_id.startswith(_DRY_RUN_PREFIX):
            existing = await self.get(order_id)
            return existing.model_copy(update={
                "status": OrderStatus.CANCELLED,
                "raw": {**existing.raw, "dry_run_cancel": True},
            })
        return Order(
            order_id=order_id,
            symbol=Symbol(ticker="000000"),
            side=OrderSide.BUY, qty=Decimal(0),
            type="market",
            status=OrderStatus.CANCELLED,
            submitted_at=datetime.now(timezone.utc),
            raw={"dry_run": True},
        )

    async def replace(
        self,
        order_id: str,
        *,
        qty: Decimal | None = None,
        price: Decimal | None = None,
    ) -> Order:
        """Dry-run replace — looks up the existing order, applies overrides."""
        existing = await self.get(order_id)
        updates: dict = {}
        if qty is not None:
            updates["qty"] = qty
        if price is not None:
            from tooja.core.enums import Currency
            from tooja.core.money import Money
            updates["price"] = Money(amount=price, currency=Currency.KRW)
        updates["raw"] = {**existing.raw, "dry_run_replace": True}
        return existing.model_copy(update=updates)

    async def get(self, order_id: str) -> Order:
        for o in await self.list_orders(status="all"):
            if o.order_id == order_id:
                return o
        raise OrderNotFound(
            f"Order not found: {order_id}", broker="kis",
        )

    async def list_orders(
        self,
        *,
        status: Literal["all", "open", "closed"] = "all",
        symbol: Symbol | str | None = None,
        since: date | datetime | None = None,
        until: date | datetime | None = None,
    ) -> list[Order]:
        rows = await self._iter_ccld(
            symbol=symbol, since=since, until=until, status=status, only_filled=False,
        )
        out: list[Order] = []
        for row in rows:
            order = order_from_daily_ccld_row(row, row.model_dump())
            if order is None:
                continue
            if status == "open" and order.status not in (
                OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED, OrderStatus.PENDING,
            ):
                continue
            if status == "closed" and order.status not in (
                OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED,
            ):
                continue
            out.append(order)
        return out

    async def iter_orders(self, **kwargs) -> AsyncIterator[Order]:
        for o in await self.list_orders(**kwargs):
            yield o

    async def list_fills(
        self,
        *,
        symbol: Symbol | str | None = None,
        since: date | datetime | None = None,
        until: date | datetime | None = None,
    ) -> list[Fill]:
        rows = await self._iter_ccld(
            symbol=symbol, since=since, until=until, status="closed", only_filled=True,
        )
        out: list[Fill] = []
        for row in rows:
            f = fill_from_daily_ccld_row(row, row.model_dump())
            if f is not None:
                out.append(f)
        return out

    async def iter_fills(self, **kwargs) -> AsyncIterator[Fill]:
        for f in await self.list_fills(**kwargs):
            yield f

    async def _iter_ccld(
        self,
        *,
        symbol: Symbol | str | None,
        since: date | datetime | None,
        until: date | datetime | None,
        status: str,
        only_filled: bool,
    ) -> list:
        creds = self._broker.credentials
        today = date.today()
        end_d = _yyyymmdd(until) if until else _yyyymmdd(today)
        start_d = _yyyymmdd(since) if since else _yyyymmdd(today)
        pdno = _as_symbol(symbol).ticker if symbol else None
        ccld_dvsn = "01" if only_filled else ("02" if status == "open" else "00")

        req = InquireDailyCcldRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            INQR_STRT_DT=start_d,
            INQR_END_DT=end_d,
            SLL_BUY_DVSN_CD="00",
            PDNO=pdno,
            ORD_GNO_BRNO="",
            ODNO="",
            CCLD_DVSN=ccld_dvsn,
            INQR_DVSN="00",
            INQR_DVSN_1="",
            INQR_DVSN_3="00",
            EXCG_ID_DVSN_CD="KRX",
            CTX_AREA_FK100="",
            CTX_AREA_NK100="",
        )

        all_rows: list = []
        tr_cont = ""
        guard = 0
        while True:
            extra = {"tr_cont": tr_cont} if tr_cont else None
            resp = await call(
                self._broker, InquireDailyCcldExecutor, req, extra_headers=extra,
            )
            all_rows.extend(getattr(resp, "output1", []) or [])
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
        return all_rows
