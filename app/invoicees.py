from pathlib import Path
import tomllib

from app.schedules.address import Invoicee


def get_invoicees(source: Path) -> Invoicee:
    with source.open("rb") as f:
        invoicees = tomllib.load(f)

        return {k: Invoicee(**v) for k, v in invoicees.items()}
