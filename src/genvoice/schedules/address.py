from pydantic import EmailStr, Field, AliasChoices

from genvoice.schedules import Base


class Address(Base):
    name: str
    contact_name: str | None = None
    street_address: str
    suburb: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "suburb",
            "district",
        ),
    )
    city: str = Field(
        validation_alias=AliasChoices(
            "city",
            "prefecture",
        )
    )
    postcode: str
    country: str
    email: EmailStr
    phone: str | None = None
