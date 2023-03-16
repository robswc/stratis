import inspect
import json
import sys
from typing import List, Union

import pandas as pd
from loguru import logger
from pydantic import BaseModel

from components.backtest.backtest import Backtest
from components.manager.manager import ComponentManager
from components.ohlc import OHLC
from components.orders.order_manager import OrderManager
from components.orders.position_manager import PositionManager
from components.parameter import BaseParameter, Parameter, ParameterModel
from components.strategy.decorators import extract_decorators

class PlotConfig(BaseModel):
    color: str = 'blue'
    type: str = 'line'
    lineWidth: int = 1

class Plot:
    def __init__(self, series: 'Series', **kwargs):
        self.data = series.as_list()
        self.name = kwargs.get('name', None)
        self.config = PlotConfig(**kwargs)

    def as_dict(self):
        return {
            'name': self.name,
            'data': self.data,
            'config': self.config.dict()
        }

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

        # handle data
        if data is None:
            data = OHLC()
        self.data = data
        self._loop_index = 0

        # create a shortcut to the symbol
        print(self.data.symbol)
        self.symbol = data.symbol

        # handle parameters
        self.parameters: List[BaseParameter] = []
        self._set_parameters()

        self.register()


        # strategy decorators
        self._step_methods = []
        self._before_methods = []
        self._after_methods = []

        befores, steps, afters = extract_decorators(self)
        self._before_methods = befores
        self._step_methods = steps
        self._after_methods = afters

        # each strategy gets a new order and position manager
        self.orders = OrderManager(self)  # eventually all orders will be converted to positions
        self.positions = PositionManager(self)

        # each strategy gets plots
        self.plots = []

    def export_plots(self, plots: List[Plot]):
        self.plots = plots


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
                if attr not in ['_before_methods', '_step_methods', '_after_methods', 'parameters']:
                    sys.modules['components.strategy.series'].Series(self.__getattribute__(attr))
            if isinstance(self.__getattribute__(attr), pd.Series):
                sys.modules['components.strategy.series'].Series(self.__getattribute__(attr).to_list())

    def _get_all_series_data(self):
        series = []
        for attr in dir(self):
            if isinstance(self.__getattribute__(attr), sys.modules['components.strategy.series'].Series):
                series.append(self.__getattribute__(attr))
        return series

    def _get_all_plots(self):
        # will use in the future to get all plots
        plots = []
        for attr in dir(self):
            if isinstance(self.__getattribute__(attr), Plot):
                plots.append(self.__getattribute__(attr))
        return plots

    def run(self, data: OHLC, parameters: dict = None, **kwargs):

        # set parameters
        if parameters is not None:
            for p in self.parameters:
                if p.name in parameters:
                    p.value = parameters[p.name]

        self.__init__(data=data)
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

        # handle backtest
        b = Backtest(strategy=self, data=data)

        # runs the backtest
        b.test()

        # run after methods
        for method in self._after_methods:
            getattr(self, method)()

        # get all plots
        plots = self.plots

        if kwargs.get('plots', False):
            logger.debug(f'Requested plots, found {len(plots)}')
            return b.result, plots
        return b.result


