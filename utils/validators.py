import re


CURRENCY_CODE_PATTERN = re.compile(r"^[A-Z]{3}$")


def validate_currency_code(code: str) -> str:
    code = code.strip().upper()

    if not CURRENCY_CODE_PATTERN.fullmatch(code):
        raise ValueError(
            "Код валюты должен состоять из 3 латинских букв"
        )

    return code


def validate_currency_pair(pair: str) -> tuple[str, str]:
    pair = pair.strip().upper()

    if len(pair) != 6 or not pair.isalpha():
        raise ValueError(
            "Некорректная валютная пара"
        )

    base_code = pair[:3]
    target_code = pair[3:]

    validate_currency_code(base_code)
    validate_currency_code(target_code)

    return base_code, target_code
