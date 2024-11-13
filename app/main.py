from jinja2 import Template
from pathlib import Path
import tomllib

from bank_instructions import get_instructions
from invoicees import get_invoicees

with open(Path(__file__).parents[1] / "pyproject.toml", "rb") as f:
    config = tomllib.load(f).get("tool", {}).get("genvoice", {})

bank_instructions_path = Path(config["bank_instructions_path"])
INSTRUCTIONS = get_instructions(bank_instructions_path)

invoicees_path = Path(config["invoicees_path"])
INVOICEES = get_invoicees(invoicees_path)

invoice_template_path = Path(config["invoice_template_path"])
INVOICE_TEMPLATE = Template(open(str(invoice_template_path)).read())


def main():
    data = {
        "invoice_date": "2023-10-20",
        "period_from": "2023-09-01",
        "period_to": "2023-09-30",
        "due_date": "2023-11-05",
        "total": 50.00,
        "invoice_number": "1",
        "sender": {
            "name": "Joe Bloggs",
            "street_address": "123 Main St",
            "district": "Anywhere",
            "city": "Anytown",
            "post_code": "12345",
            "country": "USA",
            "email": "joe.bloggs@example.com",
        },
        "invoicee": {
            "name": "Jane Smith",
            "street_address": "123 Main St",
            "district": "Anywhere",
            "city": "Anytown",
            "post_code": "12345",
            "country": "USA",
            "email": "jane.smith@example.com",
        },
        "bank_instructions": {
            "bank_name": "abc bank",
            "branch_name": "Main Branch",
            "branch_code": "123",
            "swift_bic_code": "ABC123",
            "recipient_type": "Savings",
            "bank_code": "123",
            "account_number": "12_3456_7890",
            "account_type": "Savings",
        },
        "items": [
            {"description": "sprockets", "quantity": 1, "price": 10.00, "total": 10.00},
            {"description": "widgets", "quantity": 2, "price": 20.00, "total": 40.00},
        ],
    }

    rendered_html = INVOICE_TEMPLATE.render(data)

    with open("data/index.html", "w") as f:
        f.write(rendered_html)


if __name__ == "__main__":
    main()
