from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from dotenv import dotenv_values
from tiingo import TiingoClient as Client

from app.core.market_data_interface import APIClient
from app.core.models import MarketOHLCVModel


class TiingoMarketClient(APIClient):
    def __init__(self):
        self.env_cfg = dotenv_values(Path(__file__).parent / ".env")

        self.conn = Client({
            "api_key": self.env_cfg["API_KEY"],
            "session": True
        })

    def get_historical_ohlcv_data(
        self,
        ticker: str,
        start_date: str | date | datetime,
        end_date: str | date | datetime,
        frequency: str
    ) -> list[MarketOHLCVModel]:

        ohlcv_data = self.conn.get_ticker_price(
            ticker=ticker,
            startDate=start_date,
            endDate=end_date,
            frequency=frequency,
            columns="open,high,low,close,volume"
        )

        rows = []

        for row in ohlcv_data:
            row: Any
            rows.append(
                MarketOHLCVModel(
                timestamp=datetime.fromisoformat(row["date"]),
                open=Decimal(row["open"]),
                high=Decimal(row["high"]),
                low=Decimal(row["low"]),
                close=Decimal(row["close"]),
                volume=Decimal(row["volume"])
            )
        )

        return rows
