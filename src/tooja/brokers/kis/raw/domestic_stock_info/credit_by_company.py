"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class CreditByCompanyRequest(KisBaseModel):
    """요청."""

    fid_rank_sort_cls_code: str  # 순위 정렬 구분 코드 — 0:코드순, 1:이름순
    fid_slct_yn: str  # 선택 여부 — 0:신용주문가능, 1: 신용주문불가
    fid_input_iscd: str  # 입력 종목코드 — 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
    fid_cond_scr_div_code: str  # 조건 화면 분류 코드 — Unique key(20477)
    fid_cond_mrkt_div_code: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)

class CreditByCompanyResponse_OutputItem(KisBaseModel):
    """nested item."""

    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    crdt_rate: str | None = None  # 신용 비율

class CreditByCompanyResponse(KisCommonResponse):
    """응답 본문."""

    output: list[CreditByCompanyResponse_OutputItem] = []  # 응답상세 — array

class CreditByCompanyExecutor(ApiExecutor[CreditByCompanyRequest, CreditByCompanyResponse]):
    """국내주식 당사 신용가능종목[국내주식-111]."""

    # 국내주식 당사 신용가능종목 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0477] 당사 신용가능 종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 100건 확인 가능하며, 다음 조회가 불가합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/credit-by-company"
    METHOD = "GET"
    RESPONSE_TYPE = CreditByCompanyResponse
    TR_ID = "FHPST04770000"
