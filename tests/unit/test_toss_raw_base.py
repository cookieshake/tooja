"""Toss raw base: TDecimal parsing, error envelope, executor request building."""

from __future__ import annotations

from decimal import Decimal

import httpx
from pydantic import Field

from tooja.brokers.toss.raw.base import (
    TDecimal,
    TossApiError,
    TossApiExecutor,
    TossBaseModel,
    parse_error_envelope,
)


class _Req(TossBaseModel):
    symbol: str
    count: int | None = None


class _Resp(TossBaseModel):
    symbol: str
    last_price: TDecimal = Field(default=None, alias="lastPrice")


def test_tdecimal_parses_string_to_decimal():
    class M(TossBaseModel):
        v: TDecimal = None
    assert M(v="72000").v == Decimal("72000")
    assert M(v=None).v is None
    assert M(v="").v is None  # empty string -> None, not a crash


def test_error_envelope_parsing():
    body = {"error": {"requestId": "r1", "code": "order-not-found", "message": "없음", "data": {"x": 1}}}
    err = parse_error_envelope(body, http_status=404)
    assert isinstance(err, TossApiError)
    assert err.code == "order-not-found"
    assert err.http_status == 404
    assert err.request_id == "r1"
    assert err.data == {"x": 1}


def test_error_envelope_oauth_shape():
    # token endpoint uses {error, error_description} not the envelope
    body = {"error": "invalid_client", "error_description": "bad secret"}
    err = parse_error_envelope(body, http_status=401)
    assert err.code == "invalid_client"
    assert "bad secret" in (err.message or "")


def test_executor_get_builds_query_and_path(monkeypatch):
    captured = {}

    class GetThing(TossApiExecutor):
        PATH = "/api/v1/orders/{orderId}"
        METHOD = "GET"
        RESPONSE_TYPE = _Resp
        PATH_PARAMS = ("orderId",)
        QUERY_PARAMS = ("symbol", "count")

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        return httpx.Response(200, json={"symbol": "005930", "lastPrice": "72000"})

    async def run():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x") as client:
            ex = GetThing(
                path_params={"orderId": "abc"},
                query={"symbol": "005930", "count": 5},
                client=client,
                base_url="https://x",
            )
            return await ex.execute()

    import asyncio
    resp = asyncio.run(run())
    assert captured["method"] == "GET"
    assert "/api/v1/orders/abc" in captured["url"]
    assert "symbol=005930" in captured["url"] and "count=5" in captured["url"]
    assert resp.symbol == "005930"
    assert resp.last_price == Decimal("72000")


def test_executor_post_json_body(monkeypatch):
    captured = {}

    class PostThing(TossApiExecutor):
        PATH = "/api/v1/orders"
        METHOD = "POST"
        RESPONSE_TYPE = _Resp
        BODY_CONTENT = "json"

    async def handler(request: httpx.Request) -> httpx.Response:
        import json
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"symbol": "005930"})

    async def run():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x") as client:
            ex = PostThing(body={"symbol": "005930", "side": "BUY"}, client=client, base_url="https://x")
            return await ex.execute()

    import asyncio
    asyncio.run(run())
    assert captured["body"] == {"symbol": "005930", "side": "BUY"}


def test_no_blanket_camel_alias_for_snake_wire_keys():

    class TokenReq(TossBaseModel):
        grant_type: str
        client_id: str

    m = TokenReq(grant_type="client_credentials", client_id="abc")
    dumped = m.model_dump(by_alias=True)
    assert dumped == {"grant_type": "client_credentials", "client_id": "abc"}
