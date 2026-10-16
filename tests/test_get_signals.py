from decimal import Decimal

from app.get_signals import get_all_signals, get_signal_by_ticker
from app.raw_prices import RAW_PRICES

EXPECTED_SIGNAL_FIELDS = {
    "ticker",
    "prev_price",
    "cur_price",
    "price_change",
    "price_change_pct",
    "signal",
    "timestamp",
}


def test_get_all_signals_length_against_raw_prices():
    result = get_all_signals()

    assert len(result) == len(RAW_PRICES)


def test_get_all_signals_returns_expected_fields():
    result = get_all_signals()

    for signal in result:
        assert EXPECTED_SIGNAL_FIELDS.issubset(signal.keys())


def test_get_all_signals_contains_calculated_aapl_signal():
    result = get_all_signals()

    aapl_signal = next(signal for signal in result if signal["ticker"] == "AAPL")

    assert aapl_signal["prev_price"] == Decimal("365.50")
    assert aapl_signal["cur_price"] == Decimal("379.49")
    assert aapl_signal["price_change"] == Decimal("13.99")
    assert aapl_signal["price_change_pct"] == Decimal("3.828")
    assert aapl_signal["signal"] == "momentum_up"
    assert aapl_signal["timestamp"] == "2026-10-02T12:00:00Z"


def test_get_signal_by_ticker_returns_signal():
    result = get_signal_by_ticker("AAPL")

    assert result is not None
    assert result["ticker"] == "AAPL"
    assert EXPECTED_SIGNAL_FIELDS.issubset(result.keys())


def test_get_signal_by_ticker_handles_lowercase():
    result = get_signal_by_ticker("aapl")

    assert result is not None
    assert result["ticker"] == "AAPL"


def test_get_signal_by_ticker_unknown_returns_none():
    result = get_signal_by_ticker("UNKNOWN")

    assert result is None
