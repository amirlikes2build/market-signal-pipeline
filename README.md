# Market Signal Pipeline

A production-style Python project for building a market-data pipeline that ingests price data, generates research signals, and exposes those signals through an API.

The goal is to build a quant data engineering portfolio project that demonstrates backend engineering, data pipelines, signal generation, testing, CI/CD, containers, cloud deployment, batch processing, and eventually streaming architecture.

This project is being built as part of a transition toward a Quant Data Engineer / Financial Data Engineer role.

## Project vision

The long-term aim is to build a realistic market-data platform with the following flow:

Market data source\
→ ingestion layer\
→ validation and cleaning\
→ raw data storage\
→ signal engine\
→ signal storage\
→ API layer\
→ scheduled batch jobs\
→ streaming pipeline\
→ cloud deployment

The project starts with fake/generated market data so that the pipeline, tests, and architecture can be built safely before introducing real external data providers.

## Target tech stack

- Python
- FastAPI
- pytest
- Ruff
- Docker
- GitHub Actions
- GitHub Container Registry
- Render
- pandas
- NumPy
- PostgreSQL
- DuckDB
- Parquet
- Apache Airflow
- Kafka / Redpanda
- AWS: S3, ECS/Fargate, ECR, CloudWatch, IAM

## Market data direction

The project will initially use generated market data, then evolve toward external market data providers.

Possible future data sources include:

- `yfinance` for personal-learning experiments
- Alpha Vantage for free or low-cost API-based data
- Polygon/Massive-style APIs for more serious market-data access
- Bloomberg or Refinitiv-style feeds as enterprise-level reference targets

The code should be designed so that the data provider can be swapped without rewriting the signal engine.

## Signal engine direction

The signal engine starts with simple price-change momentum and is intended to evolve into a more advanced research signal layer.

Planned signal features include:

- percentage returns
- moving averages
- rolling volatility
- z-scores
- breakout-style signals
- mean-reversion-style signals
- volume and price anomaly detection
- confidence scoring

The goal is not to create a live trading bot, but to build a strong financial data engineering system that can generate explainable research signals from market data.

## Target architecture

The project is being built gradually toward a distributed architecture:

1. API service for exposing market signals.
2. Market data producer for generating or ingesting price ticks.
3. Batch generator for producing historical-style market data.
4. Storage layer for raw ticks and generated signals.
5. pandas and NumPy layer for more advanced calculations.
6. Scheduled batch workflows with Airflow.
7. Streaming pipeline with Kafka or Redpanda.
8. Cloud deployment using AWS services.
9. Monitoring, logging, and smoke testing.

## Development workflow

The target development workflow is:

Push to main\
→ run linting\
→ run tests\
→ build Docker image\
→ push image to container registry\
→ deploy service\
→ smoke-test deployed API

## API direction

The API is intended to expose endpoints such as:

`GET /healthz`

Service health check.

`GET /signals`

Returns available signal records.

`GET /signals/{ticker}`

Returns a signal record for a specific ticker.

Future API endpoints may include:

`GET /market-data/ticks`

Returns generated or ingested market data ticks.

`GET /signals/{ticker}/history`

Returns historical signals for a ticker.

`GET /signals/{ticker}/metrics`

Returns richer signal metrics such as rolling volatility, moving averages, and confidence scores.

## Disclaimer

This project is for learning, engineering practice, and portfolio development only. It does not provide financial advice, trading recommendations, or production investment signals.
