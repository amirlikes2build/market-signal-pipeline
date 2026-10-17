from decimal import Decimal

import pytest

from app.pipeline_runner import run_market_tick_pipeline
from app.signal_storage import load_signals_from_jsonl
from app.tick_storage import load_ticks_from_jsonl


@pytest.fixture
def starting_prices():
    return {
        "AAPL": Decimal("100.00"),
        "MSFT": Decimal("200.00"),
    }


@pytest.fixture
def pipeline_result(tmp_path, starting_prices):
    tick_path = tmp_path / "ticks.jsonl"
    signal_path = tmp_path / "signals.jsonl"

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=5,
        output_path_ticks=tick_path,
        output_path_signals=signal_path,
    )

    return {
        "summary": summary,
        "tick_path": tick_path,
        "signal_path": signal_path,
    }


def test_pipeline_creates_both_output_files(pipeline_result):
    assert pipeline_result["tick_path"].exists()
    assert pipeline_result["signal_path"].exists()


def test_pipeline_summary_has_correct_counts(pipeline_result, starting_prices):
    summary = pipeline_result["summary"]

    expected_count = len(starting_prices) * 5

    assert summary["tick_count"] == expected_count
    assert summary["signal_count"] == expected_count


def test_pipeline_summary_has_correct_tickers(pipeline_result):
    summary = pipeline_result["summary"]

    assert summary["tickers"] == ["AAPL", "MSFT"]


def test_pipeline_summary_has_correct_paths(pipeline_result):
    summary = pipeline_result["summary"]

    assert summary["ticks_output_path"] == str(pipeline_result["tick_path"])
    assert summary["signals_output_path"] == str(pipeline_result["signal_path"])


def test_saved_ticks_and_signals_match_summary(pipeline_result):
    summary = pipeline_result["summary"]

    ticks = load_ticks_from_jsonl(pipeline_result["tick_path"])
    signals = load_signals_from_jsonl(pipeline_result["signal_path"])

    assert len(ticks) == summary["tick_count"]
    assert len(signals) == summary["signal_count"]

    assert [signal["ticker"] for signal in signals] == [
        tick["ticker"] for tick in ticks
    ]

    assert [signal["timestamp"] for signal in signals] == [
        tick["timestamp"] for tick in ticks
    ]

    assert summary["first_timestamp"] == ticks[0]["timestamp"]
    assert summary["last_timestamp"] == ticks[-1]["timestamp"]

    for signal in signals:
        assert isinstance(signal["prev_price"], Decimal)
        assert isinstance(signal["cur_price"], Decimal)
        assert isinstance(signal["price_change"], Decimal)
        assert isinstance(signal["price_change_pct"], Decimal)
        assert signal["signal"] in {
            "momentum_up",
            "momentum_down",
            "neutral",
        }


def test_pipeline_supports_different_tickers(tmp_path):
    starting_prices = {
        "TSLA": Decimal("300.00"),
        "META": Decimal("500.00"),
    }

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=3,
        output_path_ticks=tmp_path / "different_ticks.jsonl",
        output_path_signals=tmp_path / "different_signals.jsonl",
    )

    assert summary["tick_count"] == 6
    assert summary["signal_count"] == 6
    assert summary["tickers"] == ["META", "TSLA"]
