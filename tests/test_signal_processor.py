from decimal import Decimal

import pytest

from app.tick_signal_processor import process_ticks_to_signals

EXPECTED_OUTPUT = {
    "ticker",
    "prev_price",
    "cur_price",
    "price_change",
    "price_change_pct",
    "signal",
    "timestamp",
}


@pytest.fixture
def sample_tick():
    return {
        "ticker": "AAPL",
        "prev_price": Decimal("100.00"),
        "cur_price": Decimal("102.00"),
        "timestamp": "2026-10-16T12:00:00Z",
    }


def test_expected_transformation(sample_tick):
    signals = process_ticks_to_signals([sample_tick])

    assert len(signals) == 1

    signal = signals[0]

    assert EXPECTED_OUTPUT.issubset(signal.keys())
    assert signal["ticker"] == "AAPL"
    assert signal["prev_price"] == Decimal("100.00")
    assert signal["cur_price"] == Decimal("102.00")
    assert signal["price_change"] == Decimal("2.00")
    assert signal["price_change_pct"] == Decimal("2.000")
    assert signal["signal"] == "momentum_up"
    assert signal["timestamp"] == sample_tick["timestamp"]


def test_multiple_ticks_produce_multiple_signals(sample_tick):
    ticks = [
        sample_tick,
        {
            "ticker": "MSFT",
            "prev_price": Decimal("200.00"),
            "cur_price": Decimal("196.00"),
            "timestamp": "2026-10-16T12:00:01Z",
        },
        {
            "ticker": "NVDA",
            "prev_price": Decimal("300.00"),
            "cur_price": Decimal("301.00"),
            "timestamp": "2026-10-16T12:00:02Z",
        },
    ]

    signals = process_ticks_to_signals(ticks)

    assert len(signals) == 3

    assert [signal["ticker"] for signal in signals] == [
        "AAPL",
        "MSFT",
        "NVDA",
    ]

    assert [signal["signal"] for signal in signals] == [
        "momentum_up",
        "momentum_down",
        "neutral",
    ]

    assert [signal["timestamp"] for signal in signals] == [
        tick["timestamp"] for tick in ticks
    ]


def test_empty_ticks_returns_empty_list():
    signals = process_ticks_to_signals([])

    assert signals == []


def test_original_ticks_are_not_modified(sample_tick):
    original_tick = sample_tick.copy()

    process_ticks_to_signals([sample_tick])

    assert sample_tick == original_tick
