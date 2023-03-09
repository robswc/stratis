import pandas as pd

from components.symbol import Symbol


class OHLC:
    """
    OHLCV data class. This class is used to store OHLCV data.
    Wraps around a pandas dataframe.
    """

    def __init__(self):
        self.symbol = None
        self.dataframe = None

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

        # create a symbol from the symbol string
        self.symbol = Symbol(symbol)

        # load the data from the csv file
        self.dataframe = pd.read_csv(path)
        self.dataframe.set_index('timestamp', inplace=True)

        self._validate()

        return self