"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class IntstockMultpriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE_1: str  # 조건 시장 분류 코드1 — 그룹별종목조회 결과 fid_mrkt_cls_code(시장구분) 1 입력 J: KRX, NX: NXT, UN: 통합 ex) J
    FID_INPUT_ISCD_1: str  # 입력 종목코드1 — 그룹별종목조회 결과 jong_code(종목코드) 1 입력 ex) 005930
    FID_COND_MRKT_DIV_CODE_2: str  # 조건 시장 분류 코드2
    FID_INPUT_ISCD_2: str  # 입력 종목코드2
    FID_COND_MRKT_DIV_CODE_3: str  # 조건 시장 분류 코드3
    FID_INPUT_ISCD_3: str  # 입력 종목코드3
    FID_COND_MRKT_DIV_CODE_4: str  # 조건 시장 분류 코드4
    FID_INPUT_ISCD_4: str  # 입력 종목코드4
    FID_COND_MRKT_DIV_CODE_5: str  # 조건 시장 분류 코드5
    FID_INPUT_ISCD_5: str  # 입력 종목코드5
    FID_COND_MRKT_DIV_CODE_6: str  # 조건 시장 분류 코드6
    FID_INPUT_ISCD_6: str  # 입력 종목코드6
    FID_COND_MRKT_DIV_CODE_7: str  # 조건 시장 분류 코드7
    FID_INPUT_ISCD_7: str  # 입력 종목코드7
    FID_COND_MRKT_DIV_CODE_8: str  # 조건 시장 분류 코드8
    FID_INPUT_ISCD_8: str  # 입력 종목코드8
    FID_COND_MRKT_DIV_CODE_9: str  # 조건 시장 분류 코드9
    FID_INPUT_ISCD_9: str  # 입력 종목코드9
    FID_COND_MRKT_DIV_CODE_10: str  # 조건 시장 분류 코드10
    FID_INPUT_ISCD_10: str  # 입력 종목코드10
    FID_COND_MRKT_DIV_CODE_11: str  # 조건 시장 분류 코드11
    FID_INPUT_ISCD_11: str  # 입력 종목코드11
    FID_COND_MRKT_DIV_CODE_12: str  # 조건 시장 분류 코드12
    FID_INPUT_ISCD_12: str  # 입력 종목코드12
    FID_COND_MRKT_DIV_CODE_13: str  # 조건 시장 분류 코드13
    FID_INPUT_ISCD_13: str  # 입력 종목코드13
    FID_COND_MRKT_DIV_CODE_14: str  # 조건 시장 분류 코드14
    FID_INPUT_ISCD_14: str  # 입력 종목코드14
    FID_COND_MRKT_DIV_CODE_15: str  # 조건 시장 분류 코드15
    FID_INPUT_ISCD_15: str  # 입력 종목코드15
    FID_COND_MRKT_DIV_CODE_16: str  # 조건 시장 분류 코드16
    FID_INPUT_ISCD_16: str  # 입력 종목코드16
    FID_COND_MRKT_DIV_CODE_17: str  # 조건 시장 분류 코드17
    FID_INPUT_ISCD_17: str  # 입력 종목코드17
    FID_COND_MRKT_DIV_CODE_18: str  # 조건 시장 분류 코드18
    FID_INPUT_ISCD_18: str  # 입력 종목코드18
    FID_COND_MRKT_DIV_CODE_19: str  # 조건 시장 분류 코드19
    FID_INPUT_ISCD_19: str  # 입력 종목코드19
    FID_COND_MRKT_DIV_CODE_20: str  # 조건 시장 분류 코드20
    FID_INPUT_ISCD_20: str  # 입력 종목코드20
    FID_COND_MRKT_DIV_CODE_21: str  # 조건 시장 분류 코드21
    FID_INPUT_ISCD_21: str  # 입력 종목코드21
    FID_COND_MRKT_DIV_CODE_22: str  # 조건 시장 분류 코드22
    FID_INPUT_ISCD_22: str  # 입력 종목코드22
    FID_COND_MRKT_DIV_CODE_23: str  # 조건 시장 분류 코드23
    FID_INPUT_ISCD_23: str  # 입력 종목코드23
    FID_COND_MRKT_DIV_CODE_24: str  # 조건 시장 분류 코드24
    FID_INPUT_ISCD_24: str  # 입력 종목코드24
    FID_COND_MRKT_DIV_CODE_25: str  # 조건 시장 분류 코드25
    FID_INPUT_ISCD_25: str  # 입력 종목코드25
    FID_COND_MRKT_DIV_CODE_26: str  # 조건 시장 분류 코드26
    FID_INPUT_ISCD_26: str  # 입력 종목코드26
    FID_COND_MRKT_DIV_CODE_27: str  # 조건 시장 분류 코드27
    FID_INPUT_ISCD_27: str  # 입력 종목코드27
    FID_COND_MRKT_DIV_CODE_28: str  # 조건 시장 분류 코드28
    FID_INPUT_ISCD_28: str  # 입력 종목코드28
    FID_COND_MRKT_DIV_CODE_29: str  # 조건 시장 분류 코드29
    FID_INPUT_ISCD_29: str  # 입력 종목코드29
    FID_COND_MRKT_DIV_CODE_30: str  # 조건 시장 분류 코드30
    FID_INPUT_ISCD_30: str  # 입력 종목코드30

class IntstockMultpriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    kospi_kosdaq_cls_name: str | None = None  # 코스피 코스닥 구분 명
    mrkt_trtm_cls_name: str | None = None  # 시장 조치 구분 명
    hour_cls_code: str | None = None  # 시간 구분 코드
    inter_shrn_iscd: str | None = None  # 관심 단축 종목코드
    inter_kor_isnm: str | None = None  # 관심 한글 종목명
    inter2_prpr: str | None = None  # 관심2 현재가
    inter2_prdy_vrss: str | None = None  # 관심2 전일 대비
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    inter2_oprc: str | None = None  # 관심2 시가
    inter2_hgpr: str | None = None  # 관심2 고가
    inter2_lwpr: str | None = None  # 관심2 저가
    inter2_llam: str | None = None  # 관심2 하한가
    inter2_mxpr: str | None = None  # 관심2 상한가
    inter2_askp: str | None = None  # 관심2 매도호가
    inter2_bidp: str | None = None  # 관심2 매수호가
    seln_rsqn: str | None = None  # 매도 잔량
    shnu_rsqn: str | None = None  # 매수2 잔량
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    acml_tr_pbmn: str | None = None  # 누적 거래 대금
    inter2_prdy_clpr: str | None = None  # 관심2 전일 종가
    oprc_vrss_hgpr_rate: str | None = None  # 시가 대비 최고가 비율
    intr_antc_cntg_vrss: str | None = None  # 관심 예상 체결 대비
    intr_antc_cntg_vrss_sign: str | None = None  # 관심 예상 체결 대비 부호
    intr_antc_cntg_prdy_ctrt: str | None = None  # 관심 예상 체결 전일 대비율
    intr_antc_vol: str | None = None  # 관심 예상 거래량
    inter2_sdpr: str | None = None  # 관심2 기준가

class IntstockMultpriceResponse(KisCommonResponse):
    """응답 본문."""

    output: IntstockMultpriceResponse_OutputItem | None = None  # 응답상세

class IntstockMultpriceExecutor(ApiExecutor[IntstockMultpriceRequest, IntstockMultpriceResponse]):
    """관심종목(멀티종목) 시세조회 [국내주식-205]."""

    # 관심종목(멀티종목) 시세조회 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0161] 관심종목 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/intstock-multprice"
    METHOD = "GET"
    RESPONSE_TYPE = IntstockMultpriceResponse
    TR_ID = "FHKST11300006"
