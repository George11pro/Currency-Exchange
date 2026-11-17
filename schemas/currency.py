# Pydantic схемы
from pydantic import BaseModel


class CurrencyResponse(BaseModel):
    id: int
    name: str
    code: str
    sign: str


class CurrencyCreate(BaseModel):
    name: str
    code: str
    sign: str