"""KIS Rankings subclient — volume / market_cap / price_change rankings.

Supported RankingType values: VOLUME, MARKET_CAP, PRICE_CHANGE_UP,
PRICE_CHANGE_DOWN. Others raise UnsupportedOperation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tooja.brokers.kis._call import call
from tooja.brokers.kis._mappers import (
    ranking_entry_from_market_cap_row,
    ranking_entry_from_volume_row,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.fluctuation import (
    FluctuationExecutor,
    FluctuationRequest,
)
from tooja.brokers.kis.raw.domestic_stock_rank_analysis.market_cap import (
    MarketCapExecutor,
    MarketCapRequest,
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
            return await self._volume(limit=limit)
        if type is RankingType.MARKET_CAP:
            return await self._market_cap(limit=limit)
        if type in (RankingType.PRICE_CHANGE_UP, RankingType.PRICE_CHANGE_DOWN):
            return await self._fluctuation(
                limit=limit,
                up=type is RankingType.PRICE_CHANGE_UP,
            )
        raise UnsupportedOperation(
            f"KIS rankings.get(type={type.value}) unsupported",
            broker="kis",
        )

    async def _volume(self, *, limit: int) -> list[RankingEntry]:
        req = VolumeRankRequest(
            FID_COND_MRKT_DIV_CODE="J",
            FID_COND_SCR_DIV_CODE="20171",
            FID_INPUT_ISCD="0000",
            FID_DIV_CLS_CODE="0",
            FID_BLNG_CLS_CODE="0",
            FID_TRGT_CLS_CODE="111111111",
            FID_TRGT_EXLS_CLS_CODE="0000000000",
            FID_INPUT_PRICE_1="",
            FID_INPUT_PRICE_2="",
            FID_VOL_CNT="",
        )
        resp = await call(self._broker, VolumeRankExecutor, req)
        return _collect(resp, ranking_entry_from_volume_row, limit)

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
