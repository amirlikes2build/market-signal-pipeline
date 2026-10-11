from decimal import Decimal

from app.tick_batch_generator import generate_market_ticks

EXAMPLE_INPUT = {
    "AMD": Decimal("608.10"),
    "NVDA": Decimal("229.28"),
}

EXPECTED_MARKET_TICK_FIELDS = {
    "ticker",
    "prev_price",
    "cur_price",
    "timestamp",
}


def test_output_is_a_list():
    number_of_ticks = 1
    response = generate_market_ticks(EXAMPLE_INPUT, number_of_ticks)

    assert isinstance(response, list)


def test_output_has_correct_amount_ticks():
    number_of_ticks = 5
    response = generate_market_ticks(EXAMPLE_INPUT, number_of_ticks)

    assert len(response) == number_of_ticks * len(EXAMPLE_INPUT)


def test_every_tick_has_correct_fields():
    number_of_ticks = 5
    response = generate_market_ticks(EXAMPLE_INPUT, number_of_ticks)

    for tick in response:
        assert EXPECTED_MARKET_TICK_FIELDS.issubset(tick.keys())


def test_expected_tickers():
    number_of_ticks = 5
    response = generate_market_ticks(EXAMPLE_INPUT, number_of_ticks)

    seen = {tick["ticker"] for tick in response}

    assert seen == set(EXAMPLE_INPUT.keys())


def test_tick_uses_cur_price_and_prev_price_correctly():
    number_of_ticks = 5
    response = generate_market_ticks(EXAMPLE_INPUT, number_of_ticks)

    amd_ticks = [tick for tick in response if tick["ticker"] == "AMD"]

    assert amd_ticks[0]["cur_price"] == amd_ticks[1]["prev_price"]


def test_starting_prices_is_not_mutated():
    number_of_ticks = 5
    starting_prices = {
        "AMD": Decimal("608.10"),
        "NVDA": Decimal("229.28"),
    }
    original_starting_prices = starting_prices.copy()

    generate_market_ticks(starting_prices, number_of_ticks)

    assert starting_prices == original_starting_prices
