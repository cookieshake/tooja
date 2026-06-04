import pytest

from tooja.core.stream import (
    OrderUpdateStream,
    OrderbookStream,
    QuoteStream,
    TradeStream,
)


def test_streams_are_abc():
    import abc
    for cls in (QuoteStream, TradeStream, OrderbookStream, OrderUpdateStream):
        assert isinstance(cls, abc.ABCMeta)


def test_stream_cannot_instantiate_directly():
    """Instantiation requires every abstract method to be implemented."""
    with pytest.raises(TypeError):
        QuoteStream()  # abstract methods unimplemented
