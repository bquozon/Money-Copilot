from money_copilot.finance.db import connect
from money_copilot.finance.importer import import_csv
from money_copilot.finance.queries import monthly_income, monthly_spending, top_expenses


def test_monthly_spending():
    conn = connect(":memory:")
    import_csv(conn, "tests/fixtures/transactions_sample.csv")
    assert monthly_spending(conn, 2026, 9) == 364349


def test_monthly_income():
    conn = connect(":memory:")
    import_csv(conn, "tests/fixtures/transactions_sample.csv")
    res = monthly_income(conn, 2026, 9) == 585000
    assert res


def test_top_expenses():
    conn = connect(":memory:")
    import_csv(conn, "tests/fixtures/transactions_sample.csv")
    res = top_expenses(conn, 2026, 9, 2) == [
        ("2026-09-01", "Rent Wohnbau AG Zürich", 145000),
        ("2026-09-15", "Savings transfer to CH56 0483 5012 3456 7800 9", 50000),
    ]
    assert res
