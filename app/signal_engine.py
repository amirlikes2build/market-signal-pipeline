from decimal import ROUND_HALF_UP, Decimal


def calculate_price_signal(
    ticker: str,
    prev_price: Decimal,
    cur_price: Decimal,
) -> dict[str, Decimal | str]:

    if prev_price <= 0:
        raise ValueError("prev_price has to be greater than 0")

    price_change = cur_price - prev_price
    price_change_pct = (price_change / prev_price) * 100

    if price_change_pct >= 1:
        signal = "momentum_up"
    elif price_change_pct <= -1:
        signal = "momentum_down"
    else:
        signal = "neutral"

    return {
        "ticker": ticker,
        "prev_price": prev_price,
        "cur_price": cur_price,
        "price_change": price_change.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        ),
        "price_change_pct": price_change_pct.quantize(
            Decimal("0.001"),
            rounding=ROUND_HALF_UP,
        ),
        "signal": signal,
    }
