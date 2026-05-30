"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DailyLoanTransRequest(KisBaseModel):
    """요청."""

    MRKT_DIV_CLS_CODE: str  # 조회구분 — 1(코스피), 2(코스닥), 3(종목)
    MKSC_SHRN_ISCD: str  # 종목코드
    START_DATE: str  # 조회시작일시 — 조회기간 ~
    END_DATE: str  # 조회종료일시 — ~ 조회기간
    CTS: str  # 이전조회KEY

class DailyLoanTransResponse_Output1Item(KisBaseModel):
    """nested item."""

    bsop_date: str | None = None  # 일자
    stck_prpr: str | None = None  # 주식 종가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    new_stcn: str | None = None  # 당일 증가 주수 (체결)
    rdmp_stcn: str | None = None  # 당일 감소 주수 (상환)
    prdy_rmnd_vrss: str | None = None  # 대차거래 증감
    rmnd_stcn: str | None = None  # 당일 잔고 주수
    rmnd_amt: str | None = None  # 당일 잔고 금액

class DailyLoanTransResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[DailyLoanTransResponse_Output1Item] = []  # 응답상세 — array

class DailyLoanTransExecutor(ApiExecutor[DailyLoanTransRequest, DailyLoanTransResponse]):
    """종목별 일별 대차거래추이 [국내주식-135]."""

    # 종목별 일별 대차거래추이 API입니다. 한 번의 조회에 최대 100건까지 조회 가능하며, start_date, end_date 를 수정하여 다음 조회가 가능합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/daily-loan-trans"
    METHOD = "GET"
    RESPONSE_TYPE = DailyLoanTransResponse
    TR_ID = "HHPST074500C0"
