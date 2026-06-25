import importlib


def test_mcp_package_imports_without_mcp_sdk():
    mod = importlib.import_module("tooja.mcp")
    assert mod is not None
