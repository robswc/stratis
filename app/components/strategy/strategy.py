import inspect
import sys
from typing import List, Union

from loguru import logger

from components.ohlc import OHLC
from components.parameter import BaseParameter, Parameter
from components.strategy.decorators import extract_decorators

class StrategyManager:

    _strategies = []

    @classmethod
    def register(cls, strategy):
        cls._strategies.append(strategy)
        logger.debug(f'Registered strategy {strategy.name} ({strategy.__module__})')

    @classmethod
    def all(cls):
        return cls._strategies

    @classmethod
    def get(cls, name):
        for s in cls._strategies:
            if s.name == name:
                return s
        raise Exception(f'No strategy found with name {name}')

class BaseStrategy:
    parameters: List[BaseParameter] = []
    _loop_index = 0

    # strategy decorators
    _step_methods = []
    _before_methods = []
    _after_methods = []

    objects = StrategyManager

    def __init__(self):
        self.name = self.__class__.__name__
        self.data: Union[OHLC, None] = None
        self._set_parameters()

        befores, steps, afters = extract_decorators(self)
        self._before_methods = befores
        self._step_methods = steps
        self._after_methods = afters

        # register the strategy
        self.objects.register(self)

    def _set_parameters(self):
        # find all parameters in the class
        for attr in dir(self):
            if isinstance(self.__getattribute__(attr), BaseParameter):
                self.parameters.append(self.__getattribute__(attr))
            if isinstance(self.__getattribute__(attr), Parameter):
                p = self.__getattribute__(attr).value
                p.name = attr
                self.parameters.append(p)

    def show_parameters(self):
        return '\n'.join([str(p) for p in self.parameters])

    def _setup_data(self, data: OHLC):
        self.data = data

    def run(self, data: OHLC, parameters: dict = None):
        self._setup_data(data)

        # run before methods
        for method in self._before_methods:
            getattr(self, method)()

        # run step methods
        for i in range(len(self.data.dataframe)):
            for method in self._step_methods:
                getattr(self, method)()
            self.data.advance_index()