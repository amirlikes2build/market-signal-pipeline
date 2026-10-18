from abc import ABC, abstractmethod
from datetime import date, datetime

from app.core.models import MarketOHLCVModel


class APIClient(ABC):
    @abstractmethod
    def get_historical_ohlcv_data(
        self,
        ticker: str,
        start_date: datetime | date | str,
        end_date: datetime | date | str,
        frequency: str
    ) -> list[MarketOHLCVModel]:

        """ Retrieve historical OHCLV data for a ticker """
