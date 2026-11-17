from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_currencies():
    response = client.get("/currencies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_existing_currency():
    response = client.get("/currency/USD")

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == "USD"
    assert data["name"] == "United States dollar"
    assert data["sign"] == "$"


def test_get_currency_case_insensitive():
    response = client.get("/currency/usd")

    assert response.status_code == 200

    data = response.json()

    assert data["code"] == "USD"
я

def test_get_nonexistent_currency():
    response = client.get("/currency/XXX")

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Валюта не найдена"


def test_get_currency_with_invalid_code():
    response = client.get("/currency/US")

    assert response.status_code == 400


def test_create_currency():
    response = client.post(
        "/currencies",
        data={
            "name": "Canadian dollar",
            "code": "CAD",
            "sign": "$"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Canadian dollar"
    assert data["code"] == "CAD"
    assert data["sign"] == "$"
    assert isinstance(data["id"], int)


def test_create_duplicate_currency():
    response = client.post(
        "/currencies",
        data={
            "name": "Canadian dollar",
            "code": "CAD",
            "sign": "$"
        }
    )

    assert response.status_code == 409

    data = response.json()

    assert data["message"] == "Валюта с таким кодом уже существует"
