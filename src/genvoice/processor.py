# pyright: basic

from . import db
from .schedules.invoice import Invoice, LineItem
from .schedules.bank_instructions import BankInstructions
from .schedules.address import Address


def get_template_data(invoice_id: int):
    invoice = Invoice(**db.get_invoice(invoice_id))
    line_items = list(LineItem(**li) for li in db.get_line_items(invoice_id))
    sender = Address(**db.get_sender(invoice.sender))
    invoicee = Address(**db.get_invoicee(invoice.invoicee))
    bank_instructions = BankInstructions(
        **db.get_bank_instructions(invoice.bank_instructions)
    )

    template_dict = {}

    template_dict["invoicee"] = invoicee.model_dump()
    template_dict["sender"] = sender.model_dump()
    template_dict["bank_instructions"] = bank_instructions.model_dump()
    template_dict["items"] = [li.model_dump() for li in line_items]
    for li in template_dict["items"]:
        li["total"] = f"${li['total']:,.2f}"

    template_dict["invoice_date"] = invoice.invoice_date
    template_dict["invoice_number"] = invoice.invoice_id
    template_dict["due_date"] = invoice.due_date
    template_dict["total"] = f"${sum(li.total for li in line_items):,.2f}"

    return template_dict
