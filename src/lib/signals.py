"""Signal generator based on RSI values."""


def generate_signal(rsi_value):
    """Generate a trading signal from an RSI value.

    Args:
        rsi_value: RSI value (float) or None if not yet available.

    Returns:
        "BUY" if RSI < 30 (strict),
        "SELL" if RSI > 70 (strict),
        "HOLD" if 30 <= RSI <= 70,
        None if RSI is None.
    """
    if rsi_value is None:
        return None
    if rsi_value < 30:
        return "BUY"
    if rsi_value > 70:
        return "SELL"
    return "HOLD"


def generate_signals(rsi_values):
    """Generate trading signals for a list of RSI values.

    Args:
        rsi_values: List of RSI values (floats or None).

    Returns:
        List of signal strings ("BUY", "SELL", "HOLD", or None).
    """
    return [generate_signal(v) for v in rsi_values]
