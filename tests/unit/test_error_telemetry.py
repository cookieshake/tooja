"""Unmapped broker error codes should be logged so the mapping tables can be
grown from real traffic, while mapped codes stay quiet."""

import logging

from tooja.brokers.kis._call import _translate as kis_translate
from tooja.brokers.kis.raw.base import KisApiError
from tooja.brokers.toss._call import _translate as toss_translate
from tooja.brokers.toss.raw.base import TossApiError
from tooja.core.errors import AuthError, BrokerAPIError

KIS_LOGGER = "tooja.brokers.kis._call"
TOSS_LOGGER = "tooja.brokers.toss._call"


def _warnings(caplog):
    return [r for r in caplog.records if r.levelno >= logging.WARNING]


def test_kis_unmapped_code_logs_warning(caplog):
    err = KisApiError("알 수 없는 오류", code="ZZZ99999", rt_cd="1")
    with caplog.at_level(logging.WARNING, logger=KIS_LOGGER):
        result = kis_translate(err, "/uapi/domestic-stock/v1/x")
    assert isinstance(result, BrokerAPIError)
    assert "ZZZ99999" in caplog.text
    assert "/uapi/domestic-stock/v1/x" in caplog.text


def test_kis_mapped_code_stays_quiet(caplog):
    err = KisApiError("토큰만료", code="EGW00121", rt_cd="1")
    with caplog.at_level(logging.WARNING, logger=KIS_LOGGER):
        result = kis_translate(err, "/uapi/x")
    assert isinstance(result, AuthError)
    assert _warnings(caplog) == []


def test_kis_pattern_matched_code_stays_quiet(caplog):
    # Classified via the Korean message pattern, not the code table — still mapped.
    err = KisApiError("주문가능 잔고 부족", code="UNKNOWN01", rt_cd="1")
    with caplog.at_level(logging.WARNING, logger=KIS_LOGGER):
        result = kis_translate(err, "/uapi/x")
    assert not isinstance(result, BrokerAPIError)
    assert _warnings(caplog) == []


def test_toss_unmapped_code_logs_warning(caplog):
    err = TossApiError("weird-failure", "boom", http_status=400)
    with caplog.at_level(logging.WARNING, logger=TOSS_LOGGER):
        result = toss_translate(err, "/api/v1/x")
    assert isinstance(result, BrokerAPIError)
    assert "weird-failure" in caplog.text
    assert "/api/v1/x" in caplog.text


def test_toss_status_fallback_is_not_unmapped(caplog):
    # 401 with an unknown code maps to AuthError via the status fallback —
    # that is a mapping, so it should not warn.
    err = TossApiError("unauthorized-ish", "no", http_status=401)
    with caplog.at_level(logging.WARNING, logger=TOSS_LOGGER):
        result = toss_translate(err, "/api/x")
    assert isinstance(result, AuthError)
    assert _warnings(caplog) == []
