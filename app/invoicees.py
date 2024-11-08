from pathlib import Path
import tomllib

from schedules.invoicee import Invoicee


def get_invoicees(source: Path) -> Invoicee:
    with source.open("rb") as f:
        invoicees = tomllib.load(f)

        return {k: Invoicee(**v) for k, v in invoicees.items()}
