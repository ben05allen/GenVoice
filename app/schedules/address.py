from pydantic import EmailStr

from . import BaseModel


class Address(BaseModel):
    name: str
    street_address: str
    district: str | None = None
    city: str
    post_code: str
    country: str
    email: EmailStr
    phone_number: str | None = None
