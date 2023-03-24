import numpy as np

from components.strategy import Series


def atr(high: Series, low: Series, close: Series, period: int = 12) -> Series:
    """ Calculate the average true range """

    high = np.array(high)
    low = np.array(low)
    close = np.array(close)

    if len(high) != len(low) != len(close):
        raise ValueError("Input lists must have the same length")

    if len(high) < period:
        raise ValueError("Input lists must have at least 'period' number of elements")

    true_range = []

    for i in range(1, len(high)):
        tr = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
        true_range.append(tr)

    result = []

    for i in range(period, len(true_range) + 1):
        average = np.mean(true_range[i - period: i])
        result.append(average)

    return Series(result)
