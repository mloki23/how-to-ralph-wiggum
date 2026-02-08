"""Integration test: full pipeline on sample data."""

import json
import os
import subprocess
import sys
import unittest


class TestIntegration(unittest.TestCase):

    OUTPUT_FILE = "test_output_integration.json"

    def tearDown(self):
        if os.path.exists(self.OUTPUT_FILE):
            os.unlink(self.OUTPUT_FILE)

    def test_full_pipeline(self):
        """Run main.py on sample data and verify output."""
        result = subprocess.run(
            [sys.executable, "src/main.py", "src/data/sample.csv", "-o", self.OUTPUT_FILE],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

        # Output file should exist
        self.assertTrue(os.path.exists(self.OUTPUT_FILE))

        # Should be valid JSON
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        # Should be a list of records
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 15)

        # Each record has the expected keys
        for record in data:
            self.assertIn("date", record)
            self.assertIn("close", record)
            self.assertIn("rsi", record)
            self.assertIn("signal", record)

        # Should have at least one of each signal type
        signals = [r["signal"] for r in data if r["signal"] is not None]
        self.assertIn("BUY", signals, "Expected at least one BUY signal")
        self.assertIn("SELL", signals, "Expected at least one SELL signal")
        self.assertIn("HOLD", signals, "Expected at least one HOLD signal")

    def test_missing_file_error(self):
        """Running with a nonexistent CSV should fail with non-zero exit code."""
        result = subprocess.run(
            [sys.executable, "src/main.py", "/nonexistent/file.csv", "-o", self.OUTPUT_FILE],
            capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
