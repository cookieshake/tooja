"""Regression tests for KisWsStream / KisOrderUpdateStream frame parsing."""

from __future__ import annotations

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from tooja.brokers.kis._mappers import (
    _WS_ORDER_COLUMNS, _WS_QUOTE_COLUMNS,
    order_update_from_ws_record, quote_from_ws_record,
)
from tooja.brokers.kis._ws_stream import KisOrderUpdateStream, KisWsStream, _SubscriptionTopic
from tooja.core.enums import OrderStatus


def _fake_broker():
    b = MagicMock()
    b.is_virtual = True
    creds = MagicMock()
    creds.hts_id = "HTS_TEST"
    b.credentials = creds
    return b


# ─── _WS_ORDER_COLUMNS column-set covers ODER_QTY (partial-fill bug regression) ──


def test_order_columns_include_oder_qty():
    """If ODER_QTY is missing, partial fills get marked as FILLED — regression
    for https://github.com/cookieshake/tooja/pull/2 review comment."""
    assert "ODER_QTY" in _WS_ORDER_COLUMNS
    assert "BRNC_NO" in _WS_ORDER_COLUMNS


def test_order_columns_match_raw_subscriber():
    """Adapter columns must match the raw H0STCNI0 subscriber's COLUMNS,
    since the WS frame parser zips by index."""
    from tooja.brokers.kis.raw.domestic_stock_ws.h0stcni0 import H0stcni0Subscriber
    assert _WS_ORDER_COLUMNS == H0stcni0Subscriber.COLUMNS


def test_partial_fill_via_full_frame_path():
    """Build a fake H0STCNI0 frame and parse it end-to-end through
    KisOrderUpdateStream._parse. Verify PARTIALLY_FILLED comes out."""
    broker = _fake_broker()
    stream = KisOrderUpdateStream(
        broker, tr_id="H0STCNI0",
        columns=_WS_ORDER_COLUMNS, mapper=order_update_from_ws_record,
        include_control=False, auto_reconnect=False, buffer_size=10,
    )
    # Build a body with ^-joined values for every column.
    # Order qty=10, filled=3, RFUS_YN=0, CNTG_YN=2 (체결).
    values = {
        "CUST_ID": "U", "ACNT_NO": "A", "ODER_NO": "0000000001",
        "OODER_NO": "", "SELN_BYOV_CLS": "02", "RCTF_CLS": "0",
        "ODER_KIND": "00", "ODER_COND": "0", "STCK_SHRN_ISCD": "005930",
        "CNTG_QTY": "3", "CNTG_UNPR": "70000", "STCK_CNTG_HOUR": "143000",
        "RFUS_YN": "0", "CNTG_YN": "2", "ACPT_YN": "2",
        "BRNC_NO": "01577", "ODER_QTY": "10",
        "ACNT_NAME": "", "ORD_COND_PRC": "0", "ORD_EXG_GB": "1",
        "POPUP_YN": "N", "FILLER": "", "CRDT_CLS": "",
        "CRDT_LOAN_DATE": "", "CNTG_ISNM40": "삼성전자", "ODER_PRC": "70000",
    }
    body = "^".join(values[c] for c in _WS_ORDER_COLUMNS)
    frame = f"0|H0STCNI0|1|{body}"
    out = stream._parse(frame)
    assert len(out) == 1
    u = out[0]
    assert u.status is OrderStatus.PARTIALLY_FILLED
    assert u.filled_qty == Decimal("3")


# ─── _parse_kst_datetime leading-zero handling ─────────────


def test_parse_kst_datetime_handles_missing_leading_zero():
    """KIS sometimes emits '93000' instead of '093000' for 09:30:00."""
    from tooja.brokers.kis._mappers import _parse_kst_datetime
    d = _parse_kst_datetime("20260601", "93000")
    assert d is not None
    # 09:30:00 KST -> 00:30:00 UTC
    assert d.hour == 0
    assert d.minute == 30


# ─── PINGPONG keepalive ────────────────────────────────────


def test_pingpong_triggers_echo_send():
    """When the server sends a PINGPONG control frame, _handle_control schedules
    an echo to keep the connection alive."""
    import asyncio

    broker = _fake_broker()
    topic = _SubscriptionTopic(
        tr_id="H0STCNT0", columns=_WS_QUOTE_COLUMNS, mapper=quote_from_ws_record,
    )
    stream = KisWsStream(
        broker, topic, symbols=["005930"],
        include_control=False, auto_reconnect=False, buffer_size=10,
    )
    stream._ws = MagicMock()
    stream._ws.send = AsyncMock()

    ping_frame = '{"header":{"tr_id":"PINGPONG","datetime":"20260601143000"}}'

    async def _run():
        result = stream._handle_control(ping_frame)
        # Give the scheduled send-task a chance to run.
        await asyncio.sleep(0)
        return result

    out = asyncio.run(_run())
    assert out == []
    stream._ws.send.assert_called_once_with(ping_frame)
