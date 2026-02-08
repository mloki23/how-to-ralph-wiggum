"""CSV reader module for trading data files."""

import csv

EXPECTED_COLUMNS = {"date", "open", "high", "low", "close", "volume"}


def read_csv(filepath):
    """Read a CSV file with OHLCV trading data.

    Args:
        filepath: Path to the CSV file.

    Returns:
        List of dicts with keys: date (str), open, high, low, close, volume (float).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or has wrong columns.
    """
    try:
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                raise ValueError(f"CSV file is empty: {filepath}")

            actual_columns = set(reader.fieldnames)
            missing = EXPECTED_COLUMNS - actual_columns
            if missing:
                raise ValueError(
                    f"CSV missing required columns: {sorted(missing)}. "
                    f"Found: {sorted(actual_columns)}"
                )

            rows = []
            for row in reader:
                rows.append({
                    "date": row["date"],
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"]),
                })

            if not rows:
                raise ValueError(f"CSV file has no data rows: {filepath}")

            return rows
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
