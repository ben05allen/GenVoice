from pydantic import ValidationError
import pytest

from schedules.address import Address


def test_invoicee():
    Address(
        name="John Doe",
        phone_number="+1234567890",
        street_address="123 Main St",
        district="Westside",
        city="Anytown",
        post_code="90001",
        country="USA",
        email="john.doe@example.com",
    )


def test_invoice_with_bad_email_raises():
    with pytest.raises(ValidationError):
        Address(
            name="John Doe",
            phone_number="+1234567890",
            street_address="123 Main St",
            district="Westside",
            city="Anytown",
            post_code="90001",
            country="USA",
            email="john.doe.example.com",
        )
