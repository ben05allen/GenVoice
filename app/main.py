from datetime import datetime
from jinja2 import Template
import json
from pathlib import Path
from weasyprint import HTML

from __init__ import BASE_PATH, config
from schedules.invoice import Invoice


invoice_data_path = Path(config["invoice_data_path"])
INVOICE_DATA = json.load(open(str(invoice_data_path)))

invoice_template_path = Path(config["invoice_template_path"])
INVOICE_TEMPLATE = Template(open(str(invoice_template_path)).read())

OUT_DIR = Path(config["out_dir"])
if not OUT_DIR.exists():
    OUT_DIR.mkdir()


def main():
    parsed_data = Invoice(**INVOICE_DATA)
    rendered_html = INVOICE_TEMPLATE.render(parsed_data.model_dump())
    file_name = (
        "invoice"
        # f"_{"_".join(parsed_data.invoicee.name.split())}_"
        # f"{parsed_data.invoice_number}_"
        # f"{datetime.now().strftime("%Y%m%d%H%M%S")}"
        ".pdf"
    )

    HTML(
        string=rendered_html,
        base_url=BASE_PATH.resolve(),
    ).write_pdf(OUT_DIR / file_name)


if __name__ == "__main__":
    main()
