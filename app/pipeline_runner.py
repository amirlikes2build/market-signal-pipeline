from decimal import Decimal
from pathlib import Path

from app.signal_storage import save_signals_to_jsonl
from app.tick_batch_generator import generate_market_ticks
from app.tick_signal_processor import process_ticks_to_signals
from app.tick_storage import load_ticks_from_jsonl, save_ticks_to_jsonl


def run_market_tick_pipeline(
    starting_prices: dict[str, Decimal],
    number_of_ticks: int,
    output_path_ticks: str | Path,
    output_path_signals: str | Path,
) -> dict[str, str | int | list[str]]:
    generated_ticks = generate_market_ticks(
        starting_prices=starting_prices, number_of_ticks=number_of_ticks
    )

    save_ticks_to_jsonl(ticks=generated_ticks, output_path=output_path_ticks)
    ticks = load_ticks_from_jsonl(input_path=output_path_ticks)

    if len(ticks) < 1:
        raise ValueError("tick data cannot be empty")

    signals = process_ticks_to_signals(ticks=ticks)
    save_signals_to_jsonl(signals, output_path=output_path_signals)

    return {
        "ticks_output_path": str(output_path_ticks),
        "signals_output_path": str(output_path_signals),
        "tick_count": len(ticks),
        "signal_count": len(signals),
        "tickers": sorted({row["ticker"] for row in ticks}),
        "first_timestamp": ticks[0]["timestamp"],
        "last_timestamp": ticks[-1]["timestamp"],
    }
