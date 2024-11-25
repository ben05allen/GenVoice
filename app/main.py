from datetime import datetime
from jinja2 import Template
from pathlib import Path
import tomllib
from typing import Any
from weasyprint import HTML

from schedules.invoice import Invoice


BASE_PATH = Path(__file__).parents[1]


class Settings:
    def __init__(
        self,
        base_path: str | Path = BASE_PATH,
        invoice_data_path: str | Path | None = None,
        invoice_template_path: str | Path | None = None,
        out_dir: str | Path | None = None,
    ):
        self.base_path = Path(base_path) if isinstance(base_path, str) else base_path

        if invoice_data_path:
            if isinstance(invoice_data_path, str):
                invoice_data_path = Path(invoice_data_path)
            self.invoice_data_path = self.base_path / invoice_data_path

        if invoice_template_path:
            if isinstance(invoice_template_path, str):
                invoice_template_path = Path(invoice_template_path)
            self.invoice_template_path = self.base_path / invoice_template_path

        if out_dir:
            if isinstance(out_dir, str):
                out_dir = Path(out_dir)
            self.out_dir = self.base_path / out_dir
            if not self.out_dir.exists():
                self.out_dir.mkdir()

    @classmethod
    def load_tool_config(cls, base_path: str | Path) -> "Settings":
        if isinstance(base_path, str):
            base_path = Path(base_path)

        with open(base_path / "pyproject.toml", "rb") as f:
            config = tomllib.load(f).get("tool", {}).get("genvoice", {})

        return Settings(
            base_path,
            invoice_data_path=config["invoice_data_path"],
            invoice_template_path=config["invoice_template_path"],
            out_dir=config["out_dir"],
        )

    def get_invoice_data(self) -> Any:
        # return json.load(open(str(self.invoice_data_path)))
        return tomllib.load(open(str(self.invoice_data_path), "rb"))

    def get_invoice_template(self) -> Template:
        return Template(open(str(self.invoice_template_path)).read())

    @property
    def get_out_dir(self) -> Path:
        return self.out_dir

    @property
    def resolved_base_dir(self) -> str:
        return str(self.base_path.resolve())


def main():
    settings = Settings.load_tool_config(BASE_PATH)

    invoice_data = settings.get_invoice_data()
    invoice_data["items"] = invoice_data["items"].values()
    parsed_data = Invoice(**invoice_data)
    invoice_template = settings.get_invoice_template()
    rendered_html = invoice_template.render(parsed_data.model_dump())

    file_name = (
        "invoice"
        # f"_{"_".join(parsed_data.invoicee.name.split())}"
        # f"{_parsed_data.invoice_number}"
        # f"{_datetime.now().strftime("%Y%m%d%H%M%S")}"
        ".pdf"
    )

    HTML(
        string=rendered_html,
        base_url=settings.resolved_base_dir,
    ).write_pdf(settings.get_out_dir / file_name)


if __name__ == "__main__":
    main()
