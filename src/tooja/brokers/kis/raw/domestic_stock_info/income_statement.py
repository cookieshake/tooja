"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IncomeStatementRequest(KisBaseModel):
    """요청."""

    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 0: 년, 1: 분기 ※ 분기데이터는 연단위 누적합산
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — J
    fid_input_iscd: str  # 입력 종목코드 — 000660 : 종목코드

class IncomeStatementResponse_OutputItem(KisBaseModel):
    """nested item."""

    stac_yymm: str | None = None  # 결산 년월
    sale_account: str | None = None  # 매출액
    sale_cost: str | None = None  # 매출 원가
    sale_totl_prfi: str | None = None  # 매출 총 이익
    depr_cost: str | None = None  # 감가상각비 — 출력되지 않는 데이터(99.99 로 표시)
    sell_mang: str | None = None  # 판매 및 관리비 — 출력되지 않는 데이터(99.99 로 표시)
    bsop_prti: str | None = None  # 영업 이익
    bsop_non_ernn: str | None = None  # 영업 외 수익 — 출력되지 않는 데이터(99.99 로 표시)
    bsop_non_expn: str | None = None  # 영업 외 비용 — 출력되지 않는 데이터(99.99 로 표시)
    op_prfi: str | None = None  # 경상 이익
    spec_prfi: str | None = None  # 특별 이익
    spec_loss: str | None = None  # 특별 손실
    thtr_ntin: str | None = None  # 당기순이익

class IncomeStatementResponse(KisCommonResponse):
    """응답 본문."""

    output: list[IncomeStatementResponse_OutputItem] = []  # 응답상세 — array

class IncomeStatementExecutor(ApiExecutor[IncomeStatementRequest, IncomeStatementResponse]):
    """국내주식 손익계산서[v1_국내주식-079]."""

    # 국내주식 손익계산서 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0635] 재무분석종합 화면의 하단 '2. 손익계산서' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/finance/income-statement"
    METHOD = "GET"
    RESPONSE_TYPE = IncomeStatementResponse
    TR_ID = "FHKST66430200"
