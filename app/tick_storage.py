import json
from decimal import Decimal
from pathlib import Path


def save_ticks_to_jsonl(
    ticks: list[dict[str, str | Decimal]], output_path: str | Path
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for tick in ticks:
            file.write(json.dumps(tick, default=str) + "\n")


def load_ticks_from_jsonl(input_path: str | Path) -> list[dict]:
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f'Path: "{path.absolute()}" does not exist')

    with path.open("r", encoding="utf-8") as file:
        ticks = []

        for row in file:
            tick = json.loads(row)
            tick["cur_price"] = Decimal(tick["cur_price"])
            tick["prev_price"] = Decimal(tick["prev_price"])
            ticks.append(tick)

        return ticks
