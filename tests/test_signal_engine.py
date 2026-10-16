from decimal import Decimal

import pytest

from app.signal_engine import calculate_price_signal


def test_full_output_momentum_up():
    result = calculate_price_signal(
        ticker="NFLX",
        prev_price=Decimal("70.00"),
        cur_price=Decimal("100.00"),
    )

    assert result == {
        "ticker": "NFLX",
        "prev_price": Decimal("70.00"),
        "cur_price": Decimal("100.00"),
        "price_change": Decimal("30.00"),
        "price_change_pct": Decimal("42.857"),
        "signal": "momentum_up",
    }


def test_momentum_down():
    result = calculate_price_signal(
        ticker="GOOG",
        prev_price=Decimal("346.32"),
        cur_price=Decimal("300.20"),
    )

    assert result["signal"] == "momentum_down"


def test_momentum_neutral():
    result = calculate_price_signal(
        ticker="AMAZ",
        prev_price=Decimal("100.00"),
        cur_price=Decimal("100.2"),
    )

    assert result["signal"] == "neutral"


def test_zero_values():
    with pytest.raises(ValueError):
        calculate_price_signal(
            ticker="AMD",
            prev_price=Decimal("0.00"),
            cur_price=Decimal("98.00"),
        )
