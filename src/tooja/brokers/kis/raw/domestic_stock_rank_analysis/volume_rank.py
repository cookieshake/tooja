"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class VolumeRankRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # 조건 시장 분류 코드 — J:KRX, NX:NXT
    FID_COND_SCR_DIV_CODE: str  # 조건 화면 분류 코드 — 20171
    FID_INPUT_ISCD: str  # 입력 종목코드 — 0000(전체) 기타(업종코드)
    FID_DIV_CLS_CODE: str  # 분류 구분 코드 — 0(전체) 1(보통주) 2(우선주)
    FID_BLNG_CLS_CODE: str  # 소속 구분 코드 — 0 : 평균거래량 1:거래증가율 2:평균거래회전율 3:거래금액순 4:평균거래금액회전율
    FID_TRGT_CLS_CODE: str  # 대상 구분 코드 — 1 or 0 9자리 (차례대로 증거금 30% 40% 50% 60% 100% 신용보증금 30% 40% 50% 60%) ex) "111111111"
    FID_TRGT_EXLS_CLS_CODE: str  # 대상 제외 구분 코드 — 1 or 0 10자리 (차례대로 투자위험/경고/주의 관리종목 정리매매 불성실공시 우선주 거래정지 ETF ETN 신용주문불가 SPAC) ex) "0000000000"
    FID_INPUT_PRICE_1: str  # 입력 가격1 — 가격 ~ ex) "0" 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력
    FID_INPUT_PRICE_2: str  # 입력 가격2 — ~ 가격 ex) "1000000" 전체 가격 대상 조회 시 FID_INPUT_PRICE_1, FID_INPUT_PRICE_2 모두 ""(공란) 입력
    FID_VOL_CNT: str  # 거래량 수 — 거래량 ~ ex) "100000" 전체 거래량 대상 조회 시 FID_VOL_CNT ""(공란) 입력

class VolumeRankResponse_OutputItem(KisBaseModel):
    """nested item."""

    hts_kor_isnm: str | None = None  # HTS 한글 종목명
    mksc_shrn_iscd: str | None = None  # 유가증권 단축 종목코드
    data_rank: str | None = None  # 데이터 순위
    stck_prpr: str | None = None  # 주식 현재가
    prdy_vrss_sign: str | None = None  # 전일 대비 부호
    prdy_vrss: str | None = None  # 전일 대비
    prdy_ctrt: str | None = None  # 전일 대비율
    acml_vol: str | None = None  # 누적 거래량
    prdy_vol: str | None = None  # 전일 거래량
    lstn_stcn: str | None = None  # 상장 주수
    avrg_vol: str | None = None  # 평균 거래량
    n_befr_clpr_vrss_prpr_rate: str | None = None  # N일전종가대비현재가대비율
    vol_inrt: str | None = None  # 거래량증가율
    vol_tnrt: str | None = None  # 거래량 회전율
    nday_vol_tnrt: str | None = None  # N일 거래량 회전율
    avrg_tr_pbmn: str | None = None  # 평균 거래 대금
    tr_pbmn_tnrt: str | None = None  # 거래대금회전율
    nday_tr_pbmn_tnrt: str | None = None  # N일 거래대금 회전율
    acml_tr_pbmn: str | None = None  # 누적 거래 대금

class VolumeRankResponse(KisCommonResponse):
    """응답 본문."""

    Output: list[VolumeRankResponse_OutputItem] = []  # 응답상세 — Array

class VolumeRankExecutor(ApiExecutor[VolumeRankRequest, VolumeRankResponse]):
    """거래량순위[v1_국내주식-047]."""

    # 국내주식 거래량순위 API입니다. 한국투자 HTS(eFriend Plus) &gt; [0171] 거래량 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최대 30건 확인 가능하며, 다음 조회가 불가합니다. + 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다. 종목조건검색 API는 H

    PATH = "/uapi/domestic-stock/v1/quotations/volume-rank"
    METHOD = "GET"
    RESPONSE_TYPE = VolumeRankResponse
    TR_ID = "FHPST01710000"
