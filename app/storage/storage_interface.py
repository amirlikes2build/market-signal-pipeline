from abc import ABC, abstractmethod


class StorageInterface(ABC):
    @abstractmethod
    def write_ohlcv_data(self, data: list[dict], ticker: str, frequency: str) -> None:
        """Store OHCLV data"""
