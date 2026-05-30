"""Auto-generated from apiportal spec — do not edit by hand."""

from __future__ import annotations

from tooja.brokers.kis.raw.base import KisBaseModel
from tooja.brokers.kis.raw.ws_base import WsSubscriber


class H0gscni0Message(KisBaseModel):
    """WS 메시지 1건."""

    CUST_ID: str  # 고객 ID — '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨'
    ACNT_NO: str  # 계좌번호
    ODER_NO: str  # 주문번호
    OODER_NO: str  # 원주문번호
    SELN_BYOV_CLS: str  # 매도매수구분 — 01:매도 02:매수 03:전매도 04:환매수
    RCTF_CLS: str  # 정정구분 — 0:정상 1:정정 2:취소
    ODER_KIND2: str  # 주문종류2 — 1:시장가 2:지정자 6:단주시장가 7:단주지정가 A:MOO B:LOO C:MOC D:LOC
    STCK_SHRN_ISCD: str  # 주식 단축 종목코드
    CNTG_QTY: str  # 체결수량 — - 주문통보의 경우 해당 위치에 주문수량이 출력 - 체결통보인 경우 해당 위치에 체결수량이 출력
    CNTG_UNPR: str  # 체결단가 — ※ 주문통보 시에는 주문단가가, 체결통보 시에는 체결단가가 수신 됩니다. ※ 체결단가의 경우, 국가에 따라 소수점 생략 위치가 상이합니다. 미국 4 일본 1 중국 3 홍콩 3 베트남 0 EX) 미국 AAPL(현재가 : 148.0100)의 
    STCK_CNTG_HOUR: str  # 주식 체결 시간 — 특정 거래소의 체결시간 데이터는 수신되지 않습니다. 체결시간 데이터가 필요할 경우, 체결통보 데이터 수신 시 타임스탬프를 찍는 것으로 대체하시길 바랍니다.
    RFUS_YN: str  # 거부여부 — 0:정상 1:거부
    CNTG_YN: str  # 체결여부 — 1:주문,정정,취소,거부 2:체결
    ACPT_YN: str  # 접수여부 — 1:주문접수 2:확인 3:취소(FOK/IOC)
    BRNC_NO: str  # 지점번호
    ODER_QTY: str  # 주문 수량 — - 주문통보인 경우 해당 위치 미출력 (주문통보의 주문수량은 CNTG_QTY 위치에 출력) - 체결통보인 경우 해당 위치에 주문수량이 출력
    ACNT_NAME: str  # 계좌명
    CNTG_ISNM: str  # 체결종목명
    ODER_COND: str  # 해외종목구분 — 4:홍콩(HKD) 5:상해B(USD) 6:NASDAQ 7:NYSE 8:AMEX 9:OTCB C:홍콩(CNY) A:상해A(CNY) B:심천B(HKD) D:도쿄 E:하노이 F:호치민
    DEBT_GB: str  # 담보유형코드 — 10:현금 15:해외주식담보대출
    DEBT_DATE: str  # 담보대출일자 — 대출일(YYYYMMDD)
    START_TM: str  # 분할매수/매도 시작시간 — HHMMSS
    END_TM: str  # 분할매수/매도 종료시간 — HHMMSS
    TM_DIV_TP: str  # 시간분할타입유형 — 00 시간직접설정, 02 : 정규장까지
    CNTG_UNPR12: str  # 체결단가12

class H0gscni0Subscriber(WsSubscriber[H0gscni0Message]):
    """해외주식 실시간체결통보[실시간-009]."""

    TR_ID = "H0GSCNI0"
    RESPONSE_TYPE = H0gscni0Message
    COLUMNS = ("CUST_ID", "ACNT_NO", "ODER_NO", "OODER_NO", "SELN_BYOV_CLS", "RCTF_CLS", "ODER_KIND2", "STCK_SHRN_ISCD", "CNTG_QTY", "CNTG_UNPR", "STCK_CNTG_HOUR", "RFUS_YN", "CNTG_YN", "ACPT_YN", "BRNC_NO", "ODER_QTY", "ACNT_NAME", "CNTG_ISNM", "ODER_COND", "DEBT_GB", "DEBT_DATE", "START_TM", "END_TM", "TM_DIV_TP", "CNTG_UNPR12",)
