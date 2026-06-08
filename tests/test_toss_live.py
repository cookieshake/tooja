"""Live, read-only round-trip tests against the real Toss Open API.

Opt-in: marked `toss_live` and excluded from the default run (see pytest.ini).
Run manually with credentials present (env or repo-root .env):

    uv run pytest tests/test_toss_live.py -m toss_live -v

Credentials: TOSS_API_KEY (client_id), TOSS_SECRET_KEY (client_secret),
optional TOSS_ACCOUNT_SEQ (else discovered via GET /accounts). The Toss console
must allow the caller's IP. These tests are READ-ONLY — they never place,
modify, or cancel orders. They exercise the generated raw layer + mappers
against live wire responses (the gap mocked unit/wire-regression tests cannot
cover).
"""

from __future__ import annotations

import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from tooja.core.enums import Currency
from tooja.core.models import Balance, PriceLimit, Quote, StockInfo, StockWarnings

pytestmark = [pytest.mark.toss_live, pytest.mark.asyncio]


def _creds() -> tuple[str, str, int | None]:
    env = dict(os.environ)
    dotenv = Path(__file__).resolve().parent.parent / ".env"
    if dotenv.exists():
        for line in dotenv.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    api_key = env.get("TOSS_API_KEY") or env.get("TOSS_CLIENT_ID")
    secret = env.get("TOSS_SECRET_KEY") or env.get("TOSS_CLIENT_SECRET")
    seq_raw = env.get("TOSS_ACCOUNT_SEQ")
    seq = int(seq_raw) if seq_raw and seq_raw.isdigit() else None
    if not api_key or not secret:
        pytest.skip("TOSS_API_KEY / TOSS_SECRET_KEY not set (env or .env)")
    return api_key, secret, seq


@pytest.fixture
async def broker():
    from tooja.brokers.toss import TossBroker
    from tooja.brokers.toss._call import call
    from tooja.brokers.toss.raw.account.get_accounts import GetAccountsExecutor

    api_key, secret, seq = _creds()
    async with TossBroker(client_id=api_key, client_secret=secret, account_seq=seq) as b:
        if b.account_seq is None:
            # Discover the account seq so account/order read tests can run.
            resp = await call(b, GetAccountsExecutor)
            accounts = getattr(resp, "root", []) or []
            if accounts:
                b.account_seq = accounts[0].account_seq
        yield b


async def test_market_get_quote_krx(broker):
    q = await broker.market.get_quote("005930")
    assert isinstance(q, Quote)
    assert q.symbol.ticker == "005930"
    assert q.price.currency == Currency.KRW
    assert q.price.amount > 0


async def test_market_get_quote_us_ticker_maps_currency(broker):
    q = await broker.market.get_quote("NASD:AAPL")
    assert q.symbol.ticker == "AAPL"
    assert q.price.currency == Currency.USD
    assert q.price.amount > 0


async def test_market_ohlcv_1d_and_1m(broker):
    daily = await broker.market.get_ohlcv("005930", interval="1d", limit=5)
    assert daily and all(c.close.amount > 0 for c in daily)
    minute = await broker.market.get_ohlcv("005930", interval="1m", limit=5)
    assert isinstance(minute, list)


async def test_market_unsupported_interval_raises(broker):
    from tooja.core.errors import UnsupportedOperation

    with pytest.raises(UnsupportedOperation):
        await broker.market.get_ohlcv("005930", interval="5m", limit=5)


async def test_market_price_limits_krx_has_band(broker):
    pl = await broker.market.get_price_limits("005930")
    assert isinstance(pl, PriceLimit)
    assert pl.upper_limit is not None and pl.lower_limit is not None
    assert pl.upper_limit.amount > pl.lower_limit.amount


async def test_info_get_stock(broker):
    s = await broker.info.get_stock("005930")
    assert isinstance(s, StockInfo)
    assert s.name  # non-empty Korean name
    assert s.symbol.ticker == "005930"


async def test_info_get_warnings_returns_model(broker):
    w = await broker.info.get_warnings("005930")
    assert isinstance(w, StockWarnings)


async def test_info_is_holiday_returns_bool(broker):
    assert isinstance(await broker.info.is_holiday(date.today()), bool)


async def test_account_balance_and_buying_power(broker):
    bal = await broker.account.get_balance()
    assert isinstance(bal, Balance)
    bp = await broker.account.get_buying_power(currency=Currency.KRW)
    assert bp.currency == Currency.KRW
    assert bp.amount >= Decimal(0)


async def test_orders_list_open_is_list(broker):
    orders = await broker.orders.list_orders(status="open")
    assert isinstance(orders, list)
