from pathlib import Path

import duckdb
import pandas as pd


class DuckDBClient:
    def __init__(self):
        self.parquet_storage = Path(__file__).resolve().parent.parent / "parquet_engine" / "ohlcv_data"

    def fetch_ohlcv_data(self, ticker: str, start_date=None, end_date=None) -> pd.DataFrame | bool:
        file_path = self.parquet_storage / f"{ticker}.parquet"

        if not file_path.exists():
            return False

        result = duckdb.sql(
            "SELECT * FROM read_parquet(?)",
            params=[str(file_path)]
        ).df()

        return result

client = DuckDBClient()

print(client.fetch_ohlcv_data('AAPL'))
