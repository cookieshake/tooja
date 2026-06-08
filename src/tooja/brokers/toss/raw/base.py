"""Toss raw layer base — executor, base model, decimal coercion, error envelope.

Generated endpoint modules subclass TossApiExecutor and declare PATH/METHOD plus
which named params are path/query/header and whether a JSON or form body is sent.
Auth headers (Bearer, X-Tossinvest-Account) are injected by the adapter's _call
layer, not here — the executor only carries the wire shape of one endpoint.
"""

from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation
from typing import Annotated, Any, ClassVar, Generic, Literal, TypeVar

import httpx
from pydantic import BaseModel, BeforeValidator, ConfigDict

logger = logging.getLogger(__name__)

BASE_URL = "https://openapi.tossinvest.com"


def _parse_decimal(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        if not v:
            return None
        try:
            return Decimal(v)
        except (InvalidOperation, ValueError):
            return None
    return v


TDecimal = Annotated[Decimal | None, BeforeValidator(_parse_decimal)]


class TossBaseModel(BaseModel):
    """Base for all generated Toss request/response models."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class TossApiError(Exception):
    """A Toss API error — from the `{error:{code,message,...}}` envelope or the
    OAuth `{error, error_description}` shape."""

    def __init__(
        self,
        code: str,
        message: str | None = None,
        *,
        http_status: int,
        request_id: str | None = None,
        data: Any = None,
    ):
        self.code = code
        self.message = message
        self.http_status = http_status
        self.request_id = request_id
        self.data = data
        super().__init__(f"[{http_status} {code}] {message}")


def parse_error_envelope(body: Any, *, http_status: int) -> TossApiError:
    """Build a TossApiError from a parsed JSON error body (either shape)."""
    if isinstance(body, dict) and isinstance(body.get("error"), dict):
        e = body["error"]
        return TossApiError(
            code=e.get("code", "unknown"),
            message=e.get("message"),
            http_status=http_status,
            request_id=e.get("requestId"),
            data=e.get("data"),
        )
    if isinstance(body, dict) and isinstance(body.get("error"), str):
        # OAuth2 error shape
        return TossApiError(
            code=body["error"],
            message=body.get("error_description"),
            http_status=http_status,
        )
    return TossApiError(code="unknown", message=str(body)[:200], http_status=http_status)


TResponse = TypeVar("TResponse", bound=BaseModel)


class TossApiExecutor(Generic[TResponse]):
    """Executor for one Toss endpoint. Subclasses set the ClassVars below.

    The 200 payload returned is the endpoint's `result` (already unwrapped from
    the ApiResponse envelope), parsed into RESPONSE_TYPE. List results are wrapped
    by the generator in a model with a single `root` field — see the generator.
    """

    PATH: ClassVar[str]
    METHOD: ClassVar[str] = "GET"
    RESPONSE_TYPE: ClassVar[type]
    PATH_PARAMS: ClassVar[tuple[str, ...]] = ()
    QUERY_PARAMS: ClassVar[tuple[str, ...]] = ()
    HEADER_PARAMS: ClassVar[tuple[str, ...]] = ()
    BODY_CONTENT: ClassVar[Literal["none", "json", "form"]] = "none"
    ENVELOPED: ClassVar[bool] = True  # 200 wrapped in {"result": ...}; False for /oauth2/token

    def __init__(
        self,
        *,
        path_params: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        body: Any = None,
        client: httpx.AsyncClient,
        base_url: str = BASE_URL,
    ):
        self.path_params = path_params or {}
        self.query = {k: v for k, v in (query or {}).items() if v is not None}
        self.headers = headers or {}
        self.body = body
        self._client = client
        self.base_url = base_url

    def _url(self) -> str:
        path = self.PATH
        for name, val in self.path_params.items():
            path = path.replace("{" + name + "}", str(val))
        return f"{self.base_url.rstrip('/')}{path}"

    async def execute(self) -> TResponse:
        url = self._url()
        kwargs: dict[str, Any] = {"headers": self.headers}
        if self.query:
            kwargs["params"] = self.query
        if self.BODY_CONTENT == "json" and self.body is not None:
            kwargs["json"] = self.body
        elif self.BODY_CONTENT == "form" and self.body is not None:
            kwargs["data"] = self.body

        response = await self._client.request(self.METHOD, url, **kwargs)
        return self._parse(response)

    def _parse(self, response: httpx.Response) -> TResponse:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                body = e.response.json()
            except ValueError:
                logger.error("Toss HTTP %s: %s", e.response.status_code, e.response.text[:200])
                raise TossApiError(
                    code="http-error", message=e.response.text[:200],
                    http_status=e.response.status_code,
                ) from e
            raise parse_error_envelope(body, http_status=e.response.status_code) from e

        payload = response.json()
        if self.ENVELOPED and isinstance(payload, dict) and "result" in payload:
            payload = payload["result"]
        return self._coerce(payload)

    def _coerce(self, payload: Any) -> TResponse:
        # List results are wrapped by the generator in a {root: [...]} model.
        if isinstance(payload, list):
            return self.RESPONSE_TYPE.model_validate({"root": payload})  # type: ignore[attr-defined]
        return self.RESPONSE_TYPE.model_validate(payload)  # type: ignore[attr-defined]
