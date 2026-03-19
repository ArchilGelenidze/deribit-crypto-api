from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)


def test_root_redirect():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_get_all_prices_missing_ticker():
    response = client.get("/prices/all")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "ticker"]


def test_get_all_prices_invalid_ticker():
    response = client.get("/prices/all?ticker=xrp_usd")

    assert response.status_code == 422
    assert "btc_usd" in response.text


def test_get_latest_price_missing_ticker():
    response = client.get("/prices/latest")

    assert response.status_code == 422


def test_get_price_by_date_invalid_date_format():
    response = client.get("/prices/by-date?ticker=btc_usd&target_date=сегодня")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "target_date"]


def test_get_price_by_date_missing_params():
    response = client.get("/prices/by-date")

    assert response.status_code == 422
    assert len(response.json()["detail"]) == 2
