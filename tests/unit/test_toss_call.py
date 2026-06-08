"""Toss call bridge: error classification, auth-header injection, retries."""

from __future__ import annotations

from types import SimpleNamespace

import httpx
import pytest

from tooja.brokers.toss._call import call
from tooja.brokers.toss._rate_limit import DEFAULT
from tooja.brokers.toss.mapping import classify_toss_error
from tooja.brokers.toss.raw.base import BASE_URL, TossApiExecutor, TossBaseModel
from tooja.core.errors import (
    AuthError,
    BrokerAPIError,
    BrokerError,
    NetworkError,
    RateLimitError,
)
from tooja.core.errors import TimeoutError as BTimeout
from tooja.core.rate_limit import TokenBucket


# --- dummy response model + executors ----------------------------------------


class _Echo(TossBaseModel):
    ok: bool = True


class _AccountExecutor(TossApiExecutor[_Echo]):
    PATH = "/api/v1/with-account"
    METHOD = "GET"
    RESPONSE_TYPE = _Echo
    HEADER_PARAMS = ("X-Tossinvest-Account",)


class _PlainExecutor(TossApiExecutor[_Echo]):
    PATH = "/api/v1/plain"
    METHOD = "GET"
    RESPONSE_TYPE = _Echo


# --- fake broker --------------------------------------------------------------


def _make_broker(handler, *, account_seq=42):
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport, base_url=BASE_URL)
    state = {"token": "tok-1", "invalidated": 0, "issues": 0}

    async def get_access_token():
        state["issues"] += 1
        return state["token"]

    def invalidate_token():
        state["invalidated"] += 1
        state["token"] = "tok-2"

    broker = SimpleNamespace(
        http=http,
        base_url=BASE_URL,
        account_seq=account_seq,
        rate_limit=DEFAULT,
        _rate_limiter=TokenBucket(capacity=DEFAULT.per_sec),
        get_access_token=get_access_token,
        invalidate_token=invalidate_token,
        _require_open=lambda: None,
    )
    broker._state = state
    return broker


def _ok_envelope(captured):
    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"result": {"ok": True}})

    return handler


# --- classify_toss_error ------------------------------------------------------


@pytest.mark.parametrize("code", ["invalid-token", "expired-token", "edge-blocked", "invalid_client"])
def test_classify_auth_errors(code):
    assert classify_toss_error(code, 401) is AuthError


@pytest.mark.parametrize("code", ["rate-limit-exceeded", "edge-rate-limit-exceeded"])
def test_classify_rate_limit(code):
    assert classify_toss_error(code, 429) is RateLimitError


def test_classify_order_not_found():
    cls = classify_toss_error("order-not-found", 404)
    assert issubclass(cls, BrokerError)


def test_classify_generic_falls_to_broker_api_error():
    assert classify_toss_error("something-weird", 400) is BrokerAPIError


# --- header injection ---------------------------------------------------------


@pytest.mark.asyncio
async def test_bearer_header_always_present():
    captured = []
    broker = _make_broker(_ok_envelope(captured))
    async with broker.http:
        resp = await call(broker, _PlainExecutor)
    assert resp.ok is True
    assert captured[0].headers["Authorization"] == "Bearer tok-1"
    assert "X-Tossinvest-Account" not in captured[0].headers


@pytest.mark.asyncio
async def test_account_header_injected_only_for_declaring_executor():
    captured = []
    broker = _make_broker(_ok_envelope(captured))
    async with broker.http:
        await call(broker, _AccountExecutor)
    assert captured[0].headers["Authorization"] == "Bearer tok-1"
    assert captured[0].headers["X-Tossinvest-Account"] == "42"


@pytest.mark.asyncio
async def test_missing_account_seq_raises():
    captured = []
    broker = _make_broker(_ok_envelope(captured), account_seq=None)
    async with broker.http:
        with pytest.raises(BrokerError) as ei:
            await call(broker, _AccountExecutor)
    assert "account_seq" in str(ei.value)
    assert captured == []  # never hit the wire


@pytest.mark.asyncio
async def test_extra_headers_merged():
    captured = []
    broker = _make_broker(_ok_envelope(captured))
    async with broker.http:
        await call(broker, _PlainExecutor, extra_headers={"X-Custom": "v"})
    assert captured[0].headers["X-Custom"] == "v"


# --- token-expiry free retry --------------------------------------------------


@pytest.mark.asyncio
async def test_invalid_token_triggers_one_reissue_and_retry():
    captured = []

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if len(captured) == 1:
            return httpx.Response(
                401, json={"error": {"code": "invalid-token", "message": "expired"}}
            )
        return httpx.Response(200, json={"result": {"ok": True}})

    broker = _make_broker(handler)
    async with broker.http:
        resp = await call(broker, _PlainExecutor)
    assert resp.ok is True
    assert broker._state["invalidated"] == 1
    assert captured[1].headers["Authorization"] == "Bearer tok-2"


@pytest.mark.asyncio
async def test_invalid_token_retry_only_once():
    captured = []

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            401, json={"error": {"code": "invalid-token", "message": "expired"}}
        )

    broker = _make_broker(handler)
    async with broker.http:
        with pytest.raises(AuthError):
            await call(broker, _PlainExecutor)
    assert len(captured) == 2  # original + one free retry, then give up


# --- error translation --------------------------------------------------------


@pytest.mark.asyncio
async def test_error_envelope_translated_to_mapped_brokererror():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"error": {"code": "order-not-found", "message": "no such order"}}
        )

    broker = _make_broker(handler)
    async with broker.http:
        with pytest.raises(BrokerError) as ei:
            await call(broker, _PlainExecutor)
    err = ei.value
    assert err.broker == "toss"
    assert err.raw_code == "order-not-found"
    assert err.raw_message == "no such order"
    assert err.endpoint == "/api/v1/plain"


@pytest.mark.asyncio
async def test_generic_4xx_is_broker_api_error():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400, json={"error": {"code": "bad-request", "message": "nope"}}
        )

    broker = _make_broker(handler)
    async with broker.http:
        with pytest.raises(BrokerAPIError):
            await call(broker, _PlainExecutor)


@pytest.mark.asyncio
async def test_429_retries_then_raises_rate_limit():
    captured = []

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            429, json={"error": {"code": "rate-limit-exceeded", "message": "slow down"}}
        )

    broker = _make_broker(handler)
    # shrink backoff/retries so the test is fast
    from tooja.core.rate_limit import RateLimitConfig

    broker.rate_limit = RateLimitConfig(per_sec=5, max_retries=2, base_backoff=0.0)
    async with broker.http:
        with pytest.raises(RateLimitError):
            await call(broker, _PlainExecutor)
    assert len(captured) == 3  # initial + 2 retries (attempts consumed)


@pytest.mark.asyncio
async def test_network_error_wrapped():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom")

    broker = _make_broker(handler)
    async with broker.http:
        with pytest.raises(NetworkError) as ei:
            await call(broker, _PlainExecutor)
    assert ei.value.endpoint == "/api/v1/plain"


@pytest.mark.asyncio
async def test_timeout_wrapped():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow")

    broker = _make_broker(handler)
    async with broker.http:
        with pytest.raises(BTimeout) as ei:
            await call(broker, _PlainExecutor)
    assert ei.value.endpoint == "/api/v1/plain"
