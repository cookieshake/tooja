"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SearchInfoRequest(KisBaseModel):
    """요청."""

    PDNO: str  # 상품번호 — '주식(하이닉스) : 000660 (코드 : 300) 선물(101S12) : KR4101SC0009 (코드 : 301) 미국(AAPL) : AAPL (코드 : 512)'
    PRDT_TYPE_CD: str  # 상품유형코드 — '300 주식 301 선물옵션 302 채권 512 미국 나스닥 / 513 미국 뉴욕 / 529 미국 아멕스 515 일본 501 홍콩 / 543 홍콩CNY / 558 홍콩USD 507 베트남 하노이 / 508 베트남 호치민 551 중국 

class SearchInfoResponse_OutputItem(KisBaseModel):
    """nested item."""

    pdno: str | None = None  # 상품번호
    prdt_type_cd: str | None = None  # 상품유형코드
    prdt_name: str | None = None  # 상품명
    prdt_name120: str | None = None  # 상품명120
    prdt_abrv_name: str | None = None  # 상품약어명
    prdt_eng_name: str | None = None  # 상품영문명
    prdt_eng_name120: str | None = None  # 상품영문명120
    prdt_eng_abrv_name: str | None = None  # 상품영문약어명
    std_pdno: str | None = None  # 표준상품번호
    shtn_pdno: str | None = None  # 단축상품번호
    prdt_sale_stat_cd: str | None = None  # 상품판매상태코드
    prdt_risk_grad_cd: str | None = None  # 상품위험등급코드
    prdt_clsf_cd: str | None = None  # 상품분류코드
    prdt_clsf_name: str | None = None  # 상품분류명
    sale_strt_dt: str | None = None  # 판매시작일자
    sale_end_dt: str | None = None  # 판매종료일자
    wrap_asst_type_cd: str | None = None  # 랩어카운트자산유형코드
    ivst_prdt_type_cd: str | None = None  # 투자상품유형코드
    ivst_prdt_type_cd_name: str | None = None  # 투자상품유형코드명
    frst_erlm_dt: str | None = None  # 최초등록일자

class SearchInfoResponse(KisCommonResponse):
    """응답 본문."""

    output: SearchInfoResponse_OutputItem | None = None  # 응답상세1

class SearchInfoExecutor(ApiExecutor[SearchInfoRequest, SearchInfoResponse]):
    """상품기본조회[v1_국내주식-029]."""

    PATH = "/uapi/domestic-stock/v1/quotations/search-info"
    METHOD = "GET"
    RESPONSE_TYPE = SearchInfoResponse
    TR_ID = "CTPF1604R"
