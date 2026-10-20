from abc import ABC, abstractmethod

from app.core.models import MarketOHLCVModel


class StorageInterface(ABC):
    @abstractmethod
    def store_ohlcv_data(self, data: list[MarketOHLCVModel], ticker: str) -> None:
        """ Store OHCLV data """
