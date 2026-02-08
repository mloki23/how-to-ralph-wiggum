"""Tests for the signal generator module."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.signals import generate_signal, generate_signals


class TestSignals(unittest.TestCase):

    def test_buy_below_30(self):
        self.assertEqual(generate_signal(29.99), "BUY")
        self.assertEqual(generate_signal(0.0), "BUY")
        self.assertEqual(generate_signal(10.0), "BUY")

    def test_sell_above_70(self):
        self.assertEqual(generate_signal(70.01), "SELL")
        self.assertEqual(generate_signal(100.0), "SELL")
        self.assertEqual(generate_signal(85.0), "SELL")

    def test_hold_in_range(self):
        self.assertEqual(generate_signal(50.0), "HOLD")
        self.assertEqual(generate_signal(30.0), "HOLD")
        self.assertEqual(generate_signal(70.0), "HOLD")
        self.assertEqual(generate_signal(45.0), "HOLD")

    def test_boundary_30_is_hold(self):
        """RSI exactly 30.0 should be HOLD, not BUY (strict less-than)."""
        self.assertEqual(generate_signal(30.0), "HOLD")

    def test_boundary_70_is_hold(self):
        """RSI exactly 70.0 should be HOLD, not SELL (strict greater-than)."""
        self.assertEqual(generate_signal(70.0), "HOLD")

    def test_boundary_29_99_is_buy(self):
        self.assertEqual(generate_signal(29.99), "BUY")

    def test_boundary_70_01_is_sell(self):
        self.assertEqual(generate_signal(70.01), "SELL")

    def test_none_rsi_gives_none_signal(self):
        self.assertIsNone(generate_signal(None))

    def test_generate_signals_list(self):
        rsi_values = [None, None, 25.0, 50.0, 75.0]
        signals = generate_signals(rsi_values)
        self.assertEqual(signals, [None, None, "BUY", "HOLD", "SELL"])

    def test_extreme_values(self):
        self.assertEqual(generate_signal(0.0), "BUY")
        self.assertEqual(generate_signal(100.0), "SELL")


if __name__ == "__main__":
    unittest.main()
