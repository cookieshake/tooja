"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireTimeFuturechartpriceRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목코드 — ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고
    EXCH_CD: str  # 거래소코드 — CME
    START_DATE_TIME: str  # 조회시작일시 — 공백
    CLOSE_DATE_TIME: str  # 조회종료일시 — ex) 20230823
    QRY_TP: str  # 조회구분 — Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
    QRY_CNT: str  # 요청개수 — 120 (조회갯수)
    QRY_GAP: str  # 묶음개수 — 5 (분간격)
    INDEX_KEY: str  # 이전조회KEY — 다음조회(QRY_TP를 P로 입력) 시, 이전 호출의 "output1 > index_key" 기입하여 조회

class InquireTimeFuturechartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    ret_cnt: str | None = None  # 자료개수
    last_n_cnt: str | None = None  # N틱최종개수
    index_key: str | None = None  # 이전조회KEY

class InquireTimeFuturechartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    data_date: str | None = None  # 일자
    data_time: str | None = None  # 시각
    open_price: str | None = None  # 시가
    high_price: str | None = None  # 고가
    low_price: str | None = None  # 저가
    last_price: str | None = None  # 체결가격 — 체결가격 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
    last_qntt: str | None = None  # 체결수량
    vol: str | None = None  # 누적거래수량
    prev_diff_flag: str | None = None  # 전일대비구분
    prev_diff_price: str | None = None  # 전일대비가격
    prev_diff_rate: str | None = None  # 전일대비율

class InquireTimeFuturechartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output2: InquireTimeFuturechartpriceResponse_Output2Item | None = None  # 응답상세
    output1: list[InquireTimeFuturechartpriceResponse_Output1Item] = []  # 응답상세 — array

class InquireTimeFuturechartpriceExecutor(ApiExecutor[InquireTimeFuturechartpriceRequest, InquireTimeFuturechartpriceResponse]):
    """해외선물 분봉조회[해외선물-016]."""

    # 해외선물분봉조회 API입니다. ★ 반드시 아래 호출방법을 확인하시고 호출 사용하시기 바랍니다. 한국투자 HTS(eFriend Plus) &gt; [5502] 해외선물옵션 체결추이 화면에서 "분" 선택 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ 해외선물분봉조회 조회 방법 params . START_DATE_TIME: 공란 입력 ("") . CLOSE_DATE_TIME: 조회일자 입

    PATH = "/uapi/overseas-futureoption/v1/quotations/inquire-time-futurechartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireTimeFuturechartpriceResponse
    TR_ID = "HHDFC55020400"
