from decimal import Decimal

from app.pipeline_runner import run_market_tick_pipeline
from app.tick_storage import load_ticks_from_jsonl


def test_pipeline_creates_output_file(tmp_path):
    starting_prices = {
        "AAPL": Decimal("100.00"),
        "MSFT": Decimal("200.00"),
    }
    output_path = tmp_path / "ticks.jsonl"

    run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=5,
        output_path=output_path,
    )

    assert output_path.exists()


def test_pipeline_summary_has_correct_tick_count(tmp_path):
    starting_prices = {
        "AAPL": Decimal("100.00"),
        "MSFT": Decimal("200.00"),
    }
    number_of_ticks = 5
    output_path = tmp_path / "ticks.jsonl"

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=number_of_ticks,
        output_path=output_path,
    )

    assert summary["tick_count"] == len(starting_prices) * number_of_ticks


def test_pipeline_summary_has_correct_tickers(tmp_path):
    starting_prices = {
        "AAPL": Decimal("100.00"),
        "MSFT": Decimal("200.00"),
    }
    output_path = tmp_path / "ticks.jsonl"

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=5,
        output_path=output_path,
    )

    assert summary["tickers"] == ["AAPL", "MSFT"]


def test_pipeline_summary_output_path_matches_passed_path(tmp_path):
    starting_prices = {
        "AAPL": Decimal("100.00"),
        "MSFT": Decimal("200.00"),
    }
    output_path = tmp_path / "ticks.jsonl"

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=5,
        output_path=output_path,
    )

    assert summary["output_path"] == str(output_path)


def test_saved_file_record_count_matches_summary_tick_count(tmp_path):
    starting_prices = {
        "AAPL": Decimal("100.00"),
        "MSFT": Decimal("200.00"),
    }
    output_path = tmp_path / "ticks.jsonl"

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=5,
        output_path=output_path,
    )

    loaded_ticks = load_ticks_from_jsonl(output_path)

    assert len(loaded_ticks) == summary["tick_count"]


def test_pipeline_has_no_hardcoded_ticker_dependency(tmp_path):
    starting_prices = {
        "TSLA": Decimal("300.00"),
        "META": Decimal("500.00"),
    }
    number_of_ticks = 3
    output_path = tmp_path / "different_tickers.jsonl"

    summary = run_market_tick_pipeline(
        starting_prices=starting_prices,
        number_of_ticks=number_of_ticks,
        output_path=output_path,
    )

    assert summary["tick_count"] == len(starting_prices) * number_of_ticks
    assert summary["tickers"] == ["META", "TSLA"]
