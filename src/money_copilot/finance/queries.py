import calendar
from datetime import date


def _month_bounds(year: int, month: int) -> (date, date):
    _, last_day = calendar.monthrange(year, month)
    return date(year, month, 1), date(year, month, last_day)


def monthly_spending(conn, year: int, month: int) -> int:
    first_date, last_date = _month_bounds(year, month)
    total = conn.execute(
        "SELECT SUM(-amount_cents) FROM transactions "
        "WHERE booked_at BETWEEN ? AND ? AND amount_cents < 0",
        (first_date.isoformat(), last_date.isoformat()),
    ).fetchone()
    return total[0]


def monthly_income(conn, year: int, month: int) -> int:
    first_date, last_date = _month_bounds(year, month)
    total = conn.execute(
        "SELECT SUM(amount_cents) FROM transactions "
        "WHERE booked_at BETWEEN ? AND ? AND amount_cents > 0",
        (first_date.isoformat(), last_date.isoformat()),
    ).fetchone()
    return total[0]


def top_expenses(conn, year: int, month: int, n: int) -> list[tuple[str, str, int]]:
    first_date, last_date = _month_bounds(year, month)
    top = conn.execute(
        "SELECT booked_at, description, -amount_cents FROM transactions "
        "WHERE booked_at BETWEEN ? AND ? AND amount_cents < 0 "
        "ORDER BY amount_cents ASC "
        "LIMIT ?",
        (first_date.isoformat(), last_date.isoformat(), n),
    ).fetchall()
    return top


# Debugging 

# from money_copilot.finance.db import connect
# from money_copilot.finance.importer import import_csv

# conn = connect(":memory:")
# import_csv(conn, "tests/fixtures/transactions_sample.csv")
# res = top_expenses(conn, 2026, 9, 2)
# print(res)
