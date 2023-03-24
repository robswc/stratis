import random
from typing import Union

import numpy as np
import pandas as pd
from loguru import logger

from components.ohlc.symbol import Symbol

EMPTY_DATA = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume', 'timestamp'])
EMPTY_DATA.set_index('timestamp', inplace=True)


class FutureTimestampRequested(Exception):
    def __init__(self, dataframe, index):
        super().__init__(f'Future timestamp requested. You must ensure the OHLCs resolution is set for future '
                         f'timestamp extrapolation.\n'
                         f'Dataframe length: {len(dataframe)}, index: {index}\n')


class OHLC:
    """
    OHLCV data class. This class is used to store OHLCV data.
    Wraps around a pandas dataframe.
    """

    def __init__(
            self,
            symbol: Symbol = None,
            dataframe: pd.DataFrame = None,
            resolution: Union[int, None] = None,
    ):
        self.symbol = symbol

        # if no dataframe is provided, use an empty dataframe
        if dataframe is None:
            dataframe = EMPTY_DATA
        self.dataframe = dataframe

        # if no resolution is provided, attempt to interpret it
        if resolution is None:
            try:
                self._interpret_resolution()
            except ValueError:
                logger.error(f'Unable to interpret resolution for {self.symbol}')
                self.resolution = 0
        else:
            self.resolution = resolution
        self._index = 0

        # if a dataframe is provided, validate it
        if dataframe is not None:
            self._validate()

    def _interpret_resolution(self):
        """Attempts to interpret the resolution of the OHLC data."""
        # generate a sample size that is 25% of the data
        sample_size = len(self.dataframe) // 4

        # generate a set of random indexes to sample
        indexes = random.sample(range(len(self.dataframe) - 1), sample_size)

        # take random sample pairs and calculate the difference between timestamps
        diffs = [self.dataframe.index[i + 1] - self.dataframe.index[i] for i in indexes]

        # get the most common difference, convert to minutes
        self.resolution = int(max(set(diffs), key=diffs.count) / 1000 / 60)

    def advance_index(self, n: int = 1):
        self._index += n

    def reset_index(self):
        self._index = 0

    def _get_ohlc(self, column: str, index: int = None):
        if index is None:
            index = self._index
        try:
            value = self.dataframe[column].iloc[index]
        except IndexError:
            logger.error(f'Index out of range. Index: {index}, Length: {len(self.dataframe)}')
            value = None
        return value

    @property
    def open(self):
        return self._get_ohlc('open')

    @property
    def high(self):
        return self._get_ohlc('high')

    @property
    def low(self):
        return self._get_ohlc('low')

    @property
    def close(self):
        return self._get_ohlc('close')

    @property
    def volume(self):
        return self.dataframe['volume']

    @property
    def timestamp(self):
        return self.dataframe.index[self._index]

    def get_timestamp(self, offset: int = 0):
        try:
            return self.dataframe.index[self._index + offset]
        except IndexError:
            if self._index + offset == len(self.dataframe):
                raise FutureTimestampRequested(self.dataframe, self._index + offset)

    def all(self, column: str):
        try:
            return self.dataframe[column]
        except KeyError:
            return []

    def __str__(self):
        return f'OHLC: {self.symbol}'

    def __getattr__(self, item):
        # check if the attribute is part of the class
        if item in self.__dict__:
            return self.__dict__[item]
        # else, forward the attribute to the dataframe
        else:
            return getattr(self.dataframe, item)

    def _validate(self):
        # ensure data has the correct columns
        if not {'open', 'high', 'low', 'close', 'volume'}.issubset(self.dataframe.columns):
            raise ValueError(f'Invalid data. Missing columns. Expected: open, high, low, close, volume.')

        # ensure the index of data is 'timestamp'
        if self.dataframe.index.name != 'timestamp':
            raise ValueError(f'Invalid data. Index must be named "timestamp", not "{self.dataframe.index.name}".')

    @staticmethod
    def from_csv(path: str, symbol: str):
        """
        Loads data from a csv file.
        :param symbol: symbol for the data
        :param path: Path to csv file.
        :return: self
        """

        # strategy a symbol from the symbol string
        symbol = Symbol(symbol)

        # load the data from the csv file
        dataframe = pd.read_csv(path)
        dataframe.set_index('timestamp', inplace=True)

        # create and validate OHLC object
        ohlc = OHLC(symbol=symbol, dataframe=dataframe)
        ohlc._validate()

        return ohlc

    def to_dict(self):
        df = self.dataframe.copy()
        df['time'] = df.index
        return df.to_dict(orient='records')
