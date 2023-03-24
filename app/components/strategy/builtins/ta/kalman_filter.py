import math

import pandas as pd
from loguru import logger

from components.strategy import Series

import numpy as np


def kalman_filter(src: pd.Series, gain):
    src = list(src)
    kf = np.zeros(len(src))
    velo = np.zeros(len(src))
    smooth = np.zeros(len(src))
    for i in range(len(src)):
        dk = src[i] - kf[i-1] if i > 0 else src[i]
        smooth[i] = kf[i-1] + dk * np.sqrt((gain / 10000) * 2)
        velo[i] = velo[i-1] + ((gain / 10000) * dk)
        kf[i] = smooth[i] + velo[i]
    return Series(list(kf))

