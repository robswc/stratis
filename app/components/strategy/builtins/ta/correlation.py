from typing import List, Union

import numpy as np
import pandas as pd

from components.strategy import Series


def correlation_coefficient(x: Union[List[float], Series], y: Union[List[float], Series], period: int) -> Series:
    """ Calculate the correlation coefficient between two lists """
    if len(x) != len(y):
        raise ValueError("Input arrays must have the same length")

    if len(x) < period:
        raise ValueError("Period must be less than or equal to the length of input arrays")

    x = np.asarray(x)
    y = np.asarray(y)

    result = np.zeros(len(x) - period + 1)

    # calculate the rolling sums for both x and y.
    x_sum = np.cumsum(x)
    y_sum = np.cumsum(y)

    # calculate the rolling sums for x * y, x^2, and y^2.
    xy_sum = np.cumsum(x * y)
    x2_sum = np.cumsum(x**2)
    y2_sum = np.cumsum(y**2)

    for i in range(len(result)):
        if i == 0:
            x_sum_window = x_sum[period - 1]
            y_sum_window = y_sum[period - 1]
            xy_sum_window = xy_sum[period - 1]
            x2_sum_window = x2_sum[period - 1]
            y2_sum_window = y2_sum[period - 1]
        else:
            x_sum_window = x_sum[i + period - 1] - x_sum[i - 1]
            y_sum_window = y_sum[i + period - 1] - y_sum[i - 1]
            xy_sum_window = xy_sum[i + period - 1] - xy_sum[i - 1]
            x2_sum_window = x2_sum[i + period - 1] - x2_sum[i - 1]
            y2_sum_window = y2_sum[i + period - 1] - y2_sum[i - 1]

        # Calculate the correlation coefficient for the current window.
        numerator = period * xy_sum_window - x_sum_window * y_sum_window
        denominator = np.sqrt((period * x2_sum_window - x_sum_window**2) * (period * y2_sum_window - y_sum_window**2))
        result[i] = numerator / denominator

    pad_size = period - 1
    result = np.pad(result, (pad_size, 0), mode='constant', constant_values=np.nan)
    return Series(list(result))