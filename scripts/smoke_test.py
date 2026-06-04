"""Smoke test: issue a KIS demo token and call a quote endpoint.

Run: uv run python scripts/smoke_test.py

Requires .env with KIS_APP_KEY, KIS_APP_SECRET, KIS_ENV=demo.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from tooja.brokers.kis.raw.domestic_stock_quotations.inquire_price import (
    InquirePriceExecutor,
    InquirePriceRequest,
)
from tooja.brokers.kis.raw.domestic_stock_trading.inquire_balance import (
    InquireBalanceExecutor,
    InquireBalanceRequest,
)
from tooja.brokers.kis.raw.oauth.tokenp import TokenpExecutor, TokenpRequest


CANONICAL_KEYS = ("APP_KEY", "APP_SECRET", "CANO", "ACNT_PRDT_CD", "HTS_ID")


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    # Promote KIS_<PROFILE>_* into KIS_* based on KIS_ENV.
    profile = "REAL" if env.get("KIS_ENV", "demo").lower() == "real" else "DEMO"
    for key in CANONICAL_KEYS:
        target = f"KIS_{key}"
        source = f"KIS_{profile}_{key}"
        if not env.get(target) and env.get(source):
            env[target] = env[source]
    return env


async def main() -> None:
    env = load_env(Path(__file__).resolve().parent.parent / ".env")
    app_key = env["KIS_APP_KEY"]
    app_secret = env["KIS_APP_SECRET"]
    is_virtual = env.get("KIS_ENV", "demo") == "demo"
    print(f"env: {'demo (virtual)' if is_virtual else 'real'}")

    # 1. Issue access token.
    tok = await TokenpExecutor(
        request=TokenpRequest(
            grant_type="client_credentials",
            appkey=app_key,
            appsecret=app_secret,
        ),
        is_virtual=is_virtual,
    ).execute()
    token = tok.access_token
    print(f"[1] access_token: {token[:24]}... (expires_in={tok.expires_in})")

    # 2. Quote lookup — Samsung Electronics 005930 (KRX).
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": app_key,
        "appsecret": app_secret,
    }
    print("\n[2] Quote: Samsung Electronics (005930, KRX)")
    price_resp = await InquirePriceExecutor(
        request=InquirePriceRequest(
            FID_COND_MRKT_DIV_CODE="J",  # KRX
            FID_INPUT_ISCD="005930",
        ),
        headers=headers,
        is_virtual=is_virtual,
    ).execute()
    print(f"  rt_cd={price_resp.rt_cd} msg={price_resp.msg1}")
    output = getattr(price_resp, "output", None)
    if output:
        items = output if isinstance(output, list) else [output]
        sample = items[0] if items else None
        if sample is not None:
            data = sample.model_dump() if hasattr(sample, "model_dump") else sample
            for k in ("stck_prpr", "prdy_vrss", "prdy_ctrt", "acml_vol", "stck_oprc", "stck_hgpr", "stck_lwpr"):
                if k in data:
                    print(f"    {k:14s} = {data[k]}")

    # 3. Balance lookup (demo).
    cano = env.get("KIS_CANO")
    acnt_prdt_cd = env.get("KIS_ACNT_PRDT_CD", "01")
    if not cano:
        print("\n[3] Balance: skipped (KIS_CANO not set)")
        return
    print(f"\n[3] Balance ({cano}-{acnt_prdt_cd})")
    bal_resp = await InquireBalanceExecutor(
        request=InquireBalanceRequest(
            CANO=cano,
            ACNT_PRDT_CD=acnt_prdt_cd,
            AFHR_FLPR_YN="N",
            OFL_YN="",
            INQR_DVSN="01",
            UNPR_DVSN="01",
            FUND_STTL_ICLD_YN="N",
            FNCG_AMT_AUTO_RDPT_YN="N",
            PRCS_DVSN="00",
            CTX_AREA_FK100="",
            CTX_AREA_NK100="",
        ),
        headers=headers,
        is_virtual=is_virtual,
    ).execute()
    print(f"  rt_cd={bal_resp.rt_cd} msg={bal_resp.msg1}")

    print(f"  output1 (holdings, {len(bal_resp.output1)} rows):")
    for h in bal_resp.output1[:5]:
        print(f"    {h.pdno} {h.prdt_name:20s} qty={h.hldg_qty} avg={h.pchs_avg_pric} cur={h.prpr} pnl={h.evlu_pfls_amt}")
    if len(bal_resp.output1) > 5:
        print(f"    ... and {len(bal_resp.output1)-5} more")

    if bal_resp.output2:
        s = bal_resp.output2[0]
        print("  output2 (account summary):")
        for k in ("dnca_tot_amt", "tot_evlu_amt", "nass_amt", "pchs_amt_smtl_amt", "evlu_amt_smtl_amt", "evlu_pfls_smtl_amt"):
            v = getattr(s, k, None)
            print(f"    {k:24s} = {v}")


if __name__ == "__main__":
    asyncio.run(main())
