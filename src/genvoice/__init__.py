import argparse
from datetime import datetime
from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

from .processor import get_template_data


def arg_parser():
    parser = argparse.ArgumentParser(description="Create PDF invoices")
    parser.add_argument(
        "--invoice", "-i", required=True, help="Invoice number", type=int
    )
    parser.add_argument(
        "--template", "-t", required=True, help="Path to invoice template"
    )
    parser.add_argument(
        "--destination", "-d", help="Destination path of PDF", default="."
    )

    parser.add_argument(
        "--no_bank_details", "-n", help="Omit bank details from invoice", action="store_true"
    )

    return parser


def main():
    args = arg_parser().parse_args()

    invoice_template_path = Path(args.template)
    destination = Path(args.destination)

    if not destination.exists():
        destination.mkdir()

    if destination.is_dir():
        file_name = (
            f"invoice_{args.invoice}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        )

        destination /= file_name

    exclude_bank_details = args.no_bank_details
    template_dict = get_template_data(args.invoice, exclude_bank_details=exclude_bank_details)
    invoice_template = Template(open(str(invoice_template_path.resolve())).read())
    rendered_html = invoice_template.render(template_dict)

    HTML(string=rendered_html).write_pdf(str(destination.resolve()))
