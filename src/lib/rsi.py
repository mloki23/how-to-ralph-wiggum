"""RSI (Relative Strength Index) calculator using Wilder's smoothing method."""


def calculate_rsi(close_prices, period=14):
    """Calculate 14-period RSI using Wilder's smoothing.

    Args:
        close_prices: List of closing prices (floats).
        period: RSI period (default 14).

    Returns:
        List of RSI values (same length as close_prices).
        First `period` entries are None (not enough data).
        First valid RSI is at index `period` (needs period+1 prices).
    """
    n = len(close_prices)

    # Need at least period+1 prices to compute one RSI value
    if n < period + 1:
        return [None] * n

    # Calculate price changes
    changes = [close_prices[i] - close_prices[i - 1] for i in range(1, n)]

    gains = [max(c, 0.0) for c in changes]
    losses = [abs(min(c, 0.0)) for c in changes]

    rsi_values = [None] * period  # First `period` entries have no RSI

    # First averages: simple mean of first `period` values
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Compute RSI for the first valid point (index `period`)
    rsi_values.append(_compute_rsi(avg_gain, avg_loss))

    # Subsequent values use Wilder's smoothing
    for i in range(period, len(changes)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period
        rsi_values.append(_compute_rsi(avg_gain, avg_loss))

    return rsi_values


def _compute_rsi(avg_gain, avg_loss):
    """Compute RSI from average gain and loss.

    Edge cases:
        - avg_loss == 0 and avg_gain > 0: RSI = 100 (all gains)
        - avg_gain == 0 and avg_loss > 0: RSI = 0 (all losses)
        - Both zero (flat prices): RSI = 100 by convention
    """
    if avg_loss == 0:
        return 100.0
    if avg_gain == 0:
        return 0.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))
