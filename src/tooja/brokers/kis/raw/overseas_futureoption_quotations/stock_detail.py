"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class StockDetailRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고

class StockDetailResponse_Output1Item(KisBaseModel):
    """nested item."""

    exch_cd: str | None = None  # 거래소코드
    tick_sz: str | None = None  # 틱사이즈
    disp_digit: str | None = None  # 가격표시진법
    trst_mgn: str | None = None  # 증거금
    sttl_date: str | None = None  # 정산일
    prev_price: str | None = None  # 전일종가 — 전일종가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    crc_cd: str | None = None  # 거래통화
    clas_cd: str | None = None  # 품목종류
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
    sprd_srs_cd1: str | None = None  # 스프레드 종목 #1
    sprd_srs_cd2: str | None = None  # 스프레드 종목 #2

class StockDetailResponse(KisCommonResponse):
    """응답 본문."""

    output1: StockDetailResponse_Output1Item | None = None  # 응답상세1

class StockDetailExecutor(ApiExecutor[StockDetailRequest, StockDetailResponse]):
    """해외선물종목상세 [v1_해외선물-008]."""

    # (중요) 해외선물시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다. - ffcode.mst(해외선물종목마스터 파일) 다운로드 방법 2가지 1) 한국투자증권 Github의 파이썬 샘플코드를 사용하여 mst 파일 다운로드 및 excel 파일로 정제 https://github.com/koreainvestment/open-t

    PATH = "/uapi/overseas-futureoption/v1/quotations/stock-detail"
    METHOD = "GET"
    RESPONSE_TYPE = StockDetailResponse
    TR_ID = "HHDFC55010100"
