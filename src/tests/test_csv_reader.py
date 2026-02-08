"""Tests for the CSV reader module."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.csv_reader import read_csv


class TestCsvReader(unittest.TestCase):

    def _write_csv(self, content):
        """Helper to write a temp CSV file and return its path."""
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        f.write(content)
        f.close()
        return f.name

    def test_read_valid_csv(self):
        path = self._write_csv(
            "date,open,high,low,close,volume\n"
            "2024-01-01,100.0,105.0,99.0,103.0,1000\n"
            "2024-01-02,103.0,107.0,101.0,106.0,1200\n"
        )
        try:
            rows = read_csv(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["date"], "2024-01-01")
            self.assertAlmostEqual(rows[0]["close"], 103.0)
            self.assertAlmostEqual(rows[1]["volume"], 1200.0)
        finally:
            os.unlink(path)

    def test_numeric_fields_are_float(self):
        path = self._write_csv(
            "date,open,high,low,close,volume\n"
            "2024-01-01,100,105,99,103,1000\n"
        )
        try:
            rows = read_csv(path)
            for field in ("open", "high", "low", "close", "volume"):
                self.assertIsInstance(rows[0][field], float)
        finally:
            os.unlink(path)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            read_csv("/nonexistent/path/to/file.csv")

    def test_empty_file(self):
        path = self._write_csv("")
        try:
            with self.assertRaises(ValueError):
                read_csv(path)
        finally:
            os.unlink(path)

    def test_wrong_columns(self):
        path = self._write_csv("name,value\nfoo,123\n")
        try:
            with self.assertRaises(ValueError) as ctx:
                read_csv(path)
            self.assertIn("missing required columns", str(ctx.exception).lower())
        finally:
            os.unlink(path)

    def test_header_only_no_data(self):
        path = self._write_csv("date,open,high,low,close,volume\n")
        try:
            with self.assertRaises(ValueError):
                read_csv(path)
        finally:
            os.unlink(path)

    def test_read_sample_csv(self):
        """Verify the bundled sample data loads correctly."""
        sample = os.path.join(os.path.dirname(__file__), "..", "data", "sample.csv")
        rows = read_csv(sample)
        self.assertGreater(len(rows), 15)
        self.assertIn("date", rows[0])
        self.assertIn("close", rows[0])


if __name__ == "__main__":
    unittest.main()
