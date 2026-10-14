import json
from decimal import Decimal

import pytest

from app.tick_batch_generator import generate_market_ticks
from app.tick_storage import load_ticks_from_jsonl, save_ticks_to_jsonl

TEST_TICKS_INPUT = {
    "AMD": Decimal("608.10"),
    "NVDA": Decimal("229.28"),
}


@pytest.fixture
def ticks():
    return generate_market_ticks(TEST_TICKS_INPUT, 10)


@pytest.fixture
def saved_ticks_file(tmp_path, ticks):
    output_path = tmp_path / "test_tick_output.jsonl"

    save_ticks_to_jsonl(ticks, output_path)

    return output_path


def test_save_creates_file(saved_ticks_file):
    assert saved_ticks_file.exists()


def test_number_of_lines_equals_number_of_ticks(saved_ticks_file, ticks):
    lines = saved_ticks_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == len(ticks)


def test_each_line_is_valid_json(saved_ticks_file):
    lines = saved_ticks_file.read_text(encoding="utf-8").splitlines()

    for line in lines:
        loaded_line = json.loads(line)
        assert isinstance(loaded_line, dict)


def test_load_returns_same_number_of_records(saved_ticks_file, ticks):
    loaded_ticks = load_ticks_from_jsonl(saved_ticks_file)

    assert len(loaded_ticks) == len(ticks)


def test_loaded_price_fields_come_back_as_decimal(saved_ticks_file):
    loaded_ticks = load_ticks_from_jsonl(saved_ticks_file)

    first_tick = loaded_ticks[0]

    assert isinstance(first_tick["prev_price"], Decimal)
    assert isinstance(first_tick["cur_price"], Decimal)


def test_missing_file_raises_file_not_found_error(tmp_path):
    missing_path = tmp_path / "missing.jsonl"

    with pytest.raises(FileNotFoundError):
        load_ticks_from_jsonl(missing_path)
