from datetime import date

from pydantic import BaseModel


class Transaction(BaseModel):
    iban: str
    booked_at: date
    description: str
    amount_cents: int
    balance_cents: int
    valuta_date: date
