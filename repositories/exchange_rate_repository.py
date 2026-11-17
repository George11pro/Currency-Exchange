from decimal import Decimal

from database.database import get_connection


def get_all_exchange_rates():
    connection = get_connection()

    try:
        return connection.execute("""
            SELECT
                er.ID,
                er.Rate,

                bc.ID AS BaseCurrencyId,
                bc.Code AS BaseCurrencyCode,
                bc.FullName AS BaseCurrencyName,
                bc.Sign AS BaseCurrencySign,

                tc.ID AS TargetCurrencyId,
                tc.Code AS TargetCurrencyCode,
                tc.FullName AS TargetCurrencyName,
                tc.Sign AS TargetCurrencySign

            FROM ExchangeRates er

            JOIN Currencies bc
                ON er.BaseCurrencyId = bc.ID

            JOIN Currencies tc
                ON er.TargetCurrencyId = tc.ID

            ORDER BY er.ID
        """).fetchall()

    finally:
        connection.close()


def get_exchange_rate(
    base_code: str,
    target_code: str
):
    connection = get_connection()

    try:
        return connection.execute("""
            SELECT
                er.ID,
                er.Rate,

                bc.ID AS BaseCurrencyId,
                bc.Code AS BaseCurrencyCode,
                bc.FullName AS BaseCurrencyName,
                bc.Sign AS BaseCurrencySign,

                tc.ID AS TargetCurrencyId,
                tc.Code AS TargetCurrencyCode,
                tc.FullName AS TargetCurrencyName,
                tc.Sign AS TargetCurrencySign

            FROM ExchangeRates er

            JOIN Currencies bc
                ON er.BaseCurrencyId = bc.ID

            JOIN Currencies tc
                ON er.TargetCurrencyId = tc.ID

            WHERE bc.Code = ?
              AND tc.Code = ?
        """, (
            base_code,
            target_code
        )).fetchone()

    finally:
        connection.close()


def create_exchange_rate(
    base_currency_id: int,
    target_currency_id: int,
    rate: Decimal
):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO ExchangeRates (
                BaseCurrencyId,
                TargetCurrencyId,
                Rate
            )
            VALUES (?, ?, ?)
        """, (
            base_currency_id,
            target_currency_id,
            str(rate)
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def update_exchange_rate(
    base_currency_id: int,
    target_currency_id: int,
    rate: Decimal
):
    connection = get_connection()

    try:
        connection.execute("""
            UPDATE ExchangeRates
            SET Rate = ?
            WHERE BaseCurrencyId = ?
              AND TargetCurrencyId = ?
        """, (
            str(rate),
            base_currency_id,
            target_currency_id
        ))

        connection.commit()

    finally:
        connection.close()
