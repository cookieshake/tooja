"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PbarTratioRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건시장분류코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력종목코드 — 주식단축종목코드
    FID_COND_SCR_DIV_CODE: str  # 조건화면분류코드 — Uniquekey(20113)
    FID_INPUT_HOUR_1: str  # 입력시간1 — 공백

class PbarTratioResponse_Output1Item(KisBaseModel):
    """nested item."""

    rprs_mrkt_kor_name: str | None = None  # 대표시장한글명
    stck_shrn_iscd: str | None = None  # 주식단축종목코드
    hts_kor_isnm: str | None = None  # HTS한글종목명
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss_sign: str | None = None  # 전일대비부호
    prdy_vrss: str | None = None  # 전일대비
    prdy_ctrt: str | None = None  # 전일대비율
    acml_vol: str | None = None  # 누적거래량
    prdy_vol: str | None = None  # 전일거래량
    wghn_avrg_stck_prc: str | None = None  # 가중평균주식가격
    lstn_stcn: str | None = None  # 상장주수

class PbarTratioResponse_Output2Item(KisBaseModel):
    """nested item."""

    data_rank: str | None = None  # 데이터순위
    stck_prpr: str | None = None  # 주식현재가
    cntg_vol: str | None = None  # 체결거래량
    acml_vol_rlim: str | None = None  # 누적거래량비중

class PbarTratioResponse(KisCommonResponse):
    """응답 본문."""

    output1: PbarTratioResponse_Output1Item | None = None  # 응답상세
    output2: list[PbarTratioResponse_Output2Item] = []  # 응답상세 — array

class PbarTratioExecutor(ApiExecutor[PbarTratioRequest, PbarTratioResponse]):
    """국내주식 매물대/거래비중 [국내주식-196]."""

    # 국내주식 매물대/거래비중 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0113] 당일가격대별 매물대 화면의 데이터 중 일부를 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/pbar-tratio"
    METHOD = "GET"
    RESPONSE_TYPE = PbarTratioResponse
    TR_ID = "FHPST01130000"
