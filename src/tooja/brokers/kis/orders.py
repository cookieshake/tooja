"""KIS Orders subclient — real POST to KIS.

env="demo" routes to KIS mock server (가짜 자금). env="real" routes to live
production server (실제 자금). The library does NOT add a dry-run flag; the
env selection is the entire safety boundary, matching ccxt/Alpaca/IB
convention.

Side -> TR_ID:
- BUY  : TTTC0012U (real) / VTTC0012U (demo)
- SELL : TTTC0011U (real) / VTTC0011U (demo)

cancel/replace: order-rvsecncl, RVSE_CNCL_DVSN_CD = 02 (cancel) / 01 (replace).
"""

from __future__ import annotations

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
from tooja.brokers.kis.raw.domestic_stock_trading.order_cash import (
    OrderCashExecutor,
    OrderCashRequest,
)
from tooja.brokers.kis.raw.domestic_stock_trading.order_rvsecncl import (
    OrderRvsecnclExecutor,
    OrderRvsecnclRequest,
)
from tooja.core.clients import OrdersClient
from tooja.core.enums import OrderSide, OrderStatus, TimeInForce
from tooja.core.errors import OrderNotFound, OrderRejected
from tooja.core.models import Fill, Order, OrderRequest, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


# TR_IDs not exposed by the raw layer (raw defaults to sell).
_TR_BUY_REAL = "TTTC0012U"
_TR_BUY_DEMO = "VTTC0012U"
_TR_SELL_REAL = "TTTC0011U"
_TR_SELL_DEMO = "VTTC0011U"


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


def _yyyymmdd(d: date | datetime) -> str:
    if isinstance(d, datetime):
        d = d.date()
    return d.strftime("%Y%m%d")


def _order_tr_id(side: OrderSide, is_virtual: bool) -> str:
    if side is OrderSide.BUY:
        return _TR_BUY_DEMO if is_virtual else _TR_BUY_REAL
    return _TR_SELL_DEMO if is_virtual else _TR_SELL_REAL


class KisOrdersClient(OrdersClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def create(self, req: OrderRequest) -> Order:
        sym = _as_symbol(req.symbol)
        creds = self._broker.credentials
        ord_dvsn = kis_ord_dvsn(req.type)
        price = getattr(req, "price", None)
        ord_unpr = str(price.amount) if price is not None else "0"

        raw_req = OrderCashRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            PDNO=sym.ticker,
            ORD_DVSN=ord_dvsn,
            ORD_QTY=str(req.qty),
            ORD_UNPR=ord_unpr,
        )

        tr_id = _order_tr_id(req.side, self._broker.is_virtual)
        resp = await call(self._broker, OrderCashExecutor, raw_req, tr_id=tr_id)

        out = getattr(resp, "output", []) or []
        if not out or not getattr(out[0], "ODNO", None):
            raise OrderRejected(
                "KIS order-cash returned no ODNO", broker="kis",
                endpoint=OrderCashExecutor.PATH,
            )
        head = out[0]
        ord_tmd = getattr(head, "ORD_TMD", None)
        submitted = _parse_ord_tmd(ord_tmd) or datetime.now(timezone.utc)

        return Order(
            order_id=head.ODNO,
            symbol=sym,
            side=req.side,
            qty=req.qty,
            filled_qty=Decimal(0),
            avg_fill_price=None,
            type=req.type,
            price=price,
            stop_price=getattr(req, "stop_price", None),
            status=OrderStatus.OPEN,
            time_in_force=getattr(req, "time_in_force", TimeInForce.DAY),
            client_order_id=req.client_order_id,
            submitted_at=submitted,
            raw={
                "krx_fwdg_ord_orgno": getattr(head, "KRX_FWDG_ORD_ORGNO", None),
                "ord_tmd": ord_tmd,
            },
        )

    async def cancel(self, order_id: str) -> Order:
        existing = await self.get(order_id)
        return await self._rvsecncl(existing, dvsn="02", new_qty=None, new_price=None)

    async def replace(
        self,
        order_id: str,
        *,
        qty: Decimal | None = None,
        price: Decimal | None = None,
    ) -> Order:
        existing = await self.get(order_id)
        return await self._rvsecncl(existing, dvsn="01", new_qty=qty, new_price=price)

    async def _rvsecncl(
        self,
        existing: Order,
        *,
        dvsn: str,
        new_qty: Decimal | None,
        new_price: Decimal | None,
    ) -> Order:
        creds = self._broker.credentials
        krx_org = existing.raw.get("krx_fwdg_ord_orgno") or ""
        eff_qty = new_qty if new_qty is not None else existing.qty
        eff_price = new_price if new_price is not None else (
            existing.price.amount if existing.price is not None else Decimal(0)
        )
        all_qty = "Y" if (dvsn == "02" and new_qty is None) else "N"
        raw_req = OrderRvsecnclRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            KRX_FWDG_ORD_ORGNO=krx_org,
            ORGN_ODNO=existing.order_id,
            ORD_DVSN=kis_ord_dvsn(existing.type),
            RVSE_CNCL_DVSN_CD=dvsn,
            ORD_QTY=str(eff_qty),
            ORD_UNPR=str(eff_price),
            QTY_ALL_ORD_YN=all_qty,
        )
        resp = await call(self._broker, OrderRvsecnclExecutor, raw_req)
        out = getattr(resp, "output", []) or []
        if not out or not getattr(out[0], "odno", None):
            raise OrderRejected(
                f"KIS order-rvsecncl returned no odno (dvsn={dvsn})",
                broker="kis", endpoint=OrderRvsecnclExecutor.PATH,
            )
        new_id = out[0].odno
        new_status = OrderStatus.CANCELLED if dvsn == "02" else OrderStatus.OPEN
        return existing.model_copy(update={
            "order_id": new_id,
            "qty": eff_qty,
            "price": existing.price if new_price is None else existing.price.model_copy(
                update={"amount": new_price}
            ) if existing.price else None,
            "status": new_status,
            "raw": {**existing.raw, "rvsecncl_dvsn": dvsn},
        })

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


def _parse_ord_tmd(s: str | None) -> datetime | None:
    """KIS ord_tmd is HHMMSS in KST; date defaults to today.

    KIS sometimes omits leading zeros (e.g. "93000" for 09:30:00), so we pad.
    """
    from datetime import timedelta
    if not s:
        return None
    try:
        sp = s.zfill(6)
        h, m, sec = int(sp[:2]), int(sp[2:4]), int(sp[4:6])
    except ValueError:
        return None
    today = date.today()
    kst = datetime(today.year, today.month, today.day, h, m, sec)
    return (kst - timedelta(hours=9)).replace(tzinfo=timezone.utc)
