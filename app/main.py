from pathlib import Path
import tomllib

from get_bank_instructions import get_instructions


with open(Path(__file__).parents[1] / "config" / "config.toml", "rb") as f:
    config = tomllib.load(f)

bank_instructions_path = config["bank_instructions"]["path"]
instructions = get_instructions(Path(bank_instructions_path))


def main():
    print(instructions)


if __name__ == "__main__":
    main()
