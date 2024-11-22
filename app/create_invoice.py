from pathlib import Path
import tomllib

from bank_instructions import get_instructions
from invoicees import get_invoicees


BASE_PATH = Path(__file__).parents[1]


class Details:
    def __init__(
        self,
        base_path: str | Path,
        invoicees_path: str | Path | None = None,
        bank_instructions_path: str | Path | None = None,
    ):
        if isinstance(base_path, str):
            base_path = Path(base_path)
        self.base_path = base_path

        if isinstance(invoicees_path, str):
            invoicees_path = base_path / invoicees_path
        self.invoicees_path = invoicees_path

        if isinstance(bank_instructions_path, str):
            bank_instructions_path = base_path / bank_instructions_path
        self.bank_instructions_path = bank_instructions_path

    @classmethod
    def load_tool_config(cls, base_path: str | Path):
        if isinstance(base_path, str):
            base_path = Path(base_path)

        with open(base_path / "pyproject.toml", "rb") as f:
            config = tomllib.load(f).get("tool", {}).get("genvoice", {})

        bank_instructions_path = config["bank_instructions_path"]
        invoicees_path = config["invoicees_path"]

        return cls(
            base_path,
            invoicees_path=invoicees_path,
            bank_instructions_path=bank_instructions_path,
        )


# TODO: Generate JSON for customer invoice
def main():
    details = Details.load_tool_config(BASE_PATH)

    instructions = get_instructions(details.bank_instructions_path)

    invoicees = get_invoicees(details.invoicees_path)


if __name__ == "__main__":
    main()
