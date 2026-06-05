"""KIS Rankings subclient.

Supported RankingType:
- VOLUME / TURNOVER
- MARKET_CAP
- PRICE_CHANGE_UP / PRICE_CHANGE_DOWN
- FOREIGN_NET_BUY / FOREIGN_NET_SELL
- INSTITUTIONAL_NET_BUY / INSTITUTIONAL_NET_SELL
- SHORT_SELLING_VOLUME / SHORT_SELLING_VALUE
- MARGIN_BALANCE
- BID_QTY / ASK_QTY
- NEW_HIGH / NEW_LOW
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    ranking_entry_from_credit_balance_row,
    ranking_entry_from_highlow_row,
    ranking_entry_from_investor_total_row,
    ranking_entry_from_market_cap_row,
    ranking_entry_from_quote_balance_row,
    ranking_entry_from_short_row,
    ranking_entry_from_turnover_row,
    ranking_entry_from_volume_row,
)
from tooja.brokers.kis.raw.domestic_stock_quote_analysis.foreign_institution_total import (
    ForeignInstitutionTotalExecutor,
    ForeignInstitutionTotalRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.credit_balance import (
    CreditBalanceExecutor,
    CreditBalanceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.fluctuation import (
    FluctuationExecutor,
    FluctuationRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.market_cap import (
    MarketCapExecutor,
    MarketCapRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.near_new_highlow import (
    NearNewHighlowExecutor,
    NearNewHighlowRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.quote_balance import (
    QuoteBalanceExecutor,
    QuoteBalanceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.short_sale import (
    ShortSaleExecutor,
    ShortSaleRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.volume_rank import (
    VolumeRankExecutor,
    VolumeRankRequest,
)
from tooja.core.clients import RankingsClient
from tooja.core.enums import Exchange, RankingType
from tooja.core.errors import UnsupportedOperation
from tooja.core.models import RankingEntry

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker


class KisRankingsClient(RankingsClient):
    _broker_name = "kis"

    def __init__(self, broker: "KisBroker"):
        self._broker = broker

    async def get(
        self,
        type: RankingType,
        *,
        market: Exchange = Exchange.KRX,
        limit: int = 30,
    ) -> list[RankingEntry]:
        if type is RankingType.VOLUME:
            return await self._volume(limit=limit, sort_blng="0")
        if type is RankingType.TURNOVER:
            return await self._volume(limit=limit, sort_blng="3", mapper=ranking_entry_from_turnover_row)
        if type is RankingType.MARKET_CAP:
            return await self._market_cap(limit=limit)
        if type is RankingType.PRICE_CHANGE_UP:
            return await self._fluctuation(limit=limit, up=True)
        if type is RankingType.PRICE_CHANGE_DOWN:
            return await self._fluctuation(limit=limit, up=False)
        if type is RankingType.FOREIGN_NET_BUY:
            return await self._investor_total(limit=limit, sort="0", actor="1",
                                              value_field="frgn_ntby_qty")
        if type is RankingType.FOREIGN_NET_SELL:
            return await self._investor_total(limit=limit, sort="1", actor="1",
                                              value_field="frgn_ntby_qty")
        if type is RankingType.INSTITUTIONAL_NET_BUY:
            return await self._investor_total(limit=limit, sort="0", actor="2",
                                              value_field="orgn_ntby_qty")
        if type is RankingType.INSTITUTIONAL_NET_SELL:
            return await self._investor_total(limit=limit, sort="1", actor="2",
                                              value_field="orgn_ntby_qty")
        if type is RankingType.SHORT_SELLING_VOLUME:
            return await self._short_sale(limit=limit)
        if type is RankingType.SHORT_SELLING_VALUE:
            return await self._short_sale(limit=limit)
        if type is RankingType.MARGIN_BALANCE:
            return await self._margin_balance(limit=limit)
        if type is RankingType.BID_QTY:
            return await self._quote_balance(limit=limit, sort="0")
        if type is RankingType.ASK_QTY:
            return await self._quote_balance(limit=limit, sort="1")
        if type is RankingType.NEW_HIGH:
            return await self._highlow(limit=limit, near_high=True)
        if type is RankingType.NEW_LOW:
            return await self._highlow(limit=limit, near_high=False)
        raise UnsupportedOperation(
            f"KIS rankings.get(type={type.value}) unsupported",
            broker="kis",
        )

    async def _volume(self, *, limit: int, sort_blng: str = "0", mapper=ranking_entry_from_volume_row) -> list[RankingEntry]:
        req = VolumeRankRequest(
            FID_COND_MRKT_DIV_CODE="J",
            FID_COND_SCR_DIV_CODE="20171",
            FID_INPUT_ISCD="0000",
            FID_DIV_CLS_CODE="0",
            FID_BLNG_CLS_CODE=sort_blng,
            FID_TRGT_CLS_CODE="111111111",
            FID_TRGT_EXLS_CLS_CODE="0000000000",
            FID_INPUT_PRICE_1="",
            FID_INPUT_PRICE_2="",
            FID_VOL_CNT="",
        )
        resp = await call(self._broker, VolumeRankExecutor, req)
        return _collect(resp, mapper, limit)

    async def _market_cap(self, *, limit: int) -> list[RankingEntry]:
        req = MarketCapRequest(
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="20174",
            fid_input_iscd="0000",
            fid_div_cls_code="0",
            fid_input_price_1="",
            fid_input_price_2="",
            fid_vol_cnt="",
            fid_trgt_cls_code="0",
            fid_trgt_exls_cls_code="0",
        )
        resp = await call(self._broker, MarketCapExecutor, req)
        return _collect(resp, ranking_entry_from_market_cap_row, limit)

    async def _fluctuation(self, *, limit: int, up: bool) -> list[RankingEntry]:
        req = FluctuationRequest(
            fid_rsfl_rate2="",
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="20170",
            fid_input_iscd="0000",
            fid_rank_sort_cls_code="0" if up else "1",
            fid_input_cnt_1="0",
            fid_prc_cls_code="1",
            fid_input_price_1="",
            fid_input_price_2="",
            fid_vol_cnt="",
            fid_trgt_cls_code="0",
            fid_trgt_exls_cls_code="0",
            fid_div_cls_code="0",
            fid_rsfl_rate1="",
        )
        resp = await call(self._broker, FluctuationExecutor, req)
        return _collect(resp, ranking_entry_from_volume_row, limit)

    async def _investor_total(
        self, *, limit: int, sort: str, actor: str, value_field: str,
    ) -> list[RankingEntry]:
        req = ForeignInstitutionTotalRequest(
            FID_COND_MRKT_DIV_CODE="V",
            FID_COND_SCR_DIV_CODE="16449",
            FID_INPUT_ISCD="0000",
            FID_DIV_CLS_CODE="0",
            FID_RANK_SORT_CLS_CODE=sort,
            FID_ETC_CLS_CODE=actor,
        )
        resp = await call(self._broker, ForeignInstitutionTotalExecutor, req)

        def _mapper(item, raw_row):
            return ranking_entry_from_investor_total_row(item, raw_row, value_field=value_field)

        return _collect(resp, _mapper, limit)

    async def _short_sale(self, *, limit: int) -> list[RankingEntry]:
        req = ShortSaleRequest(
            FID_APLY_RANG_VOL="",
            FID_COND_MRKT_DIV_CODE="J",
            FID_COND_SCR_DIV_CODE="20482",
            FID_INPUT_ISCD="0000",
            FID_PERIOD_DIV_CODE="D",
            FID_INPUT_CNT_1="0",
            FID_TRGT_EXLS_CLS_CODE="",
            FID_TRGT_CLS_CODE="",
            FID_APLY_RANG_PRC_1="",
            FID_APLY_RANG_PRC_2="",
        )
        resp = await call(self._broker, ShortSaleExecutor, req)
        return _collect(resp, ranking_entry_from_short_row, limit)

    async def _margin_balance(self, *, limit: int) -> list[RankingEntry]:
        req = CreditBalanceRequest(
            FID_COND_MRKT_DIV_CODE="J",
            FID_COND_SCR_DIV_CODE="11701",
            FID_INPUT_ISCD="0000",
            FID_OPTION="3",
            FID_RANK_SORT_CLS_CODE="2",
        )
        resp = await call(self._broker, CreditBalanceExecutor, req)
        return _collect(resp, ranking_entry_from_credit_balance_row, limit)

    async def _quote_balance(self, *, limit: int, sort: str) -> list[RankingEntry]:
        req = QuoteBalanceRequest(
            fid_vol_cnt="",
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="20172",
            fid_input_iscd="0000",
            fid_rank_sort_cls_code=sort,
            fid_div_cls_code="0",
            fid_trgt_cls_code="0",
            fid_trgt_exls_cls_code="0",
            fid_input_price_1="",
            fid_input_price_2="",
        )
        resp = await call(self._broker, QuoteBalanceExecutor, req)
        return _collect(resp, ranking_entry_from_quote_balance_row, limit)

    async def _highlow(self, *, limit: int, near_high: bool) -> list[RankingEntry]:
        req = NearNewHighlowRequest(
            fid_aply_rang_vol="0",
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="20187",
            fid_div_cls_code="0",
            fid_input_cnt_1="0",
            fid_input_cnt_2="100",
            fid_prc_cls_code="0" if near_high else "1",
            fid_input_iscd="0000",
            fid_trgt_cls_code="0",
            fid_trgt_exls_cls_code="0",
            fid_aply_rang_prc_1="",
            fid_aply_rang_prc_2="",
        )
        resp = await call(self._broker, NearNewHighlowExecutor, req)
        return _collect(resp, ranking_entry_from_highlow_row, limit)


def _collect(resp, mapper, limit: int) -> list[RankingEntry]:
    out: list[RankingEntry] = []
    rows = getattr(resp, "output", None) or getattr(resp, "output1", None) or []
    for row in rows:
        entry = mapper(row, row.model_dump())
        if entry is not None:
            out.append(entry)
        if len(out) >= limit:
            break
    return out
