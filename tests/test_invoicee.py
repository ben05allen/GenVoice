from pydantic import ValidationError
import pytest

from genvoice.schedules.address import Address


def test_invoicee():
    Address(
        name="John Doe",
        phone="+1234567890",
        street_address="123 Main St",
        suburb="Westside",
        city="Anytown",
        postcode="90001",
        country="USA",
        email="john.doe@example.com",
    )


def test_invoice_with_bad_email_raises():
    with pytest.raises(ValidationError):
        Address(
            name="John Doe",
            phone="+1234567890",
            street_address="123 Main St",
            district="Westside",  # type: ignore
            city="Anytown",
            postcode="90001",
            country="USA",
            email="john.doe.example.com",
        )
