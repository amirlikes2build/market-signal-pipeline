from decimal import Decimal

from app.tick_batch_generator import generate_market_ticks
from app.tick_signal_processor import process_ticks_to_signals

DEMO_STARTING_PRICES = {
    "AAPL": Decimal("365.50"),
    "MSFT": Decimal("275.50"),
    "NVDA": Decimal("135.50"),
}


def get_all_signals() -> list[dict]:
    ticks = generate_market_ticks(
        starting_prices=DEMO_STARTING_PRICES,
        number_of_ticks=1,
    )

    return process_ticks_to_signals(ticks)


def get_signal_by_ticker(ticker: str) -> dict | None:
    ticker = ticker.upper()

    if ticker not in DEMO_STARTING_PRICES:
        return None

    ticks = generate_market_ticks(
        starting_prices={ticker: DEMO_STARTING_PRICES[ticker]},
        number_of_ticks=1,
    )

    signals = process_ticks_to_signals(ticks)

    return signals[0]
