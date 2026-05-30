"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class DisplayBoardCallputRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (O: 옵션)
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — Unique key(20503)
    FID_MRKT_CLS_CODE: str  # 시장 구분 코드 — 시장구분코드 (CO: 콜옵션)
    FID_MTRT_CNT: str  # 만기 수 — - FID_COND_MRKT_CLS_CODE : 공백(KOSPI200), MKI(미니KOSPI200), KQI(KOSDAQ150) 인 경우 : 만기년월(YYYYMM) 입력 (ex. 202407) - FID_COND_MRKT_CLS_CODE
    FID_COND_MRKT_CLS_CODE: str  # 조건 시장 구분 코드 — 공백: KOSPI200 MKI: 미니KOSPI200 WKM: KOSPI200위클리(월) WKI: KOSPI200위클리(목) KQI: KOSDAQ150
    FID_MRKT_CLS_CODE1: str  # 시장 구분 코드 — 시장구분코드 (PO: 풋옵션)

class DisplayBoardCallputResponse_Output1Item(KisBaseModel):
    """nested item."""

    acpr: str | None = None  # 행사가
    unch_prpr: str | None = None  # 환산 현재가
    optn_shrn_iscd: str | None = None  # 옵션 단축 종목코드
    optn_prpr: str | None = None  # 옵션 현재가
    optn_prdy_vrss: str | None = None  # 옵션 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    optn_prdy_ctrt: str | None = None  # 옵션 전일 대비율
    optn_bidp: str | None = None  # 옵션 매수호가
    optn_askp: str | None = None  # 옵션 매도호가
    tmvl_val: str | None = None  # 시간가치 값
    nmix_sdpr: str | None = None  # 지수 기준가
    acml_vol: str | None = None  # 누적 거래량
    seln_rsqn: str | None = None  # 매도 잔량
    shnu_rsqn: str | None = None  # 매수2 잔량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_otst_stpl_qty: str | None = None  # HTS 미결제 약정 수량
    otst_stpl_qty_icdc: str | None = None  # 미결제 약정 수량 증감
    delta_val: str | None = None  # 델타 값
    gama: str | None = None  # 감마
    vega: str | None = None  # 베가
    theta: str | None = None  # 세타
    rho: str | None = None  # 로우
    hts_ints_vltl: str | None = None  # HTS 내재 변동성
    invl_val: str | None = None  # 내재가치 값
    esdg: str | None = None  # 괴리도
    dprt: str | None = None  # 괴리율
    hist_vltl: str | None = None  # 역사적 변동성
    hts_thpr: str | None = None  # HTS 이론가
    optn_oprc: str | None = None  # 옵션 시가2
    optn_hgpr: str | None = None  # 옵션 최고가
    optn_lwpr: str | None = None  # 옵션 최저가
    optn_mxpr: str | None = None  # 옵션 상한가
    optn_llam: str | None = None  # 옵션 하한가
    atm_cls_name: str | None = None  # ATM 구분 명
    rgbf_vrss_icdc: str | None = None  # 직전 대비 증감
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    futs_antc_cnpr: str | None = None  # 선물예상체결가
    futs_antc_cntg_vrss: str | None = None  # 선물예상체결대비
    antc_cntg_vrss_sign: str | None = None  # 예상 체결 대비 부호
    antc_cntg_prdy_ctrt: str | None = None  # 예상 체결 전일 대비율

class DisplayBoardCallputResponse_Output2Item(KisBaseModel):
    """nested item."""

    acpr: str | None = None  # 행사가
    unch_prpr: str | None = None  # 환산 현재가
    optn_shrn_iscd: str | None = None  # 옵션 단축 종목코드
    optn_prpr: str | None = None  # 옵션 현재가
    optn_prdy_vrss: str | None = None  # 옵션 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    optn_prdy_ctrt: str | None = None  # 옵션 전일 대비율
    optn_bidp: str | None = None  # 옵션 매수호가
    optn_askp: str | None = None  # 옵션 매도호가
    tmvl_val: str | None = None  # 시간가치 값
    nmix_sdpr: str | None = None  # 지수 기준가
    acml_vol: str | None = None  # 누적 거래량
    seln_rsqn: str | None = None  # 매도 잔량
    shnu_rsqn: str | None = None  # 매수2 잔량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    hts_otst_stpl_qty: str | None = None  # HTS 미결제 약정 수량
    otst_stpl_qty_icdc: str | None = None  # 미결제 약정 수량 증감
    delta_val: str | None = None  # 델타 값
    gama: str | None = None  # 감마
    vega: str | None = None  # 베가
    theta: str | None = None  # 세타
    rho: str | None = None  # 로우
    hts_ints_vltl: str | None = None  # HTS 내재 변동성
    invl_val: str | None = None  # 내재가치 값
    esdg: str | None = None  # 괴리도
    dprt: str | None = None  # 괴리율
    hist_vltl: str | None = None  # 역사적 변동성
    hts_thpr: str | None = None  # HTS 이론가
    optn_oprc: str | None = None  # 옵션 시가2
    optn_hgpr: str | None = None  # 옵션 최고가
    optn_lwpr: str | None = None  # 옵션 최저가
    optn_mxpr: str | None = None  # 옵션 상한가
    optn_llam: str | None = None  # 옵션 하한가
    atm_cls_name: str | None = None  # ATM 구분 명
    rgbf_vrss_icdc: str | None = None  # 직전 대비 증감
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    futs_antc_cnpr: str | None = None  # 선물예상체결가
    futs_antc_cntg_vrss: str | None = None  # 선물예상체결대비
    antc_cntg_vrss_sign: str | None = None  # 예상 체결 대비 부호
    antc_cntg_prdy_ctrt: str | None = None  # 예상 체결 전일 대비율

class DisplayBoardCallputResponse(KisCommonResponse):
    """응답 본문."""

    output1: list[DisplayBoardCallputResponse_Output1Item] = []  # 응답상세 — array
    output2: list[DisplayBoardCallputResponse_Output2Item] = []  # 응답상세 — array

class DisplayBoardCallputExecutor(ApiExecutor[DisplayBoardCallputRequest, DisplayBoardCallputResponse]):
    """국내옵션전광판_콜풋[국내선물-022]."""

    # 국내옵션전광판_콜풋 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0503] 선물옵션 종합시세(Ⅰ) 화면의 "중앙" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. ※ output1, output2 각각 높은 행사가 순으로 100건까지만 확인이 가능합니다. ※ 조회시간이 긴 API인 점 참고 부탁드리며, 잦은 호출을 삼가해주시기 바랍니다. (1초당 최대 1건 권장)

    PATH = "/uapi/domestic-futureoption/v1/quotations/display-board-callput"
    METHOD = "GET"
    RESPONSE_TYPE = DisplayBoardCallputResponse
    TR_ID = "FHPIF05030100"
