"""Tests for the JSON writer module."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.json_writer import write_json


class TestJsonWriter(unittest.TestCase):

    def test_writes_valid_json(self):
        records = [
            {"date": "2024-01-01", "close": 100.0, "rsi": 45.5, "signal": "HOLD"},
            {"date": "2024-01-02", "close": 102.0, "rsi": 72.3, "signal": "SELL"},
        ]
        path = tempfile.mktemp(suffix=".json")
        try:
            write_json(records, path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["signal"], "HOLD")
            self.assertEqual(data[1]["close"], 102.0)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_output_structure(self):
        records = [
            {"date": "2024-01-01", "close": 100.0, "rsi": None, "signal": None},
        ]
        path = tempfile.mktemp(suffix=".json")
        try:
            write_json(records, path)
            with open(path) as f:
                data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertIn("date", data[0])
            self.assertIn("close", data[0])
            self.assertIn("rsi", data[0])
            self.assertIn("signal", data[0])
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_none_values_become_null(self):
        """None RSI/signal should be written as JSON null."""
        records = [
            {"date": "2024-01-01", "close": 100.0, "rsi": None, "signal": None},
        ]
        path = tempfile.mktemp(suffix=".json")
        try:
            write_json(records, path)
            with open(path) as f:
                raw = f.read()
            self.assertIn("null", raw)
            data = json.loads(raw)
            self.assertIsNone(data[0]["rsi"])
            self.assertIsNone(data[0]["signal"])
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_indent_formatting(self):
        """Output should use indent=2 for readability."""
        records = [{"date": "2024-01-01", "close": 100.0, "rsi": 50.0, "signal": "HOLD"}]
        path = tempfile.mktemp(suffix=".json")
        try:
            write_json(records, path)
            with open(path) as f:
                raw = f.read()
            # indent=2 means lines like '  "date": ...'
            self.assertIn('  "date"', raw)
        finally:
            if os.path.exists(path):
                os.unlink(path)


if __name__ == "__main__":
    unittest.main()
