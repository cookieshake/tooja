"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireOvertimePriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드

class InquireOvertimePriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    bstp_kor_isnm: str | None = None  # 업종 한글 종목명 — ※ 거래소 정보로 특정 종목은 업종구분이 없어 데이터 미회신
    mang_issu_cls_name: str | None = None  # 관리 종목 구분 명
    ovtm_untp_prpr: str | None = None  # 시간외 단일가 현재가
    ovtm_untp_prdy_vrss: str | None = None  # 시간외 단일가 전일 대비
    ovtm_untp_prdy_vrss_sign: str | None = None  # 시간외 단일가 전일 대비 부호
    ovtm_untp_prdy_ctrt: str | None = None  # 시간외 단일가 전일 대비율
    ovtm_untp_vol: str | None = None  # 시간외 단일가 거래량
    ovtm_untp_tr_pbmn: str | None = None  # 시간외 단일가 거래 대금
    ovtm_untp_mxpr: str | None = None  # 시간외 단일가 상한가
    ovtm_untp_llam: str | None = None  # 시간외 단일가 하한가
    ovtm_untp_oprc: str | None = None  # 시간외 단일가 시가2
    ovtm_untp_hgpr: str | None = None  # 시간외 단일가 최고가
    ovtm_untp_lwpr: str | None = None  # 시간외 단일가 최저가
    marg_rate: str | None = None  # 증거금 비율
    ovtm_untp_antc_cnpr: str | None = None  # 시간외 단일가 예상 체결가
    ovtm_untp_antc_cntg_vrss: str | None = None  # 시간외 단일가 예상 체결 대비
    ovtm_untp_antc_cntg_vrss_sign: str | None = None  # 시간외 단일가 예상 체결 대비
    ovtm_untp_antc_cntg_ctrt: str | None = None  # 시간외 단일가 예상 체결 대비율
    ovtm_untp_antc_cnqn: str | None = None  # 시간외 단일가 예상 체결량
    crdt_able_yn: str | None = None  # 신용 가능 여부
    new_lstn_cls_name: str | None = None  # 신규 상장 구분 명
    sltr_yn: str | None = None  # 정리매매 여부
    mang_issu_yn: str | None = None  # 관리 종목 여부
    mrkt_warn_cls_code: str | None = None  # 시장 경고 구분 코드
    trht_yn: str | None = None  # 거래정지 여부
    vlnt_deal_cls_name: str | None = None  # 임의 매매 구분 명
    ovtm_untp_sdpr: str | None = None  # 시간외 단일가 기준가
    mrkt_warn_cls_name: str | None = None  # 시장 경구 구분 명
    revl_issu_reas_name: str | None = None  # 재평가 종목 사유 명
    insn_pbnt_yn: str | None = None  # 불성실 공시 여부
    flng_cls_name: str | None = None  # 락 구분 이름
    rprs_mrkt_kor_name: str | None = None  # 대표 시장 한글 명
    ovtm_vi_cls_code: str | None = None  # 시간외단일가VI적용구분코드
    bidp: str | None = None  # 매수호가
    askp: str | None = None  # 매도호가

class InquireOvertimePriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireOvertimePriceResponse_OutputItem | None = None  # 응답상세

class InquireOvertimePriceExecutor(ApiExecutor[InquireOvertimePriceRequest, InquireOvertimePriceResponse]):
    """국내주식 시간외현재가[국내주식-076]."""

    # 국내주식 시간외현재가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0230] 시간외 현재가 화면의 좌측 상단기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-overtime-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireOvertimePriceResponse
    TR_ID = "FHPST02300000"
