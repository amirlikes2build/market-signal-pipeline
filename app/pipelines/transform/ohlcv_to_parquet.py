from dataclasses import asdict
from decimal import ROUND_HALF_EVEN, Decimal

from app.core.models import MarketOHLCVModel


def transform_to_parquet_format(data: list[MarketOHLCVModel]) -> list[dict]:
    list_of_ohlcv = []

    for item in data:
        ohlcv_entry = asdict(item)
        for name, value in ohlcv_entry.items():
            if isinstance(value, Decimal):
                ohlcv_entry[name] = ohlcv_entry[name].quantize(
                    exp=Decimal("0.01"),
                    rounding=ROUND_HALF_EVEN)

        list_of_ohlcv.append(ohlcv_entry)

    return list_of_ohlcv
