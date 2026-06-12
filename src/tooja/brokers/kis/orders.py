"""KIS Orders subclient — real POST to KIS.

env="demo" routes to KIS mock server (가짜 자금). env="real" routes to live
production server (실제 자금). The library does NOT add a dry-run flag; the
env selection is the entire safety boundary, matching ccxt/Alpaca/IB
convention.

Routing: Symbol.exchange KRX/NXT -> domestic cash endpoints; the nine
overseas exchanges (NASD/NYSE/AMEX/SEHK/SHAA/SZAA/TKSE/HASE/VNSE) ->
/uapi/overseas-stock/v1/trading/* with a per-region TR matrix (see
_OVRS_ORDER_TR / _OVRS_RVSECNCL_TR). Overseas regular-session orders are
limit-only; market orders raise UnsupportedOperation.

Domestic TR_IDs:
- BUY  : TTTC0012U (real) / VTTC0012U (demo)
- SELL : TTTC0011U (real) / VTTC0011U (demo)

cancel/replace: order-rvsecncl, RVSE_CNCL_DVSN_CD = 02 (cancel) / 01 (replace).
"""

from __future__ import annotations

import asyncio
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, AsyncIterator, Literal

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    fill_from_daily_ccld_row,
    fill_from_ovrs_ccnl_row,
    kis_ord_dvsn,
    kst_today,
    order_from_daily_ccld_row,
    order_from_ovrs_ccnl_row,
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
from tooja.brokers.kis.raw.overseas_stock_trading.inquire_ccnl import (
    InquireCcnlExecutor as OvrsInquireCcnlExecutor,
    InquireCcnlRequest as OvrsInquireCcnlRequest,
)
from tooja.brokers.kis.raw.overseas_stock_trading.order import (
    OrderExecutor as OvrsOrderExecutor,
    OrderRequest as OvrsOrderRequest,
)
from tooja.brokers.kis.raw.overseas_stock_trading.order_rvsecncl import (
    OrderRvsecnclExecutor as OvrsRvsecnclExecutor,
    OrderRvsecnclRequest as OvrsRvsecnclRequest,
)
from tooja.core.clients import OrdersClient
from tooja.core.enums import Exchange, OrderSide, OrderStatus, TimeInForce
from tooja.core.errors import (
    OrderNotFound,
    OrderRejected,
    PermissionDenied,
    UnsupportedOperation,
)
from tooja.core.markets import currency_of
from tooja.core.models import Fill, Order, OrderRequest, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


# TR_IDs not exposed by the raw layer (raw defaults to sell).
_TR_BUY_REAL = "TTTC0012U"
_TR_BUY_DEMO = "VTTC0012U"
_TR_SELL_REAL = "TTTC0011U"
_TR_SELL_DEMO = "VTTC0011U"

# Overseas TR matrix (specs/kis/api-list/overseas_stock_trading.json).
# Region key: US = NASD/NYSE/AMEX, JP = TKSE, HK = SEHK, SHA = SHAA,
# SZN = SZAA, VN = HASE/VNSE.
_OVRS_REGION: dict[Exchange, str] = {
    Exchange.NASD: "US", Exchange.NYSE: "US", Exchange.AMEX: "US",
    Exchange.TKSE: "JP", Exchange.SEHK: "HK",
    Exchange.SHAA: "SHA", Exchange.SZAA: "SZN",
    Exchange.HASE: "VN", Exchange.VNSE: "VN",
}

# (region, side) -> (real, demo). Demo is V + same suffix, EXCEPT US sell:
# KIS demo uses VTTT1001U while real uses TTTT1006U.
_OVRS_ORDER_TR: dict[tuple[str, OrderSide], tuple[str, str]] = {
    ("US", OrderSide.BUY): ("TTTT1002U", "VTTT1002U"),
    ("US", OrderSide.SELL): ("TTTT1006U", "VTTT1001U"),
    ("JP", OrderSide.BUY): ("TTTS0308U", "VTTS0308U"),
    ("JP", OrderSide.SELL): ("TTTS0307U", "VTTS0307U"),
    ("SHA", OrderSide.BUY): ("TTTS0202U", "VTTS0202U"),
    ("SHA", OrderSide.SELL): ("TTTS1005U", "VTTS1005U"),
    ("HK", OrderSide.BUY): ("TTTS1002U", "VTTS1002U"),
    ("HK", OrderSide.SELL): ("TTTS1001U", "VTTS1001U"),
    ("SZN", OrderSide.BUY): ("TTTS0305U", "VTTS0305U"),
    ("SZN", OrderSide.SELL): ("TTTS0304U", "VTTS0304U"),
    ("VN", OrderSide.BUY): ("TTTS0311U", "VTTS0311U"),
    ("VN", OrderSide.SELL): ("TTTS0310U", "VTTS0310U"),
}

