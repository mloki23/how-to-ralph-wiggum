"""Simple Trading Signal Generator - Main entry point."""

import argparse
import sys
import os

# Add src directory to path so lib modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.csv_reader import read_csv
from lib.rsi import calculate_rsi
from lib.signals import generate_signals
from lib.json_writer import write_json


def main():
    parser = argparse.ArgumentParser(description="Generate trading signals from CSV data")
    parser.add_argument("csv_path", nargs="?", default="src/data/sample.csv",
                        help="Path to input CSV file (default: src/data/sample.csv)")
    parser.add_argument("-o", "--output", default="output.json",
                        help="Output JSON file path (default: output.json)")
    args = parser.parse_args()

    try:
        # Read CSV data
        data = read_csv(args.csv_path)
        print(f"Read {len(data)} rows from {args.csv_path}")

        # Extract close prices and calculate RSI
        close_prices = [row["close"] for row in data]
        rsi_values = calculate_rsi(close_prices)

        # Generate signals
        signals = generate_signals(rsi_values)

        # Build output records
        records = []
        for i, row in enumerate(data):
            records.append({
                "date": row["date"],
                "close": row["close"],
                "rsi": round(rsi_values[i], 2) if rsi_values[i] is not None else None,
                "signal": signals[i],
            })

        # Write output
        write_json(records, args.output)
        print(f"Wrote {len(records)} records to {args.output}")

        # Print summary
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        hold_count = signals.count("HOLD")
        none_count = signals.count(None)
        print(f"Signals: {buy_count} BUY, {sell_count} SELL, {hold_count} HOLD, {none_count} pending")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
