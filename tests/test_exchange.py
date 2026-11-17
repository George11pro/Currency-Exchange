from decimal import Decimal

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_exchange_same_currency():
    response = client.get(
        "/exchange",
        params={
            "from": "USD",
            "to": "USD",
            "amount": "100"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "USD"
    assert Decimal(data["rate"]) == Decimal("1")
    assert Decimal(data["amount"]) == Decimal("100")
    assert Decimal(data["convertedAmount"]) == Decimal("100")


def test_exchange_with_direct_rate():
    create_response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "AUD",
            "targetCurrencyCode": "JPY",
            "rate": "95.5"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/exchange",
        params={
            "from": "AUD",
            "to": "JPY",
            "amount": "2"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "AUD"
    assert data["targetCurrency"]["code"] == "JPY"
    assert Decimal(data["rate"]) == Decimal("95.5")
    assert Decimal(data["amount"]) == Decimal("2")
    assert Decimal(data["convertedAmount"]) == Decimal("191")


def test_exchange_with_reverse_rate():
    response = client.get(
        "/exchange",
        params={
            "from": "JPY",
            "to": "AUD",
            "amount": "95.5"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "JPY"
    assert data["targetCurrency"]["code"] == "AUD"
    assert Decimal(data["rate"]) == Decimal("1") / Decimal("95.5")
    assert Decimal(data["amount"]) == Decimal("95.5")
    assert Decimal(data["convertedAmount"]) == Decimal("1")


def test_exchange_with_cross_rate_through_usd():
    usd_to_aud_response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "AUD",
            "rate": "1.5"
        }
    )

    assert usd_to_aud_response.status_code == 201

    usd_to_rub_response = client.post(
        "/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "RUB",
            "rate": "90"
        }
    )

    assert usd_to_rub_response.status_code == 201

    response = client.get(
        "/exchange",
        params={
            "from": "AUD",
            "to": "RUB",
            "amount": "10"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["baseCurrency"]["code"] == "AUD"
    assert data["targetCurrency"]["code"] == "RUB"
    assert Decimal(data["rate"]) == Decimal("60")
    assert Decimal(data["amount"]) == Decimal("10")
    assert Decimal(data["convertedAmount"]) == Decimal("600")


def test_exchange_with_zero_amount():
    response = client.get(
        "/exchange",
        params={
            "from": "USD",
            "to": "USD",
            "amount": "0"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert Decimal(data["amount"]) == Decimal("0")
    assert Decimal(data["convertedAmount"]) == Decimal("0")


def test_exchange_with_negative_amount():
    response = client.get(
        "/exchange",
        params={
            "from": "USD",
            "to": "USD",
            "amount": "-1"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["message"] == "Сумма не может быть отрицательной"


def test_exchange_with_invalid_base_currency_code():
    response = client.get(
        "/exchange",
        params={
            "from": "US",
            "to": "EUR",
            "amount": "100"
        }
    )

    assert response.status_code == 400


def test_exchange_with_invalid_target_currency_code():
    response = client.get(
        "/exchange",
        params={
            "from": "USD",
            "to": "EU",
            "amount": "100"
        }
    )

    assert response.status_code == 400


def test_exchange_with_unknown_base_currency():
    response = client.get(
        "/exchange",
        params={
            "from": "XXX",
            "to": "USD",
            "amount": "100"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Базовая валюта не найдена"


def test_exchange_with_unknown_target_currency():
    response = client.get(
        "/exchange",
        params={
            "from": "USD",
            "to": "XXX",
            "amount": "100"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Целевая валюта не найдена"


def test_exchange_with_missing_rate():
    response = client.get(
        "/exchange",
        params={
            "from": "AUD",
            "to": "GBP",
            "amount": "100"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Обменный курс не найден"


def test_exchange_with_missing_required_parameter():
    response = client.get(
        "/exchange",
        params={
            "from": "USD",
            "to": "EUR"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["message"] == "Некорректные данные запроса"