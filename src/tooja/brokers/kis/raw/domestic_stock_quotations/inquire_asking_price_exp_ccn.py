"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class InquireAskingPriceExpCcnRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT, UN:통합
    FID_INPUT_ISCD: str  # 입력 종목코드 — 종목코드 (ex 005930 삼성전자)

class InquireAskingPriceExpCcnResponse_Output1Item(KisBaseModel):
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
    new_mkop_cls_code: str | None = None  # 신 장운영 구분 코드 — ' '00' : 장전 예상체결가와 장마감 동시호가 '49' : 장후 예상체결가 (1) 첫 번째 비트 1 : 장개시전 2 : 장중 3 : 장종료후 4 : 시간외단일가 7 : 일반Buy-in 8 : 당일Buy-in (2) 두 번째

class InquireAskingPriceExpCcnResponse_Output2Item(KisBaseModel):
    """nested item."""

    antc_mkop_cls_code: str | None = None  # 예상 장운영 구분 코드
    stck_prpr: str | None = None  # 주식 현재가
    stck_oprc: str | None = None  # 주식 시가2
    stck_hgpr: str | None = None  # 주식 최고가
    stck_lwpr: str | None = None  # 주식 최저가
    stck_sdpr: str | None = None  # 주식 기준가
    antc_cnpr: str | None = None  # 예상 체결가
    antc_cntg_vrss_sign: str | None = None  # 예상 체결 대비 부호
    antc_cntg_vrss: str | None = None  # 예상 체결 대비
    antc_cntg_prdy_ctrt: str | None = None  # 예상 체결 전일 대비율
    antc_vol: str | None = None  # 예상 거래량
    stck_shrn_iscd: str | None = None  # 주식 단축 종목코드
    vi_cls_code: str | None = None  # VI적용구분코드

class InquireAskingPriceExpCcnResponse(KisCommonResponse):
    """응답 본문."""

    output1: InquireAskingPriceExpCcnResponse_Output1Item | None = None  # 응답상세
    output2: InquireAskingPriceExpCcnResponse_Output2Item | None = None  # 응답상세

class InquireAskingPriceExpCcnExecutor(ApiExecutor[InquireAskingPriceExpCcnRequest, InquireAskingPriceExpCcnResponse]):
    """주식현재가 호가/예상체결[v1_국내주식-011]."""

    # 주식현재가 호가 예상체결 API입니다. 매수 매도 호가를 확인하실 수 있습니다. 실시간 데이터를 원하신다면 웹소켓 API를 활용하세요.

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
    METHOD = "GET"
    RESPONSE_TYPE = InquireAskingPriceExpCcnResponse
    TR_ID = "FHKST01010200"
