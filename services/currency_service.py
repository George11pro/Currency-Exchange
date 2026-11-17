
from repositories.currency_repository import (
    get_all_currencies,
    get_currency_by_code,
    create_currency
)

from utils.validators import validate_currency_code


def get_currencies():
    return get_all_currencies()


def get_currency(code: str):
    code = validate_currency_code(code)

    return get_currency_by_code(code)


def add_currency(code: str, name: str, sign: str):
    code = validate_currency_code(code)

    return create_currency(
        code=code,
        name=name,
        sign=sign
    )



def add_currency(code: str, name: str, sign: str):
    code = validate_currency_code(code)
    return create_currency(code, name, sign)
