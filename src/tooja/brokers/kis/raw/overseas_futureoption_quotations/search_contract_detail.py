"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SearchContractDetailRequest(KisBaseModel):
    """요청."""

    QRY_CNT: str  # 요청개수 — 입력한 코드 개수
    SRS_CD_01: str  # 품목종류 — 최대 32개 까지 가능
    SRS_CD_02_: str  # 품목종류…
    SRS_CD_32: str  # 품목종류

class SearchContractDetailResponse_Output2Item(KisBaseModel):
    """nested item."""

    exch_cd: str | None = None  # 거래소코드
    clas_cd: str | None = None  # 품목종류
    crc_cd: str | None = None  # 거래통화
    sttl_price: str | None = None  # 정산가
    sttl_date: str | None = None  # 정산일
    trst_mgn: str | None = None  # 증거금
    disp_digit: str | None = None  # 가격표시진법
    tick_sz: str | None = None  # 틱사이즈
    tick_val: str | None = None  # 틱가치
    mrkt_open_date: str | None = None  # 장개시일자
    mrkt_open_time: str | None = None  # 장개시시각
    mrkt_close_date: str | None = None  # 장마감일자
    mrkt_close_time: str | None = None  # 장마감시각
    trd_fr_date: str | None = None  # 상장일
    expr_date: str | None = None  # 만기일
    trd_to_date: str | None = None  # 최종거래일
    remn_cnt: str | None = None  # 잔존일수
    stat_tp: str | None = None  # 매매여부
    ctrt_size: str | None = None  # 계약크기
    stl_tp: str | None = None  # 최종결제구분
    frst_noti_date: str | None = None  # 최초식별일
    sub_exch_nm: str | None = None  # 서브거래소코드

class SearchContractDetailResponse(KisCommonResponse):
    """응답 본문."""

    output2: list[SearchContractDetailResponse_Output2Item] = []  # 응답상세 — array

class SearchContractDetailExecutor(ApiExecutor[SearchContractDetailRequest, SearchContractDetailResponse]):
    """해외선물 상품기본정보 [해외선물-023]."""

    # 해외선물옵션 상품기본정보 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0054] 해외선물옵션 상품기본정보 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. QRY_CNT에 SRS_CD 요청 개수 입력, SRS_CD_01 ~SRS_CD_32 까지 최대 32건의 상품코드 추가 입력하여 해외선물옵션 상품기본정보 확인이 가능합니다.

    PATH = "/uapi/overseas-futureoption/v1/quotations/search-contract-detail"
    METHOD = "GET"
    RESPONSE_TYPE = SearchContractDetailResponse
    TR_ID = "HHDFC55200000"
