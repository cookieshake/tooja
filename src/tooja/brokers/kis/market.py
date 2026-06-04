"""KIS Market subclient — quote / orderbook / ohlcv.

Routes by Symbol.exchange:
- KRX / NXT : domestic_stock_quotations.* (KRW)
- NASD/NYSE/AMEX/SEHK/TKSE/SHAA/SZAA/HASE/VNSE : overseas_stock_quotations.*
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Literal

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    excd_for,
    ohlcv_from_chartprice_item,
    ohlcv_from_intraday_item,
    ohlcv_from_overseas_daily_item,
    orderbook_from_inquire_asking,
    quote_from_inquire_price,
    quote_from_overseas_price,
)
from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_asking_price_exp_ccn import (
    InquireAskingPriceExpCcnExecutor,
    InquireAskingPriceExpCcnRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_daily_itemchartprice import (
    InquireDailyItemchartpriceExecutor,
    InquireDailyItemchartpriceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_price import (
    InquirePriceExecutor,
    InquirePriceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_time_itemchartprice import (
    InquireTimeItemchartpriceExecutor,
    InquireTimeItemchartpriceRequest,
)
from tooja.brokers.kis.raw.overseas_stock_quotations.dailyprice import (
    DailypriceExecutor,
    DailypriceRequest,
)
from tooja.brokers.kis.raw.overseas_stock_quotations.price import (
    PriceExecutor,
    PriceRequest,
)
from tooja.core.clients import MarketClient
from tooja.core.enums import Exchange
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import OHLCV, Orderbook, Quote, Symbol

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


_INTERVAL_TO_PERIOD: dict[str, str] = {"1d": "D", "1w": "W", "1M": "M"}
_INTERVAL_TO_OVERSEAS: dict[str, str] = {"1d": "0", "1w": "1", "1M": "2"}
_INTRADAY_INTERVALS = {"1m", "5m", "15m", "30m", "1h"}


def _as_symbol(s: Symbol | str) -> Symbol:
    return s if isinstance(s, Symbol) else Symbol.parse(s)


def _yyyymmdd(d: date | datetime | str) -> str:
    if isinstance(d, str):
        return d.replace("-", "")[:8]
    if isinstance(d, datetime):
        d = d.date()
    return d.strftime("%Y%m%d")


class KisMarketClient(MarketClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def get_quote(self, symbol: Symbol | str) -> Quote:
        sym = _as_symbol(symbol)
        excd = excd_for(sym.exchange)
        if excd is not None:
            return await self._overseas_quote(sym, excd)
        if sym.exchange not in (Exchange.KRX, Exchange.NXT):
            raise UnsupportedOperation(
                f"KIS market.get_quote: exchange {sym.exchange} unsupported",
                broker="kis",
            )
        req = InquirePriceRequest(FID_COND_MRKT_DIV_CODE="J", FID_INPUT_ISCD=sym.ticker)
        resp = await call(self._broker, InquirePriceExecutor, req)
        if resp.output is None:
            raise UnsupportedOperation(
                f"KIS inquire-price returned no output for {sym}", broker="kis",
            )
        return quote_from_inquire_price(sym, resp.output, resp.output.model_dump())

    async def _overseas_quote(self, sym: Symbol, excd: str) -> Quote:
        req = PriceRequest(AUTH="", EXCD=excd, SYMB=sym.ticker)
        resp = await call(self._broker, PriceExecutor, req)
        out = getattr(resp, "output", None)
        if out is None:
            raise UnsupportedOperation(
                f"KIS overseas price returned no output for {sym}", broker="kis",
            )
        return quote_from_overseas_price(sym, out, out.model_dump())

    async def get_quotes(self, symbols: list[Symbol | str]) -> list[Quote]:
        result: list[Quote] = []
        for s in symbols:
            result.append(await self.get_quote(s))
        return result

    async def get_orderbook(self, symbol: Symbol | str, *, depth: int = 10) -> Orderbook:
        sym = _as_symbol(symbol)
        if excd_for(sym.exchange) is not None:
            raise UnsupportedOperation(
                "KIS overseas orderbook returns only 1 best bid/ask via dailyprice; "
                "use stream.orderbook for live overseas depth",
                broker="kis",
            )
        req = InquireAskingPriceExpCcnRequest(
            FID_COND_MRKT_DIV_CODE="J", FID_INPUT_ISCD=sym.ticker,
        )
        resp = await call(self._broker, InquireAskingPriceExpCcnExecutor, req)
        if resp.output1 is None:
            raise UnsupportedOperation(
                f"KIS asking-price returned no output1 for {sym}", broker="kis",
            )
        return orderbook_from_inquire_asking(
            sym, resp.output1, resp.output1.model_dump(), depth=depth,
        )

    async def get_ohlcv(
        self,
        symbol: Symbol | str,
        *,
        interval: Literal["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"],
        start: date | datetime | str | None = None,
        end: date | datetime | str | None = None,
        limit: int | None = None,
    ) -> list[OHLCV]:
        sym = _as_symbol(symbol)
        excd = excd_for(sym.exchange)
        if excd is not None:
            if interval not in _INTERVAL_TO_OVERSEAS:
                raise UnsupportedOperation(
                    f"KIS overseas get_ohlcv interval={interval} unsupported", broker="kis",
                )
            return await self._overseas_daily_ohlcv(
                sym, excd, gubn=_INTERVAL_TO_OVERSEAS[interval], end=end, limit=limit,
            )
        if interval in _INTRADAY_INTERVALS:
            return await self._intraday_ohlcv(sym, interval=interval, limit=limit)
        if interval not in _INTERVAL_TO_PERIOD:
            raise UnsupportedOperation(
                f"KIS get_ohlcv interval={interval} unsupported", broker="kis",
            )
        return await self._daily_ohlcv(
            sym, period=_INTERVAL_TO_PERIOD[interval], start=start, end=end, limit=limit,
        )

    async def _daily_ohlcv(
        self, sym: Symbol, *, period: str, start, end, limit,
    ) -> list[OHLCV]:
        today = date.today()
        end_d = _yyyymmdd(end) if end else today.strftime("%Y%m%d")
        if start is None:
            window_days = (limit or 100) * (1 if period == "D" else 7 if period == "W" else 31)
            start_d = (today - timedelta(days=window_days)).strftime("%Y%m%d")
        else:
            start_d = _yyyymmdd(start)
        req = InquireDailyItemchartpriceRequest(
            FID_COND_MRKT_DIV_CODE="J",
            FID_INPUT_ISCD=sym.ticker,
            FID_INPUT_DATE_1=start_d,
            FID_INPUT_DATE_2=end_d,
            FID_PERIOD_DIV_CODE=period,
            FID_ORG_ADJ_PRC="0",
        )
        resp = await call(self._broker, InquireDailyItemchartpriceExecutor, req)
        bars: list[OHLCV] = []
        for row in resp.output2:
            bar = ohlcv_from_chartprice_item(sym, row)
            if bar is not None:
                bars.append(bar)
        bars.sort(key=lambda b: b.time)
        if limit is not None:
            bars = bars[-limit:]
        return bars

    async def _intraday_ohlcv(self, sym: Symbol, *, interval: str, limit) -> list[OHLCV]:
        req = InquireTimeItemchartpriceRequest(
            FID_ETC_CLS_CODE="",
            FID_COND_MRKT_DIV_CODE="J",
            FID_INPUT_ISCD=sym.ticker,
            FID_INPUT_HOUR_1="153000",
            FID_PW_DATA_INCU_YN="N",
        )
        resp = await call(self._broker, InquireTimeItemchartpriceExecutor, req)
        bars: list[OHLCV] = []
        for row in resp.output2:
            bar = ohlcv_from_intraday_item(sym, row)
            if bar is not None:
                bars.append(bar)
        bars.sort(key=lambda b: b.time)
        if limit is not None:
            bars = bars[-limit:]
        return bars

    async def _overseas_daily_ohlcv(
        self, sym: Symbol, excd: str, *, gubn: str, end, limit,
    ) -> list[OHLCV]:
        end_d = _yyyymmdd(end) if end else date.today().strftime("%Y%m%d")
        req = DailypriceRequest(
            AUTH="", EXCD=excd, SYMB=sym.ticker, GUBN=gubn, BYMD=end_d, MODP="1",
        )
        resp = await call(self._broker, DailypriceExecutor, req)
        bars: list[OHLCV] = []
        for row in getattr(resp, "output2", []) or []:
            bar = ohlcv_from_overseas_daily_item(sym, row)
            if bar is not None:
                bars.append(bar)
        bars.sort(key=lambda b: b.time)
        if limit is not None:
            bars = bars[-limit:]
        return bars
