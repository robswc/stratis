from typing import Union

import pandas as pd


class Series:
    def __init__(self, data: Union[list, pd.Series]):
        self._loop_index = 0
        self._data: Union[list, pd.Series] = data

    def advance_index(self):
        self._loop_index += 1

    def __float__(self):
        if isinstance(self._data, list):
            return self._data[self._loop_index]
        if isinstance(self._data, pd.Series):
            return self._data.iloc[self._loop_index]