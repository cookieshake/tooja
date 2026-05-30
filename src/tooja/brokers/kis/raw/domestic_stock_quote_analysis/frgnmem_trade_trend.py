"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import (
    ApiExecutor, KisBaseModel, KisCommonResponse,
)


class FrgnmemTradeTrendRequest(KisBaseModel):
    """요청."""

    FID_COND_MRKT_DIV_CODE: str  # FID 조건 시장 분류 코드 — J 고정 입력
    FID_COND_SCR_DIV_CODE: str  # 화면분류코드 — 20432(primary key)
    FID_INPUT_ISCD: str  # 종목코드 — ex. 005930(삼성전자) ※ FID_INPUT_ISCD(종목코드) 혹은 FID_MRKT_CLS_CODE(시장구분코드) 둘 중 하나만 입력
    FID_INPUT_ISCD_2: str  # 회원사코드 — ex. 99999(전체) ※ 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조)
    FID_MRKT_CLS_CODE: str  # 시장구분코드 — A(전체),K(코스피), Q(코스닥), K2(코스피200), W(ELW) ※ FID_INPUT_ISCD(종목코드) 혹은 FID_MRKT_CLS_CODE(시장구분코드) 둘 중 하나만 입력
    FID_VOL_CNT: str  # 거래량 — 거래량 ~

class FrgnmemTradeTrendResponse_Output1Item(KisBaseModel):
    """nested item."""

    total_seln_qty: str | None = None  # 총매도수량
    total_shnu_qty: str | None = None  # 총매수2수량

class FrgnmemTradeTrendResponse_Output2Item(KisBaseModel):
    """nested item."""

    bsop_hour: str | None = None  # 영업시간
    mbcr_name: str | None = None  # 회원사명
    hts_kor_isnm: str | None = None  # HTS한글종목명
    stck_prpr: str | None = None  # 주식현재가
    prdy_vrss: str | None = None  # 전일대비
    prdy_vrss_sign: str | None = None  # 전일대비부호
    cntg_vol: str | None = None  # 체결거래량
    acml_ntby_qty: str | None = None  # 누적순매수수량
    glob_ntby_qty: str | None = None  # 외국계순매수수량
    frgn_ntby_qty_icdc: str | None = None  # 외국인순매수수량증감

class FrgnmemTradeTrendResponse(KisCommonResponse):
    """응답 본문."""

    output1: FrgnmemTradeTrendResponse_Output1Item | None = None  # 응답상세 — array
    output2: list[FrgnmemTradeTrendResponse_Output2Item] = []  # 응답상세 — array

class FrgnmemTradeTrendExecutor(ApiExecutor[FrgnmemTradeTrendRequest, FrgnmemTradeTrendResponse]):
    """회원사 실시간 매매동향(틱) [국내주식-163]."""

    # 회원사 실시간 매매동향(틱) API입니다. 한국투자 HTS(eFriend Plus) &gt; [0432] 회원사 실시간 매매동향 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 최근 100건까지 데이터 조회 가능합니다.

    PATH = "/uapi/domestic-stock/v1/quotations/frgnmem-trade-trend"
    METHOD = "GET"
    RESPONSE_TYPE = FrgnmemTradeTrendResponse
    TR_ID = "FHPST04320000"
