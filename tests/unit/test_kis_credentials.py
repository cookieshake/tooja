from tooja.brokers.kis.credentials import KisCredentials


def test_credentials_construction():
    c = KisCredentials(
        app_key="K", app_secret="S", cano="12345678", acnt_prdt_cd="01", hts_id="H",
    )
    assert c.app_key == "K"
    assert c.cano == "12345678"


def test_credentials_frozen():
    import dataclasses
    c = KisCredentials(
        app_key="K", app_secret="S", cano="12345678", acnt_prdt_cd="01", hts_id="H",
    )
    import pytest
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.app_key = "X"  # type: ignore[misc]


def test_repr_masks_secrets():
    c = KisCredentials(
        app_key="PSrqwPYlqoq03M7QKLLq0I0qauk0U5F1AJSp",
        app_secret="VERY_LONG_REAL_SECRET_VALUE",
        cano="63749662",
        acnt_prdt_cd="01",
        hts_id="cookiesh",
    )
    r = repr(c)
    assert "VERY_LONG_REAL_SECRET_VALUE" not in r
    assert "PSrqwPYlqoq03M7QKLLq0I0qauk0U5F1AJSp" not in r
    # Last 4 of app_key OK as hint
    assert r.endswith("hts_id='cookiesh')")
    # Non-secret fields still visible
    assert "63749662" in r
    assert "cookiesh" in r


def test_repr_short_app_key_full_mask():
    c = KisCredentials(
        app_key="abc", app_secret="s", cano="C", acnt_prdt_cd="01", hts_id="H",
    )
    r = repr(c)
    # Keys shorter than 4 chars get fully masked.
    assert "abc" not in r
    assert "***" in r
