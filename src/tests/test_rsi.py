"""Tests for the RSI calculator module."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.rsi import calculate_rsi


class TestRsi(unittest.TestCase):

    def test_first_14_entries_are_none(self):
        """First 14 entries (indices 0-13) should be None."""
        prices = [100.0 + i for i in range(20)]
        rsi = calculate_rsi(prices)
        for i in range(14):
            self.assertIsNone(rsi[i], f"RSI at index {i} should be None")
        self.assertIsNotNone(rsi[14], "RSI at index 14 should be a value")

    def test_fewer_than_15_points(self):
        """With fewer than 15 data points, all RSI values should be None."""
        for n in range(0, 15):
            prices = [100.0 + i for i in range(n)]
            rsi = calculate_rsi(prices)
            self.assertEqual(len(rsi), n)
            self.assertTrue(all(v is None for v in rsi),
                            f"All RSI should be None with {n} prices")

    def test_all_gains_rsi_100(self):
        """Monotonically increasing prices should produce RSI = 100."""
        prices = [100.0 + i * 2.0 for i in range(20)]
        rsi = calculate_rsi(prices)
        for i in range(14, len(rsi)):
            self.assertAlmostEqual(rsi[i], 100.0,
                                   msg=f"RSI at {i} should be 100 for all-gains")

    def test_all_losses_rsi_0(self):
        """Monotonically decreasing prices should produce RSI = 0."""
        prices = [200.0 - i * 2.0 for i in range(20)]
        rsi = calculate_rsi(prices)
        for i in range(14, len(rsi)):
            self.assertAlmostEqual(rsi[i], 0.0,
                                   msg=f"RSI at {i} should be 0 for all-losses")

    def test_flat_prices(self):
        """Identical prices (no change) should produce RSI = 100 by convention."""
        prices = [50.0] * 20
        rsi = calculate_rsi(prices)
        for i in range(14, len(rsi)):
            self.assertAlmostEqual(rsi[i], 100.0,
                                   msg=f"RSI at {i} should be 100 for flat prices")

    def test_output_length_matches_input(self):
        """RSI output list should have same length as input prices."""
        for n in [0, 1, 14, 15, 30, 50]:
            prices = [100.0 + i for i in range(n)]
            rsi = calculate_rsi(prices)
            self.assertEqual(len(rsi), n)

    def test_rsi_values_in_range(self):
        """All non-None RSI values should be in [0, 100]."""
        prices = [100 + (i % 7) * 3 - 10 for i in range(40)]
        rsi = calculate_rsi(prices)
        for i, v in enumerate(rsi):
            if v is not None:
                self.assertGreaterEqual(v, 0.0, f"RSI at {i} below 0")
                self.assertLessEqual(v, 100.0, f"RSI at {i} above 100")

    def test_known_values(self):
        """Verify RSI against hand-calculated values for a small known series.

        Prices: 44, 44.34, 44.09, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
                46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41,
                46.22, 45.64
        This is a classic RSI test series. We verify the first RSI value is
        reasonable (around 70) rather than exact due to floating point.
        """
        prices = [44, 44.34, 44.09, 43.61, 44.33, 44.83, 45.10, 45.42,
                  45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00,
                  46.03, 46.41, 46.22, 45.64]
        rsi = calculate_rsi(prices)
        # First RSI at index 14
        self.assertIsNotNone(rsi[14])
        # Hand-calculated: avg_gain=3.62/14, avg_loss=1.34/14, RS=2.7015, RSI≈72.98
        self.assertAlmostEqual(rsi[14], 72.98, delta=0.1)


if __name__ == "__main__":
    unittest.main()
