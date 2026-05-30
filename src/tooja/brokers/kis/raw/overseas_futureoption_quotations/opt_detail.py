"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class OptDetailRequest(KisBaseModel):
    """요청."""

    SRS_CD: str  # 종목명 — ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고

class OptDetailResponse_Output1Item(KisBaseModel):
    """nested item."""

    exch_cd: str | None = None  # 거래소코드
    clas_cd: str | None = None  # 품목종류
    crc_cd: str | None = None  # 거래통화
    sttl_price: str | None = None  # 전일종가 — (★주의) 정산가 X 전일종가 O 가 수신됨 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션
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

class OptDetailResponse(KisCommonResponse):
    """응답 본문."""

    output1: OptDetailResponse_Output1Item | None = None  # 응답상세

class OptDetailExecutor(ApiExecutor[OptDetailRequest, OptDetailResponse]):
    """해외옵션종목상세 [해외선물-034]."""

    # 해외옵션종목상세 API입니다. (주의) sstl_price 자리에 정산가 X 전일종가 O 가 수신되는 점 유의 부탁드립니다. (중요) 해외옵션시세 출력값을 해석하실 때 focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다. - focode.mst(해외지수옵션 종목마스터파일), fostkco

    PATH = "/uapi/overseas-futureoption/v1/quotations/opt-detail"
    METHOD = "GET"
    RESPONSE_TYPE = OptDetailResponse
    TR_ID = "HHDFO55010100"
