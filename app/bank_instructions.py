from pathlib import Path
import tomllib

from schedules.bank_instructions import BankInstructions


def get_instructions(source: Path) -> BankInstructions:
    with source.open("rb") as f:
        instructions = tomllib.load(f)

        return BankInstructions(**instructions.get("bank_instructions"))
