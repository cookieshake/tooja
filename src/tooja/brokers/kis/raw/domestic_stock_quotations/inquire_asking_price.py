"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAskingPriceRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목번호 (6자리)

class InquireAskingPriceResponse_OutputItem(KisBaseModel):
    """nested item."""

    aspr_acpt_hour: str | None = None  # 호가 접수 시간
    askp1: str | None = None  # 매도호가1
    askp2: str | None = None  # 매도호가2
    askp3: str | None = None  # 매도호가3
    askp4: str | None = None  # 매도호가4
    askp5: str | None = None  # 매도호가5
    askp6: str | None = None  # 매도호가6
    askp7: str | None = None  # 매도호가7
    askp8: str | None = None  # 매도호가8
    askp9: str | None = None  # 매도호가9
    askp10: str | None = None  # 매도호가10
    bidp1: str | None = None  # 매수호가1
    bidp2: str | None = None  # 매수호가2
    bidp3: str | None = None  # 매수호가3
    bidp4: str | None = None  # 매수호가4
    bidp5: str | None = None  # 매수호가5
    bidp6: str | None = None  # 매수호가6
    bidp7: str | None = None  # 매수호가7
    bidp8: str | None = None  # 매수호가8
    bidp9: str | None = None  # 매수호가9
    bidp10: str | None = None  # 매수호가10
    askp_rsqn1: str | None = None  # 매도호가 잔량1
    askp_rsqn2: str | None = None  # 매도호가 잔량2
    askp_rsqn3: str | None = None  # 매도호가 잔량3
    askp_rsqn4: str | None = None  # 매도호가 잔량4
    askp_rsqn5: str | None = None  # 매도호가 잔량5
    askp_rsqn6: str | None = None  # 매도호가 잔량6
    askp_rsqn7: str | None = None  # 매도호가 잔량7
    askp_rsqn8: str | None = None  # 매도호가 잔량8
    askp_rsqn9: str | None = None  # 매도호가 잔량9
    askp_rsqn10: str | None = None  # 매도호가 잔량10
    bidp_rsqn1: str | None = None  # 매수호가 잔량1
    bidp_rsqn2: str | None = None  # 매수호가 잔량2
    bidp_rsqn3: str | None = None  # 매수호가 잔량3
    bidp_rsqn4: str | None = None  # 매수호가 잔량4
    bidp_rsqn5: str | None = None  # 매수호가 잔량5
    bidp_rsqn6: str | None = None  # 매수호가 잔량6
    bidp_rsqn7: str | None = None  # 매수호가 잔량7
    bidp_rsqn8: str | None = None  # 매수호가 잔량8
    bidp_rsqn9: str | None = None  # 매수호가 잔량9
    bidp_rsqn10: str | None = None  # 매수호가 잔량10
    askp_rsqn_icdc1: str | None = None  # 매도호가 잔량 증감1
    askp_rsqn_icdc2: str | None = None  # 매도호가 잔량 증감2
    askp_rsqn_icdc3: str | None = None  # 매도호가 잔량 증감3
    askp_rsqn_icdc4: str | None = None  # 매도호가 잔량 증감4
    askp_rsqn_icdc5: str | None = None  # 매도호가 잔량 증감5
    askp_rsqn_icdc6: str | None = None  # 매도호가 잔량 증감6
    askp_rsqn_icdc7: str | None = None  # 매도호가 잔량 증감7
    askp_rsqn_icdc8: str | None = None  # 매도호가 잔량 증감8
    askp_rsqn_icdc9: str | None = None  # 매도호가 잔량 증감9
    askp_rsqn_icdc10: str | None = None  # 매도호가 잔량 증감10
    bidp_rsqn_icdc1: str | None = None  # 매수호가 잔량 증감1
    bidp_rsqn_icdc2: str | None = None  # 매수호가 잔량 증감2
    bidp_rsqn_icdc3: str | None = None  # 매수호가 잔량 증감3
    bidp_rsqn_icdc4: str | None = None  # 매수호가 잔량 증감4
    bidp_rsqn_icdc5: str | None = None  # 매수호가 잔량 증감5
    bidp_rsqn_icdc6: str | None = None  # 매수호가 잔량 증감6
    bidp_rsqn_icdc7: str | None = None  # 매수호가 잔량 증감7
    bidp_rsqn_icdc8: str | None = None  # 매수호가 잔량 증감8
    bidp_rsqn_icdc9: str | None = None  # 매수호가 잔량 증감9
    bidp_rsqn_icdc10: str | None = None  # 매수호가 잔량 증감10
    total_askp_rsqn: str | None = None  # 총 매도호가 잔량
    total_bidp_rsqn: str | None = None  # 총 매수호가 잔량
    total_askp_rsqn_icdc: str | None = None  # 총 매도호가 잔량 증감
    total_bidp_rsqn_icdc: str | None = None  # 총 매수호가 잔량 증감
    ovtm_total_askp_icdc: str | None = None  # 시간외 총 매도호가 증감
    ovtm_total_bidp_icdc: str | None = None  # 시간외 총 매수호가 증감
    ovtm_total_askp_rsqn: str | None = None  # 시간외 총 매도호가 잔량
    ovtm_total_bidp_rsqn: str | None = None  # 시간외 총 매수호가 잔량
    ntby_aspr_rsqn: str | None = None  # 순매수 호가 잔량
    new_mkop_cls_code: str | None = None  # 신 장운영 구분 코드
    lp_askp_rsqn1: str | None = None  # LP 매도호가 잔량1
    lp_askp_rsqn2: str | None = None  # LP 매도호가 잔량2
    lp_askp_rsqn3: str | None = None  # LP 매도호가 잔량3
    lp_askp_rsqn4: str | None = None  # LP 매도호가 잔량4
    lp_askp_rsqn5: str | None = None  # LP 매도호가 잔량5
    lp_askp_rsqn6: str | None = None  # LP 매도호가 잔량6
    lp_askp_rsqn7: str | None = None  # LP 매도호가 잔량7
    lp_askp_rsqn8: str | None = None  # LP 매도호가 잔량8
    lp_askp_rsqn9: str | None = None  # LP 매도호가 잔량9
    lp_askp_rsqn10: str | None = None  # LP 매도호가 잔량10
    lp_bidp_rsqn1: str | None = None  # LP 매수호가 잔량1
    lp_bidp_rsqn2: str | None = None  # LP 매수호가 잔량2
    lp_bidp_rsqn3: str | None = None  # LP 매수호가 잔량3
    lp_bidp_rsqn4: str | None = None  # LP 매수호가 잔량4
    lp_bidp_rsqn5: str | None = None  # LP 매수호가 잔량5
    lp_bidp_rsqn6: str | None = None  # LP 매수호가 잔량6
    lp_bidp_rsqn7: str | None = None  # LP 매수호가 잔량7
    lp_bidp_rsqn8: str | None = None  # LP 매수호가 잔량8
    lp_bidp_rsqn9: str | None = None  # LP 매수호가 잔량9
    lp_bidp_rsqn10: str | None = None  # LP 매수호가 잔량10
    lp_total_askp_rsqn: str | None = None  # LP 총 매도호가 잔량
    lp_total_bidp_rsqn: str | None = None  # LP 총 매수호가 잔량
    mid_prc: str | None = None  # KRX 중간가
    midp_total_rsqn: str | None = None  # KRX 중간가잔량합계수량
    midp_cls_code: str | None = None  # KRX 중간가구분코드
    mid_prc2: str | None = None  # NXT 중간가 — 미사용 필드
    midp_total_rsqn2: str | None = None  # NXT 중간가잔량합계수량 — 미사용 필드
    midp_cls_code2: str | None = None  # NXT 중간가구분코드 — 미사용 필드

class InquireAskingPriceResponse(KisCommonResponse):
    """응답 본문."""

    output: InquireAskingPriceResponse_OutputItem | None = None  # 응답상세

class InquireAskingPriceExecutor(ApiExecutor[InquireAskingPriceRequest, InquireAskingPriceResponse]):
    """ETF 현재가 호가."""

    # 국내주식 ETF 현재가 호가 API입니다. 해당 API는 고객 개인 유량과 무관하게 초당 120 건 호출 제한을 두고 있어, 이용 시 호출 제한이 있사오니 참고 부탁드립니다.

    PATH = "/uapi/etfetn/v1/quotations/inquire-asking-price"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAskingPriceResponse
    TR_ID = "FHPST02400200"
