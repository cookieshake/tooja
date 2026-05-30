"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class MandDepositRequest(KisBaseModel):
    """요청."""

    T_DT: str  # 조회일자To — ~ 일자
    SHT_CD: str  # 종목코드 — 공백: 전체, 특정종목 조회시 : 종목코드
    F_DT: str  # 조회일자From — 일자 ~
    CTS: str  # CTS — 공백

class MandDepositResponse_Output1Item(KisBaseModel):
    """nested item."""

    sht_cd: str | None = None  # 종목코드
    isin_name: str | None = None  # 종목명
    stk_qty: str | None = None  # 주식수
    depo_date: str | None = None  # 예치일
    depo_reason: str | None = None  # 사유
    tot_issue_qty_per_rate: str | None = None  # 총발행주식수대비비율(%)

class MandDepositResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[MandDepositResponse_Output1Item] = []  # 응답상세 — array

class MandDepositExecutor(ApiExecutor[MandDepositRequest, MandDepositResponse]):
    """예탁원정보(의무예치일정)[국내주식-153]."""

    # 예탁원정보(의무예치일정) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0758] 의무예치 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.

    PATH = "/uapi/domestic-stock/v1/ksdinfo/mand-deposit"
    METHOD = "GET"
    RESPONSE_TYPE = MandDepositResponse
    TR_ID = "HHKDB669110C0"
