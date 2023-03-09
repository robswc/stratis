from typing import List

from components.ohlc import OHLC
from components.baseparameter import BaseParameter


class Strategy:

    parameters: List[BaseParameter] = []

    def __init__(self):
        self.name = self.__class__.__name__

    def __str__(self):
        return self.name

    def set_parameters(self):
        raise NotImplementedError

    def run(self, data: OHLC):
        raise NotImplementedError