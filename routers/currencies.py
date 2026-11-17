import sqlite3

from fastapi import APIRouter, Form, HTTPException

from schemas.currency import CurrencyResponse

from services.currency_service import (
    get_currencies,
    get_currency,
    add_currency
)


router = APIRouter()


def serialize_currency(currency):
    return {
        "id": currency["ID"],
        "name": currency["FullName"],
        "code": currency["Code"],
        "sign": currency["Sign"]
    }


@router.get(
    "/currencies",
    response_model=list[CurrencyResponse]
)
def get_all():
    currencies = get_currencies()

    return [
        serialize_currency(currency)
        for currency in currencies
    ]


@router.get(
    "/currency/{code}",
    response_model=CurrencyResponse
)
def get_one(code: str):
    try:
        currency = get_currency(code)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if currency is None:
        raise HTTPException(
            status_code=404,
            detail="Валюта не найдена"
        )

    return serialize_currency(currency)


@router.post(
    "/currencies",
    status_code=201,
    response_model=CurrencyResponse
)
def create(
    name: str = Form(...),
    code: str = Form(...),
    sign: str = Form(...)
):
    if not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Название валюты не может быть пустым"
        )

    if not sign.strip():
        raise HTTPException(
            status_code=400,
            detail="Символ валюты не может быть пустым"
        )

    try:
        currency_id = add_currency(
            code=code,
            name=name.strip(),
            sign=sign.strip()
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Валюта с таким кодом уже существует"
        )

    return {
        "id": currency_id,
        "name": name.strip(),
        "code": code.strip().upper(),
        "sign": sign.strip()
    }
