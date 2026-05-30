"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class SearchOptDetailRequest(KisBaseModel):
    """요청."""

    QRY_CNT: str  # 요청개수 — 입력한 코드 개수
    SRS_CD_01: str  # 종목코드1 — SRS_CD_01부터 차례로 입력(ex ) OESU24 C5500 최대 30개 까지 가능
    SRS_CD_02___: str  # 종목코드2
    SRS_CD_30: str  # 종목코드30

class SearchOptDetailResponse_Output2Item(KisBaseModel):
    """nested item."""

    exch_cd: str | None = None  # 거래소코드
    clas_cd: str | None = None  # 품목종류
    crc_cd: str | None = None  # 거래통화
    sttl_price: str | None = None  # 정산가 — 정산가 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션
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

class SearchOptDetailResponse(KisCommonResponse):
    """응답 본문."""

    output2: list[SearchOptDetailResponse_Output2Item] = []  # 응답상세 — array

class SearchOptDetailExecutor(ApiExecutor[SearchOptDetailRequest, SearchOptDetailResponse]):
    """해외옵션 상품기본정보 [해외선물-041]."""

    # 해외옵션 상품기본정보 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0054] 관심종목 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. (중요) 해외옵션시세 출력값을 해석하실 때 focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니

    PATH = "/uapi/overseas-futureoption/v1/quotations/search-opt-detail"
    METHOD = "GET"
    RESPONSE_TYPE = SearchOptDetailResponse
    TR_ID = "HHDFO55200000"
