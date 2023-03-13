import inspect
import sys
from typing import List, Union

import pandas as pd
from loguru import logger
from pydantic import BaseModel

from components.ohlc import OHLC
from components.orders.order_manager import OrderManager
from components.parameter import BaseParameter, Parameter, ParameterModel
from components.strategy.decorators import extract_decorators


class StrategyModel(BaseModel):
    name: str
    parameters: List[ParameterModel]


class StrategyManager:
    _strategies = []

    @classmethod
    def register(cls, strategy):
        # check if the strategy is already registered
        if strategy in cls._strategies:
            return
        cls._strategies.append(strategy)
        logger.debug(f'Registered strategy {cls.__name__} ({strategy.__module__})')

    @classmethod
    def all(cls):
        return [s for s in cls._strategies]

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

    # each strategy gets a new order manager
    orders = OrderManager()

    objects = StrategyManager

    def __init__(self, data: Union[OHLC, None] = None):
        self.name = self.__class__.__name__
        if data is None:
            data = OHLC()
        self.data = data
        self._set_parameters()

        # register the strategy
        self.objects.register(self)

        befores, steps, afters = extract_decorators(self)
        self._before_methods = befores
        self._step_methods = steps
        self._after_methods = afters

    def as_model(self) -> StrategyModel:
        return StrategyModel(
            name=self.name,
            parameters=[p.as_model() for p in self.parameters],
        )

    def _get_all_parameters(self):
        parameters = []
        for attr in dir(self):
            if isinstance(self.__getattribute__(attr), BaseParameter):
                self.parameters.append(self.__getattribute__(attr))
            if isinstance(self.__getattribute__(attr), Parameter):
                p = self.__getattribute__(attr).value
                p.name = attr
                parameters.append(p)
        return parameters

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

    def _create_series(self):
        for attr in dir(self):
            if isinstance(self.__getattribute__(attr), list):
                sys.modules['components.strategy.series'].Series(self.__getattribute__(attr))
            if isinstance(self.__getattribute__(attr), pd.Series):
                sys.modules['components.strategy.series'].Series(self.__getattribute__(attr).to_list())

    def _get_all_series_data(self):
        series = []
        for attr in dir(self):
            if isinstance(self.__getattribute__(attr), sys.modules['components.strategy.series'].Series):
                series.append(self.__getattribute__(attr))
        return series

    def run(self, data: OHLC, parameters: dict = None):
        self._setup_data(data)
        self._create_series()

        # run before methods
        for method in self._before_methods:
            getattr(self, method)()

        # run step methods
        for i in range(len(self.data.dataframe)):
            for method in self._step_methods:
                getattr(self, method)()

            # advance the index of all series
            for s in self._get_all_series_data():
                s.advance_index()

            # advance the index of the data
            self.data.advance_index()
