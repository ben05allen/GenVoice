from datetime import date
from pydantic import model_validator, field_serializer
from typing_extensions import Self

from . import BaseModel
from .bank_instructions import BankInstructions
from .address import Address


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
    due_date: date
    total: float | None = None
    invoice_number: str
    invoicee: Address
    sender: Address
    bank_instructions: BankInstructions
    items: list[LineItem]

    @field_serializer("invoice_date", "due_date")
    def serialize_dates(self, date: date):
        return date.strftime("%B %d, %Y")

    @model_validator(mode="after")
    def total_invoices(self) -> Self:
        self.total = sum(item.price * item.quantity for item in self.items)
        return self
