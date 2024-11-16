from datetime import date
from pydantic import model_validator, field_serializer

from . import BaseModel
from bank_instructions import BankInstructions
from address import Address


class LineItem(BaseModel):
    description: str
    quantity: int
    price: float
    total: float | None

    @model_validator(mode="before")
    @classmethod
    def calculate_total(cls, data):
        if isinstance(data, dict) and data.get("total") is None:
            data["total"] = data["quantity"] * data["price"]
        return data


class Invoice(BaseModel):
    invoice_date: date
    period_from: date
    period_to: date
    due_date: date
    total: float
    invoice_number: str
    invoicee: Address
    sender: Address
    bank_instructions: BankInstructions
    items: list[LineItem]

    @field_serializer("invoice_date", "period_from", "period_to", "due_date")
    def serialize_date(self, date: date, _info):
        return date.strftime("%d/%m/%Y")
