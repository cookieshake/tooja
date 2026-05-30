"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PeriodRightsRequest(KisBaseModel):
    """요청."""

    RGHT_TYPE_CD: str  # 권리유형코드 — '%%(전체), 01(유상), 02(무상), 03(배당), 11(합병), 14(액면분할), 15(액면병합), 17(감자), 54(WR청구), 61(원리금상환), 71(WR소멸), 74(배당옵션), 75(특별배당), 76(ISINCODE
    INQR_DVSN_CD: str  # 조회구분코드 — 02(현지기준일), 03(청약시작일), 04(청약종료일)
    INQR_STRT_DT: str  # 조회시작일자 — 일자 ~
    INQR_END_DT: str  # 조회종료일자 — ~ 일자
    PDNO: str  # 상품번호 — 공백
    PRDT_TYPE_CD: str  # 상품유형코드 — 공백
    CTX_AREA_NK50: str  # 연속조회키50 — 공백
    CTX_AREA_FK50: str  # 연속조회검색조건50 — 공백

class PeriodRightsResponse_OutputItem(KisBaseModel):
    """nested item."""

    bass_dt: str | None = None  # 기준일자
    rght_type_cd: str | None = None  # 권리유형코드
    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    prdt_type_cd: str | None = None  # 상품유형코드
    std_pdno: str | None = None  # 표준상품번호
    acpl_bass_dt: str | None = None  # 현지기준일자
    sbsc_strt_dt: str | None = None  # 청약시작일자
    sbsc_end_dt: str | None = None  # 청약종료일자
    cash_alct_rt: str | None = None  # 현금배정비율
    stck_alct_rt: str | None = None  # 주식배정비율
    crcy_cd: str | None = None  # 통화코드
    crcy_cd2: str | None = None  # 통화코드2
    crcy_cd3: str | None = None  # 통화코드3
    crcy_cd4: str | None = None  # 통화코드4
    alct_frcr_unpr: str | None = None  # 배정외화단가
    stkp_dvdn_frcr_amt2: str | None = None  # 주당배당외화금액2
    stkp_dvdn_frcr_amt3: str | None = None  # 주당배당외화금액3
    stkp_dvdn_frcr_amt4: str | None = None  # 주당배당외화금액4
    dfnt_yn: str | None = None  # 확정여부

class PeriodRightsResponse(KisCommonResponse):
    """응답 본문."""

    output: list[PeriodRightsResponse_OutputItem] = []  # 응답상세 — array

class PeriodRightsExecutor(ApiExecutor[PeriodRightsRequest, PeriodRightsResponse]):
    """해외주식 기간별권리조회 [해외주식-052]."""

    # 해외주식 기간별권리조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7520] 기간별해외증권권리조회 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 확정여부가 '예정'으로 표시되는 경우는 권리정보가 변경될 수 있으니 참고자료로만 활용하시기 바랍니다.

    PATH = "/uapi/overseas-price/v1/quotations/period-rights"
    METHOD = "GET"
    RESPONSE_TYPE = PeriodRightsResponse
    TR_ID = "CTRGT011R"
