from money_copilot.finance.db import connect
from money_copilot.finance.importer import import_csv


def test_import_is_idempotent():
    conn = connect(":memory:")
    assert import_csv(conn, "tests/fixtures/transactions_sample.csv") == 89
    assert import_csv(conn, "tests/fixtures/transactions_sample.csv") == 0
