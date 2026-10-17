import inspect
import json
from contextlib import closing
from datetime import date

from money_copilot.agent.types import ToolCall
from money_copilot.finance.db import connect
from money_copilot.finance.queries import (
    monthly_income,
    monthly_spending,
    range_income,
    range_spending,
    top_expenses,
    top_incomes,
)

TOOLS = {}
SCHEMAS = []
DB_PATH = "data/money.db"

PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}


def tool(func):
    params = inspect.signature(func).parameters
    SCHEMAS.append(
        {
            "type": "function",
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": {
                    n: {"type": PY_TO_JSON[p.annotation]} for n, p in params.items()
                },
                "required": list(params),
                "additionalProperties": False,
            },
            "strict": True,
        }
    )
    TOOLS[func.__name__] = func
    return func


def run_tool(call: ToolCall) -> str:
    if call.name not in TOOLS:
        return f"Error: unknown tool '{call.name}'"
    try:
        result = TOOLS[call.name](**call.arguments)
    except TypeError as e:
        return f"Error: bad argument: {e}"
    return json.dumps(result)


@tool
def add(x: int, y: int):
    """
    Adds two numbers together
    """
    print(f"Tool add was called and returned {x + y} ")
    return x + y


@tool
def get_range_spending(start_date: str, end_date: str) -> str:
    """
    Total amount spent (debits) between start_date and end_date, both inclusive,
    formatted YYYY-MM-DD. Returns CHF.
    """
    try:
        start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
    except ValueError:
        return "Error: dates must be in YYYY-MM-DD format"
    with closing(connect(DB_PATH)) as conn:
        cents = range_spending(conn, start, end) or 0
    return f"{cents / 100:.2f}"


@tool
def get_range_income(start_date: str, end_date: str) -> str:
    """
    Total amount gained (credits) between start_date and end_date, both inclusive,
    formatted YYYY-MM-DD. Returns CHF.
    """
    try:
        start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
    except ValueError:
        return "Error: dates must be in YYYY-MM-DD format"
    with closing(connect(DB_PATH)) as conn:
        cents = range_income(conn, start, end) or 0
    return f"{cents / 100:.2f}"


@tool
def get_monthly_spending(year: int, month: int) -> str:
    """
    Total amount spent (Debits) during given month and of given year, both ints.
    Returns CHF.
    """
    if month > 12 or month < 1:
        return "Error: month value must be between 1 and 12 included"
    with closing(connect(DB_PATH)) as conn:
        cents = monthly_spending(conn, year, month) or 0
    print(f"{cents / 100:.2f}")
    return f"{cents / 100:.2f}"


@tool
def get_monthly_income(year: int, month: int) -> str:
    """
    Total amount gained (Credits) during given month and of given year, both ints.
    Returns CHF.
    """
    if month > 12 or month < 1:
        return "Error: month value must be between 1 and 12 included"
    with closing(connect(DB_PATH)) as conn:
        cents = monthly_income(conn, year, month) or 0
    return f"{cents / 100:.2f}"


@tool
def get_top_expenses(year: int, month: int, n: int) -> str:
    """
    Top n expenses of given month and of given year, all 3 are ints.
    Returns CHF.
    """
    if n < 1:
        return "Error: n must be at least 1"
    if month > 12 or month < 1:
        return "Error: month value must be between 1 and 12 included"
    result = f"Top {n} expenses : \n"
    with closing(connect(DB_PATH)) as conn:
        top = top_expenses(conn, year, month, n)

    if not top:
        return "No expenses this month."
    for e in top:
        res = f"Booked at date : {e[0]}, Description: {e[1]}, Amount (CHF): {e[2] / 100:.2f} \n"
        result += res

    return result


@tool
def get_top_incomes(year: int, month: int, n: int) -> str:
    """
    Top n incomes of given month and of given year, all 3 are ints.
    Returns CHF.
    """
    if n < 1:
        return "Error: n must be at least 1"
    if month > 12 or month < 1:
        return "Error: month value must be between 1 and 12 included"
    result = f"Top {n} incomes : \n"
    with closing(connect(DB_PATH)) as conn:
        top = top_incomes(conn, year, month, n)
    if not top:
        return "No incomes this month."
    for e in top:
        res = f"Booked at date : {e[0]}, Description: {e[1]}, Amount (CHF): {e[2] / 100:.2f} \n"
        result += res

    return result
