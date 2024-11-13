from pathlib import Path
import tomllib

from bank_instructions import get_instructions
from invoicees import get_invoicees

with open(Path(__file__).parents[1] / "pyproject.toml", "rb") as f:
    config = tomllib.load(f).get("tool", {}).get("genvoice", {})

bank_instructions_path = config["bank_instructions_path"]
INSTRUCTIONS = get_instructions(Path(bank_instructions_path))

invoicees_path = config["invoicees_path"]
INVOICEES = get_invoicees(Path(invoicees_path))


def main():
    print(INVOICEES)


if __name__ == "__main__":
    main()
