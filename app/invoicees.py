from pathlib import Path
import tomllib

from schedules.address import Address


def get_invoicees(source: Path) -> dict[str, Address]:
    with source.open("rb") as f:
        invoicees = tomllib.load(f)

        return {k: Address(**v) for k, v in invoicees.items()}
