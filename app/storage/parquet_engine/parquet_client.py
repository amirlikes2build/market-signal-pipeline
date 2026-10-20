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
    def _transform_ohlcv_to_parquet_table(data: list[MarketOHLCVModel]) -> pa.table:
        ohlcv_data = [asdict(item) for item in data]
        table = pa.Table.from_pylist(ohlcv_data)

        return table

    def store_ohlcv_data(self, data: list[MarketOHLCVModel], ticker: str) -> None:
        table = self._transform_ohlcv_to_parquet_table(data)
        pq.write_table(table, self.folder_path / f"{ticker}.parquet")

    def read_back_parquet(self, table) -> pd.DataFrame:
        df = pd.read_parquet(table)
        return df


data = [
    MarketOHLCVModel(
        1, 2, 3, 4, 5, 6
    )
]

client = ParquetStorageEngine()
client.store_ohlcv_data(data, "AAPL")
