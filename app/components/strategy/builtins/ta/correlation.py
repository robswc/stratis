import numpy as np

from components.strategy import Series


def correlation_coefficient(x: Series, y: Series, period: int) -> Series:
    """ Calculate the correlation coefficient between two lists """
    x = np.array(x)
    y = np.array(y)

    # Calculate the correlation coefficient
    return Series(np.corrcoef(x, y)[0, 1])
