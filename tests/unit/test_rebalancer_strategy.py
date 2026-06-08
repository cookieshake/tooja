from tooja.core.enums import RebalanceDirection


def test_rebalance_direction_values():
    assert RebalanceDirection.BOTH.value == "both"
    assert RebalanceDirection.BUY_ONLY.value == "buy_only"
    assert RebalanceDirection.SELL_ONLY.value == "sell_only"
