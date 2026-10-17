import csv
import io

from money_copilot.finance.models import Transaction


def _read_text(csv_path: str) -> str:
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(csv_path, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unknown encoding for {csv_path}")


def load_transactions(csv_path: str) -> list[Transaction]:
    transactions = []

    reader = csv.DictReader(io.StringIO(_read_text(csv_path)), delimiter=";")
    for row in reader:
        trs = Transaction(
            iban=row["IBAN"],
            booked_at=row["Booked At"],
            description=row["Text"],
            amount_cents=round(float(row["Credit/Debit Amount"]) * 100),
            balance_cents=round(float(row["Balance"]) * 100),
            valuta_date=row["Valuta Date"],
        )
        transactions.append(trs)
    return transactions


# transactions = load_transactions("tests/fixtures/transactions_sample.csv")
# print(transactions[0])
