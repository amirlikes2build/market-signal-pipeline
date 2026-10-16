from decimal import Decimal
from pathlib import Path

from app.tick_batch_generator import generate_market_ticks
from app.tick_storage import load_ticks_from_jsonl, save_ticks_to_jsonl


def run_market_tick_pipeline(
    starting_prices: dict[str, Decimal],
    number_of_ticks: int,
    output_path: str | Path,
) -> dict[str, str | int | list[str]]:
    generated_ticks = generate_market_ticks(
        starting_prices=starting_prices, number_of_ticks=number_of_ticks
    )

    save_ticks_to_jsonl(ticks=generated_ticks, output_path=output_path)

    loaded_ticks = load_ticks_from_jsonl(output_path)

    if len(loaded_ticks) < 1:
        raise ValueError("Empty data passed")

    return {
        "output_path": str(output_path),
        "tick_count": len(loaded_ticks),
        "tickers": sorted({row["ticker"] for row in loaded_ticks}),
        "first_timestamp": loaded_ticks[0]["timestamp"],
        "last_timestamp": loaded_ticks[-1]["timestamp"],
    }
