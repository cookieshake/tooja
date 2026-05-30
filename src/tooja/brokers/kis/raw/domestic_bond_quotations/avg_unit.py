"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class AvgUnitRequest(KisBaseModel):
    """요청."""

    INQR_STRT_DT: str  # 조회시작일자 — 일자 ~
    INQR_END_DT: str  # 조회종료일자 — ~ 일자
    PDNO: str  # 상품번호 — 공백: 전체, 특정종목 조회시 : 종목코드
    PRDT_TYPE_CD: str  # 상품유형코드 — Unique key(302)
    VRFC_KIND_CD: str  # 검증종류코드 — Unique key(00)
    CTX_AREA_NK30: str  # 연속조회키30 — 공백
    CTX_AREA_FK100: str  # 연속조회검색조건100 — 공백

class AvgUnitResponse_Output1Item(KisBaseModel):
    """nested item."""

    evlu_dt: str | None = None  # 평가일자
    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    prdt_name: str | None = None  # 상품명
    kis_unpr: str | None = None  # 한국신용평가단가
    kbp_unpr: str | None = None  # 한국채권평가단가
    nice_evlu_unpr: str | None = None  # 한국신용정보평가단가
    fnp_unpr: str | None = None  # 에프앤자산평가단가
    avg_evlu_unpr: str | None = None  # 평균평가단가
    kis_crdt_grad_text: str | None = None  # 한국신용평가신용등급내용
    kbp_crdt_grad_text: str | None = None  # 한국채권평가신용등급내용
    nice_crdt_grad_text: str | None = None  # 한국신용정보신용등급내용
    fnp_crdt_grad_text: str | None = None  # 에프앤자산평가신용등급내용
    chng_yn: str | None = None  # 변경여부
    kis_erng_rt: str | None = None  # 한국신용평가수익율
    kbp_erng_rt: str | None = None  # 한국채권평가수익율
    nice_evlu_erng_rt: str | None = None  # 한국신용정보평가수익율
    fnp_erng_rt: str | None = None  # 에프앤자산평가수익율
    avg_evlu_erng_rt: str | None = None  # 평균평가수익율
    kis_rf_unpr: str | None = None  # 한국신용평가RF단가
    kbp_rf_unpr: str | None = None  # 한국채권평가RF단가
    nice_evlu_rf_unpr: str | None = None  # 한국신용정보평가RF단가
    avg_evlu_rf_unpr: str | None = None  # 평균평가RF단가

class AvgUnitResponse_Output2Item(KisBaseModel):
    """nested item."""

    evlu_dt: str | None = None  # 평가일자
    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    prdt_name: str | None = None  # 상품명
    kis_evlu_amt: str | None = None  # 한국신용평가평가금액
    kbp_evlu_amt: str | None = None  # 한국채권평가평가금액
    nice_evlu_amt: str | None = None  # 한국신용정보평가금액
    fnp_evlu_amt: str | None = None  # 에프앤자산평가평가금액
    avg_evlu_amt: str | None = None  # 평균평가금액
    chng_yn: str | None = None  # 변경여부

class AvgUnitResponse_Output3Item(KisBaseModel):
    """nested item."""

    evlu_dt: str | None = None  # 평가일자
    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    prdt_name: str | None = None  # 상품명
    kis_crcy_cd: str | None = None  # 한국신용평가통화코드
    kis_evlu_unit_pric: str | None = None  # 한국신용평가평가단위가격
    kis_evlu_pric: str | None = None  # 한국신용평가평가가격
    kbp_crcy_cd: str | None = None  # 한국채권평가통화코드
    kbp_evlu_unit_pric: str | None = None  # 한국채권평가평가단위가격
    kbp_evlu_pric: str | None = None  # 한국채권평가평가가격
    nice_crcy_cd: str | None = None  # 한국신용정보통화코드
    nice_evlu_unit_pric: str | None = None  # 한국신용정보평가단위가격
    nice_evlu_pric: str | None = None  # 한국신용정보평가가격
    avg_evlu_unit_pric: str | None = None  # 평균평가단위가격
    avg_evlu_pric: str | None = None  # 평균평가가격
    chng_yn: str | None = None  # 변경여부

class AvgUnitResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[AvgUnitResponse_Output1Item] = []  # 응답상세 — array
    output2: list[AvgUnitResponse_Output2Item] = []  # 응답상세 — array
    output3: list[AvgUnitResponse_Output3Item] = []  # 응답상세 — array

class AvgUnitExecutor(ApiExecutor[AvgUnitRequest, AvgUnitResponse]):
    """장내채권 평균단가조회 [국내주식-158]."""

    # 장내채권 평균단가조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [7216] 채권 발행정보 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-bond/v1/quotations/avg-unit"
    METHOD = "GET"
    RESPONSE_TYPE = AvgUnitResponse
    TR_ID = "CTPF2005R"
