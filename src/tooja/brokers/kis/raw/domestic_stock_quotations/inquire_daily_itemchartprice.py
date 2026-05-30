"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireDailyItemchartpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)
    FID_INPUT_DATE_1: str  # 입력 날짜 1 — 조회 시작일자
    FID_INPUT_DATE_2: str  # 입력 날짜 2 — 조회 종료일자 (최대 100개)
    FID_PERIOD_DIV_CODE: str  # 기간분류코드 — D:일봉 W:주봉, M:월봉, Y:년봉
    FID_ORG_ADJ_PRC: str  # 수정주가 원주가 가격 여부 — 0:수정주가 1:원주가

class InquireDailyItemchartpriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    prdy_vrss: str | None = None  # 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    stck_prdy_clpr: str | None = None  # 주식 전일 종가
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    stck_prpr: str | None = None  # 주식 현재가
    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    prdy_vol: str | None = None  # 전일 거래량
    stck_mxpr: str | None = None  # 주식 상한가
    stck_llam: str | None = None  # 주식 하한가
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    stck_prdy_oprc: str | None = None  # 주식 전일 시가
    stck_prdy_hgpr: str | None = None  # 주식 전일 최고가
    stck_prdy_lwpr: str | None = None  # 주식 전일 최저가
    askp: str | None = None  # 매도호가
    bidp: str | None = None  # 매수호가
    prdy_vrss_vol: str | None = None  # 전일 대비 거래량
    vol_tnrt: str | None = None  # 거래량 회전율 — 11(8.2)
    stck_fcam: str | None = None  # 주식 액면가
    lstn_stcn: str | None = None  # 상장 주수
    cpfn: str | None = None  # 자본금
    hts_avls: str | None = None  # HTS 시가총액
    per: str | None = None  # PER — 11(8.2)
    eps: str | None = None  # EPS — 14(11.2)
    pbr: str | None = None  # PBR — 11(8.2)
    itewhol_loan_rmnd_ratem: str | None = None  # 전체 융자 잔고 비율 — 13(8.4)

class InquireDailyItemchartpriceResponse_Output2Item(KisBaseModel):
    """nested item."""

    stck_bsop_date: str | None = None  # 주식 영업 일자
    stck_clpr: str | None = None  # 주식 종가
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    acml_vol: str | None = None  # 누적 거래량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    flng_cls_code: str | None = None  # 락 구분 코드 — 01 : 권리락 02 : 배당락 03 : 분배락 04 : 권배락 05 : 중간(분기)배당락 06 : 권리중간배당락 07 : 권리분기배당락
    prtt_rate: str | None = None  # 분할 비율 — 기준가/전일 종가
    mod_yn: str | None = None  # 변경 여부 — 현재 영업일에 체결이 발생하지 않아 시가가 없을경우 Y 로 표시(차트에서 사용)
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    revl_issu_reas: str | None = None  # 재평가사유코드 — 00:해당없음 01:회사분할 02:자본감소 03:장기간정지 04:초과분배 05:대규모배당 06:회사분할합병 07:ETN증권병합/분할 08:신종증권기세조정 99:기타

class InquireDailyItemchartpriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireDailyItemchartpriceResponse_Output1Item | None = None  # 응답상세 — single
    output2: list[InquireDailyItemchartpriceResponse_Output2Item] = []  # 응답상세 — Array

class InquireDailyItemchartpriceExecutor(ApiExecutor[InquireDailyItemchartpriceRequest, InquireDailyItemchartpriceResponse]):
    """국내주식기간별시세(일/주/월/년)[v1_국내주식-016]."""

    # 국내주식기간별시세(일/주/월/년) API입니다. 실전계좌/모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    METHOD = "GET"
    RESPONSE_TYPE = InquireDailyItemchartpriceResponse
    TR_ID = "FHKST03010100"
