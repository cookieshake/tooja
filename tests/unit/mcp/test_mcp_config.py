from decimal import Decimal

import pytest

from tooja.core.errors import ConfigError
from tooja.mcp.config import (
    KisAccountConfig,
    McpConfig,
    TossAccountConfig,
    interpolate_env,
    load_config,
    load_from_env,
    load_toml,
)


def test_interpolate_env_substitutes_and_errors():
    assert interpolate_env("${A}-x", {"A": "k"}) == "k-x"
    with pytest.raises(ConfigError):
        interpolate_env("${MISSING}", {})


def test_account_union_discriminates_on_broker():
    cfg = McpConfig.model_validate(
        {"accounts": {"m": {"broker": "kis", "app_key": "k", "app_secret": "s",
                            "cano": "1", "hts_id": "h", "trading": True}}}
    )
    acc = cfg.accounts["m"]
    assert isinstance(acc, KisAccountConfig)
    assert acc.trading is True and acc.env == "real"


def test_empty_accounts_rejected():
    with pytest.raises(ValueError):
        McpConfig.model_validate({"accounts": {}})


def test_load_toml_with_env_interpolation(tmp_path):
    p = tmp_path / "mcp.toml"
    p.write_text(
        '[accounts.main]\n'
        'broker = "kis"\n'
        'env = "demo"\n'
        'app_key = "${K_KEY}"\n'
        'app_secret = "s"\n'
        'cano = "12345678"\n'
        'hts_id = "id"\n'
        'trading = true\n'
        'max_order_value = 1000000\n'
        '[accounts.toss1]\n'
        'broker = "toss"\n'
        'client_id = "c"\n'
        'client_secret = "x"\n'
    )
    cfg = load_toml(str(p), {"K_KEY": "real-key"})
    assert cfg.accounts["main"].app_key == "real-key"
    assert cfg.accounts["main"].max_order_value == Decimal("1000000")
    assert isinstance(cfg.accounts["toss1"], TossAccountConfig)


def test_load_from_env_single_flat():
    env = {
        "TOOJA_MCP_BROKER": "kis", "TOOJA_MCP_ENV": "demo",
        "TOOJA_MCP_APP_KEY": "k", "TOOJA_MCP_APP_SECRET": "s",
        "TOOJA_MCP_CANO": "12345678", "TOOJA_MCP_HTS_ID": "id",
        "TOOJA_MCP_TRADING": "1", "TOOJA_MCP_MAX_ORDER_VALUE": "500000",
    }
    cfg = load_from_env(env)
    acc = cfg.accounts["default"]
    assert acc.broker == "kis" and acc.trading is True
    assert str(acc.max_order_value) == "500000"


def test_load_from_env_multi_prefixed():
    env = {
        "TOOJA_MCP_ACCOUNTS": "main,pension",
        "TOOJA_MCP_MAIN_BROKER": "kis", "TOOJA_MCP_MAIN_APP_KEY": "k",
        "TOOJA_MCP_MAIN_APP_SECRET": "s", "TOOJA_MCP_MAIN_CANO": "1",
        "TOOJA_MCP_MAIN_HTS_ID": "id", "TOOJA_MCP_MAIN_TRADING": "true",
        "TOOJA_MCP_PENSION_BROKER": "kis", "TOOJA_MCP_PENSION_APP_KEY": "k2",
        "TOOJA_MCP_PENSION_APP_SECRET": "s2", "TOOJA_MCP_PENSION_CANO": "2",
        "TOOJA_MCP_PENSION_HTS_ID": "id2",
    }
    cfg = load_from_env(env)
    assert set(cfg.accounts) == {"main", "pension"}
    assert cfg.accounts["main"].trading is True
    assert cfg.accounts["pension"].trading is False


def test_load_config_prefers_toml_when_path_set(tmp_path):
    p = tmp_path / "mcp.toml"
    p.write_text('[accounts.x]\nbroker = "toss"\nclient_id = "c"\nclient_secret = "s"\n')
    cfg = load_config({"TOOJA_MCP_CONFIG": str(p)})
    assert set(cfg.accounts) == {"x"}
