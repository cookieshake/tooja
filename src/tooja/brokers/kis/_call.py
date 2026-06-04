"""Shared call helper — wraps raw executor with auth header injection + error mapping.

Every subclient (market/account/orders/...) goes through `call(broker, executor)`:
    1. fetch access_token (and retry once on EGW00123 token-expired)
    2. inject standard auth headers + tr_id
    3. execute
    4. translate KisApiError -> mapped BrokerError via classify_kis_error
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import httpx

from tooja.brokers.kis.mapping import classify_kis_error
from tooja.brokers.kis.raw.base import ApiExecutor, KisApiError, TokenExpiredError
from tooja.core.errors import BrokerAPIError, BrokerError, NetworkError

if TYPE_CHECKING:
    from tooja.brokers.kis.broker import KisBroker

TResponse = TypeVar("TResponse")


async def call(
    broker: "KisBroker",
    executor_cls: type[ApiExecutor],
    request,
    *,
    tr_id: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> object:
    """Execute one KIS REST call with auth + error mapping.

    `tr_id` defaults to executor's TR_ID (resolved for real/virtual env).
    """
    broker._require_open()  # noqa: SLF001 — peer module within the broker package
    return await _call_once(
        broker, executor_cls, request, tr_id=tr_id, extra_headers=extra_headers, retry=True
    )


async def _call_once(
    broker: "KisBroker",
    executor_cls: type[ApiExecutor],
    request,
    *,
    tr_id: str | None,
    extra_headers: dict[str, str] | None,
    retry: bool,
):
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
    except TokenExpiredError:
        broker.invalidate_token()
        if retry:
            return await _call_once(
                broker, executor_cls, request,
                tr_id=tr_id, extra_headers=extra_headers, retry=False,
            )
        raise
    except KisApiError as e:
        raise _translate(e, executor_cls.PATH) from e
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
