"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class PriceDetailRequest(KisBaseModel):
    """요청."""

    AUTH: str  # 사용자권한정보
    EXCD: str  # 거래소명 — HKS : 홍콩 NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 TSE : 도쿄 SHS : 상해 SZS : 심천 SHI : 상해지수 SZI : 심천지수 HSX : 호치민 HNX : 하노이 BAY : 뉴욕(주간) BAQ : 나스닥(주간)
    SYMB: str  # 종목코드

class PriceDetailResponse_OutputItem(KisBaseModel):
    """nested item."""

    rsym: str | None = None  # 실시간조회종목코드
    pvol: str | None = None  # 전일거래량
    open: str | None = None  # 시가
    high: str | None = None  # 고가
    low: str | None = None  # 저가
    last: str | None = None  # 현재가
    base: str | None = None  # 전일종가
    tomv: str | None = None  # 시가총액
    pamt: str | None = None  # 전일거래대금
    uplp: str | None = None  # 상한가
    dnlp: str | None = None  # 하한가
    h52p: str | None = None  # 52주최고가
    h52d: str | None = None  # 52주최고일자
    l52p: str | None = None  # 52주최저가
    l52d: str | None = None  # 52주최저일자
    perx: str | None = None  # PER
    pbrx: str | None = None  # PBR
    epsx: str | None = None  # EPS
    bpsx: str | None = None  # BPS
    shar: str | None = None  # 상장주수
    mcap: str | None = None  # 자본금
    curr: str | None = None  # 통화
    zdiv: str | None = None  # 소수점자리수
    vnit: str | None = None  # 매매단위
    t_xprc: str | None = None  # 원환산당일가격
    t_xdif: str | None = None  # 원환산당일대비
    t_xrat: str | None = None  # 원환산당일등락
    p_xprc: str | None = None  # 원환산전일가격
    p_xdif: str | None = None  # 원환산전일대비
    p_xrat: str | None = None  # 원환산전일등락
    t_rate: str | None = None  # 당일환율
    p_rate: str | None = None  # 전일환율
    t_xsgn: str | None = None  # 원환산당일기호 — HTS 색상표시용
    p_xsng: str | None = None  # 원환산전일기호 — HTS 색상표시용
    e_ordyn: str | None = None  # 거래가능여부
    e_hogau: str | None = None  # 호가단위
    e_icod: str | None = None  # 업종(섹터)
    e_parp: str | None = None  # 액면가
    tvol: str | None = None  # 거래량
    tamt: str | None = None  # 거래대금
    etyp_nm: str | None = None  # ETP 분류명

class PriceDetailResponse(KisCommonResponse):
    """응답 본문."""

    output: PriceDetailResponse_OutputItem | None = None  # 응답상세

class PriceDetailExecutor(ApiExecutor[PriceDetailRequest, PriceDetailResponse]):
    """해외주식 현재가상세[v1_해외주식-029]."""

    # 해외주식 현재가상세 API입니다. 해당 API를 활용하여 해외주식 종목의 매매단위(vnit), 호가단위(e_hogau), PER, PBR, EPS, BPS 등의 데이터를 확인하실 수 있습니다. 해외주식 시세는 무료시세(지연시세)만이 제공되며, API로는 유료시세(실시간시세)를 받아보실 수 없습니다. ※ 지연시세 지연시간 : 미국 - 실시간무료(0분 지연, 나스닥 마켓센터에서 거래되는 호가 및 호가 잔량 정보) 홍콩, 베트남, 

    PATH = "/uapi/overseas-price/v1/quotations/price-detail"
    METHOD = "GET"
    RESPONSE_TYPE = PriceDetailResponse
    TR_ID = "HHDFS76200200"
