# pyright: basic

from decimal import Decimal

from genvoice.schedules.invoice import Invoice, LineItem


def test_invoice_serializer():
    invoice = Invoice(
        invoice_id=1,
        invoice_date="2025-01-01",  # pyright: ignore
        due_date="2025-01-15",  # pyright: ignore
        period_start_date=None,
        invoicee=1,
        sender=2,
        bank_instructions=3,
    ).model_dump()

    assert invoice["invoice_id"] == 1
    assert invoice["invoice_date"] == "January 1, 2025"
    assert invoice["due_date"] == "January 15, 2025"
    assert invoice["period_start_date"] is None
    assert invoice["period_end_date"] is None
    assert invoice["invoicee"] == 1
    assert invoice["sender"] == 2
    assert invoice["bank_instructions"] == 3


def test_new_line_item_success():
    line_item = LineItem(
        description="New Line Item",
        currency="NZD",
        quantity=Decimal("5"),
        price=Decimal("20.00"),
        total=None,
    )

    assert line_item.description == "New Line Item"
    assert line_item.currency == "NZD"
    assert line_item.quantity == Decimal("5")
    assert line_item.price == Decimal("20.00")
    assert line_item.total == Decimal("100.00")


def test_line_item_conversions():
    line_item = LineItem(
        description="New Line Item",
        currency="NZD",
        quantity=5,  # pyright: ignore
        price=20.00,  # pyright: ignore
        total=None,
    )

    assert line_item.description == "New Line Item"
    assert line_item.currency == "NZD"
    assert line_item.quantity == Decimal("5")
    assert line_item.price == Decimal("20.00")
    assert line_item.total == Decimal("100.00")


def test_line_item_total_not_provided():
    line_item = LineItem(
        description="New Line Item",
        currency="NZD",
        quantity=5,  # pyright: ignore
        price=20.00,  # pyright: ignore
    )

    assert line_item.description == "New Line Item"
    assert line_item.currency == "NZD"
    assert line_item.quantity == Decimal("5")
    assert line_item.price == Decimal("20.00")
    assert line_item.total == Decimal("100.00")


def test_line_items_round_up():
    line_item = LineItem(
        description="New Line Item",
        currency="NZD",
        quantity=Decimal("5.015"),
        price=Decimal("5.025"),
        total=None,
    )

    assert line_item.quantity == Decimal("5.02")
    assert line_item.price == Decimal("5.03")
