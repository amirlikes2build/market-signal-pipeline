from dataclasses import asdict

import pyarrow as pa

from app.core.models import MarketOHLCVModel


def generate_parquet_table(data: list[MarketOHLCVModel]) -> dict:
    ohlcv_data = [asdict(item) for item in data]
    table = pa.Table.from_pylist(ohlcv_data)
    
    return table
