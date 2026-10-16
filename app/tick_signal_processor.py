from app.signal_engine import calculate_price_signal


def process_ticks_to_signals(ticks: list[dict]) -> list[dict]:

    signals = []

    for tick in ticks:
        base = calculate_price_signal(
            tick["ticker"],
            tick["prev_price"],
            tick["cur_price"],
        )
        row = {**base, "timestamp": tick["timestamp"]}

        signals.append(row)

    return signals
