import pandas as pd

from components.ohlc.symbol import Symbol

EMPTY_DATA = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume', 'timestamp'])
EMPTY_DATA.set_index('timestamp', inplace=True)


class OHLC:
    """
    OHLCV data class. This class is used to store OHLCV data.
    Wraps around a pandas dataframe.
    """

    def __init__(self, symbol: Symbol = None, dataframe: pd.DataFrame = None):
        self.symbol = symbol
        if dataframe is None:
            dataframe = EMPTY_DATA
        self.dataframe = dataframe
        self._index = 0

        # if a dataframe is provided, validate it
        if dataframe is not None:
            self._validate()

    def advance_index(self, n: int = 1):
        self._index += n

    def reset_index(self):
        self._index = 0

    def _get_ohlc(self, column: str, index: int = None):
        if index is None:
            index = self._index
        value = self.dataframe[column].iloc[index]
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
        return self.dataframe.index[self._index + offset]

    def all(self, column: str):
        return self.dataframe[column]

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

    def from_csv(self, path: str, symbol: str):
        """
        Loads data from a csv file.
        :param symbol: symbol for the data
        :param path: Path to csv file.
        :return: self
        """

        # strategy a symbol from the symbol string
        self.symbol = Symbol(symbol)

        # load the data from the csv file
        self.dataframe = pd.read_csv(path)
        self.dataframe.set_index('timestamp', inplace=True)

        self._validate()

        return self

    def to_dict(self):
        df = self.dataframe.copy()
        df['time'] = df.index
        return df.to_dict(orient='records')
