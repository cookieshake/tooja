"""TokenBucket + EGW00201 retry/backoff."""

from __future__ import annotations

import asyncio
import time

import pytest

from tooja.brokers.kis._rate_limit import TokenBucket


@pytest.mark.asyncio
async def test_token_bucket_allows_capacity_immediately():
    """Capacity-many acquires should complete near-instantly."""
    bucket = TokenBucket(capacity=5)
    t0 = time.monotonic()
    for _ in range(5):
        await bucket.acquire()
    elapsed = time.monotonic() - t0
    assert elapsed < 0.05


@pytest.mark.asyncio
async def test_token_bucket_throttles_beyond_capacity():
    """The 4th acquire on a capacity-3 bucket must wait until the 1st expires."""
    bucket = TokenBucket(capacity=3)
    t0 = time.monotonic()
    for _ in range(3):
        await bucket.acquire()
    # 4th should wait roughly until ~1s after t0.
    await bucket.acquire()
    elapsed = time.monotonic() - t0
    # Allow scheduling jitter: at least 0.9s, less than 1.5s.
    assert 0.9 < elapsed < 1.5


@pytest.mark.asyncio
async def test_token_bucket_concurrent_acquires_share_throttle():
    """N=10 concurrent acquires on a capacity-5 bucket finish in ~1 second."""
    bucket = TokenBucket(capacity=5)
    t0 = time.monotonic()
    await asyncio.gather(*(bucket.acquire() for _ in range(10)))
    elapsed = time.monotonic() - t0
    assert 0.9 < elapsed < 1.5


def test_token_bucket_capacity_must_be_positive():
    with pytest.raises(ValueError):
        TokenBucket(capacity=0)


# ─── EGW00201 retry/backoff ──────────────────────────


@pytest.mark.asyncio
async def test_call_retries_on_rate_limit_then_succeeds(monkeypatch):
    """When KIS returns EGW00201 twice then OK, _call.call should return OK."""
    from tooja.brokers.kis import _call as call_mod
    from tooja.brokers.kis.raw.base import KisApiError

    calls: list[int] = []

    class _Sentinel:
        PATH = "/x"

    async def fake_once(broker, executor_cls, request, *, tr_id, extra_headers):
        calls.append(len(calls))
        if len(calls) < 3:
            raise KisApiError("초당 거래건수를 초과하였습니다.", "EGW00201", "1")
        return "OK"

    # Speed up backoff to keep the test fast.
    monkeypatch.setattr(call_mod, "_RATE_LIMIT_BASE_BACKOFF", 0.001)
    monkeypatch.setattr(call_mod, "_call_once", fake_once)

    class _FakeBroker:
        def _require_open(self): pass
        def invalidate_token(self): pass

    result = await call_mod.call(_FakeBroker(), _Sentinel, request=None)
    assert result == "OK"
    assert len(calls) == 3


@pytest.mark.asyncio
async def test_call_exhausts_rate_limit_retries(monkeypatch):
    from tooja.brokers.kis import _call as call_mod
    from tooja.brokers.kis.raw.base import KisApiError
    from tooja.core.errors import RateLimitError

    async def always_rate_limited(broker, executor_cls, request, *, tr_id, extra_headers):
        raise KisApiError("초당 거래건수를 초과하였습니다.", "EGW00201", "1")

    monkeypatch.setattr(call_mod, "_RATE_LIMIT_BASE_BACKOFF", 0.001)
    monkeypatch.setattr(call_mod, "_call_once", always_rate_limited)

    class _Sentinel:
        PATH = "/x"

    class _FakeBroker:
        def _require_open(self): pass
        def invalidate_token(self): pass

    with pytest.raises(RateLimitError) as ei:
        await call_mod.call(_FakeBroker(), _Sentinel, request=None)
    assert ei.value.raw_code == "EGW00201"


@pytest.mark.asyncio
async def test_call_non_rate_limit_error_raises_immediately(monkeypatch):
    """An unrelated KisApiError must not trigger retries."""
    from tooja.brokers.kis import _call as call_mod
    from tooja.brokers.kis.raw.base import KisApiError
    from tooja.core.errors import AuthError

    calls = []

    async def fake_once(broker, executor_cls, request, *, tr_id, extra_headers):
        calls.append(1)
        raise KisApiError("권한 없음", "EGW00121", "1")  # auth, not rate limit

    monkeypatch.setattr(call_mod, "_call_once", fake_once)

    class _Sentinel:
        PATH = "/x"

    class _FakeBroker:
        def _require_open(self): pass
        def invalidate_token(self): pass

    with pytest.raises(AuthError):
        await call_mod.call(_FakeBroker(), _Sentinel, request=None)
    assert len(calls) == 1  # no retries
