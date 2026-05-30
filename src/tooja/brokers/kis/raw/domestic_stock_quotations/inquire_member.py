"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireMemberRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # FID 입력 종목코드 — 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)

class InquireMemberResponse_OutputItem(KisBaseModel):
    """nested item."""

    seln_mbcr_no1: str | None = None  # 매도 회원사 번호1
    seln_mbcr_no2: str | None = None  # 매도 회원사 번호2
    seln_mbcr_no3: str | None = None  # 매도 회원사 번호3
    seln_mbcr_no4: str | None = None  # 매도 회원사 번호4
    seln_mbcr_no5: str | None = None  # 매도 회원사 번호5
    seln_mbcr_name1: str | None = None  # 매도 회원사 명1
    seln_mbcr_name2: str | None = None  # 매도 회원사 명2
    seln_mbcr_name3: str | None = None  # 매도 회원사 명3
    seln_mbcr_name4: str | None = None  # 매도 회원사 명4
    seln_mbcr_name5: str | None = None  # 매도 회원사 명5
    total_seln_qty1: str | None = None  # 총 매도 수량1
    total_seln_qty2: str | None = None  # 총 매도 수량2
    total_seln_qty3: str | None = None  # 총 매도 수량3
    total_seln_qty4: str | None = None  # 총 매도 수량4
    total_seln_qty5: str | None = None  # 총 매도 수량5
    seln_mbcr_rlim1: str | None = None  # 매도 회원사 비중1
    seln_mbcr_rlim2: str | None = None  # 매도 회원사 비중2
    seln_mbcr_rlim3: str | None = None  # 매도 회원사 비중3
    seln_mbcr_rlim4: str | None = None  # 매도 회원사 비중4
    seln_mbcr_rlim5: str | None = None  # 매도 회원사 비중5
    seln_qty_icdc1: str | None = None  # 매도 수량 증감1
    seln_qty_icdc2: str | None = None  # 매도 수량 증감2
    seln_qty_icdc3: str | None = None  # 매도 수량 증감3
    seln_qty_icdc4: str | None = None  # 매도 수량 증감4
    seln_qty_icdc5: str | None = None  # 매도 수량 증감5
    shnu_mbcr_no1: str | None = None  # 매수2 회원사 번호1
    shnu_mbcr_no2: str | None = None  # 매수2 회원사 번호2
    shnu_mbcr_no3: str | None = None  # 매수2 회원사 번호3
    shnu_mbcr_no4: str | None = None  # 매수2 회원사 번호4
    shnu_mbcr_no5: str | None = None  # 매수2 회원사 번호5
    shnu_mbcr_name1: str | None = None  # 매수2 회원사 명1
    shnu_mbcr_name2: str | None = None  # 매수2 회원사 명2
    shnu_mbcr_name3: str | None = None  # 매수2 회원사 명3
    shnu_mbcr_name4: str | None = None  # 매수2 회원사 명4
    shnu_mbcr_name5: str | None = None  # 매수2 회원사 명5
    total_shnu_qty1: str | None = None  # 총 매수2 수량1
    total_shnu_qty2: str | None = None  # 총 매수2 수량2
    total_shnu_qty3: str | None = None  # 총 매수2 수량3
    total_shnu_qty4: str | None = None  # 총 매수2 수량4
    total_shnu_qty5: str | None = None  # 총 매수2 수량5
    shnu_mbcr_rlim1: str | None = None  # 매수2 회원사 비중1
    shnu_mbcr_rlim2: str | None = None  # 매수2 회원사 비중2
    shnu_mbcr_rlim3: str | None = None  # 매수2 회원사 비중3
    shnu_mbcr_rlim4: str | None = None  # 매수2 회원사 비중4
    shnu_mbcr_rlim5: str | None = None  # 매수2 회원사 비중5
    shnu_qty_icdc1: str | None = None  # 매수2 수량 증감1
    shnu_qty_icdc2: str | None = None  # 매수2 수량 증감2
    shnu_qty_icdc3: str | None = None  # 매수2 수량 증감3
    shnu_qty_icdc4: str | None = None  # 매수2 수량 증감4
    shnu_qty_icdc5: str | None = None  # 매수2 수량 증감5
    glob_total_seln_qty: str | None = None  # 외국계 총 매도 수량
    glob_seln_rlim: str | None = None  # 외국계 매도 비중
    glob_ntby_qty: str | None = None  # 외국계 순매수 수량
    glob_total_shnu_qty: str | None = None  # 외국계 총 매수2 수량
    glob_shnu_rlim: str | None = None  # 외국계 매수2 비중
    seln_mbcr_glob_yn_1: str | None = None  # 매도 회원사 외국계 여부1
    seln_mbcr_glob_yn_2: str | None = None  # 매도 회원사 외국계 여부2
    seln_mbcr_glob_yn_3: str | None = None  # 매도 회원사 외국계 여부3
    seln_mbcr_glob_yn_4: str | None = None  # 매도 회원사 외국계 여부4
    seln_mbcr_glob_yn_5: str | None = None  # 매도 회원사 외국계 여부5
    shnu_mbcr_glob_yn_1: str | None = None  # 매수2 회원사 외국계 여부1
    shnu_mbcr_glob_yn_2: str | None = None  # 매수2 회원사 외국계 여부2
    shnu_mbcr_glob_yn_3: str | None = None  # 매수2 회원사 외국계 여부3
    shnu_mbcr_glob_yn_4: str | None = None  # 매수2 회원사 외국계 여부4
    shnu_mbcr_glob_yn_5: str | None = None  # 매수2 회원사 외국계 여부5
    glob_total_seln_qty_icdc: str | None = None  # 외국계 총 매도 수량 증감
    glob_total_shnu_qty_icdc: str | None = None  # 외국계 총 매수2 수량 증감

class InquireMemberResponse(KisCommonResponse):
    """응답 본문."""

    output: list[str] = []  # 응답상세

class InquireMemberExecutor(ApiExecutor[InquireMemberRequest, InquireMemberResponse]):
    """주식현재가 회원사[v1_국내주식-013]."""

    # 주식 현재가 회원사 API입니다. 회원사의 투자 정보를 확인할 수 있습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-member"
    METHOD = "GET"
    RESPONSE_TYPE = InquireMemberResponse
    TR_ID = "FHKST01010600"
