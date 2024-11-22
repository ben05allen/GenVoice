from pathlib import Path
import tomllib

from bank_instructions import get_instructions
from invoicees import get_invoicees


BASE_PATH = Path(__file__).parents[1]
with open(BASE_PATH / "pyproject.toml", "rb") as f:
    config = tomllib.load(f).get("tool", {}).get("genvoice", {})

bank_instructions_path = Path(config["bank_instructions_path"])
INSTRUCTIONS = get_instructions(bank_instructions_path)

invoicees_path = Path(config["invoicees_path"])
INVOICEES = get_invoicees(invoicees_path)

# TODO: Generate JSON for customer invoice
