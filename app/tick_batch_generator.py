from decimal import Decimal

from app.price_generator import market_data_producer


def generate_market_ticks(
    starting_prices: dict[str, Decimal], number_of_ticks: int
) -> list[dict[str, str | Decimal]]:

    output = []
    tracked_prices = starting_prices.copy()

    for _ in range(number_of_ticks):
        for ticker in tracked_prices:
            new_data = market_data_producer(
                ticker=ticker,
                prev_price=tracked_prices[ticker],
            )

            output.append(new_data)

            tracked_prices[ticker] = new_data["cur_price"]

    return output
