from tooja.brokers.kis.mapping import classify_kis_error
from tooja.core.errors import (
    AuthError,
    BrokerAPIError,
    InsufficientFunds,
    MarketClosed,
    NetworkError,
    OrderNotFound,
    OrderRejected,
    PermissionDenied,
    RateLimitError,
    SymbolNotFound,
)


def test_success_returns_none():
    assert classify_kis_error("0", "MCA00000", "정상처리") is None


def test_known_code_auth():
    assert classify_kis_error("1", "EGW00121", "토큰만료") is AuthError


def test_known_code_permission_denied():
    assert classify_kis_error("1", "APAC0134", "계좌 미등록") is PermissionDenied
    assert classify_kis_error("1", "SKFT2101", "선물옵션 미신청") is PermissionDenied
    assert classify_kis_error("1", "EGW00550", "CME SUB 미신청") is PermissionDenied


def test_known_code_rate_limit():
    assert classify_kis_error("1", "EGW00201", "초당 거래건수 초과") is RateLimitError


def test_known_code_network_transient():
    assert classify_kis_error("1", "EGW00203", "OPS 라우팅 오류") is NetworkError


def test_known_code_order_rejected():
    assert classify_kis_error("1", "APBK1227", "조회구분 입력 오류") is OrderRejected


def test_known_code_symbol_not_found():
    assert classify_kis_error("1", "APBK1631", "데이터 없음") is SymbolNotFound


def test_pattern_insufficient_funds():
    assert classify_kis_error("1", "XXXXXXXX", "예수금 부족합니다") is InsufficientFunds
    assert classify_kis_error("1", "XXXXXXXX", "잔고 부족") is InsufficientFunds


def test_pattern_market_closed():
    assert classify_kis_error("1", "XXXXXXXX", "장 마감되었습니다") is MarketClosed
    assert classify_kis_error("1", "XXXXXXXX", "개장 전입니다") is MarketClosed


def test_pattern_order_not_found():
    assert classify_kis_error("1", "XXXXXXXX", "주문번호가 없습니다") is OrderNotFound


def test_unknown_falls_to_broker_api_error():
    assert classify_kis_error("1", "ZZZZZZZZ", "no idea") is BrokerAPIError


def test_rt_cd_zero_overrides_unknown_msg():
    # rt_cd=0이면 어떤 msg든 성공
    assert classify_kis_error("0", "ZZZZ", "이상하지만 성공") is None
