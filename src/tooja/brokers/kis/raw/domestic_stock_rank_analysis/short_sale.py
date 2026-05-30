"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ShortSaleRequest(KisBaseModel):
    """요청."""

    FID_APLY_RANG_VOL: str  # FID 적용 범위 거래량 — 공백
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(20482)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100, 3003: 코스닥150
    FID_PERIOD_DIV_CODE: str  # 조회구분 (일/월) — 조회구분 (일/월) D: 일, M:월
    FID_INPUT_CNT_1: str  # 조회가간(일수 — '조회가간(일수): 조회구분(D) 0:1일, 1:2일, 2:3일, 3:4일, 4:1주일, 9:2주일, 14:3주일, 조회구분(M) 1:1개월, 2:2개월, 3:3개월'
    FID_TRGT_EXLS_CLS_CODE: str  # 대상 제외 구분 코드 — 공백
    FID_TRGT_CLS_CODE: str  # FID 대상 구분 코드 — 공백
    FID_APLY_RANG_PRC_1: str  # FID 적용 범위 가격1 — 가격 ~
    FID_APLY_RANG_PRC_2: str  # FID 적용 범위 가격2 — ~ 가격

class ShortSaleResponse_OutputItem(KisBaseModel):
    """nested item."""

    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    ssts_cntg_qty: str | None = None  # 공매도 체결 수량
    ssts_vol_rlim: str | None = None  # 공매도 거래량 비중
    ssts_tr_pbmn: str | None = None  # 공매도 거래 대금
    ssts_tr_pbmn_rlim: str | None = None  # 공매도 거래대금 비중
    stnd_date1: str | None = None  # 기준 일자1
    stnd_date2: str | None = None  # 기준 일자2
    avrg_prc: str | None = None  # 평균가격

class ShortSaleResponse(KisCommonResponse):
    """응답 본문."""

    output: list[ShortSaleResponse_OutputItem] = []  # 응답상세 — array

class ShortSaleExecutor(ApiExecutor[ShortSaleRequest, ShortSaleResponse]):
    """국내주식 공매도 상위종목[국내주식-133]."""

    # 공매도 상위종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0482] 공매도 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. ※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API는 HTS

    PATH = "/uapi/domestic-stock/v1/ranking/short-sale"
    METHOD = "GET"
    RESPONSE_TYPE = ShortSaleResponse
    TR_ID = "FHPST04820000"
