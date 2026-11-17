from database.database import get_connection


def get_all_currencies():
    connection = get_connection()

    try:
        return connection.execute("""
            SELECT
                ID,
                Code,
                FullName,
                Sign
            FROM Currencies 
            ORDER BY ID
        """).fetchall()

    finally:
        connection.close()


def get_currency_by_code(code: str):
    connection = get_connection()

    try:
        return connection.execute("""
            SELECT
                ID,
                Code,
                FullName,
                Sign
            FROM Currencies
            WHERE Code = ?
        """, (code,)).fetchone()

    finally:
        connection.close()


def create_currency(
    code: str,
    name: str,
    sign: str
):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO Currencies (
                Code,
                FullName,
                Sign
            )
            VALUES (?, ?, ?)
        """, (
            code,
            name,
            sign
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()
