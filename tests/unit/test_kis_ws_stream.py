"""Regression tests for KisWsStream / KisOrderUpdateStream frame parsing."""

from __future__ import annotations

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock


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


def test_quote_columns_match_raw_subscriber():
    """_WS_QUOTE_COLUMNS must equal the raw H0STCNT0 COLUMNS source of truth
    so multi-record packets stay aligned and CCLD_DVSN is at the right index."""
    from tooja.brokers.kis.raw.domestic_stock_ws.h0stcnt0 import H0stcnt0Subscriber
    assert _WS_QUOTE_COLUMNS == H0stcnt0Subscriber.COLUMNS
    # Trade side mapping in trade_from_ws_record reads CCLD_DVSN.
    assert "CCLD_DVSN" in _WS_QUOTE_COLUMNS


def test_trade_topic_uses_full_quote_columns():
    """Regression: _TRADE_TOPIC must share _WS_QUOTE_COLUMNS, not a prefix+1
    variant — otherwise CCLD_DVSN lands on the wrong index."""
    from tooja.brokers.kis.stream import _TRADE_TOPIC, _QUOTE_TOPIC
    assert _TRADE_TOPIC.columns == _QUOTE_TOPIC.columns


def test_orderbook_columns_match_raw_subscriber():
    from tooja.brokers.kis.raw.domestic_stock_ws.h0stasp0 import H0stasp0Subscriber
    from tooja.brokers.kis.stream import _ORDERBOOK_TOPIC
    assert _ORDERBOOK_TOPIC.columns == H0stasp0Subscriber.COLUMNS


def test_multi_record_quote_frame_parses_all_records():
    """A 2-record H0STCNT0 frame: with the right per=46 stride, both records
    should produce a Quote. A short stride would garble record #2."""
    from tooja.brokers.kis.raw.domestic_stock_ws.h0stcnt0 import H0stcnt0Subscriber

    cols = H0stcnt0Subscriber.COLUMNS
    # Build two records with distinct tickers; only the fields used by
    # quote_from_ws_record need real values, the rest can be empty strings.
    def _make(ticker: str, time_s: str, prpr: str) -> list[str]:
        vals = [""] * len(cols)
        idx = {c: i for i, c in enumerate(cols)}
        vals[idx["MKSC_SHRN_ISCD"]] = ticker
        vals[idx["STCK_CNTG_HOUR"]] = time_s
        vals[idx["STCK_PRPR"]] = prpr
        vals[idx["PRDY_VRSS_SIGN"]] = "2"
        return vals

    body_tokens = _make("005930", "143000", "70000") + _make("035720", "143100", "55000")
    body = "^".join(body_tokens)
    frame = f"0|H0STCNT0|2|{body}"

    broker = _fake_broker()
    topic = _SubscriptionTopic(
        tr_id="H0STCNT0", columns=cols, mapper=quote_from_ws_record,
    )
    stream = KisWsStream(
        broker, topic, symbols=["005930"],
        include_control=False, auto_reconnect=False, buffer_size=10,
    )
    out = stream._parse(frame)
    assert len(out) == 2
    assert {q.symbol.ticker for q in out} == {"005930", "035720"}


def test_pingpong_echo_swallows_send_failure():
    """If the WS is closing when we try to echo PINGPONG, the background task
    must not raise an unhandled exception into the loop."""
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
    stream._ws.send = AsyncMock(side_effect=RuntimeError("connection closed"))

    ping_frame = '{"header":{"tr_id":"PINGPONG"}}'

    async def _run():
        stream._handle_control(ping_frame)
        # Drain pending tasks; if the create_task'd send raises uncaught,
        # asyncio will surface it during shutdown.
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

    asyncio.run(_run())
    stream._ws.send.assert_called_once_with(ping_frame)
