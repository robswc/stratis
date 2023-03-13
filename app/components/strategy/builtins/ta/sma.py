from components.strategy import Series


def sma(data, period) -> Series:
    """Simple Moving Average"""
    return Series(data.rolling(period).mean())