# region -> (real, demo); one TR covers both modify and cancel.
_OVRS_RVSECNCL_TR: dict[str, tuple[str, str]] = {
    "US": ("TTTT1004U", "VTTT1004U"),
    "HK": ("TTTS1003U", "VTTS1003U"),
    "JP": ("TTTS0309U", "VTTS0309U"),
    "SHA": ("TTTS0302U", "VTTS0302U"),
    "SZN": ("TTTS0306U", "VTTS0306U"),
    "VN": ("TTTS0312U", "VTTS0312U"),
}


def _is_overseas(exchange: Exchange) -> bool:
    return exchange in _OVRS_REGION


def _ovrs_order_tr_id(exchange: Exchange, side: OrderSide, is_virtual: bool) -> str:
    real, demo = _OVRS_ORDER_TR[(_OVRS_REGION[exchange], side)]
    return demo if is_virtual else real


def _ovrs_rvsecncl_tr_id(exchange: Exchange, is_virtual: bool) -> str:
    real, demo = _OVRS_RVSECNCL_TR[_OVRS_REGION[exchange]]
    return demo if is_virtual else real


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
        if _is_overseas(sym.exchange):
            return await self._create_overseas(req, sym)
        return await self._create_domestic(req, sym)

    async def _create_domestic(self, req: OrderRequest, sym: Symbol) -> Order:
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
        return self._order_from_create_resp(
            resp, sym, req, price, endpoint=OrderCashExecutor.PATH,
        )

    async def _create_overseas(self, req: OrderRequest, sym: Symbol) -> Order:
        if req.type == "market":
            raise UnsupportedOperation(
                "KIS overseas orders support limit only — the regular-session "
                "API has no market ORD_DVSN",
                broker="kis",
            )
        price = req.price
        expected = currency_of(sym.exchange)
        if price.currency != expected:
            raise ValueError(
                f"order price currency {price.currency.value} does not match "
                f"{sym.exchange.value} settlement currency {expected.value}"
            )
        creds = self._broker.credentials
        raw_req = OvrsOrderRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            OVRS_EXCG_CD=sym.exchange.value,
            PDNO=sym.ticker,
            ORD_QTY=str(req.qty),
            OVRS_ORD_UNPR=str(price.amount),
            SLL_TYPE="00" if req.side is OrderSide.SELL else None,
            ORD_SVR_DVSN_CD="0",
            ORD_DVSN="00",
        )
        tr_id = _ovrs_order_tr_id(sym.exchange, req.side, self._broker.is_virtual)
        resp = await call(self._broker, OvrsOrderExecutor, raw_req, tr_id=tr_id)
        return self._order_from_create_resp(
            resp, sym, req, price, endpoint=OvrsOrderExecutor.PATH,
        )

    def _order_from_create_resp(
        self, resp, sym: Symbol, req: OrderRequest, price, *, endpoint: str,
    ) -> Order:
        # Domestic order-cash returns `output` as a (normalized) list;
        # the overseas order endpoint returns a single object.
        out = getattr(resp, "output", None)
        head = out[0] if isinstance(out, list) and out else (
            out if not isinstance(out, list) else None
        )
        if head is None or not getattr(head, "ODNO", None):
            raise OrderRejected(
                "KIS order returned no ODNO", broker="kis", endpoint=endpoint,
            )
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
        if _is_overseas(existing.symbol.exchange):
            return await self._rvsecncl_overseas(
                existing, dvsn=dvsn, new_qty=new_qty, new_price=new_price,
            )
        creds = self._broker.credentials
        # KRX_FWDG_ORD_ORGNO source differs by how `existing` was built:
        #   - create() stores it under "krx_fwdg_ord_orgno"
        #   - get()/list_orders() carry the raw inquire-daily-ccld row, which
        #     names it "ord_gno_brno" (and exposes "ord_orgno" too)
        krx_org = (
            existing.raw.get("krx_fwdg_ord_orgno")
            or existing.raw.get("ord_gno_brno")
            or existing.raw.get("ord_orgno")
            or ""
        )
        # Full cancel: send qty=0 + QTY_ALL_ORD_YN=Y. Sending the original qty
        # can be rejected with "quantity exceeded" if the order was partially
        # filled before we cancel.
        if dvsn == "02" and new_qty is None:
            eff_qty: Decimal = Decimal(0)
            all_qty = "Y"
        else:
            eff_qty = new_qty if new_qty is not None else existing.qty
            all_qty = "N"
        eff_price = new_price if new_price is not None else (
            existing.price.amount if existing.price is not None else Decimal(0)
        )
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
        if not out or not getattr(out[0], "ODNO", None):
            raise OrderRejected(
                f"KIS order-rvsecncl returned no ODNO (dvsn={dvsn})",
                broker="kis", endpoint=OrderRvsecnclExecutor.PATH,
            )
        new_id = out[0].ODNO
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

    async def _rvsecncl_overseas(
        self,
        existing: Order,
        *,
        dvsn: str,
        new_qty: Decimal | None,
        new_price: Decimal | None,
    ) -> Order:
        # SHA/SZN/VN are cancel-only per the KIS TR list — a replace is still
        # sent and KIS's rejection propagates; no client-side pre-block.
        creds = self._broker.credentials
        if dvsn == "02" and new_qty is None:
            # The overseas API has no QTY_ALL_ORD_YN — cancel the unfilled
            # remainder explicitly.
            remaining = existing.qty - existing.filled_qty
            eff_qty: Decimal = remaining if remaining > 0 else existing.qty
        else:
            eff_qty = new_qty if new_qty is not None else existing.qty
        if dvsn == "02":
            eff_price = Decimal(0)  # spec: cancel sends "0"
        else:
            eff_price = new_price if new_price is not None else (
                existing.price.amount if existing.price is not None else Decimal(0)
            )
        raw_req = OvrsRvsecnclRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            OVRS_EXCG_CD=existing.symbol.exchange.value,
            PDNO=existing.symbol.ticker,
            ORGN_ODNO=existing.order_id,
            RVSE_CNCL_DVSN_CD=dvsn,
            ORD_QTY=str(eff_qty),
            OVRS_ORD_UNPR=str(eff_price),
            ORD_SVR_DVSN_CD="0",
        )
        tr_id = _ovrs_rvsecncl_tr_id(
            existing.symbol.exchange, self._broker.is_virtual,
        )
        resp = await call(self._broker, OvrsRvsecnclExecutor, raw_req, tr_id=tr_id)
        out = getattr(resp, "output", None)
        head = out[0] if isinstance(out, list) and out else (
            out if not isinstance(out, list) else None
        )
        if head is None or not getattr(head, "ODNO", None):
            raise OrderRejected(
                f"KIS overseas order-rvsecncl returned no ODNO (dvsn={dvsn})",
                broker="kis", endpoint=OvrsRvsecnclExecutor.PATH,
            )
        new_status = OrderStatus.CANCELLED if dvsn == "02" else OrderStatus.OPEN
        return existing.model_copy(update={
            "order_id": head.ODNO,
            "qty": eff_qty,
            "price": existing.price if new_price is None else (
                existing.price.model_copy(update={"amount": new_price})
                if existing.price else None
            ),
            "status": new_status,
            "raw": {**existing.raw, "rvsecncl_dvsn": dvsn},
        })

    async def get(self, order_id: str) -> Order:
        # Domestic inquire-daily-ccld supports server-side ODNO filtering;
        # the overseas inquire-ccnl does not (the spec mandates an empty
        # ODNO), so overseas rows are matched client-side.
        dom_rows, ovrs_rows = await self._gather_ccld_rows(
            symbol=None, since=None, until=None,
            status="all", only_filled=False, order_id=order_id,
        )
        for row in dom_rows:
            order = order_from_daily_ccld_row(row, row.model_dump())
            if order is not None and order.order_id == order_id:
                return order
        for row in ovrs_rows:
            order = order_from_ovrs_ccnl_row(row, row.model_dump())
            if order is not None and order.order_id == order_id:
                return order
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
        sym = _as_symbol(symbol) if symbol else None
        dom_rows, ovrs_rows = await self._gather_ccld_rows(
            symbol=sym, since=since, until=until,
            status=status, only_filled=False,
        )
        mapped = [order_from_daily_ccld_row(r, r.model_dump()) for r in dom_rows]
        mapped += [order_from_ovrs_ccnl_row(r, r.model_dump()) for r in ovrs_rows]
        out: list[Order] = []
        for order in mapped:
            if order is None:
                continue
            # Client-side filters back up the server-side ones: demo accounts
            # can only query overseas wildcards, and the overseas endpoint
            # cannot filter by status reliably.
            if sym is not None and (
                order.symbol.ticker != sym.ticker
                or order.symbol.exchange != sym.exchange
            ):
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
        sym = _as_symbol(symbol) if symbol else None
        dom_rows, ovrs_rows = await self._gather_ccld_rows(
            symbol=sym, since=since, until=until,
            status="closed", only_filled=True,
        )
        fills = [fill_from_daily_ccld_row(r, r.model_dump()) for r in dom_rows]
        fills += [fill_from_ovrs_ccnl_row(r, r.model_dump()) for r in ovrs_rows]
        out: list[Fill] = []
        for f in fills:
            if f is None:
                continue
            if sym is not None and (
                f.symbol.ticker != sym.ticker or f.symbol.exchange != sym.exchange
            ):
                continue
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
        order_id: str | None = None,
    ) -> list:
        creds = self._broker.credentials
        today = kst_today()
        end_d = _yyyymmdd(until) if until else _yyyymmdd(today)
        start_d = _yyyymmdd(since) if since else _yyyymmdd(today)
        # KIS rejects null in request fields — empty string queries all symbols.
        pdno = _as_symbol(symbol).ticker if symbol else ""
        ccld_dvsn = "01" if only_filled else ("02" if status == "open" else "00")

        req = InquireDailyCcldRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            INQR_STRT_DT=start_d,
            INQR_END_DT=end_d,
            SLL_BUY_DVSN_CD="00",
            PDNO=pdno,
            ORD_GNO_BRNO="",
            ODNO=order_id or "",
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

    async def _iter_ovrs_ccnl(
        self,
        *,
        symbol: Symbol | str | None,
        since: date | datetime | None,
        until: date | datetime | None,
        status: str,
        only_filled: bool,
    ) -> list:
        creds = self._broker.credentials
        today = kst_today()
        start_d = _yyyymmdd(since) if since else _yyyymmdd(today)
        end_d = _yyyymmdd(until) if until else _yyyymmdd(today)
        sym = _as_symbol(symbol) if symbol else None
        if self._broker.is_virtual:
            # Demo accounts only accept the wildcard query (PDNO="",
            # SLL_BUY_DVSN=00, CCLD_NCCS_DVSN=00); filtering happens
            # client-side in the callers.
            pdno, excg, ccld = "", "%", "00"
        else:
            pdno = sym.ticker if sym else "%"
            excg = sym.exchange.value if sym else "%"
            ccld = "01" if only_filled else ("02" if status == "open" else "00")

        req = OvrsInquireCcnlRequest(
            CANO=creds.cano,
            ACNT_PRDT_CD=creds.acnt_prdt_cd,
            PDNO=pdno,
            ORD_STRT_DT=start_d,
            ORD_END_DT=end_d,
            SLL_BUY_DVSN="00",
            CCLD_NCCS_DVSN=ccld,
            OVRS_EXCG_CD=excg,
            SORT_SQN="DS",
            ORD_DT="",
            ORD_GNO_BRNO="",
            ODNO="",  # spec: ODNO search is not supported — must stay empty
            CTX_AREA_NK200="",
            CTX_AREA_FK200="",
        )

        all_rows: list = []
        tr_cont = ""
        guard = 0
        while True:
            extra = {"tr_cont": tr_cont} if tr_cont else None
            resp = await call(
                self._broker, OvrsInquireCcnlExecutor, req, extra_headers=extra,
            )
            all_rows.extend(getattr(resp, "output", []) or [])
            hdr = getattr(resp, "headers", None)
            nxt = getattr(hdr, "tr_cont", None) if hdr else None
            if nxt not in ("F", "M"):
                break
            req = req.model_copy(update={
                "CTX_AREA_FK200": getattr(resp, "ctx_area_fk200", "") or "",
                "CTX_AREA_NK200": getattr(resp, "ctx_area_nk200", "") or "",
            })
            tr_cont = "N"
            guard += 1
            if guard > 50:
                break
        return all_rows

    async def _gather_ccld_rows(
        self,
        *,
        symbol: Symbol | str | None,
        since: date | datetime | None,
        until: date | datetime | None,
        status: str,
        only_filled: bool,
        order_id: str | None = None,
    ) -> tuple[list, list]:
        """(domestic_rows, overseas_rows) per the routing rules."""
        sym = _as_symbol(symbol) if symbol else None
        if sym is not None and _is_overseas(sym.exchange):
            # An EXPLICIT overseas query propagates PermissionDenied — a
            # silent [] would misreport an unenrolled account as orderless.
            rows = await self._iter_ovrs_ccnl(
                symbol=sym, since=since, until=until,
                status=status, only_filled=only_filled,
            )
            return [], rows
        if sym is not None:
            rows = await self._iter_ccld(
                symbol=sym, since=since, until=until,
                status=status, only_filled=only_filled, order_id=order_id,
            )
            return rows, []

        async def ovrs_lenient() -> list:
            # Same carve-out as KisAccountClient.get_balance: an account not
            # enrolled for overseas trading is a permanent config state, so
            # the implicit fan-out degrades to domestic-only.
            try:
                return await self._iter_ovrs_ccnl(
                    symbol=None, since=since, until=until,
                    status=status, only_filled=only_filled,
                )
            except PermissionDenied:
                return []

        dom_rows, ovrs_rows = await asyncio.gather(
            self._iter_ccld(
                symbol=None, since=since, until=until,
                status=status, only_filled=only_filled, order_id=order_id,
            ),
            ovrs_lenient(),
        )
        return dom_rows, ovrs_rows


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
    today = kst_today()
    kst = datetime(today.year, today.month, today.day, h, m, sec)
    return (kst - timedelta(hours=9)).replace(tzinfo=timezone.utc)
