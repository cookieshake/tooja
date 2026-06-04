"""Shared call helper — wraps raw executor with auth header injection + error mapping.

Every subclient (market/account/orders/...) goes through `call(broker, executor)`:
    1. acquire token bucket (client-side rate limit)
    2. fetch access_token (retry once on EGW00123 token-expired)
    3. inject standard auth headers + tr_id
    4. execute
    5. translate KisApiError -> mapped BrokerError via classify_kis_error
    6. retry on EGW00201 (server-side rate limit) with exponential backoff
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, TypeVar

import httpx

from tooja.brokers.kis.mapping import classify_kis_error
from tooja.brokers.kis.raw.base import ApiExecutor, KisApiError, TokenExpiredError
from tooja.core.errors import BrokerAPIError, BrokerError, NetworkError

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker

logger = logging.getLogger(__name__)

TResponse = TypeVar("TResponse")


async def call(
    broker: "KisBroker",
    executor_cls: type[ApiExecutor],
    request,
    *,
    tr_id: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> object:
    """Execute one KIS REST call with auth + error mapping + retries.

    `tr_id` defaults to executor's TR_ID (resolved for real/virtual env).
    """
    broker._require_open()  # noqa: SLF001 — peer module within the broker package
    return await _call_with_retries(
        broker, executor_cls, request, tr_id=tr_id, extra_headers=extra_headers,
    )


async def _call_with_retries(
    broker: "KisBroker",
    executor_cls: type[ApiExecutor],
    request,
    *,
    tr_id: str | None,
    extra_headers: dict[str, str] | None,
) -> object:
    cfg = broker.rate_limit
    token_retry_used = False
    for attempt in range(cfg.max_retries + 1):
        try:
            return await _call_once(
                broker, executor_cls, request,
                tr_id=tr_id, extra_headers=extra_headers,
            )
        except TokenExpiredError:
            if token_retry_used:
                raise
            broker.invalidate_token()
            token_retry_used = True
            continue
        except KisApiError as e:
            translated = _translate(e, executor_cls.PATH)
            if e.code == "EGW00201" and attempt < cfg.max_retries:
                backoff = cfg.base_backoff * (2 ** attempt)
                logger.warning(
                    "KIS EGW00201 rate limited on %s; backing off %.2fs (attempt %d/%d)",
                    executor_cls.PATH, backoff, attempt + 1, cfg.max_retries,
                )
                await asyncio.sleep(backoff)
                continue
            raise translated from e
    # Loop exit without return means the final retry also got EGW00201.
    raise BrokerAPIError(
        f"KIS EGW00201 rate limit retries exhausted ({cfg.max_retries})",
        broker="kis",
        raw_code="EGW00201",
        endpoint=executor_cls.PATH,
    )


async def _call_once(
    broker: "KisBroker",
    executor_cls: type[ApiExecutor],
    request,
    *,
    tr_id: str | None,
    extra_headers: dict[str, str] | None,
):
    async with broker._rate_limiter:  # noqa: SLF001 — peer module
        token = await broker.get_access_token()
        resolved_tr_id = tr_id or _resolve_tr_id(executor_cls, broker.is_virtual)
        headers = broker.build_auth_headers(token, resolved_tr_id or "")
        if extra_headers:
            headers.update(extra_headers)

        executor = executor_cls(
            request=request,
            headers=headers,
            base_url=broker.base_url,
            is_virtual=broker.is_virtual,
            client=broker.http,
        )
        try:
            return await executor.execute()
        except httpx.TimeoutException as e:
            from tooja.core.errors import TimeoutError as BTimeout
            raise BTimeout(
                f"KIS request timed out: {executor_cls.PATH}",
                broker="kis",
                endpoint=executor_cls.PATH,
            ) from e
        except httpx.HTTPError as e:
            raise NetworkError(
                f"KIS network error: {e}",
                broker="kis",
                endpoint=executor_cls.PATH,
            ) from e


def _resolve_tr_id(executor_cls: type[ApiExecutor], is_virtual: bool) -> str | None:
    if is_virtual:
        return executor_cls.TR_ID_VIRTUAL or executor_cls.TR_ID
    return executor_cls.TR_ID


def _translate(err: KisApiError, endpoint: str) -> BrokerError:
    cls = classify_kis_error(err.rt_cd, err.code, err.message) or BrokerAPIError
    return cls(
        err.message,
        broker="kis",
        raw_code=err.code,
        raw_message=err.message,
        endpoint=endpoint,
    )
