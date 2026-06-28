"""Config models + env/TOML loading for the MCP server."""

from __future__ import annotations

import re
import tomllib
from collections.abc import Mapping
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, model_validator

from tooja.core.errors import ConfigError

_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def interpolate_env(value: str, environ: Mapping[str, str]) -> str:
    def repl(m: re.Match[str]) -> str:
        name = m.group(1)
        if name not in environ:
            raise ConfigError(f"env var not set for ${{{name}}}", broker="mcp")
        return environ[name]

    return _ENV_RE.sub(repl, value)


class _AccountCommon(BaseModel):
    trading: bool = False


class KisAccountConfig(_AccountCommon):
    broker: Literal["kis"]
    env: Literal["real", "demo"] = "real"
    app_key: str
    app_secret: str
    cano: str
    hts_id: str
    acnt_prdt_cd: str = "01"


class TossAccountConfig(_AccountCommon):
    broker: Literal["toss"]
    client_id: str
    client_secret: str
    account_seq: int | None = None


AccountConfig = Annotated[
    KisAccountConfig | TossAccountConfig,
    Field(discriminator="broker"),
]


class McpConfig(BaseModel):
    accounts: dict[str, AccountConfig]

    @model_validator(mode="after")
    def _non_empty(self) -> McpConfig:
        if not self.accounts:
            raise ConfigError("no accounts configured", broker="mcp")
        return self


def _interpolate_tree(obj: Any, environ: Mapping[str, str]) -> Any:
    if isinstance(obj, str):
        return interpolate_env(obj, environ)
    if isinstance(obj, dict):
        return {k: _interpolate_tree(v, environ) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_interpolate_tree(v, environ) for v in obj]
    return obj


def load_toml(path: str, environ: Mapping[str, str]) -> McpConfig:
    with open(path, "rb") as f:
        data = tomllib.load(f)
    data = _interpolate_tree(data, environ)
    return McpConfig.model_validate(data)


_TRUE = {"1", "true", "yes", "on"}
_BOOL_FIELDS = {"trading"}
# fields that are not credential strings — parsed specially
_KNOWN_FIELDS = {
    "broker", "env", "app_key", "app_secret", "cano", "hts_id", "acnt_prdt_cd",
    "client_id", "client_secret", "account_seq", "trading",
}


def _account_from_flat(items: Mapping[str, str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for field, raw in items.items():
        if field not in _KNOWN_FIELDS:
            continue
        if field in _BOOL_FIELDS:
            out[field] = raw.strip().lower() in _TRUE
        else:
            out[field] = raw
    return out


def load_from_env(environ: Mapping[str, str]) -> McpConfig:
    names_raw = environ.get("TOOJA_MCP_ACCOUNTS")
    accounts: dict[str, Any] = {}
    if names_raw:
        for name in (n.strip() for n in names_raw.split(",") if n.strip()):
            prefix = f"TOOJA_MCP_{name.upper()}_"
            items = {
                k[len(prefix):].lower(): v
                for k, v in environ.items()
                if k.startswith(prefix)
            }
            accounts[name] = _account_from_flat(items)
    else:
        prefix = "TOOJA_MCP_"
        skip = {"TOOJA_MCP_ACCOUNTS", "TOOJA_MCP_CONFIG"}
        items = {
            k[len(prefix):].lower(): v
            for k, v in environ.items()
            if k.startswith(prefix) and k not in skip
        }
        if items:
            accounts["default"] = _account_from_flat(items)
    return McpConfig.model_validate({"accounts": accounts})


def load_config(environ: Mapping[str, str]) -> McpConfig:
    path = environ.get("TOOJA_MCP_CONFIG")
    if path:
        return load_toml(path, environ)
    return load_from_env(environ)
