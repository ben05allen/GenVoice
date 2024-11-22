from pathlib import Path

from . import config
from bank_instructions import get_instructions
from invoicees import get_invoicees


bank_instructions_path = Path(config["bank_instructions_path"])
INSTRUCTIONS = get_instructions(bank_instructions_path)

invoicees_path = Path(config["invoicees_path"])
INVOICEES = get_invoicees(invoicees_path)
