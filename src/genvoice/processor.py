from . import db
from .schedules.invoice import Invoice, LineItem
from .schedules.bank_instructions import BankInstructions
from .schedules.address import Address
from .schedules.payment_link import PaymentLink


def get_template_data(invoice_id: int, exclude_bank_details: bool = True):
    invoice = Invoice(**db.get_invoice(invoice_id)).model_dump()  # type: ignore
    line_items = list(LineItem(**li) for li in db.get_line_items(invoice_id))  # type: ignore
    sender = Address(**db.get_sender(invoice["sender"]))  # type: ignore
    invoicee = Address(**db.get_invoicee(invoice["invoicee"]))  # type: ignore
    
    bank_instructions = None
    if not exclude_bank_details:
        bank_instructions = BankInstructions(  # type: ignore
            **db.get_bank_instructions(invoice["bank_instructions"])
        )

    payment_link = None
    if invoice.get("payment_link"):
        payment_link = PaymentLink(**db.get_payment_link(invoice["payment_link"]))  # type: ignore

    template_dict = {}

    template_dict["invoicee"] = invoicee.model_dump()
    template_dict["sender"] = sender.model_dump()
    if not exclude_bank_details:
        assert bank_instructions is not None
        template_dict["bank_instructions"] = bank_instructions.model_dump()
    template_dict["items"] = [li.model_dump() for li in line_items]

    if payment_link:
        template_dict["payment_link"] = payment_link.url

    for li in template_dict["items"]:
        li["total"] = f"${li['total']:,.2f}"

    template_dict["invoice_date"] = invoice["invoice_date"]
    template_dict["invoice_number"] = f"{invoice['invoice_id']:04d}"
    template_dict["period_start"] = invoice["period_start_date"]
    template_dict["period_end"] = invoice["period_end_date"]
    template_dict["due_date"] = invoice["due_date"]
    template_dict["total"] = f"${sum(li.total for li in line_items):,.2f}"

    return template_dict
