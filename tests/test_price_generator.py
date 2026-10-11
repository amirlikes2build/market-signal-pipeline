from datetime import datetime
from decimal import Decimal

import pytest

from app.price_generator import market_data_producer

EXPECTED_MARKET_TICK_FIELDS = {"ticker", "prev_price", "cur_price", "timestamp"}


def test_market_tick_expected_fields():
    response = market_data_producer("MSFT", Decimal("550.50"))
    assert EXPECTED_MARKET_TICK_FIELDS.issubset(response.keys())


def test_market_tick_lowercase_ticker():
    response = market_data_producer("msft", Decimal("550.50"))
    assert response["ticker"] == "MSFT"


def test_market_tick_original_prev_price_remains():
    prev_price = Decimal("550.50")
    response = market_data_producer("msft", prev_price)
    assert response["prev_price"] == prev_price


def test_market_tick_cur_price_is_decimal():
    response = market_data_producer("MSFT", Decimal("550.50"))
    assert isinstance(response["cur_price"], Decimal)


def test_market_tick_cur_price_is_greater_than_zero():
    response = market_data_producer("MSFT", Decimal("0.01"))
    assert response["cur_price"] > Decimal(0)


def test_market_tick_cur_price_includes_timestamp():
    response = market_data_producer("MSFT", Decimal("550.50"))
    timestamp = datetime.fromisoformat(response["timestamp"])
    assert isinstance(timestamp, datetime)


def test_market_prev_price_equals_zero():
    with pytest.raises(ValueError):
        market_data_producer("MSFT", Decimal(0))


def test_market_prev_price_negative_value():
    with pytest.raises(ValueError):
        market_data_producer("MSFT", Decimal(-550))


def test_market_prev_price_blank_ticker():
    with pytest.raises(ValueError):
        market_data_producer("", Decimal("550.50"))
