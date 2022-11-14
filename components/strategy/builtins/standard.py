import math
from typing import List

from loguru import logger

from components.strategy.strategy import Plot
import pandas as pd


def nz(x, y):
    try:
        if math.isnan(x):
            return y
    except:
        return y

    if x == 0:
        return y
    try:
        if isinstance(x, int) or isinstance(x, float) is True:
            return x
    except:
        return y


def na(source, idx):
    try:
        if source[idx]:
            return False
    except:
        return True


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

    @staticmethod
    def correlation(x, y, length: int) -> Plot:
        """ Correlation Coefficient """
        logger.debug(f'Calculating Correlation for {length} period')
        length = int(length)
        data = {
            'x': x,
            'y': y}
        df = pd.DataFrame(data=data, columns=['x', 'y'])
        cc = df['x'].rolling(length).corr(df['y'])
        new = [None if math.isnan(x) else x for x in cc.tolist()]
        new.extend([None])
        return Plot().from_list(new)

    @staticmethod
    def linreg(source, period):
        def create_linear_regression(src, source_idx, length):
            ex, ey, ex2, ey2, exy = 0, 0, 0, 0, 0
            close_i = 0
            for i in range(length):
                close_i = nz(src[source_idx + (i * -1)], 0)
                ex = ex + i
                ey = ey + close_i
                ex2 = ex2 + (i * i)
                ey2 = ey2 + (close_i * close_i)
                exy = exy + (close_i * i)

            ext2 = ex ** 2
            eyt2 = ey ** 2
            # PearsonsR = (Exy - ((Ex*Ey)/period))/(sqrt(Ex2-(ExT2/period))*sqrt(Ey2-(EyT2/period)))
            a1 = (exy - ((ex * ey) / length))
            a2 = math.sqrt(ex2 - (ext2 / length))
            r = a1 / (a2 * math.sqrt(ey2 - (eyt2 / length)))
            # ExEx = Ex * Ex, slope = Ex2==ExEx ? 0.0 : (period * Exy - Ex * Ey) / (period * Ex2 - ExEx)
            exex = ex * ex
            slope = 0 if ex2 == exex else (length * exy - ex * ey) / (length * ex2 - exex)
            # linearRegression = (Ey - slope * Ex) / period
            regression = (ey - slope * ex) / length
            return regression, r

        regression_list = []
        r_list = []
        for idx in range(len(source)):
            try:
                reg, pr = create_linear_regression(source, idx, period)
            except:
                print('----->', 'ERROR AT', idx, '/', len(source))
            regression_list.append(reg)
            r_list.append(pr)

        return regression_list, r_list

    @staticmethod
    def rma(source, length):
        """ Calculate Pinescript-esque RMA """
        rma = []
        alpha = 1 / length
        for idx, i in enumerate(source):
            if idx == 0:
                rma.append(source[idx])
            else:
                rma.append((alpha * source[idx]) + (1 - alpha) * rma[idx - 1])
        return Plot().from_list(rma)

    # alpha = 1 / length
    # sum = 0.0
    # sum := na(sum[1]) ? ta.sma(src, length): alpha * src + (1 - alpha) * nz(sum[1])

    @staticmethod
    def atr(high, low, close, length):
        atr = Plot()

        # math.
        for idx in range(len(high)):
            if idx != 0:
                t1 = high[idx] - low[idx]
                t2 = abs(high[idx] - close[idx - 1])
                t3 = abs(low[idx] - close[idx - 1])
                v = max(t1, t2, t3)
            else:
                v = high[idx] - low[idx]
            atr.append(v)

        print(atr)
        smoothed_atr = TechnicalAnalysis.rma(atr, length)
        return Plot().from_list(smoothed_atr)


        # data_dict = {
        #     'high': high,
        #     'low': low,
        #     'close': close}
        # data = pd.DataFrame(data_dict, columns=['high', 'low', 'close'])
        # high = data['high']
        # low = data['low']
        # close = data['close']
        #
        # # true range
        # tr = []
        # for idx, i in enumerate(close):
        #     try:
        #         prev_close = close[idx - 1]
        #     except:
        #         prev_close = close[idx]
        #     v1 = high[idx] - low[idx]
        #     v2 = abs(high[idx] - prev_close)
        #     v3 = abs(low[idx] - prev_close)
        #     value = round(max(v1, v2, v3), 3)
        #     tr.append(value)
        # rma_values = TechnicalAnalysis.rma(tr, length)
        # rma_values.pop(0)
        # return Plot().from_list(rma_values)
