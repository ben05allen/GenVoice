from genvoice.schedules.invoice import Invoice


DATA = {
    "invoice_date": "2023-10-20",
    "period_start_date": "2023-09-01",
    "period_end_date": "2023-09-30",
    "due_date": "2023-11-05",
    "id": 4,
    "sender": 1,
    "invoicee": 1,
    "bank_instructions": 1,
}


def test_dates_are_formatted():
    inv = Invoice(**DATA).model_dump()  # type: ignore
    assert inv["period_start_date"] == "September 1, 2023"
    assert inv["period_end_date"] == "September 30, 2023"
    assert inv["invoice_date"] == "October 20, 2023"
    assert inv["due_date"] == "November 5, 2023"
    assert inv["sender"] == 1
