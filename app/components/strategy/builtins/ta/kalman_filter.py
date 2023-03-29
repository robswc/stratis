import math

import pandas as pd
from loguru import logger

from components.strategy import Series
import numpy as np


def kalman_filter(src: pd.Series, gain):
    src = np.array(src)
    n = len(src)
    kf = np.zeros(n)
    velo = np.zeros(n)
    smooth = np.zeros(n)
    gain_sqrt = np.sqrt(gain / 5000)

    for i in range(n):
        if i > 0:
            dk = src[i] - kf[i - 1]
        else:
            dk = src[i]
        smooth[i] = kf[i - 1] + dk * gain_sqrt if i > 0 else src[i]
        velo[i] = velo[i - 1] + (gain / 10000) * dk
        kf[i] = smooth[i] + velo[i]
    return Series(list(kf))
