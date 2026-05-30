"""Live integration tests against KIS demo (모의투자).

Hits the real KIS demo endpoint for EVERY apiportal-defined REST endpoint
(WS endpoints covered separately). Dangerous POST orders are dry-run only
(builds Request model + would-be call info, does not send).

Run:    uv run pytest -m kis_live -s
Report: written to .kis-spec/test_results.json

Skipped automatically (collected but skipped):
- dangerous POST endpoints (order/revise/cancel/buy/sell) — DRY_RUN classification

Throttled to ~2 req/s for demo rate-limit safety.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import time
import importlib
from pathlib import Path
from typing import Any

import httpx
import pytest

from tooja.brokers.kis.raw.base import (
    REAL_BASE_URL,
    VIRTUAL_BASE_URL,
    KisApiError,
    TokenExpiredError,
)
from tooja.brokers.kis.raw.oauth.tokenp import TokenpExecutor, TokenpRequest

ROOT = Path(__file__).resolve().parent.parent
SPEC_DIR = ROOT / ".kis-spec" / "api-list"
CATS_FILE = ROOT / ".kis-spec" / "categories.json"
REPORT_PATH = ROOT / ".kis-spec" / "test_results.json"
TOKEN_CACHE = ROOT / ".kis-spec" / "token.json"
APPROVAL_CACHE = ROOT / ".kis-spec" / "approval_key.json"

REQ_DELAY = 0.55  # ~1.8 req/s — demo limit margin
WS_WAIT_SECONDS = 4.0  # subscribe 후 메시지 기다리는 시간
TOKEN_HOLDER: dict[str, str] = {}


def _is_virtual() -> bool:
    return os.environ.get("KIS_ENV", "demo").lower() != "real"


def _http_base() -> str:
    return VIRTUAL_BASE_URL if _is_virtual() else REAL_BASE_URL


def _ws_base() -> str:
    # 실전 WS: ws://ops.koreainvestment.com:21000, 모의: :31000
    return "ws://ops.koreainvestment.com:31000" if _is_virtual() else "ws://ops.koreainvestment.com:21000"

DANGEROUS_PATH_RE = re.compile(
    # / 또는 - 뒤에 위험 토큰 — daytime-order, daytime-order-rvsecncl도 포함
    r"[/-](order|revise|cancel|buy|sell|revoke|rvsecncl|order-cash|order-credit|order-resv)\b",
    re.IGNORECASE,
)


def is_dangerous(ep: dict[str, Any]) -> bool:
    method = (ep.get("httpMethod") or "GET").upper()
    if method != "POST":
        return False
    path = ep.get("accessUrl") or ""
    # 토큰 발급/폐기는 OAuth flow에서 사용, 위험 아님
    if "/oauth2/" in path:
        return False
    # 매수가능/주문가능 ‘조회’는 안전 (inquire-psbl-*)
    if "/inquire-" in path:
        return False
    return bool(DANGEROUS_PATH_RE.search(path))


def is_ws_endpoint(category_slug: str, ep: dict[str, Any]) -> bool:
    if category_slug.endswith("_ws"):
        return True
    return (ep.get("accessUrl") or "").startswith("/tryitout/")


# ---------- reqExample robust parser ----------

def _fix_json(raw: str) -> str:
    s = raw.strip()
    s = re.sub(r"^\s*\"?input\"?\s*:\s*", "", s)
    if not s.startswith("{") and not s.startswith("["):
        s = "{" + s.rstrip(", \n\r\t") + "}"
    s = re.sub(r",(\s*[}\]])", r"\1", s)
    return s


_KV_LINE = re.compile(r'^\s*"?([A-Za-z_][A-Za-z0-9_]*)"?\s*[:=]\s*(.*?)\s*,?\s*$')


def _strip_value(v: str) -> str:
    v = v.strip()
    if v.endswith(","):
        v = v[:-1].rstrip()
    # 이중/잘못된 따옴표 — '"foo"' / '":"foo"' / '"":foo' 모두 처리
    while v.startswith(('"', "'")):
        v = v[1:]
    while v.endswith(('"', "'")):
        v = v[:-1]
    # ":"foo" 같은 누락된 선행 콜론
    if v.startswith(":"):
        v = v[1:].lstrip('"\'').rstrip('"\'')
    return v.strip()


def _parse_kv_lines(raw: str) -> dict[str, Any]:
    """줄별 KEY:VALUE / KEY=VALUE / "KEY":"VALUE" 형식 파서. JSON 실패 시 fallback."""
    out: dict[str, Any] = {}
    for line in raw.splitlines():
        line = line.strip()
        # 최상위 JSON 잡음만 한 글자씩 제거 (값 내부 brace는 보존)
        if line.startswith("{"):
            line = line[1:].lstrip()
        if line.endswith(","):
            line = line[:-1].rstrip()
        if line.endswith("}") and line.count("{") < line.count("}"):
            line = line[:-1].rstrip()
        if not line:
            continue
        m = _KV_LINE.match(line)
        if not m:
            continue
        k, v = m.group(1), _strip_value(m.group(2))
        out[k] = v
    return out


def parse_req_example(raw: str | None) -> dict[str, Any]:
    if not raw or not raw.strip():
        return {}
    for candidate in (raw, _fix_json(raw)):
        try:
            v = json.loads(candidate)
            if isinstance(v, dict):
                # JSON 파싱 성공 — 값에 잔여 따옴표/콤마가 섞여 있을 수 있어 정리
                return {k: (_strip_value(vv) if isinstance(vv, str) else vv) for k, vv in v.items()}
        except Exception:
            pass
    # JSON 실패 → 줄별 KV
    return _parse_kv_lines(raw)


_TEMPLATE_RE = re.compile(r"\{\{\s*([A-Z_][A-Z_0-9]*)\s*\}\}")


def _apply_templates(val: Any) -> Any:
    """{{HTS_ID}} 같은 템플릿을 환경값으로 치환."""
    if not isinstance(val, str) or "{{" not in val:
        return val
    def sub(m: re.Match[str]) -> str:
        key = m.group(1)
        if key == "HTS_ID":
            return os.environ.get("KIS_HTS_ID", "")
        if key == "CANO":
            return os.environ.get("KIS_CANO", "")
        if key == "ACNT_PRDT_CD":
            return os.environ.get("KIS_ACNT_PRDT_CD", "01")
        return os.environ.get(f"KIS_{key}", "")
    return _TEMPLATE_RE.sub(sub, val)


# ---------- placeholder substitution ----------

_PLACEHOLDER_PATTERNS = [
    re.compile(r"X{6,}"),
    re.compile(r"^[0-9A-Z]+X+[0-9A-Z]*$"),
]


def substitute(val: Any) -> Any:
    if not isinstance(val, str):
        return val
    # 일반 placeholder (XXXXXXXX 류) — CANO/계좌
    if any(p.search(val) for p in _PLACEHOLDER_PATTERNS):
        if "ACNT_PRDT" in val or len(val) == 2:
            return os.environ.get("KIS_ACNT_PRDT_CD", "01")
        return os.environ.get("KIS_CANO", "50190267")
    return val


def _today_yyyymmdd() -> str:
    import datetime
    return datetime.date.today().strftime("%Y%m%d")


def _days_ago_yyyymmdd(n: int) -> str:
    import datetime
    return (datetime.date.today() - datetime.timedelta(days=n)).strftime("%Y%m%d")


def _guess_value(cd: str, ep: dict[str, Any]) -> str | None:
    """필드명/endpoint context로 합리적 입력값 추정."""
    u = cd.upper()
    access = ep.get("accessUrl", "")
    is_overseas = "/overseas-" in access or "overseas" in (ep.get("apiCollectionName") or "").lower()
    is_bond = "/domestic-bond" in access or "채권" in (ep.get("name") or "")
    is_futureoption = "futureoption" in access or "선물" in (ep.get("name") or "")
    is_industry_index = "/inquire-index-" in access or "comp-interest" in access

    # 계좌
    if u == "CANO":
        return os.environ.get("KIS_CANO", "")
    if u in ("ACNT_PRDT_CD", "ACNT_PRDT_NO"):
        return os.environ.get("KIS_ACNT_PRDT_CD", "01")
    if u in ("HTS_USER_ID", "USER_ID", "HTS_ID"):
        return os.environ.get("KIS_HTS_ID", "user_id")
    if u == "PHONE_NUMBER":
        return ""
    if u == "PERSONALSECKEY":
        return ""

    # 종목/상품 코드
    if "ISCD" in u or u in ("PDNO", "INPUT_ISCD", "STOCK_CODE", "SHTN_PDNO"):
        if is_industry_index:
            return "0001"  # 코스피
        if is_overseas:
            return "AAPL"
        if is_bond:
            return "KR103502GE17"
        return "005930"

    # 거래소 코드 (소문자/접미사 변형 포함)
    if u == "EXCH_DIV_CLS_CODE":
        return "J"  # J:KRX (NX:NXT, UN:통합 — 기본은 KRX)
    if u == "MRKT_DIV_CLS_CODE":
        return "1"  # 1:코스피 4:코스닥
    # FID_COND_MRKT_DIV_CODE_<N> 멀티슬롯 — 모두 J:KRX 기본
    if re.fullmatch(r"FID_COND_MRKT_DIV_CODE_[0-9]+", u):
        return "J"
    if u in ("FID_COND_MRKT_DIV_CODE", "FID_COND_MRKT_CLS_CODE"):
        if is_industry_index:
            return "U"  # 업종
        if is_bond:
            return "B"  # 채권
        if is_overseas:
            return "N"  # 해외주식 시세
        if is_futureoption:
            return "F"  # 선물
        if "/elw/" in access:
            return "W"  # ELW
        return "J"  # 국내주식
    if u in ("EXCD",):
        return "NAS" if is_overseas else "KRX"
    if u in ("EXCG_ID_DVSN_CD",):
        return "KRX"
    if u in ("OVRS_EXCG_CD",):
        return "NASD"
    if u in ("MKET_ID_CD",):
        return "STK"
    if u in ("TR_MKET_CLS_CODE",):
        return "J"

    # 날짜 (시작/종료/조회일)
    if u.endswith("_DT") or u.endswith("_DATE") or "DATE" in u or u.endswith("_YMD"):
        # 시작 → 30일 전, 끝 → 오늘
        if any(s in u for s in ("STRT", "FROM", "BEGIN", "FR_DT", "_1")):
            return _days_ago_yyyymmdd(30)
        return _today_yyyymmdd()
    if u.endswith("_HOUR") or "_HOUR_" in u:
        return "100000"

    # 분류/구분 — 흔한 디폴트
    if u in ("FID_PERIOD_DIV_CODE",):
        return "D"  # 일봉
    if u in ("FID_ORG_ADJ_PRC",):
        return "0"
    if u in ("FID_INPUT_ISCD_1",):
        return "0000"
    if u in ("FID_VOL_CNT",):
        return "0"
    if u in ("FID_INPUT_HOUR_1",):
        return "100000"
    if u in ("INQR_DVSN", "INQR_DVSN_1", "INQR_DVSN_3"):
        return "01"
    if u in ("UNPR_DVSN",):
        return "01"
    if u in ("AFHR_FLPR_YN", "OFL_YN", "FUND_STTL_ICLD_YN", "FNCG_AMT_AUTO_RDPT_YN",
             "INCL_YN", "CCLD_DVSN"):
        return "N"
    if u in ("SLL_BUY_DVSN", "SLL_BUY_DVSN_CD"):
        return "00"  # 전체
    if u in ("CCLD_NCCS_DVSN",):
        return "00"  # 체결 + 미체결 전부
    if u in ("SORT_SQN", "PRCS_DVSN_1"):
        return "00"
    if u == "ACNO":
        return (os.environ.get("KIS_CANO", "") + os.environ.get("KIS_ACNT_PRDT_CD", "01"))
    if u in ("ORD_GNO_BRNO", "ODNO"):
        return ""  # 주문번호는 없음
    if u in ("PRCS_DVSN",):
        return "00"
    if u in ("ORD_DVSN",):
        return "00"
    if u in ("CTX_AREA_FK100", "CTX_AREA_NK100", "CTX_AREA_FK200", "CTX_AREA_NK200"):
        return ""
    if u in ("CUSTTYPE",):
        return "P"

    # KIS 시세/순위/조건검색 공통 필드
    if u in ("FID_COND_SCR_DIV_CODE",):
        return "20171"  # 가장 흔한 화면구분코드 (endpoint별 다를 수 있음)
    if u in ("FID_MRKT_CLS_CODE", "FID_NEWS_OFER_ENTP_CODE", "FID_ETC_CLS_CODE",
             "FID_MKOP_CLS_CODE", "FID_PW_DATA_INCU_YN", "FID_TITL_CNTT", "FID_DIV_CLS_CODE"):
        return ""
    if u in ("CTS", "AUTH", "KEYB", "CTS_AREA", "CTS_KEY", "CTS_NK", "CTS_FK"):
        return ""
    if u in ("QRY_CNT", "NREC"):
        return "1"  # NREC: 해외 multprice 1건만
    if u in ("SORT_DVSN", "SORT_SQN", "FID_RANK_SORT_CLS_CODE", "GUBN", "GB1"):
        return "0"
    if u in ("GUBN2",):
        return "0"
    if u in ("NDAY",):
        return "1"
    # 해외 multprice EXCD_01..10, SYMB_01..10 (NREC=1이므로 01만 채우면 OK)
    if u.startswith("EXCD_"):
        return "NAS" if u.endswith("_01") else ""
    if u.startswith("SYMB_"):
        return "AAPL" if u.endswith("_01") else ""
    # 업종코드 (해외 industry-theme)
    if u == "ICOD":
        return "010"  # 운수창고 (대표 업종)
    if u in ("INFO_GB", "CLASS_CD", "NATION_CD", "EXCHANGE_CD", "DATA_DT", "DATA_TM", "SYMB"):
        return ""  # 해외 news-title 등 — 빈값 허용
    if u in ("QRY_TP", "QRY_GAP"):
        return "0"
    if u in ("VOL_RANG",):
        return "0"
    if u in ("KEYB",):
        return ""
    if u in ("FID_INPUT_PRICE_1", "FID_INPUT_PRICE_2", "PRC1", "PRC2"):
        return "0"
    if u in ("FID_FAKE_TICK_INCU_YN",):
        return "N"
    if u in ("MARKET_GB", "HIGH_GB"):
        return "0"
    if u in ("EXCH_DIV_CLS_CODE",):
        return "1"
    if u in ("CBLC_DVSN",):
        return "00"
    if u in ("FID_RANK_SORT_CLS_CODE_2",):
        return "0"
    if u in ("FID_COND_MRKT_DIV_CODE1", "FID_COND_MRKT_DIV_CODE_1"):
        return "J"
    if u in ("FID_INPUT_OPTION_1", "FID_INPUT_OPTION_2"):
        return "0"
    if u in ("INDEX_KEY",):
        return ""
    if u in ("FID_RANK_SORT_CLS_CODE_3",):
        return "0"
    if u in ("FID_INPUT_VOL_1", "FID_INPUT_VOL_2"):
        return "0"
    if u in ("FID_APLY_RANG_PRC_1", "FID_APLY_RANG_PRC_2"):
        return "0"
    if u in ("FID_PRC_CLS_CODE",):
        return "0"
    if u in ("INQR_DVSN_1", "INQR_DVSN_3"):
        return "1"  # 1자리 사이즈 케이스
    if u in ("CALL_PUT_CD",):
        return "C"
    if u in ("FID_INPUT_CNT_1", "FID_INPUT_CNT_2"):
        return "30"
    if u in ("FID_INPUT_SRNO",):
        return "0"
    if u in ("FID_BLNG_CLS_CODE", "FID_TRGT_EXLS_CLS_CODE", "FID_SCTN_CLS_CODE",
             "FID_TRGT_CLS_CODE"):
        return "0"
    if u in ("MINX",):
        return "0"
    if u in ("PDPR_TYPE_CD", "PRDT_TYPE_CD"):
        return "300"  # 일반주식
    if u in ("SRS_CD", "SHT_CD"):
        return "AAPL" if is_overseas else "005930"
    if u in ("SYMB",):
        return "AAPL"
    if u in ("EXCH_CD",):
        return "NAS"
    if u in ("TYPE",):
        return "0"
    if u in ("INQR_STRT_TIME", "INQR_END_TIME", "STRT_TIME", "CHEC_STRT_HOUR"):
        return "100000"
    if u in ("FID_HOUR_CLS_CODE",):
        return "100000"  # 6자리 시간

    return None


# URL별 reqExample/apiPropertys 결함 보정 (KIS apiportal spec과 실제 서버 불일치).
# 실서버 실험으로 정답값 검증된 케이스만 등록.
_PER_URL_OVERRIDES: dict[str, dict[str, str]] = {
    # spec이 FID_COND_MRKT_DIV_CODE만 정의, 실서버는 _1 suffix도 함께 요구
    "/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume": {
        "FID_COND_MRKT_DIV_CODE_1": "J",
        "FID_INPUT_ISCD_1": "005930",
    },
    # spec reqExample은 빈 값, 실서버는 실제 날짜/시간 요구
    "/uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice": {
        "FID_INPUT_DATE_1": "__TODAY__",
        "FID_INPUT_HOUR_1": "153000",
    },
    # apiPropertys에 안 나오는 hidden 필수 필드
    "/uapi/overseas-stock/v1/ranking/market-cap": {
        "CURR_GB": "",
    },
    # spec reqExample이 _3='U' 박았으나 실서버 거부 — J(KRX)로 강제
    "/uapi/domestic-stock/v1/quotations/intstock-multprice": {
        "FID_COND_MRKT_DIV_CODE_3": "J",
    },
    # spec reqExample은 ISCD_1만, 실서버는 ISCD_2도 요구
    "/uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market": {
        "FID_INPUT_ISCD_2": "KSP",
    },
    # spec reqExample은 FUOP_DVSN (오타), apiPropertys는 FUOP_DVSN_CD가 정답
    "/uapi/overseas-futureoption/v1/trading/inquire-daily-ccld": {
        "FUOP_DVSN_CD": "00",
    },
}


def build_request(ep: dict[str, Any]) -> dict[str, Any]:
    """reqExample → Request body dict (with placeholders substituted + spec-driven填充)."""
    raw = parse_req_example(ep.get("reqExample"))

    req_b = [p for p in (ep.get("apiPropertys") or []) if p.get("bodyType") == "req_b"]
    cd_set = {p["propertyCd"] for p in req_b}
    cd_upper_map = {p["propertyCd"].upper(): p["propertyCd"] for p in req_b}

    normalized: dict[str, Any] = {}
    for k, v in raw.items():
        v = _apply_templates(substitute(v))
        if k in cd_set:
            normalized[k] = v
            continue
        canonical = cd_upper_map.get(k.upper())
        if canonical:
            normalized[canonical] = v
            continue
        normalized[k] = v

    # 계좌 필드는 reqExample이 다른 사람 모의계좌를 포함할 수 있으므로 무조건 env로 덮어쓰기
    for cd in cd_set:
        u = cd.upper()
        if u == "CANO":
            normalized[cd] = os.environ.get("KIS_CANO", "")
        elif u in ("ACNT_PRDT_CD", "ACNT_PRDT_NO"):
            normalized[cd] = os.environ.get("KIS_ACNT_PRDT_CD", "01")
        elif u == "ACNO":
            normalized[cd] = (os.environ.get("KIS_CANO", "") + os.environ.get("KIS_ACNT_PRDT_CD", "01"))
        elif u in ("HTS_USER_ID", "USER_ID", "HTS_ID") and os.environ.get("KIS_HTS_ID"):
            normalized[cd] = os.environ["KIS_HTS_ID"]

    # spec req_b 중 reqExample에 *전혀* 없는 필드만 휴리스틱 → description ex → "" 순 채움.
    # (빈 값 ""은 KIS가 종종 의도하는 값이므로 덮어쓰지 않음)
    for p in req_b:
        cd = p["propertyCd"]
        if cd in normalized:
            continue
        guess = _guess_value(cd, ep)
        if guess is None:
            guess = _ex_from_description(p.get("description") or "")
        if guess is not None:
            normalized[cd] = guess

    # URL별 결함 보정 — 실서버 실험으로 검증된 정답값으로 덮어쓰기
    override = _PER_URL_OVERRIDES.get(ep.get("apiAccessUrl") or ep.get("accessUrl") or "")
    if override:
        for k, v in override.items():
            normalized[k] = _today_yyyymmdd() if v == "__TODAY__" else v

    return normalized


_EX_RE = re.compile(r"(?:^|[(\s])ex[.\):\s]+\s*([A-Za-z0-9_\-]+)", re.IGNORECASE)


def _ex_from_description(desc: str) -> str | None:
    """spec description의 "ex.) 20171" / "(ex 005930)" 등에서 첫 예시값 추출."""
    if not desc:
        return None
    m = _EX_RE.search(desc)
    if not m:
        return None
    v = m.group(1).strip()
    # 공통 잡음 제거
    if v.lower() in ("string", "number", "null", "n", "y"):
        return None
    return v


# ---------- live call ----------

def _load_cached(path: Path, ttl_seconds: int) -> str | None:
    if not path.exists():
        return None
    try:
        d = json.loads(path.read_text())
        if time.time() - d["fetched_at"] < ttl_seconds:
            return d["value"]
    except Exception:
        pass
    return None


def _save_cached(path: Path, value: str) -> None:
    path.write_text(json.dumps({"value": value, "fetched_at": time.time()}))


async def get_token() -> str:
    if "token" in TOKEN_HOLDER:
        return TOKEN_HOLDER["token"]
    # 24h 이내 캐시된 토큰 재사용 — KIS는 6h 이내 재요청 시 같은 값 줌, 잦은 발급은 403
    cached = _load_cached(TOKEN_CACHE, 23 * 3600)
    if cached:
        TOKEN_HOLDER["token"] = cached
        return cached
    app_key = os.environ["KIS_APP_KEY"]
    app_secret = os.environ["KIS_APP_SECRET"]
    tok = await TokenpExecutor(
        request=TokenpRequest(
            grant_type="client_credentials",
            appkey=app_key,
            appsecret=app_secret,
        ),
        is_virtual=_is_virtual(),
    ).execute()
    TOKEN_HOLDER["token"] = tok.access_token
    _save_cached(TOKEN_CACHE, tok.access_token)
    return tok.access_token


async def get_approval_key() -> str:
    if "approval" in TOKEN_HOLDER:
        return TOKEN_HOLDER["approval"]
    cached = _load_cached(APPROVAL_CACHE, 23 * 3600)
    if cached:
        TOKEN_HOLDER["approval"] = cached
        return cached
    # /oauth2/Approval — WebSocket용 접속키 발급
    app_key = os.environ["KIS_APP_KEY"]
    app_secret = os.environ["KIS_APP_SECRET"]
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{_http_base()}/oauth2/Approval",
            json={"grant_type": "client_credentials", "appkey": app_key, "secretkey": app_secret},
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=20,
        )
    r.raise_for_status()
    key = r.json()["approval_key"]
    TOKEN_HOLDER["approval"] = key
    _save_cached(APPROVAL_CACHE, key)
    return key


def headers_for(token: str) -> dict[str, str]:
    return {
        "authorization": f"Bearer {token}",
        "appkey": os.environ["KIS_APP_KEY"],
        "appsecret": os.environ["KIS_APP_SECRET"],
        "custtype": "P",
    }


async def call_raw(ep: dict[str, Any], body: dict[str, Any], token: str,
                   shared_client: httpx.AsyncClient) -> dict[str, Any]:
    """spec 기반 직접 호출 — Executor 클래스 거치지 않고 raw HTTP (스키마 검증 별도).

    Returns dict: {"status": http_status, "body": parsed_json_or_text, "tr_id": ...}
    """
    method = (ep.get("httpMethod") or "GET").upper()
    url = f"{_http_base()}{ep['accessUrl']}"
    # 실전이면 realTrId, 모의면 virtualTrId 우선
    if _is_virtual():
        tr_id_raw = ep.get("virtualTrId") or ep.get("realTrId") or ""
    else:
        tr_id_raw = ep.get("realTrId") or ""
    tr_id = tr_id_raw.split(",")[0].strip().split("(")[0].strip()
    # KIS TR_ID는 항상 6자 이상 (예: TTTC0081R, FHKST01010100). 한글 섞인 자유 형식인 경우 첫 6자+ 토큰 추출.
    if not re.fullmatch(r"[A-Z0-9]{6,}", tr_id or ""):
        m = re.search(r"[A-Z0-9]{6,}", tr_id_raw)
        tr_id = m.group(0) if m else ""

    h = headers_for(token)
    if tr_id:
        h["tr_id"] = tr_id
    h["Content-Type"] = "application/json; charset=utf-8"

    try:
        if method == "POST":
            r = await shared_client.post(url, headers=h, json=body, timeout=20)
        else:
            r = await shared_client.get(url, headers=h, params=body, timeout=20)
        ct = r.headers.get("content-type", "")
        body_out: Any
        if "json" in ct.lower():
            try:
                body_out = r.json()
            except Exception:
                # KIS가 broken JSON 보내는 경우 (예: 키 따옴표 누락) — 휴리스틱 복구
                text = r.text
                fixed = re.sub(r'([,{]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', text)
                try:
                    body_out = json.loads(fixed)
                except Exception:
                    body_out = text[:500]
        else:
            body_out = r.text[:500]
    except httpx.HTTPError as e:
        return {"status": -1, "body": f"HTTPError: {e}", "tr_id": tr_id, "url": url}
    return {"status": r.status_code, "body": body_out, "tr_id": tr_id, "url": url}


def classify(result: dict[str, Any]) -> str:
    if result["status"] == -1:
        return "NETWORK_ERROR"
    body = result["body"]
    if isinstance(body, dict):
        rt_cd = body.get("rt_cd")
        # KIS gateway가 msg_cd/msg1 의미를 반대로 채우는 케이스 多 → 둘 다 검사
        text = f"{body.get('msg_cd','')} {body.get('msg1','')}"
        if rt_cd == "0":
            return "OK"
        # rate limit / 일시 지연 (재시도 가능)
        if "EGW00201" in text or "초당 거래" in text:
            return "RATE_LIMITED"
        if "90020000" in text or "서비스가 지연" in text:
            return "RATE_LIMITED"
        # 게이트웨이가 모의에서 라우팅 못 함 = 사실상 미지원
        if "EGW00203" in text or "OPS라우팅" in text:
            return "DEMO_UNSUPPORTED"
        if "EGW00310" in text or "TR-ID가 유효하지 않" in text:
            return "DEMO_UNSUPPORTED"
        if "EGW02006" in text or "모의투자 TR 이 아닙" in text:
            return "DEMO_UNSUPPORTED"
        if "모의투자 미지원" in text:
            return "DEMO_UNSUPPORTED"
        # paging 안내 (KIS는 다음 페이지 있을 때 MCA05762로 알림) — 본 페이지 데이터는 정상
        if "MCA05762" in text or "조회가 계속 됩니다" in text:
            return "OK"
        # 조회 결과 없음 — 호출은 성공, 데이터만 없음
        if "KIOK0560" in text or "조회할 내용이 없" in text:
            return "OK"
        if "APBK1631" in text or "데이터 찾을수없" in text or "조회된 데이터가 없" in text:
            return "OK"
        # 선물옵션 계좌 미신청 (1건의 레코드 검증 실패 = 계좌 데이터 0건)
        if "SKFT2101" in text or "정확히 1건의 레코드" in text:
            return "ACCOUNT_NOT_REGISTERED"
        # KIS 계좌에 해당 시장(선물옵션/야간/해외선물 등) 미신청
        if any(k in text for k in ("APAC0134", "APAC0071", "EGW00550")) or "해당하는 계좌번호가 존재하지 않" in text or "계좌번호가 존재하지" in text or "거래소 신청 계좌가 아닙니다" in text:
            return "ACCOUNT_NOT_REGISTERED"
        # 계좌 타입 미스매치 (신용/위탁 전용 endpoint)
        if "APBK1617" in text or "APAC0489" in text or "신용계좌만" in text or "위탁계좌인 경우만" in text:
            return "ACCOUNT_TYPE_MISMATCH"
        # 진짜 인증/토큰 관련 (EGW001*만)
        if "EGW001" in text:
            return "AUTH_ERROR"
        # 모의투자 / 미지원 명시
        if ("모의" in text and ("미지원" in text or "지원하지" in text)) or "미지원" in text:
            return "DEMO_UNSUPPORTED"
        # 입력 필드 결함 (우리 입력 빌드 문제)
        if "OPSQ" in text or "INPUT FIELD NOT FOUND" in text or "필수입력값" in text:
            return "INPUT_MISSING"
        if rt_cd == "1":
            return "API_ERROR"
        if "msg1" in body or "msg_cd" in body:
            return "API_ERROR"
    if result["status"] >= 500:
        return "SERVER_ERROR"
    if result["status"] >= 400:
        return "CLIENT_ERROR"
    return "UNKNOWN"


# ---------- pytest fixtures + collection ----------

def _collect_endpoints() -> list[tuple[str, dict[str, Any]]]:
    cats = json.loads(CATS_FILE.read_text())
    out: list[tuple[str, dict[str, Any]]] = []
    for cat in cats:
        slug = cat["slug"]
        path = SPEC_DIR / f"{slug}.json"
        if not path.exists():
            continue
        for ep in json.loads(path.read_text()):
            out.append((slug, ep))
    return out


ALL_EPS = _collect_endpoints()
REST_EPS = [(s, e) for s, e in ALL_EPS if not is_ws_endpoint(s, e)]
WS_EPS = [(s, e) for s, e in ALL_EPS if is_ws_endpoint(s, e)]


RESULTS: list[dict[str, Any]] = []


def _ep_id(item: tuple[str, dict[str, Any]]) -> str:
    s, e = item
    return f"{s}::{e.get('accessUrl','?')}"


@pytest.mark.kis_live
@pytest.mark.parametrize("item", REST_EPS, ids=_ep_id)
async def test_rest_endpoint(item):
    slug, ep = item
    if "KIS_APP_KEY" not in os.environ:
        pytest.skip("KIS_APP_KEY not set")
    token = await get_token()  # cached after first call
    record: dict[str, Any] = {
        "slug": slug, "name": ep.get("name"), "url": ep.get("accessUrl"),
        "method": (ep.get("httpMethod") or "").upper(),
        "tr_id": ep.get("virtualTrId") or ep.get("realTrId"),
    }
    if is_dangerous(ep):
        record["category"] = "DRY_RUN"
        record["note"] = "POST order — not sent"
        RESULTS.append(record)
        _save_results()
        return

    # spec이 직접 "모의투자 미지원" 표기한 endpoint는 모의에서만 호출 전 skip (실전에서는 호출)
    raw_v = (ep.get("virtualTrId") or "")
    if _is_virtual() and ("미지원" in raw_v or "지원하지" in raw_v):
        record["category"] = "DEMO_UNSUPPORTED"
        record["note"] = f"spec virtualTrId: {raw_v}"
        RESULTS.append(record); _save_results(); return

    # OAuth 카테고리는 본 테스트 라운드에서 skip — 토큰은 setup에서 처리됨, 재호출 시 403
    if slug == "oauth":
        record["category"] = "SKIPPED_OAUTH"
        record["note"] = "token already cached; OAuth endpoints excluded from API sweep"
        RESULTS.append(record); _save_results(); return

    body = build_request(ep)
    record["request_keys"] = sorted(body.keys())

    await asyncio.sleep(REQ_DELAY)
    async with httpx.AsyncClient() as http_client:
        result = await call_raw(ep, body, token, http_client)
        record["category"] = classify(result)
        # RATE_LIMITED는 1회 재시도 (1.5초 대기)
        if record["category"] == "RATE_LIMITED":
            await asyncio.sleep(1.5)
            result = await call_raw(ep, body, token, http_client)
            record["category"] = classify(result)
            record["retried"] = True
    record["status"] = result["status"]
    if record["category"] != "OK":
        b = result["body"]
        if isinstance(b, dict):
            record["msg_cd"] = b.get("msg_cd")
            record["msg1"] = (b.get("msg1") or "")[:160]
        else:
            record["error"] = str(b)[:200]
    RESULTS.append(record)
    _save_results()


def _ws_tr_key(ep: dict[str, Any]) -> str:
    """endpoint별 합리적인 tr_key 추정. 대부분 종목코드 또는 HTS_ID."""
    name = ep.get("name", "")
    access = ep.get("accessUrl", "")
    tr_id = (ep.get("realTrId") or "")
    # 해외주식: DNASAAPL (거래소 4자리 + 티커)
    if "해외주식" in name or "/overseas-stock" in access or "overseas_stock" in (ep.get("apiCollectionName") or ""):
        return "DNASAAPL"
    # 국내선물옵션: 코스피200 선물
    if "선물옵션" in name or tr_id.startswith("H0I") or tr_id.startswith("H0Z") or tr_id.startswith("H0M") or tr_id.startswith("H0C"):
        return "101W12"
    # 채권: 임의 ISIN 또는 종목 — KIS 모의는 미지원이 대부분
    if "채권" in name or "/bond" in access:
        return "KR103502GE17"
    # 통보(체결/주문): HTS ID 필요 — placeholder
    if "통보" in name or "체결통보" in name or tr_id.endswith("0CNI0") or tr_id.endswith("0CNI9"):
        return os.environ.get("KIS_HTS_ID", "user_id")
    # 기본: 삼성전자
    return "005930"


@pytest.mark.kis_live
@pytest.mark.parametrize("item", WS_EPS, ids=_ep_id)
async def test_ws_endpoint(item):
    import websockets
    slug, ep = item
    if "KIS_APP_KEY" not in os.environ:
        pytest.skip("KIS_APP_KEY not set")

    tr_id = (ep.get("realTrId") or "").split(",")[0].strip()
    m = re.search(r"[A-Z0-9]+", tr_id)
    tr_id = m.group(0) if m else ""
    tr_key = _ws_tr_key(ep)

    record: dict[str, Any] = {
        "slug": slug, "name": ep.get("name"), "url": ep.get("accessUrl"),
        "method": "WS", "tr_id": tr_id, "tr_key": tr_key,
    }

    # 체결통보 TR (HTS_ID 필요) — spec req_b에 HTS_USER_ID/USER_ID 있거나 name에 "통보" 포함 → skip
    name = ep.get("name") or ""
    needs_hts = ("통보" in name or "체결통보" in name or
                 any(p.get("propertyCd","").upper() in ("HTS_USER_ID","USER_ID","HTS_ID")
                     for p in (ep.get("apiPropertys") or [])))
    if needs_hts and not os.environ.get("KIS_HTS_ID"):
        record["category"] = "SKIPPED_HTS_ID"
        record["note"] = "set KIS_HTS_ID to test 체결통보 TRs"
        RESULTS.append(record); _save_results(); return

    try:
        try:
            approval = await get_approval_key()
        except Exception as e:
            record["category"] = "WS_AUTH_FAIL"
            record["error"] = f"{type(e).__name__}: {e}"[:200]
            return

        msg = json.dumps({
            "header": {"approval_key": approval, "custtype": "P", "tr_type": "1", "content-type": "utf-8"},
            "body": {"input": {"tr_id": tr_id, "tr_key": tr_key}},
        })

        try:
            async with websockets.connect(_ws_base(),
                                          open_timeout=10, close_timeout=2) as ws:
                await ws.send(msg)
                first = await asyncio.wait_for(ws.recv(), timeout=8)
                if isinstance(first, bytes):
                    first = first.decode("utf-8", errors="replace")
                record["first_frame_kind"] = "json" if first.startswith("{") else "data"

                if first.startswith("{"):
                    try:
                        ack = json.loads(first)
                    except Exception:
                        ack = {}
                    body = ack.get("body", {})
                    rt_cd = body.get("rt_cd")
                    msg1 = (body.get("msg1") or "")[:160]
                    msg_cd = body.get("msg_cd") or ""
                    text = f"{msg_cd} {msg1}"
                    record["msg_cd"] = msg_cd
                    record["msg1"] = msg1
                    if rt_cd == "0":
                        try:
                            data_frame = await asyncio.wait_for(ws.recv(), timeout=WS_WAIT_SECONDS)
                            if isinstance(data_frame, bytes):
                                data_frame = data_frame.decode("utf-8", errors="replace")
                            record["category"] = "WS_OK"
                            record["sample"] = str(data_frame)[:200]
                        except (asyncio.TimeoutError, TimeoutError):
                            record["category"] = "WS_SUBSCRIBED_NO_DATA"
                    elif "모의" in text or "미지원" in text or "지원하지" in text:
                        record["category"] = "WS_DEMO_UNSUPPORTED"
                    elif "권한" in text or "EGW001" in text or "EGW002" in text:
                        record["category"] = "WS_AUTH_ERROR"
                    elif "TR" in text and ("유효" in text or "ID" in text):
                        record["category"] = "WS_DEMO_UNSUPPORTED"
                    elif "OPSP0017" in text or "htsid가잘못" in text:
                        # KIS 모의가 해당 시장 체결통보를 거절 — 시장별 미신청 또는 모의 미지원
                        record["category"] = "WS_DEMO_UNSUPPORTED"
                    else:
                        record["category"] = "WS_API_ERROR"
                else:
                    record["category"] = "WS_OK"
                    record["sample"] = str(first)[:200]

                # unsubscribe (best-effort)
                try:
                    await ws.send(json.dumps({
                        "header": {"approval_key": approval, "custtype": "P", "tr_type": "2", "content-type": "utf-8"},
                        "body": {"input": {"tr_id": tr_id, "tr_key": tr_key}},
                    }))
                except Exception:
                    pass
        except (asyncio.TimeoutError, TimeoutError):
            record["category"] = "WS_TIMEOUT"
        except BaseException as e:
            record["category"] = "WS_CONNECT_FAIL"
            record["error"] = f"{type(e).__name__}: {e}"[:200]

        # KIS WS는 동일 approval_key로 너무 잦은 reconnect를 차단. 약간의 간격 둠
        await asyncio.sleep(0.6)
    finally:
        RESULTS.append(record)
        _save_results()


def _save_results() -> None:
    REPORT_PATH.write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2))


def pytest_sessionfinish(session, exitstatus):
    if not RESULTS:
        return
    from collections import Counter
    cnt = Counter(r["category"] for r in RESULTS)
    print("\n========== LIVE TEST SUMMARY ==========")
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"  {k:18s} {v}")
    print(f"  TOTAL              {sum(cnt.values())}")
    print(f"  Report: {REPORT_PATH}")
