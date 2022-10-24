from typing import List

from loguru import logger

from components.strategy.strategy import Plot


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
