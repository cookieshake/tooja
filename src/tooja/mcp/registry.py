"""Named-account registry: builds brokers and resolves the target account per call."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from tooja.brokers.kis.broker import KisBroker
from tooja.brokers.toss.broker import TossBroker
from tooja.core.broker import Broker
from tooja.core.errors import ConfigError
from tooja.mcp.config import AccountConfig, KisAccountConfig, McpConfig, TossAccountConfig


@dataclass
class Account:
    name: str
    broker: Broker
    trading: bool


class Registry:
    def __init__(self, accounts: dict[str, Account]) -> None:
        self._accounts = accounts

    def resolve(self, name: str | None) -> Account:
        if name is None:
            if len(self._accounts) == 1:
                return next(iter(self._accounts.values()))
            raise ConfigError(
                f"account is required: choose one of {sorted(self._accounts)}",
                broker="mcp",
            )
        try:
            return self._accounts[name]
        except KeyError:
            raise ConfigError(
                f"unknown account {name!r}: choose one of {sorted(self._accounts)}",
                broker="mcp",
            ) from None

    @property
    def has_kis(self) -> bool:
        return any(a.broker.broker_name == "kis" for a in self._accounts.values())

    @property
    def has_trading(self) -> bool:
        return any(a.trading for a in self._accounts.values())

    def all(self) -> list[Account]:
        return list(self._accounts.values())

    async def aclose(self) -> None:
        errors: list[Exception] = []
        for acc in self._accounts.values():
            try:
                await acc.broker.close()
            except Exception as exc:  # noqa: BLE001 — every broker must be closed; re-raise after
                errors.append(exc)
        if errors:
            if len(errors) == 1:
                raise errors[0]
            raise ExceptionGroup("failed to close one or more brokers", errors)


def _default_factory(cfg: AccountConfig) -> Broker:
    if isinstance(cfg, KisAccountConfig):
        return KisBroker(
            app_key=cfg.app_key,
            app_secret=cfg.app_secret,
            cano=cfg.cano,
            hts_id=cfg.hts_id,
            acnt_prdt_cd=cfg.acnt_prdt_cd,
            env=cfg.env,
        )
    if isinstance(cfg, TossAccountConfig):
        return TossBroker(
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
            account_seq=cfg.account_seq,
        )
    raise ConfigError(f"unknown broker config: {type(cfg).__name__}", broker="mcp")


def build_registry(
    config: McpConfig,
    *,
    broker_factory: Callable[[AccountConfig], Broker] = _default_factory,
) -> Registry:
    accounts = {
        name: Account(
            name=name,
            broker=broker_factory(cfg),
            trading=cfg.trading,
        )
        for name, cfg in config.accounts.items()
    }
    return Registry(accounts)
