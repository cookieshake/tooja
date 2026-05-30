"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpPriceTrendRequest(KisBaseModel):
    """요청."""

    fid_mkop_cls_code: str  # 장운영 구분 코드 — 0:전체, 4:체결량 0 제외
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    fid_input_iscd: str  # 입력 종목코드 — 종목코드(ex. 005930)

class ExpPriceTrendResponse_Output1Item(KisBaseModel):
    """nested item."""

    rprs_mrkt_kor_name: str | None = None  # 대표 시장 한글 명
    antc_cnpr: str | None = None  # 예상 체결가
    antc_cntg_vrss_sign: str | None = None  # 예상 체결 대비 부호
    antc_cntg_vrss: str | None = None  # 예상 체결 대비
    antc_cntg_prdy_ctrt: str | None = None  # 예상 체결 전일 대비율
    antc_vol: str | None = None  # 예상 거래량
    antc_tr_pbmn: str | None = None  # 예상 거래대금

class ExpPriceTrendResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_cntg_hour: str | None = None  # 주식 체결 시간
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량

class ExpPriceTrendResponse(KisCommonResponse):
    """응답 본문."""

    output1: ExpPriceTrendResponse_Output1Item | None = None  # 응답상세
    output2: list[ExpPriceTrendResponse_Output2Item] = []  # 응답상세 — array

class ExpPriceTrendExecutor(ApiExecutor[ExpPriceTrendRequest, ExpPriceTrendResponse]):
    """국내주식 예상체결가 추이[국내주식-118]."""

    # 국내주식 예상체결가 추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0184] 예상체결지수 추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/exp-price-trend"
    METHOD = "GET"
    RESPONSE_TYPE = ExpPriceTrendResponse
    TR_ID = "FHPST01810000"
