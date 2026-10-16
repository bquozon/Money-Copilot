import sqlite3

from money_copilot.finance.loader import load_transactions
from money_copilot.finance.models import Transaction


def save_transactions(conn: sqlite3.Connection, txs: list[Transaction]) -> int:
    rows = [
        (
            t.iban,
            t.booked_at.isoformat(),
            t.description,
            t.amount_cents,
            t.balance_cents,
            t.valuta_date,
        )
        for t in txs
    ]
    with conn:
        cursor = conn.executemany(
            "INSERT OR IGNORE INTO transactions (iban, booked_at, description, amount_cents, balance_cents, valuta_date) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
    return cursor.rowcount


def import_csv(conn: sqlite3.Connection, path: str) -> int:
    txs = load_transactions(path)
    return save_transactions(conn, txs)


# conn = connect(":memory:")
# print(import_csv(conn, "tests/fixtures/transactions_sample.csv"))
