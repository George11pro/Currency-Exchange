from fastapi.testclient import TestClient
from decimal import Decimal

from main import app


client = TestClient(app)


def test_get_exchange_rates():
    response = client.get("/exchangeRates")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_create_exchange_rate():
    response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "EUR",
            "rate": "0.92"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "EUR"
    assert Decimal(data["rate"]) == Decimal("0.92")
    assert isinstance(data["id"], int)


def test_get_exchange_rate():
    response = client.get("/exchangeRate/USDEUR")

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "EUR"
    assert Decimal(data["rate"]) == Decimal("0.92")


def test_get_exchange_rate_case_insensitive():
    response = client.get("/exchangeRate/usdeur")

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "EUR"


def test_get_nonexistent_exchange_rate():
    response = client.get("/exchangeRate/USDGBP")

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Обменный курс не найден"


def test_get_exchange_rate_with_invalid_pair():
    response = client.get("/exchangeRate/USD")

    assert response.status_code == 400


def test_create_duplicate_exchange_rate():
    response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "EUR",
            "rate": "0.95"
        }
    )

    assert response.status_code == 409

    data = response.json()

    assert data["message"] == "Валютная пара уже существует"


def test_create_exchange_rate_with_unknown_base_currency():
    response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "XXX",
            "targetCurrencyCode": "EUR",
            "rate": "0.92"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Базовая валюта не найдена"


def test_create_exchange_rate_with_unknown_target_currency():
    response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "XXX",
            "rate": "0.92"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Целевая валюта не найдена"


def test_create_exchange_rate_with_invalid_rate():
    response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "GBP",
            "rate": "-1"
        }
    )

    assert response.status_code == 400


def test_update_exchange_rate():
    response = client.patch(
        "/exchangeRate/USDEUR",
        data={
            "rate": "0.95"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "EUR"
    assert Decimal(data["rate"]) == Decimal("0.95")


def test_update_nonexistent_exchange_rate():
    response = client.patch(
        "/exchangeRate/USDGBP",
        data={
            "rate": "0.95"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Обменный курс не найден"


def test_update_exchange_rate_with_invalid_rate():
    response = client.patch(
        "/exchangeRate/USDEUR",
        data={
            "rate": "-1"
        }
    )

    assert response.status_code == 400
