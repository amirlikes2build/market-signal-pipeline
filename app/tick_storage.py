import json
from decimal import Decimal
from pathlib import Path


def save_ticks_to_json(
    ticks: list[dict[str, str | Decimal]], output_path: str | Path
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(ticks, file, indent=2, default=float)


def load_ticks_from_json(input_path: str | Path) -> list[dict]:
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f'Path: "{path.absolute()}" does not exist')

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

print(load_ticks_from_json("raw_jsons/1.json"))
