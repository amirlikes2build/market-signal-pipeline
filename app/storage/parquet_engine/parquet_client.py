from dataclasses import asdict
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from app.core.models import MarketOHLCVModel
from app.storage.storage_interface import StorageInterface


class ParquetStorageEngine(StorageInterface):
    def __init__(self, folder_path: Path | None = None):
        self.folder_path = folder_path or Path("app/storage/parquet_engine/ohlcv_data")
        self.folder_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _transform_ohlcv_to_parquet_table(
        data: list[MarketOHLCVModel],
        schema: pa.Schema
    ) -> pa.Table:

        ohlcv_data = [asdict(item) for item in data]
        table = pa.Table.from_pylist(ohlcv_data, schema)

        return table

    @staticmethod
    def define_schema():
        return pa.schema([
            ("timestamp", pa.timestamp(unit='ms', tz='UTC')),
            ("open", pa.decimal128(10, 2)),
            ("high", pa.decimal128(10, 2)),
            ("low", pa.decimal128(10, 2)),
            ("close", pa.decimal128(10, 2)),
            ("volume", pa.int64())
        ])

    def write_ohlcv_data(self,
        data: list[MarketOHLCVModel],
        ticker: str,
        frequency: str
    ) -> None:

        path = self.folder_path / frequency
        print(path)
        path.mkdir(parents=True, exist_ok=True)

        table = self._transform_ohlcv_to_parquet_table(data, ParquetStorageEngine.define_schema())
        pq.write_table(table, path / f"{ticker}.parquet")

    def read_parquet_file(self, file_path: Path | str) -> pd.DataFrame:
        return pd.read_parquet(file_path)

from datetime import datetime
from decimal import Decimal

from app.core.models import MarketOHLCVModel

data = [MarketOHLCVModel(timestamp=datetime.fromisoformat("2013-07-07T00:56:46Z"), open=Decimal("123.12"), high=Decimal("123.12"),
    low=Decimal("123.12"), close=Decimal("123.12"), volume=1234)]

c = ParquetStorageEngine()

# c.write_ohlcv_data(data, 'MSFT', frequency='daily')

print(c.read_parquet_file(file_path="/Users/admin/Documents/builds/market-signal-pipeline/app/storage/parquet_engine/ohlcv_data/daily/MSFT.parquet"))
