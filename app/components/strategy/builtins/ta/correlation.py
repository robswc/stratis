import numpy as np
import pandas as pd

from components.strategy import Series


def correlation_coefficient(x: Series, y: Series, period: int) -> Series:
    """ Calculate the correlation coefficient between two lists """
    if len(x) != len(y):
        raise ValueError("Input arrays must have the same length")

    if len(x) < period:
        raise ValueError("Period must be less than or equal to the length of input arrays")

    x = np.asarray(x.as_list())
    y = np.asarray(y.as_list())

    result = np.zeros(len(x) - period + 1)

    for i in range(len(result)):
        x_window = x[i:i + period]
        y_window = y[i:i + period]
        result[i] = np.corrcoef(x_window, y_window)[0, 1]

    pad_size = period - 1
    result = np.pad(result, (pad_size, 0), mode='constant', constant_values=np.nan)

    return Series(list(result))
