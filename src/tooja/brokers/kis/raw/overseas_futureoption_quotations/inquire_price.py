"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquirePriceRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고

class InquirePriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    proc_date: str | None = None  # 최종처리일자
    high_price: str | None = None  # 고가 — 고가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    proc_time: str | None = None  # 최종처리시각
    open_price: str | None = None  # 시가 — 시가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    trst_mgn: str | None = None  # 증거금
    low_price: str | None = None  # 저가 — 저가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    last_price: str | None = None  # 현재가 — 현재가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    vol: str | None = None  # 누적거래수량
    prev_diff_flag: str | None = None  # 전일대비구분 — 전일대비구분 '1':상한 '2':상승 '3':보합 '4':하한 '5':하락
    prev_diff_price: str | None = None  # 전일대비가격
    prev_diff_rate: str | None = None  # 전일대비율
    bid_qntt: str | None = None  # 매수1수량
    bid_price: str | None = None  # 매수1호가 — 매수1호가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    ask_qntt: str | None = None  # 매도1수량
    ask_price: str | None = None  # 매도1호가 — 매도1호가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    prev_price: str | None = None  # 전일종가 — 전일종가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    exch_cd: str | None = None  # 거래소코드
    crc_cd: str | None = None  # 거래통화
    trd_fr_date: str | None = None  # 상장일
    expr_date: str | None = None  # 만기일
    trd_to_date: str | None = None  # 최종거래일
    remn_cnt: str | None = None  # 잔존일수
    last_qntt: str | None = None  # 체결량
    tot_ask_qntt: str | None = None  # 총매도잔량
    tot_bid_qntt: str | None = None  # 총매수잔량
    tick_size: str | None = None  # 틱사이즈
    open_date: str | None = None  # 장개시일자
    open_time: str | None = None  # 장개시시각
    close_date: str | None = None  # 장종료일자
    close_time: str | None = None  # 장종료시각
    sbsnsdate: str | None = None  # 영업일자
    sttl_price: str | None = None  # 정산가

class InquirePriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquirePriceResponse_Output1Item | None = None  # 응답상세1

class InquirePriceExecutor(ApiExecutor[InquirePriceRequest, InquirePriceResponse]):
    """해외선물종목현재가 [v1_해외선물-009]."""

    # (중요) 해외선물시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다. - ffcode.mst(해외선물종목마스터 파일) 다운로드 방법 2가지 1) 한국투자증권 Github의 파이썬 샘플코드를 사용하여 mst 파일 다운로드 및 excel 파일로 정제 https://github.com/koreainvestment/open-t

    PATH = "/uapi/overseas-futureoption/v1/quotations/inquire-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquirePriceResponse
    TR_ID = "HHDFC55010000"
