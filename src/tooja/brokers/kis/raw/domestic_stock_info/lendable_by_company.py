"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class LendableByCompanyRequest(KisBaseModel):
    """요청."""

    EXCG_DVSN_CD: str  # 거래소구분코드 — 00(전체), 02(거래소), 03(코스닥)
    PDNO: str  # 상품번호 — 공백 : 전체조회, 종목코드 입력 시 해당종목만 조회
    THCO_STLN_PSBL_YN: str  # 당사대주가능여부 — Y
    INQR_DVSN_1: str  # 조회구분1 — 0 : 전체조회, 1: 종목코드순 정렬
    CTX_AREA_FK200: str  # 연속조회검색조건200 — 미입력 (다음조회 불가)
    CTX_AREA_NK100: str  # 연속조회키100 — 미입력 (다음조회 불가)

class LendableByCompanyResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_name: str | None = None  # 상품명
    papr: str | None = None  # 액면가
    bfdy_clpr: str | None = None  # 전일종가
    sbst_prvs: str | None = None  # 대용가
    tr_stop_dvsn_name: str | None = None  # 거래정지구분명
    psbl_yn_name: str | None = None  # 가능여부명
    lmt_qty1: str | None = None  # 한도수량1
    use_qty1: str | None = None  # 사용수량1
    trad_psbl_qty2: str | None = None  # 매매가능수량2 — 가능수량
    rght_type_cd: str | None = None  # 권리유형코드
    bass_dt: str | None = None  # 기준일자
    psbl_yn: str | None = None  # 가능여부

class LendableByCompanyResponse_Output2Item(KisBaseModel):
    """nested item."""

    tot_stup_lmt_qty: str | None = None  # 총설정한도수량
    brch_lmt_qty: str | None = None  # 지점한도수량
    rqst_psbl_qty: str | None = None  # 신청가능수량

class LendableByCompanyResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[LendableByCompanyResponse_Output1Item] = []  # 응답상세 — array
    output2: LendableByCompanyResponse_Output2Item | None = None  # 응답상세

class LendableByCompanyExecutor(ApiExecutor[LendableByCompanyRequest, LendableByCompanyResponse]):
    """당사 대주가능 종목 [국내주식-195]."""

    # 당사 대주가능 종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0490] 당사 대주가능 종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 본 API는 다음조회가 불가합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/lendable-by-company"
    METHOD = "GET"
    RESPONSE_TYPE = LendableByCompanyResponse
    TR_ID = "CTSC2702R"
