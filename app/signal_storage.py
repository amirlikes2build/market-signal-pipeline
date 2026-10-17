import json
from decimal import Decimal
from pathlib import Path


def save_signals_to_jsonl(
    signals: list[dict[str, str | Decimal]], output_path: str | Path
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for signal in signals:
            file.write(json.dumps(signal, default=str) + "\n")


def load_signals_from_jsonl(input_path: str | Path) -> list[dict]:
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f'Path: "{path.absolute()}" does not exist')

    with path.open("r", encoding="utf-8") as file:
        signals = []

        for row in file:
            signal = json.loads(row)
            signal["cur_price"] = Decimal(signal["cur_price"])
            signal["prev_price"] = Decimal(signal["prev_price"])
            signal["price_change"] = Decimal(signal["price_change"])
            signal["price_change_pct"] = Decimal(signal["price_change_pct"])
            signals.append(signal)

        return signals
