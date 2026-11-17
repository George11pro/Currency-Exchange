from decimal import Decimal
from pydantic import BaseModel
from schemas.currency import CurrencyResponse


class ExchangeRateResponse(BaseModel):
    id: int
    baseCurrency: CurrencyResponse
    targetCurrency: CurrencyResponse
    rate: Decimal


class ExchangeResponse(BaseModel):
    baseCurrency: CurrencyResponse
    targetCurrency: CurrencyResponse
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal


class ExchangeRateCreate(BaseModel):
    baseCurrencyCode: str
    targetCurrencyCode: str
    rate: Decimal


class ExchangeRateUpdate(BaseModel):
    rate: Decimal