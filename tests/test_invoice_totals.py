# pyright: basic

from genvoice.schedules.invoice import Invoice


DATA = {
    "invoice_date": "2023-10-20",
    "period_from": "2023-09-01",
    "period_to": "2023-09-30",
    "due_date": "2023-11-05",
    "id": 4,
    "sender": {
        "name": "Joe Bloggs",
        "street_address": "123 Main St",
        "district": "Anywhere",
        "city": "Anytown",
        "postcode": "12345",
        "country": "USA",
        "email": "joe.bloggs@example.com",
    },
    "invoicee": {
        "name": "Jane Smith",
        "street_address": "123 Main St",
        "district": "Anywhere",
        "city": "Anytown",
        "postcode": "12345",
        "country": "USA",
        "email": "jane.smith@example.com",
    },
    "bank_instructions": {
        "bank_name": "abc bank",
        "branch": "Main Branch",
        "branch_code": "123",
        "swift_bic_code": "ABC123",
        "recipient_type": "Private",
        "bank_code": "123",
        "account_number": "12_3456_7890",
        "account_type": "Futsuu",
    },
    "items": [
        {
            "id": 1,
            "invoice_id": 4,
            "description": "sprockets",
            "currency": "USD",
            "quantity": 1,
            "price": 10.00,
        },
        {
            "id": 2,
            "invoice_id": 4,
            "description": "widgets",
            "currency": "USD",
            "quantity": 2,
            "price": 20.556,
        },
    ],
}


def test_totals_add_up():
    inv = Invoice(**DATA)
    assert inv.total == 1 * 10 + 2 * 20.556
