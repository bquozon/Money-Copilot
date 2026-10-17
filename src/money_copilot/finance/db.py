import sqlite3
from pathlib import Path

SCHEMA = """CREATE TABLE IF NOT EXISTS transactions (
    id      INTEGER     PRIMARY KEY,
    iban    TEXT    NOT NULL,
    booked_at   TEXT    NOT NULL,
    description   TEXT    NOT NULL,
    amount_cents   INTEGER     NOT NULL,
    balance_cents     INTEGER    NOT NULL,
    valuta_date     TEXT    NOT NULL,
    UNIQUE(balance_cents, amount_cents, description, booked_at));"""


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn


def delete_db(path: str) -> bool:
    try:
        Path(path).unlink()
        return True
    except FileNotFoundError:
        print("Error: the file doesn't exist")
        return False


"""
TESTS
"""
# conn = connect(":memory:")
# conn.execute(
#     "INSERT INTO transactions "
#     "(iban, booked_at, description, credit_debit_cent, balance_cent, valuta_date) "
#     "VALUES (?, ?, ?, ?, ?, ?)",
#     (
#         "CH9300762011623852957",
#         "2026-07-03",
#         "Card payment Migros Zürich HB",
#         -5683,
#         124592,
#         "2026-07-07",
#     ),
# )
# print(conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0])
