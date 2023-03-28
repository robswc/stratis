import math
from typing import Union

import pandas as pd
from loguru import logger


class EndOfData(Exception):
    pass


# eventually create a base series and have different types of series
class Series:
    def __init__(self, data: Union[list, pd.Series], name: str = None):
        self._loop_index = 0
        self._data = data
        self.name = name

    def advance_index(self):
        if self._loop_index + 1 == len(self._data):
            raise EndOfData(
                f'End of data reached ({self.name}). Index: {self._loop_index}, Length: {len(self._data)}, Data:'
                f' {self._data[-5:]}'
            )
        self._loop_index += 1

    def as_list(self):
        if isinstance(self._data, list):
            return self._data
        if isinstance(self._data, pd.Series):
            df = self._data.copy()
            # replace NaN with previous value
            df.fillna(method='backfill', inplace=True)
            return df.tolist()

    def __repr__(self):
        return str(float(self))

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        if isinstance(self._data, list):
            return self._data[item]
        if isinstance(self._data, pd.Series):
            return self._data.iloc[item]

    def __float__(self):
        try:
            if isinstance(self._data, list):
                return self._data[self._loop_index]
            if isinstance(self._data, pd.Series):
                return self._data.iloc[self._loop_index]
        except IndexError:
            logger.error(f'Index out of range. Index: {self._loop_index}, Length: {len(self._data)}')

    def shift(self, n=1):
        if isinstance(self._data, list):
            return self._data[self._loop_index - n]
        if isinstance(self._data, pd.Series):
            return self._data.iloc[self._loop_index - n]

    def __int__(self):
        return int(float(self))

    def __add__(self, other):
        return float(self) + other

    def __sub__(self, other):
        return float(self) - other

    def __mul__(self, other):
        return float(self) * other

    def __truediv__(self, other):
        return float(self) / other

    def __floordiv__(self, other):
        return float(self) // other

    def __mod__(self, other):
        return float(self) % other

    def __pow__(self, other):
        return float(self) ** other

    def __lt__(self, other):
        return float(self) < other

    def __le__(self, other):
        return float(self) <= other

    def __eq__(self, other):
        return float(self) == other

    def __ne__(self, other):
        return float(self) != other

    def __gt__(self, other):
        return float(self) > other

    def __ge__(self, other):
        return float(self) >= other

    def __and__(self, other):
        return float(self) and other

    def __or__(self, other):
        return float(self) or other

    def __neg__(self):
        return -float(self)

    def __pos__(self):
        return +float(self)

    def __abs__(self):
        return abs(float(self))

    def __invert__(self):
        return ~float(self)

    def __round__(self, n=None):
        return round(float(self), n)

    def __trunc__(self):
        return math.trunc(float(self))

    def __floor__(self):
        return math.floor(float(self))

    def __ceil__(self):
        return math.ceil(float(self))

    def __index__(self):
        return float(self)

    def __radd__(self, other):
        return other + float(self)

    def __rsub__(self, other):
        return other - float(self)

    def __rmul__(self, other):
        return other * float(self)

    def __rtruediv__(self, other):
        return other / float(self)
