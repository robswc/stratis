import math
from typing import Union

import pandas as pd

# eventually create a base series and have different types of series
class Series:
    def __init__(self, data: Union[list, pd.Series]):
        self._loop_index = 0
        self._data = data

    def advance_index(self):
        self._loop_index += 1

    def __repr__(self):
        return str(float(self))

    def __float__(self):
        if isinstance(self._data, list):
            return self._data[self._loop_index]
        if isinstance(self._data, pd.Series):
            return self._data.iloc[self._loop_index]

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
