# pyright: basic 

from datetime import date
from pydantic import AliasChoices, model_validator, field_serializer, Field
from typing_extensions import Self

from genvoice.schedules import Base
from .bank_instructions import BankInstructions
from .address import Address


class LineItem(Base):
    line_item_id: int = Field(validation_alias='id')
    invoice_id: int
    description: str
    currency: str
    quantity: int
    price: float
    total: float | None

    @model_validator(mode="before")
    @classmethod
    def calculate_total(cls, data):
        if isinstance(data, dict) and data.get("total") is None:
            data["total"] = data["quantity"] * data["price"]
        return data


class Invoice(Base):
    invoice_date: date
    due_date: date
    period_start_date: date | None = Field(default=None, validation_alias=AliasChoices("period_start_date", "start_date"))
    period_end_date: date | None = Field(default=None, validation_alias=AliasChoices("period_end_date", "end_date"))
    total: float | None = None
    invoice_number: str = Field(validation_alias="id")
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
