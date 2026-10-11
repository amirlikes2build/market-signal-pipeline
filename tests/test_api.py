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
    assert response.json() == {"message": "mini-ci-cd is running"}


def test_healthz():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "mini-ci-cd",
    }


"""

Here we are testing the response object of Endpoint, one note is that: the reason why do we json() over response first. Is because the response carries
several other bits of data like the status code which we checked first if it equates to 200 (what we expect for a succesfull request). So by doing
json() we just get the message body.

Based of the data structure we used, we expect a LIST of a dicts (where each dict is a signal record) so this is what we expect.

Hence we first do isinstance to check if the our structure is of a list nature.

Then we check if our result actually gave us any signals, so we check if there is at least one dict (in this case signal) in our list.

Then we do a schema check on the first item in the list, using index lookup (0 in this case) is generally fine since we have already tested and stated we at least expect one signal anyways. And ofc we do keys() over it to grab the field names.

"""


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
