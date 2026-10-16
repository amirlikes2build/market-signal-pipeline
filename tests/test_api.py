from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

EXPECTED_SIGNAL_FIELDS = {
    "ticker",
    "previous_price",
    "current_price",
    "price_change",
    "price_change_pct",
    "signal",
    "timestamp",
}


def test_get_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "market-signal-pipeline is running"}


def test_healthz():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "market-signal-pipeline",
    }


def test_get_signals_returns_list_of_signals():
    response = client.get("/signals")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert EXPECTED_SIGNAL_FIELDS.issubset(data[0].keys())


def test_get_signal_normal():
    response = client.get("/signals/AAPL")

    assert response.status_code == 200

    data = response.json()

    assert data["ticker"] == "AAPL"
    assert EXPECTED_SIGNAL_FIELDS.issubset(data.keys())


def test_get_signal_lowercase():
    response = client.get("/signals/aapl")

    assert response.status_code == 200

    data = response.json()

    assert data["ticker"] == "AAPL"
    assert EXPECTED_SIGNAL_FIELDS.issubset(data.keys())


def test_get_signal_unknown_ticker():
    response = client.get("/signals/UNKNOWN")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Signal not found for ticker: UNKNOWN",
    }
