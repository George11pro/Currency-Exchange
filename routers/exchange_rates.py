from decimal import Decimal

from fastapi import APIRouter, Form, HTTPException, Query

from schemas.exchange_rate import (
    ExchangeRateResponse,
    ExchangeResponse
)

from services.exchange_rate_service import (
    get_exchange_rates,
    get_rate,
    add_exchange_rate,
    update_rate,
    calculate_exchange
)

from utils.validators import (
    validate_currency_code,
    validate_currency_pair
)


router = APIRouter()


def serialize_exchange_rate(exchange_rate):
    return {
        "id": exchange_rate["ID"],
        "baseCurrency": {
            "id": exchange_rate["BaseCurrencyId"],
            "name": exchange_rate["BaseCurrencyName"],
            "code": exchange_rate["BaseCurrencyCode"],
            "sign": exchange_rate["BaseCurrencySign"]
        },
        "targetCurrency": {
            "id": exchange_rate["TargetCurrencyId"],
            "name": exchange_rate["TargetCurrencyName"],
            "code": exchange_rate["TargetCurrencyCode"],
            "sign": exchange_rate["TargetCurrencySign"]
        },
        "rate": Decimal(str(exchange_rate["Rate"]))
    }


@router.get(
    "/exchangeRates",
    response_model=list[ExchangeRateResponse]
)
def get_all():
    exchange_rates = get_exchange_rates()

    return [
        serialize_exchange_rate(exchange_rate)
        for exchange_rate in exchange_rates
    ]


@router.get(
    "/exchangeRate/{pair}",
    response_model=ExchangeRateResponse
)
def get_one(pair: str):
    try:
        base_code, target_code = validate_currency_pair(pair)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    exchange_rate = get_rate(
        base_code,
        target_code
    )

    if exchange_rate is None:
        raise HTTPException(
            status_code=404,
            detail="Обменный курс не найден"
        )

    return serialize_exchange_rate(exchange_rate)


@router.post(
    "/exchangeRates",
    status_code=201,
    response_model=ExchangeRateResponse
)
def create(
    baseCurrencyCode: str = Form(...),
    targetCurrencyCode: str = Form(...),
    rate: Decimal = Form(...)
):
    try:
        base_code = validate_currency_code(
            baseCurrencyCode
        )

        target_code = validate_currency_code(
            targetCurrencyCode
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if rate <= 0:
        raise HTTPException(
            status_code=400,
            detail="Курс должен быть больше нуля"
        )

    exchange_rate_id, error = add_exchange_rate(
        base_code=base_code,
        target_code=target_code,
        rate=rate
    )

    if error == "base_currency_not_found":
        raise HTTPException(
            status_code=404,
            detail="Базовая валюта не найдена"
        )

    if error == "target_currency_not_found":
        raise HTTPException(
            status_code=404,
            detail="Целевая валюта не найдена"
        )

    if error == "already_exists":
        raise HTTPException(
            status_code=409,
            detail="Валютная пара уже существует"
        )

    exchange_rate = get_rate(
        base_code,
        target_code
    )

    return serialize_exchange_rate(exchange_rate)


@router.patch(
    "/exchangeRate/{pair}",
    response_model=ExchangeRateResponse
)
def update(
    pair: str,
    rate: Decimal = Form(...)
):
    try:
        base_code, target_code = validate_currency_pair(pair)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if rate <= 0:
        raise HTTPException(
            status_code=400,
            detail="Курс должен быть больше нуля"
        )

    exchange_rate = update_rate(
        base_code,
        target_code,
        rate
    )

    if exchange_rate is None:
        raise HTTPException(
            status_code=404,
            detail="Обменный курс не найден"
        )

    return serialize_exchange_rate(exchange_rate)


@router.get(
    "/exchange",
    response_model=ExchangeResponse
)
def exchange(
    from_code: str = Query(..., alias="from"),
    to: str = Query(...),
    amount: Decimal = Query(...)
):
    try:
        from_code = validate_currency_code(from_code)
        to_code = validate_currency_code(to)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Сумма не может быть отрицательной"
        )

    result, error = calculate_exchange(
        from_code,
        to_code
    )

    if error == "base_currency_not_found":
        raise HTTPException(
            status_code=404,
            detail="Базовая валюта не найдена"
        )

    if error == "target_currency_not_found":
        raise HTTPException(
            status_code=404,
            detail="Целевая валюта не найдена"
        )

    if error == "rate_not_found":
        raise HTTPException(
            status_code=404,
            detail="Обменный курс не найден"
        )

    rate = result["rate"]

    if not isinstance(rate, Decimal):
        rate = Decimal(str(rate))

    converted_amount = amount * rate

    return {
        "baseCurrency": {
            "id": result["baseCurrency"]["ID"],
            "name": result["baseCurrency"]["FullName"],
            "code": result["baseCurrency"]["Code"],
            "sign": result["baseCurrency"]["Sign"]
        },
        "targetCurrency": {
            "id": result["targetCurrency"]["ID"],
            "name": result["targetCurrency"]["FullName"],
            "code": result["targetCurrency"]["Code"],
            "sign": result["targetCurrency"]["Sign"]
        },
        "rate": rate,
        "amount": amount,
        "convertedAmount": converted_amount
    }
