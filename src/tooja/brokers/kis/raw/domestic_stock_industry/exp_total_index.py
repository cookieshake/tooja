"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpTotalIndexRequest(KisBaseModel):
    """요청."""

    fid_mrkt_cls_code: str  # 시장 구분 코드 — 0:전체 K:거래소 Q:코스닥
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (업종 U)
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key(11175)
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
    fid_mkop_cls_code: str  # 장운영 구분 코드 — 1:장시작전, 2:장마감

class ExpTotalIndexResponse_Output1Item(KisBaseModel):
    """nested item."""

    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    ascn_issu_cnt: str | None = None  # 상승 종목 수
    down_issu_cnt: str | None = None  # 하락 종목 수
    stnr_issu_cnt: str | None = None  # 보합 종목 수
    bstp_cls_code: str | None = None  # 업종 구분 코드

class ExpTotalIndexResponse_Output2Item(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    bstp_nmix_prpr: str | None = None  # 업종 지수 현재가
    bstp_nmix_prdy_vrss: str | None = None  # 업종 지수 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    bstp_nmix_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    nmix_sdpr: str | None = None  # 지수 기준가
    ascn_issu_cnt: str | None = None  # 상승 종목 수
    stnr_issu_cnt: str | None = None  # 보합 종목 수
    down_issu_cnt: str | None = None  # 하락 종목 수

class ExpTotalIndexResponse(KisCommonResponse):
    """응답 본문."""

    output1: ExpTotalIndexResponse_Output1Item | None = None  # 응답상세
    output2: list[ExpTotalIndexResponse_Output2Item] = []  # 응답상세 — array

class ExpTotalIndexExecutor(ApiExecutor[ExpTotalIndexRequest, ExpTotalIndexResponse]):
    """국내주식 예상체결 전체지수[국내주식-122]."""

    # 국내주식 예상체결 전체지수 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0185] 예상체결 전체지수 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/exp-total-index"
    METHOD = "GET"
    RESPONSE_TYPE = ExpTotalIndexResponse
    TR_ID = "FHKUP11750000"
