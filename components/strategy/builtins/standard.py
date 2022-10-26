import math
from typing import List

from loguru import logger

from components.strategy.strategy import Plot


def nz(x, y):
    if x == 0:
        return y
    try:
        if isinstance(x, int) or isinstance(x, float) is True:
            return x
    except:
        return y


class TechnicalAnalysis:

    @staticmethod
    def sma(data: List, period: int) -> Plot:
        """ Simple Moving Average """
        # Uses 'None' values for missing data
        logger.debug(f'Calculating SMA for {period} period')
        moving_average = []
        for i in range(len(data)):
            if i < period:
                moving_average.append(None)
            else:
                moving_average.append(sum(data[i - period:i]) / period)
        return Plot().from_list(moving_average)

    @staticmethod
    def kalman_filter(data: List, gain: int) -> Plot:
        """ Kalman Filter """
        # Uses 'None' values for missing data
        logger.debug(f'Calculating Kalman Filter with {gain} gain')
        post_src = [data[1]]
        kf = [0]
        dk = [0]
        velo = [0]
        smooth = [0]
        result = [0]

        for i in data:
            post_src.append(i)
            dk.append(post_src[-1] - nz(kf[-1], post_src[-1]))
            smooth.append(nz(kf[-1], post_src[-1]) + dk[-1] * math.sqrt((gain / 10000) * 2))
            velo.append(nz(velo[-1], 0) + (gain / 10000) * dk[-1])
            kf.append(round(smooth[-1] + velo[-1], 2))
            result.append(kf)
        kf[0] = post_src[0]
        kf.pop(0)
        kf.pop()

        return Plot().from_list(kf)
