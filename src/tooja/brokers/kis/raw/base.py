from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation
from typing import Annotated, Any, AsyncGenerator, ClassVar, Generic, TypeVar

import httpx
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, PrivateAttr

logger = logging.getLogger(__name__)

REAL_BASE_URL = "https://openapi.koreainvestment.com:9443"
VIRTUAL_BASE_URL = "https://openapivts.koreainvestment.com:29443"

_PAGINATION_KEYS = ("CTX_AREA_FK100", "CTX_AREA_FK200", "CTX_AREA_NK100", "CTX_AREA_NK200")


def _parse_decimal(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip().replace(",", "")
        if not v:
            return None
        try:
            return Decimal(v)
        except (InvalidOperation, ValueError):
            return None
    return v


SDecimal = Annotated[Decimal | None, BeforeValidator(_parse_decimal)]


class KisRequestHeader(BaseModel):
    """KIS API request header."""

    model_config = ConfigDict(populate_by_name=True)

    authorization: str
    appkey: str
    appsecret: str
    personalseckey: str | None = None
    tr_id: str
    tr_cont: str | None = None
    custtype: str | None = None
    seq_no: str | None = None
    mac_address: str | None = None
    phone_number: str | None = None
    ip_addr: str | None = None
    gt_uid: str | None = None


class KisResponseHeader(BaseModel):
    """KIS API response header."""

    model_config = ConfigDict(populate_by_name=True)

    content_type: str | None = Field(None, alias="content-type")
    tr_id: str | None = None
    tr_cont: str | None = None
    gt_uid: str | None = None


class KisBaseModel(BaseModel):
    """KIS response base model that preserves response headers."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    _headers: KisResponseHeader | None = PrivateAttr(default=None)

    @property
    def headers(self) -> KisResponseHeader | None:
        return self._headers


class KisCommonResponse(KisBaseModel):
    """Common response fields (rt_cd / msg_cd / msg1)."""

    rt_cd: str
    msg_cd: str
    msg1: str


class KisApiError(Exception):
    def __init__(self, message: str, code: str, rt_cd: str):
        self.message = message
        self.code = code
        self.rt_cd = rt_cd
        super().__init__(f"[{code}] {message} (rt_cd={rt_cd})")


class TokenExpiredError(Exception):
    """Token expired (EGW00123)."""


TRequest = TypeVar("TRequest", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)

HeadersLike = KisRequestHeader | dict[str, str] | None


class ApiExecutor(Generic[TRequest, TResponse]):
    """Executor for a single KIS endpoint."""

    PATH: ClassVar[str]
    METHOD: ClassVar[str] = "GET"
    RESPONSE_TYPE: ClassVar[type]
    TR_ID: ClassVar[str | None] = None
    TR_ID_VIRTUAL: ClassVar[str | None] = None

    def __init__(
        self,
        request: TRequest,
        headers: HeadersLike = None,
        base_url: str | None = None,
        is_virtual: bool = False,
        client: httpx.AsyncClient | None = None,
    ):
        self.request = request
        self._custom_headers = headers
        self.is_virtual = is_virtual
        self.base_url = base_url or (VIRTUAL_BASE_URL if is_virtual else REAL_BASE_URL)
        self._client = client

    def _resolve_tr_id(self) -> str | None:
        if self.is_virtual:
            return self.TR_ID_VIRTUAL or self.TR_ID
        return self.TR_ID

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json; charset=utf-8"}

        tr_id = self._resolve_tr_id()
        if tr_id:
            headers["tr_id"] = tr_id

        if self._custom_headers is None:
            return headers
        if isinstance(self._custom_headers, KisRequestHeader):
            headers.update(
                self._custom_headers.model_dump(by_alias=True, exclude_none=True)
            )
        else:
            headers.update(self._custom_headers)
        return headers

    async def execute(self) -> TResponse:
        url = f"{self.base_url.rstrip('/')}/{self.PATH.lstrip('/')}"
        headers = self._build_headers()
        payload = self.request.model_dump(by_alias=True, exclude_none=True)

        if self._client is not None:
            response = await self._send(self._client, url, headers, payload)
        else:
            async with httpx.AsyncClient() as client:
                response = await self._send(client, url, headers, payload)

        return self._parse_response(response)

    async def _send(
        self,
        client: httpx.AsyncClient,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
    ) -> httpx.Response:
        if self.METHOD == "POST":
            return await client.post(url, headers=headers, json=payload)
        if self.METHOD == "GET":
            return await client.get(url, headers=headers, params=payload)
        raise ValueError(f"Unsupported method: {self.METHOD}")

    def _parse_response(self, response: httpx.Response) -> TResponse:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._raise_for_status_error(e)
            raise

        parsed: TResponse = self.RESPONSE_TYPE(**response.json())

        try:
            parsed._headers = KisResponseHeader(**response.headers)  # type: ignore[attr-defined]
        except Exception as e:
            logger.warning("Failed to parse response headers: %s", e)

        if getattr(parsed, "rt_cd", "0") != "0":
            raise KisApiError(
                getattr(parsed, "msg1", "Unknown Error"),
                getattr(parsed, "msg_cd", "Unknown Code"),
                getattr(parsed, "rt_cd"),
            )

        return parsed

    def _raise_for_status_error(self, e: httpx.HTTPStatusError) -> None:
        try:
            body = e.response.json()
        except ValueError:
            logger.error("HTTP %s: %s", e.response.status_code, e.response.text)
            return

        if isinstance(body, dict) and body.get("msg_cd") == "EGW00123":
            raise TokenExpiredError(f"Token expired: {body.get('msg1')}") from e

        logger.error("HTTP %s: %s", e.response.status_code, body)


class PaginatedApiExecutor(ApiExecutor[TRequest, TResponse]):
    """Executor that supports tr_cont continuation queries (one request per page)."""

    async def paginate(self) -> AsyncGenerator[TResponse, None]:
        request = self._reset_pagination_keys(self.request)
        custom_headers = self._custom_headers

        while True:
            executor = type(self)(
                request=request,
                headers=custom_headers,
                base_url=self.base_url,
                is_virtual=self.is_virtual,
                client=self._client,
            )
            response = await executor.execute()
            yield response

            response_headers = getattr(response, "headers", None)
            tr_cont = getattr(response_headers, "tr_cont", None)
            if tr_cont not in ("F", "M"):
                break

            custom_headers = self._with_tr_cont(custom_headers, "N")
            request = self._carry_pagination_keys(request, response)

    async def execute_all(self) -> list[TResponse]:
        return [r async for r in self.paginate()]

    @staticmethod
    def _reset_pagination_keys(request: TRequest) -> TRequest:
        updates = {k: "" for k in _PAGINATION_KEYS if hasattr(request, k)}
        return request.model_copy(update=updates) if updates else request

    @staticmethod
    def _carry_pagination_keys(request: TRequest, response: TResponse) -> TRequest:
        updates = {
            k: getattr(response, k, "")
            for k in _PAGINATION_KEYS
            if hasattr(request, k) and hasattr(response, k)
        }
        return request.model_copy(update=updates) if updates else request

    @staticmethod
    def _with_tr_cont(headers: HeadersLike, value: str) -> HeadersLike:
        if headers is None:
            return {"tr_cont": value}
        if isinstance(headers, KisRequestHeader):
            return headers.model_copy(update={"tr_cont": value})
        return {**headers, "tr_cont": value}
