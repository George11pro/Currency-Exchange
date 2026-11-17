from decimal import Decimal

from repositories.currency_repository import get_currency_by_code

from repositories.exchange_rate_repository import (
    get_all_exchange_rates,
    get_exchange_rate,
    create_exchange_rate,
    update_exchange_rate
)


def get_exchange_rates():
    return get_all_exchange_rates()


def get_rate(base_code: str, target_code: str):
    return get_exchange_rate(
        base_code.upper(),
        target_code.upper()
    )


def add_exchange_rate(
    base_code: str,
    target_code: str,
    rate: Decimal
):
    base_code = base_code.upper()
    target_code = target_code.upper()

    base_currency = get_currency_by_code(base_code)

    if base_currency is None:
        return None, "base_currency_not_found"

    target_currency = get_currency_by_code(target_code)

    if target_currency is None:
        return None, "target_currency_not_found"

    if get_exchange_rate(base_code, target_code) is not None:
        return None, "already_exists"

    exchange_rate_id = create_exchange_rate(
        base_currency["ID"],
        target_currency["ID"],
        rate
    )

    return exchange_rate_id, None


def update_rate(
    base_code: str,
    target_code: str,
    rate: Decimal
):
    exchange_rate = get_exchange_rate(
        base_code.upper(),
        target_code.upper()
    )

    if exchange_rate is None:
        return None

    update_exchange_rate(
        exchange_rate["BaseCurrencyId"],
        exchange_rate["TargetCurrencyId"],
        rate
    )

    return get_exchange_rate(
        base_code.upper(),
        target_code.upper()
    )


def calculate_exchange(
    base_code: str,
    target_code: str
):
    base_code = base_code.upper()
    target_code = target_code.upper()

    base_currency = get_currency_by_code(base_code)
    target_currency = get_currency_by_code(target_code)

    if base_currency is None:
        return None, "base_currency_not_found"

    if target_currency is None:
        return None, "target_currency_not_found"

    if base_code == target_code:
        return {
            "baseCurrency": base_currency,
            "targetCurrency": target_currency,
            "rate": Decimal("1")
        }, None

    # 1. Прямой курс A -> B

    direct_rate = get_exchange_rate(
        base_code,
        target_code
    )

    if direct_rate is not None:
        return {
            "baseCurrency": base_currency,
            "targetCurrency": target_currency,
            "rate": Decimal(str(direct_rate["Rate"]))
        }, None

    # 2. Обратный курс B -> A

    reverse_rate = get_exchange_rate(
        target_code,
        base_code
    )

    if reverse_rate is not None:
        reverse_value = Decimal(str(reverse_rate["Rate"]))

        if reverse_value == 0:
            return None, "rate_not_found"

        return {
            "baseCurrency": base_currency,
            "targetCurrency": target_currency,
            "rate": Decimal("1") / reverse_value
        }, None

    # 3. Курс через USD

    usd_to_base = get_exchange_rate(
        "USD",
        base_code
    )

    usd_to_target = get_exchange_rate(
        "USD",
        target_code
    )

    if usd_to_base is not None and usd_to_target is not None:
        base_rate = Decimal(str(usd_to_base["Rate"]))
        target_rate = Decimal(str(usd_to_target["Rate"]))

        if base_rate == 0:
            return None, "rate_not_found"

        return {
            "baseCurrency": base_currency,
            "targetCurrency": target_currency,
            "rate": target_rate / base_rate
        }, None

    return None, "rate_not_found"
