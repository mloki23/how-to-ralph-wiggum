"""JSON writer module for trading signal output."""

import json


def write_json(records, filepath="output.json"):
    """Write signal records to a JSON file.

    Args:
        records: List of dicts with keys: date, close, rsi, signal.
        filepath: Output file path (default: output.json).
    """
    with open(filepath, "w") as f:
        json.dump(records, f, indent=2)
