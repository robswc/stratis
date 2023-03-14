import inspect
import sys
from typing import List, Union

import pandas as pd
from loguru import logger
from pydantic import BaseModel

from components.manager.manager import ComponentManager
from components.ohlc import OHLC
from components.orders.order_manager import OrderManager
from components.parameter import BaseParameter, Parameter, ParameterModel
from components.strategy.decorators import extract_decorators

class StrategyManager(ComponentManager):
    _components = []

class StrategyModel(BaseModel):
    name: str
    parameters: List[ParameterModel]

class BaseStrategy:
    objects = StrategyManager

    @classmethod
    def register(cls):
        cls.objects.register(cls)

    def __init__(self, data: Union[OHLC, None] = None):
        self.name = self.__class__.__name__
        if data is None:
            data = OHLC()
        self.data = data
        self.parameters: List[BaseParameter] = []
        self._set_parameters()

        self.register()

        self._loop_index = 0

        # strategy decorators
        self._step_methods = []
        self._before_methods = []
        self._after_methods = []

        befores, steps, afters = extract_decorators(self)
        self._before_methods = befores
        self._step_methods = steps
        self._after_methods = afters

        # each strategy gets a new order manager
        self.orders = OrderManager()

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
