import random
from datetime import UTC, datetime
from decimal import Decimal


def generate_next_price(prev_price: Decimal) -> Decimal:
    std = max(prev_price / 100, Decimal("0.01"))
    flux = Decimal(str(random.gauss(0, float(std))))
    prev_price_flux = prev_price + flux

    final_price = max(prev_price_flux.quantize(Decimal("0.01")), Decimal("0.01"))

    return final_price


def market_data_producer(ticker: str, prev_price: Decimal) -> dict[str, str | Decimal]:

    if not isinstance(prev_price, Decimal):
        raise TypeError("<prev_price> must be a Decimal")

    if prev_price <= 0:
        raise ValueError("<prev_price> must be greater than 0")

    ticker = str(ticker).strip().upper()
    if not ticker:
        raise ValueError("<ticker> cannot be empty")

    cur_price = generate_next_price(prev_price)

    return {
        "ticker": ticker,
        "prev_price": prev_price,
        "cur_price": cur_price,
        "timestamp": datetime.now(UTC).isoformat(),
    }
