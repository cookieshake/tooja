"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class ColableByCompanyRequest(KisBaseModel):
    """요청."""

    PDNO: str  # 상품번호 — ex)AMD
    PRDT_TYPE_CD: str  # 상품유형코드 — 공백
    INQR_STRT_DT: str  # 조회시작일자 — 공백
    INQR_END_DT: str  # 조회종료일자 — 공백
    INQR_DVSN: str  # 조회구분 — 공백
    NATN_CD: str  # 국가코드 — 840(미국), 344(홍콩), 156(중국)
    INQR_SQN_DVSN: str  # 조회순서구분 — 01(이름순), 02(코드순)
    RT_DVSN_CD: str  # 비율구분코드 — 공백
    RT: str  # 비율 — 공백
    LOAN_PSBL_YN: str  # 대출가능여부 — 공백
    CTX_AREA_FK100: str  # 연속조회검색조건100 — 공백
    CTX_AREA_NK100: str  # 연속조회키100 — 공백

class ColableByCompanyResponse_Output1Item(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    ovrs_item_name: str | None = None  # 해외종목명
    loan_rt: str | None = None  # 대출비율
    mgge_mntn_rt: str | None = None  # 담보유지비율
    mgge_ensu_rt: str | None = None  # 담보확보비율
    loan_exec_psbl_yn: str | None = None  # 대출실행가능여부
    stff_name: str | None = None  # 직원명
    erlm_dt: str | None = None  # 등록일자
    tr_mket_name: str | None = None  # 거래시장명
    crcy_cd: str | None = None  # 통화코드
    natn_kor_name: str | None = None  # 국가한글명
    ovrs_excg_cd: str | None = None  # 해외거래소코드

class ColableByCompanyResponse_Output2Item(KisBaseModel):
    """nested item."""

    loan_psbl_item_num: str | None = None  # 대출가능종목수

class ColableByCompanyResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[str] = []  # 응답상세
    output2: ColableByCompanyResponse_Output2Item | None = None  # 응답상세 — array

class ColableByCompanyExecutor(ApiExecutor[ColableByCompanyRequest, ColableByCompanyResponse]):
    """당사 해외주식담보대출 가능 종목 [해외주식-051]."""

    # 당사 해외주식담보대출 가능 종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0497] 당사 해외주식담보대출 가능 종목 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 한 번의 호출에 20건까지 조회가 가능하며 다음조회가 불가하기에, PDNO에 데이터 확인하고자 하는 종목코드를 입력하여 단건조회용으로 사용하시기 바랍니다.

    PATH = "/uapi/overseas-price/v1/quotations/colable-by-company"
    METHOD = "GET"
    RESPONSE_TYPE = ColableByCompanyResponse
    TR_ID = "CTLN4050R"
