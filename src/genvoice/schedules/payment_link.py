from decimal import ROUND_HALF_UP, Decimal

from pydantic import field_validator

from genvoice.schedules import Base


class PaymentLink(Base):
    id: int
    currency: str
    amount: Decimal
    url: str

    @field_validator("amount", mode="before")
    @classmethod
    def round_decimals(cls, v: float | Decimal | str) -> Decimal:
        if not isinstance(v, Decimal):
            v = Decimal(str(v))

        return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
