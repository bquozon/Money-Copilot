import csv

from money_copilot.finance.models import Transaction


def load_transactions(csv_path: str) -> list[Transaction]:
    transactions = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

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
