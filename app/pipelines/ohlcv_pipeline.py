from datetime import datetime

from app.core.models import MarketOHLCVModel
from app.pipelines.transform.ohlcv_to_parquet import transform_to_parquet_format


def extract_ohlcv_data(
    market_client, ticker: str, start_date, end_date, frequency
) -> list[MarketOHLCVModel]:

    raw_data = market_client.get_historical_ohlcv_data(
        ticker=ticker, start_date=start_date, end_date=end_date, frequency=frequency
    )

    return raw_data


def transform_ohlcv_data(raw_data: list[MarketOHLCVModel]) -> list[dict]:
    return transform_to_parquet_format(raw_data)


def load_ohlcv_data(
    storage_client, data: list[dict], ticker: str, frequency: str
) -> None:
    storage_client.write_ohlcv_data(data, ticker, frequency)


def run_pipeline(
    market_client,
    storage_client,
    ticker: str,
    start_date: datetime | str,
    end_date: datetime | str,
    frequency: str,
) -> None:

    raw_data = extract_ohlcv_data(
        market_client=market_client,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )

    data = transform_ohlcv_data(raw_data)

    load_ohlcv_data(
        storage_client=storage_client, data=data, ticker=ticker, frequency=frequency
    )


# run_pipeline(
#     market_client=TiingoMarketClient(),
#     storage_client=ParquetStorageEngine(),
#     ticker="AMD",
#     start_date="2026-01-01",
#     end_date="2026-02-2",
#     frequency="1min"
# )
