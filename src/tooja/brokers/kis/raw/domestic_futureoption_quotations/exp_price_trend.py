"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ExpPriceTrendRequest(KisBaseModel):
    """요청."""

    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목번호 (지수선물:6자리, 지수옵션 9자리)
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — F : 지수선물, O : 지수옵션

class ExpPriceTrendResponse_Output1Item(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # 영업 시간
    futs_antc_cnpr: str | None = None  # 업종 지수 현재가
    antc_cntg_vrss_sign: str | None = None  # 업종 지수 전일 대비
    futs_antc_cntg_vrss: str | None = None  # 전일 대비 부호
    antc_cntg_prdy_ctrt: str | None = None  # 업종 지수 전일 대비율
    futs_sdpr: str | None = None  # 누적 거래 대금

class ExpPriceTrendResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_cntg_hour: str | None = None  # 주식체결시간
    futs_antc_cnpr: str | None = None  # 선물예상체결가
    antc_cntg_vrss_sign: str | None = None  # 예상체결대비부호
    futs_antc_cntg_vrss: str | None = None  # 선물예상체결대비
    antc_cntg_prdy_ctrt: str | None = None  # 예상체결전일대비율

class ExpPriceTrendResponse(KisCommonResponse):
    """응답 본문."""

    output1: ExpPriceTrendResponse_Output1Item | None = None  # 응답상세
    output2: list[ExpPriceTrendResponse_Output2Item] = []  # 응답상세 — array

class ExpPriceTrendExecutor(ApiExecutor[ExpPriceTrendRequest, ExpPriceTrendResponse]):
    """선물옵션 일중예상체결추이[국내선물-018]."""

    # 선물옵션 일중예상체결추이 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0548] 선물옵션 예상체결추이 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-futureoption/v1/quotations/exp-price-trend"
    METHOD = "GET"
    RESPONSE_TYPE = ExpPriceTrendResponse
    TR_ID = "FHPIF05110100"
