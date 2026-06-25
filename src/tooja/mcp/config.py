"""Config models + env/TOML loading for the MCP server."""

from __future__ import annotations

import re
import tomllib
from collections.abc import Mapping
from decimal import Decimal
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
    max_order_value: Decimal | None = None


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
            raise ValueError("no accounts configured")
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
