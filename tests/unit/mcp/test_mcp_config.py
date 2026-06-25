from decimal import Decimal

import pytest

from tooja.core.errors import ConfigError
from tooja.mcp.config import (
    KisAccountConfig,
    McpConfig,
    TossAccountConfig,
    interpolate_env,
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
