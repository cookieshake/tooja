"""Shared call helper — wraps a raw Toss executor with auth-header injection,
error mapping, and retries.

Every subclient (market/account/orders/...) goes through `call(broker, executor_cls, ...)`:
    1. broker._require_open()
    2. acquire token bucket (client-side rate limit)
    3. fetch OAuth access token; inject `Authorization: Bearer <token>`
    4. inject `X-Tossinvest-Account` iff the executor declares that header param
    5. merge any extra headers
    6. execute
    7. on TossApiError:
         - token-expiry codes -> invalidate + retry once (free, no attempt used)
         - 429 -> exponential-backoff retry up to rate_limit.max_retries
         - else translate via classify_toss_error -> raise mapped BrokerError
    8. wrap httpx.TimeoutException -> TimeoutError, httpx.HTTPError -> NetworkError
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

import httpx

from tooja.brokers.toss.mapping import classify_toss_error
from tooja.brokers.toss.raw.base import TossApiError, TossApiExecutor
from tooja.core.errors import BrokerAPIError, BrokerError, NetworkError

if TYPE_CHECKING:
    from tooja.brokers.toss.broker import TossBroker

logger = logging.getLogger(__name__)

_ACCOUNT_HEADER = "X-Tossinvest-Account"
# Token-expiry codes get one free reissue+retry (does not consume an attempt).
_TOKEN_EXPIRY_CODES = frozenset({"invalid-token", "expired-token"})


async def call(
    broker: "TossBroker",
    executor_cls: type[TossApiExecutor],
    *,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    body: Any = None,
    extra_headers: dict[str, str] | None = None,
) -> Any:
    """Execute one Toss REST call with auth + error mapping + retries."""
    broker._require_open()  # noqa: SLF001 — peer module within the broker package

    cfg = broker.rate_limit
    token_retry_used = False
    attempt = 0
    while attempt <= cfg.max_retries:
        try:
            return await _call_once(
                broker, executor_cls,
                path_params=path_params, query=query, body=body,
                extra_headers=extra_headers,
            )
        except TossApiError as e:
            if e.code in _TOKEN_EXPIRY_CODES and not token_retry_used:
                broker.invalidate_token()
                token_retry_used = True
                continue  # free retry — do NOT increment attempt
            if e.http_status == 429 and attempt < cfg.max_retries:
                backoff = cfg.base_backoff * (2 ** attempt)
                logger.warning(
                    "Toss rate limited on %s (%s); backing off %.2fs (attempt %d/%d)",
                    executor_cls.PATH, e.code, backoff, attempt + 1, cfg.max_retries,
                )
                await asyncio.sleep(backoff)
                attempt += 1
                continue
            raise _translate(e, executor_cls.PATH) from e
    # Unreachable: loop returns or raises on every path above.
    raise AssertionError("unreachable")


async def _call_once(
    broker: "TossBroker",
    executor_cls: type[TossApiExecutor],
    *,
    path_params: dict[str, Any] | None,
    query: dict[str, Any] | None,
    body: Any,
    extra_headers: dict[str, str] | None,
) -> Any:
    async with broker._rate_limiter:  # noqa: SLF001 — peer module
        token = await broker.get_access_token()
        headers: dict[str, str] = {"Authorization": f"Bearer {token}"}

        if _ACCOUNT_HEADER in executor_cls.HEADER_PARAMS:
            if broker.account_seq is None:
                raise BrokerError(
                    "Toss account/order operations require account_seq; "
                    "pass TossBroker(account_seq=...). "
                    "List via broker.raw.account.get_accounts().",
                    broker="toss",
                    endpoint=executor_cls.PATH,
                )
            headers[_ACCOUNT_HEADER] = str(broker.account_seq)

        if extra_headers:
            headers.update(extra_headers)

        executor = executor_cls(
            path_params=path_params,
            query=query,
            headers=headers,
            body=body,
            client=broker.http,
            base_url=broker.base_url,
        )
        try:
            return await executor.execute()
        except httpx.TimeoutException as e:
            from tooja.core.errors import TimeoutError as BTimeout

            raise BTimeout(
                f"Toss request timed out: {executor_cls.PATH}",
                broker="toss",
                endpoint=executor_cls.PATH,
            ) from e
        except httpx.HTTPError as e:
            raise NetworkError(
                f"Toss network error: {e}",
                broker="toss",
                endpoint=executor_cls.PATH,
            ) from e


def _translate(err: TossApiError, endpoint: str) -> BrokerError:
    cls = classify_toss_error(err.code, err.http_status)
    if cls is BrokerAPIError:
        logger.warning(
            "Toss unmapped error code %s (HTTP %s) on %s: %s — falling back to "
            "BrokerAPIError (consider adding it to classify_toss_error)",
            err.code, err.http_status, endpoint, err.message,
        )
    return cls(
        err.message or err.code,
        broker="toss",
        raw_code=err.code,
        raw_message=err.message,
        endpoint=endpoint,
    )
