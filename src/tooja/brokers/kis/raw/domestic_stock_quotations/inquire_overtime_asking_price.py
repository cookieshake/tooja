"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireOvertimeAskingPriceRequest(KisBaseModel):
    """요청."""

    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드
    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — 시장구분코드 (주식 J)

class InquireOvertimeAskingPriceResponse_Output1Item(KisBaseModel):
    """nested item."""

    ovtm_untp_last_hour: str | None = None  # 시간외 단일가 최종 시간
    ovtm_untp_askp1: str | None = None  # 시간외 단일가 매도호가1
    ovtm_untp_askp2: str | None = None  # 시간외 단일가 매도호가2
    ovtm_untp_askp3: str | None = None  # 시간외 단일가 매도호가3
    ovtm_untp_askp4: str | None = None  # 시간외 단일가 매도호가4
    ovtm_untp_askp5: str | None = None  # 시간외 단일가 매도호가5
    ovtm_untp_askp6: str | None = None  # 시간외 단일가 매도호가6
    ovtm_untp_askp7: str | None = None  # 시간외 단일가 매도호가7
    ovtm_untp_askp8: str | None = None  # 시간외 단일가 매도호가8
    ovtm_untp_askp9: str | None = None  # 시간외 단일가 매도호가9
    ovtm_untp_askp10: str | None = None  # 시간외 단일가 매도호가10
    ovtm_untp_bidp1: str | None = None  # 시간외 단일가 매수호가1
    ovtm_untp_bidp2: str | None = None  # 시간외 단일가 매수호가2
    ovtm_untp_bidp3: str | None = None  # 시간외 단일가 매수호가3
    ovtm_untp_bidp4: str | None = None  # 시간외 단일가 매수호가4
    ovtm_untp_bidp5: str | None = None  # 시간외 단일가 매수호가5
    ovtm_untp_bidp6: str | None = None  # 시간외 단일가 매수호가6
    ovtm_untp_bidp7: str | None = None  # 시간외 단일가 매수호가7
    ovtm_untp_bidp8: str | None = None  # 시간외 단일가 매수호가8
    ovtm_untp_bidp9: str | None = None  # 시간외 단일가 매수호가9
    ovtm_untp_bidp10: str | None = None  # 시간외 단일가 매수호가10
    ovtm_untp_askp_icdc1: str | None = None  # 시간외 단일가 매도호가 증감1
    ovtm_untp_askp_icdc2: str | None = None  # 시간외 단일가 매도호가 증감2
    ovtm_untp_askp_icdc3: str | None = None  # 시간외 단일가 매도호가 증감3
    ovtm_untp_askp_icdc4: str | None = None  # 시간외 단일가 매도호가 증감4
    ovtm_untp_askp_icdc5: str | None = None  # 시간외 단일가 매도호가 증감5
    ovtm_untp_askp_icdc6: str | None = None  # 시간외 단일가 매도호가 증감6
    ovtm_untp_askp_icdc7: str | None = None  # 시간외 단일가 매도호가 증감7
    ovtm_untp_askp_icdc8: str | None = None  # 시간외 단일가 매도호가 증감8
    ovtm_untp_askp_icdc9: str | None = None  # 시간외 단일가 매도호가 증감9
    ovtm_untp_askp_icdc10: str | None = None  # 시간외 단일가 매도호가 증감10
    ovtm_untp_bidp_icdc1: str | None = None  # 시간외 단일가 매수호가 증감1
    ovtm_untp_bidp_icdc2: str | None = None  # 시간외 단일가 매수호가 증감2
    ovtm_untp_bidp_icdc3: str | None = None  # 시간외 단일가 매수호가 증감3
    ovtm_untp_bidp_icdc4: str | None = None  # 시간외 단일가 매수호가 증감4
    ovtm_untp_bidp_icdc5: str | None = None  # 시간외 단일가 매수호가 증감5
    ovtm_untp_bidp_icdc6: str | None = None  # 시간외 단일가 매수호가 증감6
    ovtm_untp_bidp_icdc7: str | None = None  # 시간외 단일가 매수호가 증감7
    ovtm_untp_bidp_icdc8: str | None = None  # 시간외 단일가 매수호가 증감8
    ovtm_untp_bidp_icdc9: str | None = None  # 시간외 단일가 매수호가 증감9
    ovtm_untp_bidp_icdc10: str | None = None  # 시간외 단일가 매수호가 증감10
    ovtm_untp_askp_rsqn1: str | None = None  # 시간외 단일가 매도호가 잔량1
    ovtm_untp_askp_rsqn2: str | None = None  # 시간외 단일가 매도호가 잔량2
    ovtm_untp_askp_rsqn3: str | None = None  # 시간외 단일가 매도호가 잔량3
    ovtm_untp_askp_rsqn4: str | None = None  # 시간외 단일가 매도호가 잔량4
    ovtm_untp_askp_rsqn5: str | None = None  # 시간외 단일가 매도호가 잔량5
    ovtm_untp_askp_rsqn6: str | None = None  # 시간외 단일가 매도호가 잔량6
    ovtm_untp_askp_rsqn7: str | None = None  # 시간외 단일가 매도호가 잔량7
    ovtm_untp_askp_rsqn8: str | None = None  # 시간외 단일가 매도호가 잔량8
    ovtm_untp_askp_rsqn9: str | None = None  # 시간외 단일가 매도호가 잔량9
    ovtm_untp_askp_rsqn10: str | None = None  # 시간외 단일가 매도호가 잔량10
    ovtm_untp_bidp_rsqn1: str | None = None  # 시간외 단일가 매수호가 잔량1
    ovtm_untp_bidp_rsqn2: str | None = None  # 시간외 단일가 매수호가 잔량2
    ovtm_untp_bidp_rsqn3: str | None = None  # 시간외 단일가 매수호가 잔량3
    ovtm_untp_bidp_rsqn4: str | None = None  # 시간외 단일가 매수호가 잔량4
    ovtm_untp_bidp_rsqn5: str | None = None  # 시간외 단일가 매수호가 잔량5
    ovtm_untp_bidp_rsqn6: str | None = None  # 시간외 단일가 매수호가 잔량6
    ovtm_untp_bidp_rsqn7: str | None = None  # 시간외 단일가 매수호가 잔량7
    ovtm_untp_bidp_rsqn8: str | None = None  # 시간외 단일가 매수호가 잔량8
    ovtm_untp_bidp_rsqn9: str | None = None  # 시간외 단일가 매수호가 잔량9
    ovtm_untp_bidp_rsqn10: str | None = None  # 시간외 단일가 매수호가 잔량10
    ovtm_untp_total_askp_rsqn: str | None = None  # 시간외 단일가 총 매도호가 잔량
    ovtm_untp_total_bidp_rsqn: str | None = None  # 시간외 단일가 총 매수호가 잔량
    ovtm_untp_total_askp_rsqn_icdc: str | None = None  # 시간외 단일가 총 매도호가 잔량
    ovtm_untp_total_bidp_rsqn_icdc: str | None = None  # 시간외 단일가 총 매수호가 잔량
    ovtm_untp_ntby_bidp_rsqn: str | None = None  # 시간외 단일가 순매수 호가 잔량
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    total_askp_rsqn_icdc: str | None = None  # 총 매도호가 잔량 증감
    total_bidp_rsqn_icdc: str | None = None  # 총 매수호가 잔량 증감
    ovtm_total_askp_rsqn: str | None = None  # 시간외 총 매도호가 잔량
    ovtm_total_bidp_rsqn: str | None = None  # 시간외 총 매수호가 잔량
    ovtm_total_askp_icdc: str | None = None  # 시간외 총 매도호가 증감
    ovtm_total_bidp_icdc: str | None = None  # 시간외 총 매수호가 증감

class InquireOvertimeAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireOvertimeAskingPriceResponse_Output1Item | None = None  # 응답상세

class InquireOvertimeAskingPriceExecutor(ApiExecutor[InquireOvertimeAskingPriceRequest, InquireOvertimeAskingPriceResponse]):
    """국내주식 시간외호가[국내주식-077]."""

    # 국내주식 시간외호가 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0230] 시간외 현재가 화면의 '호가' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireOvertimeAskingPriceResponse
    TR_ID = "FHPST02300400"
