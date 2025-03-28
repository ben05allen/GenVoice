# pyright: basic

from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pydantic import (
    AliasChoices,
    model_validator,
    field_validator,
    field_serializer,
    Field,
)
from typing import Any
from typing_extensions import Self

from genvoice.schedules import Base


class LineItem(Base):
    description: str
    currency: str
    quantity: Decimal
    price: Decimal
    total: Decimal | None = None

    @field_validator("quantity", "price", mode="before")
    @classmethod
    def round_decimals(cls, v: Any):
        if not isinstance(v, Decimal):
            v = Decimal(str(v))

        return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @model_validator(mode="after")
    def calculate_total(self) -> Self:
        if self.total is None:
            self.total = (self.quantity * self.price).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        return self


class Invoice(Base):
    invoice_id: int = Field(validation_alias=AliasChoices("id", "invoice_id"))
    invoice_date: date = Field(
        validation_alias=AliasChoices(
            "invoice_date",
            "date",
        )
    )
    due_date: date
    period_start_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "period_start_date",
            "start_date",
        ),
    )
    period_end_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "period_end_date",
            "end_date",
        ),
    )
    invoicee: int
    sender: int
    bank_instructions: int

    @field_serializer(
        "invoice_date",
        "due_date",
        "period_start_date",
        "period_end_date",
    )
    def serialize_dates(self, date: date | None):
        if date is not None:
            return date.strftime("%B %-d, %Y")

        return None
