import os
from pathlib import Path

import pytest


TEST_DATABASE_PATH = Path(__file__).parent / "test.db"

os.environ["DATABASE_PATH"] = str(TEST_DATABASE_PATH)

from database.database import create_tables, get_connection


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_tables()

    connection = get_connection()

    try:
        connection.executemany(
            """
            INSERT INTO Currencies (
                Code,
                FullName,
                Sign
            )
            VALUES (?, ?, ?)
            """,
            [
                ("USD", "United States dollar", "$"),
                ("EUR", "Euro", "€"),
                ("RUB", "Russian ruble", "₽"),
                ("GBP", "Pound sterling", "£"),
                ("AUD", "Australian dollar", "A$"),
                ("JPY", "Japanese yen", "¥"),
            ]
        )

        connection.commit()

    finally:
        connection.close()

    yield

    if TEST_DATABASE_PATH.exists():
        TEST_DATABASE_PATH.unlink()
