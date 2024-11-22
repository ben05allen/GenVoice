from pathlib import Path
import tomllib

BASE_PATH = Path(__file__).parents[1]

with open(BASE_PATH / "pyproject.toml", "rb") as f:
    config = tomllib.load(f).get("tool", {}).get("genvoice", {})
