from dataclasses import asdict
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from app.core.market_data_interface import MarketOHLCVModel
from app.storage.storage_interface import StorageInterface


class ParquetStorageEngine(StorageInterface):
    def __init__(self):
        self.folder_path = Path("app/storage/parquet_engine/ohlcv_data")
        self.folder_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def transform_ohlcv_to_parquet_table(data: list[MarketOHLCVModel]):
        ohlcv_data = [asdict(item) for item in data]
        table = pa.Table.from_pylist(ohlcv_data)

        return table

    def store_ohlcv_data(self, data: list[MarketOHLCVModel], ticker: str) -> None:
        table = self.transform_ohlcv_to_parquet_table(data)
        pq.write_table(table, self.folder_path / f"{ticker}.parquet")
