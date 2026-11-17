import os
from pathlib import Path
import sqlite3


DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        Path(__file__).parent / "currency_exchange.db"
    )
)

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Currencies (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Code VARCHAR(3) NOT NULL UNIQUE,
                FullName VARCHAR(100) NOT NULL,
                Sign VARCHAR(10) NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS ExchangeRates (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                BaseCurrencyId INTEGER NOT NULL,
                TargetCurrencyId INTEGER NOT NULL,
                Rate DECIMAL(20, 10) NOT NULL,

                FOREIGN KEY (BaseCurrencyId)
                    REFERENCES Currencies(ID),

                FOREIGN KEY (TargetCurrencyId)
                    REFERENCES Currencies(ID),

                UNIQUE (BaseCurrencyId, TargetCurrencyId)
            )
        """)

        connection.commit()

    finally:
        connection.close()