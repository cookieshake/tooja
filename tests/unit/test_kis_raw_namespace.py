import pytest

from tooja.brokers.kis.raw_namespace import KisRawNamespace


class _StubBroker:
    pass


_EXPECTED_CATEGORIES = {
    "oauth",
    "domestic_bond_quotations", "domestic_bond_trading", "domestic_bond_ws",
    "domestic_futureoption_quotations", "domestic_futureoption_trading",
    "domestic_futureoption_ws",
    "domestic_stock_elw_quotations", "domestic_stock_industry",
    "domestic_stock_info", "domestic_stock_quotations",
    "domestic_stock_quote_analysis", "domestic_stock_rank_analysis",
    "domestic_stock_trading", "domestic_stock_ws",
    "overseas_futureoption_quotations", "overseas_futureoption_trading",
    "overseas_futureoption_ws",
    "overseas_stock_quotations", "overseas_stock_quote_analysis",
    "overseas_stock_trading", "overseas_stock_ws",
}


def test_raw_namespace_all_categories_resolve():
    """All 22 category attributes must be accessible."""
    ns = KisRawNamespace(_StubBroker())
    for name in _EXPECTED_CATEGORIES:
        assert hasattr(ns, name), f"missing category {name}"


def test_raw_namespace_does_not_eager_load():
    """_cache must be empty right after construction — category module import is deferred until first access."""
    ns = KisRawNamespace(_StubBroker())
    assert ns._cache == {}


def test_raw_namespace_caches_on_access():
    ns = KisRawNamespace(_StubBroker())
    cat1 = ns.domestic_stock_quotations
    assert "domestic_stock_quotations" in ns._cache
    cat2 = ns.domestic_stock_quotations
    assert cat1 is cat2  # Same instance reused.


def test_raw_namespace_only_caches_accessed_categories():
    """Touching one category does not cache the others."""
    ns = KisRawNamespace(_StubBroker())
    _ = ns.oauth
    assert set(ns._cache.keys()) == {"oauth"}


def test_raw_namespace_unknown_category_raises():
    ns = KisRawNamespace(_StubBroker())
    with pytest.raises(AttributeError, match="nonexistent_category"):
        ns.nonexistent_category


def test_category_delegates_module_attribute_access():
    """_Category exposes the underlying module's attributes (Executor / Request classes, ...)."""
    ns = KisRawNamespace(_StubBroker())
    cat = ns.oauth
    # The oauth category is a package containing endpoint modules like raw/oauth/tokenp.
    # If delegation works, the module's basic attributes (__name__, etc.) are reachable.
    assert cat.__name__.endswith(".oauth")  # type: ignore[attr-defined]


def test_category_unknown_attr_raises_attribute_error():
    ns = KisRawNamespace(_StubBroker())
    cat = ns.domestic_stock_quotations
    with pytest.raises(AttributeError):
        _ = cat.nonexistent_endpoint_xyz
