from app.get_signals import get_all_signals, get_signal_by_ticker


EXPECTED_SIGNAL_FIELDS = {
    "ticker",
    "prev_price",
    "cur_price",
    "price_change",
    "price_change_pct",
    "signal",
    "timestamp",
}


def test_get_all_signals_returns_expected_count():
    signals = get_all_signals()

    assert len(signals) == 3


def test_get_all_signals_returns_expected_fields():
    signals = get_all_signals()

    for signal in signals:
        assert EXPECTED_SIGNAL_FIELDS.issubset(signal.keys())


def test_get_all_signals_returns_expected_tickers():
    signals = get_all_signals()

    tickers = {signal["ticker"] for signal in signals}

    assert tickers == {"AAPL", "MSFT", "NVDA"}


def test_get_signal_by_ticker_returns_signal():
    signal = get_signal_by_ticker("AAPL")

    assert signal is not None
    assert signal["ticker"] == "AAPL"
    assert EXPECTED_SIGNAL_FIELDS.issubset(signal.keys())


def test_get_signal_by_ticker_handles_lowercase():
    signal = get_signal_by_ticker("aapl")

    assert signal is not None
    assert signal["ticker"] == "AAPL"


def test_get_signal_by_ticker_unknown_returns_none():
    signal = get_signal_by_ticker("UNKNOWN")

    assert signal is None
